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
    def __init__(self, koren_VALUE):
        self.koren_VALUE = koren_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.napaka_VALUE = None

    def __call__(self, Argumenti):
        Argumenti = list(map(str, Argumenti))
        self.명령들.append(Argumenti)
        if self.napaka_VALUE == Argumenti[1] or (Argumenti[0] == 'make' and self.napaka_VALUE == 'make'):
            self.napaka_VALUE = None
            raise modul_VALUE.실행오류('시험용 napaka_VALUE')
        if Argumenti[0] == 'make':
            POT = self.koren_VALUE / 'os/build/kernel.iso'
            POT.parent.mkdir(parents=True, exist_ok=True)
            POT.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Dejanje = Argumenti[1]
        if Dejanje == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Dejanje == 'createvm':
            INDEX, Ime = Argumenti[Argumenti.index('--uuid') + 1], Argumenti[Argumenti.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Ime, 'VMState': 'poweroff',
                'CfgFile': str(self.koren_VALUE / '.vbox/machines' / Ime / (Ime + '.vbox')), 'owner': None}
            return ''
        računalnik = self.가상기계들[Argumenti[2]]
        if Dejanje == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ime), json.dumps(VALUE)) for Ime, VALUE in računalnik.items() if Ime != 'owner')
        if Dejanje == 'getextradata': return 'Value: ' + računalnik['owner'] if računalnik['owner'] else 'No value set!'
        if Dejanje == 'setextradata': računalnik['owner'] = Argumenti[4]
        elif Dejanje == 'storagectl': računalnik['storagecontrollername0'] = 'JKOROS IDE'
        elif Dejanje == 'storageattach': računalnik['JKOROS IDE-0-0'] = Argumenti[Argumenti.index('--medium') + 1]
        elif Dejanje == 'startvm': računalnik['VMState'] = 'running'
        elif Dejanje == 'controlvm':
            assert Argumenti[3] == 'resume'
            računalnik['VMState'] = 'running'
        elif Dejanje != 'modifyvm': raise AssertionError(Argumenti)
        return ''


class preskusiti_izvajati(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.koren_VALUE = Path(self.임시.name)
        (self.koren_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.koren_VALUE)
        self.Izvedi_ukaz = modul_VALUE.aplikacija_zaganjalnik(self.koren_VALUE, 'jkoros operating system', Ukaz=self.상자)

    def Ustvari_vnos(self):
        REZULTAT = self.Izvedi_ukaz.Izvedi_ukaz()
        self.상자.명령들.clear()
        return self.상자.가상기계들[REZULTAT['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Ukaz[0] == 'VBoxManage' and Ukaz[1] in ('list', 'showvminfo', 'getextradata') for Ukaz in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        REZULTAT = self.Izvedi_ukaz.Izvedi_ukaz()
        self.assertEqual(REZULTAT['state'], 'running')
        self.assertTrue(Path(REZULTAT['iso']).is_file())
        self.assertTrue(any('--nic1' in Ukaz and 'none' in Ukaz for Ukaz in self.상자.명령들))
        self.assertFalse(any('hdd' in Ukaz or 'discardstate' in Ukaz or 'createmedium' in Ukaz for Ukaz in self.상자.명령들))

    def test_실행중유지(self):
        self.Ustvari_vnos()
        self.assertEqual(self.Izvedi_ukaz.Izvedi_ukaz()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        računalnik = self.Ustvari_vnos()
        računalnik['VMState'] = 'saved'
        LOG_VALUE = self.Izvedi_ukaz.POT(self.Izvedi_ukaz.Branje()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Izvedi_ukaz.Izvedi_ukaz()
        self.assertFalse(any(Ukaz[0] == 'make' or Ukaz[1] == 'modifyvm' for Ukaz in self.상자.명령들))
        self.assertEqual([POT.read_text() for POT in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def preskusiti_Premor_AND_nadaljevati(self):
        self.Ustvari_vnos()['VMState'] = 'paused'
        self.Izvedi_ukaz.Izvedi_ukaz()
        self.assertTrue(any(Ukaz[1] == 'controlvm' and Ukaz[3] == 'resume' for Ukaz in self.상자.명령들))
        self.assertFalse(any(Ukaz[0] == 'make' for Ukaz in self.상자.명령들))

    def preskusiti_Drugo_navidezni_računalnik_ime_spor(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.변경없음()

    def test_소유표식거부(self):
        self.Ustvari_vnos()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Ustvari_vnos()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        računalnik = self.Ustvari_vnos()
        računalnik['VMState'] = 'poweroff'
        računalnik['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.변경없음()

    def test_전환중거부(self):
        self.Ustvari_vnos()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.변경없음()

    def test_등록해제거부(self):
        self.Ustvari_vnos()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        računalnik = self.Ustvari_vnos()
        računalnik['VMState'] = 'poweroff'
        이전 = dict(računalnik)
        self.상자.napaka_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.assertEqual(računalnik, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.napaka_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()
        self.상자.명령들.clear()
        self.assertEqual(self.Izvedi_ukaz.Izvedi_ukaz()['state'], 'running')
        self.assertFalse(any(Ukaz[1] == 'createvm' for Ukaz in self.상자.명령들))

    def test_보존ISO변조거부(self):
        računalnik = self.Ustvari_vnos()
        računalnik['VMState'] = 'poweroff'
        Path(računalnik['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.Izvedi_ukaz()

    def test_상태미생성(self):
        self.assertEqual(self.Izvedi_ukaz.oddaja_stanje()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for POT in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.POT(POT)
        (self.koren_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvedi_ukaz.POT('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        REZULTAT = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(REZULTAT['VMState'], 'running')
        self.assertEqual(REZULTAT['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
