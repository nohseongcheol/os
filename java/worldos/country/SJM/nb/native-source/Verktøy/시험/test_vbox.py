import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definisjon_VERDI = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VERDI = importlib.util.module_from_spec(Definisjon_VERDI)
Definisjon_VERDI.loader.exec_module(modul_VERDI)


class 가짜상자:
    def __init__(self, rot_VERDI):
        self.rot_VERDI = rot_VERDI
        self.명령들 = []
        self.Virtual_Machines = {}
        self.feil_VERDI = None

    def __call__(self, Argumenter):
        Argumenter = list(map(str, Argumenter))
        self.명령들.append(Argumenter)
        if self.feil_VERDI == Argumenter[1] or (Argumenter[0] == 'make' and self.feil_VERDI == 'make'):
            self.feil_VERDI = None
            raise modul_VERDI.kjøring_feil('시험용 feil_VERDI')
        if Argumenter[0] == 'make':
            Sti = self.rot_VERDI / 'os/build/kernel.iso'
            Sti.parent.mkdir(parents=True, exist_ok=True)
            Sti.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Handling = Argumenter[1]
        if Handling == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VERDI['name'], INDEKS) for INDEKS, VERDI in self.Virtual_Machines.items())
        if Handling == 'createvm':
            INDEKS, Navn = Argumenter[Argumenter.index('--uuid') + 1], Argumenter[Argumenter.index('--name') + 1]
            self.Virtual_Machines[INDEKS] = {'UUID': INDEKS, 'name': Navn, 'VMState': 'poweroff',
                'CfgFile': str(self.rot_VERDI / '.vbox/machines' / Navn / (Navn + '.vbox')), 'owner': None}
            return ''
        maskin = self.Virtual_Machines[Argumenter[2]]
        if Handling == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Navn), json.dumps(VERDI)) for Navn, VERDI in maskin.items() if Navn != 'owner')
        if Handling == 'getextradata': return 'Value: ' + maskin['owner'] if maskin['owner'] else 'No value set!'
        if Handling == 'setextradata': maskin['owner'] = Argumenter[4]
        elif Handling == 'storagectl': maskin['storagecontrollername0'] = 'JKOROS IDE'
        elif Handling == 'storageattach': maskin['JKOROS IDE-0-0'] = Argumenter[Argumenter.index('--medium') + 1]
        elif Handling == 'startvm': maskin['VMState'] = 'running'
        elif Handling == 'controlvm':
            assert Argumenter[3] == 'resume'
            maskin['VMState'] = 'running'
        elif Handling != 'modifyvm': raise AssertionError(Argumenter)
        return ''


class test_kjøre(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rot_VERDI = Path(self.임시.name)
        (self.rot_VERDI / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rot_VERDI)
        self.Utfør_kommando = modul_VERDI.app_appskuff(self.rot_VERDI, 'jkoros operating system', Kommando=self.상자)

    def åpne_oppføring(self):
        KR = self.Utfør_kommando.Utfør_kommando()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[KR['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Kommando[0] == 'VBoxManage' and Kommando[1] in ('list', 'showvminfo', 'getextradata') for Kommando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        KR = self.Utfør_kommando.Utfør_kommando()
        self.assertEqual(KR['state'], 'running')
        self.assertTrue(Path(KR['iso']).is_file())
        self.assertTrue(any('--nic1' in Kommando and 'none' in Kommando for Kommando in self.상자.명령들))
        self.assertFalse(any('hdd' in Kommando or 'discardstate' in Kommando or 'createmedium' in Kommando for Kommando in self.상자.명령들))

    def test_실행중유지(self):
        self.åpne_oppføring()
        self.assertEqual(self.Utfør_kommando.Utfør_kommando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        maskin = self.åpne_oppføring()
        maskin['VMState'] = 'saved'
        LOG_VERDI = self.Utfør_kommando.Sti(self.Utfør_kommando.Les()['serial_log'])
        LOG_VERDI.write_text('saved log')
        self.Utfør_kommando.Utfør_kommando()
        self.assertFalse(any(Kommando[0] == 'make' or Kommando[1] == 'modifyvm' for Kommando in self.상자.명령들))
        self.assertEqual([Sti.read_text() for Sti in LOG_VERDI.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Pause_OG_CV(self):
        self.åpne_oppføring()['VMState'] = 'paused'
        self.Utfør_kommando.Utfør_kommando()
        self.assertTrue(any(Kommando[1] == 'controlvm' and Kommando[3] == 'resume' for Kommando in self.상자.명령들))
        self.assertFalse(any(Kommando[0] == 'make' for Kommando in self.상자.명령들))

    def test_Annet_VM_navn_konflikt(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_소유표식거부(self):
        self.åpne_oppføring()['owner'] = 'someone-else'
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.åpne_oppføring()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        maskin = self.åpne_oppføring()
        maskin['VMState'] = 'poweroff'
        maskin['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_전환중거부(self):
        self.åpne_oppføring()['VMState'] = 'saving'
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_등록해제거부(self):
        self.åpne_oppføring()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        maskin = self.åpne_oppføring()
        maskin['VMState'] = 'poweroff'
        Forrige_vare = dict(maskin)
        self.상자.feil_VERDI = 'make'
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.assertEqual(maskin, Forrige_vare)

    def test_중단된소유표식설정복구(self):
        self.상자.feil_VERDI = 'setextradata'
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()
        self.상자.명령들.clear()
        self.assertEqual(self.Utfør_kommando.Utfør_kommando()['state'], 'running')
        self.assertFalse(any(Kommando[1] == 'createvm' for Kommando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        maskin = self.åpne_oppføring()
        maskin['VMState'] = 'poweroff'
        Path(maskin['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Utfør_kommando()

    def test_상태미생성(self):
        self.assertEqual(self.Utfør_kommando.vise_status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Sti in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Sti(Sti)
        (self.rot_VERDI / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VERDI.kjøring_feil): self.Utfør_kommando.Sti('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        KR = modul_VERDI.attributtverdi('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(KR['VMState'], 'running')
        self.assertEqual(KR['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
