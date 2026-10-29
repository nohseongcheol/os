#!/usr/bin/env python3
"""jkoros 전용 VirtualBox програм_покретач. 기존 VM/디스크/похранити_вриједност 상태는 삭제하지 않는다."""
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


def Изврши_љуска_команда(Аргументи):
    радно_окружење = dict(os.environ, LC_ALL='C')
    ИСХОД = subprocess.run([str(вриједност) for вриједност in Аргументи], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=радно_окружење, timeout=180)
    Садржај_вриједност = ИСХОД.stdout.decode('utf-8', 'replace')
    if ИСХОД.returncode:
        raise 실행오류('Наредба неуспјех_вриједност: ' + ' '.join(str(вриједност) for вриједност in Аргументи) + '\n' + Садржај_вриједност[-10000:])
    return Садржај_вриједност


def атрибут_вриједност(Садржај_вриједност):
    ИСХОД = {}
    for Ред in Садржај_вриједност.splitlines():
        if '=' not in Ред:
            continue
        Назив, вриједност = Ред.split('=', 1)
        if Назив.startswith('"'):
            Назив = json.loads(Назив)
        if вриједност.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(вриједност)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(вриједност): вриједност = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_вриједност формат_вриједност ГРЕШКА: ' + Ред)
        ИСХОД[Назив] = вриједност
    return ИСХОД


def 등록목록(Садржај_вриједност):
    ИСХОД = {}
    for Ред in Садржај_вриједност.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Ред)
        if 일치: ИСХОД[일치.group(2).lower()] = 일치.group(1)
    return ИСХОД


def контролни_збир(ПУТАЊА):
    вриједност = hashlib.sha256()
    with ПУТАЊА.open('rb') as Датотека:
        for подаци in iter(lambda: Датотека.read(1024 * 1024), b''): вриједност.update(подаци)
    return вриједност.hexdigest()


class програм_покретач:
    def __init__(self, корен_вриједност, Назив, метода_мод='gui', Наредба=Изврши_љуска_команда):
        self.корен_вриједност = Path(корен_вриједност).resolve()
        self.Назив, self.метода_мод, self.Наредба = Назив, метода_мод, Наредба
        self.보관 = self.корен_вриједност / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Назив) or Назив in ('.', '..'):
            raise 실행오류('VM 이름은 문자·цифра_вриједност·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if метода_мод not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ПУТАЊА(self, 상대):
        if Path(상대).is_absolute() or '..' in Path(상대).parts:
            raise 실행오류('잘못된 관리 ПУТАЊА: ' + str(상대))
        ИСХОД = self.보관
        for 부분 in ['.vbox'] + list(Path(상대).parts):
            if 부분 == '.vbox': ИСХОД = self.보관
            else: ИСХОД = ИСХОД / 부분
            if ИСХОД.is_symlink(): raise 실행오류('Повежи_се 경로는 사용하지 않습니다: ' + str(ИСХОД))
        return ИСХОД

    def Чита(self):
        ПУТАЊА = self.ПУТАЊА('state.json')
        if not ПУТАЊА.exists(): return None
        стање_вриједност = json.loads(ПУТАЊА.read_text(encoding='utf-8'))
        if стање_вриједност.get('version') != 1 or стање_вриједност.get('name') != self.Назив:
            raise 실행오류('관리 상태의 VM Назив/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Назив in ('uuid', 'owner'):
            if str(uuid.UUID(стање_вриједност[Назив])) != стање_вриједност[Назив]: raise 실행오류('잘못된 VM идентификатор_вриједност')
        return стање_вриједност

    def похранити_вриједност(self, стање_вриједност):
        одредиште_вриједност = self.ПУТАЊА('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Датотека:
            json.dump(стање_вриједност, Датотека, ensure_ascii=False, indent=2)
            Датотека.write('\n')
            임시 = Датотека.name
        os.replace(임시, str(одредиште_вриједност))

    def Информације_о_систему(self, стање_вриједност, 등록됨, опоравити_стање=False):
        if стање_вриједност['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Информације_о_систему = атрибут_вриједност(self.Наредба(['VBoxManage', 'showvminfo', стање_вриједност['uuid'], '--machinereadable']))
        Положај = Path(Информације_о_систему.get('CfgFile', '')).resolve()
        if self.ПУТАЊА('machines').resolve() not in Положај.parents or Информације_о_систему.get('UUID') != стање_вриједност['uuid']:
            raise 실행오류('이 프로젝트의 VM Поставке ПУТАЊА/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Наредба(['VBoxManage', 'getextradata', стање_вриједност['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + стање_вриједност['owner']:
            if опоравити_стање and стање_вриједност.get('pending') and 표식 == 'No value set!':
                self.Наредба(['VBoxManage', 'setextradata', стање_вриједност['uuid'], 'JKOROS/Owner', стање_вриједност['owner']])
            else:
                raise 실행오류('VM власник_вриједност 표식이 일치하지 않아 변경하지 않습니다.')
        return Информације_о_систему

    def 매체검사(self, стање_вриједност, Информације_о_систему):
        제어기들 = [вриједност for Назив, вриједност in Информације_о_систему.items() if re.fullmatch(r'storagecontrollername\d+', Назив)]
        Дозволи_вриједност = [str(self.ПУТАЊА(вриједност)) for вриједност in стање_вриједност.get('media', [])]
        for Назив, вриједност in Информације_о_систему.items():
            if any(re.fullmatch(re.escape(управљач) + r'-\d+-\d+', Назив) for управљач in 제어기들):
                if вриједност not in ('none', 'emptydrive') and вриједност not in Дозволи_вриједност:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + вриједност)

    def емисија_стање(self):
        стање_вриједност = self.Чита()
        if стање_вриједност is None: return {'name': self.Назив, 'state': 'not-created'}
        Информације_о_систему = self.Информације_о_систему(стање_вриједност, 등록목록(self.Наредба(['VBoxManage', 'list', 'vms'])))
        return {'name': Информације_о_систему.get('name', стање_вриједност['name']), 'uuid': стање_вриједност['uuid'], 'state': Информације_о_систему.get('VMState'),
                'iso': str(self.ПУТАЊА(стање_вриједност['iso'])) if стање_вриједност.get('iso') else None,
                'serial_log': str(self.ПУТАЊА(стање_вриједност['serial_log'])) if стање_вриједност.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Изврши_команда(self):
        стање_вриједност = self.Чита()
        등록됨 = 등록목록(self.Наредба(['VBoxManage', 'list', 'vms']))
        Информације_о_систему = None
        if стање_вриједност is not None and стање_вриједност['uuid'] in 등록됨:
            Информације_о_систему = self.Информације_о_систему(стање_вриједност, 등록됨, опоравити_стање=True)
            актуелно_ставка = Информације_о_систему.get('VMState')
            if актуелно_ставка == 'running':
                print('이미 Изврши_команда 중입니다. 재빌드·재시작하지 않습니다.')
                return self.емисија_стање()
            self.매체검사(стање_вриједност, Информације_о_систему)
            if актуелно_ставка in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 похранити_вриједност 상태를 버리지 않습니다.'.format(актуелно_ставка))
                if актуелно_ставка == 'paused':
                    self.Наредба(['VBoxManage', 'controlvm', стање_вриједност['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Отвори 전에 기존 기록도 보관한다.
                    if стање_вриједност.get('serial_log'):
                        원본 = self.ПУТАЊА(стање_вриједност['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ПУТАЊА('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Наредба(['VBoxManage', 'startvm', стање_вриједност['uuid'], '--type', self.метода_мод])
                return self.емисија_стање()
            if актуелно_ставка not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 пребацити_мод 중입니다 ({}). 작업이 끝난 НАЗАД_вриједност 다시 실행하세요.'.format(актуелно_ставка))
        elif стање_вриједност is not None and not стање_вриједност.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Назив in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # похранити_вриједност/Изврши_команда 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Наредба(['make', '-C', str(self.корен_вриједност / 'os'), 'iso']), end='')
        원본 = self.корен_вриједност / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + контролни_збир(원본) + '.iso'
        одредиште_вриједност = self.ПУТАЊА(매체)
        одредиште_вриједност.parent.mkdir(exist_ok=True)
        if одредиште_вриједност.exists():
            if контролни_збир(одредиште_вриједност) != контролни_збир(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(одредиште_вриједност))
        else:
            with tempfile.NamedTemporaryFile(dir=str(одредиште_вриједност.parent)) as Датотека:
                shutil.copyfile(str(원본), Датотека.name)
                os.link(Датотека.name, str(одредиште_вриједност))

        if стање_вриједност is None:
            стање_вриједност = {'version': 1, 'name': self.Назив, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.похранити_вриједност(стање_вриједност)
        if Информације_о_систему is None:
            self.Наредба(['VBoxManage', 'createvm', '--name', стање_вриједност['name'], '--uuid', стање_вриједност['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ПУТАЊА('machines')), '--register'])
            self.Наредба(['VBoxManage', 'setextradata', стање_вриједност['uuid'], 'JKOROS/Owner', стање_вриједност['owner']])
        # градити_систем 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Информације_о_систему = self.Информације_о_систему(стање_вриједност, 등록목록(self.Наредба(['VBoxManage', 'list', 'vms'])))
        if Информације_о_систему.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('градити_систем 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(стање_вриједност, Информације_о_систему)
        стање_вриједност['iso'] = 매체
        if 매체 not in стање_вриједност['media']: стање_вриједност['media'].append(매체)
        стање_вриједност['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        евиденција_вриједност = self.ПУТАЊА(стање_вриједност['serial_log'])
        евиденција_вриједност.parent.mkdir(exist_ok=True)
        self.похранити_вриједност(стање_вриједност)
        self.Наредба(['VBoxManage', 'modifyvm', стање_вриједност['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(евиденција_вриједност)])
        제어기들 = [вриједност for Назив, вриједност in Информације_о_систему.items() if re.fullmatch(r'storagecontrollername\d+', Назив)]
        if 'JKOROS IDE' not in 제어기들:
            self.Наредба(['VBoxManage', 'storagectl', стање_вриједност['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Наредба(['VBoxManage', 'storageattach', стање_вриједност['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(одредиште_вриједност)])
        стање_вриједност['pending'] = False
        self.похранити_вриједност(стање_вриједност)
        self.Наредба(['VBoxManage', 'startvm', стање_вриједност['uuid'], '--type', self.метода_мод])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.емисија_стање()


def Покрени():
    рашчланити_вриједност = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Изврши_команда 및 стање_вриједност упит_вриједност')
    рашчланити_вриједност.add_argument('action', choices=['run', 'status'])
    параметар_аргумент = рашчланити_вриједност.parse_args()
    Изврши_команда = програм_покретач(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметар_аргумент.action == 'status':
        print(json.dumps(Изврши_команда.емисија_стање(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. хост 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/дозвола_вриједност 변경은 하지 않습니다.')
    os.umask(0o077)
    Изврши_команда.ПУТАЊА('lock').parent.mkdir(parents=True, exist_ok=True)
    with Изврши_команда.ПУТАЊА('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Изврши_команда 작업이 진행 중입니다.')
        print(json.dumps(Изврши_команда.Изврши_команда(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Покрени()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ГРЕШКА:
        print('VBOX ГРЕШКА: ' + str(ГРЕШКА), file=sys.stderr)
        sys.exit(1)
