#!/usr/bin/env python3
"""jkoros 전용 VirtualBox праграма_выклік_праграм. 기존 VM/디스크/сховішча_значэнне 상태는 삭제하지 않는다."""
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


def выканаць_абалонка_каманда(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(значэнне) for значэнне in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    кантэнт_значэнне = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Загад няўдача_значэнне: ' + ' '.join(str(значэнне) for значэнне in 인수) + '\n' + кантэнт_значэнне[-10000:])
    return кантэнт_значэнне


def атрыбут_значэнне(кантэнт_значэнне):
    결과 = {}
    for лінія in кантэнт_значэнне.splitlines():
        if '=' not in лінія:
            continue
        Назва, значэнне = лінія.split('=', 1)
        if Назва.startswith('"'):
            Назва = json.loads(Назва)
        if значэнне.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(значэнне)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(значэнне): значэнне = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрыбут_значэнне фармат_значэнне ПАМЫЛКА: ' + лінія)
        결과[Назва] = значэнне
    return 결과


def 등록목록(кантэнт_значэнне):
    결과 = {}
    for лінія in кантэнт_значэнне.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', лінія)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def кантрольная_сума(ШЛЯХ):
    значэнне = hashlib.sha256()
    with ШЛЯХ.open('rb') as Файл:
        for дадзеныя in iter(lambda: Файл.read(1024 * 1024), b''): значэнне.update(дадзеныя)
    return значэнне.hexdigest()


class праграма_выклік_праграм:
    def __init__(self, 뿌리, Назва, спосаб_рэжым='gui', Загад=выканаць_абалонка_каманда):
        self.뿌리 = Path(뿌리).resolve()
        self.Назва, self.спосаб_рэжым, self.Загад = Назва, спосаб_рэжым, Загад
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Назва) or Назва in ('.', '..'):
            raise 실행오류('VM 이름은 문자·лічба_значэнне·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if спосаб_рэжым not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ШЛЯХ(self, аднарангавы_значэнне):
        if Path(аднарангавы_значэнне).is_absolute() or '..' in Path(аднарангавы_значэнне).parts:
            raise 실행오류('잘못된 관리 ШЛЯХ: ' + str(аднарангавы_значэнне))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(аднарангавы_значэнне).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Злучыцца 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Чытанне(self):
        ШЛЯХ = self.ШЛЯХ('state.json')
        if not ШЛЯХ.exists(): return None
        стан_значэнне = json.loads(ШЛЯХ.read_text(encoding='utf-8'))
        if стан_значэнне.get('version') != 1 or стан_значэнне.get('name') != self.Назва:
            raise 실행오류('관리 상태의 VM Назва/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Назва in ('uuid', 'owner'):
            if str(uuid.UUID(стан_значэнне[Назва])) != стан_значэнне[Назва]: raise 실행오류('잘못된 VM ідэнтыфікатар_значэнне')
        return стан_значэнне

    def сховішча_значэнне(self, стан_значэнне):
        прызначэнне_значэнне_a0fbc067 = self.ШЛЯХ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Файл:
            json.dump(стан_значэнне, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
            임시 = Файл.name
        os.replace(임시, str(прызначэнне_значэнне_a0fbc067))

    def Сістэмная_інфармацыя(self, стан_значэнне, 등록됨, аднавіць_стан=False):
        if стан_значэнне['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Сістэмная_інфармацыя = атрыбут_значэнне(self.Загад(['VBoxManage', 'showvminfo', стан_значэнне['uuid'], '--machinereadable']))
        Пазіцыя = Path(Сістэмная_інфармацыя.get('CfgFile', '')).resolve()
        if self.ШЛЯХ('machines').resolve() not in Пазіцыя.parents or Сістэмная_інфармацыя.get('UUID') != стан_значэнне['uuid']:
            raise 실행오류('이 프로젝트의 VM Усталёўкі ШЛЯХ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Загад(['VBoxManage', 'getextradata', стан_значэнне['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + стан_значэнне['owner']:
            if аднавіць_стан and стан_значэнне.get('pending') and 표식 == 'No value set!':
                self.Загад(['VBoxManage', 'setextradata', стан_значэнне['uuid'], 'JKOROS/Owner', стан_значэнне['owner']])
            else:
                raise 실행오류('VM уласнік_значэнне 표식이 일치하지 않아 변경하지 않습니다.')
        return Сістэмная_інфармацыя

    def чэк_носьбіт(self, стан_значэнне, Сістэмная_інфармацыя):
        제어기들 = [значэнне for Назва, значэнне in Сістэмная_інфармацыя.items() if re.fullmatch(r'storagecontrollername\d+', Назва)]
        Дазволіць_значэнне = [str(self.ШЛЯХ(значэнне)) for значэнне in стан_значэнне.get('media', [])]
        for Назва, значэнне in Сістэмная_інфармацыя.items():
            if any(re.fullmatch(re.escape(адміністратар_дадзеных) + r'-\d+-\d+', Назва) for адміністратар_дадзеных in 제어기들):
                if значэнне not in ('none', 'emptydrive') and значэнне not in Дазволіць_значэнне:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + значэнне)

    def паказаць_стан(self):
        стан_значэнне = self.Чытанне()
        if стан_значэнне is None: return {'name': self.Назва, 'state': 'not-created'}
        Сістэмная_інфармацыя = self.Сістэмная_інфармацыя(стан_значэнне, 등록목록(self.Загад(['VBoxManage', 'list', 'vms'])))
        return {'name': Сістэмная_інфармацыя.get('name', стан_значэнне['name']), 'uuid': стан_значэнне['uuid'], 'state': Сістэмная_інфармацыя.get('VMState'),
                'iso': str(self.ШЛЯХ(стан_значэнне['iso'])) if стан_значэнне.get('iso') else None,
                'serial_log': str(self.ШЛЯХ(стан_значэнне['serial_log'])) if стан_значэнне.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def выканаць_каманда(self):
        стан_значэнне = self.Чытанне()
        등록됨 = 등록목록(self.Загад(['VBoxManage', 'list', 'vms']))
        Сістэмная_інфармацыя = None
        if стан_значэнне is not None and стан_значэнне['uuid'] in 등록됨:
            Сістэмная_інфармацыя = self.Сістэмная_інфармацыя(стан_значэнне, 등록됨, аднавіць_стан=True)
            현재 = Сістэмная_інфармацыя.get('VMState')
            if 현재 == 'running':
                print('이미 выканаць_каманда 중입니다. 재빌드·재시작하지 않습니다.')
                return self.паказаць_стан()
            self.чэк_носьбіт(стан_значэнне, Сістэмная_інфармацыя)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 сховішча_значэнне 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Загад(['VBoxManage', 'controlvm', стан_значэнне['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Адкрыць 전에 기존 기록도 보관한다.
                    if стан_значэнне.get('serial_log'):
                        원본 = self.ШЛЯХ(стан_значэнне['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ШЛЯХ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Загад(['VBoxManage', 'startvm', стан_значэнне['uuid'], '--type', self.спосаб_рэжым])
                return self.паказаць_стан()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 пераход_рэжым 중입니다 ({}). 작업이 끝난 Назад_значэнне 다시 실행하세요.'.format(현재))
        elif стан_значэнне is not None and not стан_значэнне.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Назва in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # сховішча_значэнне/выканаць_каманда 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Загад(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        носьбіт_значэнне = 'media/kernel-' + кантрольная_сума(원본) + '.iso'
        прызначэнне_значэнне_a0fbc067 = self.ШЛЯХ(носьбіт_значэнне)
        прызначэнне_значэнне_a0fbc067.parent.mkdir(exist_ok=True)
        if прызначэнне_значэнне_a0fbc067.exists():
            if кантрольная_сума(прызначэнне_значэнне_a0fbc067) != кантрольная_сума(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(прызначэнне_значэнне_a0fbc067))
        else:
            with tempfile.NamedTemporaryFile(dir=str(прызначэнне_значэнне_a0fbc067.parent)) as Файл:
                shutil.copyfile(str(원본), Файл.name)
                os.link(Файл.name, str(прызначэнне_значэнне_a0fbc067))

        if стан_значэнне is None:
            стан_значэнне = {'version': 1, 'name': self.Назва, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.сховішча_значэнне(стан_значэнне)
        if Сістэмная_інфармацыя is None:
            self.Загад(['VBoxManage', 'createvm', '--name', стан_значэнне['name'], '--uuid', стан_значэнне['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ШЛЯХ('machines')), '--register'])
            self.Загад(['VBoxManage', 'setextradata', стан_значэнне['uuid'], 'JKOROS/Owner', стан_значэнне['owner']])
        # зборка_сістэма 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Сістэмная_інфармацыя = self.Сістэмная_інфармацыя(стан_значэнне, 등록목록(self.Загад(['VBoxManage', 'list', 'vms'])))
        if Сістэмная_інфармацыя.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('зборка_сістэма 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.чэк_носьбіт(стан_значэнне, Сістэмная_інфармацыя)
        стан_значэнне['iso'] = носьбіт_значэнне
        if носьбіт_значэнне not in стан_значэнне['media']: стан_значэнне['media'].append(носьбіт_значэнне)
        стан_значэнне['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        журнал_значэнне = self.ШЛЯХ(стан_значэнне['serial_log'])
        журнал_значэнне.parent.mkdir(exist_ok=True)
        self.сховішча_значэнне(стан_значэнне)
        self.Загад(['VBoxManage', 'modifyvm', стан_значэнне['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(журнал_значэнне)])
        제어기들 = [значэнне for Назва, значэнне in Сістэмная_інфармацыя.items() if re.fullmatch(r'storagecontrollername\d+', Назва)]
        if 'JKOROS IDE' not in 제어기들:
            self.Загад(['VBoxManage', 'storagectl', стан_значэнне['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Загад(['VBoxManage', 'storageattach', стан_значэнне['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(прызначэнне_значэнне_a0fbc067)])
        стан_значэнне['pending'] = False
        self.сховішча_значэнне(стан_значэнне)
        self.Загад(['VBoxManage', 'startvm', стан_значэнне['uuid'], '--type', self.спосаб_рэжым])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.паказаць_стан()


def Выканаць():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox выканаць_каманда 및 стан_значэнне запыт_значэнне')
    해석.add_argument('action', choices=['run', 'status'])
    параметр_аргумент = 해석.parse_args()
    выканаць_каманда = праграма_выклік_праграм(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметр_аргумент.action == 'status':
        print(json.dumps(выканаць_каманда.паказаць_стан(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. вузел 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/дазвол_значэнне 변경은 하지 않습니다.')
    os.umask(0o077)
    выканаць_каманда.ШЛЯХ('lock').parent.mkdir(parents=True, exist_ok=True)
    with выканаць_каманда.ШЛЯХ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox выканаць_каманда 작업이 진행 중입니다.')
        print(json.dumps(выканаць_каманда.выканаць_каманда(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Выканаць()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ПАМЫЛКА:
        print('VBOX ПАМЫЛКА: ' + str(ПАМЫЛКА), file=sys.stderr)
        sys.exit(1)
