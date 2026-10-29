import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definitie_WAARDE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
module_WAARDE = importlib.util.module_from_spec(Definitie_WAARDE)
Definitie_WAARDE.loader.exec_module(module_WAARDE)


class 가짜상자:
    def __init__(self, wortel_WAARDE):
        self.wortel_WAARDE = wortel_WAARDE
        self.명령들 = []
        self.Virtual_Machines = {}
        self.fout_WAARDE = None

    def __call__(self, argumenten):
        argumenten = list(map(str, argumenten))
        self.명령들.append(argumenten)
        if self.fout_WAARDE == argumenten[1] or (argumenten[0] == 'make' and self.fout_WAARDE == 'make'):
            self.fout_WAARDE = None
            raise module_WAARDE.uitvoerbewerking_fout('시험용 fout_WAARDE')
        if argumenten[0] == 'make':
            pad = self.wortel_WAARDE / 'os/build/kernel.iso'
            pad.parent.mkdir(parents=True, exist_ok=True)
            pad.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Actie = argumenten[1]
        if Actie == 'list':
            return '\n'.join('"{}" {{{}}}'.format(WAARDE['name'], INDEX) for INDEX, WAARDE in self.Virtual_Machines.items())
        if Actie == 'createvm':
            INDEX, Naam = argumenten[argumenten.index('--uuid') + 1], argumenten[argumenten.index('--name') + 1]
            self.Virtual_Machines[INDEX] = {'UUID': INDEX, 'name': Naam, 'VMState': 'poweroff',
                'CfgFile': str(self.wortel_WAARDE / '.vbox/machines' / Naam / (Naam + '.vbox')), 'owner': None}
            return ''
        machine = self.Virtual_Machines[argumenten[2]]
        if Actie == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Naam), json.dumps(WAARDE)) for Naam, WAARDE in machine.items() if Naam != 'owner')
        if Actie == 'getextradata': return 'Value: ' + machine['owner'] if machine['owner'] else 'No value set!'
        if Actie == 'setextradata': machine['owner'] = argumenten[4]
        elif Actie == 'storagectl': machine['storagecontrollername0'] = 'JKOROS IDE'
        elif Actie == 'storageattach': machine['JKOROS IDE-0-0'] = argumenten[argumenten.index('--medium') + 1]
        elif Actie == 'startvm': machine['VMState'] = 'running'
        elif Actie == 'controlvm':
            assert argumenten[3] == 'resume'
            machine['VMState'] = 'running'
        elif Actie != 'modifyvm': raise AssertionError(argumenten)
        return ''


class test_uitvoeren(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.wortel_WAARDE = Path(self.임시.name)
        (self.wortel_WAARDE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.wortel_WAARDE)
        self.Uitvoeren_opdracht = module_WAARDE.app_app_lade(self.wortel_WAARDE, 'jkoros operating system', opdracht=self.상자)

    def maken_invoer(self):
        resultaat = self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[resultaat['uuid']]

    def 변경없음(self):
        self.assertTrue(all(opdracht[0] == 'VBoxManage' and opdracht[1] in ('list', 'showvminfo', 'getextradata') for opdracht in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        resultaat = self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.assertEqual(resultaat['state'], 'running')
        self.assertTrue(Path(resultaat['iso']).is_file())
        self.assertTrue(any('--nic1' in opdracht and 'none' in opdracht for opdracht in self.상자.명령들))
        self.assertFalse(any('hdd' in opdracht or 'discardstate' in opdracht or 'createmedium' in opdracht for opdracht in self.상자.명령들))

    def test_실행중유지(self):
        self.maken_invoer()
        self.assertEqual(self.Uitvoeren_opdracht.Uitvoeren_opdracht()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        machine = self.maken_invoer()
        machine['VMState'] = 'saved'
        LOG_WAARDE = self.Uitvoeren_opdracht.pad(self.Uitvoeren_opdracht.Lezen()['serial_log'])
        LOG_WAARDE.write_text('saved log')
        self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.assertFalse(any(opdracht[0] == 'make' or opdracht[1] == 'modifyvm' for opdracht in self.상자.명령들))
        self.assertEqual([pad.read_text() for pad in LOG_WAARDE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Onderbreken_EN_cv(self):
        self.maken_invoer()['VMState'] = 'paused'
        self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.assertTrue(any(opdracht[1] == 'controlvm' and opdracht[3] == 'resume' for opdracht in self.상자.명령들))
        self.assertFalse(any(opdracht[0] == 'make' for opdracht in self.상자.명령들))

    def test_Overige_VM_naam_conflict(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.변경없음()

    def test_소유표식거부(self):
        self.maken_invoer()['owner'] = 'someone-else'
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.maken_invoer()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        machine = self.maken_invoer()
        machine['VMState'] = 'poweroff'
        machine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.변경없음()

    def test_전환중거부(self):
        self.maken_invoer()['VMState'] = 'saving'
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.변경없음()

    def test_등록해제거부(self):
        self.maken_invoer()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        machine = self.maken_invoer()
        machine['VMState'] = 'poweroff'
        Vorige_item = dict(machine)
        self.상자.fout_WAARDE = 'make'
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.assertEqual(machine, Vorige_item)

    def test_중단된소유표식설정복구(self):
        self.상자.fout_WAARDE = 'setextradata'
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()
        self.상자.명령들.clear()
        self.assertEqual(self.Uitvoeren_opdracht.Uitvoeren_opdracht()['state'], 'running')
        self.assertFalse(any(opdracht[1] == 'createvm' for opdracht in self.상자.명령들))

    def test_보존ISO변조거부(self):
        machine = self.maken_invoer()
        machine['VMState'] = 'poweroff'
        Path(machine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.Uitvoeren_opdracht()

    def test_상태미생성(self):
        self.assertEqual(self.Uitvoeren_opdracht.weergeven_Status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for pad in ('../outside', '/tmp/outside'):
            with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.pad(pad)
        (self.wortel_WAARDE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(module_WAARDE.uitvoerbewerking_fout): self.Uitvoeren_opdracht.pad('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        resultaat = module_WAARDE.kenmerkwaarde('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(resultaat['VMState'], 'running')
        self.assertEqual(resultaat['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
