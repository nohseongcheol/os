#!/usr/bin/env python3
"""jkoros 전용 VirtualBox अनुप्रयोग_चालक. 기존 VM/디스크/साठवणे_मूल्य 상태는 삭제하지 않는다."""
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


class निष्पादन_त्रुटी(RuntimeError):
    pass


def शेल_आज्ञा_कार्यवाही_करा(बाबी):
    पर्यावरण = dict(os.environ, LC_ALL='C')
    मोजमाप = subprocess.run([str(मूल्य) for मूल्य in बाबी], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=पर्यावरण, timeout=180)
    सामुग्री_मूल्य = मोजमाप.stdout.decode('utf-8', 'replace')
    if मोजमाप.returncode:
        raise निष्पादन_त्रुटी('आदेश बिघाड_मूल्य: ' + ' '.join(str(मूल्य) for मूल्य in बाबी) + '\n' + सामुग्री_मूल्य[-10000:])
    return सामुग्री_मूल्य


def गुणधर्म_मूल्य(सामुग्री_मूल्य):
    मोजमाप = {}
    for ओळ in सामुग्री_मूल्य.splitlines():
        if '=' not in ओळ:
            continue
        नाव, मूल्य = ओळ.split('=', 1)
        if नाव.startswith('"'):
            नाव = json.loads(नाव)
        if मूल्य.startswith('"'):
            try:
                मूल्य_वाचा, शेवट = json.JSONDecoder().raw_decode(मूल्य)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if शेवट == len(मूल्य): मूल्य = मूल्य_वाचा
            except ValueError:
                raise निष्पादन_त्रुटी('VirtualBox गुणधर्म_मूल्य स्वरूप_मूल्य त्रुटी: ' + ओळ)
        मोजमाप[नाव] = मूल्य
    return मोजमाप


def नोंदणीकृत_नोंदी(सामुग्री_मूल्य):
    मोजमाप = {}
    for ओळ in सामुग्री_मूल्य.splitlines():
        आहे_समान = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ओळ)
        if आहे_समान: मोजमाप[आहे_समान.group(2).lower()] = आहे_समान.group(1)
    return मोजमाप


def चेकसम(मार्ग):
    मूल्य = hashlib.sha256()
    with मार्ग.open('rb') as फाइल:
        for डेटा in iter(lambda: फाइल.read(1024 * 1024), b''): मूल्य.update(डेटा)
    return मूल्य.hexdigest()


class अनुप्रयोग_चालक:
    def __init__(self, मूळ_मूल्य, नाव, पद्धत_मोड='gui', आदेश=शेल_आज्ञा_कार्यवाही_करा):
        self.मूळ_मूल्य = Path(मूळ_मूल्य).resolve()
        self.नाव, self.पद्धत_मोड, self.आदेश = नाव, पद्धत_मोड, आदेश
        self.जतनकरा_मूल्य = self.मूळ_मूल्य / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', नाव) or नाव in ('.', '..'):
            raise निष्पादन_त्रुटी('VM 이름은 वर्ण·अंक_मूल्य·공백·밑줄·괄호·마침표·하이픈만 사용할 संख्या 있습니다.')
        if पद्धत_मोड not in ('gui', 'headless'): raise निष्पादन_त्रुटी('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def मार्ग(self, समकक्ष_मूल्य):
        if Path(समकक्ष_मूल्य).is_absolute() or '..' in Path(समकक्ष_मूल्य).parts:
            raise निष्पादन_त्रुटी('잘못된 관리 मार्ग: ' + str(समकक्ष_मूल्य))
        मोजमाप = self.जतनकरा_मूल्य
        for उपभाग_मूल्य in ['.vbox'] + list(Path(समकक्ष_मूल्य).parts):
            if उपभाग_मूल्य == '.vbox': मोजमाप = self.जतनकरा_मूल्य
            else: मोजमाप = मोजमाप / उपभाग_मूल्य
            if मोजमाप.is_symlink(): raise निष्पादन_त्रुटी('जोडा 경로는 사용하지 않습니다: ' + str(मोजमाप))
        return मोजमाप

    def वाचन(self):
        मार्ग = self.मार्ग('state.json')
        if not मार्ग.exists(): return None
        राज्य_मूल्य = json.loads(मार्ग.read_text(encoding='utf-8'))
        if राज्य_मूल्य.get('version') != 1 or राज्य_मूल्य.get('name') != self.नाव:
            raise निष्पादन_त्रुटी('관리 상태의 VM नाव/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for नाव in ('uuid', 'owner'):
            if str(uuid.UUID(राज्य_मूल्य[नाव])) != राज्य_मूल्य[नाव]: raise निष्पादन_त्रुटी('잘못된 VM आयडेंटिफायर_मूल्य')
        return राज्य_मूल्य

    def साठवणे_मूल्य(self, राज्य_मूल्य):
        गंतव्यस्थान_मूल्य = self.मार्ग('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.जतनकरा_मूल्य), delete=False) as फाइल:
            json.dump(राज्य_मूल्य, फाइल, ensure_ascii=False, indent=2)
            फाइल.write('\n')
            तात्पुरते_मूल्य = फाइल.name
        os.replace(तात्पुरते_मूल्य, str(गंतव्यस्थान_मूल्य))

    def सिस्टम_माहिती(self, राज्य_मूल्य, नोंदणीकृत_मूल्य, पुनर्प्राप्त_करा_राज्य=False):
        if राज्य_मूल्य['uuid'] not in नोंदणीकृत_मूल्य:
            raise निष्पादन_त्रुटी('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        सिस्टम_माहिती = गुणधर्म_मूल्य(self.आदेश(['VBoxManage', 'showvminfo', राज्य_मूल्य['uuid'], '--machinereadable']))
        जागा = Path(सिस्टम_माहिती.get('CfgFile', '')).resolve()
        if self.मार्ग('machines').resolve() not in जागा.parents or सिस्टम_माहिती.get('UUID') != राज्य_मूल्य['uuid']:
            raise निष्पादन_त्रुटी('이 프로젝트의 VM संयोजना मार्ग/UUID와 일치하지 않아 변경하지 않습니다.')
        खूण_मूल्य = self.आदेश(['VBoxManage', 'getextradata', राज्य_मूल्य['uuid'], 'JKOROS/Owner']).strip()
        if खूण_मूल्य != 'Value: ' + राज्य_मूल्य['owner']:
            if पुनर्प्राप्त_करा_राज्य and राज्य_मूल्य.get('pending') and खूण_मूल्य == 'No value set!':
                self.आदेश(['VBoxManage', 'setextradata', राज्य_मूल्य['uuid'], 'JKOROS/Owner', राज्य_मूल्य['owner']])
            else:
                raise निष्पादन_त्रुटी('VM मालक_मूल्य 표식이 일치하지 않아 변경하지 않습니다.')
        return सिस्टम_माहिती

    def माध्यमे_तपासा(self, राज्य_मूल्य, सिस्टम_माहिती):
        नियंत्रक_यादी = [मूल्य for नाव, मूल्य in सिस्टम_माहिती.items() if re.fullmatch(r'storagecontrollername\d+', नाव)]
        परवानगी_द्या_मूल्य = [str(self.मार्ग(मूल्य)) for मूल्य in राज्य_मूल्य.get('media', [])]
        for नाव, मूल्य in सिस्टम_माहिती.items():
            if any(re.fullmatch(re.escape(नियंत्रक) + r'-\d+-\d+', नाव) for नियंत्रक in नियंत्रक_यादी):
                if मूल्य not in ('none', 'emptydrive') and मूल्य not in परवानगी_द्या_मूल्य:
                    raise निष्पादन_त्रुटी('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + मूल्य)

    def राज्य_शो(self):
        राज्य_मूल्य = self.वाचन()
        if राज्य_मूल्य is None: return {'name': self.नाव, 'state': 'not-created'}
        सिस्टम_माहिती = self.सिस्टम_माहिती(राज्य_मूल्य, नोंदणीकृत_नोंदी(self.आदेश(['VBoxManage', 'list', 'vms'])))
        return {'name': सिस्टम_माहिती.get('name', राज्य_मूल्य['name']), 'uuid': राज्य_मूल्य['uuid'], 'state': सिस्टम_माहिती.get('VMState'),
                'iso': str(self.मार्ग(राज्य_मूल्य['iso'])) if राज्य_मूल्य.get('iso') else None,
                'serial_log': str(self.मार्ग(राज्य_मूल्य['serial_log'])) if राज्य_मूल्य.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def आज्ञा_कार्यवाही_करा(self):
        राज्य_मूल्य = self.वाचन()
        नोंदणीकृत_मूल्य = नोंदणीकृत_नोंदी(self.आदेश(['VBoxManage', 'list', 'vms']))
        सिस्टम_माहिती = None
        if राज्य_मूल्य is not None and राज्य_मूल्य['uuid'] in नोंदणीकृत_मूल्य:
            सिस्टम_माहिती = self.सिस्टम_माहिती(राज्य_मूल्य, नोंदणीकृत_मूल्य, पुनर्प्राप्त_करा_राज्य=True)
            सध्याचे_आयटम = सिस्टम_माहिती.get('VMState')
            if सध्याचे_आयटम == 'running':
                print('이미 आज्ञा_कार्यवाही_करा 중입니다. 재빌드·재시작하지 않습니다.')
                return self.राज्य_शो()
            self.माध्यमे_तपासा(राज्य_मूल्य, सिस्टम_माहिती)
            if सध्याचे_आयटम in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 साठवणे_मूल्य 상태를 버리지 않습니다.'.format(सध्याचे_आयटम))
                if सध्याचे_आयटम == 'paused':
                    self.आदेश(['VBoxManage', 'controlvm', राज्य_मूल्य['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 पुनःप्रयत्न_मूल्य उघडा 전에 기존 기록도 보관한다.
                    if राज्य_मूल्य.get('serial_log'):
                        मूळ = self.मार्ग(राज्य_मूल्य['serial_log'])
                        if मूळ.is_file():
                            shutil.copyfile(str(मूळ), str(self.मार्ग('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.आदेश(['VBoxManage', 'startvm', राज्य_मूल्य['uuid'], '--type', self.पद्धत_मोड])
                return self.राज्य_शो()
            if सध्याचे_आयटम not in ('poweroff', 'aborted'):
                raise निष्पादन_त्रुटी('VM이 स्विच_मोड 중입니다 ({}). 작업이 끝난 मागे_मूल्य पुनःप्रयत्न_मूल्य 실행하세요.'.format(सध्याचे_आयटम))
        elif राज्य_मूल्य is not None and not राज्य_मूल्य.get('pending'):
            raise निष्पादन_त्रुटी('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 पुनःप्रयत्न_मूल्य 등록하세요.')
        elif self.नाव in नोंदणीकृत_मूल्य.values():
            raise निष्पादन_त्रुटी('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # साठवणे_मूल्य/आज्ञा_कार्यवाही_करा 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.आदेश(['make', '-C', str(self.मूळ_मूल्य / 'os'), 'iso']), end='')
        मूळ = self.मूळ_मूल्य / 'os/build/kernel.iso'
        if not मूळ.is_file() or मूळ.stat().st_size == 0: raise निष्पादन_त्रुटी('प्रणालीप्रारंभ ISO가 생성되지 않았습니다.')
        माध्यमे_मूल्य = 'media/kernel-' + चेकसम(मूळ) + '.iso'
        गंतव्यस्थान_मूल्य = self.मार्ग(माध्यमे_मूल्य)
        गंतव्यस्थान_मूल्य.parent.mkdir(exist_ok=True)
        if गंतव्यस्थान_मूल्य.exists():
            if चेकसम(गंतव्यस्थान_मूल्य) != चेकसम(मूळ): raise निष्पादन_त्रुटी('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(गंतव्यस्थान_मूल्य))
        else:
            with tempfile.NamedTemporaryFile(dir=str(गंतव्यस्थान_मूल्य.parent)) as फाइल:
                shutil.copyfile(str(मूळ), फाइल.name)
                os.link(फाइल.name, str(गंतव्यस्थान_मूल्य))

        if राज्य_मूल्य is None:
            राज्य_मूल्य = {'version': 1, 'name': self.नाव, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.साठवणे_मूल्य(राज्य_मूल्य)
        if सिस्टम_माहिती is None:
            self.आदेश(['VBoxManage', 'createvm', '--name', राज्य_मूल्य['name'], '--uuid', राज्य_मूल्य['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.मार्ग('machines')), '--register'])
            self.आदेश(['VBoxManage', 'setextradata', राज्य_मूल्य['uuid'], 'JKOROS/Owner', राज्य_मूल्य['owner']])
        # सिस्टम_बांधणी 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        सिस्टम_माहिती = self.सिस्टम_माहिती(राज्य_मूल्य, नोंदणीकृत_नोंदी(self.आदेश(['VBoxManage', 'list', 'vms'])))
        if सिस्टम_माहिती.get('VMState') not in ('poweroff', 'aborted'):
            raise निष्पादन_त्रुटी('सिस्टम_बांधणी 중 VM 상태가 바뀌었습니다. पुनःप्रयत्न_मूल्य make vbox를 실행하세요.')
        self.माध्यमे_तपासा(राज्य_मूल्य, सिस्टम_माहिती)
        राज्य_मूल्य['iso'] = माध्यमे_मूल्य
        if माध्यमे_मूल्य not in राज्य_मूल्य['media']: राज्य_मूल्य['media'].append(माध्यमे_मूल्य)
        राज्य_मूल्य['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        लॉग_मूल्य = self.मार्ग(राज्य_मूल्य['serial_log'])
        लॉग_मूल्य.parent.mkdir(exist_ok=True)
        self.साठवणे_मूल्य(राज्य_मूल्य)
        self.आदेश(['VBoxManage', 'modifyvm', राज्य_मूल्य['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(लॉग_मूल्य)])
        नियंत्रक_यादी = [मूल्य for नाव, मूल्य in सिस्टम_माहिती.items() if re.fullmatch(r'storagecontrollername\d+', नाव)]
        if 'JKOROS IDE' not in नियंत्रक_यादी:
            self.आदेश(['VBoxManage', 'storagectl', राज्य_मूल्य['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.आदेश(['VBoxManage', 'storageattach', राज्य_मूल्य['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(गंतव्यस्थान_मूल्य)])
        राज्य_मूल्य['pending'] = False
        self.साठवणे_मूल्य(राज्य_मूल्य)
        self.आदेश(['VBoxManage', 'startvm', राज्य_मूल्य['uuid'], '--type', self.पद्धत_मोड])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.राज्य_शो()


def सुरू_करा():
    मूल्य_पार्स_करा = argparse.ArgumentParser(description='jkoros 전용 VirtualBox आज्ञा_कार्यवाही_करा 및 राज्य_मूल्य क्वेरी_मूल्य')
    मूल्य_पार्स_करा.add_argument('action', choices=['run', 'status'])
    परिमापन_वितर्क = मूल्य_पार्स_करा.parse_args()
    आज्ञा_कार्यवाही_करा = अनुप्रयोग_चालक(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if परिमापन_वितर्क.action == 'status':
        print(json.dumps(आज्ञा_कार्यवाही_करा.राज्य_शो(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise निष्पादन_त्रुटी('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise निष्पादन_त्रुटी('/dev/vboxdrv에 접근할 संख्या 없습니다. होस्ट 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/परवानगी_मूल्य 변경은 하지 않습니다.')
    os.umask(0o077)
    आज्ञा_कार्यवाही_करा.मार्ग('lock').parent.mkdir(parents=True, exist_ok=True)
    with आज्ञा_कार्यवाही_करा.मार्ग('lock').open('a') as कुलूप_मूल्य:
        try: fcntl.flock(कुलूप_मूल्य, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise निष्पादन_त्रुटी('다른 jkoros VirtualBox आज्ञा_कार्यवाही_करा 작업이 진행 중입니다.')
        print(json.dumps(आज्ञा_कार्यवाही_करा.आज्ञा_कार्यवाही_करा(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: सुरू_करा()
    except (निष्पादन_त्रुटी, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as त्रुटी:
        print('VBOX त्रुटी: ' + str(त्रुटी), file=sys.stderr)
        sys.exit(1)
