#!/usr/bin/env python3
"""Check ip.conf wiring and owned-file integrity for every native edition."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    edits = json.loads((ROOT/'native/inputs/ip-config-update.json').read_text())['files']
    canonical = (ROOT/'tools/ip_config.py').read_bytes()
    results = []
    for metadata in sorted((ROOT/'country').glob('*/native.json'))+sorted((ROOT/'country').glob('*/*/native.json')):
        config = json.loads(metadata.read_text()); folder = metadata.parent
        mapping = config['identifiers']; source = folder/config['source']
        def local(name):
            parts = []
            for part in name.split('/'):
                stem, dot, suffix = part.partition('.')
                parts.append(mapping.get(stem,stem)+dot+suffix)
            return '/'.join(parts)
        manifest = json.loads((folder/'native-generated.json').read_text())
        checked = 0
        for item in edits:
            name = item['path']
            path = folder/'native-java'/(mapping.get('국가실행기','국가실행기')+'.java') if name=='launcher.java' else source/local(name)
            data=path.read_bytes();relative=str(path.relative_to(folder))
            assert hashlib.sha256(data).hexdigest()==manifest[relative],str(path)
            assert path.stat().st_nlink==1,str(path)
            if name.endswith('.py'):ast.parse(data.decode(),filename=str(path))
            checked+=1
        helper=source/'platforms/rpi4-native/tools/ip_config.py'
        assert helper.read_bytes()==canonical,str(helper)
        assert 'ip.conf' in config['owned_files']
        assert 'platforms/rpi4-native/tools/ip_config.py' in config['owned_files']
        for path in (helper,source/'ip.conf',metadata):
            assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest[str(path.relative_to(folder))],str(path)
        bridge=(source/local('platforms/rpi4-native/도구/통신다리.py')).read_text()
        network=(source/local('platforms/rpi4-native/통신망/통신망.c')).read_text()
        assert 'Guest forward address must be 10.0.2.1..254' not in bridge,str(source)
        assert 'dhcp_start(' not in network,str(source)
        assert all(macro in network for macro in ('IP_CONFIG_IP','IP_CONFIG_NETMASK','IP_CONFIG_GATEWAY'))
        launcher=(folder/'native-java'/(mapping.get('국가실행기','국가실행기')+'.java')).read_text()
        assert 'Files.readAllBytes(ipConfig)' in launcher
        results.append({'edition':str(folder.relative_to(ROOT)),'passed':True,'files_checked':checked+3})
    linux = 0
    for path in (ROOT/'country').glob('*/*/edition.json'):
        folder=path.parent
        assert (folder/'ip_config.py').read_bytes()==canonical,str(folder)
        assert (folder/'edition.py').read_bytes()==(ROOT/'tools/edition.py').read_bytes(),str(folder)
        linux+=1
    report={'passed':True,'native_editions':len(results),'linux_editions':linux,
            'native_files_checked':sum(r['files_checked'] for r in results),'results':results}
    (ROOT/'build/ip-config/audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('IP CONFIG AUDIT PASS',len(results),'native,',linux,'Linux editions',flush=True)


if __name__=='__main__':main()
