#!/usr/bin/env python3
"""jkoros 전용 VirtualBox програм_жаратма_тарткычы. 기존 VM/디스크/сактагыч_маани 상태는 삭제하지 않는다."""
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


def аткаруу_сырты_буйрук(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(маани) for маани in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Мазмун_маани = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Команда натыйжасыз_маани: ' + ' '.join(str(маани) for маани in 인수) + '\n' + Мазмун_маани[-10000:])
    return Мазмун_маани


def атрибут_маани(Мазмун_маани):
    결과 = {}
    for сап in Мазмун_маани.splitlines():
        if '=' not in сап:
            continue
        Аты, маани = сап.split('=', 1)
        if Аты.startswith('"'):
            Аты = json.loads(Аты)
        if маани.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(маани)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(маани): маани = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_маани формат_маани Ката: ' + сап)
        결과[Аты] = маани
    return 결과


def 등록목록(Мазмун_маани):
    결과 = {}
    for сап in Мазмун_маани.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', сап)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(ЖОЛ):
    маани = hashlib.sha256()
    with ЖОЛ.open('rb') as Файл:
        for берилмелер in iter(lambda: Файл.read(1024 * 1024), b''): маани.update(берилмелер)
    return маани.hexdigest()


class програм_жаратма_тарткычы:
    def __init__(self, 뿌리, Аты, ыкма_режим='gui', Команда=аткаруу_сырты_буйрук):
        self.뿌리 = Path(뿌리).resolve()
        self.Аты, self.ыкма_режим, self.Команда = Аты, ыкма_режим, Команда
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Аты) or Аты in ('.', '..'):
            raise 실행오류('VM 이름은 문자·санарип_маани·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ыкма_режим not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ЖОЛ(self, бирдей_маани):
        if Path(бирдей_маани).is_absolute() or '..' in Path(бирдей_маани).parts:
            raise 실행오류('잘못된 관리 ЖОЛ: ' + str(бирдей_маани))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(бирдей_маани).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Туташуу 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Окуу(self):
        ЖОЛ = self.ЖОЛ('state.json')
        if not ЖОЛ.exists(): return None
        абал_маани = json.loads(ЖОЛ.read_text(encoding='utf-8'))
        if абал_маани.get('version') != 1 or абал_маани.get('name') != self.Аты:
            raise 실행오류('관리 상태의 VM Аты/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Аты in ('uuid', 'owner'):
            if str(uuid.UUID(абал_маани[Аты])) != абал_маани[Аты]: raise 실행오류('잘못된 VM аныктагыч_маани')
        return абал_маани

    def сактагыч_маани(self, абал_маани):
        көздөө_жайы_маани = self.ЖОЛ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Файл:
            json.dump(абал_маани, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
            임시 = Файл.name
        os.replace(임시, str(көздөө_жайы_маани))

    def Система_маалыматы(self, абал_маани, 등록됨, калыбына_келтирүү_абал=False):
        if абал_маани['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Система_маалыматы = атрибут_маани(self.Команда(['VBoxManage', 'showvminfo', абал_маани['uuid'], '--machinereadable']))
        Турган_жери = Path(Система_маалыматы.get('CfgFile', '')).resolve()
        if self.ЖОЛ('machines').resolve() not in Турган_жери.parents or Система_маалыматы.get('UUID') != абал_маани['uuid']:
            raise 실행오류('이 프로젝트의 VM Орнотуулар ЖОЛ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Команда(['VBoxManage', 'getextradata', абал_маани['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + абал_маани['owner']:
            if калыбына_келтирүү_абал and абал_маани.get('pending') and 표식 == 'No value set!':
                self.Команда(['VBoxManage', 'setextradata', абал_маани['uuid'], 'JKOROS/Owner', абал_маани['owner']])
            else:
                raise 실행오류('VM ээ_кожоюн_кимдир_бирөөгө_таандык_болуу_маани 표식이 일치하지 않아 변경하지 않습니다.')
        return Система_маалыматы

    def 매체검사(self, абал_маани, Система_маалыматы):
        제어기들 = [маани for Аты, маани in Система_маалыматы.items() if re.fullmatch(r'storagecontrollername\d+', Аты)]
        Уруксат_берүү_маани = [str(self.ЖОЛ(маани)) for маани in абал_маани.get('media', [])]
        for Аты, маани in Система_маалыматы.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Аты) for 제어기 in 제어기들):
                if маани not in ('none', 'emptydrive') and маани not in Уруксат_берүү_маани:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + маани)

    def көрсөтүү_абал(self):
        абал_маани = self.Окуу()
        if абал_маани is None: return {'name': self.Аты, 'state': 'not-created'}
        Система_маалыматы = self.Система_маалыматы(абал_маани, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        return {'name': Система_маалыматы.get('name', абал_маани['name']), 'uuid': абал_маани['uuid'], 'state': Система_маалыматы.get('VMState'),
                'iso': str(self.ЖОЛ(абал_маани['iso'])) if абал_маани.get('iso') else None,
                'serial_log': str(self.ЖОЛ(абал_маани['serial_log'])) if абал_маани.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def аткаруу_буйрук(self):
        абал_маани = self.Окуу()
        등록됨 = 등록목록(self.Команда(['VBoxManage', 'list', 'vms']))
        Система_маалыматы = None
        if абал_маани is not None and абал_маани['uuid'] in 등록됨:
            Система_маалыматы = self.Система_маалыматы(абал_маани, 등록됨, калыбына_келтирүү_абал=True)
            현재 = Система_маалыматы.get('VMState')
            if 현재 == 'running':
                print('이미 аткаруу_буйрук 중입니다. 재빌드·재시작하지 않습니다.')
                return self.көрсөтүү_абал()
            self.매체검사(абал_маани, Система_маалыматы)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 сактагыч_маани 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Команда(['VBoxManage', 'controlvm', абал_маани['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Ачуу 전에 기존 기록도 보관한다.
                    if абал_маани.get('serial_log'):
                        원본 = self.ЖОЛ(абал_маани['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ЖОЛ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Команда(['VBoxManage', 'startvm', абал_маани['uuid'], '--type', self.ыкма_режим])
                return self.көрсөтүү_абал()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 котормо_режим 중입니다 ({}). 작업이 끝난 Артка_маани 다시 실행하세요.'.format(현재))
        elif абал_маани is not None and not абал_маани.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Аты in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # сактагыч_маани/аткаруу_буйрук 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Команда(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        көздөө_жайы_маани = self.ЖОЛ(매체)
        көздөө_жайы_маани.parent.mkdir(exist_ok=True)
        if көздөө_жайы_маани.exists():
            if 검사합(көздөө_жайы_маани) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(көздөө_жайы_маани))
        else:
            with tempfile.NamedTemporaryFile(dir=str(көздөө_жайы_маани.parent)) as Файл:
                shutil.copyfile(str(원본), Файл.name)
                os.link(Файл.name, str(көздөө_жайы_маани))

        if абал_маани is None:
            абал_маани = {'version': 1, 'name': self.Аты, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.сактагыч_маани(абал_маани)
        if Система_маалыматы is None:
            self.Команда(['VBoxManage', 'createvm', '--name', абал_маани['name'], '--uuid', абал_маани['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ЖОЛ('machines')), '--register'])
            self.Команда(['VBoxManage', 'setextradata', абал_маани['uuid'], 'JKOROS/Owner', абал_маани['owner']])
        # курам_тутум 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Система_маалыматы = self.Система_маалыматы(абал_маани, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        if Система_маалыматы.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('курам_тутум 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(абал_маани, Система_маалыматы)
        абал_маани['iso'] = 매체
        if 매체 not in абал_маани['media']: абал_маани['media'].append(매체)
        абал_маани['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        жазуу_маани = self.ЖОЛ(абал_маани['serial_log'])
        жазуу_маани.parent.mkdir(exist_ok=True)
        self.сактагыч_маани(абал_маани)
        self.Команда(['VBoxManage', 'modifyvm', абал_маани['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(жазуу_маани)])
        제어기들 = [маани for Аты, маани in Система_маалыматы.items() if re.fullmatch(r'storagecontrollername\d+', Аты)]
        if 'JKOROS IDE' not in 제어기들:
            self.Команда(['VBoxManage', 'storagectl', абал_маани['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Команда(['VBoxManage', 'storageattach', абал_маани['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(көздөө_жайы_маани)])
        абал_маани['pending'] = False
        self.сактагыч_маани(абал_маани)
        self.Команда(['VBoxManage', 'startvm', абал_маани['uuid'], '--type', self.ыкма_режим])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.көрсөтүү_абал()


def Жүргүзүү():
    талдоо_маани = argparse.ArgumentParser(description='jkoros 전용 VirtualBox аткаруу_буйрук 및 абал_маани сурам_маани')
    талдоо_маани.add_argument('action', choices=['run', 'status'])
    인자 = талдоо_маани.parse_args()
    аткаруу_буйрук = програм_жаратма_тарткычы(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(аткаруу_буйрук.көрсөтүү_абал(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. кабылдоо 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/уруксат_маани 변경은 하지 않습니다.')
    os.umask(0o077)
    аткаруу_буйрук.ЖОЛ('lock').parent.mkdir(parents=True, exist_ok=True)
    with аткаруу_буйрук.ЖОЛ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox аткаруу_буйрук 작업이 진행 중입니다.')
        print(json.dumps(аткаруу_буйрук.аткаруу_буйрук(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Жүргүзүү()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Ката:
        print('VBOX Ката: ' + str(Ката), file=sys.stderr)
        sys.exit(1)
