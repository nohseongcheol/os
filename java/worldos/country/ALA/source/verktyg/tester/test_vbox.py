import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definition_värde = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_värde = importlib.util.module_from_spec(Definition_värde)
Definition_värde.loader.exec_module(modul_värde)


class 가짜상자:
    def __init__(self, rot_värde):
        self.rot_värde = rot_värde
        self.명령들 = []
        self.Virtual_Machines = {}
        self.fel_värde = None

    def __call__(self, argument):
        argument = list(map(str, argument))
        self.명령들.append(argument)
        if self.fel_värde == argument[1] or (argument[0] == 'make' and self.fel_värde == 'make'):
            self.fel_värde = None
            raise modul_värde.körning_fel_3f02a041('시험용 fel_värde')
        if argument[0] == 'make':
            sökväg_2 = self.rot_värde / 'os/build/kernel.iso'
            sökväg_2.parent.mkdir(parents=True, exist_ok=True)
            sökväg_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Åtgärd = argument[1]
        if Åtgärd == 'list':
            return '\n'.join('"{}" {{{}}}'.format(värde['name'], INDEX) for INDEX, värde in self.Virtual_Machines.items())
        if Åtgärd == 'createvm':
            INDEX, Namn = argument[argument.index('--uuid') + 1], argument[argument.index('--name') + 1]
            self.Virtual_Machines[INDEX] = {'UUID': INDEX, 'name': Namn, 'VMState': 'poweroff',
                'CfgFile': str(self.rot_värde / '.vbox/machines' / Namn / (Namn + '.vbox')), 'owner': None}
            return ''
        dator = self.Virtual_Machines[argument[2]]
        if Åtgärd == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Namn), json.dumps(värde)) for Namn, värde in dator.items() if Namn != 'owner')
        if Åtgärd == 'getextradata': return 'Value: ' + dator['owner'] if dator['owner'] else 'No value set!'
        if Åtgärd == 'setextradata': dator['owner'] = argument[4]
        elif Åtgärd == 'storagectl': dator['storagecontrollername0'] = 'JKOROS IDE'
        elif Åtgärd == 'storageattach': dator['JKOROS IDE-0-0'] = argument[argument.index('--medium') + 1]
        elif Åtgärd == 'startvm': dator['VMState'] = 'running'
        elif Åtgärd == 'controlvm':
            assert argument[3] == 'resume'
            dator['VMState'] = 'running'
        elif Åtgärd != 'modifyvm': raise AssertionError(argument)
        return ''


class test_köra(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rot_värde = Path(self.임시.name)
        (self.rot_värde / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rot_värde)
        self.köra_kommando = modul_värde.app_Startbild(self.rot_värde, 'jkoros operating system', kommando=self.상자)

    def Skapa_post(self):
        RESULTAT = self.köra_kommando.köra_kommando()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[RESULTAT['uuid']]

    def 변경없음(self):
        self.assertTrue(all(kommando[0] == 'VBoxManage' and kommando[1] in ('list', 'showvminfo', 'getextradata') for kommando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        RESULTAT = self.köra_kommando.köra_kommando()
        self.assertEqual(RESULTAT['state'], 'running')
        self.assertTrue(Path(RESULTAT['iso']).is_file())
        self.assertTrue(any('--nic1' in kommando and 'none' in kommando for kommando in self.상자.명령들))
        self.assertFalse(any('hdd' in kommando or 'discardstate' in kommando or 'createmedium' in kommando for kommando in self.상자.명령들))

    def test_실행중유지(self):
        self.Skapa_post()
        self.assertEqual(self.köra_kommando.köra_kommando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        dator = self.Skapa_post()
        dator['VMState'] = 'saved'
        LOG_värde = self.köra_kommando.sökväg_2(self.köra_kommando.Läs()['serial_log'])
        LOG_värde.write_text('saved log')
        self.köra_kommando.köra_kommando()
        self.assertFalse(any(kommando[0] == 'make' or kommando[1] == 'modifyvm' for kommando in self.상자.명령들))
        self.assertEqual([sökväg_2.read_text() for sökväg_2 in LOG_värde.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Pausa_AND_CV(self):
        self.Skapa_post()['VMState'] = 'paused'
        self.köra_kommando.köra_kommando()
        self.assertTrue(any(kommando[1] == 'controlvm' and kommando[3] == 'resume' for kommando in self.상자.명령들))
        self.assertFalse(any(kommando[0] == 'make' for kommando in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.변경없음()

    def test_소유표식거부(self):
        self.Skapa_post()['owner'] = 'someone-else'
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Skapa_post()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        dator = self.Skapa_post()
        dator['VMState'] = 'poweroff'
        dator['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.변경없음()

    def test_전환중거부(self):
        self.Skapa_post()['VMState'] = 'saving'
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.변경없음()

    def test_등록해제거부(self):
        self.Skapa_post()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        dator = self.Skapa_post()
        dator['VMState'] = 'poweroff'
        Föregående_objekt = dict(dator)
        self.상자.fel_värde = 'make'
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.assertEqual(dator, Föregående_objekt)

    def test_중단된소유표식설정복구(self):
        self.상자.fel_värde = 'setextradata'
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()
        self.상자.명령들.clear()
        self.assertEqual(self.köra_kommando.köra_kommando()['state'], 'running')
        self.assertFalse(any(kommando[1] == 'createvm' for kommando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        dator = self.Skapa_post()
        dator['VMState'] = 'poweroff'
        Path(dator['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.köra_kommando()

    def test_상태미생성(self):
        self.assertEqual(self.köra_kommando.visa_status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for sökväg_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.sökväg_2(sökväg_2)
        (self.rot_värde / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_värde.körning_fel_3f02a041): self.köra_kommando.sökväg_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        RESULTAT = modul_värde.attribut_värde('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(RESULTAT['VMState'], 'running')
        self.assertEqual(RESULTAT['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
