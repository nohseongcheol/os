#!/usr/bin/env python3
"""jkoros 전용 VirtualBox програма_стартувач. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Изврши_обвивка_наредба(Аргументи):
    환경 = dict(os.environ, LC_ALL='C')
    мерка = subprocess.run([str(VALUE) for VALUE in Аргументи], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Содржина_VALUE = мерка.stdout.decode('utf-8', 'replace')
    if мерка.returncode:
        raise 실행오류('Команда неуспех_VALUE: ' + ' '.join(str(VALUE) for VALUE in Аргументи) + '\n' + Содржина_VALUE[-10000:])
    return Содржина_VALUE


def атрибут_VALUE(Содржина_VALUE):
    мерка = {}
    for ред in Содржина_VALUE.splitlines():
        if '=' not in ред:
            continue
        Име, VALUE = ред.split('=', 1)
        if Име.startswith('"'):
            Име = json.loads(Име)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_VALUE формат_VALUE ГРЕШКА: ' + ред)
        мерка[Име] = VALUE
    return мерка


def 등록목록(Содржина_VALUE):
    мерка = {}
    for ред in Содржина_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ред)
        if 일치: мерка[일치.group(2).lower()] = 일치.group(1)
    return мерка


def контролна_сума(ПАТЕКА):
    VALUE = hashlib.sha256()
    with ПАТЕКА.open('rb') as Датотека:
        for податоци in iter(lambda: Датотека.read(1024 * 1024), b''): VALUE.update(податоци)
    return VALUE.hexdigest()


class програма_стартувач:
    def __init__(self, корен_VALUE, Име, метод_MODE='gui', Команда=Изврши_обвивка_наредба):
        self.корен_VALUE = Path(корен_VALUE).resolve()
        self.Име, self.метод_MODE, self.Команда = Име, метод_MODE, Команда
        self.보관 = self.корен_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Име) or Име in ('.', '..'):
            raise 실행오류('VM 이름은 문자·цифра_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if метод_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ПАТЕКА(self, рамноправен_уред_VALUE):
        if Path(рамноправен_уред_VALUE).is_absolute() or '..' in Path(рамноправен_уред_VALUE).parts:
            raise 실행오류('잘못된 관리 ПАТЕКА: ' + str(рамноправен_уред_VALUE))
        мерка = self.보관
        for 부분 in ['.vbox'] + list(Path(рамноправен_уред_VALUE).parts):
            if 부분 == '.vbox': мерка = self.보관
            else: мерка = мерка / 부분
            if мерка.is_symlink(): raise 실행오류('Врзи_се 경로는 사용하지 않습니다: ' + str(мерка))
        return мерка

    def Читај(self):
        ПАТЕКА = self.ПАТЕКА('state.json')
        if not ПАТЕКА.exists(): return None
        статус_VALUE = json.loads(ПАТЕКА.read_text(encoding='utf-8'))
        if статус_VALUE.get('version') != 1 or статус_VALUE.get('name') != self.Име:
            raise 실행오류('관리 상태의 VM Име/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Име in ('uuid', 'owner'):
            if str(uuid.UUID(статус_VALUE[Име])) != статус_VALUE[Име]: raise 실행오류('잘못된 VM идентификатор_VALUE')
        return статус_VALUE

    def Store_VALUE(self, статус_VALUE):
        одредиште_VALUE = self.ПАТЕКА('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Датотека:
            json.dump(статус_VALUE, Датотека, ensure_ascii=False, indent=2)
            Датотека.write('\n')
            임시 = Датотека.name
        os.replace(임시, str(одредиште_VALUE))

    def msinfo32_exe(self, статус_VALUE, 등록됨, опоравува_статус=False):
        if статус_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = атрибут_VALUE(self.Команда(['VBoxManage', 'showvminfo', статус_VALUE['uuid'], '--machinereadable']))
        Позиција = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.ПАТЕКА('machines').resolve() not in Позиција.parents or msinfo32_exe.get('UUID') != статус_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Подесувања ПАТЕКА/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Команда(['VBoxManage', 'getextradata', статус_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + статус_VALUE['owner']:
            if опоравува_статус and статус_VALUE.get('pending') and 표식 == 'No value set!':
                self.Команда(['VBoxManage', 'setextradata', статус_VALUE['uuid'], 'JKOROS/Owner', статус_VALUE['owner']])
            else:
                raise 실행오류('VM сопственик_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, статус_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Име, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Име)]
        Дозволи_VALUE = [str(self.ПАТЕКА(VALUE)) for VALUE in статус_VALUE.get('media', [])]
        for Име, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(контролер) + r'-\d+-\d+', Име) for контролер in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Дозволи_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def прикажи_статус(self):
        статус_VALUE = self.Читај()
        if статус_VALUE is None: return {'name': self.Име, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(статус_VALUE, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', статус_VALUE['name']), 'uuid': статус_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.ПАТЕКА(статус_VALUE['iso'])) if статус_VALUE.get('iso') else None,
                'serial_log': str(self.ПАТЕКА(статус_VALUE['serial_log'])) if статус_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Изврши_наредба(self):
        статус_VALUE = self.Читај()
        등록됨 = 등록목록(self.Команда(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if статус_VALUE is not None and статус_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(статус_VALUE, 등록됨, опоравува_статус=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 Изврши_наредба 중입니다. 재빌드·재시작하지 않습니다.')
                return self.прикажи_статус()
            self.매체검사(статус_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Команда(['VBoxManage', 'controlvm', статус_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Отвори 전에 기존 기록도 보관한다.
                    if статус_VALUE.get('serial_log'):
                        원본 = self.ПАТЕКА(статус_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ПАТЕКА('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Команда(['VBoxManage', 'startvm', статус_VALUE['uuid'], '--type', self.метод_MODE])
                return self.прикажи_статус()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Назад_VALUE 다시 실행하세요.'.format(현재))
        elif статус_VALUE is not None and not статус_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Име in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Изврши_наредба 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Команда(['make', '-C', str(self.корен_VALUE / 'os'), 'iso']), end='')
        원본 = self.корен_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + контролна_сума(원본) + '.iso'
        одредиште_VALUE = self.ПАТЕКА(매체)
        одредиште_VALUE.parent.mkdir(exist_ok=True)
        if одредиште_VALUE.exists():
            if контролна_сума(одредиште_VALUE) != контролна_сума(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(одредиште_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(одредиште_VALUE.parent)) as Датотека:
                shutil.copyfile(str(원본), Датотека.name)
                os.link(Датотека.name, str(одредиште_VALUE))

        if статус_VALUE is None:
            статус_VALUE = {'version': 1, 'name': self.Име, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(статус_VALUE)
        if msinfo32_exe is None:
            self.Команда(['VBoxManage', 'createvm', '--name', статус_VALUE['name'], '--uuid', статус_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ПАТЕКА('machines')), '--register'])
            self.Команда(['VBoxManage', 'setextradata', статус_VALUE['uuid'], 'JKOROS/Owner', статус_VALUE['owner']])
        # верзија_систем 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(статус_VALUE, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('верзија_систем 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(статус_VALUE, msinfo32_exe)
        статус_VALUE['iso'] = 매체
        if 매체 not in статус_VALUE['media']: статус_VALUE['media'].append(매체)
        статус_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.ПАТЕКА(статус_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(статус_VALUE)
        self.Команда(['VBoxManage', 'modifyvm', статус_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Име, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Име)]
        if 'JKOROS IDE' not in 제어기들:
            self.Команда(['VBoxManage', 'storagectl', статус_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Команда(['VBoxManage', 'storageattach', статус_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(одредиште_VALUE)])
        статус_VALUE['pending'] = False
        self.Store_VALUE(статус_VALUE)
        self.Команда(['VBoxManage', 'startvm', статус_VALUE['uuid'], '--type', self.метод_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.прикажи_статус()


def Изврши_2():
    разложи_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Изврши_наредба 및 статус_VALUE прашалник_VALUE')
    разложи_VALUE.add_argument('action', choices=['run', 'status'])
    параметар_аргумент = разложи_VALUE.parse_args()
    Изврши_наредба = програма_стартувач(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметар_аргумент.action == 'status':
        print(json.dumps(Изврши_наредба.прикажи_статус(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. вдоми 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/дозвола_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Изврши_наредба.ПАТЕКА('lock').parent.mkdir(parents=True, exist_ok=True)
    with Изврши_наредба.ПАТЕКА('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Изврши_наредба 작업이 진행 중입니다.')
        print(json.dumps(Изврши_наредба.Изврши_наредба(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Изврши_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ГРЕШКА:
        print('VBOX ГРЕШКА: ' + str(ГРЕШКА), file=sys.stderr)
        sys.exit(1)
