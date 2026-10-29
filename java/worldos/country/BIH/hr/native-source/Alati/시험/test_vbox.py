import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

definicija_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(definicija_VALUE)
definicija_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, korijen_VALUE):
        self.korijen_VALUE = korijen_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.kvar_VALUE = None

    def __call__(self, Argumenti):
        Argumenti = list(map(str, Argumenti))
        self.명령들.append(Argumenti)
        if self.kvar_VALUE == Argumenti[1] or (Argumenti[0] == 'make' and self.kvar_VALUE == 'make'):
            self.kvar_VALUE = None
            raise modul_VALUE.실행오류('시험용 kvar_VALUE')
        if Argumenti[0] == 'make':
            PUTANJA = self.korijen_VALUE / 'os/build/kernel.iso'
            PUTANJA.parent.mkdir(parents=True, exist_ok=True)
            PUTANJA.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aktivnost = Argumenti[1]
        if Aktivnost == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Aktivnost == 'createvm':
            INDEX, Ime = Argumenti[Argumenti.index('--uuid') + 1], Argumenti[Argumenti.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Ime, 'VMState': 'poweroff',
                'CfgFile': str(self.korijen_VALUE / '.vbox/machines' / Ime / (Ime + '.vbox')), 'owner': None}
            return ''
        stroj = self.가상기계들[Argumenti[2]]
        if Aktivnost == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ime), json.dumps(VALUE)) for Ime, VALUE in stroj.items() if Ime != 'owner')
        if Aktivnost == 'getextradata': return 'Value: ' + stroj['owner'] if stroj['owner'] else 'No value set!'
        if Aktivnost == 'setextradata': stroj['owner'] = Argumenti[4]
        elif Aktivnost == 'storagectl': stroj['storagecontrollername0'] = 'JKOROS IDE'
        elif Aktivnost == 'storageattach': stroj['JKOROS IDE-0-0'] = Argumenti[Argumenti.index('--medium') + 1]
        elif Aktivnost == 'startvm': stroj['VMState'] = 'running'
        elif Aktivnost == 'controlvm':
            assert Argumenti[3] == 'resume'
            stroj['VMState'] = 'running'
        elif Aktivnost != 'modifyvm': raise AssertionError(Argumenti)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.korijen_VALUE = Path(self.임시.name)
        (self.korijen_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.korijen_VALUE)
        self.Izvrši_naredba = modul_VALUE.program_pokretač(self.korijen_VALUE, 'jkoros operating system', Naredba=self.상자)

    def Create_unos(self):
        REZULTAT = self.Izvrši_naredba.Izvrši_naredba()
        self.상자.명령들.clear()
        return self.상자.가상기계들[REZULTAT['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Naredba[0] == 'VBoxManage' and Naredba[1] in ('list', 'showvminfo', 'getextradata') for Naredba in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        REZULTAT = self.Izvrši_naredba.Izvrši_naredba()
        self.assertEqual(REZULTAT['state'], 'running')
        self.assertTrue(Path(REZULTAT['iso']).is_file())
        self.assertTrue(any('--nic1' in Naredba and 'none' in Naredba for Naredba in self.상자.명령들))
        self.assertFalse(any('hdd' in Naredba or 'discardstate' in Naredba or 'createmedium' in Naredba for Naredba in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_unos()
        self.assertEqual(self.Izvrši_naredba.Izvrši_naredba()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        stroj = self.Create_unos()
        stroj['VMState'] = 'saved'
        LOG_VALUE = self.Izvrši_naredba.PUTANJA(self.Izvrši_naredba.Čitaj()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Izvrši_naredba.Izvrši_naredba()
        self.assertFalse(any(Naredba[0] == 'make' or Naredba[1] == 'modifyvm' for Naredba in self.상자.명령들))
        self.assertEqual([PUTANJA.read_text() for PUTANJA in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_unos()['VMState'] = 'paused'
        self.Izvrši_naredba.Izvrši_naredba()
        self.assertTrue(any(Naredba[1] == 'controlvm' and Naredba[3] == 'resume' for Naredba in self.상자.명령들))
        self.assertFalse(any(Naredba[0] == 'make' for Naredba in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_unos()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_unos()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        stroj = self.Create_unos()
        stroj['VMState'] = 'poweroff'
        stroj['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_unos()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_unos()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        stroj = self.Create_unos()
        stroj['VMState'] = 'poweroff'
        이전 = dict(stroj)
        self.상자.kvar_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.assertEqual(stroj, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.kvar_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()
        self.상자.명령들.clear()
        self.assertEqual(self.Izvrši_naredba.Izvrši_naredba()['state'], 'running')
        self.assertFalse(any(Naredba[1] == 'createvm' for Naredba in self.상자.명령들))

    def test_보존ISO변조거부(self):
        stroj = self.Create_unos()
        stroj['VMState'] = 'poweroff'
        Path(stroj['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.Izvrši_naredba()

    def test_상태미생성(self):
        self.assertEqual(self.Izvrši_naredba.emisija_Stanje()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for PUTANJA in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.PUTANJA(PUTANJA)
        (self.korijen_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_naredba.PUTANJA('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        REZULTAT = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(REZULTAT['VMState'], 'running')
        self.assertEqual(REZULTAT['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
