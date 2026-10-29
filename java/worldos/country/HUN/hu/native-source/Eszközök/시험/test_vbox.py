import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definíció_ÉRTÉK = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_ÉRTÉK = importlib.util.module_from_spec(Definíció_ÉRTÉK)
Definíció_ÉRTÉK.loader.exec_module(modul_ÉRTÉK)


class 가짜상자:
    def __init__(self, gyök_ÉRTÉK):
        self.gyök_ÉRTÉK = gyök_ÉRTÉK
        self.명령들 = []
        self.Virtual_Machines = {}
        self.hiba_ÉRTÉK = None

    def __call__(self, Argumentumok):
        Argumentumok = list(map(str, Argumentumok))
        self.명령들.append(Argumentumok)
        if self.hiba_ÉRTÉK == Argumentumok[1] or (Argumentumok[0] == 'make' and self.hiba_ÉRTÉK == 'make'):
            self.hiba_ÉRTÉK = None
            raise modul_ÉRTÉK.végrehajtás_hiba('시험용 hiba_ÉRTÉK')
        if Argumentumok[0] == 'make':
            ÚTVONAL = self.gyök_ÉRTÉK / 'os/build/kernel.iso'
            ÚTVONAL.parent.mkdir(parents=True, exist_ok=True)
            ÚTVONAL.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Művelet = Argumentumok[1]
        if Művelet == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ÉRTÉK['name'], INDEX) for INDEX, ÉRTÉK in self.Virtual_Machines.items())
        if Művelet == 'createvm':
            INDEX, Név = Argumentumok[Argumentumok.index('--uuid') + 1], Argumentumok[Argumentumok.index('--name') + 1]
            self.Virtual_Machines[INDEX] = {'UUID': INDEX, 'name': Név, 'VMState': 'poweroff',
                'CfgFile': str(self.gyök_ÉRTÉK / '.vbox/machines' / Név / (Név + '.vbox')), 'owner': None}
            return ''
        gép = self.Virtual_Machines[Argumentumok[2]]
        if Művelet == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Név), json.dumps(ÉRTÉK)) for Név, ÉRTÉK in gép.items() if Név != 'owner')
        if Művelet == 'getextradata': return 'Value: ' + gép['owner'] if gép['owner'] else 'No value set!'
        if Művelet == 'setextradata': gép['owner'] = Argumentumok[4]
        elif Művelet == 'storagectl': gép['storagecontrollername0'] = 'JKOROS IDE'
        elif Művelet == 'storageattach': gép['JKOROS IDE-0-0'] = Argumentumok[Argumentumok.index('--medium') + 1]
        elif Művelet == 'startvm': gép['VMState'] = 'running'
        elif Művelet == 'controlvm':
            assert Argumentumok[3] == 'resume'
            gép['VMState'] = 'running'
        elif Művelet != 'modifyvm': raise AssertionError(Argumentumok)
        return ''


class teszt_futtat(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.gyök_ÉRTÉK = Path(self.임시.name)
        (self.gyök_ÉRTÉK / '.vbox').mkdir()
        self.상자 = 가짜상자(self.gyök_ÉRTÉK)
        self.végrehajt_parancs = modul_ÉRTÉK.app_indító(self.gyök_ÉRTÉK, 'jkoros operating system', Parancs=self.상자)

    def készít_bejegyzés(self):
        KR = self.végrehajt_parancs.végrehajt_parancs()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[KR['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Parancs[0] == 'VBoxManage' and Parancs[1] in ('list', 'showvminfo', 'getextradata') for Parancs in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        KR = self.végrehajt_parancs.végrehajt_parancs()
        self.assertEqual(KR['state'], 'running')
        self.assertTrue(Path(KR['iso']).is_file())
        self.assertTrue(any('--nic1' in Parancs and 'none' in Parancs for Parancs in self.상자.명령들))
        self.assertFalse(any('hdd' in Parancs or 'discardstate' in Parancs or 'createmedium' in Parancs for Parancs in self.상자.명령들))

    def test_실행중유지(self):
        self.készít_bejegyzés()
        self.assertEqual(self.végrehajt_parancs.végrehajt_parancs()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        gép = self.készít_bejegyzés()
        gép['VMState'] = 'saved'
        LOG_ÉRTÉK = self.végrehajt_parancs.ÚTVONAL(self.végrehajt_parancs.Olvasás()['serial_log'])
        LOG_ÉRTÉK.write_text('saved log')
        self.végrehajt_parancs.végrehajt_parancs()
        self.assertFalse(any(Parancs[0] == 'make' or Parancs[1] == 'modifyvm' for Parancs in self.상자.명령들))
        self.assertEqual([ÚTVONAL.read_text() for ÚTVONAL in LOG_ÉRTÉK.parent.glob('before-resume-*.log')], ['saved log'])

    def teszt_Szünet_ÉS_CV(self):
        self.készít_bejegyzés()['VMState'] = 'paused'
        self.végrehajt_parancs.végrehajt_parancs()
        self.assertTrue(any(Parancs[1] == 'controlvm' and Parancs[3] == 'resume' for Parancs in self.상자.명령들))
        self.assertFalse(any(Parancs[0] == 'make' for Parancs in self.상자.명령들))

    def teszt_Egyéb_VM_név_ütközés(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.변경없음()

    def test_소유표식거부(self):
        self.készít_bejegyzés()['owner'] = 'someone-else'
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.készít_bejegyzés()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        gép = self.készít_bejegyzés()
        gép['VMState'] = 'poweroff'
        gép['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.변경없음()

    def test_전환중거부(self):
        self.készít_bejegyzés()['VMState'] = 'saving'
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.변경없음()

    def test_등록해제거부(self):
        self.készít_bejegyzés()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        gép = self.készít_bejegyzés()
        gép['VMState'] = 'poweroff'
        Előző_cikk = dict(gép)
        self.상자.hiba_ÉRTÉK = 'make'
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.assertEqual(gép, Előző_cikk)

    def test_중단된소유표식설정복구(self):
        self.상자.hiba_ÉRTÉK = 'setextradata'
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()
        self.상자.명령들.clear()
        self.assertEqual(self.végrehajt_parancs.végrehajt_parancs()['state'], 'running')
        self.assertFalse(any(Parancs[1] == 'createvm' for Parancs in self.상자.명령들))

    def test_보존ISO변조거부(self):
        gép = self.készít_bejegyzés()
        gép['VMState'] = 'poweroff'
        Path(gép['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.végrehajt_parancs()

    def test_상태미생성(self):
        self.assertEqual(self.végrehajt_parancs.bemutató_Állapot()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ÚTVONAL in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.ÚTVONAL(ÚTVONAL)
        (self.gyök_ÉRTÉK / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_ÉRTÉK.végrehajtás_hiba): self.végrehajt_parancs.ÚTVONAL('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        KR = modul_ÉRTÉK.attribútum_ÉRTÉK('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(KR['VMState'], 'running')
        self.assertEqual(KR['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
