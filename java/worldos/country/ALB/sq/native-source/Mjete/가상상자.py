#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_hapës. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def zbatoj_pasues_komandë(Argumente):
    환경 = dict(os.environ, LC_ALL='C')
    llogaritje = subprocess.run([str(VALUE) for VALUE in Argumente], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Përmbajtje_VALUE = llogaritje.stdout.decode('utf-8', 'replace')
    if llogaritje.returncode:
        raise 실행오류('Komanda dështim_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumente) + '\n' + Përmbajtje_VALUE[-10000:])
    return Përmbajtje_VALUE


def atribut_VALUE(Përmbajtje_VALUE):
    llogaritje = {}
    for linjë in Përmbajtje_VALUE.splitlines():
        if '=' not in linjë:
            continue
        Emër, VALUE = linjë.split('=', 1)
        if Emër.startswith('"'):
            Emër = json.loads(Emër)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribut_VALUE format_VALUE GABIM: ' + linjë)
        llogaritje[Emër] = VALUE
    return llogaritje


def 등록목록(Përmbajtje_VALUE):
    llogaritje = {}
    for linjë in Përmbajtje_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', linjë)
        if 일치: llogaritje[일치.group(2).lower()] = 일치.group(1)
    return llogaritje


def kontrolli_i_shumës(POZICIONI):
    VALUE = hashlib.sha256()
    with POZICIONI.open('rb') as Kartelë:
        for të_dhëna in iter(lambda: Kartelë.read(1024 * 1024), b''): VALUE.update(të_dhëna)
    return VALUE.hexdigest()


class program_hapës:
    def __init__(self, rrënjë_VALUE, Emër, metoda_MODE='gui', Komanda=zbatoj_pasues_komandë):
        self.rrënjë_VALUE = Path(rrënjë_VALUE).resolve()
        self.Emër, self.metoda_MODE, self.Komanda = Emër, metoda_MODE, Komanda
        self.보관 = self.rrënjë_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Emër) or Emër in ('.', '..'):
            raise 실행오류('VM 이름은 문자·shifër_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metoda_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def POZICIONI(self, homolog_VALUE):
        if Path(homolog_VALUE).is_absolute() or '..' in Path(homolog_VALUE).parts:
            raise 실행오류('잘못된 관리 POZICIONI: ' + str(homolog_VALUE))
        llogaritje = self.보관
        for 부분 in ['.vbox'] + list(Path(homolog_VALUE).parts):
            if 부분 == '.vbox': llogaritje = self.보관
            else: llogaritje = llogaritje / 부분
            if llogaritje.is_symlink(): raise 실행오류('Lidhu 경로는 사용하지 않습니다: ' + str(llogaritje))
        return llogaritje

    def Leximi(self):
        POZICIONI = self.POZICIONI('state.json')
        if not POZICIONI.exists(): return None
        status_VALUE = json.loads(POZICIONI.read_text(encoding='utf-8'))
        if status_VALUE.get('version') != 1 or status_VALUE.get('name') != self.Emër:
            raise 실행오류('관리 상태의 VM Emër/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Emër in ('uuid', 'owner'):
            if str(uuid.UUID(status_VALUE[Emër])) != status_VALUE[Emër]: raise 실행오류('잘못된 VM identifikues_VALUE')
        return status_VALUE

    def Store_VALUE(self, status_VALUE):
        vendmbërritje_VALUE = self.POZICIONI('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Kartelë:
            json.dump(status_VALUE, Kartelë, ensure_ascii=False, indent=2)
            Kartelë.write('\n')
            임시 = Kartelë.name
        os.replace(임시, str(vendmbërritje_VALUE))

    def msinfo32_exe(self, status_VALUE, 등록됨, rikuperoj_status=False):
        if status_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribut_VALUE(self.Komanda(['VBoxManage', 'showvminfo', status_VALUE['uuid'], '--machinereadable']))
        Pozicioni = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.POZICIONI('machines').resolve() not in Pozicioni.parents or msinfo32_exe.get('UUID') != status_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Rregullime POZICIONI/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Komanda(['VBoxManage', 'getextradata', status_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + status_VALUE['owner']:
            if rikuperoj_status and status_VALUE.get('pending') and 표식 == 'No value set!':
                self.Komanda(['VBoxManage', 'setextradata', status_VALUE['uuid'], 'JKOROS/Owner', status_VALUE['owner']])
            else:
                raise 실행오류('VM pronari_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, status_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Emër, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Emër)]
        Lejoj_VALUE = [str(self.POZICIONI(VALUE)) for VALUE in status_VALUE.get('media', [])]
        for Emër, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(pult) + r'-\d+-\d+', Emër) for pult in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Lejoj_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def shfaq_status(self):
        status_VALUE = self.Leximi()
        if status_VALUE is None: return {'name': self.Emër, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록목록(self.Komanda(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', status_VALUE['name']), 'uuid': status_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.POZICIONI(status_VALUE['iso'])) if status_VALUE.get('iso') else None,
                'serial_log': str(self.POZICIONI(status_VALUE['serial_log'])) if status_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def zbatoj_komandë(self):
        status_VALUE = self.Leximi()
        등록됨 = 등록목록(self.Komanda(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if status_VALUE is not None and status_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록됨, rikuperoj_status=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 zbatoj_komandë 중입니다. 재빌드·재시작하지 않습니다.')
                return self.shfaq_status()
            self.매체검사(status_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Komanda(['VBoxManage', 'controlvm', status_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Hap 전에 기존 기록도 보관한다.
                    if status_VALUE.get('serial_log'):
                        원본 = self.POZICIONI(status_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.POZICIONI('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Komanda(['VBoxManage', 'startvm', status_VALUE['uuid'], '--type', self.metoda_MODE])
                return self.shfaq_status()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 PAS_VALUE 다시 실행하세요.'.format(현재))
        elif status_VALUE is not None and not status_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Emër in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/zbatoj_komandë 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Komanda(['make', '-C', str(self.rrënjë_VALUE / 'os'), 'iso']), end='')
        원본 = self.rrënjë_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + kontrolli_i_shumës(원본) + '.iso'
        vendmbërritje_VALUE = self.POZICIONI(매체)
        vendmbërritje_VALUE.parent.mkdir(exist_ok=True)
        if vendmbërritje_VALUE.exists():
            if kontrolli_i_shumës(vendmbërritje_VALUE) != kontrolli_i_shumës(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(vendmbërritje_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(vendmbërritje_VALUE.parent)) as Kartelë:
                shutil.copyfile(str(원본), Kartelë.name)
                os.link(Kartelë.name, str(vendmbërritje_VALUE))

        if status_VALUE is None:
            status_VALUE = {'version': 1, 'name': self.Emër, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(status_VALUE)
        if msinfo32_exe is None:
            self.Komanda(['VBoxManage', 'createvm', '--name', status_VALUE['name'], '--uuid', status_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.POZICIONI('machines')), '--register'])
            self.Komanda(['VBoxManage', 'setextradata', status_VALUE['uuid'], 'JKOROS/Owner', status_VALUE['owner']])
        # ndërtoj_sistem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록목록(self.Komanda(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ndërtoj_sistem 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(status_VALUE, msinfo32_exe)
        status_VALUE['iso'] = 매체
        if 매체 not in status_VALUE['media']: status_VALUE['media'].append(매체)
        status_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.POZICIONI(status_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(status_VALUE)
        self.Komanda(['VBoxManage', 'modifyvm', status_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Emër, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Emër)]
        if 'JKOROS IDE' not in 제어기들:
            self.Komanda(['VBoxManage', 'storagectl', status_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Komanda(['VBoxManage', 'storageattach', status_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(vendmbërritje_VALUE)])
        status_VALUE['pending'] = False
        self.Store_VALUE(status_VALUE)
        self.Komanda(['VBoxManage', 'startvm', status_VALUE['uuid'], '--type', self.metoda_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.shfaq_status()


def Ekzekuto():
    analizoj_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox zbatoj_komandë 및 status_VALUE pyetja_VALUE')
    analizoj_VALUE.add_argument('action', choices=['run', 'status'])
    parametër_argument = analizoj_VALUE.parse_args()
    zbatoj_komandë = program_hapës(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametër_argument.action == 'status':
        print(json.dumps(zbatoj_komandë.shfaq_status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. pritës 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/leje_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    zbatoj_komandë.POZICIONI('lock').parent.mkdir(parents=True, exist_ok=True)
    with zbatoj_komandë.POZICIONI('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox zbatoj_komandë 작업이 진행 중입니다.')
        print(json.dumps(zbatoj_komandë.zbatoj_komandë(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Ekzekuto()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as GABIM:
        print('VBOX GABIM: ' + str(GABIM), file=sys.stderr)
        sys.exit(1)
