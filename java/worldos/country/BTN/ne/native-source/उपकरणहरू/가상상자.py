#!/usr/bin/env python3
"""jkoros 전용 VirtualBox अनुप्रयोग_कर्मचारी_अगुवा. 기존 VM/디스크/भण्डार_गर्नुहोस्_मान 상태는 삭제하지 않는다."""
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


def कार्यान्वयन_गर्नुहोस्_शेल_आदेश(तर्क):
    환경 = dict(os.environ, LC_ALL='C')
    मापन = subprocess.run([str(मान) for मान in तर्क], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    सामग्री_मान = मापन.stdout.decode('utf-8', 'replace')
    if मापन.returncode:
        raise 실행오류('आदेश विफल_मान: ' + ' '.join(str(मान) for मान in तर्क) + '\n' + सामग्री_मान[-10000:])
    return सामग्री_मान


def विशेषण_मान(सामग्री_मान):
    मापन = {}
    for रेखा in सामग्री_मान.splitlines():
        if '=' not in रेखा:
            continue
        नाम, मान = रेखा.split('=', 1)
        if नाम.startswith('"'):
            नाम = json.loads(नाम)
        if मान.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(मान)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(मान): मान = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox विशेषण_मान ढाँचा_मान त्रुटि: ' + रेखा)
        मापन[नाम] = मान
    return मापन


def 등록목록(सामग्री_मान):
    मापन = {}
    for रेखा in सामग्री_मान.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', रेखा)
        if 일치: मापन[일치.group(2).lower()] = 일치.group(1)
    return मापन


def 검사합(मार्ग):
    मान = hashlib.sha256()
    with मार्ग.open('rb') as फाइल:
        for लगत in iter(lambda: फाइल.read(1024 * 1024), b''): मान.update(लगत)
    return मान.hexdigest()


class अनुप्रयोग_कर्मचारी_अगुवा:
    def __init__(self, रूट_मान, नाम, तरिका_मोड='gui', आदेश=कार्यान्वयन_गर्नुहोस्_शेल_आदेश):
        self.रूट_मान = Path(रूट_मान).resolve()
        self.नाम, self.तरिका_मोड, self.आदेश = नाम, तरिका_मोड, आदेश
        self.보관 = self.रूट_मान / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', नाम) or नाम in ('.', '..'):
            raise 실행오류('VM 이름은 문자·अङ्क_मान·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if तरिका_मोड not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def मार्ग(self, समान_मान):
        if Path(समान_मान).is_absolute() or '..' in Path(समान_मान).parts:
            raise 실행오류('잘못된 관리 मार्ग: ' + str(समान_मान))
        मापन = self.보관
        for 부분 in ['.vbox'] + list(Path(समान_मान).parts):
            if 부분 == '.vbox': मापन = self.보관
            else: मापन = मापन / 부분
            if मापन.is_symlink(): raise 실행오류('जडान 경로는 사용하지 않습니다: ' + str(मापन))
        return मापन

    def पढनुहोस्(self):
        मार्ग = self.मार्ग('state.json')
        if not मार्ग.exists(): return None
        स्थिति_मान = json.loads(मार्ग.read_text(encoding='utf-8'))
        if स्थिति_मान.get('version') != 1 or स्थिति_मान.get('name') != self.नाम:
            raise 실행오류('관리 상태의 VM नाम/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for नाम in ('uuid', 'owner'):
            if str(uuid.UUID(स्थिति_मान[नाम])) != स्थिति_मान[नाम]: raise 실행오류('잘못된 VM परिचायक_मान')
        return स्थिति_मान

    def भण्डार_गर्नुहोस्_मान(self, स्थिति_मान):
        गन्तव्य_मान = self.मार्ग('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as फाइल:
            json.dump(स्थिति_मान, फाइल, ensure_ascii=False, indent=2)
            फाइल.write('\n')
            임시 = फाइल.name
        os.replace(임시, str(गन्तव्य_मान))

    def प्रणाली_जानकारी(self, स्थिति_मान, 등록됨, पुन_प्राप्त_गर्नुहोस्_स्थिति=False):
        if स्थिति_मान['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        प्रणाली_जानकारी = विशेषण_मान(self.आदेश(['VBoxManage', 'showvminfo', स्थिति_मान['uuid'], '--machinereadable']))
        स्थिति = Path(प्रणाली_जानकारी.get('CfgFile', '')).resolve()
        if self.मार्ग('machines').resolve() not in स्थिति.parents or प्रणाली_जानकारी.get('UUID') != स्थिति_मान['uuid']:
            raise 실행오류('이 프로젝트의 VM सेटिङ मार्ग/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.आदेश(['VBoxManage', 'getextradata', स्थिति_मान['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + स्थिति_मान['owner']:
            if पुन_प्राप्त_गर्नुहोस्_स्थिति and स्थिति_मान.get('pending') and 표식 == 'No value set!':
                self.आदेश(['VBoxManage', 'setextradata', स्थिति_मान['uuid'], 'JKOROS/Owner', स्थिति_मान['owner']])
            else:
                raise 실행오류('VM मालिक_मान 표식이 일치하지 않아 변경하지 않습니다.')
        return प्रणाली_जानकारी

    def 매체검사(self, स्थिति_मान, प्रणाली_जानकारी):
        제어기들 = [मान for नाम, मान in प्रणाली_जानकारी.items() if re.fullmatch(r'storagecontrollername\d+', नाम)]
        अनुमति_दिनुहोस्_मान = [str(self.मार्ग(मान)) for मान in स्थिति_मान.get('media', [])]
        for नाम, मान in प्रणाली_जानकारी.items():
            if any(re.fullmatch(re.escape(नियन्त्रक) + r'-\d+-\d+', नाम) for नियन्त्रक in 제어기들):
                if मान not in ('none', 'emptydrive') and मान not in अनुमति_दिनुहोस्_मान:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + मान)

    def शो_स्थिति(self):
        स्थिति_मान = self.पढनुहोस्()
        if स्थिति_मान is None: return {'name': self.नाम, 'state': 'not-created'}
        प्रणाली_जानकारी = self.प्रणाली_जानकारी(स्थिति_मान, 등록목록(self.आदेश(['VBoxManage', 'list', 'vms'])))
        return {'name': प्रणाली_जानकारी.get('name', स्थिति_मान['name']), 'uuid': स्थिति_मान['uuid'], 'state': प्रणाली_जानकारी.get('VMState'),
                'iso': str(self.मार्ग(स्थिति_मान['iso'])) if स्थिति_मान.get('iso') else None,
                'serial_log': str(self.मार्ग(स्थिति_मान['serial_log'])) if स्थिति_मान.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def कार्यान्वयन_गर्नुहोस्_आदेश(self):
        स्थिति_मान = self.पढनुहोस्()
        등록됨 = 등록목록(self.आदेश(['VBoxManage', 'list', 'vms']))
        प्रणाली_जानकारी = None
        if स्थिति_मान is not None and स्थिति_मान['uuid'] in 등록됨:
            प्रणाली_जानकारी = self.प्रणाली_जानकारी(स्थिति_मान, 등록됨, पुन_प्राप्त_गर्नुहोस्_स्थिति=True)
            현재 = प्रणाली_जानकारी.get('VMState')
            if 현재 == 'running':
                print('이미 कार्यान्वयन_गर्नुहोस्_आदेश 중입니다. 재빌드·재시작하지 않습니다.')
                return self.शो_स्थिति()
            self.매체검사(स्थिति_मान, प्रणाली_जानकारी)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 भण्डार_गर्नुहोस्_मान 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.आदेश(['VBoxManage', 'controlvm', स्थिति_मान['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 खोल्नुहोस् 전에 기존 기록도 보관한다.
                    if स्थिति_मान.get('serial_log'):
                        원본 = self.मार्ग(स्थिति_मान['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.मार्ग('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.आदेश(['VBoxManage', 'startvm', स्थिति_मान['uuid'], '--type', self.तरिका_मोड])
                return self.शो_स्थिति()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 परिवर्तन_मोड 중입니다 ({}). 작업이 끝난 पछाडि_मान 다시 실행하세요.'.format(현재))
        elif स्थिति_मान is not None and not स्थिति_मान.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.नाम in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # भण्डार_गर्नुहोस्_मान/कार्यान्वयन_गर्नुहोस्_आदेश 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.आदेश(['make', '-C', str(self.रूट_मान / 'os'), 'iso']), end='')
        원본 = self.रूट_मान / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        गन्तव्य_मान = self.मार्ग(매체)
        गन्तव्य_मान.parent.mkdir(exist_ok=True)
        if गन्तव्य_मान.exists():
            if 검사합(गन्तव्य_मान) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(गन्तव्य_मान))
        else:
            with tempfile.NamedTemporaryFile(dir=str(गन्तव्य_मान.parent)) as फाइल:
                shutil.copyfile(str(원본), फाइल.name)
                os.link(फाइल.name, str(गन्तव्य_मान))

        if स्थिति_मान is None:
            स्थिति_मान = {'version': 1, 'name': self.नाम, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.भण्डार_गर्नुहोस्_मान(स्थिति_मान)
        if प्रणाली_जानकारी is None:
            self.आदेश(['VBoxManage', 'createvm', '--name', स्थिति_मान['name'], '--uuid', स्थिति_मान['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.मार्ग('machines')), '--register'])
            self.आदेश(['VBoxManage', 'setextradata', स्थिति_मान['uuid'], 'JKOROS/Owner', स्थिति_मान['owner']])
        # बनाउनुहोस्_प्रणाली 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        प्रणाली_जानकारी = self.प्रणाली_जानकारी(स्थिति_मान, 등록목록(self.आदेश(['VBoxManage', 'list', 'vms'])))
        if प्रणाली_जानकारी.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('बनाउनुहोस्_प्रणाली 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(स्थिति_मान, प्रणाली_जानकारी)
        स्थिति_मान['iso'] = 매체
        if 매체 not in स्थिति_मान['media']: स्थिति_मान['media'].append(매체)
        स्थिति_मान['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        लग_मान = self.मार्ग(स्थिति_मान['serial_log'])
        लग_मान.parent.mkdir(exist_ok=True)
        self.भण्डार_गर्नुहोस्_मान(स्थिति_मान)
        self.आदेश(['VBoxManage', 'modifyvm', स्थिति_मान['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(लग_मान)])
        제어기들 = [मान for नाम, मान in प्रणाली_जानकारी.items() if re.fullmatch(r'storagecontrollername\d+', नाम)]
        if 'JKOROS IDE' not in 제어기들:
            self.आदेश(['VBoxManage', 'storagectl', स्थिति_मान['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.आदेश(['VBoxManage', 'storageattach', स्थिति_मान['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(गन्तव्य_मान)])
        स्थिति_मान['pending'] = False
        self.भण्डार_गर्नुहोस्_मान(स्थिति_मान)
        self.आदेश(['VBoxManage', 'startvm', स्थिति_मान['uuid'], '--type', self.तरिका_मोड])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.शो_स्थिति()


def चलाउनुहोस्():
    पदच्छेद_गर्नुहोस्_मान = argparse.ArgumentParser(description='jkoros 전용 VirtualBox कार्यान्वयन_गर्नुहोस्_आदेश 및 स्थिति_मान क्वेरी_मान')
    पदच्छेद_गर्नुहोस्_मान.add_argument('action', choices=['run', 'status'])
    인자 = पदच्छेद_गर्नुहोस्_मान.parse_args()
    कार्यान्वयन_गर्नुहोस्_आदेश = अनुप्रयोग_कर्मचारी_अगुवा(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(कार्यान्वयन_गर्नुहोस्_आदेश.शो_स्थिति(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. होस्ट 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/अनुमति_मान 변경은 하지 않습니다.')
    os.umask(0o077)
    कार्यान्वयन_गर्नुहोस्_आदेश.मार्ग('lock').parent.mkdir(parents=True, exist_ok=True)
    with कार्यान्वयन_गर्नुहोस्_आदेश.मार्ग('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox कार्यान्वयन_गर्नुहोस्_आदेश 작업이 진행 중입니다.')
        print(json.dumps(कार्यान्वयन_गर्नुहोस्_आदेश.कार्यान्वयन_गर्नुहोस्_आदेश(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: चलाउनुहोस्()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as त्रुटि:
        print('VBOX त्रुटि: ' + str(त्रुटि), file=sys.stderr)
        sys.exit(1)
