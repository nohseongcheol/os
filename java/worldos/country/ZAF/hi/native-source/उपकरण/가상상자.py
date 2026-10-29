#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ऐप_लॉन्चर. 기존 VM/디스크/स्टोर_मान 상태는 삭제하지 않는다."""
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


class 실행오류(RuntimeError):
    pass


def निष्पादित_करें_शेल_आदेश(तर्क):
    환경 = dict(os.environ, LC_ALL='C')
    परिणाम = subprocess.run([str(मान) for मान in तर्क], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    सामग्री_मान = परिणाम.stdout.decode('utf-8', 'replace')
    if परिणाम.returncode:
        raise 실행오류('आदेश विफलता_मान: ' + ' '.join(str(मान) for मान in तर्क) + '\n' + सामग्री_मान[-10000:])
    return सामग्री_मान


def विशेषता_मान(सामग्री_मान):
    परिणाम = {}
    for पंक्ति in सामग्री_मान.splitlines():
        if '=' not in पंक्ति:
            continue
        नाम, मान = पंक्ति.split('=', 1)
        if नाम.startswith('"'):
            नाम = json.loads(नाम)
        if मान.startswith('"'):
            try:
                पढें_मान, 끝 = json.JSONDecoder().raw_decode(मान)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(मान): मान = पढें_मान
            except ValueError:
                raise 실행오류('VirtualBox विशेषता_मान फॉर्मैट_मान त्रुटि: ' + पंक्ति)
        परिणाम[नाम] = मान
    return परिणाम


def 등록목록(सामग्री_मान):
    परिणाम = {}
    for पंक्ति in सामग्री_मान.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', पंक्ति)
        if 일치: परिणाम[일치.group(2).lower()] = 일치.group(1)
    return परिणाम


def योगफल_की_जाँच(पथ):
    मान = hashlib.sha256()
    with पथ.open('rb') as संचिका:
        for आँकड़े in iter(lambda: संचिका.read(1024 * 1024), b''): मान.update(आँकड़े)
    return मान.hexdigest()


class ऐप_लॉन्चर:
    def __init__(self, मूल_मान, नाम, विधि_मोड='gui', आदेश=निष्पादित_करें_शेल_आदेश):
        self.मूल_मान = Path(मूल_मान).resolve()
        self.नाम, self.विधि_मोड, self.आदेश = नाम, विधि_मोड, आदेश
        self.보관 = self.मूल_मान / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', नाम) or नाम in ('.', '..'):
            raise 실행오류('VM 이름은 문자·अंक_मान·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if विधि_मोड not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def पथ(self, पीअर_मान):
        if Path(पीअर_मान).is_absolute() or '..' in Path(पीअर_मान).parts:
            raise 실행오류('잘못된 관리 पथ: ' + str(पीअर_मान))
        परिणाम = self.보관
        for 부분 in ['.vbox'] + list(Path(पीअर_मान).parts):
            if 부분 == '.vbox': परिणाम = self.보관
            else: परिणाम = परिणाम / 부분
            if परिणाम.is_symlink(): raise 실행오류('जोड़ना 경로는 사용하지 않습니다: ' + str(परिणाम))
        return परिणाम

    def पढ़ें(self):
        पथ = self.पथ('state.json')
        if not पथ.exists(): return None
        अवस्था_मान = json.loads(पथ.read_text(encoding='utf-8'))
        if अवस्था_मान.get('version') != 1 or अवस्था_मान.get('name') != self.नाम:
            raise 실행오류('관리 상태의 VM नाम/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for नाम in ('uuid', 'owner'):
            if str(uuid.UUID(अवस्था_मान[नाम])) != अवस्था_मान[नाम]: raise 실행오류('잘못된 VM पहचानकर्ता_मान')
        return अवस्था_मान

    def स्टोर_मान(self, अवस्था_मान):
        गंतव्य_मान = self.पथ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as संचिका:
            json.dump(अवस्था_मान, संचिका, ensure_ascii=False, indent=2)
            संचिका.write('\n')
            임시 = संचिका.name
        os.replace(임시, str(गंतव्य_मान))

    def सिस्टम_जानकारी(self, अवस्था_मान, 등록됨, पुनर्प्राप्त_करें_अवस्था=False):
        if अवस्था_मान['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        सिस्टम_जानकारी = विशेषता_मान(self.आदेश(['VBoxManage', 'showvminfo', अवस्था_मान['uuid'], '--machinereadable']))
        स्थान = Path(सिस्टम_जानकारी.get('CfgFile', '')).resolve()
        if self.पथ('machines').resolve() not in स्थान.parents or सिस्टम_जानकारी.get('UUID') != अवस्था_मान['uuid']:
            raise 실행오류('이 프로젝트의 VM विन्यास पथ/UUID와 일치하지 않아 변경하지 않습니다.')
        मार्कर_मान = self.आदेश(['VBoxManage', 'getextradata', अवस्था_मान['uuid'], 'JKOROS/Owner']).strip()
        if मार्कर_मान != 'Value: ' + अवस्था_मान['owner']:
            if पुनर्प्राप्त_करें_अवस्था and अवस्था_मान.get('pending') and मार्कर_मान == 'No value set!':
                self.आदेश(['VBoxManage', 'setextradata', अवस्था_मान['uuid'], 'JKOROS/Owner', अवस्था_मान['owner']])
            else:
                raise 실행오류('VM स्वामी_मान 표식이 일치하지 않아 변경하지 않습니다.')
        return सिस्टम_जानकारी

    def जाँचें_मीडिया(self, अवस्था_मान, सिस्टम_जानकारी):
        제어기들 = [मान for नाम, मान in सिस्टम_जानकारी.items() if re.fullmatch(r'storagecontrollername\d+', नाम)]
        अनुमति_दें_मान = [str(self.पथ(मान)) for मान in अवस्था_मान.get('media', [])]
        for नाम, मान in सिस्टम_जानकारी.items():
            if any(re.fullmatch(re.escape(कंट्रोलर) + r'-\d+-\d+', नाम) for कंट्रोलर in 제어기들):
                if मान not in ('none', 'emptydrive') and मान not in अनुमति_दें_मान:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + मान)

    def शो_अवस्था(self):
        अवस्था_मान = self.पढ़ें()
        if अवस्था_मान is None: return {'name': self.नाम, 'state': 'not-created'}
        सिस्टम_जानकारी = self.सिस्टम_जानकारी(अवस्था_मान, 등록목록(self.आदेश(['VBoxManage', 'list', 'vms'])))
        return {'name': सिस्टम_जानकारी.get('name', अवस्था_मान['name']), 'uuid': अवस्था_मान['uuid'], 'state': सिस्टम_जानकारी.get('VMState'),
                'iso': str(self.पथ(अवस्था_मान['iso'])) if अवस्था_मान.get('iso') else None,
                'serial_log': str(self.पथ(अवस्था_मान['serial_log'])) if अवस्था_मान.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def निष्पादित_करें_आदेश(self):
        अवस्था_मान = self.पढ़ें()
        등록됨 = 등록목록(self.आदेश(['VBoxManage', 'list', 'vms']))
        सिस्टम_जानकारी = None
        if अवस्था_मान is not None and अवस्था_मान['uuid'] in 등록됨:
            सिस्टम_जानकारी = self.सिस्टम_जानकारी(अवस्था_मान, 등록됨, पुनर्प्राप्त_करें_अवस्था=True)
            अद्यतित_आइटम = सिस्टम_जानकारी.get('VMState')
            if अद्यतित_आइटम == 'running':
                print('이미 निष्पादित_करें_आदेश 중입니다. 재빌드·재시작하지 않습니다.')
                return self.शो_अवस्था()
            self.जाँचें_मीडिया(अवस्था_मान, सिस्टम_जानकारी)
            if अद्यतित_आइटम in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 स्टोर_मान 상태를 버리지 않습니다.'.format(अद्यतित_आइटम))
                if अद्यतित_आइटम == 'paused':
                    self.आदेश(['VBoxManage', 'controlvm', अवस्था_मान['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 खोलें 전에 기존 기록도 보관한다.
                    if अवस्था_मान.get('serial_log'):
                        원본 = self.पथ(अवस्था_मान['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.पथ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.आदेश(['VBoxManage', 'startvm', अवस्था_मान['uuid'], '--type', self.विधि_मोड])
                return self.शो_अवस्था()
            if अद्यतित_आइटम not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 स्विच_मोड 중입니다 ({}). 작업이 끝난 वापस_मान 다시 실행하세요.'.format(अद्यतित_आइटम))
        elif अवस्था_मान is not None and not अवस्था_मान.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.नाम in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # स्टोर_मान/निष्पादित_करें_आदेश 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.आदेश(['make', '-C', str(self.मूल_मान / 'os'), 'iso']), end='')
        원본 = self.मूल_मान / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        मीडिया_मान = 'media/kernel-' + योगफल_की_जाँच(원본) + '.iso'
        गंतव्य_मान = self.पथ(मीडिया_मान)
        गंतव्य_मान.parent.mkdir(exist_ok=True)
        if गंतव्य_मान.exists():
            if योगफल_की_जाँच(गंतव्य_मान) != योगफल_की_जाँच(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(गंतव्य_मान))
        else:
            with tempfile.NamedTemporaryFile(dir=str(गंतव्य_मान.parent)) as संचिका:
                shutil.copyfile(str(원본), संचिका.name)
                os.link(संचिका.name, str(गंतव्य_मान))

        if अवस्था_मान is None:
            अवस्था_मान = {'version': 1, 'name': self.नाम, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.स्टोर_मान(अवस्था_मान)
        if सिस्टम_जानकारी is None:
            self.आदेश(['VBoxManage', 'createvm', '--name', अवस्था_मान['name'], '--uuid', अवस्था_मान['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.पथ('machines')), '--register'])
            self.आदेश(['VBoxManage', 'setextradata', अवस्था_मान['uuid'], 'JKOROS/Owner', अवस्था_मान['owner']])
        # बिल्ड_सिस्टम 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        सिस्टम_जानकारी = self.सिस्टम_जानकारी(अवस्था_मान, 등록목록(self.आदेश(['VBoxManage', 'list', 'vms'])))
        if सिस्टम_जानकारी.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('बिल्ड_सिस्टम 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.जाँचें_मीडिया(अवस्था_मान, सिस्टम_जानकारी)
        अवस्था_मान['iso'] = मीडिया_मान
        if मीडिया_मान not in अवस्था_मान['media']: अवस्था_मान['media'].append(मीडिया_मान)
        अवस्था_मान['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        लॉग_मान = self.पथ(अवस्था_मान['serial_log'])
        लॉग_मान.parent.mkdir(exist_ok=True)
        self.स्टोर_मान(अवस्था_मान)
        self.आदेश(['VBoxManage', 'modifyvm', अवस्था_मान['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(लॉग_मान)])
        제어기들 = [मान for नाम, मान in सिस्टम_जानकारी.items() if re.fullmatch(r'storagecontrollername\d+', नाम)]
        if 'JKOROS IDE' not in 제어기들:
            self.आदेश(['VBoxManage', 'storagectl', अवस्था_मान['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.आदेश(['VBoxManage', 'storageattach', अवस्था_मान['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(गंतव्य_मान)])
        अवस्था_मान['pending'] = False
        self.स्टोर_मान(अवस्था_मान)
        self.आदेश(['VBoxManage', 'startvm', अवस्था_मान['uuid'], '--type', self.विधि_मोड])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.शो_अवस्था()


def चलाएँ():
    पार्स_करें_मान = argparse.ArgumentParser(description='jkoros 전용 VirtualBox निष्पादित_करें_आदेश 및 अवस्था_मान क्वेरी_मान')
    पार्स_करें_मान.add_argument('action', choices=['run', 'status'])
    पैरामीटर_तर्क = पार्स_करें_मान.parse_args()
    निष्पादित_करें_आदेश = ऐप_लॉन्चर(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if पैरामीटर_तर्क.action == 'status':
        print(json.dumps(निष्पादित_करें_आदेश.शो_अवस्था(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. आयोजक 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/अनुमति_मान 변경은 하지 않습니다.')
    os.umask(0o077)
    निष्पादित_करें_आदेश.पथ('lock').parent.mkdir(parents=True, exist_ok=True)
    with निष्पादित_करें_आदेश.पथ('lock').open('a') as लॉक_मान:
        try: fcntl.flock(लॉक_मान, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox निष्पादित_करें_आदेश 작업이 진행 중입니다.')
        print(json.dumps(निष्पादित_करें_आदेश.निष्पादित_करें_आदेश(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: चलाएँ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as त्रुटि:
        print('VBOX त्रुटि: ' + str(त्रुटि), file=sys.stderr)
        sys.exit(1)
