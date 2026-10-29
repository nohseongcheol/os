import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definicja_WARTOŚĆ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
moduł_WARTOŚĆ = importlib.util.module_from_spec(Definicja_WARTOŚĆ)
Definicja_WARTOŚĆ.loader.exec_module(moduł_WARTOŚĆ)


class 가짜상자:
    def __init__(self, korzeń_WARTOŚĆ):
        self.korzeń_WARTOŚĆ = korzeń_WARTOŚĆ
        self.명령들 = []
        self.Virtual_Machines = {}
        self.awaria_WARTOŚĆ = None

    def __call__(self, argumenty):
        argumenty = list(map(str, argumenty))
        self.명령들.append(argumenty)
        if self.awaria_WARTOŚĆ == argumenty[1] or (argumenty[0] == 'make' and self.awaria_WARTOŚĆ == 'make'):
            self.awaria_WARTOŚĆ = None
            raise moduł_WARTOŚĆ.wykonanie_błąd('시험용 awaria_WARTOŚĆ')
        if argumenty[0] == 'make':
            ścieżka_2 = self.korzeń_WARTOŚĆ / 'os/build/kernel.iso'
            ścieżka_2.parent.mkdir(parents=True, exist_ok=True)
            ścieżka_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Akcja = argumenty[1]
        if Akcja == 'list':
            return '\n'.join('"{}" {{{}}}'.format(WARTOŚĆ['name'], INDEKS) for INDEKS, WARTOŚĆ in self.Virtual_Machines.items())
        if Akcja == 'createvm':
            INDEKS, Nazwa = argumenty[argumenty.index('--uuid') + 1], argumenty[argumenty.index('--name') + 1]
            self.Virtual_Machines[INDEKS] = {'UUID': INDEKS, 'name': Nazwa, 'VMState': 'poweroff',
                'CfgFile': str(self.korzeń_WARTOŚĆ / '.vbox/machines' / Nazwa / (Nazwa + '.vbox')), 'owner': None}
            return ''
        maszyna = self.Virtual_Machines[argumenty[2]]
        if Akcja == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nazwa), json.dumps(WARTOŚĆ)) for Nazwa, WARTOŚĆ in maszyna.items() if Nazwa != 'owner')
        if Akcja == 'getextradata': return 'Value: ' + maszyna['owner'] if maszyna['owner'] else 'No value set!'
        if Akcja == 'setextradata': maszyna['owner'] = argumenty[4]
        elif Akcja == 'storagectl': maszyna['storagecontrollername0'] = 'JKOROS IDE'
        elif Akcja == 'storageattach': maszyna['JKOROS IDE-0-0'] = argumenty[argumenty.index('--medium') + 1]
        elif Akcja == 'startvm': maszyna['VMState'] = 'running'
        elif Akcja == 'controlvm':
            assert argumenty[3] == 'resume'
            maszyna['VMState'] = 'running'
        elif Akcja != 'modifyvm': raise AssertionError(argumenty)
        return ''


class przebieg_testu(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.korzeń_WARTOŚĆ = Path(self.임시.name)
        (self.korzeń_WARTOŚĆ / '.vbox').mkdir()
        self.상자 = 가짜상자(self.korzeń_WARTOŚĆ)
        self.Wykonaj_polecenie = moduł_WARTOŚĆ.program_Launcher(self.korzeń_WARTOŚĆ, 'jkoros operating system', polecenie=self.상자)

    def Twórca_wpis(self):
        WYNIK = self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[WYNIK['uuid']]

    def 변경없음(self):
        self.assertTrue(all(polecenie[0] == 'VBoxManage' and polecenie[1] in ('list', 'showvminfo', 'getextradata') for polecenie in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        WYNIK = self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.assertEqual(WYNIK['state'], 'running')
        self.assertTrue(Path(WYNIK['iso']).is_file())
        self.assertTrue(any('--nic1' in polecenie and 'none' in polecenie for polecenie in self.상자.명령들))
        self.assertFalse(any('hdd' in polecenie or 'discardstate' in polecenie or 'createmedium' in polecenie for polecenie in self.상자.명령들))

    def test_실행중유지(self):
        self.Twórca_wpis()
        self.assertEqual(self.Wykonaj_polecenie.Wykonaj_polecenie()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        maszyna = self.Twórca_wpis()
        maszyna['VMState'] = 'saved'
        LOG_WARTOŚĆ = self.Wykonaj_polecenie.ścieżka_2(self.Wykonaj_polecenie.Odczyt()['serial_log'])
        LOG_WARTOŚĆ.write_text('saved log')
        self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.assertFalse(any(polecenie[0] == 'make' or polecenie[1] == 'modifyvm' for polecenie in self.상자.명령들))
        self.assertEqual([ścieżka_2.read_text() for ścieżka_2 in LOG_WARTOŚĆ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Wstrzymaj_ORAZ_CV(self):
        self.Twórca_wpis()['VMState'] = 'paused'
        self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.assertTrue(any(polecenie[1] == 'controlvm' and polecenie[3] == 'resume' for polecenie in self.상자.명령들))
        self.assertFalse(any(polecenie[0] == 'make' for polecenie in self.상자.명령들))

    def test_Inne_maszyna_wirtualna_nazwa_kolizja(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.변경없음()

    def test_소유표식거부(self):
        self.Twórca_wpis()['owner'] = 'someone-else'
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Twórca_wpis()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        maszyna = self.Twórca_wpis()
        maszyna['VMState'] = 'poweroff'
        maszyna['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.변경없음()

    def test_전환중거부(self):
        self.Twórca_wpis()['VMState'] = 'saving'
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.변경없음()

    def test_등록해제거부(self):
        self.Twórca_wpis()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        maszyna = self.Twórca_wpis()
        maszyna['VMState'] = 'poweroff'
        Wstecz_towar = dict(maszyna)
        self.상자.awaria_WARTOŚĆ = 'make'
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.assertEqual(maszyna, Wstecz_towar)

    def test_중단된소유표식설정복구(self):
        self.상자.awaria_WARTOŚĆ = 'setextradata'
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()
        self.상자.명령들.clear()
        self.assertEqual(self.Wykonaj_polecenie.Wykonaj_polecenie()['state'], 'running')
        self.assertFalse(any(polecenie[1] == 'createvm' for polecenie in self.상자.명령들))

    def test_보존ISO변조거부(self):
        maszyna = self.Twórca_wpis()
        maszyna['VMState'] = 'poweroff'
        Path(maszyna['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.Wykonaj_polecenie()

    def test_상태미생성(self):
        self.assertEqual(self.Wykonaj_polecenie.program_Stan()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ścieżka_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.ścieżka_2(ścieżka_2)
        (self.korzeń_WARTOŚĆ / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(moduł_WARTOŚĆ.wykonanie_błąd): self.Wykonaj_polecenie.ścieżka_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        WYNIK = moduł_WARTOŚĆ.wartość_atrybutu('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(WYNIK['VMState'], 'running')
        self.assertEqual(WYNIK['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
