#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ProgramLauncher. 기존 VM/디스크/storeValue 상태는 삭제하지 않는다."""
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


class executionError(RuntimeError):
    pass


def executeShellCommand(arguments):
    environment = dict(os.environ, LC_ALL='C')
    result = subprocess.run([str(value) for value in arguments], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=environment, timeout=180)
    contentValue = result.stdout.decode('utf-8', 'replace')
    if result.returncode:
        raise executionError('command failureValue: ' + ' '.join(str(value) for value in arguments) + '\n' + contentValue[-10000:])
    return contentValue


def attributeValue(contentValue):
    result = {}
    for line in contentValue.splitlines():
        if '=' not in line:
            continue
        name, value = line.split('=', 1)
        if name.startswith('"'):
            name = json.loads(name)
        if value.startswith('"'):
            try:
                readValue, ending = json.JSONDecoder().raw_decode(value)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if ending == len(value): value = readValue
            except ValueError:
                raise executionError('VirtualBox attributeValue formatValue error: ' + line)
        result[name] = value
    return result


def registeredEntries(contentValue):
    result = {}
    for line in contentValue.splitlines():
        isEqual = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', line)
        if isEqual: result[isEqual.group(2).lower()] = isEqual.group(1)
    return result


def checksum(path):
    value = hashlib.sha256()
    with path.open('rb') as file:
        for data in iter(lambda: file.read(1024 * 1024), b''): value.update(data)
    return value.hexdigest()


class ProgramLauncher:
    def __init__(self, rootValue, name, methodMode='gui', command=executeShellCommand):
        self.rootValue = Path(rootValue).resolve()
        self.name, self.methodMode, self.command = name, methodMode, command
        self.preserveValue = self.rootValue / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', name) or name in ('.', '..'):
            raise executionError('VM 이름은 Characters·digitValue·공백·밑줄·괄호·마침표·하이픈만 사용할 number 있습니다.')
        if methodMode not in ('gui', 'headless'): raise executionError('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def path(self, peerValue):
        if Path(peerValue).is_absolute() or '..' in Path(peerValue).parts:
            raise executionError('잘못된 관리 path: ' + str(peerValue))
        result = self.preserveValue
        for subpartValue in ['.vbox'] + list(Path(peerValue).parts):
            if subpartValue == '.vbox': result = self.preserveValue
            else: result = result / subpartValue
            if result.is_symlink(): raise executionError('connect 경로는 사용하지 않습니다: ' + str(result))
        return result

    def read(self):
        path = self.path('state.json')
        if not path.exists(): return None
        stateValue = json.loads(path.read_text(encoding='utf-8'))
        if stateValue.get('version') != 1 or stateValue.get('name') != self.name:
            raise executionError('관리 상태의 VM name/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for name in ('uuid', 'owner'):
            if str(uuid.UUID(stateValue[name])) != stateValue[name]: raise executionError('잘못된 VM identifierValue')
        return stateValue

    def storeValue(self, stateValue):
        destinationValue = self.path('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.preserveValue), delete=False) as file:
            json.dump(stateValue, file, ensure_ascii=False, indent=2)
            file.write('\n')
            temporaryValue = file.name
        os.replace(temporaryValue, str(destinationValue))

    def systemInformation(self, stateValue, registeredValue, recoverState=False):
        if stateValue['uuid'] not in registeredValue:
            raise executionError('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        systemInformation = attributeValue(self.command(['VBoxManage', 'showvminfo', stateValue['uuid'], '--machinereadable']))
        position = Path(systemInformation.get('CfgFile', '')).resolve()
        if self.path('machines').resolve() not in position.parents or systemInformation.get('UUID') != stateValue['uuid']:
            raise executionError('이 프로젝트의 VM settings path/UUID와 일치하지 않아 변경하지 않습니다.')
        markerValue = self.command(['VBoxManage', 'getextradata', stateValue['uuid'], 'JKOROS/Owner']).strip()
        if markerValue != 'Value: ' + stateValue['owner']:
            if recoverState and stateValue.get('pending') and markerValue == 'No value set!':
                self.command(['VBoxManage', 'setextradata', stateValue['uuid'], 'JKOROS/Owner', stateValue['owner']])
            else:
                raise executionError('VM ownerValue 표식이 일치하지 않아 변경하지 않습니다.')
        return systemInformation

    def checkMedia(self, stateValue, systemInformation):
        controllersList = [value for name, value in systemInformation.items() if re.fullmatch(r'storagecontrollername\d+', name)]
        allowValue = [str(self.path(value)) for value in stateValue.get('media', [])]
        for name, value in systemInformation.items():
            if any(re.fullmatch(re.escape(Controller) + r'-\d+-\d+', name) for Controller in controllersList):
                if value not in ('none', 'emptydrive') and value not in allowValue:
                    raise executionError('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + value)

    def showState(self):
        stateValue = self.read()
        if stateValue is None: return {'name': self.name, 'state': 'not-created'}
        systemInformation = self.systemInformation(stateValue, registeredEntries(self.command(['VBoxManage', 'list', 'vms'])))
        return {'name': systemInformation.get('name', stateValue['name']), 'uuid': stateValue['uuid'], 'state': systemInformation.get('VMState'),
                'iso': str(self.path(stateValue['iso'])) if stateValue.get('iso') else None,
                'serial_log': str(self.path(stateValue['serial_log'])) if stateValue.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def executeCommand(self):
        stateValue = self.read()
        registeredValue = registeredEntries(self.command(['VBoxManage', 'list', 'vms']))
        systemInformation = None
        if stateValue is not None and stateValue['uuid'] in registeredValue:
            systemInformation = self.systemInformation(stateValue, registeredValue, recoverState=True)
            currentItem = systemInformation.get('VMState')
            if currentItem == 'running':
                print('이미 executeCommand 중입니다. 재빌드·재시작하지 않습니다.')
                return self.showState()
            self.checkMedia(stateValue, systemInformation)
            if currentItem in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 storeValue 상태를 버리지 않습니다.'.format(currentItem))
                if currentItem == 'paused':
                    self.command(['VBoxManage', 'controlvm', stateValue['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 retryValue open 전에 기존 기록도 보관한다.
                    if stateValue.get('serial_log'):
                        original = self.path(stateValue['serial_log'])
                        if original.is_file():
                            shutil.copyfile(str(original), str(self.path('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.command(['VBoxManage', 'startvm', stateValue['uuid'], '--type', self.methodMode])
                return self.showState()
            if currentItem not in ('poweroff', 'aborted'):
                raise executionError('VM이 switchMode 중입니다 ({}). 작업이 끝난 backValue retryValue 실행하세요.'.format(currentItem))
        elif stateValue is not None and not stateValue.get('pending'):
            raise executionError('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 retryValue 등록하세요.')
        elif self.name in registeredValue.values():
            raise executionError('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # storeValue/executeCommand 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.command(['make', '-C', str(self.rootValue / 'os'), 'iso']), end='')
        original = self.rootValue / 'os/build/kernel.iso'
        if not original.is_file() or original.stat().st_size == 0: raise executionError('machine_boot ISO가 생성되지 않았습니다.')
        mediaValue = 'media/kernel-' + checksum(original) + '.iso'
        destinationValue = self.path(mediaValue)
        destinationValue.parent.mkdir(exist_ok=True)
        if destinationValue.exists():
            if checksum(destinationValue) != checksum(original): raise executionError('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destinationValue))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destinationValue.parent)) as file:
                shutil.copyfile(str(original), file.name)
                os.link(file.name, str(destinationValue))

        if stateValue is None:
            stateValue = {'version': 1, 'name': self.name, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.storeValue(stateValue)
        if systemInformation is None:
            self.command(['VBoxManage', 'createvm', '--name', stateValue['name'], '--uuid', stateValue['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.path('machines')), '--register'])
            self.command(['VBoxManage', 'setextradata', stateValue['uuid'], 'JKOROS/Owner', stateValue['owner']])
        # buildSystem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        systemInformation = self.systemInformation(stateValue, registeredEntries(self.command(['VBoxManage', 'list', 'vms'])))
        if systemInformation.get('VMState') not in ('poweroff', 'aborted'):
            raise executionError('buildSystem 중 VM 상태가 바뀌었습니다. retryValue make vbox를 실행하세요.')
        self.checkMedia(stateValue, systemInformation)
        stateValue['iso'] = mediaValue
        if mediaValue not in stateValue['media']: stateValue['media'].append(mediaValue)
        stateValue['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        logValue = self.path(stateValue['serial_log'])
        logValue.parent.mkdir(exist_ok=True)
        self.storeValue(stateValue)
        self.command(['VBoxManage', 'modifyvm', stateValue['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(logValue)])
        controllersList = [value for name, value in systemInformation.items() if re.fullmatch(r'storagecontrollername\d+', name)]
        if 'JKOROS IDE' not in controllersList:
            self.command(['VBoxManage', 'storagectl', stateValue['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.command(['VBoxManage', 'storageattach', stateValue['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destinationValue)])
        stateValue['pending'] = False
        self.storeValue(stateValue)
        self.command(['VBoxManage', 'startvm', stateValue['uuid'], '--type', self.methodMode])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.showState()


def run():
    parseValue = argparse.ArgumentParser(description='jkoros 전용 VirtualBox executeCommand 및 stateValue queryValue')
    parseValue.add_argument('action', choices=['run', 'status'])
    parameterArgument = parseValue.parse_args()
    executeCommand = ProgramLauncher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameterArgument.action == 'status':
        print(json.dumps(executeCommand.showState(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise executionError('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise executionError('/dev/vboxdrv에 접근할 number 없습니다. Host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/permissionValue 변경은 하지 않습니다.')
    os.umask(0o077)
    executeCommand.path('lock').parent.mkdir(parents=True, exist_ok=True)
    with executeCommand.path('lock').open('a') as lockValue:
        try: fcntl.flock(lockValue, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise executionError('다른 jkoros VirtualBox executeCommand 작업이 진행 중입니다.')
        print(json.dumps(executeCommand.executeCommand(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: run()
    except (executionError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print('VBOX error: ' + str(error), file=sys.stderr)
        sys.exit(1)
