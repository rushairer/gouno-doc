#!/usr/bin/env python3
"""Read-only independent verification for the November 2026 release train.

No signing, deployment, production access, certification or staging claims.
Existing version tags and release workflows must already be successful.
"""
import argparse,base64,hashlib,json,os,re,pathlib,subprocess,time,urllib.request,urllib.parse
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--tag',required=True);p.add_argument('--sha',required=True);p.add_argument('--out',required=True);p.add_argument('--workflow',required=True);p.add_argument('--images',required=True);a=p.parse_args();assert a.repo in ['rushairer/gosso','rushairer/gosso-admin','rushairer/gouno-blog'];assert re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+',a.tag);assert re.fullmatch(r'[0-9a-f]{40}',a.sha)
root=pathlib.Path(a.out);root.mkdir(parents=True,exist_ok=True)
def api(path):
 r=subprocess.run(['gh','api',path],capture_output=True,timeout=90);r.check_returncode();return r.stdout
def read(url,headers=None):
 for n in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers=headers or {}),timeout=45) as r:return r.read()
  except Exception:
   if n==3:raise
   time.sleep(2)
def hashcheck(data,digest):
 assert 'sha256:'+hashlib.sha256(data).hexdigest()==digest,'content hash mismatch'
ref=json.loads(api(f'repos/{a.repo}/git/ref/tags/{a.tag}'));assert ref['object']['type']=='tag';annotated=json.loads(api(f'repos/{a.repo}/git/tags/{ref["object"]["sha"]}'));assert annotated['object']['type']=='commit' and annotated['object']['sha']==a.sha
release=json.loads(api(f'repos/{a.repo}/releases/tags/{a.tag}'));assert not release['draft'] and not release['prerelease'];(root/'release.json').write_text(json.dumps(release,indent=2))
runs=json.loads(api(f'repos/{a.repo}/actions/runs?per_page=50'))['workflow_runs']
published=[r for r in runs if r['head_sha']==a.sha and r['head_branch']==a.tag and r['path'].endswith('/'+a.workflow)]
assert published and published[0]['status']=='completed' and published[0]['conclusion']=='success','Tagged publication workflow has not succeeded'
assets=[]
for asset in release['assets']:
 name=asset['name'];assert pathlib.PurePath(name).name==name
 data=subprocess.run(['gh','api','-H','Accept: application/octet-stream',f"repos/{a.repo}/releases/assets/{asset['id']}"],capture_output=True,check=True,timeout=120).stdout
 (root/name).write_bytes(data)
 if asset.get('digest'):hashcheck(data,asset['digest'])
 assets.append({'name':name,'sha256':hashlib.sha256(data).hexdigest(),'api_digest_verified':bool(asset.get('digest'))})
if a.repo=='rushairer/gosso':
 repo='rushairer/gosso'
 token=json.loads(read('https://ghcr.io/token?'+urllib.parse.urlencode({'service':'ghcr.io','scope':f'repository:{repo}:pull'})))['token']
 index=read(f'https://ghcr.io/v2/{repo}/manifests/{a.tag}',{'Authorization':'Bearer '+token,'Accept':'application/vnd.oci.image.index.v1+json'})
 (root/'gosso.digest.txt').write_text('ghcr.io/rushairer/gosso@sha256:'+hashlib.sha256(index).hexdigest()+'\n')
results=[]
for item in a.images.split(','):
 kind,image=item.split('=',1); ref=(root/(kind+'.digest.txt')).read_text().strip();assert ref.startswith(image+'@sha256:');digest=ref.split('@')[1];repo=image.removeprefix('ghcr.io/')
 sboms=[]
 for asset in assets:
  name=asset['name']
  if (('sbom-'+kind+'-'+a.sha+'.') in name or name.startswith(kind+'.') or name.startswith(kind+'-sbom.')) and name.endswith('.json'):
   body=json.loads((root/name).read_bytes());fmt='SPDX' if body.get('spdxVersion','').startswith('SPDX-') else body.get('bomFormat');assert fmt in ['SPDX','CycloneDX'];sboms.append(fmt)
 assert {'SPDX','CycloneDX'}<=set(sboms),('missing SBOM',kind)
 if kind in ['gosso','backend','seed']:
  matched=[]
  for asset in assets:
   name=asset['name']
   if ((('sbom-'+kind+'-'+a.sha+'.') in name) or name.startswith(kind+'-sbom.')) and ('cyclonedx' in name or '.cdx.' in name):
    sbom=json.loads((root/name).read_bytes())
    for component in sbom.get('components',[]):
     if component.get('name')=='stdlib':matched.append(component.get('version'))
  assert matched and all(v in ['go1.27.4','1.27.4'] for v in matched),('unpatched/missing Go compiler SBOM',kind,matched)

 token=json.loads(read('https://ghcr.io/token?'+urllib.parse.urlencode({'service':'ghcr.io','scope':f'repository:{repo}:pull'})))['token'];headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json'}
 def blob(typ,dgst):
  data=read(f'https://ghcr.io/v2/{repo}/{typ}/{dgst}',headers);hashcheck(data,dgst);return data
 indexdata=blob('manifests',digest);hashcheck(read(f'https://ghcr.io/v2/{repo}/manifests/{a.tag}',headers),digest);index=json.loads(indexdata);(root/(kind+'-index.json')).write_bytes(indexdata)
 identity=f'https://github.com/{a.repo}/.github/workflows/{a.workflow}@refs/tags/{a.tag}'
 verify=subprocess.run([os.environ.get('COSIGN_BINARY','cosign'),'verify','--certificate-identity',identity,'--certificate-oidc-issuer','https://token.actions.githubusercontent.com',ref],capture_output=True,timeout=120)
 (root/(kind+'-cosign.json')).write_bytes(verify.stdout);(root/(kind+'-cosign.log')).write_bytes(verify.stderr);verify.check_returncode();signed=json.loads(verify.stdout);assert signed
 if kind=='gosso':
  att=subprocess.run([os.environ.get('COSIGN_BINARY','cosign'),'verify-attestation','--type','cyclonedx','--certificate-identity',identity,'--certificate-oidc-issuer','https://token.actions.githubusercontent.com',ref],capture_output=True,timeout=120)
  (root/'gosso-sbom-attestation.json').write_bytes(att.stdout);(root/'gosso-sbom-attestation.log').write_bytes(att.stderr);att.check_returncode()
  envelope=json.loads(att.stdout);statement=json.loads(base64.b64decode(envelope['payload']))
  assert any(x.get('digest',{}).get('sha256')==digest.split(':')[1] for x in statement['subject'])
  assert statement['predicate']==json.loads((root/'gosso-sbom.cdx.json').read_bytes()),'signed SBOM predicate differs from release attachment'

 platforms={x['platform']['architecture']:x for x in index['manifests'] if x.get('platform',{}).get('os')=='linux' and x['platform']['architecture'] in ['amd64','arm64']};assert set(platforms)=={'amd64','arm64'}
 proofs=[]
 for arch,desc in platforms.items():
  attest=[x for x in index['manifests'] if x.get('annotations',{}).get('vnd.docker.reference.type')=='attestation-manifest' and x['annotations'].get('vnd.docker.reference.digest')==desc['digest']];assert len(attest)==1
  man=json.loads(blob('manifests',attest[0]['digest']));layers=[x for x in man['layers'] if x.get('annotations',{}).get('in-toto.io/predicate-type','').startswith('https://slsa.dev/provenance/')];assert len(layers)==1
  data=blob('blobs',layers[0]['digest']);stmt=json.loads(data);pred=stmt['predicate'];assert any(x.get('digest',{}).get('sha256')==desc['digest'].split(':')[1] for x in stmt['subject'])
  expected='https://github.com/'+a.repo
  if stmt['predicateType']=='https://slsa.dev/provenance/v1':
   vcs=pred['runDetails']['metadata']['buildkit_metadata']['vcs'];assert vcs['source']==expected and vcs['revision']==a.sha
   request=pred['buildDefinition']['externalParameters']['request'];args=request['args'];rargs=request['root']['request']['args'];assert rargs['vcs:source']==expected and rargs['vcs:revision']==a.sha
   
   if a.repo!='rushairer/gosso':assert args['label:org.opencontainers.image.source']==expected and args['label:org.opencontainers.image.revision']==a.sha
   fields='BuildKit metadata and root request args' if a.repo=='rushairer/gosso' else 'BuildKit metadata, root request args and OCI labels'
   qualifier=f'Local-directory build: declared VCS source/revision cross-checked in {fields}; not a Git material content-hash claim.'
  else:
   assert any(a.repo in x.get('uri','') and a.sha in x.get('digest',{}).values() for x in pred.get('materials',[]));qualifier='Exact Git material source SHA verified.'
  (root/f'{kind}-provenance-{arch}.json').write_bytes(data);proofs.append({'arch':arch,'digest':desc['digest'],'source_sha':a.sha,'qualification':qualifier})
 results.append({'kind':kind,'image':ref,'tag_resolves_to_digest':True,'cosign_identity':identity,'cosign_verified':True,'sbom_formats':sboms,'platforms':proofs})
receipt={'repo':a.repo,'tag':a.tag,'sha':a.sha,'release_url':release['html_url'],'assets':assets,'images':results,'manual_certification':('not applicable to backend' if a.repo=='rushairer/gosso' else 'not verified; maintainer publication exception'),'staging':'not verified; maintainer publication exception','production_deployed':False}
if a.repo=='rushairer/gosso':
 source=a.sha
 info=json.loads(read('https://proxy.golang.org/github.com/rushairer/gosso/@v/v1.7.2.info'));assert info['Version']=='v1.7.2';assert info['Origin']['Hash']==source;(root/'go-proxy-info.json').write_text(json.dumps(info,indent=2))
 mod=read('https://proxy.golang.org/github.com/rushairer/gosso/@v/v1.7.2.mod');assert b'go 1.26.11' in mod and b'github.com/rushairer/gouno v1.4.0' in mod;(root/'go-proxy.mod').write_bytes(mod)
 repo='rushairer/gosso/charts/gosso';token=json.loads(read('https://ghcr.io/token?'+urllib.parse.urlencode({'service':'ghcr.io','scope':f'repository:{repo}:pull'})))['token'];h={'Authorization':'Bearer '+token,'Accept':'application/vnd.oci.image.manifest.v1+json'}
 data=read(f'https://ghcr.io/v2/{repo}/manifests/1.7.2',h);manifest=json.loads(data);(root/'helm-manifest.json').write_bytes(data)
 layers=[x for x in manifest['layers'] if x['mediaType']=='application/vnd.cncf.helm.chart.content.v1.tar+gzip'];assert len(layers)==1;digest=layers[0]['digest'];archive=read(f'https://ghcr.io/v2/{repo}/blobs/{digest}',h);assert 'sha256:'+hashlib.sha256(archive).hexdigest()==digest
 with __import__('tarfile').open(fileobj=__import__('io').BytesIO(archive),mode='r:gz') as t:
  chart=t.extractfile('gosso/Chart.yaml').read().decode();assert '\nversion: 1.7.2\n' in '\n'+chart and '\nappVersion: 1.7.2\n' in chart.replace('"','');(root/'helm-chart.yaml').write_text(chart)
 helm_receipt={'source_sha':source,'public_go_proxy_verified':True,'helm_oci_verified':True,'helm_manifest_digest':'sha256:'+hashlib.sha256(data).hexdigest(),'helm_chart_blob_digest':digest};(root/'helm-module-verification.json').write_text(json.dumps(helm_receipt,indent=2));receipt['helm_module']=helm_receipt
receipt['publication_workflow']={'id':published[0]['id'],'url':published[0]['html_url'],'sha':a.sha};receipt['independent_verifier']={'repo':os.environ.get('GITHUB_REPOSITORY'),'source_sha':os.environ.get('GITHUB_SHA'),'run_id':os.environ.get('GITHUB_RUN_ID')}
(root/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print('GOUNO_VERIFICATION_JSON='+json.dumps(receipt,separators=(',',':')));print(json.dumps({'release':release['html_url'],'images':[x['image'] for x in results],'verified':True}))
