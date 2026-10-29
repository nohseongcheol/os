#!/usr/bin/env python3
"""jkoros 전용 VirtualBox програма_програма_за_стартиране. 기존 VM/디스크/хранилище_стойност 상태는 삭제하지 않는다."""
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


def изпълнявам_обвивка_команда(Параметри):
    환경 = dict(os.environ, LC_ALL='C')
    РЕЗУЛТАТ = subprocess.run([str(стойност) for стойност in Параметри], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Съдържание_стойност = РЕЗУЛТАТ.stdout.decode('utf-8', 'replace')
    if РЕЗУЛТАТ.returncode:
        raise 실행오류('Команда отказ_стойност: ' + ' '.join(str(стойност) for стойност in Параметри) + '\n' + Съдържание_стойност[-10000:])
    return Съдържание_стойност


def атрибут_стойност(Съдържание_стойност):
    РЕЗУЛТАТ = {}
    for ред in Съдържание_стойност.splitlines():
        if '=' not in ред:
            continue
        Име, стойност = ред.split('=', 1)
        if Име.startswith('"'):
            Име = json.loads(Име)
        if стойност.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(стойност)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(стойност): стойност = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_стойност формат_стойност ГРЕШКА: ' + ред)
        РЕЗУЛТАТ[Име] = стойност
    return РЕЗУЛТАТ


def 등록목록(Съдържание_стойност):
    РЕЗУЛТАТ = {}
    for ред in Съдържание_стойност.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ред)
        if 일치: РЕЗУЛТАТ[일치.group(2).lower()] = 일치.group(1)
    return РЕЗУЛТАТ


def контролна_сума(ПЪТ):
    стойност = hashlib.sha256()
    with ПЪТ.open('rb') as Файл:
        for данни in iter(lambda: Файл.read(1024 * 1024), b''): стойност.update(данни)
    return стойност.hexdigest()


class програма_програма_за_стартиране:
    def __init__(self, корен_стойност, Име, метод_режим='gui', Команда=изпълнявам_обвивка_команда):
        self.корен_стойност = Path(корен_стойност).resolve()
        self.Име, self.метод_режим, self.Команда = Име, метод_режим, Команда
        self.보관 = self.корен_стойност / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Име) or Име in ('.', '..'):
            raise 실행오류('VM 이름은 문자·цифра_стойност·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if метод_режим not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ПЪТ(self, крайно_устройство_стойност):
        if Path(крайно_устройство_стойност).is_absolute() or '..' in Path(крайно_устройство_стойност).parts:
            raise 실행오류('잘못된 관리 ПЪТ: ' + str(крайно_устройство_стойност))
        РЕЗУЛТАТ = self.보관
        for 부분 in ['.vbox'] + list(Path(крайно_устройство_стойност).parts):
            if 부분 == '.vbox': РЕЗУЛТАТ = self.보관
            else: РЕЗУЛТАТ = РЕЗУЛТАТ / 부분
            if РЕЗУЛТАТ.is_symlink(): raise 실행오류('Свързване 경로는 사용하지 않습니다: ' + str(РЕЗУЛТАТ))
        return РЕЗУЛТАТ

    def Четене(self):
        ПЪТ = self.ПЪТ('state.json')
        if not ПЪТ.exists(): return None
        Състояние_стойност = json.loads(ПЪТ.read_text(encoding='utf-8'))
        if Състояние_стойност.get('version') != 1 or Състояние_стойност.get('name') != self.Име:
            raise 실행오류('관리 상태의 VM Име/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Име in ('uuid', 'owner'):
            if str(uuid.UUID(Състояние_стойност[Име])) != Състояние_стойност[Име]: raise 실행오류('잘못된 VM Идентификатор_стойност')
        return Състояние_стойност

    def хранилище_стойност(self, Състояние_стойност):
        местоназначение_стойност = self.ПЪТ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Файл:
            json.dump(Състояние_стойност, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
            임시 = Файл.name
        os.replace(임시, str(местоназначение_стойност))

    def Системна_информация(self, Състояние_стойност, 등록됨, възстановявам_Състояние=False):
        if Състояние_стойност['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Системна_информация = атрибут_стойност(self.Команда(['VBoxManage', 'showvminfo', Състояние_стойност['uuid'], '--machinereadable']))
        Позиция = Path(Системна_информация.get('CfgFile', '')).resolve()
        if self.ПЪТ('machines').resolve() not in Позиция.parents or Системна_информация.get('UUID') != Състояние_стойност['uuid']:
            raise 실행오류('이 프로젝트의 VM Настройки ПЪТ/UUID와 일치하지 않아 변경하지 않습니다.')
        маркер_стойност = self.Команда(['VBoxManage', 'getextradata', Състояние_стойност['uuid'], 'JKOROS/Owner']).strip()
        if маркер_стойност != 'Value: ' + Състояние_стойност['owner']:
            if възстановявам_Състояние and Състояние_стойност.get('pending') and маркер_стойност == 'No value set!':
                self.Команда(['VBoxManage', 'setextradata', Състояние_стойност['uuid'], 'JKOROS/Owner', Състояние_стойност['owner']])
            else:
                raise 실행오류('VM собственик_стойност 표식이 일치하지 않아 변경하지 않습니다.')
        return Системна_информация

    def 매체검사(self, Състояние_стойност, Системна_информация):
        제어기들 = [стойност for Име, стойност in Системна_информация.items() if re.fullmatch(r'storagecontrollername\d+', Име)]
        позволявам_стойност = [str(self.ПЪТ(стойност)) for стойност in Състояние_стойност.get('media', [])]
        for Име, стойност in Системна_информация.items():
            if any(re.fullmatch(re.escape(контролер) + r'-\d+-\d+', Име) for контролер in 제어기들):
                if стойност not in ('none', 'emptydrive') and стойност not in позволявам_стойност:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + стойност)

    def показвам_Състояние(self):
        Състояние_стойност = self.Четене()
        if Състояние_стойност is None: return {'name': self.Име, 'state': 'not-created'}
        Системна_информация = self.Системна_информация(Състояние_стойност, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        return {'name': Системна_информация.get('name', Състояние_стойност['name']), 'uuid': Състояние_стойност['uuid'], 'state': Системна_информация.get('VMState'),
                'iso': str(self.ПЪТ(Състояние_стойност['iso'])) if Състояние_стойност.get('iso') else None,
                'serial_log': str(self.ПЪТ(Състояние_стойност['serial_log'])) if Състояние_стойност.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def изпълнявам_команда(self):
        Състояние_стойност = self.Четене()
        등록됨 = 등록목록(self.Команда(['VBoxManage', 'list', 'vms']))
        Системна_информация = None
        if Състояние_стойност is not None and Състояние_стойност['uuid'] in 등록됨:
            Системна_информация = self.Системна_информация(Състояние_стойност, 등록됨, възстановявам_Състояние=True)
            в_срок_артикул = Системна_информация.get('VMState')
            if в_срок_артикул == 'running':
                print('이미 изпълнявам_команда 중입니다. 재빌드·재시작하지 않습니다.')
                return self.показвам_Състояние()
            self.매체검사(Състояние_стойност, Системна_информация)
            if в_срок_артикул in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 хранилище_стойност 상태를 버리지 않습니다.'.format(в_срок_артикул))
                if в_срок_артикул == 'paused':
                    self.Команда(['VBoxManage', 'controlvm', Състояние_стойност['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 опитвам_повторно_стойност Отваряне 전에 기존 기록도 보관한다.
                    if Състояние_стойност.get('serial_log'):
                        원본 = self.ПЪТ(Състояние_стойност['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ПЪТ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Команда(['VBoxManage', 'startvm', Състояние_стойност['uuid'], '--type', self.метод_режим])
                return self.показвам_Състояние()
            if в_срок_артикул not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 комутатор_режим 중입니다 ({}). 작업이 끝난 НАЗАД_стойност опитвам_повторно_стойност 실행하세요.'.format(в_срок_артикул))
        elif Състояние_стойност is not None and not Състояние_стойност.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 опитвам_повторно_стойност 등록하세요.')
        elif self.Име in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # хранилище_стойност/изпълнявам_команда 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Команда(['make', '-C', str(self.корен_стойност / 'os'), 'iso']), end='')
        원본 = self.корен_стойност / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + контролна_сума(원본) + '.iso'
        местоназначение_стойност = self.ПЪТ(매체)
        местоназначение_стойност.parent.mkdir(exist_ok=True)
        if местоназначение_стойност.exists():
            if контролна_сума(местоназначение_стойност) != контролна_сума(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(местоназначение_стойност))
        else:
            with tempfile.NamedTemporaryFile(dir=str(местоназначение_стойност.parent)) as Файл:
                shutil.copyfile(str(원본), Файл.name)
                os.link(Файл.name, str(местоназначение_стойност))

        if Състояние_стойност is None:
            Състояние_стойност = {'version': 1, 'name': self.Име, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.хранилище_стойност(Състояние_стойност)
        if Системна_информация is None:
            self.Команда(['VBoxManage', 'createvm', '--name', Състояние_стойност['name'], '--uuid', Състояние_стойност['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ПЪТ('machines')), '--register'])
            self.Команда(['VBoxManage', 'setextradata', Състояние_стойност['uuid'], 'JKOROS/Owner', Състояние_стойност['owner']])
        # компилация_система 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Системна_информация = self.Системна_информация(Състояние_стойност, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        if Системна_информация.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('компилация_система 중 VM 상태가 바뀌었습니다. опитвам_повторно_стойност make vbox를 실행하세요.')
        self.매체검사(Състояние_стойност, Системна_информация)
        Състояние_стойност['iso'] = 매체
        if 매체 not in Състояние_стойност['media']: Състояние_стойност['media'].append(매체)
        Състояние_стойност['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        регистрирам_стойност = self.ПЪТ(Състояние_стойност['serial_log'])
        регистрирам_стойност.parent.mkdir(exist_ok=True)
        self.хранилище_стойност(Състояние_стойност)
        self.Команда(['VBoxManage', 'modifyvm', Състояние_стойност['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(регистрирам_стойност)])
        제어기들 = [стойност for Име, стойност in Системна_информация.items() if re.fullmatch(r'storagecontrollername\d+', Име)]
        if 'JKOROS IDE' not in 제어기들:
            self.Команда(['VBoxManage', 'storagectl', Състояние_стойност['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Команда(['VBoxManage', 'storageattach', Състояние_стойност['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(местоназначение_стойност)])
        Състояние_стойност['pending'] = False
        self.хранилище_стойност(Състояние_стойност)
        self.Команда(['VBoxManage', 'startvm', Състояние_стойност['uuid'], '--type', self.метод_режим])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.показвам_Състояние()


def Стартиране():
    анализирам_стойност = argparse.ArgumentParser(description='jkoros 전용 VirtualBox изпълнявам_команда 및 Състояние_стойност заявка_стойност')
    анализирам_стойност.add_argument('action', choices=['run', 'status'])
    параметър_аргумент = анализирам_стойност.parse_args()
    изпълнявам_команда = програма_програма_за_стартиране(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметър_аргумент.action == 'status':
        print(json.dumps(изпълнявам_команда.показвам_Състояние(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. хост 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/разрешение_стойност 변경은 하지 않습니다.')
    os.umask(0o077)
    изпълнявам_команда.ПЪТ('lock').parent.mkdir(parents=True, exist_ok=True)
    with изпълнявам_команда.ПЪТ('lock').open('a') as заключване_стойност:
        try: fcntl.flock(заключване_стойност, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox изпълнявам_команда 작업이 진행 중입니다.')
        print(json.dumps(изпълнявам_команда.изпълнявам_команда(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Стартиране()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ГРЕШКА:
        print('VBOX ГРЕШКА: ' + str(ГРЕШКА), file=sys.stderr)
        sys.exit(1)
