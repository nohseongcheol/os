#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 실행기. 기존 VM/디스크/похранити_вриједност 상태는 삭제하지 않는다."""
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
    결과 = subprocess.run([str(вриједност) for вриједност in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Садржај_вриједност = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('команда неуспјех_вриједност: ' + ' '.join(str(вриједност) for вриједност in 인수) + '\n' + Садржај_вриједност[-10000:])
    return Садржај_вриједност


def атрибут_вриједност(Садржај_вриједност):
    결과 = {}
    for редак in Садржај_вриједност.splitlines():
        if '=' not in редак:
            continue
        назив, вриједност = редак.split('=', 1)
        if назив.startswith('"'):
            назив = json.loads(назив)
        if вриједност.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(вриједност)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(вриједност): вриједност = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_вриједност формат_вриједност грешка: ' + редак)
        결과[назив] = вриједност
    return 결과


def 등록목록(Садржај_вриједност):
    결과 = {}
    for редак in Садржај_вриједност.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', редак)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(пут):
    вриједност = hashlib.sha256()
    with пут.open('rb') as фајл:
        for подаци in iter(lambda: фајл.read(1024 * 1024), b''): вриједност.update(подаци)
    return вриједност.hexdigest()


class 실행기:
    def __init__(self, 뿌리, назив, 방식='gui', команда=명령실행):
        self.뿌리 = Path(뿌리).resolve()
        self.назив, self.방식, self.команда = назив, 방식, команда
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', назив) or назив in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def пут(self, peer_вриједност):
        if Path(peer_вриједност).is_absolute() or '..' in Path(peer_вриједност).parts:
            raise 실행오류('잘못된 관리 пут: ' + str(peer_вриједност))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_вриједност).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('повезати 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        пут = self.пут('state.json')
        if not пут.exists(): return None
        стање_вриједност = json.loads(пут.read_text(encoding='utf-8'))
        if стање_вриједност.get('version') != 1 or стање_вриједност.get('name') != self.назив:
            raise 실행오류('관리 상태의 VM назив/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for назив in ('uuid', 'owner'):
            if str(uuid.UUID(стање_вриједност[назив])) != стање_вриједност[назив]: raise 실행오류('잘못된 VM 식별자')
        return стање_вриједност

    def похранити_вриједност(self, стање_вриједност):
        одредиште_вриједност = self.пут('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as фајл:
            json.dump(стање_вриједност, фајл, ensure_ascii=False, indent=2)
            фајл.write('\n')
            임시 = фајл.name
        os.replace(임시, str(одредиште_вриједност))

    def систем_информација(self, стање_вриједност, 등록됨, 복구=False):
        if стање_вриједност['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        систем_информација = атрибут_вриједност(self.команда(['VBoxManage', 'showvminfo', стање_вриједност['uuid'], '--machinereadable']))
        위치 = Path(систем_информација.get('CfgFile', '')).resolve()
        if self.пут('machines').resolve() not in 위치.parents or систем_информација.get('UUID') != стање_вриједност['uuid']:
            raise 실행오류('이 프로젝트의 VM Подешавања пут/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.команда(['VBoxManage', 'getextradata', стање_вриједност['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + стање_вриједност['owner']:
            if 복구 and стање_вриједност.get('pending') and 표식 == 'No value set!':
                self.команда(['VBoxManage', 'setextradata', стање_вриједност['uuid'], 'JKOROS/Owner', стање_вриједност['owner']])
            else:
                raise 실행오류('VM 소유 표식이 일치하지 않아 변경하지 않습니다.')
        return систем_информација

    def 매체검사(self, стање_вриједност, систем_информација):
        제어기들 = [вриједност for назив, вриједност in систем_информација.items() if re.fullmatch(r'storagecontrollername\d+', назив)]
        Дозволити_вриједност = [str(self.пут(вриједност)) for вриједност in стање_вриједност.get('media', [])]
        for назив, вриједност in систем_информација.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', назив) for 제어기 in 제어기들):
                if вриједност not in ('none', 'emptydrive') and вриједност not in Дозволити_вриједност:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + вриједност)

    def приказати_стање(self):
        стање_вриједност = self.읽기()
        if стање_вриједност is None: return {'name': self.назив, 'state': 'not-created'}
        систем_информација = self.систем_информација(стање_вриједност, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        return {'name': систем_информација.get('name', стање_вриједност['name']), 'uuid': стање_вриједност['uuid'], 'state': систем_информација.get('VMState'),
                'iso': str(self.пут(стање_вриједност['iso'])) if стање_вриједност.get('iso') else None,
                'serial_log': str(self.пут(стање_вриједност['serial_log'])) if стање_вриједност.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        стање_вриједност = self.읽기()
        등록됨 = 등록목록(self.команда(['VBoxManage', 'list', 'vms']))
        систем_информација = None
        if стање_вриједност is not None and стање_вриједност['uuid'] in 등록됨:
            систем_информација = self.систем_информација(стање_вриједност, 등록됨, 복구=True)
            현재 = систем_информација.get('VMState')
            if 현재 == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.приказати_стање()
            self.매체검사(стање_вриједност, систем_информација)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 похранити_вриједност 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.команда(['VBoxManage', 'controlvm', стање_вриједност['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 отворити 전에 기존 기록도 보관한다.
                    if стање_вриједност.get('serial_log'):
                        원본 = self.пут(стање_вриједност['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.пут('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.команда(['VBoxManage', 'startvm', стање_вриједност['uuid'], '--type', self.방식])
                return self.приказати_стање()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 промијенити_мод 중입니다 ({}). 작업이 끝난 Назад_вриједност 다시 실행하세요.'.format(현재))
        elif стање_вриједност is not None and not стање_вриједност.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.назив in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # похранити_вриједност/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.команда(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        одредиште_вриједност = self.пут(매체)
        одредиште_вриједност.parent.mkdir(exist_ok=True)
        if одредиште_вриједност.exists():
            if 검사합(одредиште_вриједност) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(одредиште_вриједност))
        else:
            with tempfile.NamedTemporaryFile(dir=str(одредиште_вриједност.parent)) as фајл:
                shutil.copyfile(str(원본), фајл.name)
                os.link(фајл.name, str(одредиште_вриједност))

        if стање_вриједност is None:
            стање_вриједност = {'version': 1, 'name': self.назив, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.похранити_вриједност(стање_вриједност)
        if систем_информација is None:
            self.команда(['VBoxManage', 'createvm', '--name', стање_вриједност['name'], '--uuid', стање_вриједност['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.пут('machines')), '--register'])
            self.команда(['VBoxManage', 'setextradata', стање_вриједност['uuid'], 'JKOROS/Owner', стање_вриједност['owner']])
        # направити_систем 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        систем_информација = self.систем_информација(стање_вриједност, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        if систем_информација.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('направити_систем 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(стање_вриједност, систем_информација)
        стање_вриједност['iso'] = 매체
        if 매체 not in стање_вриједност['media']: стање_вриједност['media'].append(매체)
        стање_вриједност['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        дневник_рада_вриједност = self.пут(стање_вриједност['serial_log'])
        дневник_рада_вриједност.parent.mkdir(exist_ok=True)
        self.похранити_вриједност(стање_вриједност)
        self.команда(['VBoxManage', 'modifyvm', стање_вриједност['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(дневник_рада_вриједност)])
        제어기들 = [вриједност for назив, вриједност in систем_информација.items() if re.fullmatch(r'storagecontrollername\d+', назив)]
        if 'JKOROS IDE' not in 제어기들:
            self.команда(['VBoxManage', 'storagectl', стање_вриједност['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.команда(['VBoxManage', 'storageattach', стање_вриједност['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(одредиште_вриједност)])
        стање_вриједност['pending'] = False
        self.похранити_вриједност(стање_вриједност)
        self.команда(['VBoxManage', 'startvm', стање_вриједност['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.приказати_стање()


def 시작():
    рашчлањивати_вриједност = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 стање_вриједност упит_вриједност')
    рашчлањивати_вриједност.add_argument('action', choices=['run', 'status'])
    인자 = рашчлањивати_вриједност.parse_args()
    실행 = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(실행.приказати_стање(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. хост_рачунар 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/дозвола_вриједност 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.пут('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.пут('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: 시작()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as грешка:
        print('VBOX грешка: ' + str(грешка), file=sys.stderr)
        sys.exit(1)
