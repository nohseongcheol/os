#!/usr/bin/env python3
"""jkoros 전용 VirtualBox кушымта_хезмәткәр. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def үтәргә_тышча_команда(인수):
    환경 = dict(os.environ, LC_ALL='C')
    үлчәм = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Эчтәлек_VALUE = үлчәм.stdout.decode('utf-8', 'replace')
    if үлчәм.returncode:
        raise 실행오류('команда эштән_туктау_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Эчтәлек_VALUE[-10000:])
    return Эчтәлек_VALUE


def аергыч_VALUE_286d43f0(Эчтәлек_VALUE):
    үлчәм = {}
    for юл in Эчтәлек_VALUE.splitlines():
        if '=' not in юл:
            continue
        исем, VALUE = юл.split('=', 1)
        if исем.startswith('"'):
            исем = json.loads(исем)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox аергыч_VALUE_286d43f0 формат_VALUE Хата: ' + юл)
        үлчәм[исем] = VALUE
    return үлчәм


def 등록목록(Эчтәлек_VALUE):
    үлчәм = {}
    for юл in Эчтәлек_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', юл)
        if 일치: үлчәм[일치.group(2).lower()] = 일치.group(1)
    return үлчәм


def 검사합(Yul):
    VALUE = hashlib.sha256()
    with Yul.open('rb') as Birem:
        for мәгълүмат in iter(lambda: Birem.read(1024 * 1024), b''): VALUE.update(мәгълүмат)
    return VALUE.hexdigest()


class кушымта_хезмәткәр:
    def __init__(self, тамыр_VALUE, исем, ысул_MODE='gui', команда=үтәргә_тышча_команда):
        self.тамыр_VALUE = Path(тамыр_VALUE).resolve()
        self.исем, self.ысул_MODE, self.команда = исем, ысул_MODE, команда
        self.보관 = self.тамыр_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', исем) or исем in ('.', '..'):
            raise 실행오류('VM 이름은 문자·сан_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ысул_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Yul(self, тиңдәш_VALUE):
        if Path(тиңдәш_VALUE).is_absolute() or '..' in Path(тиңдәш_VALUE).parts:
            raise 실행오류('잘못된 관리 Yul: ' + str(тиңдәш_VALUE))
        үлчәм = self.보관
        for 부분 in ['.vbox'] + list(Path(тиңдәш_VALUE).parts):
            if 부분 == '.vbox': үлчәм = self.보관
            else: үлчәм = үлчәм / 부분
            if үлчәм.is_symlink(): raise 실행오류('ялгау 경로는 사용하지 않습니다: ' + str(үлчәм))
        return үлчәм

    def 읽기(self):
        Yul = self.Yul('state.json')
        if not Yul.exists(): return None
        халәт_VALUE = json.loads(Yul.read_text(encoding='utf-8'))
        if халәт_VALUE.get('version') != 1 or халәт_VALUE.get('name') != self.исем:
            raise 실행오류('관리 상태의 VM исем/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for исем in ('uuid', 'owner'):
            if str(uuid.UUID(халәт_VALUE[исем])) != халәт_VALUE[исем]: raise 실행오류('잘못된 VM күрсәткеч_VALUE')
        return халәт_VALUE

    def Store_VALUE(self, халәт_VALUE):
        күчерү_урыны_VALUE = self.Yul('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Birem:
            json.dump(халәт_VALUE, Birem, ensure_ascii=False, indent=2)
            Birem.write('\n')
            임시 = Birem.name
        os.replace(임시, str(күчерү_урыны_VALUE))

    def msinfo32_exe(self, халәт_VALUE, 등록됨, тергезү_халәт=False):
        if халәт_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = аергыч_VALUE_286d43f0(self.команда(['VBoxManage', 'showvminfo', халәт_VALUE['uuid'], '--machinereadable']))
        урнаштыру = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Yul('machines').resolve() not in урнаштыру.parents or msinfo32_exe.get('UUID') != халәт_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Caylaw Yul/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.команда(['VBoxManage', 'getextradata', халәт_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + халәт_VALUE['owner']:
            if тергезү_халәт and халәт_VALUE.get('pending') and 표식 == 'No value set!':
                self.команда(['VBoxManage', 'setextradata', халәт_VALUE['uuid'], 'JKOROS/Owner', халәт_VALUE['owner']])
            else:
                raise 실행오류('VM биләүче_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def чек_туплагыч(self, халәт_VALUE, msinfo32_exe):
        제어기들 = [VALUE for исем, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', исем)]
        Рөхсәт_VALUE = [str(self.Yul(VALUE)) for VALUE in халәт_VALUE.get('media', [])]
        for исем, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(контроллер) + r'-\d+-\d+', исем) for контроллер in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Рөхсәт_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def күрсәтү_халәт(self):
        халәт_VALUE = self.읽기()
        if халәт_VALUE is None: return {'name': self.исем, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(халәт_VALUE, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', халәт_VALUE['name']), 'uuid': халәт_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Yul(халәт_VALUE['iso'])) if халәт_VALUE.get('iso') else None,
                'serial_log': str(self.Yul(халәт_VALUE['serial_log'])) if халәт_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def үтәргә_команда(self):
        халәт_VALUE = self.읽기()
        등록됨 = 등록목록(self.команда(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if халәт_VALUE is not None and халәт_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(халәт_VALUE, 등록됨, тергезү_халәт=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 үтәргә_команда 중입니다. 재빌드·재시작하지 않습니다.')
                return self.күрсәтү_халәт()
            self.чек_туплагыч(халәт_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.команда(['VBoxManage', 'controlvm', халәт_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ачу 전에 기존 기록도 보관한다.
                    if халәт_VALUE.get('serial_log'):
                        원본 = self.Yul(халәт_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Yul('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.команда(['VBoxManage', 'startvm', халәт_VALUE['uuid'], '--type', self.ысул_MODE])
                return self.күрсәтү_халәт()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Артка_VALUE 다시 실행하세요.'.format(현재))
        elif халәт_VALUE is not None and not халәт_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.исем in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/үтәргә_команда 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.команда(['make', '-C', str(self.тамыр_VALUE / 'os'), 'iso']), end='')
        원본 = self.тамыр_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        туплагыч_VALUE = 'media/kernel-' + 검사합(원본) + '.iso'
        күчерү_урыны_VALUE = self.Yul(туплагыч_VALUE)
        күчерү_урыны_VALUE.parent.mkdir(exist_ok=True)
        if күчерү_урыны_VALUE.exists():
            if 검사합(күчерү_урыны_VALUE) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(күчерү_урыны_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(күчерү_урыны_VALUE.parent)) as Birem:
                shutil.copyfile(str(원본), Birem.name)
                os.link(Birem.name, str(күчерү_урыны_VALUE))

        if халәт_VALUE is None:
            халәт_VALUE = {'version': 1, 'name': self.исем, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(халәт_VALUE)
        if msinfo32_exe is None:
            self.команда(['VBoxManage', 'createvm', '--name', халәт_VALUE['name'], '--uuid', халәт_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Yul('machines')), '--register'])
            self.команда(['VBoxManage', 'setextradata', халәт_VALUE['uuid'], 'JKOROS/Owner', халәт_VALUE['owner']])
        # төзү_система 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(халәт_VALUE, 등록목록(self.команда(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('төзү_система 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.чек_туплагыч(халәт_VALUE, msinfo32_exe)
        халәт_VALUE['iso'] = туплагыч_VALUE
        if туплагыч_VALUE not in халәт_VALUE['media']: халәт_VALUE['media'].append(туплагыч_VALUE)
        халәт_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Yul(халәт_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(халәт_VALUE)
        self.команда(['VBoxManage', 'modifyvm', халәт_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for исем, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', исем)]
        if 'JKOROS IDE' not in 제어기들:
            self.команда(['VBoxManage', 'storagectl', халәт_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.команда(['VBoxManage', 'storageattach', халәт_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(күчерү_урыны_VALUE)])
        халәт_VALUE['pending'] = False
        self.Store_VALUE(халәт_VALUE)
        self.команда(['VBoxManage', 'startvm', халәт_VALUE['uuid'], '--type', self.ысул_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.күрсәтү_халәт()


def эшләтү():
    бүлү_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox үтәргә_команда 및 халәт_VALUE таләп_VALUE')
    бүлү_VALUE.add_argument('action', choices=['run', 'status'])
    인자 = бүлү_VALUE.parse_args()
    үтәргә_команда = кушымта_хезмәткәр(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(үтәргә_команда.күрсәтү_халәт(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. хост 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/рөхсәт_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    үтәргә_команда.Yul('lock').parent.mkdir(parents=True, exist_ok=True)
    with үтәргә_команда.Yul('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox үтәргә_команда 작업이 진행 중입니다.')
        print(json.dumps(үтәргә_команда.үтәргә_команда(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: эшләтү()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Хата:
        print('VBOX Хата: ' + str(Хата), file=sys.stderr)
        sys.exit(1)
