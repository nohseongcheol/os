import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

definitionValue = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBoxManager.py'))
moduleValue = importlib.util.module_from_spec(definitionValue)
definitionValue.loader.exec_module(moduleValue)


class FakeBox:
    def __init__(self, rootValue):
        self.rootValue = rootValue
        self.commandsList = []
        self.virtualMachines = {}
        self.failureValue = None

    def __call__(self, arguments):
        arguments = list(map(str, arguments))
        self.commandsList.append(arguments)
        if self.failureValue == arguments[1] or (arguments[0] == 'make' and self.failureValue == 'make'):
            self.failureValue = None
            raise moduleValue.executionError('시험용 failureValue')
        if arguments[0] == 'make':
            path = self.rootValue / 'os/build/kernel.iso'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        action = arguments[1]
        if action == 'list':
            return '\n'.join('"{}" {{{}}}'.format(value['name'], index) for index, value in self.virtualMachines.items())
        if action == 'createvm':
            index, name = arguments[arguments.index('--uuid') + 1], arguments[arguments.index('--name') + 1]
            self.virtualMachines[index] = {'UUID': index, 'name': name, 'VMState': 'poweroff',
                'CfgFile': str(self.rootValue / '.vbox/machines' / name / (name + '.vbox')), 'owner': None}
            return ''
        machine = self.virtualMachines[arguments[2]]
        if action == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(name), json.dumps(value)) for name, value in machine.items() if name != 'owner')
        if action == 'getextradata': return 'Value: ' + machine['owner'] if machine['owner'] else 'No value set!'
        if action == 'setextradata': machine['owner'] = arguments[4]
        elif action == 'storagectl': machine['storagecontrollername0'] = 'JKOROS IDE'
        elif action == 'storageattach': machine['JKOROS IDE-0-0'] = arguments[arguments.index('--medium') + 1]
        elif action == 'startvm': machine['VMState'] = 'running'
        elif action == 'controlvm':
            assert arguments[3] == 'resume'
            machine['VMState'] = 'running'
        elif action != 'modifyvm': raise AssertionError(arguments)
        return ''


class testRun(unittest.TestCase):
    def setUp(self):
        self.temporaryValue = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.temporaryValue.cleanup)
        self.rootValue = Path(self.temporaryValue.name)
        (self.rootValue / '.vbox').mkdir()
        self.boxValue = FakeBox(self.rootValue)
        self.executeCommand = moduleValue.ProgramLauncher(self.rootValue, 'jkoros operating system', command=self.boxValue)

    def createEntry(self):
        result = self.executeCommand.executeCommand()
        self.boxValue.commandsList.clear()
        return self.boxValue.virtualMachines[result['uuid']]

    def isUnchanged(self):
        self.assertTrue(all(command[0] == 'VBoxManage' and command[1] in ('list', 'showvminfo', 'getextradata') for command in self.boxValue.commandsList))

    def test_initial_creation_and_optical_boot(self):
        result = self.executeCommand.executeCommand()
        self.assertEqual(result['state'], 'running')
        self.assertTrue(Path(result['iso']).is_file())
        self.assertTrue(any('--nic1' in command and 'none' in command for command in self.boxValue.commandsList))
        self.assertFalse(any('hdd' in command or 'discardstate' in command or 'createmedium' in command for command in self.boxValue.commandsList))

    def test_running_vm_preserved(self):
        self.createEntry()
        self.assertEqual(self.executeCommand.executeCommand()['state'], 'running')
        self.isUnchanged()

    def test_saved_state_resume_and_log_preservation(self):
        machine = self.createEntry()
        machine['VMState'] = 'saved'
        logValue = self.executeCommand.path(self.executeCommand.read()['serial_log'])
        logValue.write_text('saved log')
        self.executeCommand.executeCommand()
        self.assertFalse(any(command[0] == 'make' or command[1] == 'modifyvm' for command in self.boxValue.commandsList))
        self.assertEqual([path.read_text() for path in logValue.parent.glob('before-resume-*.log')], ['saved log'])

    def test_pause_and_resume(self):
        self.createEntry()['VMState'] = 'paused'
        self.executeCommand.executeCommand()
        self.assertTrue(any(command[1] == 'controlvm' and command[3] == 'resume' for command in self.boxValue.commandsList))
        self.assertFalse(any(command[0] == 'make' for command in self.boxValue.commandsList))

    def test_other_vm_name_collision(self):
        self.boxValue.virtualMachines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.isUnchanged()

    def test_ownership_marker_rejected(self):
        self.createEntry()['owner'] = 'someone-else'
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.isUnchanged()

    def test_other_settings_path_rejected(self):
        self.createEntry()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.isUnchanged()

    def test_additional_user_disk_preserved(self):
        machine = self.createEntry()
        machine['VMState'] = 'poweroff'
        machine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.isUnchanged()

    def test_transition_rejected(self):
        self.createEntry()['VMState'] = 'saving'
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.isUnchanged()

    def test_unregister_rejected(self):
        self.createEntry()
        self.boxValue.virtualMachines.clear()
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.isUnchanged()

    def test_vm_preserved_on_build_failure(self):
        machine = self.createEntry()
        machine['VMState'] = 'poweroff'
        previousItem = dict(machine)
        self.boxValue.failureValue = 'make'
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.assertEqual(machine, previousItem)

    def test_interrupted_ownership_marker_recovery(self):
        self.boxValue.failureValue = 'setextradata'
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()
        self.boxValue.commandsList.clear()
        self.assertEqual(self.executeCommand.executeCommand()['state'], 'running')
        self.assertFalse(any(command[1] == 'createvm' for command in self.boxValue.commandsList))

    def test_preserved_iso_tampering_rejected(self):
        machine = self.createEntry()
        machine['VMState'] = 'poweroff'
        Path(machine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(moduleValue.executionError): self.executeCommand.executeCommand()

    def test_no_state_created(self):
        self.assertEqual(self.executeCommand.showState()['state'], 'not-created')
        self.assertFalse(self.boxValue.commandsList)

    def test_path_escape_rejected(self):
        for path in ('../outside', '/tmp/outside'):
            with self.assertRaises(moduleValue.executionError): self.executeCommand.path(path)
        (self.rootValue / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(moduleValue.executionError): self.executeCommand.path('media/kernel.iso')

    def test_virtualbox52_composite_properties(self):
        result = moduleValue.attributeValue('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(result['VMState'], 'running')
        self.assertEqual(result['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
