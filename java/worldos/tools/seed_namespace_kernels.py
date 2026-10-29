#!/usr/bin/env python3
"""Prove old source snapshots before caching unchanged ARM64 build inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'native'))
from verify_country_boots import atomic_json, digest, kernel_input_digest, PROBE_VERSION


def freeze_images():
    cache=ROOT/'build/native/country-boots/equal-source-kernels/namespace-baselines'
    count=0
    for path in sorted(cache.glob('*.json')):
        evidence=json.loads(path.read_text())
        expected=evidence['origin_pass_report']['kernel_sha256']
        image=ROOT/evidence['image']
        assert image.is_file() and digest(image)==expected,'Baseline image changed: '+str(image)
        target=path.with_suffix('.img')
        if not target.is_file() or digest(target)!=expected:
            temporary=target.with_suffix('.img.new')
            shutil.copyfile(str(image),str(temporary))
            assert digest(temporary)==expected,'Baseline image changed during copying'
            temporary.replace(target)
        evidence['image']=str(target.relative_to(ROOT))
        atomic_json(path,evidence)
        count+=1
    print('Immutable baseline image copies:',count,flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archives', nargs='*', type=Path, help='Earliest backups first; retain original archives')
    parser.add_argument('--freeze-images',action='store_true',help='Freeze already proved baseline images without re-reading source backups')
    args = parser.parse_args()
    if args.freeze_images:
        freeze_images();return
    if not args.archives:parser.error('Provide source backups or --freeze-images')
    snapshots, truncated = {}, []
    roots={p.parent.name:json.loads(p.read_text()) for p in (ROOT/'country').glob('*/native.json')}
    for archive in args.archives:
        try:
            with tarfile.open(str(archive), 'r|gz') as stream:
                for entry in stream:
                    parts = Path(entry.name).parts
                    if len(parts)<3 or parts[0]!='country' or len(parts[1])!=3 or not entry.isfile():
                        continue
                    if parts[1] not in roots:
                        continue
                    # Only representative editions. Child metadata resides one
                    # component deeper; source roots come from their root config.
                    root_config = roots[parts[1]]
                    if parts[2] not in ('native.json','native-generated.json',root_config['source']):
                        continue
                    value = stream.extractfile(entry).read()
                    if len(value)!=entry.size:
                        raise EOFError('Incomplete backup member')
                    snapshots.setdefault(entry.name, value)
        except (EOFError, tarfile.ReadError) as error:
            # An interrupted writer may lack a gzip trailer. Already complete
            # members are usable only if the full baseline SHA subsequently
            # matches the prior passed report exactly.
            truncated.append({'archive':str(archive),'error':str(error)})
    results=[]
    cache=ROOT/'build/native/country-boots/equal-source-kernels/namespace-baselines'
    cache.mkdir(parents=True,exist_ok=True)
    for path in sorted((ROOT/'country').glob('*/native.json')):
        folder=path.parent
        prior=ROOT/'build/native/country-boots'/folder.name/'report.json'
        row={'country':folder.name,'seeded':False}
        try:
            proof=json.loads(prior.read_text())
            assert proof.get('passed') and proof.get('probe_version')==PROBE_VERSION
            config=json.loads(snapshots.get(str(path.relative_to(ROOT)),path.read_bytes()))
            def read(name):
                relative=str((folder/config['source']/name).relative_to(ROOT))
                if relative in snapshots:
                    return snapshots[relative]
                return (ROOT/relative).read_bytes()
            reconstructed=hashlib.sha256()
            for name in sorted(config['owned_files']):
                reconstructed.update(name.encode());reconstructed.update(read(name))
            source_hash=reconstructed.hexdigest()
            current=json.loads(path.read_text())
            if source_hash!=proof['source_sha256']:
                # A language may already have a newer successful boot. Accept
                # its live snapshot only when the complete digest matches.
                from verify_country_boots import source_digest
                assert source_digest(folder,current)==proof['source_sha256'],'Baseline snapshot does not match old boot proof'
                config=current
                read=lambda name:(folder/config['source']/name).read_bytes()
                source_hash=proof['source_sha256']
            assert config['vendor_sha256']==current['vendor_sha256'],'Dependency changed'
            image=folder/current['source']/current['native']/'build/kernel8.img'
            if not image.is_file() or digest(image)!=proof['kernel_sha256']:
                image=ROOT/'build/native/country-boots/equal-source-kernels'/(source_hash+'-'+config['vendor_sha256']+'.img')
            assert image.is_file() and digest(image)==proof['kernel_sha256'],'Prior image is unavailable'
            key=kernel_input_digest(config,read)
            record={'kernel_input_sha256':key,'reconstructed_source_sha256':source_hash,
                    'origin_pass_report':proof,'vendor_sha256':config['vendor_sha256'],
                    'image':str(image.relative_to(ROOT)),
                    'scope':'Prior full-source snapshot reconstructed from backups and verified byte-for-byte against a passed boot proof. Only equal conservative ARM64 build inputs may reuse compilation.'}
            target=cache/(key+'-'+config['vendor_sha256']+'.json')
            if not target.exists():atomic_json(target,record)
            row.update(seeded=True,kernel_input_sha256=key,source_sha256=source_hash)
        except (AssertionError,KeyError,OSError,ValueError) as error:
            row['reason']=str(error)
        results.append(row)
    report={'seeded':sum(r['seeded'] for r in results),'countries':len(results),
            'archives':[str(p) for p in args.archives],'incomplete_archive_trailers':truncated,'results':results}
    atomic_json(ROOT/'build/localization-round2/namespace-kernel-baselines.json',report)
    freeze_images()
    print('Verified reconstructed baseline snapshots:',report['seeded'],'/',len(results),flush=True)


if __name__=='__main__':main()
