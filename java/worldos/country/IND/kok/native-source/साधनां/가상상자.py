#!/usr/bin/env python3
"""jkoros 전용 VirtualBox एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर. 기존 VM/디스크/Store_मोल 상태는 삭제하지 않는다."""
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


def पाळो_दिवचो_शॅल_आदेश(인수):
    환경 = dict(os.environ, LC_ALL='C')
    मेजप = subprocess.run([str(मोल) for मोल in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    अनुक्रमणिका_मोल = मेजप.stdout.decode('utf-8', 'replace')
    if मेजप.returncode:
        raise 실행오류('आदेश अपेस_मोल: ' + ' '.join(str(मोल) for मोल in 인수) + '\n' + अनुक्रमणिका_मोल[-10000:])
    return अनुक्रमणिका_मोल


def खाशेलपण_मोल(अनुक्रमणिका_मोल):
    मेजप = {}
    for रेग in अनुक्रमणिका_मोल.splitlines():
        if '=' not in रेग:
            continue
        नांव, मोल = रेग.split('=', 1)
        if नांव.startswith('"'):
            नांव = json.loads(नांव)
        if मोल.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(मोल)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(मोल): मोल = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox खाशेलपण_मोल स्वरूप_मोल चूक: ' + रेग)
        मेजप[नांव] = मोल
    return मेजप


def 등록목록(अनुक्रमणिका_मोल):
    मेजप = {}
    for रेग in अनुक्रमणिका_मोल.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', रेग)
        if 일치: मेजप[일치.group(2).lower()] = 일치.group(1)
    return मेजप


def 검사합(पाथ):
    मोल = hashlib.sha256()
    with पाथ.open('rb') as फायल:
        for डेटा in iter(lambda: फायल.read(1024 * 1024), b''): मोल.update(डेटा)
    return मोल.hexdigest()


class एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर:
    def __init__(self, रूट_मोल, नांव, पद्दत_मोड='gui', आदेश=पाळो_दिवचो_शॅल_आदेश):
        self.रूट_मोल = Path(रूट_मोल).resolve()
        self.नांव, self.पद्दत_मोड, self.आदेश = नांव, पद्दत_मोड, आदेश
        self.보관 = self.रूट_मोल / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', नांव) or नांव in ('.', '..'):
            raise 실행오류('VM 이름은 문자·अंक_मोल·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if पद्दत_मोड not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def पाथ(self, पीयर_मोल):
        if Path(पीयर_मोल).is_absolute() or '..' in Path(पीयर_मोल).parts:
            raise 실행오류('잘못된 관리 पाथ: ' + str(पीयर_मोल))
        मेजप = self.보관
        for 부분 in ['.vbox'] + list(Path(पीयर_मोल).parts):
            if 부분 == '.vbox': मेजप = self.보관
            else: मेजप = मेजप / 부분
            if मेजप.is_symlink(): raise 실행오류('कनॅक्ट 경로는 사용하지 않습니다: ' + str(मेजप))
        return मेजप

    def 읽기(self):
        पाथ = self.पाथ('state.json')
        if not पाथ.exists(): return None
        स्थिती_मोल_e10195a1 = json.loads(पाथ.read_text(encoding='utf-8'))
        if स्थिती_मोल_e10195a1.get('version') != 1 or स्थिती_मोल_e10195a1.get('name') != self.नांव:
            raise 실행오류('관리 상태의 VM नांव/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for नांव in ('uuid', 'owner'):
            if str(uuid.UUID(स्थिती_मोल_e10195a1[नांव])) != स्थिती_मोल_e10195a1[नांव]: raise 실행오류('잘못된 VM वळखुपी_मोल')
        return स्थिती_मोल_e10195a1

    def Store_मोल(self, स्थिती_मोल_e10195a1):
        नियुक्त_स्थान_मोल = self.पाथ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as फायल:
            json.dump(स्थिती_मोल_e10195a1, फायल, ensure_ascii=False, indent=2)
            फायल.write('\n')
            임시 = फायल.name
        os.replace(임시, str(नियुक्त_स्थान_मोल))

    def msinfo32_exe(self, स्थिती_मोल_e10195a1, 등록됨, परतून_मेळोवचें_स्थिती=False):
        if स्थिती_मोल_e10195a1['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = खाशेलपण_मोल(self.आदेश(['VBoxManage', 'showvminfo', स्थिती_मोल_e10195a1['uuid'], '--machinereadable']))
        स्थिती = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.पाथ('machines').resolve() not in स्थिती.parents or msinfo32_exe.get('UUID') != स्थिती_मोल_e10195a1['uuid']:
            raise 실행오류('이 프로젝트의 VM मांडावळी पाथ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.आदेश(['VBoxManage', 'getextradata', स्थिती_मोल_e10195a1['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + स्थिती_मोल_e10195a1['owner']:
            if परतून_मेळोवचें_स्थिती and स्थिती_मोल_e10195a1.get('pending') and 표식 == 'No value set!':
                self.आदेश(['VBoxManage', 'setextradata', स्थिती_मोल_e10195a1['uuid'], 'JKOROS/Owner', स्थिती_मोल_e10195a1['owner']])
            else:
                raise 실행오류('VM धनी_मोल 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, स्थिती_मोल_e10195a1, msinfo32_exe):
        제어기들 = [मोल for नांव, मोल in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', नांव)]
        परवानगी_दिवची_मोल = [str(self.पाथ(मोल)) for मोल in स्थिती_मोल_e10195a1.get('media', [])]
        for नांव, मोल in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(नियंत्रक) + r'-\d+-\d+', नांव) for नियंत्रक in 제어기들):
                if मोल not in ('none', 'emptydrive') and मोल not in परवानगी_दिवची_मोल:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + मोल)

    def शो_स्थिती(self):
        स्थिती_मोल_e10195a1 = self.읽기()
        if स्थिती_मोल_e10195a1 is None: return {'name': self.नांव, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(स्थिती_मोल_e10195a1, 등록목록(self.आदेश(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', स्थिती_मोल_e10195a1['name']), 'uuid': स्थिती_मोल_e10195a1['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.पाथ(स्थिती_मोल_e10195a1['iso'])) if स्थिती_मोल_e10195a1.get('iso') else None,
                'serial_log': str(self.पाथ(स्थिती_मोल_e10195a1['serial_log'])) if स्थिती_मोल_e10195a1.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def पाळो_दिवचो_आदेश(self):
        स्थिती_मोल_e10195a1 = self.읽기()
        등록됨 = 등록목록(self.आदेश(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if स्थिती_मोल_e10195a1 is not None and स्थिती_मोल_e10195a1['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(स्थिती_मोल_e10195a1, 등록됨, परतून_मेळोवचें_स्थिती=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 पाळो_दिवचो_आदेश 중입니다. 재빌드·재시작하지 않습니다.')
                return self.शो_स्थिती()
            self.매체검사(स्थिती_मोल_e10195a1, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_मोल 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.आदेश(['VBoxManage', 'controlvm', स्थिती_मोल_e10195a1['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 उगडचें 전에 기존 기록도 보관한다.
                    if स्थिती_मोल_e10195a1.get('serial_log'):
                        원본 = self.पाथ(स्थिती_मोल_e10195a1['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.पाथ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.आदेश(['VBoxManage', 'startvm', स्थिती_मोल_e10195a1['uuid'], '--type', self.पद्दत_मोड])
                return self.शो_स्थिती()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 स्विच_मोड 중입니다 ({}). 작업이 끝난 फाटीं_मोल 다시 실행하세요.'.format(현재))
        elif स्थिती_मोल_e10195a1 is not None and not स्थिती_मोल_e10195a1.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.नांव in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_मोल/पाळो_दिवचो_आदेश 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.आदेश(['make', '-C', str(self.रूट_मोल / 'os'), 'iso']), end='')
        원본 = self.रूट_मोल / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        नियुक्त_स्थान_मोल = self.पाथ(매체)
        नियुक्त_स्थान_मोल.parent.mkdir(exist_ok=True)
        if नियुक्त_स्थान_मोल.exists():
            if 검사합(नियुक्त_स्थान_मोल) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(नियुक्त_स्थान_मोल))
        else:
            with tempfile.NamedTemporaryFile(dir=str(नियुक्त_स्थान_मोल.parent)) as फायल:
                shutil.copyfile(str(원본), फायल.name)
                os.link(फायल.name, str(नियुक्त_स्थान_मोल))

        if स्थिती_मोल_e10195a1 is None:
            स्थिती_मोल_e10195a1 = {'version': 1, 'name': self.नांव, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_मोल(स्थिती_मोल_e10195a1)
        if msinfo32_exe is None:
            self.आदेश(['VBoxManage', 'createvm', '--name', स्थिती_मोल_e10195a1['name'], '--uuid', स्थिती_मोल_e10195a1['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.पाथ('machines')), '--register'])
            self.आदेश(['VBoxManage', 'setextradata', स्थिती_मोल_e10195a1['uuid'], 'JKOROS/Owner', स्थिती_मोल_e10195a1['owner']])
        # दाळचे_प्रणाली 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(स्थिती_मोल_e10195a1, 등록목록(self.आदेश(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('दाळचे_प्रणाली 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(स्थिती_मोल_e10195a1, msinfo32_exe)
        स्थिती_मोल_e10195a1['iso'] = 매체
        if 매체 not in स्थिती_मोल_e10195a1['media']: स्थिती_मोल_e10195a1['media'].append(매체)
        स्थिती_मोल_e10195a1['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_मोल = self.पाथ(स्थिती_मोल_e10195a1['serial_log'])
        LOG_मोल.parent.mkdir(exist_ok=True)
        self.Store_मोल(स्थिती_मोल_e10195a1)
        self.आदेश(['VBoxManage', 'modifyvm', स्थिती_मोल_e10195a1['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_मोल)])
        제어기들 = [मोल for नांव, मोल in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', नांव)]
        if 'JKOROS IDE' not in 제어기들:
            self.आदेश(['VBoxManage', 'storagectl', स्थिती_मोल_e10195a1['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.आदेश(['VBoxManage', 'storageattach', स्थिती_मोल_e10195a1['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(नियुक्त_स्थान_मोल)])
        स्थिती_मोल_e10195a1['pending'] = False
        self.Store_मोल(स्थिती_मोल_e10195a1)
        self.आदेश(['VBoxManage', 'startvm', स्थिती_मोल_e10195a1['uuid'], '--type', self.पद्दत_मोड])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.शो_स्थिती()


def चलोवप():
    व्याकरणी_फोडणिशी_मोल = argparse.ArgumentParser(description='jkoros 전용 VirtualBox पाळो_दिवचो_आदेश 및 स्थिती_मोल_e10195a1 क्वॅरी_मोल')
    व्याकरणी_फोडणिशी_मोल.add_argument('action', choices=['run', 'status'])
    인자 = व्याकरणी_फोडणिशी_मोल.parse_args()
    पाळो_दिवचो_आदेश = एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(पाळो_दिवचो_आदेश.शो_स्थिती(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. येजमान 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/अनुमती_मोल 변경은 하지 않습니다.')
    os.umask(0o077)
    पाळो_दिवचो_आदेश.पाथ('lock').parent.mkdir(parents=True, exist_ok=True)
    with पाळो_दिवचो_आदेश.पाथ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox पाळो_दिवचो_आदेश 작업이 진행 중입니다.')
        print(json.dumps(पाळो_दिवचो_आदेश.पाळो_दिवचो_आदेश(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: चलोवप()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as चूक:
        print('VBOX चूक: ' + str(चूक), file=sys.stderr)
        sys.exit(1)
