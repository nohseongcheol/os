#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_oopmaker. 기존 VM/디스크/bêre_VALUE 상태는 삭제하지 않는다."""
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


def uitvoer_dop_bevel(인수):
    환경 = dict(os.environ, LC_ALL='C')
    maatreël = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Inhoud_VALUE = maatreël.stdout.decode('utf-8', 'replace')
    if maatreël.returncode:
        raise 실행오류('Opdrag faling_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Inhoud_VALUE[-10000:])
    return Inhoud_VALUE


def kenmerk_VALUE(Inhoud_VALUE):
    maatreël = {}
    for lyn in Inhoud_VALUE.splitlines():
        if '=' not in lyn:
            continue
        Naam, VALUE = lyn.split('=', 1)
        if Naam.startswith('"'):
            Naam = json.loads(Naam)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox kenmerk_VALUE formaat_VALUE Fout: ' + lyn)
        maatreël[Naam] = VALUE
    return maatreël


def 등록목록(Inhoud_VALUE):
    maatreël = {}
    for lyn in Inhoud_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', lyn)
        if 일치: maatreël[일치.group(2).lower()] = 일치.group(1)
    return maatreël


def 검사합(Pad):
    VALUE = hashlib.sha256()
    with Pad.open('rb') as Lêer:
        for data in iter(lambda: Lêer.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class program_oopmaker:
    def __init__(self, wortel_VALUE, Naam, metode_MODE='gui', Opdrag=uitvoer_dop_bevel):
        self.wortel_VALUE = Path(wortel_VALUE).resolve()
        self.Naam, self.metode_MODE, self.Opdrag = Naam, metode_MODE, Opdrag
        self.보관 = self.wortel_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Naam) or Naam in ('.', '..'):
            raise 실행오류('VM 이름은 문자·syfer_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metode_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Pad(self, portuur_VALUE):
        if Path(portuur_VALUE).is_absolute() or '..' in Path(portuur_VALUE).parts:
            raise 실행오류('잘못된 관리 Pad: ' + str(portuur_VALUE))
        maatreël = self.보관
        for 부분 in ['.vbox'] + list(Path(portuur_VALUE).parts):
            if 부분 == '.vbox': maatreël = self.보관
            else: maatreël = maatreël / 부분
            if maatreël.is_symlink(): raise 실행오류('Koppel 경로는 사용하지 않습니다: ' + str(maatreël))
        return maatreël

    def Lees(self):
        Pad = self.Pad('state.json')
        if not Pad.exists(): return None
        stand_VALUE = json.loads(Pad.read_text(encoding='utf-8'))
        if stand_VALUE.get('version') != 1 or stand_VALUE.get('name') != self.Naam:
            raise 실행오류('관리 상태의 VM Naam/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Naam in ('uuid', 'owner'):
            if str(uuid.UUID(stand_VALUE[Naam])) != stand_VALUE[Naam]: raise 실행오류('잘못된 VM waarde_VALUE')
        return stand_VALUE

    def bêre_VALUE(self, stand_VALUE):
        bestemming_VALUE = self.Pad('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Lêer:
            json.dump(stand_VALUE, Lêer, ensure_ascii=False, indent=2)
            Lêer.write('\n')
            임시 = Lêer.name
        os.replace(임시, str(bestemming_VALUE))

    def Stelselinfo(self, stand_VALUE, 등록됨, herwin_stand=False):
        if stand_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Stelselinfo = kenmerk_VALUE(self.Opdrag(['VBoxManage', 'showvminfo', stand_VALUE['uuid'], '--machinereadable']))
        Posisie = Path(Stelselinfo.get('CfgFile', '')).resolve()
        if self.Pad('machines').resolve() not in Posisie.parents or Stelselinfo.get('UUID') != stand_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Instellings Pad/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Opdrag(['VBoxManage', 'getextradata', stand_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + stand_VALUE['owner']:
            if herwin_stand and stand_VALUE.get('pending') and 표식 == 'No value set!':
                self.Opdrag(['VBoxManage', 'setextradata', stand_VALUE['uuid'], 'JKOROS/Owner', stand_VALUE['owner']])
            else:
                raise 실행오류('VM eienaar_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return Stelselinfo

    def tjek_media(self, stand_VALUE, Stelselinfo):
        제어기들 = [VALUE for Naam, VALUE in Stelselinfo.items() if re.fullmatch(r'storagecontrollername\d+', Naam)]
        toelaat_VALUE = [str(self.Pad(VALUE)) for VALUE in stand_VALUE.get('media', [])]
        for Naam, VALUE in Stelselinfo.items():
            if any(re.fullmatch(re.escape(beheerder) + r'-\d+-\d+', Naam) for beheerder in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in toelaat_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def wys_stand(self):
        stand_VALUE = self.Lees()
        if stand_VALUE is None: return {'name': self.Naam, 'state': 'not-created'}
        Stelselinfo = self.Stelselinfo(stand_VALUE, 등록목록(self.Opdrag(['VBoxManage', 'list', 'vms'])))
        return {'name': Stelselinfo.get('name', stand_VALUE['name']), 'uuid': stand_VALUE['uuid'], 'state': Stelselinfo.get('VMState'),
                'iso': str(self.Pad(stand_VALUE['iso'])) if stand_VALUE.get('iso') else None,
                'serial_log': str(self.Pad(stand_VALUE['serial_log'])) if stand_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def uitvoer_bevel(self):
        stand_VALUE = self.Lees()
        등록됨 = 등록목록(self.Opdrag(['VBoxManage', 'list', 'vms']))
        Stelselinfo = None
        if stand_VALUE is not None and stand_VALUE['uuid'] in 등록됨:
            Stelselinfo = self.Stelselinfo(stand_VALUE, 등록됨, herwin_stand=True)
            현재 = Stelselinfo.get('VMState')
            if 현재 == 'running':
                print('이미 uitvoer_bevel 중입니다. 재빌드·재시작하지 않습니다.')
                return self.wys_stand()
            self.tjek_media(stand_VALUE, Stelselinfo)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 bêre_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Opdrag(['VBoxManage', 'controlvm', stand_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 skep 전에 기존 기록도 보관한다.
                    if stand_VALUE.get('serial_log'):
                        원본 = self.Pad(stand_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Pad('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Opdrag(['VBoxManage', 'startvm', stand_VALUE['uuid'], '--type', self.metode_MODE])
                return self.wys_stand()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 TERUG_VALUE 다시 실행하세요.'.format(현재))
        elif stand_VALUE is not None and not stand_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Naam in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # bêre_VALUE/uitvoer_bevel 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Opdrag(['make', '-C', str(self.wortel_VALUE / 'os'), 'iso']), end='')
        원본 = self.wortel_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        media_VALUE = 'media/kernel-' + 검사합(원본) + '.iso'
        bestemming_VALUE = self.Pad(media_VALUE)
        bestemming_VALUE.parent.mkdir(exist_ok=True)
        if bestemming_VALUE.exists():
            if 검사합(bestemming_VALUE) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(bestemming_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(bestemming_VALUE.parent)) as Lêer:
                shutil.copyfile(str(원본), Lêer.name)
                os.link(Lêer.name, str(bestemming_VALUE))

        if stand_VALUE is None:
            stand_VALUE = {'version': 1, 'name': self.Naam, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.bêre_VALUE(stand_VALUE)
        if Stelselinfo is None:
            self.Opdrag(['VBoxManage', 'createvm', '--name', stand_VALUE['name'], '--uuid', stand_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Pad('machines')), '--register'])
            self.Opdrag(['VBoxManage', 'setextradata', stand_VALUE['uuid'], 'JKOROS/Owner', stand_VALUE['owner']])
        # bou_stelsel 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Stelselinfo = self.Stelselinfo(stand_VALUE, 등록목록(self.Opdrag(['VBoxManage', 'list', 'vms'])))
        if Stelselinfo.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('bou_stelsel 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.tjek_media(stand_VALUE, Stelselinfo)
        stand_VALUE['iso'] = media_VALUE
        if media_VALUE not in stand_VALUE['media']: stand_VALUE['media'].append(media_VALUE)
        stand_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Pad(stand_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.bêre_VALUE(stand_VALUE)
        self.Opdrag(['VBoxManage', 'modifyvm', stand_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Naam, VALUE in Stelselinfo.items() if re.fullmatch(r'storagecontrollername\d+', Naam)]
        if 'JKOROS IDE' not in 제어기들:
            self.Opdrag(['VBoxManage', 'storagectl', stand_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Opdrag(['VBoxManage', 'storageattach', stand_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(bestemming_VALUE)])
        stand_VALUE['pending'] = False
        self.bêre_VALUE(stand_VALUE)
        self.Opdrag(['VBoxManage', 'startvm', stand_VALUE['uuid'], '--type', self.metode_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.wys_stand()


def Loop():
    ontleed_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox uitvoer_bevel 및 stand_VALUE navraag_VALUE')
    ontleed_VALUE.add_argument('action', choices=['run', 'status'])
    인자 = ontleed_VALUE.parse_args()
    uitvoer_bevel = program_oopmaker(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(uitvoer_bevel.wys_stand(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. hou 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/toestemming_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    uitvoer_bevel.Pad('lock').parent.mkdir(parents=True, exist_ok=True)
    with uitvoer_bevel.Pad('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox uitvoer_bevel 작업이 진행 중입니다.')
        print(json.dumps(uitvoer_bevel.uitvoer_bevel(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Loop()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Fout:
        print('VBOX Fout: ' + str(Fout), file=sys.stderr)
        sys.exit(1)
