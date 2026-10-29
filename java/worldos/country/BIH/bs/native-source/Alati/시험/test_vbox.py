import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definicija_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Definicija_VALUE)
Definicija_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, koijen_VALUE):
        self.koijen_VALUE = koijen_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.neuspjeh_VALUE = None

    def __call__(self, Argumenti):
        Argumenti = list(map(str, Argumenti))
        self.명령들.append(Argumenti)
        if self.neuspjeh_VALUE == Argumenti[1] or (Argumenti[0] == 'make' and self.neuspjeh_VALUE == 'make'):
            self.neuspjeh_VALUE = None
            raise modul_VALUE.실행오류('시험용 neuspjeh_VALUE')
        if Argumenti[0] == 'make':
            Putanja = self.koijen_VALUE / 'os/build/kernel.iso'
            Putanja.parent.mkdir(parents=True, exist_ok=True)
            Putanja.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        radnja = Argumenti[1]
        if radnja == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if radnja == 'createvm':
            INDEX, Naziv = Argumenti[Argumenti.index('--uuid') + 1], Argumenti[Argumenti.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Naziv, 'VMState': 'poweroff',
                'CfgFile': str(self.koijen_VALUE / '.vbox/machines' / Naziv / (Naziv + '.vbox')), 'owner': None}
            return ''
        mašina = self.가상기계들[Argumenti[2]]
        if radnja == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Naziv), json.dumps(VALUE)) for Naziv, VALUE in mašina.items() if Naziv != 'owner')
        if radnja == 'getextradata': return 'Value: ' + mašina['owner'] if mašina['owner'] else 'No value set!'
        if radnja == 'setextradata': mašina['owner'] = Argumenti[4]
        elif radnja == 'storagectl': mašina['storagecontrollername0'] = 'JKOROS IDE'
        elif radnja == 'storageattach': mašina['JKOROS IDE-0-0'] = Argumenti[Argumenti.index('--medium') + 1]
        elif radnja == 'startvm': mašina['VMState'] = 'running'
        elif radnja == 'controlvm':
            assert Argumenti[3] == 'resume'
            mašina['VMState'] = 'running'
        elif radnja != 'modifyvm': raise AssertionError(Argumenti)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.koijen_VALUE = Path(self.임시.name)
        (self.koijen_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.koijen_VALUE)
        self.Izvrši_komanda = modul_VALUE.program_pokretač(self.koijen_VALUE, 'jkoros operating system', Naredba=self.상자)

    def Create_unos(self):
        mjera = self.Izvrši_komanda.Izvrši_komanda()
        self.상자.명령들.clear()
        return self.상자.가상기계들[mjera['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Naredba[0] == 'VBoxManage' and Naredba[1] in ('list', 'showvminfo', 'getextradata') for Naredba in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        mjera = self.Izvrši_komanda.Izvrši_komanda()
        self.assertEqual(mjera['state'], 'running')
        self.assertTrue(Path(mjera['iso']).is_file())
        self.assertTrue(any('--nic1' in Naredba and 'none' in Naredba for Naredba in self.상자.명령들))
        self.assertFalse(any('hdd' in Naredba or 'discardstate' in Naredba or 'createmedium' in Naredba for Naredba in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_unos()
        self.assertEqual(self.Izvrši_komanda.Izvrši_komanda()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mašina = self.Create_unos()
        mašina['VMState'] = 'saved'
        LOG_VALUE = self.Izvrši_komanda.Putanja(self.Izvrši_komanda.Čitaj()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Izvrši_komanda.Izvrši_komanda()
        self.assertFalse(any(Naredba[0] == 'make' or Naredba[1] == 'modifyvm' for Naredba in self.상자.명령들))
        self.assertEqual([Putanja.read_text() for Putanja in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_unos()['VMState'] = 'paused'
        self.Izvrši_komanda.Izvrši_komanda()
        self.assertTrue(any(Naredba[1] == 'controlvm' and Naredba[3] == 'resume' for Naredba in self.상자.명령들))
        self.assertFalse(any(Naredba[0] == 'make' for Naredba in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_unos()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_unos()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mašina = self.Create_unos()
        mašina['VMState'] = 'poweroff'
        mašina['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_unos()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_unos()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mašina = self.Create_unos()
        mašina['VMState'] = 'poweroff'
        이전 = dict(mašina)
        self.상자.neuspjeh_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.assertEqual(mašina, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.neuspjeh_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.상자.명령들.clear()
        self.assertEqual(self.Izvrši_komanda.Izvrši_komanda()['state'], 'running')
        self.assertFalse(any(Naredba[1] == 'createvm' for Naredba in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mašina = self.Create_unos()
        mašina['VMState'] = 'poweroff'
        Path(mašina['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()

    def test_상태미생성(self):
        self.assertEqual(self.Izvrši_komanda.program_stanje()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Putanja in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Putanja(Putanja)
        (self.koijen_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Putanja('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        mjera = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(mjera['VMState'], 'running')
        self.assertEqual(mjera['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
