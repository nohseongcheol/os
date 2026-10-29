import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Përkufizim_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Përkufizim_VALUE)
Përkufizim_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, rrënjë_VALUE):
        self.rrënjë_VALUE = rrënjë_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.dështim_VALUE = None

    def __call__(self, Argumente):
        Argumente = list(map(str, Argumente))
        self.명령들.append(Argumente)
        if self.dështim_VALUE == Argumente[1] or (Argumente[0] == 'make' and self.dështim_VALUE == 'make'):
            self.dështim_VALUE = None
            raise modul_VALUE.실행오류('시험용 dështim_VALUE')
        if Argumente[0] == 'make':
            POZICIONI = self.rrënjë_VALUE / 'os/build/kernel.iso'
            POZICIONI.parent.mkdir(parents=True, exist_ok=True)
            POZICIONI.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Veprim = Argumente[1]
        if Veprim == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Veprim == 'createvm':
            INDEX, Emër = Argumente[Argumente.index('--uuid') + 1], Argumente[Argumente.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Emër, 'VMState': 'poweroff',
                'CfgFile': str(self.rrënjë_VALUE / '.vbox/machines' / Emër / (Emër + '.vbox')), 'owner': None}
            return ''
        makinë = self.가상기계들[Argumente[2]]
        if Veprim == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Emër), json.dumps(VALUE)) for Emër, VALUE in makinë.items() if Emër != 'owner')
        if Veprim == 'getextradata': return 'Value: ' + makinë['owner'] if makinë['owner'] else 'No value set!'
        if Veprim == 'setextradata': makinë['owner'] = Argumente[4]
        elif Veprim == 'storagectl': makinë['storagecontrollername0'] = 'JKOROS IDE'
        elif Veprim == 'storageattach': makinë['JKOROS IDE-0-0'] = Argumente[Argumente.index('--medium') + 1]
        elif Veprim == 'startvm': makinë['VMState'] = 'running'
        elif Veprim == 'controlvm':
            assert Argumente[3] == 'resume'
            makinë['VMState'] = 'running'
        elif Veprim != 'modifyvm': raise AssertionError(Argumente)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rrënjë_VALUE = Path(self.임시.name)
        (self.rrënjë_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rrënjë_VALUE)
        self.zbatoj_komandë = modul_VALUE.program_hapës(self.rrënjë_VALUE, 'jkoros operating system', Komanda=self.상자)

    def Krijo_futje(self):
        llogaritje = self.zbatoj_komandë.zbatoj_komandë()
        self.상자.명령들.clear()
        return self.상자.가상기계들[llogaritje['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Komanda[0] == 'VBoxManage' and Komanda[1] in ('list', 'showvminfo', 'getextradata') for Komanda in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        llogaritje = self.zbatoj_komandë.zbatoj_komandë()
        self.assertEqual(llogaritje['state'], 'running')
        self.assertTrue(Path(llogaritje['iso']).is_file())
        self.assertTrue(any('--nic1' in Komanda and 'none' in Komanda for Komanda in self.상자.명령들))
        self.assertFalse(any('hdd' in Komanda or 'discardstate' in Komanda or 'createmedium' in Komanda for Komanda in self.상자.명령들))

    def test_실행중유지(self):
        self.Krijo_futje()
        self.assertEqual(self.zbatoj_komandë.zbatoj_komandë()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        makinë = self.Krijo_futje()
        makinë['VMState'] = 'saved'
        LOG_VALUE = self.zbatoj_komandë.POZICIONI(self.zbatoj_komandë.Leximi()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.zbatoj_komandë.zbatoj_komandë()
        self.assertFalse(any(Komanda[0] == 'make' or Komanda[1] == 'modifyvm' for Komanda in self.상자.명령들))
        self.assertEqual([POZICIONI.read_text() for POZICIONI in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Krijo_futje()['VMState'] = 'paused'
        self.zbatoj_komandë.zbatoj_komandë()
        self.assertTrue(any(Komanda[1] == 'controlvm' and Komanda[3] == 'resume' for Komanda in self.상자.명령들))
        self.assertFalse(any(Komanda[0] == 'make' for Komanda in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.변경없음()

    def test_소유표식거부(self):
        self.Krijo_futje()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Krijo_futje()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        makinë = self.Krijo_futje()
        makinë['VMState'] = 'poweroff'
        makinë['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.변경없음()

    def test_전환중거부(self):
        self.Krijo_futje()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.변경없음()

    def test_등록해제거부(self):
        self.Krijo_futje()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        makinë = self.Krijo_futje()
        makinë['VMState'] = 'poweroff'
        이전 = dict(makinë)
        self.상자.dështim_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.assertEqual(makinë, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.dështim_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()
        self.상자.명령들.clear()
        self.assertEqual(self.zbatoj_komandë.zbatoj_komandë()['state'], 'running')
        self.assertFalse(any(Komanda[1] == 'createvm' for Komanda in self.상자.명령들))

    def test_보존ISO변조거부(self):
        makinë = self.Krijo_futje()
        makinë['VMState'] = 'poweroff'
        Path(makinë['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.zbatoj_komandë()

    def test_상태미생성(self):
        self.assertEqual(self.zbatoj_komandë.shfaq_status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for POZICIONI in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.POZICIONI(POZICIONI)
        (self.rrënjë_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.zbatoj_komandë.POZICIONI('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        llogaritje = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(llogaritje['VMState'], 'running')
        self.assertEqual(llogaritje['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
