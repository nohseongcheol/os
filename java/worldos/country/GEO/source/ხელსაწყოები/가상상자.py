#!/usr/bin/env python3
"""jkoros 전용 VirtualBox აპი_გამშვები. 기존 VM/디스크/შენახვა_მნიშვნელობა 상태는 삭제하지 않는다."""
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


def შესრულება_გარემო_ბრძანება(인수):
    환경 = dict(os.environ, LC_ALL='C')
    გაზომვა = subprocess.run([str(მნიშვნელობა) for მნიშვნელობა in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    შიგთავსი_მნიშვნელობა = გაზომვა.stdout.decode('utf-8', 'replace')
    if გაზომვა.returncode:
        raise 실행오류('ბრძანება მარცხი_მნიშვნელობა: ' + ' '.join(str(მნიშვნელობა) for მნიშვნელობა in 인수) + '\n' + შიგთავსი_მნიშვნელობა[-10000:])
    return შიგთავსი_მნიშვნელობა


def ატრიბუტი_მნიშვნელობა(შიგთავსი_მნიშვნელობა):
    გაზომვა = {}
    for ხაზი in შიგთავსი_მნიშვნელობა.splitlines():
        if '=' not in ხაზი:
            continue
        სახელი, მნიშვნელობა = ხაზი.split('=', 1)
        if სახელი.startswith('"'):
            სახელი = json.loads(სახელი)
        if მნიშვნელობა.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(მნიშვნელობა)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(მნიშვნელობა): მნიშვნელობა = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ატრიბუტი_მნიშვნელობა ფორმატი_მნიშვნელობა შეცდომა: ' + ხაზი)
        გაზომვა[სახელი] = მნიშვნელობა
    return გაზომვა


def 등록목록(შიგთავსი_მნიშვნელობა):
    გაზომვა = {}
    for ხაზი in შიგთავსი_მნიშვნელობა.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ხაზი)
        if 일치: გაზომვა[일치.group(2).lower()] = 일치.group(1)
    return გაზომვა


def 검사합(გეზი):
    მნიშვნელობა = hashlib.sha256()
    with გეზი.open('rb') as ფაილი:
        for მონაცემები in iter(lambda: ფაილი.read(1024 * 1024), b''): მნიშვნელობა.update(მონაცემები)
    return მნიშვნელობა.hexdigest()


class აპი_გამშვები:
    def __init__(self, ფესვი_მნიშვნელობა, სახელი, მეთოდი_რეჟიმი='gui', ბრძანება=შესრულება_გარემო_ბრძანება):
        self.ფესვი_მნიშვნელობა = Path(ფესვი_მნიშვნელობა).resolve()
        self.სახელი, self.მეთოდი_რეჟიმი, self.ბრძანება = სახელი, მეთოდი_რეჟიმი, ბრძანება
        self.보관 = self.ფესვი_მნიშვნელობა / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', სახელი) or სახელი in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ციფრი_მნიშვნელობა·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if მეთოდი_რეჟიმი not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def გეზი(self, კვანძი_მნიშვნელობა_6a3b6fa7):
        if Path(კვანძი_მნიშვნელობა_6a3b6fa7).is_absolute() or '..' in Path(კვანძი_მნიშვნელობა_6a3b6fa7).parts:
            raise 실행오류('잘못된 관리 გეზი: ' + str(კვანძი_მნიშვნელობა_6a3b6fa7))
        გაზომვა = self.보관
        for 부분 in ['.vbox'] + list(Path(კვანძი_მნიშვნელობა_6a3b6fa7).parts):
            if 부분 == '.vbox': გაზომვა = self.보관
            else: გაზომვა = გაზომვა / 부분
            if გაზომვა.is_symlink(): raise 실행오류('დაკავშირება 경로는 사용하지 않습니다: ' + str(გაზომვა))
        return გაზომვა

    def კითხვა(self):
        გეზი = self.გეზი('state.json')
        if not გეზი.exists(): return None
        სტატუსი_მნიშვნელობა = json.loads(გეზი.read_text(encoding='utf-8'))
        if სტატუსი_მნიშვნელობა.get('version') != 1 or სტატუსი_მნიშვნელობა.get('name') != self.სახელი:
            raise 실행오류('관리 상태의 VM სახელი/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for სახელი in ('uuid', 'owner'):
            if str(uuid.UUID(სტატუსი_მნიშვნელობა[სახელი])) != სტატუსი_მნიშვნელობა[სახელი]: raise 실행오류('잘못된 VM იდენტიფიკატორი_მნიშვნელობა')
        return სტატუსი_მნიშვნელობა

    def შენახვა_მნიშვნელობა(self, სტატუსი_მნიშვნელობა):
        მიმართულება_მნიშვნელობა = self.გეზი('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ფაილი:
            json.dump(სტატუსი_მნიშვნელობა, ფაილი, ensure_ascii=False, indent=2)
            ფაილი.write('\n')
            임시 = ფაილი.name
        os.replace(임시, str(მიმართულება_მნიშვნელობა))

    def სისტემის_ინფორმაცია(self, სტატუსი_მნიშვნელობა, 등록됨, აღდგენა_სტატუსი=False):
        if სტატუსი_მნიშვნელობა['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        სისტემის_ინფორმაცია = ატრიბუტი_მნიშვნელობა(self.ბრძანება(['VBoxManage', 'showvminfo', სტატუსი_მნიშვნელობა['uuid'], '--machinereadable']))
        პოზიცია = Path(სისტემის_ინფორმაცია.get('CfgFile', '')).resolve()
        if self.გეზი('machines').resolve() not in პოზიცია.parents or სისტემის_ინფორმაცია.get('UUID') != სტატუსი_მნიშვნელობა['uuid']:
            raise 실행오류('이 프로젝트의 VM პარამეტრები გეზი/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ბრძანება(['VBoxManage', 'getextradata', სტატუსი_მნიშვნელობა['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + სტატუსი_მნიშვნელობა['owner']:
            if აღდგენა_სტატუსი and სტატუსი_მნიშვნელობა.get('pending') and 표식 == 'No value set!':
                self.ბრძანება(['VBoxManage', 'setextradata', სტატუსი_მნიშვნელობა['uuid'], 'JKOROS/Owner', სტატუსი_მნიშვნელობა['owner']])
            else:
                raise 실행오류('VM მფლობელი_მნიშვნელობა 표식이 일치하지 않아 변경하지 않습니다.')
        return სისტემის_ინფორმაცია

    def 매체검사(self, სტატუსი_მნიშვნელობა, სისტემის_ინფორმაცია):
        제어기들 = [მნიშვნელობა for სახელი, მნიშვნელობა in სისტემის_ინფორმაცია.items() if re.fullmatch(r'storagecontrollername\d+', სახელი)]
        ნების_დართვა_მნიშვნელობა = [str(self.გეზი(მნიშვნელობა)) for მნიშვნელობა in სტატუსი_მნიშვნელობა.get('media', [])]
        for სახელი, მნიშვნელობა in სისტემის_ინფორმაცია.items():
            if any(re.fullmatch(re.escape(კონტროლერი) + r'-\d+-\d+', სახელი) for კონტროლერი in 제어기들):
                if მნიშვნელობა not in ('none', 'emptydrive') and მნიშვნელობა not in ნების_დართვა_მნიშვნელობა:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + მნიშვნელობა)

    def ჩვენება_სტატუსი(self):
        სტატუსი_მნიშვნელობა = self.კითხვა()
        if სტატუსი_მნიშვნელობა is None: return {'name': self.სახელი, 'state': 'not-created'}
        სისტემის_ინფორმაცია = self.სისტემის_ინფორმაცია(სტატუსი_მნიშვნელობა, 등록목록(self.ბრძანება(['VBoxManage', 'list', 'vms'])))
        return {'name': სისტემის_ინფორმაცია.get('name', სტატუსი_მნიშვნელობა['name']), 'uuid': სტატუსი_მნიშვნელობა['uuid'], 'state': სისტემის_ინფორმაცია.get('VMState'),
                'iso': str(self.გეზი(სტატუსი_მნიშვნელობა['iso'])) if სტატუსი_მნიშვნელობა.get('iso') else None,
                'serial_log': str(self.გეზი(სტატუსი_მნიშვნელობა['serial_log'])) if სტატუსი_მნიშვნელობა.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def შესრულება_ბრძანება(self):
        სტატუსი_მნიშვნელობა = self.კითხვა()
        등록됨 = 등록목록(self.ბრძანება(['VBoxManage', 'list', 'vms']))
        სისტემის_ინფორმაცია = None
        if სტატუსი_მნიშვნელობა is not None and სტატუსი_მნიშვნელობა['uuid'] in 등록됨:
            სისტემის_ინფორმაცია = self.სისტემის_ინფორმაცია(სტატუსი_მნიშვნელობა, 등록됨, აღდგენა_სტატუსი=True)
            현재 = სისტემის_ინფორმაცია.get('VMState')
            if 현재 == 'running':
                print('이미 შესრულება_ბრძანება 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ჩვენება_სტატუსი()
            self.매체검사(სტატუსი_მნიშვნელობა, სისტემის_ინფორმაცია)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 შენახვა_მნიშვნელობა 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ბრძანება(['VBoxManage', 'controlvm', სტატუსი_მნიშვნელობა['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 გახსნა 전에 기존 기록도 보관한다.
                    if სტატუსი_მნიშვნელობა.get('serial_log'):
                        원본 = self.გეზი(სტატუსი_მნიშვნელობა['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.გეზი('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ბრძანება(['VBoxManage', 'startvm', სტატუსი_მნიშვნელობა['uuid'], '--type', self.მეთოდი_რეჟიმი])
                return self.ჩვენება_სტატუსი()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 გადართვა_რეჟიმი 중입니다 ({}). 작업이 끝난 უკან_მნიშვნელობა 다시 실행하세요.'.format(현재))
        elif სტატუსი_მნიშვნელობა is not None and not სტატუსი_მნიშვნელობა.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.სახელი in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # შენახვა_მნიშვნელობა/შესრულება_ბრძანება 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ბრძანება(['make', '-C', str(self.ფესვი_მნიშვნელობა / 'os'), 'iso']), end='')
        원본 = self.ფესვი_მნიშვნელობა / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        მიმართულება_მნიშვნელობა = self.გეზი(매체)
        მიმართულება_მნიშვნელობა.parent.mkdir(exist_ok=True)
        if მიმართულება_მნიშვნელობა.exists():
            if 검사합(მიმართულება_მნიშვნელობა) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(მიმართულება_მნიშვნელობა))
        else:
            with tempfile.NamedTemporaryFile(dir=str(მიმართულება_მნიშვნელობა.parent)) as ფაილი:
                shutil.copyfile(str(원본), ფაილი.name)
                os.link(ფაილი.name, str(მიმართულება_მნიშვნელობა))

        if სტატუსი_მნიშვნელობა is None:
            სტატუსი_მნიშვნელობა = {'version': 1, 'name': self.სახელი, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.შენახვა_მნიშვნელობა(სტატუსი_მნიშვნელობა)
        if სისტემის_ინფორმაცია is None:
            self.ბრძანება(['VBoxManage', 'createvm', '--name', სტატუსი_მნიშვნელობა['name'], '--uuid', სტატუსი_მნიშვნელობა['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.გეზი('machines')), '--register'])
            self.ბრძანება(['VBoxManage', 'setextradata', სტატუსი_მნიშვნელობა['uuid'], 'JKOROS/Owner', სტატუსი_მნიშვნელობა['owner']])
        # აწყობა_სისტემა 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        სისტემის_ინფორმაცია = self.სისტემის_ინფორმაცია(სტატუსი_მნიშვნელობა, 등록목록(self.ბრძანება(['VBoxManage', 'list', 'vms'])))
        if სისტემის_ინფორმაცია.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('აწყობა_სისტემა 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(სტატუსი_მნიშვნელობა, სისტემის_ინფორმაცია)
        სტატუსი_მნიშვნელობა['iso'] = 매체
        if 매체 not in სტატუსი_მნიშვნელობა['media']: სტატუსი_მნიშვნელობა['media'].append(매체)
        სტატუსი_მნიშვნელობა['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ჟურნალი_მნიშვნელობა = self.გეზი(სტატუსი_მნიშვნელობა['serial_log'])
        ჟურნალი_მნიშვნელობა.parent.mkdir(exist_ok=True)
        self.შენახვა_მნიშვნელობა(სტატუსი_მნიშვნელობა)
        self.ბრძანება(['VBoxManage', 'modifyvm', სტატუსი_მნიშვნელობა['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ჟურნალი_მნიშვნელობა)])
        제어기들 = [მნიშვნელობა for სახელი, მნიშვნელობა in სისტემის_ინფორმაცია.items() if re.fullmatch(r'storagecontrollername\d+', სახელი)]
        if 'JKOROS IDE' not in 제어기들:
            self.ბრძანება(['VBoxManage', 'storagectl', სტატუსი_მნიშვნელობა['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ბრძანება(['VBoxManage', 'storageattach', სტატუსი_მნიშვნელობა['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(მიმართულება_მნიშვნელობა)])
        სტატუსი_მნიშვნელობა['pending'] = False
        self.შენახვა_მნიშვნელობა(სტატუსი_მნიშვნელობა)
        self.ბრძანება(['VBoxManage', 'startvm', სტატუსი_მნიშვნელობა['uuid'], '--type', self.მეთოდი_რეჟიმი])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ჩვენება_სტატუსი()


def გაშვება():
    ანალიზი_მნიშვნელობა = argparse.ArgumentParser(description='jkoros 전용 VirtualBox შესრულება_ბრძანება 및 სტატუსი_მნიშვნელობა მოთხოვნა_მნიშვნელობა')
    ანალიზი_მნიშვნელობა.add_argument('action', choices=['run', 'status'])
    인자 = ანალიზი_მნიშვნელობა.parse_args()
    შესრულება_ბრძანება = აპი_გამშვები(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(შესრულება_ბრძანება.ჩვენება_სტატუსი(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. მასპინძელი 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ნებართვა_მნიშვნელობა 변경은 하지 않습니다.')
    os.umask(0o077)
    შესრულება_ბრძანება.გეზი('lock').parent.mkdir(parents=True, exist_ok=True)
    with შესრულება_ბრძანება.გეზი('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox შესრულება_ბრძანება 작업이 진행 중입니다.')
        print(json.dumps(შესრულება_ბრძანება.შესრულება_ბრძანება(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: გაშვება()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as შეცდომა:
        print('VBOX შეცდომა: ' + str(შეცდომა), file=sys.stderr)
        sys.exit(1)
