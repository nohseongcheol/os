#!/usr/bin/env python3
"""jkoros 전용 VirtualBox программа_Launcher. 기존 VM/디스크/Store_ЗНАЧЕН 상태는 삭제하지 않는다."""
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


class выполнение_ошибка(RuntimeError):
    pass


def 명령실행(аргументы):
    среда = dict(os.environ, LC_ALL='C')
    результат = subprocess.run([str(ЗНАЧЕН) for ЗНАЧЕН in аргументы], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=среда, timeout=180)
    контент_ЗНАЧЕН = результат.stdout.decode('utf-8', 'replace')
    if результат.returncode:
        raise выполнение_ошибка('команда сбой_ЗНАЧЕН: ' + ' '.join(str(ЗНАЧЕН) for ЗНАЧЕН in аргументы) + '\n' + контент_ЗНАЧЕН[-10000:])
    return контент_ЗНАЧЕН


def значение_атрибута(контент_ЗНАЧЕН):
    результат = {}
    for строка_ввода in контент_ЗНАЧЕН.splitlines():
        if '=' not in строка_ввода:
            continue
        Название, ЗНАЧЕН = строка_ввода.split('=', 1)
        if Название.startswith('"'):
            Название = json.loads(Название)
        if ЗНАЧЕН.startswith('"'):
            try:
                чтение_ЗНАЧЕН, 끝 = json.JSONDecoder().raw_decode(ЗНАЧЕН)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ЗНАЧЕН): ЗНАЧЕН = чтение_ЗНАЧЕН
            except ValueError:
                raise выполнение_ошибка('VirtualBox значение_атрибута формат_ЗНАЧЕН ошибка: ' + строка_ввода)
        результат[Название] = ЗНАЧЕН
    return результат


def 등록목록(контент_ЗНАЧЕН):
    результат = {}
    for строка_ввода in контент_ЗНАЧЕН.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', строка_ввода)
        if 일치: результат[일치.group(2).lower()] = 일치.group(1)
    return результат


def контрольная_сумма(путь):
    ЗНАЧЕН = hashlib.sha256()
    with путь.open('rb') as файл:
        for данные in iter(lambda: файл.read(1024 * 1024), b''): ЗНАЧЕН.update(данные)
    return ЗНАЧЕН.hexdigest()


class программа_Launcher:
    def __init__(self, корень_ЗНАЧЕН, Название, метод_МОДА='gui', команда=명령실행):
        self.корень_ЗНАЧЕН = Path(корень_ЗНАЧЕН).resolve()
        self.Название, self.метод_МОДА, self.команда = Название, метод_МОДА, команда
        self.보관 = self.корень_ЗНАЧЕН / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Название) or Название in ('.', '..'):
            raise выполнение_ошибка('VM 이름은 문자·цифра_ЗНАЧЕН·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if метод_МОДА not in ('gui', 'headless'): raise выполнение_ошибка('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def путь(self, одноранговый_ЗНАЧЕН):
        if Path(одноранговый_ЗНАЧЕН).is_absolute() or '..' in Path(одноранговый_ЗНАЧЕН).parts:
            raise выполнение_ошибка('잘못된 관리 путь: ' + str(одноранговый_ЗНАЧЕН))
        результат = self.보관
        for 부분 in ['.vbox'] + list(Path(одноранговый_ЗНАЧЕН).parts):
            if 부분 == '.vbox': результат = self.보관
            else: результат = результат / 부분
            if результат.is_symlink(): raise выполнение_ошибка('Подключить 경로는 사용하지 않습니다: ' + str(результат))
        return результат

    def Чтение(self):
        путь = self.путь('state.json')
        if not путь.exists(): return None
        Состояние_ЗНАЧЕН = json.loads(путь.read_text(encoding='utf-8'))
        if Состояние_ЗНАЧЕН.get('version') != 1 or Состояние_ЗНАЧЕН.get('name') != self.Название:
            raise выполнение_ошибка('관리 상태의 VM Название/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Название in ('uuid', 'owner'):
            if str(uuid.UUID(Состояние_ЗНАЧЕН[Название])) != Состояние_ЗНАЧЕН[Название]: raise выполнение_ошибка('잘못된 VM идентификатор_ЗНАЧЕН')
        return Состояние_ЗНАЧЕН

    def Store_ЗНАЧЕН(self, Состояние_ЗНАЧЕН):
        цель_ЗНАЧЕН = self.путь('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as файл:
            json.dump(Состояние_ЗНАЧЕН, файл, ensure_ascii=False, indent=2)
            файл.write('\n')
            임시 = файл.name
        os.replace(임시, str(цель_ЗНАЧЕН))

    def msinfo32_exe(self, Состояние_ЗНАЧЕН, 등록됨, восстановить_Состояние=False):
        if Состояние_ЗНАЧЕН['uuid'] not in 등록됨:
            raise выполнение_ошибка('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = значение_атрибута(self.команда(['VBoxManage', 'showvminfo', Состояние_ЗНАЧЕН['uuid'], '--machinereadable']))
        позиция = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.путь('machines').resolve() not in позиция.parents or msinfo32_exe.get('UUID') != Состояние_ЗНАЧЕН['uuid']:
            raise выполнение_ошибка('이 프로젝트의 VM Настройки путь/UUID와 일치하지 않아 변경하지 않습니다.')
        метка_ЗНАЧЕН = self.команда(['VBoxManage', 'getextradata', Состояние_ЗНАЧЕН['uuid'], 'JKOROS/Owner']).strip()
        if метка_ЗНАЧЕН != 'Value: ' + Состояние_ЗНАЧЕН['owner']:
            if восстановить_Состояние and Состояние_ЗНАЧЕН.get('pending') and метка_ЗНАЧЕН == 'No value set!':
                self.команда(['VBoxManage', 'setextradata', Состояние_ЗНАЧЕН['uuid'], 'JKOROS/Owner', Состояние_ЗНАЧЕН['owner']])
            else:
                raise выполнение_ошибка('VM владелец_ЗНАЧЕН 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def чек_носители(self, Состояние_ЗНАЧЕН, msinfo32_exe):
        제어기들 = [ЗНАЧЕН for Название, ЗНАЧЕН in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Название)]
        разрешить_ЗНАЧЕН = [str(self.путь(ЗНАЧЕН)) for ЗНАЧЕН in Состояние_ЗНАЧЕН.get('media', [])]
        for Название, ЗНАЧЕН in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(геймпад) + r'-\d+-\d+', Название) for геймпад in 제어기들):
                if ЗНАЧЕН not in ('none', 'emptydrive') and ЗНАЧЕН not in разрешить_ЗНАЧЕН:
                    raise выполнение_ошибка('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ЗНАЧЕН)

    def выпуск_Состояние(self):
        Состояние_ЗНАЧЕН = self.Чтение()
        if Состояние_ЗНАЧЕН is None: return {'name': self.Название, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Состояние_ЗНАЧЕН, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Состояние_ЗНАЧЕН['name']), 'uuid': Состояние_ЗНАЧЕН['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.путь(Состояние_ЗНАЧЕН['iso'])) if Состояние_ЗНАЧЕН.get('iso') else None,
                'serial_log': str(self.путь(Состояние_ЗНАЧЕН['serial_log'])) if Состояние_ЗНАЧЕН.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        Состояние_ЗНАЧЕН = self.Чтение()
        등록됨 = 등록목록(self.команда(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Состояние_ЗНАЧЕН is not None and Состояние_ЗНАЧЕН['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Состояние_ЗНАЧЕН, 등록됨, восстановить_Состояние=True)
            текущий_товар = msinfo32_exe.get('VMState')
            if текущий_товар == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.выпуск_Состояние()
            self.чек_носители(Состояние_ЗНАЧЕН, msinfo32_exe)
            if текущий_товар in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_ЗНАЧЕН 상태를 버리지 않습니다.'.format(текущий_товар))
                if текущий_товар == 'paused':
                    self.команда(['VBoxManage', 'controlvm', Состояние_ЗНАЧЕН['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 повторить_попытку_ЗНАЧЕН Открыть 전에 기존 기록도 보관한다.
                    if Состояние_ЗНАЧЕН.get('serial_log'):
                        원본 = self.путь(Состояние_ЗНАЧЕН['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.путь('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.команда(['VBoxManage', 'startvm', Состояние_ЗНАЧЕН['uuid'], '--type', self.метод_МОДА])
                return self.выпуск_Состояние()
            if текущий_товар not in ('poweroff', 'aborted'):
                raise выполнение_ошибка('VM이 перейти_МОДА 중입니다 ({}). 작업이 끝난 BACK_ЗНАЧЕН повторить_попытку_ЗНАЧЕН 실행하세요.'.format(текущий_товар))
        elif Состояние_ЗНАЧЕН is not None and not Состояние_ЗНАЧЕН.get('pending'):
            raise выполнение_ошибка('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 повторить_попытку_ЗНАЧЕН 등록하세요.')
        elif self.Название in 등록됨.values():
            raise выполнение_ошибка('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_ЗНАЧЕН/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.команда(['make', '-C', str(self.корень_ЗНАЧЕН / 'os'), 'iso']), end='')
        원본 = self.корень_ЗНАЧЕН / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise выполнение_ошибка('запуск_машины ISO가 생성되지 않았습니다.')
        носители_ЗНАЧЕН = 'media/kernel-' + контрольная_сумма(원본) + '.iso'
        цель_ЗНАЧЕН = self.путь(носители_ЗНАЧЕН)
        цель_ЗНАЧЕН.parent.mkdir(exist_ok=True)
        if цель_ЗНАЧЕН.exists():
            if контрольная_сумма(цель_ЗНАЧЕН) != контрольная_сумма(원본): raise выполнение_ошибка('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(цель_ЗНАЧЕН))
        else:
            with tempfile.NamedTemporaryFile(dir=str(цель_ЗНАЧЕН.parent)) as файл:
                shutil.copyfile(str(원본), файл.name)
                os.link(файл.name, str(цель_ЗНАЧЕН))

        if Состояние_ЗНАЧЕН is None:
            Состояние_ЗНАЧЕН = {'version': 1, 'name': self.Название, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_ЗНАЧЕН(Состояние_ЗНАЧЕН)
        if msinfo32_exe is None:
            self.команда(['VBoxManage', 'createvm', '--name', Состояние_ЗНАЧЕН['name'], '--uuid', Состояние_ЗНАЧЕН['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.путь('machines')), '--register'])
            self.команда(['VBoxManage', 'setextradata', Состояние_ЗНАЧЕН['uuid'], 'JKOROS/Owner', Состояние_ЗНАЧЕН['owner']])
        # сборка 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Состояние_ЗНАЧЕН, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise выполнение_ошибка('сборка 중 VM 상태가 바뀌었습니다. повторить_попытку_ЗНАЧЕН make vbox를 실행하세요.')
        self.чек_носители(Состояние_ЗНАЧЕН, msinfo32_exe)
        Состояние_ЗНАЧЕН['iso'] = носители_ЗНАЧЕН
        if носители_ЗНАЧЕН not in Состояние_ЗНАЧЕН['media']: Состояние_ЗНАЧЕН['media'].append(носители_ЗНАЧЕН)
        Состояние_ЗНАЧЕН['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_ЗНАЧЕН = self.путь(Состояние_ЗНАЧЕН['serial_log'])
        LOG_ЗНАЧЕН.parent.mkdir(exist_ok=True)
        self.Store_ЗНАЧЕН(Состояние_ЗНАЧЕН)
        self.команда(['VBoxManage', 'modifyvm', Состояние_ЗНАЧЕН['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_ЗНАЧЕН)])
        제어기들 = [ЗНАЧЕН for Название, ЗНАЧЕН in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Название)]
        if 'JKOROS IDE' not in 제어기들:
            self.команда(['VBoxManage', 'storagectl', Состояние_ЗНАЧЕН['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.команда(['VBoxManage', 'storageattach', Состояние_ЗНАЧЕН['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(цель_ЗНАЧЕН)])
        Состояние_ЗНАЧЕН['pending'] = False
        self.Store_ЗНАЧЕН(Состояние_ЗНАЧЕН)
        self.команда(['VBoxManage', 'startvm', Состояние_ЗНАЧЕН['uuid'], '--type', self.метод_МОДА])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.выпуск_Состояние()


def запустить():
    анализировать_ЗНАЧЕН = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 Состояние_ЗНАЧЕН запрос_ЗНАЧЕН')
    анализировать_ЗНАЧЕН.add_argument('action', choices=['run', 'status'])
    параметр_аргумент = анализировать_ЗНАЧЕН.parse_args()
    실행 = программа_Launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметр_аргумент.action == 'status':
        print(json.dumps(실행.выпуск_Состояние(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise выполнение_ошибка('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise выполнение_ошибка('/dev/vboxdrv에 접근할 수 없습니다. узел 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/Полномочие_ЗНАЧЕН 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.путь('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.путь('lock').open('a') as блокировка_ЗНАЧЕН:
        try: fcntl.flock(блокировка_ЗНАЧЕН, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise выполнение_ошибка('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: запустить()
    except (выполнение_ошибка, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ошибка:
        print('VBOX ошибка: ' + str(ошибка), file=sys.stderr)
        sys.exit(1)
