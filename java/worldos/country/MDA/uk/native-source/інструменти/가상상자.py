#!/usr/bin/env python3
"""jkoros 전용 VirtualBox програма_запускач. 기존 VM/디스크/сховище_значення 상태는 삭제하지 않는다."""
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


def Виконати_оболонка_команда(аргументи):
    середовище = dict(os.environ, LC_ALL='C')
    результат = subprocess.run([str(значення) for значення in аргументи], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=середовище, timeout=180)
    Вміст_значення = результат.stdout.decode('utf-8', 'replace')
    if результат.returncode:
        raise 실행오류('команда неполадка_значення: ' + ' '.join(str(значення) for значення in аргументи) + '\n' + Вміст_значення[-10000:])
    return Вміст_значення


def атрибут_значення(Вміст_значення):
    результат = {}
    for рядок_введення in Вміст_значення.splitlines():
        if '=' not in рядок_введення:
            continue
        Назва, значення = рядок_введення.split('=', 1)
        if Назва.startswith('"'):
            Назва = json.loads(Назва)
        if значення.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(значення)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(значення): значення = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_значення формат_значення ПОМИЛКА: ' + рядок_введення)
        результат[Назва] = значення
    return результат


def 등록목록(Вміст_значення):
    результат = {}
    for рядок_введення in Вміст_значення.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', рядок_введення)
        if 일치: результат[일치.group(2).lower()] = 일치.group(1)
    return результат


def контрольна_сума(шлях):
    значення = hashlib.sha256()
    with шлях.open('rb') as файл:
        for дані in iter(lambda: файл.read(1024 * 1024), b''): значення.update(дані)
    return значення.hexdigest()


class програма_запускач:
    def __init__(self, корінь_значення, Назва, метод_режим='gui', команда=Виконати_оболонка_команда):
        self.корінь_значення = Path(корінь_значення).resolve()
        self.Назва, self.метод_режим, self.команда = Назва, метод_режим, команда
        self.보관 = self.корінь_значення / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Назва) or Назва in ('.', '..'):
            raise 실행오류('VM 이름은 문자·цифра_значення·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if метод_режим not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def шлях(self, точка_значення):
        if Path(точка_значення).is_absolute() or '..' in Path(точка_значення).parts:
            raise 실행오류('잘못된 관리 шлях: ' + str(точка_значення))
        результат = self.보관
        for 부분 in ['.vbox'] + list(Path(точка_значення).parts):
            if 부분 == '.vbox': результат = self.보관
            else: результат = результат / 부분
            if результат.is_symlink(): raise 실행오류('З_єднання 경로는 사용하지 않습니다: ' + str(результат))
        return результат

    def Читання(self):
        шлях = self.шлях('state.json')
        if not шлях.exists(): return None
        Стан_значення = json.loads(шлях.read_text(encoding='utf-8'))
        if Стан_значення.get('version') != 1 or Стан_значення.get('name') != self.Назва:
            raise 실행오류('관리 상태의 VM Назва/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Назва in ('uuid', 'owner'):
            if str(uuid.UUID(Стан_значення[Назва])) != Стан_значення[Назва]: raise 실행오류('잘못된 VM ідентифікатор_значення')
        return Стан_значення

    def сховище_значення(self, Стан_значення):
        місце_значення = self.шлях('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as файл:
            json.dump(Стан_значення, файл, ensure_ascii=False, indent=2)
            файл.write('\n')
            임시 = файл.name
        os.replace(임시, str(місце_значення))

    def Відомості_про_систему(self, Стан_значення, 등록됨, відновлювати_Стан=False):
        if Стан_значення['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Відомості_про_систему = атрибут_значення(self.команда(['VBoxManage', 'showvminfo', Стан_значення['uuid'], '--machinereadable']))
        позиція = Path(Відомості_про_систему.get('CfgFile', '')).resolve()
        if self.шлях('machines').resolve() not in позиція.parents or Відомості_про_систему.get('UUID') != Стан_значення['uuid']:
            raise 실행오류('이 프로젝트의 VM Налаштування шлях/UUID와 일치하지 않아 변경하지 않습니다.')
        маркер_значення_7e8f90bd = self.команда(['VBoxManage', 'getextradata', Стан_значення['uuid'], 'JKOROS/Owner']).strip()
        if маркер_значення_7e8f90bd != 'Value: ' + Стан_значення['owner']:
            if відновлювати_Стан and Стан_значення.get('pending') and маркер_значення_7e8f90bd == 'No value set!':
                self.команда(['VBoxManage', 'setextradata', Стан_значення['uuid'], 'JKOROS/Owner', Стан_значення['owner']])
            else:
                raise 실행오류('VM власник_значення 표식이 일치하지 않아 변경하지 않습니다.')
        return Відомості_про_систему

    def перевіряти_носії(self, Стан_значення, Відомості_про_систему):
        제어기들 = [значення for Назва, значення in Відомості_про_систему.items() if re.fullmatch(r'storagecontrollername\d+', Назва)]
        Дозволити_значення = [str(self.шлях(значення)) for значення in Стан_значення.get('media', [])]
        for Назва, значення in Відомості_про_систему.items():
            if any(re.fullmatch(re.escape(контролер) + r'-\d+-\d+', Назва) for контролер in 제어기들):
                if значення not in ('none', 'emptydrive') and значення not in Дозволити_значення:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + значення)

    def показувати_Стан(self):
        Стан_значення = self.Читання()
        if Стан_значення is None: return {'name': self.Назва, 'state': 'not-created'}
        Відомості_про_систему = self.Відомості_про_систему(Стан_значення, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        return {'name': Відомості_про_систему.get('name', Стан_значення['name']), 'uuid': Стан_значення['uuid'], 'state': Відомості_про_систему.get('VMState'),
                'iso': str(self.шлях(Стан_значення['iso'])) if Стан_значення.get('iso') else None,
                'serial_log': str(self.шлях(Стан_значення['serial_log'])) if Стан_значення.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Виконати_команда(self):
        Стан_значення = self.Читання()
        등록됨 = 등록목록(self.команда(['VBoxManage', 'list', 'vms']))
        Відомості_про_систему = None
        if Стан_значення is not None and Стан_значення['uuid'] in 등록됨:
            Відомості_про_систему = self.Відомості_про_систему(Стан_значення, 등록됨, відновлювати_Стан=True)
            чинний_елемент = Відомості_про_систему.get('VMState')
            if чинний_елемент == 'running':
                print('이미 Виконати_команда 중입니다. 재빌드·재시작하지 않습니다.')
                return self.показувати_Стан()
            self.перевіряти_носії(Стан_значення, Відомості_про_систему)
            if чинний_елемент in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 сховище_значення 상태를 버리지 않습니다.'.format(чинний_елемент))
                if чинний_елемент == 'paused':
                    self.команда(['VBoxManage', 'controlvm', Стан_значення['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 пробувати_знову_значення Відкрити 전에 기존 기록도 보관한다.
                    if Стан_значення.get('serial_log'):
                        원본 = self.шлях(Стан_значення['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.шлях('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.команда(['VBoxManage', 'startvm', Стан_значення['uuid'], '--type', self.метод_режим])
                return self.показувати_Стан()
            if чинний_елемент not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 перехід_режим 중입니다 ({}). 작업이 끝난 НАЗАД_значення пробувати_знову_значення 실행하세요.'.format(чинний_елемент))
        elif Стан_значення is not None and not Стан_значення.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 пробувати_знову_значення 등록하세요.')
        elif self.Назва in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # сховище_значення/Виконати_команда 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.команда(['make', '-C', str(self.корінь_значення / 'os'), 'iso']), end='')
        원본 = self.корінь_значення / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('запуск_машини ISO가 생성되지 않았습니다.')
        носії_значення = 'media/kernel-' + контрольна_сума(원본) + '.iso'
        місце_значення = self.шлях(носії_значення)
        місце_значення.parent.mkdir(exist_ok=True)
        if місце_значення.exists():
            if контрольна_сума(місце_значення) != контрольна_сума(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(місце_значення))
        else:
            with tempfile.NamedTemporaryFile(dir=str(місце_значення.parent)) as файл:
                shutil.copyfile(str(원본), файл.name)
                os.link(файл.name, str(місце_значення))

        if Стан_значення is None:
            Стан_значення = {'version': 1, 'name': self.Назва, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.сховище_значення(Стан_значення)
        if Відомості_про_систему is None:
            self.команда(['VBoxManage', 'createvm', '--name', Стан_значення['name'], '--uuid', Стан_значення['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.шлях('machines')), '--register'])
            self.команда(['VBoxManage', 'setextradata', Стан_значення['uuid'], 'JKOROS/Owner', Стан_значення['owner']])
        # збирання 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Відомості_про_систему = self.Відомості_про_систему(Стан_значення, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        if Відомості_про_систему.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('збирання 중 VM 상태가 바뀌었습니다. пробувати_знову_значення make vbox를 실행하세요.')
        self.перевіряти_носії(Стан_значення, Відомості_про_систему)
        Стан_значення['iso'] = носії_значення
        if носії_значення not in Стан_значення['media']: Стан_значення['media'].append(носії_значення)
        Стан_значення['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        журнал_значення = self.шлях(Стан_значення['serial_log'])
        журнал_значення.parent.mkdir(exist_ok=True)
        self.сховище_значення(Стан_значення)
        self.команда(['VBoxManage', 'modifyvm', Стан_значення['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(журнал_значення)])
        제어기들 = [значення for Назва, значення in Відомості_про_систему.items() if re.fullmatch(r'storagecontrollername\d+', Назва)]
        if 'JKOROS IDE' not in 제어기들:
            self.команда(['VBoxManage', 'storagectl', Стан_значення['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.команда(['VBoxManage', 'storageattach', Стан_значення['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(місце_значення)])
        Стан_значення['pending'] = False
        self.сховище_значення(Стан_значення)
        self.команда(['VBoxManage', 'startvm', Стан_значення['uuid'], '--type', self.метод_режим])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.показувати_Стан()


def запустити():
    аналізувати_значення = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Виконати_команда 및 Стан_значення запит_значення')
    аналізувати_значення.add_argument('action', choices=['run', 'status'])
    параметр_аргумент = аналізувати_значення.parse_args()
    Виконати_команда = програма_запускач(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметр_аргумент.action == 'status':
        print(json.dumps(Виконати_команда.показувати_Стан(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. хост 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/дозвіл_значення 변경은 하지 않습니다.')
    os.umask(0o077)
    Виконати_команда.шлях('lock').parent.mkdir(parents=True, exist_ok=True)
    with Виконати_команда.шлях('lock').open('a') as блокувати_значення:
        try: fcntl.flock(блокувати_значення, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Виконати_команда 작업이 진행 중입니다.')
        print(json.dumps(Виконати_команда.Виконати_команда(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: запустити()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ПОМИЛКА:
        print('VBOX ПОМИЛКА: ' + str(ПОМИЛКА), file=sys.stderr)
        sys.exit(1)
