import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definition_VÆRDI = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VÆRDI = importlib.util.module_from_spec(Definition_VÆRDI)
Definition_VÆRDI.loader.exec_module(modul_VÆRDI)


class 가짜상자:
    def __init__(self, rod_VÆRDI):
        self.rod_VÆRDI = rod_VÆRDI
        self.명령들 = []
        self.Virtual_Machines = {}
        self.fejl_VÆRDI = None

    def __call__(self, Argumenter):
        Argumenter = list(map(str, Argumenter))
        self.명령들.append(Argumenter)
        if self.fejl_VÆRDI == Argumenter[1] or (Argumenter[0] == 'make' and self.fejl_VÆRDI == 'make'):
            self.fejl_VÆRDI = None
            raise modul_VÆRDI.udførelse_fejl('시험용 fejl_VÆRDI')
        if Argumenter[0] == 'make':
            Sti = self.rod_VÆRDI / 'os/build/kernel.iso'
            Sti.parent.mkdir(parents=True, exist_ok=True)
            Sti.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Handling = Argumenter[1]
        if Handling == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VÆRDI['name'], INDEKS) for INDEKS, VÆRDI in self.Virtual_Machines.items())
        if Handling == 'createvm':
            INDEKS, Navn = Argumenter[Argumenter.index('--uuid') + 1], Argumenter[Argumenter.index('--name') + 1]
            self.Virtual_Machines[INDEKS] = {'UUID': INDEKS, 'name': Navn, 'VMState': 'poweroff',
                'CfgFile': str(self.rod_VÆRDI / '.vbox/machines' / Navn / (Navn + '.vbox')), 'owner': None}
            return ''
        maskine = self.Virtual_Machines[Argumenter[2]]
        if Handling == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Navn), json.dumps(VÆRDI)) for Navn, VÆRDI in maskine.items() if Navn != 'owner')
        if Handling == 'getextradata': return 'Value: ' + maskine['owner'] if maskine['owner'] else 'No value set!'
        if Handling == 'setextradata': maskine['owner'] = Argumenter[4]
        elif Handling == 'storagectl': maskine['storagecontrollername0'] = 'JKOROS IDE'
        elif Handling == 'storageattach': maskine['JKOROS IDE-0-0'] = Argumenter[Argumenter.index('--medium') + 1]
        elif Handling == 'startvm': maskine['VMState'] = 'running'
        elif Handling == 'controlvm':
            assert Argumenter[3] == 'resume'
            maskine['VMState'] = 'running'
        elif Handling != 'modifyvm': raise AssertionError(Argumenter)
        return ''


class testkørsel(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rod_VÆRDI = Path(self.임시.name)
        (self.rod_VÆRDI / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rod_VÆRDI)
        self.Udfør_kommando = modul_VÆRDI.app_Kvikstart(self.rod_VÆRDI, 'jkoros operating system', Kommando=self.상자)

    def åbne_post_81b8d99b(self):
        KR = self.Udfør_kommando.Udfør_kommando()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[KR['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Kommando[0] == 'VBoxManage' and Kommando[1] in ('list', 'showvminfo', 'getextradata') for Kommando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        KR = self.Udfør_kommando.Udfør_kommando()
        self.assertEqual(KR['state'], 'running')
        self.assertTrue(Path(KR['iso']).is_file())
        self.assertTrue(any('--nic1' in Kommando and 'none' in Kommando for Kommando in self.상자.명령들))
        self.assertFalse(any('hdd' in Kommando or 'discardstate' in Kommando or 'createmedium' in Kommando for Kommando in self.상자.명령들))

    def test_실행중유지(self):
        self.åbne_post_81b8d99b()
        self.assertEqual(self.Udfør_kommando.Udfør_kommando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        maskine = self.åbne_post_81b8d99b()
        maskine['VMState'] = 'saved'
        LOG_VÆRDI = self.Udfør_kommando.Sti(self.Udfør_kommando.Læse()['serial_log'])
        LOG_VÆRDI.write_text('saved log')
        self.Udfør_kommando.Udfør_kommando()
        self.assertFalse(any(Kommando[0] == 'make' or Kommando[1] == 'modifyvm' for Kommando in self.상자.명령들))
        self.assertEqual([Sti.read_text() for Sti in LOG_VÆRDI.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Afbryd_midlertidigt_OG_CV(self):
        self.åbne_post_81b8d99b()['VMState'] = 'paused'
        self.Udfør_kommando.Udfør_kommando()
        self.assertTrue(any(Kommando[1] == 'controlvm' and Kommando[3] == 'resume' for Kommando in self.상자.명령들))
        self.assertFalse(any(Kommando[0] == 'make' for Kommando in self.상자.명령들))

    def test_Andet_VM_navn_kollision(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.변경없음()

    def test_소유표식거부(self):
        self.åbne_post_81b8d99b()['owner'] = 'someone-else'
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.åbne_post_81b8d99b()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        maskine = self.åbne_post_81b8d99b()
        maskine['VMState'] = 'poweroff'
        maskine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.변경없음()

    def test_전환중거부(self):
        self.åbne_post_81b8d99b()['VMState'] = 'saving'
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.변경없음()

    def test_등록해제거부(self):
        self.åbne_post_81b8d99b()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        maskine = self.åbne_post_81b8d99b()
        maskine['VMState'] = 'poweroff'
        Forrige_vare = dict(maskine)
        self.상자.fejl_VÆRDI = 'make'
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.assertEqual(maskine, Forrige_vare)

    def test_중단된소유표식설정복구(self):
        self.상자.fejl_VÆRDI = 'setextradata'
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()
        self.상자.명령들.clear()
        self.assertEqual(self.Udfør_kommando.Udfør_kommando()['state'], 'running')
        self.assertFalse(any(Kommando[1] == 'createvm' for Kommando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        maskine = self.åbne_post_81b8d99b()
        maskine['VMState'] = 'poweroff'
        Path(maskine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Udfør_kommando()

    def test_상태미생성(self):
        self.assertEqual(self.Udfør_kommando.vise_status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Sti in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Sti(Sti)
        (self.rod_VÆRDI / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VÆRDI.udførelse_fejl): self.Udfør_kommando.Sti('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        KR = modul_VÆRDI.attribut_VÆRDI('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(KR['VMState'], 'running')
        self.assertEqual(KR['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
