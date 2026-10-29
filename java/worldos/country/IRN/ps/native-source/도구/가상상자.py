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


def 명령실행(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(ارزښت) for ارزښت in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    منځپانګه_ارزښت = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('بولۍ پاتېينه_ارزښت: ' + ' '.join(str(ارزښت) for ارزښت in 인수) + '\n' + منځپانګه_ارزښت[-10000:])
    return منځپانګه_ارزښت


def ځانتیا_ارزښت(منځپانګه_ارزښت):
    결과 = {}
    for ليکه in منځپانګه_ارزښت.splitlines():
        if '=' not in ليکه:
            continue
        نوم, ارزښت = ليکه.split('=', 1)
        if نوم.startswith('"'):
            نوم = json.loads(نوم)
        if ارزښت.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ارزښت)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ارزښت): ارزښت = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ځانتیا_ارزښت بڼه_ارزښت تېروتنه: ' + ليکه)
        결과[نوم] = ارزښت
    return 결과


def 등록목록(منځپانګه_ارزښت):
    결과 = {}
    for ليکه in منځپانګه_ارزښت.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ليکه)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(يونلور):
    ارزښت = hashlib.sha256()
    with يونلور.open('rb') as دوتنه:
        for اومتوک in iter(lambda: دوتنه.read(1024 * 1024), b''): ارزښت.update(اومتوک)
    return ارزښت.hexdigest()


class 실행기:
    def __init__(self, 뿌리, نوم, 방식='gui', بولۍ=명령실행):
        self.뿌리 = Path(뿌리).resolve()
        self.نوم, self.방식, self.بولۍ = نوم, 방식, بولۍ
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', نوم) or نوم in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def يونلور(self, جوړه_ارزښت):
        if Path(جوړه_ارزښت).is_absolute() or '..' in Path(جوړه_ارزښت).parts:
            raise 실행오류('잘못된 관리 يونلور: ' + str(جوړه_ارزښت))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(جوړه_ارزښت).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('نښلېدل 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def لوستل(self):
        يونلور = self.يونلور('state.json')
        if not يونلور.exists(): return None
        انکړ_ارزښت = json.loads(يونلور.read_text(encoding='utf-8'))
        if انکړ_ارزښت.get('version') != 1 or انکړ_ارزښت.get('name') != self.نوم:
            raise 실행오류('관리 상태의 VM نوم/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for نوم in ('uuid', 'owner'):
            if str(uuid.UUID(انکړ_ارزښت[نوم])) != انکړ_ارزښت[نوم]: raise 실행오류('잘못된 VM 식별자')
        return انکړ_ارزښت

    def 저장(self, انکړ_ارزښت):
        موخه_ارزښت = self.يونلور('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as دوتنه:
            json.dump(انکړ_ارزښت, دوتنه, ensure_ascii=False, indent=2)
            دوتنه.write('\n')
            임시 = دوتنه.name
        os.replace(임시, str(موخه_ارزښت))

    def 정보(self, انکړ_ارزښت, 등록됨, 복구=False):
        if انکړ_ارزښت['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        정보 = ځانتیا_ارزښت(self.بولۍ(['VBoxManage', 'showvminfo', انکړ_ارزښت['uuid'], '--machinereadable']))
        ځای = Path(정보.get('CfgFile', '')).resolve()
        if self.يونلور('machines').resolve() not in ځای.parents or 정보.get('UUID') != انکړ_ارزښت['uuid']:
            raise 실행오류('이 프로젝트의 VM امستنې يونلور/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.بولۍ(['VBoxManage', 'getextradata', انکړ_ارزښت['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + انکړ_ارزښت['owner']:
            if 복구 and انکړ_ارزښت.get('pending') and 표식 == 'No value set!':
                self.بولۍ(['VBoxManage', 'setextradata', انکړ_ارزښت['uuid'], 'JKOROS/Owner', انکړ_ارزښت['owner']])
            else:
                raise 실행오류('VM 소유 표식이 일치하지 않아 변경하지 않습니다.')
        return 정보

    def کتل_رسنۍ(self, انکړ_ارزښت, 정보):
        제어기들 = [ارزښت for نوم, ارزښت in 정보.items() if re.fullmatch(r'storagecontrollername\d+', نوم)]
        پرېښل_ارزښت = [str(self.يونلور(ارزښت)) for ارزښت in انکړ_ارزښت.get('media', [])]
        for نوم, ارزښت in 정보.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', نوم) for 제어기 in 제어기들):
                if ارزښت not in ('none', 'emptydrive') and ارزښت not in پرېښل_ارزښت:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ارزښت)

    def 상태보기(self):
        انکړ_ارزښت = self.لوستل()
        if انکړ_ارزښت is None: return {'name': self.نوم, 'state': 'not-created'}
        정보 = self.정보(انکړ_ارزښت, 등록목록(self.بولۍ(['VBoxManage', 'list', 'vms'])))
        return {'name': 정보.get('name', انکړ_ارزښت['name']), 'uuid': انکړ_ارزښت['uuid'], 'state': 정보.get('VMState'),
                'iso': str(self.يونلور(انکړ_ارزښت['iso'])) if انکړ_ارزښت.get('iso') else None,
                'serial_log': str(self.يونلور(انکړ_ارزښت['serial_log'])) if انکړ_ارزښت.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        انکړ_ارزښت = self.لوستل()
        등록됨 = 등록목록(self.بولۍ(['VBoxManage', 'list', 'vms']))
        정보 = None
        if انکړ_ارزښت is not None and انکړ_ارزښت['uuid'] in 등록됨:
            정보 = self.정보(انکړ_ارزښت, 등록됨, 복구=True)
            현재 = 정보.get('VMState')
            if 현재 == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.상태보기()
            self.کتل_رسنۍ(انکړ_ارزښت, 정보)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 저장 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.بولۍ(['VBoxManage', 'controlvm', انکړ_ارزښت['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 پرانيستل 전에 기존 기록도 보관한다.
                    if انکړ_ارزښت.get('serial_log'):
                        원본 = self.يونلور(انکړ_ارزښت['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.يونلور('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.بولۍ(['VBoxManage', 'startvm', انکړ_ارزښت['uuid'], '--type', self.방식])
                return self.상태보기()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 전환 중입니다 ({}). 작업이 끝난 뒤 다시 실행하세요.'.format(현재))
        elif انکړ_ارزښت is not None and not انکړ_ارزښت.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.نوم in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # 저장/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.بولۍ(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        رسنۍ_ارزښت = 'media/kernel-' + 검사합(원본) + '.iso'
        موخه_ارزښت = self.يونلور(رسنۍ_ارزښت)
        موخه_ارزښت.parent.mkdir(exist_ok=True)
        if موخه_ارزښت.exists():
            if 검사합(موخه_ارزښت) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(موخه_ارزښت))
        else:
            with tempfile.NamedTemporaryFile(dir=str(موخه_ارزښت.parent)) as دوتنه:
                shutil.copyfile(str(원본), دوتنه.name)
                os.link(دوتنه.name, str(موخه_ارزښت))

        if انکړ_ارزښت is None:
            انکړ_ارزښت = {'version': 1, 'name': self.نوم, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.저장(انکړ_ارزښت)
        if 정보 is None:
            self.بولۍ(['VBoxManage', 'createvm', '--name', انکړ_ارزښت['name'], '--uuid', انکړ_ارزښت['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.يونلور('machines')), '--register'])
            self.بولۍ(['VBoxManage', 'setextradata', انکړ_ارزښت['uuid'], 'JKOROS/Owner', انکړ_ارزښت['owner']])
        # جوړول_غونډال 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        정보 = self.정보(انکړ_ارزښت, 등록목록(self.بولۍ(['VBoxManage', 'list', 'vms'])))
        if 정보.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('جوړول_غونډال 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.کتل_رسنۍ(انکړ_ارزښت, 정보)
        انکړ_ارزښت['iso'] = رسنۍ_ارزښت
        if رسنۍ_ارزښت not in انکړ_ارزښت['media']: انکړ_ارزښت['media'].append(رسنۍ_ارزښت)
        انکړ_ارزښت['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        خبرال_ارزښت = self.يونلور(انکړ_ارزښت['serial_log'])
        خبرال_ارزښت.parent.mkdir(exist_ok=True)
        self.저장(انکړ_ارزښت)
        self.بولۍ(['VBoxManage', 'modifyvm', انکړ_ارزښت['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(خبرال_ارزښت)])
        제어기들 = [ارزښت for نوم, ارزښت in 정보.items() if re.fullmatch(r'storagecontrollername\d+', نوم)]
        if 'JKOROS IDE' not in 제어기들:
            self.بولۍ(['VBoxManage', 'storagectl', انکړ_ارزښت['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.بولۍ(['VBoxManage', 'storageattach', انکړ_ارزښت['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(موخه_ارزښت)])
        انکړ_ارزښت['pending'] = False
        self.저장(انکړ_ارزښت)
        self.بولۍ(['VBoxManage', 'startvm', انکړ_ارزښت['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.상태보기()


def ځغلول():
    تجزیه_ارزښت = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 انکړ_ارزښت پوښتنه_ارزښت')
    تجزیه_ارزښت.add_argument('action', choices=['run', 'status'])
    인자 = تجزیه_ارزښت.parse_args()
    실행 = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(실행.상태보기(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. کوربه 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/권한 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.يونلور('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.يونلور('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ځغلول()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as تېروتنه:
        print('VBOX تېروتنه: ' + str(تېروتنه), file=sys.stderr)
        sys.exit(1)
