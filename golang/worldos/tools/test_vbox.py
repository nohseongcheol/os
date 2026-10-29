import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import uuid
from unittest.mock import patch

import worldos_vbox as vbox
from install_vbox import install, FRAGMENT


class FakeVBox:
    def __init__(self, tree, existing=None):
        self.tree = tree
        self.calls = []
        self.vms = dict(existing or {})
        self.info = {}
        self.owner = {}
        self.registry = {}
        self.media = {'hdds': {}, 'dvds': {}}

    def __call__(self, args, **kwargs):
        args = [str(value) for value in args]
        self.calls.append(args)
        if args[0] == 'make':
            return 'build complete\n'
        if args[:3] == ['VBoxManage', 'list', 'vms']:
            return '\n'.join('"%s" {%s}' % (name, key) for key, name in self.vms.items())
        if args[:2] == ['VBoxManage', 'list'] and args[2] in self.media:
            return '\n\n'.join('UUID: %s\nLocation: %s\n' % (key, path) for key, path in self.media[args[2]].items())
        action = args[1]
        if action == 'showvminfo':
            return '\n'.join(json.dumps(key) + '=' + json.dumps(value) for key, value in self.info[args[2]].items())
        if action == 'getextradata':
            return 'Value: ' + self.owner.get(args[2], 'unrelated')
        if action == 'createvm':
            key, name = args[args.index('--uuid') + 1], args[args.index('--name') + 1]
            self.vms[key] = name
            self.info[key] = {'VMState': 'poweroff', 'CfgFile': str(self.tree / '.vbox/machines' / name / (name + '.vbox'))}
            self.registry[key] = Path(self.info[key]['CfgFile'])
        elif action == 'unregistervm':
            self.vms.pop(args[2]); self.info.pop(args[2]); self.registry.pop(args[2])
        elif action == 'registervm':
            cfg = Path(args[2])
            ns = {'v': 'http://www.virtualbox.org/'}
            machine = vbox.ET.parse(str(cfg)).getroot().find('v:Machine', ns)
            key = machine.get('uuid').strip('{}')
            self.vms[key] = machine.get('name')
            self.registry[key] = cfg
            self.info[key] = {'CfgFile': str(cfg), 'VMState': 'saved' if machine.get('stateFile') else 'poweroff',
                              'storagecontrollername0': 'IDE', 'storagecontrollertype0': 'PIIX4'}
            for node in machine.findall('v:ExtraData/v:ExtraDataItem', ns):
                if node.get('name') == 'WorldOS/Owner': self.owner[key] = node.get('value')
            for node in machine.findall('.//v:MediaRegistry//*[@location]', ns):
                port = 'IDE-0-1' if node.tag.endswith('HardDisk') else 'IDE-1-0'
                path = str(cfg.parent / node.get('location'))
                kind = 'hdds' if port == 'IDE-0-1' else 'dvds'
                medium_uuid = node.get('uuid', str(uuid.uuid4())).strip('{}')
                self.media[kind][medium_uuid] = path
                self.info[key][port] = path
                self.info[key][port.replace('IDE-', 'IDE-ImageUUID-')] = medium_uuid
        elif action == 'setextradata' and args[3] == 'WorldOS/Owner':
            self.owner[args[2]] = args[4]
        elif action == 'storagectl':
            self.info[args[2]].update({'storagecontrollername0': 'IDE', 'storagecontrollertype0': 'PIIX4'})
        elif action == 'storageattach':
            port, device = args[args.index('--port') + 1], args[args.index('--device') + 1]
            value = args[args.index('--medium') + 1]
            media = self.media['hdds' if args[args.index('--type') + 1] == 'hdd' else 'dvds']
            if value in media:
                medium_uuid, path = value, media[value]
            else:
                # Reproduce VirtualBox 5.2's non-normalized path registration.
                for medium_uuid, path in media.items():
                    if Path(path).resolve() == Path(value).resolve() and path != value:
                        raise vbox.LaunchError('Cannot register hard disk: UUID already exists')
                medium_uuid = next((key for key, path in media.items() if path == value), str(uuid.uuid4()))
                path = value
                media[medium_uuid] = path
            self.info[args[2]]['IDE-' + port + '-' + device] = path
            self.info[args[2]]['IDE-ImageUUID-' + port + '-' + device] = medium_uuid
        elif action == 'startvm':
            self.info[args[2]]['VMState'] = 'running'
        elif action == 'controlvm' and args[3] == 'resume':
            self.info[args[2]]['VMState'] = 'running'
        return ''


class VBoxTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='worldos-vbox-test-')
        self.root = Path(self.temporary.name)
        self.tree = self.root / '나라/KOR'
        (self.tree / '소스/build').mkdir(parents=True)
        (self.tree / '소스/Makefile').write_text('iso:\n\ttrue\n')
        (self.tree / '소스/build/kernel.iso').write_bytes(b'kernel-iso')
        (self.tree / 'Makefile').write_text('all:\n\ttrue\n')
        (self.tree / 'shell/build').mkdir(parents=True)
        (self.tree / 'shell-entry.json').write_text('{"directory":"shell"}')
        (self.tree / 'shell/shell.json').write_text('{"edition":"KOR"}')
        for name in ('worldos-shell', 'worldos-idle', 'worldos-shell-probe'):
            (self.tree / 'shell/build' / name).write_bytes(name.encode())
        (self.tree / 'posix-KOR').mkdir()
        (self.tree / 'posix-entry.json').write_text('{"directory":"posix-KOR"}')
        (self.tree / 'posix-KOR/posix.json').write_text('{"edition":"KOR"}')
        (self.root / 'tools').mkdir()
        source = Path(__file__).parent / 'worldos_vbox.py'
        shutil.copy2(str(source), str(self.root / 'tools/worldos_vbox.py'))
        self.base = self.root / 'original.vdi'
        self.base.write_bytes(b'original-user-data')
        self.record = ('KOR', self.tree, 'ko')
        self.install()
        self.fake = FakeVBox(self.tree)
        self.disks = []

    def tearDown(self):
        self.temporary.cleanup()

    def install(self, **kwargs):
        original = tempfile.mkdtemp
        def confined(*args, **values):
            values['dir'] = str(self.root)
            return original(*args, **values)
        with patch('install_vbox.tempfile.mkdtemp', side_effect=confined):
            return install(self.root, self.record, self.base, **kwargs)

    def disk(self, source, state_root, inputs, run):
        self.disks.append(source)
        path = state_root / 'media' / ('disk-%d.vdi' % len(self.disks))
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(source.read_bytes() + b'+updated-shell')
        return path, vbox.digest(source)

    def launch(self, action='run', env=None):
        with patch('worldos_vbox.shutil.which', return_value='/executable'), patch('worldos_vbox.prepare_disk', side_effect=self.disk), \
             patch('worldos_vbox.registered_path', side_effect=lambda key, env: self.fake.registry[key]):
            return vbox.launch(self.tree, action, env or {}, self.fake, lambda: None)

    def test_make_entry_and_independent_copy(self):
        self.assertIn(FRAGMENT, (self.tree / 'Makefile').read_text())
        self.assertEqual((self.tree / 'vbox.py').read_bytes(), (self.root / 'tools/worldos_vbox.py').read_bytes())
        self.install(check=True)
        vbox.validate(self.tree)

    def test_refresh_preserves_extra_files_and_rejects_edits(self):
        (self.tree / 'user-file').write_text('keep')
        self.install(refresh=True)
        self.assertEqual((self.tree / 'user-file').read_text(), 'keep')
        (self.tree / 'vbox.py').write_text('user edit')
        with self.assertRaises(vbox.LaunchError):
            self.install(refresh=True)

    def test_new_vm_builds_attaches_correct_ports_and_starts_gui(self):
        self.launch()
        state = vbox.read_json(self.tree / '.vbox/state.json')
        self.assertEqual(self.fake.info[state['vm_uuid']]['VMState'], 'running')
        attachments = [call for call in self.fake.calls if call[1] == 'storageattach']
        self.assertEqual(len(attachments), 2)
        self.assertIn(['--port', '0', '--device', '1'], [call[5:9] for call in attachments])
        self.assertEqual(self.fake.calls[-1][-2:], ['--type', 'gui'])
        self.assertEqual(self.base.read_bytes(), b'original-user-data')
        self.assertEqual(len(self.disks), 1)
        self.assertIn(['make', '-B', '-C', str(self.tree / '소스'), 'iso'], self.fake.calls)

    def test_running_vm_is_not_rebuilt_or_powered_off(self):
        self.launch()
        self.fake.calls.clear()
        self.launch()
        self.assertTrue(all(call[1] in ('list', 'showvminfo', 'getextradata') for call in self.fake.calls))
        self.assertEqual(len(self.disks), 1)

    def test_localized_kernel_directory_is_used_for_build_and_iso(self):
        (self.tree / '소스').rename(self.tree / '源代码')
        entry = vbox.read_json(self.tree / 'vbox-entry.json')
        entry['kernel_directory'] = '源代码'
        vbox.write_json(self.tree / 'vbox-entry.json', entry)
        self.launch()
        self.assertIn(['make', '-B', '-C', str(self.tree / '源代码'), 'iso'], self.fake.calls)
        self.assertEqual(self.base.read_bytes(), b'original-user-data')

    def suspended_vm(self, vm_state):
        self.launch()
        state = vbox.read_json(self.tree / '.vbox/state.json')
        self.fake.info[state['vm_uuid']]['VMState'] = vm_state
        self.fake.calls.clear()
        return state

    def preserved_resume_files(self):
        state = vbox.read_json(self.tree / '.vbox/state.json')
        paths = [self.tree / '.vbox/state.json', self.base]
        paths.extend(self.tree / '.vbox' / path for path in state['media_history'])
        return {str(path): path.read_bytes() for path in paths}

    def test_saved_vm_resumes_without_rebuilding_or_replacing_media(self):
        state = self.suspended_vm('saved')
        before = self.preserved_resume_files()
        self.launch()
        self.assertEqual(self.fake.info[state['vm_uuid']]['VMState'], 'running')
        mutations = [call for call in self.fake.calls if call[1] not in ('list', 'showvminfo', 'getextradata')]
        self.assertEqual(mutations, [['VBoxManage', 'startvm', state['vm_uuid'], '--type', 'gui']])
        self.assertEqual(self.preserved_resume_files(), before)
        self.assertEqual(len(self.disks), 1)

    def test_saved_vm_can_resume_headless_without_build_tools_or_base_disk(self):
        state = self.suspended_vm('saved')
        self.base.unlink()
        def executable(name):
            return '/executable' if name == 'VBoxManage' else None
        with patch('worldos_vbox.shutil.which', side_effect=executable), patch('worldos_vbox.prepare_disk', side_effect=AssertionError('no disk preparation')):
            vbox.launch(self.tree, 'run', {'VBOX_TYPE': 'headless'}, self.fake, lambda: None)
        self.assertEqual(self.fake.calls[-1], ['VBoxManage', 'startvm', state['vm_uuid'], '--type', 'headless'])

    def test_paused_vm_resumes_without_restarting(self):
        state = self.suspended_vm('paused')
        before = self.preserved_resume_files()
        self.launch()
        self.assertEqual(self.fake.info[state['vm_uuid']]['VMState'], 'running')
        mutations = [call for call in self.fake.calls if call[1] not in ('list', 'showvminfo', 'getextradata')]
        self.assertEqual(mutations, [['VBoxManage', 'controlvm', state['vm_uuid'], 'resume']])
        self.assertEqual(self.preserved_resume_files(), before)

    def test_prepare_never_resumes_saved_or_paused_vm(self):
        state = self.suspended_vm('saved')
        before = self.preserved_resume_files()
        for vm_state in ('saved', 'paused'):
            with self.subTest(vm_state=vm_state):
                self.fake.info[state['vm_uuid']]['VMState'] = vm_state
                self.fake.calls.clear()
                with self.assertRaisesRegex(vbox.LaunchError, 'Use make vbox to resume'):
                    self.launch('prepare')
                self.assertTrue(all(call[1] in ('list', 'showvminfo', 'getextradata') for call in self.fake.calls))
                self.assertEqual(self.preserved_resume_files(), before)

    def test_busy_vm_is_preserved(self):
        state = self.suspended_vm('saving')
        for vm_state in ('saving', 'restoring', 'starting', 'stopping', 'gurumeditation', 'unknown'):
            with self.subTest(vm_state=vm_state):
                self.fake.info[state['vm_uuid']]['VMState'] = vm_state
                self.fake.calls.clear()
                with self.assertRaisesRegex(vbox.LaunchError, 'unsupported state'):
                    self.launch()
                self.assertTrue(all(call[1] in ('list', 'showvminfo', 'getextradata') for call in self.fake.calls))

    def test_resume_failure_does_not_fall_back_to_discard_or_cold_boot(self):
        state = self.suspended_vm('saved')
        before = self.preserved_resume_files()
        previous = self.fake
        def fail_resume(args, **kwargs):
            if args[1] == 'startvm':
                previous.calls.append(args)
                raise vbox.LaunchError('restore failed')
            return previous(args, **kwargs)
        self.fake = fail_resume
        with self.assertRaisesRegex(vbox.LaunchError, 'restore failed') as raised:
            self.launch()
        self.assertIn('저장 상태 삭제', str(raised.exception))
        self.assertEqual(previous.info[state['vm_uuid']]['VMState'], 'saved')
        self.assertEqual(self.preserved_resume_files(), before)
        self.assertTrue(all(call[1] in ('list', 'showvminfo', 'getextradata', 'startvm') for call in previous.calls))

    def test_resume_checks_ownership_before_starting(self):
        state = self.suspended_vm('saved')
        self.fake.owner[state['vm_uuid']] = 'unrelated'
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        self.assertTrue(all(call[1] in ('list', 'showvminfo', 'getextradata') for call in self.fake.calls))

    def test_foreign_name_collision_never_modifies_vm(self):
        self.fake.vms['11111111-1111-1111-1111-111111111111'] = 'worldos KOR'
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        self.assertEqual(self.fake.calls, [['VBoxManage', 'list', 'vms']])
        self.launch(env={'VBOX_VM_NAME': 'worldos KOR new'})

    def test_stopped_vm_reuses_disk_and_update_clones_current_data(self):
        self.launch('prepare')
        state = vbox.read_json(self.tree / '.vbox/state.json')
        old = self.tree / '.vbox' / state['disk']
        old.write_bytes(b'guest-user-data')
        self.launch('prepare')
        self.assertEqual(len(self.disks), 1)
        (self.tree / 'shell/build/worldos-shell').write_bytes(b'new-shell')
        self.launch('prepare')
        self.assertEqual(self.disks[-1], old)
        self.assertEqual(old.read_bytes(), b'guest-user-data')
        self.assertEqual(self.base.read_bytes(), b'original-user-data')
        self.assertEqual(len([call for call in self.fake.calls if call[1] == 'createvm']), 1)

    def test_ownership_or_external_medium_changes_are_rejected(self):
        self.launch('prepare')
        state = vbox.read_json(self.tree / '.vbox/state.json')
        key = state['vm_uuid']
        self.fake.owner[key] = 'other'
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        self.fake.owner[key] = state['owner']
        self.fake.info[key]['IDE-0-1'] = str(self.base)
        with self.assertRaises(vbox.LaunchError):
            self.launch()

    def test_status_and_check_do_not_create_state(self):
        self.launch('check')
        self.launch('status')
        self.assertFalse((self.tree / '.vbox').exists())
        self.assertFalse(self.fake.calls)

    def test_symlink_paths_and_invalid_frontend_are_rejected(self):
        (self.tree / '.vbox').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        (self.tree / '.vbox').unlink()
        with self.assertRaises(vbox.LaunchError):
            self.launch(env={'VBOX_TYPE': 'invalid'})

    def test_machine_readable_output_with_metadata_and_spaces(self):
        parsed = vbox.properties('name="worldos KOR"\n"IDE-0-1"="/a path/disk.vdi"\nVMState="poweroff"\nVideoMode="720,400,0"@0,0 1\n')
        self.assertEqual(parsed['IDE-0-1'], '/a path/disk.vdi')
        self.assertEqual(parsed['VMState'], 'poweroff')
        self.assertEqual(parsed['VideoMode'], '"720,400,0"@0,0 1')
        with self.assertRaises(vbox.LaunchError):
            vbox.safe(self.root, '../elsewhere')

    def test_build_failure_never_creates_or_modifies_vm(self):
        previous = self.fake
        def fail_build(args, **kwargs):
            if args[0] == 'make':
                raise vbox.LaunchError('build failed')
            return previous(args, **kwargs)
        self.fake = fail_build
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        self.assertFalse(previous.vms)
        self.assertEqual(self.base.read_bytes(), b'original-user-data')

    def test_vm_started_during_build_is_never_reconfigured(self):
        self.launch('prepare')
        state = vbox.read_json(self.tree / '.vbox/state.json')
        original_state = (self.tree / '.vbox/state.json').read_bytes()
        previous = self.fake
        previous.calls.clear()
        def start_during_build(args, **kwargs):
            if args[0] == 'make':
                previous.info[state['vm_uuid']]['VMState'] = 'running'
            return previous(args, **kwargs)
        self.fake = start_during_build
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        self.assertEqual((self.tree / '.vbox/state.json').read_bytes(), original_state)
        self.assertFalse(any(call[1] in ('modifyvm', 'storagectl', 'storageattach', 'startvm') for call in previous.calls))

    def test_changed_controller_is_not_overwritten(self):
        self.launch('prepare')
        state = vbox.read_json(self.tree / '.vbox/state.json')
        self.fake.info[state['vm_uuid']]['storagecontrollertype0'] = 'PIIX3'
        self.fake.calls.clear()
        with self.assertRaises(vbox.LaunchError):
            self.launch()
        self.assertFalse(any(call[1] == 'modifyvm' for call in self.fake.calls))

    def moved_fixture(self, legacy=True, copy=False):
        self.launch('prepare')
        state_file = self.tree / '.vbox/state.json'
        state, _ = vbox.load_state(self.tree / '.vbox', vbox.read_json(state_file), 'KOR')
        key = state['vm_uuid']
        cfg = self.fake.registry[key]
        cfg.parent.mkdir(parents=True)
        ns = 'http://www.virtualbox.org/'
        tag = lambda name: '{' + ns + '}' + name
        xml = vbox.ET.Element(tag('VirtualBox'))
        machine = vbox.ET.SubElement(xml, tag('Machine'), uuid='{' + key + '}', name=state['name'],
                                     stateFile='Snapshots/test.sav', snapshotFolder='Snapshots')
        media = vbox.ET.SubElement(machine, tag('MediaRegistry'))
        for keyname, group, node in [('disk', 'HardDisks', 'HardDisk'), ('iso', 'DVDImages', 'Image')]:
            slot = 'IDE-ImageUUID-0-1' if keyname == 'disk' else 'IDE-ImageUUID-1-0'
            vbox.ET.SubElement(vbox.ET.SubElement(media, tag(group)), tag(node), location=state[keyname],
                               uuid='{' + self.fake.info[key][slot] + '}')
        extra = vbox.ET.SubElement(machine, tag('ExtraData'))
        for name, value in [('WorldOS/Owner', state['owner']), ('WorldOS/Edition', 'KOR')]:
            vbox.ET.SubElement(extra, tag('ExtraDataItem'), name=name, value=value)
        uart = vbox.ET.SubElement(vbox.ET.SubElement(machine, tag('Hardware')), tag('UART'))
        vbox.ET.SubElement(uart, tag('Port'), hostMode='RawFile', path=state['serial_log'])
        vbox.ET.ElementTree(xml).write(str(cfg), encoding='utf-8', xml_declaration=True)
        (cfg.parent / 'Snapshots').mkdir()
        (cfg.parent / 'Snapshots/test.sav').write_bytes(b'saved-RAM-user-work')
        if legacy:
            state['version'] = 1
            state.pop('last_location', None); state.pop('path_base', None)
            vbox.write_json(state_file, state)
        self.old_tree = self.tree
        target = self.root / 'moved workspace/나라/KOR'
        target.parent.mkdir(parents=True)
        if copy: shutil.copytree(str(self.tree), str(target))
        else: self.tree.rename(target)
        self.tree = target
        self.fake.tree = target
        self.fake.info[key] = {'name': '<inaccessible>', 'UUID': key}
        self.fake.calls.clear()
        return state

    def test_new_state_paths_are_relative_and_base_is_relative_to_edition(self):
        self.base.rename(self.tree / 'base with spaces.vdi')
        self.launch('prepare', {'VBOX_BASE_DISK': 'base with spaces.vdi'})
        state = vbox.read_json(self.tree / '.vbox/state.json')
        self.assertEqual(state['version'], 2)
        for key in ('disk', 'iso', 'serial_log'):
            self.assertFalse(Path(state[key]).is_absolute())
        self.assertEqual(self.disks, [self.tree / 'base with spaces.vdi'])

    def test_moved_legacy_saved_vm_preserves_data_and_resumes(self):
        state = self.moved_fixture()
        media = {p.name: p.read_bytes() for p in (self.tree / '.vbox/media').iterdir()}
        self.launch()
        self.assertEqual(self.fake.info[state['vm_uuid']]['VMState'], 'running')
        self.assertEqual(media, {p.name: p.read_bytes() for p in (self.tree / '.vbox/media').iterdir()})
        self.assertEqual((self.fake.registry[state['vm_uuid']].parent / 'Snapshots/test.sav').read_bytes(), b'saved-RAM-user-work')
        self.assertEqual(len(self.disks), 1)
        self.assertTrue(all(call[0] == 'VBoxManage' for call in self.fake.calls))
        mutations = [call[1] for call in self.fake.calls if call[1] not in ('list', 'showvminfo', 'getextradata')]
        self.assertEqual(mutations, ['unregistervm', 'registervm', 'startvm'])
        self.assertNotIn('--delete', [value for call in self.fake.calls for value in call])
        saved = vbox.read_json(self.tree / '.vbox/state.json')
        self.assertEqual(saved['disk'], 'media/disk-1.vdi')
        self.assertTrue(list((self.tree / '.vbox').glob('relocation-backup-*/state.json')))

    def test_relative_state_survives_two_directory_moves(self):
        state = self.moved_fixture(legacy=False)
        self.launch('relocate')
        previous = self.tree
        self.tree = self.root / 'another parent/나라/KOR'
        self.tree.parent.mkdir(parents=True)
        previous.rename(self.tree)
        self.fake.tree = self.tree
        self.fake.info[state['vm_uuid']] = {'name': '<inaccessible>'}
        self.launch('relocate')
        self.assertEqual(self.fake.registry[state['vm_uuid']], self.tree / '.vbox/machines/worldos KOR/worldos KOR.vbox')
        self.assertEqual(self.fake.info[state['vm_uuid']]['VMState'], 'saved')

    def test_moved_status_is_read_only(self):
        self.moved_fixture()
        before = (self.tree / '.vbox/state.json').read_bytes()
        self.launch('status')
        self.assertEqual((self.tree / '.vbox/state.json').read_bytes(), before)
        self.assertFalse(self.fake.calls)

    def test_copy_cannot_take_over_original_vm(self):
        self.moved_fixture(copy=True)
        with self.assertRaisesRegex(vbox.LaunchError, 'Previous edition still exists'):
            self.launch('relocate')
        self.assertEqual(self.fake.calls, [['VBoxManage', 'list', 'vms']])

    def test_moved_ownership_mismatch_never_unregisters_vm(self):
        state = self.moved_fixture()
        cfg = self.tree / '.vbox/machines/worldos KOR/worldos KOR.vbox'
        cfg.write_bytes(cfg.read_bytes().replace(state['owner'].encode(), b'foreign-owner'))
        with self.assertRaisesRegex(vbox.LaunchError, 'ownership/edition'):
            self.launch('relocate')
        self.assertFalse(any(call[1] == 'unregistervm' for call in self.fake.calls))

    def test_moved_missing_saved_state_never_unregisters_vm(self):
        self.moved_fixture()
        (self.tree / '.vbox/machines/worldos KOR/Snapshots/test.sav').unlink()
        with self.assertRaisesRegex(vbox.LaunchError, 'Missing saved execution'):
            self.launch('relocate')
        self.assertFalse(any(call[1] == 'unregistervm' for call in self.fake.calls))

    def test_moved_active_vm_is_not_changed(self):
        state = self.moved_fixture()
        self.fake.info[state['vm_uuid']] = {'VMState': 'running', 'CfgFile': str(self.fake.registry[state['vm_uuid']])}
        with self.assertRaisesRegex(vbox.LaunchError, 'active or busy'):
            self.launch('relocate')
        self.assertFalse(any(call[1] == 'unregistervm' for call in self.fake.calls))

    def test_relative_traversal_and_symlinks_are_rejected(self):
        self.launch('prepare')
        path = self.tree / '.vbox/state.json'
        raw = vbox.read_json(path)
        for bad in ('../outside.vdi', 'media/../../outside.vdi', '/other/.vbox/media/file.vdi'):
            value = dict(raw, disk=bad)
            vbox.write_json(path, value)
            with self.assertRaises(vbox.LaunchError): self.launch()
        vbox.write_json(path, raw)
        disk = self.tree / '.vbox' / raw['disk']
        disk.unlink(); disk.symlink_to(self.base)
        with self.assertRaisesRegex(vbox.LaunchError, 'symbolic link'): self.launch()

    def test_relative_tree_argument_works_from_another_directory(self):
        vbox.launch(Path(os.path.relpath(str(self.tree))), 'check', {}, self.fake, lambda: None)

    def test_wrong_registration_cannot_be_replaced(self):
        state = self.moved_fixture()
        self.fake.registry[state['vm_uuid']] = self.root / 'unrelated.vbox'
        with self.assertRaisesRegex(vbox.LaunchError, 'not the previous edition'):
            self.launch('relocate')
        self.assertFalse(any(call[1] == 'unregistervm' for call in self.fake.calls))

    def test_failed_registration_is_retryable_without_deleting_saved_data(self):
        state = self.moved_fixture()
        previous = self.fake
        before = (self.tree / '.vbox/state.json').read_bytes()
        def fail(args, **kwargs):
            if args[1] == 'registervm': raise vbox.LaunchError('injected register failure')
            return previous(args, **kwargs)
        with patch('worldos_vbox.shutil.which', return_value='/executable'), \
             patch('worldos_vbox.registered_path', side_effect=lambda key, env: previous.registry[key]):
            with self.assertRaisesRegex(vbox.LaunchError, 'registration repair failed'):
                vbox.launch(self.tree, 'relocate', {}, fail, lambda: None)
        self.assertEqual((self.tree / '.vbox/state.json').read_bytes(), before)
        self.assertNotIn(state['vm_uuid'], previous.vms)
        self.launch('relocate')
        self.assertEqual(previous.info[state['vm_uuid']]['VMState'], 'saved')
        self.assertEqual((previous.registry[state['vm_uuid']].parent / 'Snapshots/test.sav').read_bytes(), b'saved-RAM-user-work')

    def test_cold_boot_after_move_reuses_registered_media_uuids(self):
        state = self.moved_fixture()
        self.launch('relocate')
        info = self.fake.info[state['vm_uuid']]
        info['VMState'] = 'poweroff'
        self.assertIn('/../../media/', info['IDE-0-1'])
        expected = [info['IDE-ImageUUID-0-1'], info['IDE-ImageUUID-1-0']]
        before = {p.name: p.read_bytes() for p in (self.tree / '.vbox/media').iterdir()}
        self.fake.calls.clear()
        self.launch()
        attachments = [call[call.index('--medium') + 1] for call in self.fake.calls if call[1] == 'storageattach']
        self.assertEqual(attachments, expected)
        self.assertEqual(info['VMState'], 'running')
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.tree / '.vbox/media').iterdir()})
        self.assertFalse(any(call[1] in ('unregistervm', 'closemedium', 'internalcommands') for call in self.fake.calls))

    def test_detached_media_are_found_by_canonical_path(self):
        state = self.moved_fixture()
        self.launch('relocate')
        info = self.fake.info[state['vm_uuid']]
        info['VMState'] = 'poweroff'
        expected = [info['IDE-ImageUUID-0-1'], info['IDE-ImageUUID-1-0']]
        info['IDE-0-1'] = info['IDE-1-0'] = 'none'
        self.fake.calls.clear()
        self.launch('prepare')
        attachments = [call[call.index('--medium') + 1] for call in self.fake.calls if call[1] == 'storageattach']
        self.assertEqual(attachments, expected)
        self.assertIn(['VBoxManage', 'list', 'hdds'], self.fake.calls)
        self.assertIn(['VBoxManage', 'list', 'dvds'], self.fake.calls)

    def test_same_basename_is_not_treated_as_same_medium(self):
        target = self.tree / '.vbox/media/disk.vdi'
        self.fake.media['hdds']['00000000-0000-0000-0000-000000000001'] = str(self.root / 'other/disk.vdi')
        self.assertEqual(vbox.medium_reference(target, 'hdd', {}, self.fake), str(target))

    def test_ambiguous_registry_path_is_rejected(self):
        target = self.tree / '.vbox/media/disk.vdi'
        self.fake.media['hdds'] = {'00000000-0000-0000-0000-000000000001': str(target),
            '00000000-0000-0000-0000-000000000002': str(target.parent / 'nested/../disk.vdi')}
        with self.assertRaisesRegex(vbox.LaunchError, 'Multiple registered UUIDs'):
            vbox.medium_reference(target, 'hdd', {}, self.fake)


if __name__ == '__main__':
    unittest.main()
