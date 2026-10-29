import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

ਪਰਿਭਾਸ਼ਾ_ਕੀਮਤ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ਮੌਡਿਉਲ_ਕੀਮਤ = importlib.util.module_from_spec(ਪਰਿਭਾਸ਼ਾ_ਕੀਮਤ)
ਪਰਿਭਾਸ਼ਾ_ਕੀਮਤ.loader.exec_module(ਮੌਡਿਉਲ_ਕੀਮਤ)


class 가짜상자:
    def __init__(self, ਰੂਟ_ਕੀਮਤ):
        self.ਰੂਟ_ਕੀਮਤ = ਰੂਟ_ਕੀਮਤ
        self.명령들 = []
        self.가상기계들 = {}
        self.ਅਸਫਲ_ਕੀਮਤ = None

    def __call__(self, ਆਰਗੂਮੈਂਟ):
        ਆਰਗੂਮੈਂਟ = list(map(str, ਆਰਗੂਮੈਂਟ))
        self.명령들.append(ਆਰਗੂਮੈਂਟ)
        if self.ਅਸਫਲ_ਕੀਮਤ == ਆਰਗੂਮੈਂਟ[1] or (ਆਰਗੂਮੈਂਟ[0] == 'make' and self.ਅਸਫਲ_ਕੀਮਤ == 'make'):
            self.ਅਸਫਲ_ਕੀਮਤ = None
            raise ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류('시험용 ਅਸਫਲ_ਕੀਮਤ')
        if ਆਰਗੂਮੈਂਟ[0] == 'make':
            ਮਾਰਗ = self.ਰੂਟ_ਕੀਮਤ / 'os/build/kernel.iso'
            ਮਾਰਗ.parent.mkdir(parents=True, exist_ok=True)
            ਮਾਰਗ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ਐਕਸ਼ਨ = ਆਰਗੂਮੈਂਟ[1]
        if ਐਕਸ਼ਨ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ਕੀਮਤ['name'], ਅਨੁਕ੍ਰਮਣਿਕਾ) for ਅਨੁਕ੍ਰਮਣਿਕਾ, ਕੀਮਤ in self.가상기계들.items())
        if ਐਕਸ਼ਨ == 'createvm':
            ਅਨੁਕ੍ਰਮਣਿਕਾ, ਨਾਂ = ਆਰਗੂਮੈਂਟ[ਆਰਗੂਮੈਂਟ.index('--uuid') + 1], ਆਰਗੂਮੈਂਟ[ਆਰਗੂਮੈਂਟ.index('--name') + 1]
            self.가상기계들[ਅਨੁਕ੍ਰਮਣਿਕਾ] = {'UUID': ਅਨੁਕ੍ਰਮਣਿਕਾ, 'name': ਨਾਂ, 'VMState': 'poweroff',
                'CfgFile': str(self.ਰੂਟ_ਕੀਮਤ / '.vbox/machines' / ਨਾਂ / (ਨਾਂ + '.vbox')), 'owner': None}
            return ''
        ਮਸ਼ੀਨ = self.가상기계들[ਆਰਗੂਮੈਂਟ[2]]
        if ਐਕਸ਼ਨ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ਨਾਂ), json.dumps(ਕੀਮਤ)) for ਨਾਂ, ਕੀਮਤ in ਮਸ਼ੀਨ.items() if ਨਾਂ != 'owner')
        if ਐਕਸ਼ਨ == 'getextradata': return 'Value: ' + ਮਸ਼ੀਨ['owner'] if ਮਸ਼ੀਨ['owner'] else 'No value set!'
        if ਐਕਸ਼ਨ == 'setextradata': ਮਸ਼ੀਨ['owner'] = ਆਰਗੂਮੈਂਟ[4]
        elif ਐਕਸ਼ਨ == 'storagectl': ਮਸ਼ੀਨ['storagecontrollername0'] = 'JKOROS IDE'
        elif ਐਕਸ਼ਨ == 'storageattach': ਮਸ਼ੀਨ['JKOROS IDE-0-0'] = ਆਰਗੂਮੈਂਟ[ਆਰਗੂਮੈਂਟ.index('--medium') + 1]
        elif ਐਕਸ਼ਨ == 'startvm': ਮਸ਼ੀਨ['VMState'] = 'running'
        elif ਐਕਸ਼ਨ == 'controlvm':
            assert ਆਰਗੂਮੈਂਟ[3] == 'resume'
            ਮਸ਼ੀਨ['VMState'] = 'running'
        elif ਐਕਸ਼ਨ != 'modifyvm': raise AssertionError(ਆਰਗੂਮੈਂਟ)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ਰੂਟ_ਕੀਮਤ = Path(self.임시.name)
        (self.ਰੂਟ_ਕੀਮਤ / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ਰੂਟ_ਕੀਮਤ)
        self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ = ਮੌਡਿਉਲ_ਕੀਮਤ.ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ(self.ਰੂਟ_ਕੀਮਤ, 'jkoros operating system', ਕਮਾਂਡ=self.상자)

    def ਬਣਾਓ_ਦਾਖਲਾ(self):
        ਮਾਪ = self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ਮਾਪ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ਕਮਾਂਡ[0] == 'VBoxManage' and ਕਮਾਂਡ[1] in ('list', 'showvminfo', 'getextradata') for ਕਮਾਂਡ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ਮਾਪ = self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.assertEqual(ਮਾਪ['state'], 'running')
        self.assertTrue(Path(ਮਾਪ['iso']).is_file())
        self.assertTrue(any('--nic1' in ਕਮਾਂਡ and 'none' in ਕਮਾਂਡ for ਕਮਾਂਡ in self.상자.명령들))
        self.assertFalse(any('hdd' in ਕਮਾਂਡ or 'discardstate' in ਕਮਾਂਡ or 'createmedium' in ਕਮਾਂਡ for ਕਮਾਂਡ in self.상자.명령들))

    def test_실행중유지(self):
        self.ਬਣਾਓ_ਦਾਖਲਾ()
        self.assertEqual(self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ਮਸ਼ੀਨ = self.ਬਣਾਓ_ਦਾਖਲਾ()
        ਮਸ਼ੀਨ['VMState'] = 'saved'
        ਲੌਗ_ਕੀਮਤ = self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਮਾਰਗ(self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਪੜ੍ਹਨ()['serial_log'])
        ਲੌਗ_ਕੀਮਤ.write_text('saved log')
        self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.assertFalse(any(ਕਮਾਂਡ[0] == 'make' or ਕਮਾਂਡ[1] == 'modifyvm' for ਕਮਾਂਡ in self.상자.명령들))
        self.assertEqual([ਮਾਰਗ.read_text() for ਮਾਰਗ in ਲੌਗ_ਕੀਮਤ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ਬਣਾਓ_ਦਾਖਲਾ()['VMState'] = 'paused'
        self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.assertTrue(any(ਕਮਾਂਡ[1] == 'controlvm' and ਕਮਾਂਡ[3] == 'resume' for ਕਮਾਂਡ in self.상자.명령들))
        self.assertFalse(any(ਕਮਾਂਡ[0] == 'make' for ਕਮਾਂਡ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.변경없음()

    def test_소유표식거부(self):
        self.ਬਣਾਓ_ਦਾਖਲਾ()['owner'] = 'someone-else'
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ਬਣਾਓ_ਦਾਖਲਾ()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ਮਸ਼ੀਨ = self.ਬਣਾਓ_ਦਾਖਲਾ()
        ਮਸ਼ੀਨ['VMState'] = 'poweroff'
        ਮਸ਼ੀਨ['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.변경없음()

    def test_전환중거부(self):
        self.ਬਣਾਓ_ਦਾਖਲਾ()['VMState'] = 'saving'
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.변경없음()

    def test_등록해제거부(self):
        self.ਬਣਾਓ_ਦਾਖਲਾ()
        self.상자.가상기계들.clear()
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ਮਸ਼ੀਨ = self.ਬਣਾਓ_ਦਾਖਲਾ()
        ਮਸ਼ੀਨ['VMState'] = 'poweroff'
        이전 = dict(ਮਸ਼ੀਨ)
        self.상자.ਅਸਫਲ_ਕੀਮਤ = 'make'
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.assertEqual(ਮਸ਼ੀਨ, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ਅਸਫਲ_ਕੀਮਤ = 'setextradata'
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
        self.상자.명령들.clear()
        self.assertEqual(self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()['state'], 'running')
        self.assertFalse(any(ਕਮਾਂਡ[1] == 'createvm' for ਕਮਾਂਡ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ਮਸ਼ੀਨ = self.ਬਣਾਓ_ਦਾਖਲਾ()
        ਮਸ਼ੀਨ['VMState'] = 'poweroff'
        Path(ਮਸ਼ੀਨ['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()

    def test_상태미생성(self):
        self.assertEqual(self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਸ਼ੋਅ_ਸਥਿਤੀ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ਮਾਰਗ in ('../outside', '/tmp/outside'):
            with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਮਾਰਗ(ਮਾਰਗ)
        (self.ਰੂਟ_ਕੀਮਤ / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ਮੌਡਿਉਲ_ਕੀਮਤ.실행오류): self.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਮਾਰਗ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ਮਾਪ = ਮੌਡਿਉਲ_ਕੀਮਤ.ਯੋਗ_ਕੀਮਤ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ਮਾਪ['VMState'], 'running')
        self.assertEqual(ਮਾਪ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
