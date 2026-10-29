import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definitioun_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
Modüll_VALUE = importlib.util.module_from_spec(Definitioun_VALUE)
Definitioun_VALUE.loader.exec_module(Modüll_VALUE)


class 가짜상자:
    def __init__(self, Racinn_VALUE):
        self.Racinn_VALUE = Racinn_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.Feeler_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.Feeler_VALUE == 인수[1] or (인수[0] == 'make' and self.Feeler_VALUE == 'make'):
            self.Feeler_VALUE = None
            raise Modüll_VALUE.실행오류('시험용 Feeler_VALUE')
        if 인수[0] == 'make':
            Wee = self.Racinn_VALUE / 'os/build/kernel.iso'
            Wee.parent.mkdir(parents=True, exist_ok=True)
            Wee.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aktioun = 인수[1]
        if Aktioun == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Aktioun == 'createvm':
            INDEX, Numm = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Numm, 'VMState': 'poweroff',
                'CfgFile': str(self.Racinn_VALUE / '.vbox/machines' / Numm / (Numm + '.vbox')), 'owner': None}
            return ''
        Computer = self.가상기계들[인수[2]]
        if Aktioun == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Numm), json.dumps(VALUE)) for Numm, VALUE in Computer.items() if Numm != 'owner')
        if Aktioun == 'getextradata': return 'Value: ' + Computer['owner'] if Computer['owner'] else 'No value set!'
        if Aktioun == 'setextradata': Computer['owner'] = 인수[4]
        elif Aktioun == 'storagectl': Computer['storagecontrollername0'] = 'JKOROS IDE'
        elif Aktioun == 'storageattach': Computer['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Aktioun == 'startvm': Computer['VMState'] = 'running'
        elif Aktioun == 'controlvm':
            assert 인수[3] == 'resume'
            Computer['VMState'] = 'running'
        elif Aktioun != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.Racinn_VALUE = Path(self.임시.name)
        (self.Racinn_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.Racinn_VALUE)
        self.ausféieren_Befeel = Modüll_VALUE.App_App_Beräich(self.Racinn_VALUE, 'jkoros operating system', Befeel=self.상자)

    def Create_Agab(self):
        Mooss = self.ausféieren_Befeel.ausféieren_Befeel()
        self.상자.명령들.clear()
        return self.상자.가상기계들[Mooss['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Befeel[0] == 'VBoxManage' and Befeel[1] in ('list', 'showvminfo', 'getextradata') for Befeel in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        Mooss = self.ausféieren_Befeel.ausféieren_Befeel()
        self.assertEqual(Mooss['state'], 'running')
        self.assertTrue(Path(Mooss['iso']).is_file())
        self.assertTrue(any('--nic1' in Befeel and 'none' in Befeel for Befeel in self.상자.명령들))
        self.assertFalse(any('hdd' in Befeel or 'discardstate' in Befeel or 'createmedium' in Befeel for Befeel in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_Agab()
        self.assertEqual(self.ausféieren_Befeel.ausféieren_Befeel()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        Computer = self.Create_Agab()
        Computer['VMState'] = 'saved'
        LOG_VALUE = self.ausféieren_Befeel.Wee(self.ausféieren_Befeel.읽기()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.ausféieren_Befeel.ausféieren_Befeel()
        self.assertFalse(any(Befeel[0] == 'make' or Befeel[1] == 'modifyvm' for Befeel in self.상자.명령들))
        self.assertEqual([Wee.read_text() for Wee in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_Agab()['VMState'] = 'paused'
        self.ausféieren_Befeel.ausféieren_Befeel()
        self.assertTrue(any(Befeel[1] == 'controlvm' and Befeel[3] == 'resume' for Befeel in self.상자.명령들))
        self.assertFalse(any(Befeel[0] == 'make' for Befeel in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_Agab()['owner'] = 'someone-else'
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_Agab()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        Computer = self.Create_Agab()
        Computer['VMState'] = 'poweroff'
        Computer['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_Agab()['VMState'] = 'saving'
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_Agab()
        self.상자.가상기계들.clear()
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        Computer = self.Create_Agab()
        Computer['VMState'] = 'poweroff'
        이전 = dict(Computer)
        self.상자.Feeler_VALUE = 'make'
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.assertEqual(Computer, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.Feeler_VALUE = 'setextradata'
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()
        self.상자.명령들.clear()
        self.assertEqual(self.ausféieren_Befeel.ausféieren_Befeel()['state'], 'running')
        self.assertFalse(any(Befeel[1] == 'createvm' for Befeel in self.상자.명령들))

    def test_보존ISO변조거부(self):
        Computer = self.Create_Agab()
        Computer['VMState'] = 'poweroff'
        Path(Computer['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.ausféieren_Befeel()

    def test_상태미생성(self):
        self.assertEqual(self.ausféieren_Befeel.Show_Status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Wee in ('../outside', '/tmp/outside'):
            with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.Wee(Wee)
        (self.Racinn_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(Modüll_VALUE.실행오류): self.ausféieren_Befeel.Wee('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        Mooss = Modüll_VALUE.Attribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(Mooss['VMState'], 'running')
        self.assertEqual(Mooss['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
