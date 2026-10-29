import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Incazelo_inani = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Incazelo_inani)
Incazelo_inani.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ukwehluleka_inani = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ukwehluleka_inani == 인수[1] or (인수[0] == 'make' and self.ukwehluleka_inani == 'make'):
            self.ukwehluleka_inani = None
            raise 모듈.실행오류('시험용 ukwehluleka_inani')
        if 인수[0] == 'make':
            Indlela_2 = self.뿌리 / 'os/build/kernel.iso'
            Indlela_2.parent.mkdir(parents=True, exist_ok=True)
            Indlela_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Isenzo = 인수[1]
        if Isenzo == 'list':
            return '\n'.join('"{}" {{{}}}'.format(inani['name'], thola_inkomba) for thola_inkomba, inani in self.가상기계들.items())
        if Isenzo == 'createvm':
            thola_inkomba, Igama = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[thola_inkomba] = {'UUID': thola_inkomba, 'name': Igama, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Igama / (Igama + '.vbox')), 'owner': None}
            return ''
        umshini = self.가상기계들[인수[2]]
        if Isenzo == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Igama), json.dumps(inani)) for Igama, inani in umshini.items() if Igama != 'owner')
        if Isenzo == 'getextradata': return 'Value: ' + umshini['owner'] if umshini['owner'] else 'No value set!'
        if Isenzo == 'setextradata': umshini['owner'] = 인수[4]
        elif Isenzo == 'storagectl': umshini['storagecontrollername0'] = 'JKOROS IDE'
        elif Isenzo == 'storageattach': umshini['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Isenzo == 'startvm': umshini['VMState'] = 'running'
        elif Isenzo == 'controlvm':
            assert 인수[3] == 'resume'
            umshini['VMState'] = 'running'
        elif Isenzo != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.yenza_umyalo = 모듈.i_app_ikhabethe_le_app(self.뿌리, 'jkoros operating system', Umlayelo=self.상자)

    def yakha_okufakwayo(self):
        결과 = self.yenza_umyalo.yenza_umyalo()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Umlayelo[0] == 'VBoxManage' and Umlayelo[1] in ('list', 'showvminfo', 'getextradata') for Umlayelo in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.yenza_umyalo.yenza_umyalo()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Umlayelo and 'none' in Umlayelo for Umlayelo in self.상자.명령들))
        self.assertFalse(any('hdd' in Umlayelo or 'discardstate' in Umlayelo or 'createmedium' in Umlayelo for Umlayelo in self.상자.명령들))

    def test_실행중유지(self):
        self.yakha_okufakwayo()
        self.assertEqual(self.yenza_umyalo.yenza_umyalo()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        umshini = self.yakha_okufakwayo()
        umshini['VMState'] = 'saved'
        loga_inani = self.yenza_umyalo.Indlela_2(self.yenza_umyalo.Funda()['serial_log'])
        loga_inani.write_text('saved log')
        self.yenza_umyalo.yenza_umyalo()
        self.assertFalse(any(Umlayelo[0] == 'make' or Umlayelo[1] == 'modifyvm' for Umlayelo in self.상자.명령들))
        self.assertEqual([Indlela_2.read_text() for Indlela_2 in loga_inani.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.yakha_okufakwayo()['VMState'] = 'paused'
        self.yenza_umyalo.yenza_umyalo()
        self.assertTrue(any(Umlayelo[1] == 'controlvm' and Umlayelo[3] == 'resume' for Umlayelo in self.상자.명령들))
        self.assertFalse(any(Umlayelo[0] == 'make' for Umlayelo in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.변경없음()

    def test_소유표식거부(self):
        self.yakha_okufakwayo()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.yakha_okufakwayo()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        umshini = self.yakha_okufakwayo()
        umshini['VMState'] = 'poweroff'
        umshini['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.변경없음()

    def test_전환중거부(self):
        self.yakha_okufakwayo()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.변경없음()

    def test_등록해제거부(self):
        self.yakha_okufakwayo()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        umshini = self.yakha_okufakwayo()
        umshini['VMState'] = 'poweroff'
        이전 = dict(umshini)
        self.상자.ukwehluleka_inani = 'make'
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.assertEqual(umshini, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ukwehluleka_inani = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()
        self.상자.명령들.clear()
        self.assertEqual(self.yenza_umyalo.yenza_umyalo()['state'], 'running')
        self.assertFalse(any(Umlayelo[1] == 'createvm' for Umlayelo in self.상자.명령들))

    def test_보존ISO변조거부(self):
        umshini = self.yakha_okufakwayo()
        umshini['VMState'] = 'poweroff'
        Path(umshini['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.yenza_umyalo()

    def test_상태미생성(self):
        self.assertEqual(self.yenza_umyalo.khombisa_isimo()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Indlela_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.yenza_umyalo.Indlela_2(Indlela_2)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.yenza_umyalo.Indlela_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.isibaluli_inani('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
