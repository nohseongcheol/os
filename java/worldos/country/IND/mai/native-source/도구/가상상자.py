#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 실행기. 기존 VM/디스크/저장 상태는 삭제하지 않는다."""
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


def 명령실행(आर्गुमेंट्स):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(값) for 값 in आर्गुमेंट्स], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    내용 = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('कमांड 실패: ' + ' '.join(str(값) for 값 in आर्गुमेंट्स) + '\n' + 내용[-10000:])
    return 내용


def 속성(내용):
    결과 = {}
    for 줄 in 내용.splitlines():
        if '=' not in 줄:
            continue
        नाम, 값 = 줄.split('=', 1)
        if नाम.startswith('"'):
            नाम = json.loads(नाम)
        if 값.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(값)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(값): 값 = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox 속성 형식 त्रुटि: ' + 줄)
        결과[नाम] = 값
    return 결과


def 등록목록(내용):
    결과 = {}
    for 줄 in 내용.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', 줄)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(पथ):
    값 = hashlib.sha256()
    with पथ.open('rb') as फाइल:
        for 자료 in iter(lambda: फाइल.read(1024 * 1024), b''): 값.update(자료)
    return 값.hexdigest()


class 실행기:
    def __init__(self, 뿌리, नाम, 방식='gui', कमांड=명령실행):
        self.뿌리 = Path(뿌리).resolve()
        self.नाम, self.방식, self.कमांड = नाम, 방식, कमांड
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', नाम) or नाम in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def पथ(self, 상대):
        if Path(상대).is_absolute() or '..' in Path(상대).parts:
            raise 실행오류('잘못된 관리 पथ: ' + str(상대))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(상대).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('जुड़ू 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def पढ़ू(self):
        पथ = self.पथ('state.json')
        if not पथ.exists(): return None
        상태 = json.loads(पथ.read_text(encoding='utf-8'))
        if 상태.get('version') != 1 or 상태.get('name') != self.नाम:
            raise 실행오류('관리 상태의 VM नाम/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for नाम in ('uuid', 'owner'):
            if str(uuid.UUID(상태[नाम])) != 상태[नाम]: raise 실행오류('잘못된 VM 식별자')
        return 상태

    def 저장(self, 상태):
        목적 = self.पथ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as फाइल:
            json.dump(상태, फाइल, ensure_ascii=False, indent=2)
            फाइल.write('\n')
            임시 = फाइल.name
        os.replace(임시, str(목적))

    def 정보(self, 상태, 등록됨, 복구=False):
        if 상태['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        정보 = 속성(self.कमांड(['VBoxManage', 'showvminfo', 상태['uuid'], '--machinereadable']))
        स्थिति = Path(정보.get('CfgFile', '')).resolve()
        if self.पथ('machines').resolve() not in स्थिति.parents or 정보.get('UUID') != 상태['uuid']:
            raise 실행오류('이 프로젝트의 VM जमावट पथ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.कमांड(['VBoxManage', 'getextradata', 상태['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + 상태['owner']:
            if 복구 and 상태.get('pending') and 표식 == 'No value set!':
                self.कमांड(['VBoxManage', 'setextradata', 상태['uuid'], 'JKOROS/Owner', 상태['owner']])
            else:
                raise 실행오류('VM 소유 표식이 일치하지 않아 변경하지 않습니다.')
        return 정보

    def 매체검사(self, 상태, 정보):
        제어기들 = [값 for नाम, 값 in 정보.items() if re.fullmatch(r'storagecontrollername\d+', नाम)]
        허용 = [str(self.पथ(값)) for 값 in 상태.get('media', [])]
        for नाम, 값 in 정보.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', नाम) for 제어기 in 제어기들):
                if 값 not in ('none', 'emptydrive') and 값 not in 허용:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + 값)

    def 상태보기(self):
        상태 = self.पढ़ू()
        if 상태 is None: return {'name': self.नाम, 'state': 'not-created'}
        정보 = self.정보(상태, 등록목록(self.कमांड(['VBoxManage', 'list', 'vms'])))
        return {'name': 정보.get('name', 상태['name']), 'uuid': 상태['uuid'], 'state': 정보.get('VMState'),
                'iso': str(self.पथ(상태['iso'])) if 상태.get('iso') else None,
                'serial_log': str(self.पथ(상태['serial_log'])) if 상태.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        상태 = self.पढ़ू()
        등록됨 = 등록목록(self.कमांड(['VBoxManage', 'list', 'vms']))
        정보 = None
        if 상태 is not None and 상태['uuid'] in 등록됨:
            정보 = self.정보(상태, 등록됨, 복구=True)
            현재 = 정보.get('VMState')
            if 현재 == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.상태보기()
            self.매체검사(상태, 정보)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 저장 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.कमांड(['VBoxManage', 'controlvm', 상태['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 खोलू 전에 기존 기록도 보관한다.
                    if 상태.get('serial_log'):
                        원본 = self.पथ(상태['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.पथ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.कमांड(['VBoxManage', 'startvm', 상태['uuid'], '--type', self.방식])
                return self.상태보기()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 전환 중입니다 ({}). 작업이 끝난 뒤 다시 실행하세요.'.format(현재))
        elif 상태 is not None and not 상태.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.नाम in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # 저장/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.कमांड(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        목적 = self.पथ(매체)
        목적.parent.mkdir(exist_ok=True)
        if 목적.exists():
            if 검사합(목적) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(목적))
        else:
            with tempfile.NamedTemporaryFile(dir=str(목적.parent)) as फाइल:
                shutil.copyfile(str(원본), फाइल.name)
                os.link(फाइल.name, str(목적))

        if 상태 is None:
            상태 = {'version': 1, 'name': self.नाम, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.저장(상태)
        if 정보 is None:
            self.कमांड(['VBoxManage', 'createvm', '--name', 상태['name'], '--uuid', 상태['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.पथ('machines')), '--register'])
            self.कमांड(['VBoxManage', 'setextradata', 상태['uuid'], 'JKOROS/Owner', 상태['owner']])
        # 빌드 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        정보 = self.정보(상태, 등록목록(self.कमांड(['VBoxManage', 'list', 'vms'])))
        if 정보.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('빌드 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(상태, 정보)
        상태['iso'] = 매체
        if 매체 not in 상태['media']: 상태['media'].append(매체)
        상태['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        로그 = self.पथ(상태['serial_log'])
        로그.parent.mkdir(exist_ok=True)
        self.저장(상태)
        self.कमांड(['VBoxManage', 'modifyvm', 상태['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(로그)])
        제어기들 = [값 for नाम, 값 in 정보.items() if re.fullmatch(r'storagecontrollername\d+', नाम)]
        if 'JKOROS IDE' not in 제어기들:
            self.कमांड(['VBoxManage', 'storagectl', 상태['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.कमांड(['VBoxManage', 'storageattach', 상태['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(목적)])
        상태['pending'] = False
        self.저장(상태)
        self.कमांड(['VBoxManage', 'startvm', 상태['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.상태보기()


def चलाबू():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 상태 조회')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    실행 = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(실행.상태보기(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. 호스트 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/권한 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.पथ('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.पथ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: चलाबू()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as त्रुटि:
        print('VBOX त्रुटि: ' + str(त्रुटि), file=sys.stderr)
        sys.exit(1)
