#!/usr/bin/env python3
"""Restore only source edits from an alias reconciliation, preserving entry fixes."""
from datetime import datetime
import io
import json
from pathlib import Path
import sys
import tarfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
import apply_native_review as migration
ROOT=migration.ROOT


def main():
    report=json.loads(Path(sys.argv[1]).read_text())
    assert report['applied']
    editions=sorted((r['edition'] for r in report['editions']),key=len,reverse=True)
    configs={e:json.loads((ROOT/e/'native.json').read_text()) for e in editions}
    manifests={e:json.loads((ROOT/e/'native-generated.json').read_text()) for e in editions}
    stamp=datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup=ROOT/'build/localization-round2'/('before-context-restore-'+stamp+'.tar.gz')
    touched=set();changed=0
    with tarfile.open(str(backup),'w:gz') as saved, tarfile.open(report['backup'],'r|gz') as original:
        for member in original:
            edition=next((e for e in editions if member.name.startswith(e+'/')),None)
            if edition is None:continue
            relative=member.name[len(edition)+1:];config=configs[edition]
            if not (relative.startswith(config['source']+'/') or (relative.startswith('native-java/') and relative.endswith('.java'))):continue
            path=ROOT/member.name
            data=original.extractfile(member).read();prior=path.read_bytes()
            assert migration.sha(prior)==manifests[edition][relative], 'Preserving edited source: '+str(path)
            if data==prior:continue
            info=tarfile.TarInfo(member.name);info.size=len(prior);info.mode=path.stat().st_mode&0o777
            saved.addfile(info,io.BytesIO(prior))
            path.write_bytes(data);path.chmod(member.mode)
            manifests[edition][relative]=migration.sha(data);touched.add(edition);changed+=1
        for edition in sorted(touched):
            path=ROOT/edition/'native-generated.json';prior=path.read_bytes()
            info=tarfile.TarInfo(str(path.relative_to(ROOT)));info.size=len(prior);info.mode=path.stat().st_mode&0o777
            saved.addfile(info,io.BytesIO(prior));path.write_bytes(migration.encoded(manifests[edition]))
    result={'source_report':sys.argv[1],'backup':str(backup),'editions':len(touched),'source_files_restored':changed,
            'scope':'Only owned source and native Java launcher content restored. Corrected native-launch.sh entry references and current metadata retained.'}
    (ROOT/'build/localization-round2/context-restore.json').write_bytes(migration.encoded(result));print(json.dumps(result,indent=2))


if __name__=='__main__':main()
