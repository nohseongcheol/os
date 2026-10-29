import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

વ્યાખ્યા_મૂલ્ય = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
મૉડ્યૂલ_મૂલ્ય = importlib.util.module_from_spec(વ્યાખ્યા_મૂલ્ય)
વ્યાખ્યા_મૂલ્ય.loader.exec_module(મૉડ્યૂલ_મૂલ્ય)


class 가짜상자:
    def __init__(self, રૂટ_મૂલ્ય):
        self.રૂટ_મૂલ્ય = રૂટ_મૂલ્ય
        self.명령들 = []
        self.가상기계들 = {}
        self.નિષ્ફળતા_મૂલ્ય = None

    def __call__(self, દલીલો):
        દલીલો = list(map(str, દલીલો))
        self.명령들.append(દલીલો)
        if self.નિષ્ફળતા_મૂલ્ય == દલીલો[1] or (દલીલો[0] == 'make' and self.નિષ્ફળતા_મૂલ્ય == 'make'):
            self.નિષ્ફળતા_મૂલ્ય = None
            raise મૉડ્યૂલ_મૂલ્ય.실행오류('시험용 નિષ્ફળતા_મૂલ્ય')
        if દલીલો[0] == 'make':
            પથ = self.રૂટ_મૂલ્ય / 'os/build/kernel.iso'
            પથ.parent.mkdir(parents=True, exist_ok=True)
            પથ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ક્રિયા = દલીલો[1]
        if ક્રિયા == 'list':
            return '\n'.join('"{}" {{{}}}'.format(મૂલ્ય['name'], અનુક્રમણિકા) for અનુક્રમણિકા, મૂલ્ય in self.가상기계들.items())
        if ક્રિયા == 'createvm':
            અનુક્રમણિકા, નામ = દલીલો[દલીલો.index('--uuid') + 1], દલીલો[દલીલો.index('--name') + 1]
            self.가상기계들[અનુક્રમણિકા] = {'UUID': અનુક્રમણિકા, 'name': નામ, 'VMState': 'poweroff',
                'CfgFile': str(self.રૂટ_મૂલ્ય / '.vbox/machines' / નામ / (નામ + '.vbox')), 'owner': None}
            return ''
        મશીન = self.가상기계들[દલીલો[2]]
        if ક્રિયા == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(નામ), json.dumps(મૂલ્ય)) for નામ, મૂલ્ય in મશીન.items() if નામ != 'owner')
        if ક્રિયા == 'getextradata': return 'Value: ' + મશીન['owner'] if મશીન['owner'] else 'No value set!'
        if ક્રિયા == 'setextradata': મશીન['owner'] = દલીલો[4]
        elif ક્રિયા == 'storagectl': મશીન['storagecontrollername0'] = 'JKOROS IDE'
        elif ક્રિયા == 'storageattach': મશીન['JKOROS IDE-0-0'] = દલીલો[દલીલો.index('--medium') + 1]
        elif ક્રિયા == 'startvm': મશીન['VMState'] = 'running'
        elif ક્રિયા == 'controlvm':
            assert દલીલો[3] == 'resume'
            મશીન['VMState'] = 'running'
        elif ક્રિયા != 'modifyvm': raise AssertionError(દલીલો)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.રૂટ_મૂલ્ય = Path(self.임시.name)
        (self.રૂટ_મૂલ્ય / '.vbox').mkdir()
        self.상자 = 가짜상자(self.રૂટ_મૂલ્ય)
        self.અમલ_કરો_આદેશ = મૉડ્યૂલ_મૂલ્ય.એપ્લિકેશન_લૉન્ચર(self.રૂટ_મૂલ્ય, 'jkoros operating system', આદેશ=self.상자)

    def બનાવો_પ્રવેશ(self):
        પરિમાણ = self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[પરિમાણ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(આદેશ[0] == 'VBoxManage' and આદેશ[1] in ('list', 'showvminfo', 'getextradata') for આદેશ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        પરિમાણ = self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.assertEqual(પરિમાણ['state'], 'running')
        self.assertTrue(Path(પરિમાણ['iso']).is_file())
        self.assertTrue(any('--nic1' in આદેશ and 'none' in આદેશ for આદેશ in self.상자.명령들))
        self.assertFalse(any('hdd' in આદેશ or 'discardstate' in આદેશ or 'createmedium' in આદેશ for આદેશ in self.상자.명령들))

    def test_실행중유지(self):
        self.બનાવો_પ્રવેશ()
        self.assertEqual(self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        મશીન = self.બનાવો_પ્રવેશ()
        મશીન['VMState'] = 'saved'
        લૉગ_મૂલ્ય = self.અમલ_કરો_આદેશ.પથ(self.અમલ_કરો_આદેશ.વાંચો()['serial_log'])
        લૉગ_મૂલ્ય.write_text('saved log')
        self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.assertFalse(any(આદેશ[0] == 'make' or આદેશ[1] == 'modifyvm' for આદેશ in self.상자.명령들))
        self.assertEqual([પથ.read_text() for પથ in લૉગ_મૂલ્ય.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.બનાવો_પ્રવેશ()['VMState'] = 'paused'
        self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.assertTrue(any(આદેશ[1] == 'controlvm' and આદેશ[3] == 'resume' for આદેશ in self.상자.명령들))
        self.assertFalse(any(આદેશ[0] == 'make' for આદેશ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.변경없음()

    def test_소유표식거부(self):
        self.બનાવો_પ્રવેશ()['owner'] = 'someone-else'
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.બનાવો_પ્રવેશ()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        મશીન = self.બનાવો_પ્રવેશ()
        મશીન['VMState'] = 'poweroff'
        મશીન['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.변경없음()

    def test_전환중거부(self):
        self.બનાવો_પ્રવેશ()['VMState'] = 'saving'
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.변경없음()

    def test_등록해제거부(self):
        self.બનાવો_પ્રવેશ()
        self.상자.가상기계들.clear()
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        મશીન = self.બનાવો_પ્રવેશ()
        મશીન['VMState'] = 'poweroff'
        이전 = dict(મશીન)
        self.상자.નિષ્ફળતા_મૂલ્ય = 'make'
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.assertEqual(મશીન, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.નિષ્ફળતા_મૂલ્ય = 'setextradata'
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()
        self.상자.명령들.clear()
        self.assertEqual(self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()['state'], 'running')
        self.assertFalse(any(આદેશ[1] == 'createvm' for આદેશ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        મશીન = self.બનાવો_પ્રવેશ()
        મશીન['VMState'] = 'poweroff'
        Path(મશીન['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.અમલ_કરો_આદેશ()

    def test_상태미생성(self):
        self.assertEqual(self.અમલ_કરો_આદેશ.શૉ_સ્થિતિ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for પથ in ('../outside', '/tmp/outside'):
            with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.પથ(પથ)
        (self.રૂટ_મૂલ્ય / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(મૉડ્યૂલ_મૂલ્ય.실행오류): self.અમલ_કરો_આદેશ.પથ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        પરિમાણ = મૉડ્યૂલ_મૂલ્ય.વિશેષતા_મૂલ્ય('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(પરિમાણ['VMState'], 'running')
        self.assertEqual(પરિમાણ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
