import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

정의 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(정의)
정의.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, rot_VALUE):
        self.rot_VALUE = rot_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.feil_VALUE = None

    def __call__(self, Argument):
        Argument = list(map(str, Argument))
        self.명령들.append(Argument)
        if self.feil_VALUE == Argument[1] or (Argument[0] == 'make' and self.feil_VALUE == 'make'):
            self.feil_VALUE = None
            raise modul_VALUE.실행오류('시험용 feil_VALUE')
        if Argument[0] == 'make':
            STIGE = self.rot_VALUE / 'os/build/kernel.iso'
            STIGE.parent.mkdir(parents=True, exist_ok=True)
            STIGE.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Handling = Argument[1]
        if Handling == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Handling == 'createvm':
            INDEX, Namn = Argument[Argument.index('--uuid') + 1], Argument[Argument.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Namn, 'VMState': 'poweroff',
                'CfgFile': str(self.rot_VALUE / '.vbox/machines' / Namn / (Namn + '.vbox')), 'owner': None}
            return ''
        maskin = self.가상기계들[Argument[2]]
        if Handling == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Namn), json.dumps(VALUE)) for Namn, VALUE in maskin.items() if Namn != 'owner')
        if Handling == 'getextradata': return 'Value: ' + maskin['owner'] if maskin['owner'] else 'No value set!'
        if Handling == 'setextradata': maskin['owner'] = Argument[4]
        elif Handling == 'storagectl': maskin['storagecontrollername0'] = 'JKOROS IDE'
        elif Handling == 'storageattach': maskin['JKOROS IDE-0-0'] = Argument[Argument.index('--medium') + 1]
        elif Handling == 'startvm': maskin['VMState'] = 'running'
        elif Handling == 'controlvm':
            assert Argument[3] == 'resume'
            maskin['VMState'] = 'running'
        elif Handling != 'modifyvm': raise AssertionError(Argument)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rot_VALUE = Path(self.임시.name)
        (self.rot_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rot_VALUE)
        self.Utfør_kommando = modul_VALUE.app_appskuff(self.rot_VALUE, 'jkoros operating system', Kommando=self.상자)

    def Opprett_oppføring(self):
        forretningsmål = self.Utfør_kommando.Utfør_kommando()
        self.상자.명령들.clear()
        return self.상자.가상기계들[forretningsmål['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Kommando[0] == 'VBoxManage' and Kommando[1] in ('list', 'showvminfo', 'getextradata') for Kommando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        forretningsmål = self.Utfør_kommando.Utfør_kommando()
        self.assertEqual(forretningsmål['state'], 'running')
        self.assertTrue(Path(forretningsmål['iso']).is_file())
        self.assertTrue(any('--nic1' in Kommando and 'none' in Kommando for Kommando in self.상자.명령들))
        self.assertFalse(any('hdd' in Kommando or 'discardstate' in Kommando or 'createmedium' in Kommando for Kommando in self.상자.명령들))

    def test_실행중유지(self):
        self.Opprett_oppføring()
        self.assertEqual(self.Utfør_kommando.Utfør_kommando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        maskin = self.Opprett_oppføring()
        maskin['VMState'] = 'saved'
        LOG_VALUE = self.Utfør_kommando.STIGE(self.Utfør_kommando.Les()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Utfør_kommando.Utfør_kommando()
        self.assertFalse(any(Kommando[0] == 'make' or Kommando[1] == 'modifyvm' for Kommando in self.상자.명령들))
        self.assertEqual([STIGE.read_text() for STIGE in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Opprett_oppføring()['VMState'] = 'paused'
        self.Utfør_kommando.Utfør_kommando()
        self.assertTrue(any(Kommando[1] == 'controlvm' and Kommando[3] == 'resume' for Kommando in self.상자.명령들))
        self.assertFalse(any(Kommando[0] == 'make' for Kommando in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_소유표식거부(self):
        self.Opprett_oppføring()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Opprett_oppføring()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        maskin = self.Opprett_oppføring()
        maskin['VMState'] = 'poweroff'
        maskin['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_전환중거부(self):
        self.Opprett_oppføring()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_등록해제거부(self):
        self.Opprett_oppføring()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        maskin = self.Opprett_oppføring()
        maskin['VMState'] = 'poweroff'
        이전 = dict(maskin)
        self.상자.feil_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.assertEqual(maskin, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.feil_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()
        self.상자.명령들.clear()
        self.assertEqual(self.Utfør_kommando.Utfør_kommando()['state'], 'running')
        self.assertFalse(any(Kommando[1] == 'createvm' for Kommando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        maskin = self.Opprett_oppføring()
        maskin['VMState'] = 'poweroff'
        Path(maskin['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.Utfør_kommando()

    def test_상태미생성(self):
        self.assertEqual(self.Utfør_kommando.vise_status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for STIGE in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.STIGE(STIGE)
        (self.rot_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Utfør_kommando.STIGE('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        forretningsmål = modul_VALUE.attributt_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(forretningsmål['VMState'], 'running')
        self.assertEqual(forretningsmål['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
