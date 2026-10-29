#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programma_palaidējs. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Izpildīt_čaula_komanda(Parametri):
    환경 = dict(os.environ, LC_ALL='C')
    mērs = subprocess.run([str(VALUE) for VALUE in Parametri], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Saturs_VALUE = mērs.stdout.decode('utf-8', 'replace')
    if mērs.returncode:
        raise 실행오류('Komanda kļūme_VALUE: ' + ' '.join(str(VALUE) for VALUE in Parametri) + '\n' + Saturs_VALUE[-10000:])
    return Saturs_VALUE


def atribūts_VALUE(Saturs_VALUE):
    mērs = {}
    for Līniju in Saturs_VALUE.splitlines():
        if '=' not in Līniju:
            continue
        Nosaukums, VALUE = Līniju.split('=', 1)
        if Nosaukums.startswith('"'):
            Nosaukums = json.loads(Nosaukums)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribūts_VALUE formāts_VALUE Kļūda: ' + Līniju)
        mērs[Nosaukums] = VALUE
    return mērs


def 등록목록(Saturs_VALUE):
    mērs = {}
    for Līniju in Saturs_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Līniju)
        if 일치: mērs[일치.group(2).lower()] = 일치.group(1)
    return mērs


def kontrolsumma(CEĻŠ):
    VALUE = hashlib.sha256()
    with CEĻŠ.open('rb') as Fails:
        for dati in iter(lambda: Fails.read(1024 * 1024), b''): VALUE.update(dati)
    return VALUE.hexdigest()


class programma_palaidējs:
    def __init__(self, sakne_VALUE, Nosaukums, metode_MODE='gui', Komanda=Izpildīt_čaula_komanda):
        self.sakne_VALUE = Path(sakne_VALUE).resolve()
        self.Nosaukums, self.metode_MODE, self.Komanda = Nosaukums, metode_MODE, Komanda
        self.보관 = self.sakne_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nosaukums) or Nosaukums in ('.', '..'):
            raise 실행오류('VM 이름은 문자·cipars_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 numurs 있습니다.')
        if metode_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def CEĻŠ(self, vienranga_VALUE):
        if Path(vienranga_VALUE).is_absolute() or '..' in Path(vienranga_VALUE).parts:
            raise 실행오류('잘못된 관리 CEĻŠ: ' + str(vienranga_VALUE))
        mērs = self.보관
        for 부분 in ['.vbox'] + list(Path(vienranga_VALUE).parts):
            if 부분 == '.vbox': mērs = self.보관
            else: mērs = mērs / 부분
            if mērs.is_symlink(): raise 실행오류('Savienoties 경로는 사용하지 않습니다: ' + str(mērs))
        return mērs

    def Lasīt(self):
        CEĻŠ = self.CEĻŠ('state.json')
        if not CEĻŠ.exists(): return None
        Statuss_VALUE = json.loads(CEĻŠ.read_text(encoding='utf-8'))
        if Statuss_VALUE.get('version') != 1 or Statuss_VALUE.get('name') != self.Nosaukums:
            raise 실행오류('관리 상태의 VM Nosaukums/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nosaukums in ('uuid', 'owner'):
            if str(uuid.UUID(Statuss_VALUE[Nosaukums])) != Statuss_VALUE[Nosaukums]: raise 실행오류('잘못된 VM identifikators_VALUE')
        return Statuss_VALUE

    def Store_VALUE(self, Statuss_VALUE):
        mērķis_VALUE = self.CEĻŠ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fails:
            json.dump(Statuss_VALUE, Fails, ensure_ascii=False, indent=2)
            Fails.write('\n')
            임시 = Fails.name
        os.replace(임시, str(mērķis_VALUE))

    def msinfo32_exe(self, Statuss_VALUE, 등록됨, atgūt_Statuss=False):
        if Statuss_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribūts_VALUE(self.Komanda(['VBoxManage', 'showvminfo', Statuss_VALUE['uuid'], '--machinereadable']))
        Novietojums = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.CEĻŠ('machines').resolve() not in Novietojums.parents or msinfo32_exe.get('UUID') != Statuss_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Uzstādījumi CEĻŠ/UUID와 일치하지 않아 변경하지 않습니다.')
        marķieris_VALUE = self.Komanda(['VBoxManage', 'getextradata', Statuss_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if marķieris_VALUE != 'Value: ' + Statuss_VALUE['owner']:
            if atgūt_Statuss and Statuss_VALUE.get('pending') and marķieris_VALUE == 'No value set!':
                self.Komanda(['VBoxManage', 'setextradata', Statuss_VALUE['uuid'], 'JKOROS/Owner', Statuss_VALUE['owner']])
            else:
                raise 실행오류('VM īpašnieks_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def čeks_datu_nesējs(self, Statuss_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Nosaukums, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nosaukums)]
        Atļaut_VALUE = [str(self.CEĻŠ(VALUE)) for VALUE in Statuss_VALUE.get('media', [])]
        for Nosaukums, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(pārzinis) + r'-\d+-\d+', Nosaukums) for pārzinis in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Atļaut_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def rādīt_Statuss(self):
        Statuss_VALUE = self.Lasīt()
        if Statuss_VALUE is None: return {'name': self.Nosaukums, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Statuss_VALUE, 등록목록(self.Komanda(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Statuss_VALUE['name']), 'uuid': Statuss_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.CEĻŠ(Statuss_VALUE['iso'])) if Statuss_VALUE.get('iso') else None,
                'serial_log': str(self.CEĻŠ(Statuss_VALUE['serial_log'])) if Statuss_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Izpildīt_komanda(self):
        Statuss_VALUE = self.Lasīt()
        등록됨 = 등록목록(self.Komanda(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Statuss_VALUE is not None and Statuss_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Statuss_VALUE, 등록됨, atgūt_Statuss=True)
            pašreizējais_krājums = msinfo32_exe.get('VMState')
            if pašreizējais_krājums == 'running':
                print('이미 Izpildīt_komanda 중입니다. 재빌드·재시작하지 않습니다.')
                return self.rādīt_Statuss()
            self.čeks_datu_nesējs(Statuss_VALUE, msinfo32_exe)
            if pašreizējais_krājums in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(pašreizējais_krājums))
                if pašreizējais_krājums == 'paused':
                    self.Komanda(['VBoxManage', 'controlvm', Statuss_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 mēģināt_vēlreiz_VALUE Atvērt 전에 기존 기록도 보관한다.
                    if Statuss_VALUE.get('serial_log'):
                        원본 = self.CEĻŠ(Statuss_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.CEĻŠ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Komanda(['VBoxManage', 'startvm', Statuss_VALUE['uuid'], '--type', self.metode_MODE])
                return self.rādīt_Statuss()
            if pašreizējais_krājums not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 ATPAKAĻ_VALUE mēģināt_vēlreiz_VALUE 실행하세요.'.format(pašreizējais_krājums))
        elif Statuss_VALUE is not None and not Statuss_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 mēģināt_vēlreiz_VALUE 등록하세요.')
        elif self.Nosaukums in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Izpildīt_komanda 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Komanda(['make', '-C', str(self.sakne_VALUE / 'os'), 'iso']), end='')
        원본 = self.sakne_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        datu_nesējs_VALUE = 'media/kernel-' + kontrolsumma(원본) + '.iso'
        mērķis_VALUE = self.CEĻŠ(datu_nesējs_VALUE)
        mērķis_VALUE.parent.mkdir(exist_ok=True)
        if mērķis_VALUE.exists():
            if kontrolsumma(mērķis_VALUE) != kontrolsumma(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(mērķis_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(mērķis_VALUE.parent)) as Fails:
                shutil.copyfile(str(원본), Fails.name)
                os.link(Fails.name, str(mērķis_VALUE))

        if Statuss_VALUE is None:
            Statuss_VALUE = {'version': 1, 'name': self.Nosaukums, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Statuss_VALUE)
        if msinfo32_exe is None:
            self.Komanda(['VBoxManage', 'createvm', '--name', Statuss_VALUE['name'], '--uuid', Statuss_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.CEĻŠ('machines')), '--register'])
            self.Komanda(['VBoxManage', 'setextradata', Statuss_VALUE['uuid'], 'JKOROS/Owner', Statuss_VALUE['owner']])
        # būvējums_sistēma 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Statuss_VALUE, 등록목록(self.Komanda(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('būvējums_sistēma 중 VM 상태가 바뀌었습니다. mēģināt_vēlreiz_VALUE make vbox를 실행하세요.')
        self.čeks_datu_nesējs(Statuss_VALUE, msinfo32_exe)
        Statuss_VALUE['iso'] = datu_nesējs_VALUE
        if datu_nesējs_VALUE not in Statuss_VALUE['media']: Statuss_VALUE['media'].append(datu_nesējs_VALUE)
        Statuss_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.CEĻŠ(Statuss_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Statuss_VALUE)
        self.Komanda(['VBoxManage', 'modifyvm', Statuss_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Nosaukums, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nosaukums)]
        if 'JKOROS IDE' not in 제어기들:
            self.Komanda(['VBoxManage', 'storagectl', Statuss_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Komanda(['VBoxManage', 'storageattach', Statuss_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(mērķis_VALUE)])
        Statuss_VALUE['pending'] = False
        self.Store_VALUE(Statuss_VALUE)
        self.Komanda(['VBoxManage', 'startvm', Statuss_VALUE['uuid'], '--type', self.metode_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.rādīt_Statuss()


def Palaist():
    parsēt_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Izpildīt_komanda 및 Statuss_VALUE vaicāt_VALUE')
    parsēt_VALUE.add_argument('action', choices=['run', 'status'])
    parametrs_arg = parsēt_VALUE.parse_args()
    Izpildīt_komanda = programma_palaidējs(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametrs_arg.action == 'status':
        print(json.dumps(Izpildīt_komanda.rādīt_Statuss(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 numurs 없습니다. viesot 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/atļauja_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Izpildīt_komanda.CEĻŠ('lock').parent.mkdir(parents=True, exist_ok=True)
    with Izpildīt_komanda.CEĻŠ('lock').open('a') as bloķēt_VALUE:
        try: fcntl.flock(bloķēt_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Izpildīt_komanda 작업이 진행 중입니다.')
        print(json.dumps(Izpildīt_komanda.Izpildīt_komanda(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Palaist()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Kļūda:
        print('VBOX Kļūda: ' + str(Kļūda), file=sys.stderr)
        sys.exit(1)
