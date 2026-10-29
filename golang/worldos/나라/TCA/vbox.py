#!/usr/bin/env python3
"""Standalone, non-destructive VirtualBox launcher copied into every edition.

Builds only this edition. Base disk is read-only; updates clone the current disk.
Never adopts unrelated VMs, powers off guests, deletes disks, or invokes sudo.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET


class LaunchError(RuntimeError):
    pass


def safe(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise LaunchError('Unsafe relative path: ' + str(relative))
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise LaunchError('Refusing symbolic link: ' + str(current))
    return current


def digest(path):
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(block)
    return checksum.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, value):
    if path.is_symlink():
        raise LaunchError('Refusing symbolic link: ' + str(path))
    with tempfile.NamedTemporaryFile(mode='w', dir=str(path.parent), encoding='utf-8', delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(str(temporary), str(path))


def load_state(state_root, value, edition):
    """Resolve owned paths against this edition, including old absolute records.

    last_location is only a registration-migration hint, never a file read root.
    The returned runtime state uses absolute paths; the disk record is relative.
    """
    state = json.loads(json.dumps(value))
    if state.get('version') not in (1, 2) or state.get('edition') != edition:
        raise LaunchError('Launch state belongs to another edition or version')
    if state.get('version') == 2:
        if state.get('path_base') != '.vbox':
            raise LaunchError('Unknown managed path base')
        previous = Path(state.get('last_location', str(state_root)))
    else:
        paths = state.get('media_history', [])
        sample = state.get('disk') or state.get('iso') or (paths[0] if paths else None)
        previous = Path(sample).parent.parent if sample and Path(sample).is_absolute() else state_root
    if not previous.is_absolute() or previous.name != '.vbox' or '..' in previous.parts:
        raise LaunchError('Invalid previous managed directory')
    if previous != state_root:
        # Legacy locations must describe the same edition, not arbitrary files
        # with a coincidentally matching basename.
        suffix = tuple(edition.split('/'))
        if previous.parent.parts[-len(suffix):] != suffix:
            raise LaunchError('Previous managed path belongs to another edition')

    def local(value, folder):
        path = Path(value)
        if path.is_absolute():
            try:
                path = path.relative_to(previous)
            except ValueError:
                try:
                    path = path.relative_to(state_root)
                except ValueError:
                    raise LaunchError('Managed path leaves this edition: ' + str(value))
        if len(path.parts) < 2 or path.parts[0] != folder:
            raise LaunchError('Invalid managed ' + folder + ' path: ' + str(value))
        return str(safe(state_root, path))

    state['media_history'] = [local(p, 'media') for p in state.get('media_history', [])]
    for key, folder in (('disk', 'media'), ('iso', 'media'), ('serial_log', 'logs')):
        if state.get(key): state[key] = local(state[key], folder)
    for key in ('disk', 'iso'):
        if state.get(key) and state[key] not in state['media_history']:
            raise LaunchError('Current ' + key + ' is not in managed media history')
    for generation in state.get('disk_generations', []):
        generation['disk'] = local(generation['disk'], 'media')
        source = Path(generation['source'])
        if not source.is_absolute() or previous in source.parents or state_root in source.parents:
            generation['source'] = local(source, 'media')
    return state, previous


def save_state(state_root, state):
    value = json.loads(json.dumps(state))
    def relative(path):
        return str(Path(path).relative_to(state_root))
    value.update(version=2, path_base='.vbox', last_location=str(state_root))
    value['media_history'] = [relative(p) for p in value.get('media_history', [])]
    for key in ('disk', 'iso', 'serial_log'):
        if value.get(key): value[key] = relative(value[key])
    for generation in value.get('disk_generations', []):
        generation['disk'] = relative(generation['disk'])
        if state_root in Path(generation['source']).parents:
            generation['source'] = relative(generation['source'])
    write_json(safe(state_root, 'state.json'), value)


def registered_path(identifier, environment):
    """VBox 5.2 showvminfo omits CfgFile for inaccessible registrations."""
    home = Path.home()
    if environment.get('VBOX_USER_HOME'):
        candidates = [Path(environment['VBOX_USER_HOME']) / 'VirtualBox.xml']
    else:
        config = Path(environment.get('XDG_CONFIG_HOME') or str(home / '.config'))
        candidates = [config / 'VirtualBox/VirtualBox.xml', home / '.VirtualBox/VirtualBox.xml',
                      home / 'Library/VirtualBox/VirtualBox.xml']
    for candidate in candidates:
        if not candidate.is_file(): continue
        for node in ET.parse(str(candidate)).getroot().iter():
            if node.tag.rsplit('}', 1)[-1] == 'MachineEntry' and node.get('uuid', '').strip('{}').lower() == identifier:
                path = Path(node.get('src', ''))
                return path if path.is_absolute() else candidate.parent / path
    raise LaunchError('Cannot verify the previous VirtualBox registration for ' + identifier)


def relocate(state, state_root, previous, registered, run, environment):
    """Re-register this moved VM without deleting disks or saved execution.

    UUID + owner + edition are checked before changing a registration. A copy
    whose original folder still exists must never take over the original VM.
    """
    if previous == state_root: return registered
    if previous.exists() or previous.is_symlink():
        raise LaunchError('Previous edition still exists; refusing to take over a copied VM: ' + str(previous))
    for key in ('disk', 'iso'):
        if state.get(key) and not Path(state[key]).is_file():
            raise LaunchError('Moved edition is missing its ' + key + ': ' + state[key])
    identifier = state.get('vm_uuid')
    if not identifier:
        save_state(state_root, state)
        return registered
    relative = Path('machines') / state['name'] / (state['name'] + '.vbox')
    cfg = safe(state_root, relative)
    original = cfg.read_bytes()
    if b'<!DOCTYPE' in original or b'<!ENTITY' in original:
        raise LaunchError('Unexpected XML declarations in managed VM')
    xml = ET.fromstring(original)
    ns = {'v': 'http://www.virtualbox.org/'}
    machine = xml.find('v:Machine', ns)
    if machine is None or machine.get('uuid', '').strip('{}').lower() != identifier or machine.get('name') != state['name']:
        raise LaunchError('Moved VM UUID/name does not match launch state')
    markers = {n.get('name'): n.get('value') for n in machine.findall('v:ExtraData/v:ExtraDataItem', ns)}
    if markers.get('WorldOS/Owner') != state['owner'] or markers.get('WorldOS/Edition') != state['edition']:
        raise LaunchError('Moved VM ownership/edition marker does not match')

    def mapped(value, folder):
        path = Path(value)
        if not path.is_absolute(): path = cfg.parent / path
        path = Path(os.path.normpath(str(path)))
        try:
            tail = path.relative_to(previous)
        except ValueError:
            try:
                tail = path.relative_to(state_root)
            except ValueError:
                raise LaunchError('Unmanaged path in moved VM; preserving it: ' + str(value))
        if len(tail.parts) < 2 or tail.parts[0] != folder:
            raise LaunchError('Invalid moved VM path: ' + str(value))
        return safe(state_root, tail)

    for node in machine.findall('.//v:MediaRegistry//*[@location]', ns):
        path = mapped(node.get('location'), 'media')
        if str(path) not in state['media_history'] or not path.is_file():
            raise LaunchError('Unmanaged/missing medium in moved VM: ' + str(path))
        node.set('location', os.path.relpath(str(path), str(cfg.parent)))
    for node in machine.iter():
        for key in ('stateFile', 'snapshotFolder'):
            if not node.get(key): continue
            path = mapped(node.get(key), 'machines')
            if key == 'stateFile' and not path.is_file():
                raise LaunchError('Missing saved execution file; preserving VM: ' + str(path))
            node.set(key, os.path.relpath(str(path), str(cfg.parent)))
    for node in machine.findall('.//v:UART/v:Port', ns):
        if node.get('path') and node.get('hostMode') == 'RawFile':
            path = mapped(node.get('path'), 'logs')
            if str(path) != state.get('serial_log'):
                raise LaunchError('Unmanaged UART log in moved VM')
            node.set('path', str(path))

    if identifier in registered:
        info = properties(run(['VBoxManage', 'showvminfo', identifier, '--machinereadable']))
        if info.get('name') == '<inaccessible>':
            if registered_path(identifier, environment) != previous / relative:
                raise LaunchError('Inaccessible VM registration is not the previous edition')
        else:
            if Path(info.get('CfgFile', '')) not in (cfg, previous / relative):
                raise LaunchError('Registered VM belongs to another directory')
            if info.get('VMState') not in ('poweroff', 'aborted', 'saved'):
                raise LaunchError('Moved VM is active or busy; close it before moving its folder')
            token = run(['VBoxManage', 'getextradata', identifier, 'WorldOS/Owner']).strip()
            if token != 'Value: ' + state['owner']:
                raise LaunchError('Registered VM ownership marker does not match')
    elif state['name'] in registered.values():
        raise LaunchError('Name belongs to another VM: ' + state['name'])

    ET.register_namespace('', ns['v'])
    contents = b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(xml, encoding='utf-8')
    backup = safe(state_root, 'relocation-backup-' + str(uuid.uuid4()))
    backup.mkdir()
    shutil.copy2(str(cfg), str(backup / cfg.name))
    shutil.copy2(str(state_root / 'state.json'), str(backup / 'state.json'))
    write_json(backup / 'location.json', {'previous': str(previous), 'current': str(state_root), 'vm_uuid': identifier})
    print('RELOCATE', previous, '->', state_root, 'BACKUP', backup, flush=True)
    if identifier in registered:
        # No --delete: the VM, its disks and .sav files remain intact.
        run(['VBoxManage', 'unregistervm', identifier])
    with tempfile.NamedTemporaryFile(dir=str(cfg.parent), delete=False) as stream:
        stream.write(contents)
        temporary = stream.name
    os.replace(temporary, str(cfg))
    try:
        run(['VBoxManage', 'registervm', cfg])
    except LaunchError as error:
        raise LaunchError('VM registration repair failed; disks and saved state are preserved. '
                          'Retry make vbox. Configuration backup: ' + str(backup) + '\n' + str(error)) from error
    registered = machines(run(['VBoxManage', 'list', 'vms']))
    owned_info(state, state_root, registered, run)
    save_state(state_root, state)
    return registered


def command(arguments, log=None, env=None):
    result = subprocess.run([str(arg) for arg in arguments], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env)
    if log:
        with log.open('ab') as stream:
            stream.write(('$ ' + ' '.join(str(arg) for arg in arguments) + '\n').encode('utf-8'))
            stream.write(result.stdout)
    if result.returncode:
        raise LaunchError('Command failed: ' + ' '.join(str(arg) for arg in arguments) + '\n' +
                          result.stdout.decode('utf-8', errors='replace')[-12000:])
    return result.stdout.decode('utf-8', errors='replace')


def properties(text):
    result = {}
    for line in text.splitlines():
        match = re.fullmatch(r'("(?:[^"\\]|\\.)*"|[^=]+)=(.*)', line)
        if not match:
            continue
        def decode(value):
            if value.startswith('"'):
                try:
                    decoded, end = json.JSONDecoder().raw_decode(value)
                    # VirtualBox 5.2 emits composite values such as
                    # VideoMode="720,400,0"@0,0 1 while a guest is running.
                    return decoded if end == len(value) else value
                except ValueError:
                    raise LaunchError('Malformed VirtualBox property: ' + line)
            return value
        result[decode(match.group(1))] = decode(match.group(2))
    return result


def machines(text):
    found = {}
    for line in text.splitlines():
        match = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', line)
        if match:
            found[match.group(2).lower()] = match.group(1)
    return found


def validate(tree):
    config = read_json(safe(tree, 'vbox-entry.json'))
    if config.get('version') != 1 or not re.fullmatch(r'[A-Z]{3}(?:/[A-Za-z0-9_]+)?', config['edition']):
        raise LaunchError('Invalid edition in vbox-entry.json')
    if digest(safe(tree, 'vbox.py')) != config['launcher_sha256']:
        raise LaunchError('vbox.py changed since installation; preserve edits before reinstalling')
    kernel = safe(tree, config.get('kernel_directory', '소스'))
    if not safe(kernel, 'Makefile').is_file():
        raise LaunchError('Missing independent kernel source')
    shell_entry = read_json(safe(tree, 'shell-entry.json'))
    shell = safe(tree, shell_entry['directory'])
    shell_config = read_json(safe(shell, 'shell.json'))
    if shell_config['edition'] != config['edition']:
        raise LaunchError('Shell belongs to a different edition')
    posix_entry = read_json(safe(tree, 'posix-entry.json'))
    posix = safe(tree, posix_entry['directory'])
    if read_json(safe(posix, 'posix.json'))['edition'] != config['edition']:
        raise LaunchError('POSIX library belongs to a different edition')
    return config, shell, shell_config


def owned_info(state, state_root, registered, run):
    identifier = state.get('vm_uuid')
    if not identifier:
        return None
    if identifier not in registered:
        raise LaunchError('Managed VM was unregistered. Existing disks were preserved; restore registration before retrying.')
    info = properties(run(['VBoxManage', 'showvminfo', identifier, '--machinereadable']))
    cfg = Path(info.get('CfgFile', '')).resolve()
    if state_root / 'machines' not in cfg.parents:
        raise LaunchError('VM configuration moved outside this edition; refusing to modify it')
    token = run(['VBoxManage', 'getextradata', identifier, 'WorldOS/Owner']).strip()
    if token != 'Value: ' + state['owner']:
        raise LaunchError('VM ownership marker does not match; refusing to modify it')
    # Refuse to replace user-attached media even in an otherwise managed VM.
    controllers = [value for key, value in info.items() if re.fullmatch('storagecontrollername[0-9]+', key)]
    for key, value in info.items():
        if any(re.fullmatch(re.escape(name) + r'-\d+-\d+', key) for name in controllers) and value not in ('none', 'emptydrive'):
            if Path(value).resolve() not in [Path(item).resolve() for item in state.get('media_history', [])]:
                raise LaunchError('Unmanaged attached medium; preserving it: ' + value)
    return info


def check_driver():
    # Some supported installations use a root-only device with a privileged
    # VirtualBox frontend. Do not reject these based on this Python UID's access.
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise LaunchError('VirtualBox 호스트 드라이버 /dev/vboxdrv에 접근할 수 없습니다.\n'
            '실제 Ubuntu 터미널에서 장치와 권한을 확인하세요. 샌드박스에서는 장치가 가려질 수 있습니다.\n'
            '이 실행기는 sudo, 장치 권한 변경, 드라이버 재설치를 자동 수행하지 않습니다.')


def publish_iso(source, state_root):
    checksum = digest(source)
    destination = safe(state_root, 'media/kernel-' + checksum + '.iso')
    if destination.exists():
        if digest(destination) != checksum:
            raise LaunchError('Preserved ISO was modified: ' + str(destination))
    else:
        destination.parent.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=str(destination.parent)) as stream:
            shutil.copyfile(str(source), stream.name)
            os.link(stream.name, str(destination))
    return destination


def programs(shell, config):
    result = [(safe(shell, 'build/worldos-shell'), 'USER1'),
              (safe(shell, 'build/worldos-idle'), 'USER2'),
              (safe(shell, 'build/worldos-idle'), 'USER3'),
              (safe(shell, 'build/worldos-shell-probe'), 'SHEXEC')]
    if config.get('example_source'):
        result.append((safe(shell, config['example_source']), 'COMMANDS'))
    return result


def prepare_disk(source, state_root, inputs, run):
    """Always write a fresh clone. Old/current/base VDI content stays untouched."""
    before = digest(source)
    media = safe(state_root, 'media')
    media.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='prepare-', dir=str(state_root)) as temporary:
        temporary = Path(temporary)
        raw, output = temporary / 'disk.raw', temporary / 'disk.vdi'
        run(['qemu-img', 'convert', '-O', 'raw', source, raw])
        layout = run(['sfdisk', '-d', raw])
        match = re.search(r'start=\s*(\d+)', layout)
        if not match or not 0 < int(match.group(1)) * 512 < raw.stat().st_size:
            raise LaunchError('Base disk must contain the existing WorldOS FAT partition')
        partition = str(raw) + '@@' + str(int(match.group(1)) * 512)
        environment = dict(os.environ, MTOOLS_SKIP_CHECK='1')
        for required in ('LINKER', 'LIB1.SO', 'LIB2.SO'):
            run(['mdir', '-i', partition, '::' + required], env=environment)
        for path, name in inputs:
            run(['mcopy', '-o', '-i', partition, path, '::' + name], env=environment)
        run(['qemu-img', 'convert', '-f', 'raw', '-O', 'vdi', raw, output])
        if digest(source) != before:
            raise LaunchError('Source disk changed during preparation; new disk was not published')
        destination = safe(media, 'system-' + str(uuid.uuid4()) + '.vdi')
        os.link(str(output), str(destination))
    return destination, before


def medium_reference(path, kind, info, run):
    """Reuse a registered UUID even when VBox retains /machines/name/../../media.

    VBox 5.2 compares filename strings when opening media, not canonical paths.
    Opening a second spelling of one VDI therefore causes a UUID collision.
    """
    target = Path(path).resolve()
    def identifier(value):
        try:
            return str(uuid.UUID(value))
        except (ValueError, AttributeError, TypeError):
            raise LaunchError('Invalid registered medium UUID: ' + str(value))
    # Prefer the live attachment, avoiding an unnecessary global media scan.
    controllers = [value for key, value in info.items() if re.fullmatch('storagecontrollername[0-9]+', key)]
    matches = set()
    for controller in controllers:
        for key, value in info.items():
            match = re.fullmatch(re.escape(controller) + r'-(\d+)-(\d+)', key)
            if match and value not in ('none', 'emptydrive') and Path(value).resolve() == target:
                value = info.get(controller + '-ImageUUID-' + match.group(1) + '-' + match.group(2))
                if value: matches.add(identifier(value))
    if not matches:
        # A previously used image may remain registered after it was detached.
        records, current = [], {}
        text = run(['VBoxManage', 'list', 'hdds' if kind == 'hdd' else 'dvds'])
        for line in text.splitlines():
            key, separator, value = line.partition(':')
            if not separator: continue
            if key.strip() == 'UUID':
                if current: records.append(current)
                current = {}
            current[key.strip()] = value.strip()
        if current: records.append(current)
        for record in records:
            if record.get('Location') and Path(record['Location']).resolve() == target:
                matches.add(identifier(record.get('UUID')))
    if len(matches) > 1:
        raise LaunchError('Multiple registered UUIDs refer to the same managed medium: ' + str(path))
    return next(iter(matches)) if matches else str(target)


def configure(state, state_root, registered, info, run):
    if not state.get('vm_uuid'):
        if state['name'] in registered.values():
            raise LaunchError('Name belongs to another VM: ' + state['name'] +
                              '; choose a new VBOX_VM_NAME instead')
        identifier = str(uuid.uuid4())
        machine_folder = safe(state_root, 'machines/' + state['name'])
        if machine_folder.exists():
            raise LaunchError('Unregistered VM folder already exists; preserving it: ' + str(machine_folder))
        run(['VBoxManage', 'createvm', '--name', state['name'], '--uuid', identifier,
             '--ostype', 'Other', '--basefolder', state_root / 'machines', '--register'])
        # Save immediately so a failed configuration never causes a second VM.
        state['vm_uuid'] = identifier
        save_state(state_root, state)
        run(['VBoxManage', 'setextradata', identifier, 'WorldOS/Owner', state['owner']])
        run(['VBoxManage', 'setextradata', identifier, 'WorldOS/Edition', state['edition']])
        info = properties(run(['VBoxManage', 'showvminfo', identifier, '--machinereadable']))
    identifier = state['vm_uuid']
    if info.get('VMState') not in ('poweroff', 'aborted'):
        raise LaunchError('VM is not powered off; refusing to reconfigure: ' + info.get('VMState', 'unknown'))
    controllers = {value for key, value in info.items() if re.fullmatch('storagecontrollername[0-9]+', key)}
    if 'IDE' in controllers:
        controller = next(key[len('storagecontrollername'):] for key, value in info.items()
                          if re.fullmatch('storagecontrollername[0-9]+', key) and value == 'IDE')
        if info.get('storagecontrollertype' + controller) != 'PIIX4':
            raise LaunchError('Managed IDE controller was changed; restore PIIX4 before launching')
    disk = medium_reference(state['disk'], 'hdd', info, run)
    iso = medium_reference(state['iso'], 'dvddrive', info, run)
    run(['VBoxManage', 'modifyvm', identifier, '--memory', '512', '--cpus', '1', '--vram', '16',
         '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off', '--pae', 'off',
         '--paravirtprovider', 'none', '--boot1', 'dvd', '--boot2', 'disk', '--boot3', 'none', '--boot4', 'none'])
    if 'IDE' not in controllers:
        run(['VBoxManage', 'storagectl', identifier, '--name', 'IDE', '--add', 'ide', '--controller', 'PIIX4'])
    run(['VBoxManage', 'storageattach', identifier, '--storagectl', 'IDE', '--port', '0', '--device', '1',
         '--type', 'hdd', '--medium', disk])
    run(['VBoxManage', 'storageattach', identifier, '--storagectl', 'IDE', '--port', '1', '--device', '0',
         '--type', 'dvddrive', '--medium', iso])
    run(['VBoxManage', 'modifyvm', identifier, '--uart1', '0x3F8', '4', '--uartmode1', 'file', state['serial_log']])


def launch(tree, action, environment=None, runner=command, driver_check=check_driver):
    tree = Path(tree).resolve()
    environment = os.environ if environment is None else environment
    config, shell, shell_config = validate(tree)
    if action == 'check':
        print('PASS', config['edition'], 'independent make vbox entry; no VM changes')
        return
    state_root = safe(tree, '.vbox')
    state_file = safe(state_root, 'state.json')
    if action == 'status':
        if not state_file.is_file():
            print('NOT_CREATED', config['vm_name'])
            return
        state, previous = load_state(state_root, read_json(state_file), config['edition'])
        if previous != state_root:
            print(json.dumps({'name': state['name'], 'relocation_required': True,
                              'disk': state.get('disk'), 'iso': state.get('iso'),
                              'next_step': 'make vbox (or python3 vbox.py relocate)'}, ensure_ascii=False, indent=2))
            return
        info = owned_info(state, state_root, machines(runner(['VBoxManage', 'list', 'vms'])), runner)
        print(json.dumps({'name': state['name'], 'state': info.get('VMState') if info else 'prepared',
                          'disk': state.get('disk'), 'iso': state.get('iso'),
                          'serial_log': state.get('serial_log')}, ensure_ascii=False, indent=2))
        return
    if not shutil.which('VBoxManage'):
        raise LaunchError('VBoxManage is not installed; install VirtualBox on the host first')
    state_root.mkdir(exist_ok=True)
    with safe(state_root, 'launch.lock').open('a') as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise LaunchError('Another make vbox is already preparing this edition')
        raw_state = read_json(state_file) if state_file.is_file() else {
            'version': 1, 'edition': config['edition'], 'owner': str(uuid.uuid4()),
            'name': environment.get('VBOX_VM_NAME') or config['vm_name'], 'media_history': []}
        state, previous = load_state(state_root, raw_state, config['edition'])
        if not state['name'] or any(ch in state['name'] for ch in '/\\\n\r\t') or state['name'] in ('.', '..'):
            raise LaunchError('Invalid VM name')
        if environment.get('VBOX_VM_NAME') and environment['VBOX_VM_NAME'] != state['name']:
            raise LaunchError('This edition already owns a differently named VM: ' + state['name'])
        frontend = environment.get('VBOX_TYPE') or 'gui'
        if frontend not in ('gui', 'headless'):
            raise LaunchError('VBOX_TYPE must be gui or headless')
        registered = machines(runner(['VBoxManage', 'list', 'vms']))
        registered = relocate(state, state_root, previous, registered, runner, environment)
        info = owned_info(state, state_root, registered, runner)
        if action == 'relocate':
            save_state(state_root, state)
            print('LOCATION_READY', tree, '(disks and saved execution preserved)', flush=True)
            return
        if info and info.get('VMState') == 'running':
            print('ALREADY_RUNNING', state['name'], '(no rebuild, poweroff, or disk changes)')
            return
        if info and info.get('VMState') in ('saved', 'paused'):
            previous_state = info['VMState']
            if action != 'run':
                raise LaunchError('VM is ' + previous_state + '; preparation cannot rebuild it. '
                                  'Use make vbox to resume without rebuilding, or shut it down first.')
            # Resume the existing execution context, never discard it or replace
            # its ISO/disk. This path needs no compiler tools or original disk.
            if previous_state == 'saved':
                driver_check()
                arguments = ['VBoxManage', 'startvm', state['vm_uuid'], '--type', frontend]
            else:
                arguments = ['VBoxManage', 'controlvm', state['vm_uuid'], 'resume']
            print('RESUMING', state['name'], 'from', previous_state, flush=True)
            try:
                runner(arguments)
            except LaunchError as error:
                raise LaunchError('가상 머신 재개 명령이 실패했습니다. 실행기는 저장 상태 삭제, '
                                  '디스크 교체, 새 부팅을 수행하지 않았습니다.\n' + str(error)) from error
            print('RESUMED', state['name'], 'from', previous_state,
                  '(no rebuild, reconfiguration, or media replacement)', flush=True)
            return
        if info and info.get('VMState') not in ('poweroff', 'aborted'):
            raise LaunchError('VM is busy or in an unsupported state: ' + info.get('VMState', 'unknown') +
                              '; wait for its operation to finish and retry make vbox')
        if not info and state['name'] in registered.values():
            raise LaunchError('An unrelated VM already has this name: ' + state['name'] +
                              '\nUse make vbox VBOX_VM_NAME="a new name"; existing VM was not changed.')
        driver_check()
        for executable in ('make', 'qemu-img', 'sfdisk', 'mcopy', 'mdir'):
            if not shutil.which(executable):
                raise LaunchError('Missing prerequisite: ' + executable)
        source = Path(state['disk']) if state.get('disk') else Path(environment.get('VBOX_BASE_DISK') or config['base_disk'])
        if not source.is_absolute(): source = tree / source
        if not source.is_file():
            raise LaunchError('Missing base/current disk: ' + str(source) +
                              '\nFirst launch: make vbox VBOX_BASE_DISK="/absolute/path/to/base.vdi"')
        if state.get('disk') and source not in [Path(item) for item in state['media_history']]:
            raise LaunchError('Current disk is not in managed media history')
        if source.is_symlink():
            raise LaunchError('Refusing symbolic-link source disk')
        source = source.resolve()
        log_dir = safe(state_root, 'logs')
        log_dir.mkdir(exist_ok=True)
        label = str(uuid.uuid4())
        build_log = safe(log_dir, 'build-' + label + '.log')
        def run(arguments, **kwargs):
            return runner(arguments, log=build_log, **kwargs)
        print('BUILD', config['edition'], 'kernel / POSIX / shell; log:', build_log, flush=True)
        run(['make', '-C', tree, 'shell'])
        kernel = safe(tree, config.get('kernel_directory', '소스'))
        run(['make', '-B', '-C', kernel, 'iso'])
        iso = publish_iso(safe(kernel, 'build/kernel.iso'), state_root)
        inputs = programs(shell, shell_config)
        signatures = {name: digest(path) for path, name in inputs}
        if state.get('programs') != signatures or not state.get('disk'):
            disk, original_hash = prepare_disk(source, state_root, inputs, run)
            state['disk'] = str(disk)
            state['programs'] = signatures
            state.setdefault('disk_generations', []).append({'disk': str(disk), 'source': str(source),
                                                            'source_sha256_unchanged': original_hash})
            print('NEW_DISK', disk, '(previous disk preserved)', flush=True)
        state['iso'] = str(iso)
        state['serial_log'] = str(safe(log_dir, 'serial-' + label + '.log'))
        state['media_history'] = sorted(set(state['media_history'] + [state['disk'], state['iso']]))
        # Recheck live state after a potentially long build, before reconfiguration.
        if info:
            info = owned_info(state, state_root, machines(run(['VBoxManage', 'list', 'vms'])), run)
            if info.get('VMState') not in ('poweroff', 'aborted'):
                raise LaunchError('VM started during preparation; current launch state was not changed')
        save_state(state_root, state)
        configure(state, state_root, registered, info, run)
        print('READY', state['name'], '\nSERIAL_LOG', state['serial_log'], flush=True)
        if action == 'run':
            run(['VBoxManage', 'startvm', state['vm_uuid'], '--type', frontend])
            print('STARTED', state['name'], frontend, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['run', 'prepare', 'status', 'check', 'relocate'])
    parser.add_argument('--tree', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        launch(args.tree.resolve(), args.action)
    except (LaunchError, OSError, ValueError, KeyError, ET.ParseError) as error:
        print('VBOX ERROR:', error, file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
