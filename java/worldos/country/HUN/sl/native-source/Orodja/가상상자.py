#!/usr/bin/env python3
"""jkoros 전용 VirtualBox aplikacija_zaganjalnik. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Izvedi_lupina_ukaz(Argumenti):
    환경 = dict(os.environ, LC_ALL='C')
    REZULTAT = subprocess.run([str(VALUE) for VALUE in Argumenti], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    vsebina_VALUE = REZULTAT.stdout.decode('utf-8', 'replace')
    if REZULTAT.returncode:
        raise 실행오류('Ukaz napaka_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumenti) + '\n' + vsebina_VALUE[-10000:])
    return vsebina_VALUE


def atribut_VALUE(vsebina_VALUE):
    REZULTAT = {}
    for Črtni in vsebina_VALUE.splitlines():
        if '=' not in Črtni:
            continue
        Ime, VALUE = Črtni.split('=', 1)
        if Ime.startswith('"'):
            Ime = json.loads(Ime)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribut_VALUE oblika_VALUE NAPAKA: ' + Črtni)
        REZULTAT[Ime] = VALUE
    return REZULTAT


def 등록목록(vsebina_VALUE):
    REZULTAT = {}
    for Črtni in vsebina_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Črtni)
        if 일치: REZULTAT[일치.group(2).lower()] = 일치.group(1)
    return REZULTAT


def kontrolna_vsota(POT):
    VALUE = hashlib.sha256()
    with POT.open('rb') as Datoteka:
        for podatki in iter(lambda: Datoteka.read(1024 * 1024), b''): VALUE.update(podatki)
    return VALUE.hexdigest()


class aplikacija_zaganjalnik:
    def __init__(self, koren_VALUE, Ime, metoda_MODE='gui', Ukaz=Izvedi_lupina_ukaz):
        self.koren_VALUE = Path(koren_VALUE).resolve()
        self.Ime, self.metoda_MODE, self.Ukaz = Ime, metoda_MODE, Ukaz
        self.보관 = self.koren_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ime) or Ime in ('.', '..'):
            raise 실행오류('VM 이름은 문자·številka_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metoda_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def POT(self, enakovreden_VALUE):
        if Path(enakovreden_VALUE).is_absolute() or '..' in Path(enakovreden_VALUE).parts:
            raise 실행오류('잘못된 관리 POT: ' + str(enakovreden_VALUE))
        REZULTAT = self.보관
        for 부분 in ['.vbox'] + list(Path(enakovreden_VALUE).parts):
            if 부분 == '.vbox': REZULTAT = self.보관
            else: REZULTAT = REZULTAT / 부분
            if REZULTAT.is_symlink(): raise 실행오류('Poveži 경로는 사용하지 않습니다: ' + str(REZULTAT))
        return REZULTAT

    def Branje(self):
        POT = self.POT('state.json')
        if not POT.exists(): return None
        stanje_VALUE = json.loads(POT.read_text(encoding='utf-8'))
        if stanje_VALUE.get('version') != 1 or stanje_VALUE.get('name') != self.Ime:
            raise 실행오류('관리 상태의 VM Ime/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ime in ('uuid', 'owner'):
            if str(uuid.UUID(stanje_VALUE[Ime])) != stanje_VALUE[Ime]: raise 실행오류('잘못된 VM identifikator_VALUE')
        return stanje_VALUE

    def Store_VALUE(self, stanje_VALUE):
        cilj_VALUE = self.POT('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Datoteka:
            json.dump(stanje_VALUE, Datoteka, ensure_ascii=False, indent=2)
            Datoteka.write('\n')
            임시 = Datoteka.name
        os.replace(임시, str(cilj_VALUE))

    def msinfo32_exe(self, stanje_VALUE, 등록됨, obnoviti_stanje=False):
        if stanje_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribut_VALUE(self.Ukaz(['VBoxManage', 'showvminfo', stanje_VALUE['uuid'], '--machinereadable']))
        Položaj = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.POT('machines').resolve() not in Položaj.parents or msinfo32_exe.get('UUID') != stanje_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Nastavitve POT/UUID와 일치하지 않아 변경하지 않습니다.')
        oznaka_VALUE_7e8f90bd = self.Ukaz(['VBoxManage', 'getextradata', stanje_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if oznaka_VALUE_7e8f90bd != 'Value: ' + stanje_VALUE['owner']:
            if obnoviti_stanje and stanje_VALUE.get('pending') and oznaka_VALUE_7e8f90bd == 'No value set!':
                self.Ukaz(['VBoxManage', 'setextradata', stanje_VALUE['uuid'], 'JKOROS/Owner', stanje_VALUE['owner']])
            else:
                raise 실행오류('VM lastnik_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def preveriti_mediji(self, stanje_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Ime, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ime)]
        Dovoli_VALUE = [str(self.POT(VALUE)) for VALUE in stanje_VALUE.get('media', [])]
        for Ime, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(krmilnik) + r'-\d+-\d+', Ime) for krmilnik in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Dovoli_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def oddaja_stanje(self):
        stanje_VALUE = self.Branje()
        if stanje_VALUE is None: return {'name': self.Ime, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(stanje_VALUE, 등록목록(self.Ukaz(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', stanje_VALUE['name']), 'uuid': stanje_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.POT(stanje_VALUE['iso'])) if stanje_VALUE.get('iso') else None,
                'serial_log': str(self.POT(stanje_VALUE['serial_log'])) if stanje_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Izvedi_ukaz(self):
        stanje_VALUE = self.Branje()
        등록됨 = 등록목록(self.Ukaz(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if stanje_VALUE is not None and stanje_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(stanje_VALUE, 등록됨, obnoviti_stanje=True)
            sprotno_element = msinfo32_exe.get('VMState')
            if sprotno_element == 'running':
                print('이미 Izvedi_ukaz 중입니다. 재빌드·재시작하지 않습니다.')
                return self.oddaja_stanje()
            self.preveriti_mediji(stanje_VALUE, msinfo32_exe)
            if sprotno_element in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(sprotno_element))
                if sprotno_element == 'paused':
                    self.Ukaz(['VBoxManage', 'controlvm', stanje_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 znova_poskusiti_VALUE Odpri 전에 기존 기록도 보관한다.
                    if stanje_VALUE.get('serial_log'):
                        원본 = self.POT(stanje_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.POT('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Ukaz(['VBoxManage', 'startvm', stanje_VALUE['uuid'], '--type', self.metoda_MODE])
                return self.oddaja_stanje()
            if sprotno_element not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 ZAJ_VALUE znova_poskusiti_VALUE 실행하세요.'.format(sprotno_element))
        elif stanje_VALUE is not None and not stanje_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 znova_poskusiti_VALUE 등록하세요.')
        elif self.Ime in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Izvedi_ukaz 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Ukaz(['make', '-C', str(self.koren_VALUE / 'os'), 'iso']), end='')
        원본 = self.koren_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        mediji_VALUE = 'media/kernel-' + kontrolna_vsota(원본) + '.iso'
        cilj_VALUE = self.POT(mediji_VALUE)
        cilj_VALUE.parent.mkdir(exist_ok=True)
        if cilj_VALUE.exists():
            if kontrolna_vsota(cilj_VALUE) != kontrolna_vsota(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(cilj_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(cilj_VALUE.parent)) as Datoteka:
                shutil.copyfile(str(원본), Datoteka.name)
                os.link(Datoteka.name, str(cilj_VALUE))

        if stanje_VALUE is None:
            stanje_VALUE = {'version': 1, 'name': self.Ime, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(stanje_VALUE)
        if msinfo32_exe is None:
            self.Ukaz(['VBoxManage', 'createvm', '--name', stanje_VALUE['name'], '--uuid', stanje_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.POT('machines')), '--register'])
            self.Ukaz(['VBoxManage', 'setextradata', stanje_VALUE['uuid'], 'JKOROS/Owner', stanje_VALUE['owner']])
        # graditev_sistem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(stanje_VALUE, 등록목록(self.Ukaz(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('graditev_sistem 중 VM 상태가 바뀌었습니다. znova_poskusiti_VALUE make vbox를 실행하세요.')
        self.preveriti_mediji(stanje_VALUE, msinfo32_exe)
        stanje_VALUE['iso'] = mediji_VALUE
        if mediji_VALUE not in stanje_VALUE['media']: stanje_VALUE['media'].append(mediji_VALUE)
        stanje_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.POT(stanje_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(stanje_VALUE)
        self.Ukaz(['VBoxManage', 'modifyvm', stanje_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Ime, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ime)]
        if 'JKOROS IDE' not in 제어기들:
            self.Ukaz(['VBoxManage', 'storagectl', stanje_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Ukaz(['VBoxManage', 'storageattach', stanje_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(cilj_VALUE)])
        stanje_VALUE['pending'] = False
        self.Store_VALUE(stanje_VALUE)
        self.Ukaz(['VBoxManage', 'startvm', stanje_VALUE['uuid'], '--type', self.metoda_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.oddaja_stanje()


def Zaženi():
    razčlenjevati_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Izvedi_ukaz 및 stanje_VALUE poizvedba_VALUE')
    razčlenjevati_VALUE.add_argument('action', choices=['run', 'status'])
    parameter_argument = razčlenjevati_VALUE.parse_args()
    Izvedi_ukaz = aplikacija_zaganjalnik(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(Izvedi_ukaz.oddaja_stanje(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. gostiti 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/dovoljenje_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Izvedi_ukaz.POT('lock').parent.mkdir(parents=True, exist_ok=True)
    with Izvedi_ukaz.POT('lock').open('a') as zaklepanje_VALUE:
        try: fcntl.flock(zaklepanje_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Izvedi_ukaz 작업이 진행 중입니다.')
        print(json.dumps(Izvedi_ukaz.Izvedi_ukaz(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Zaženi()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as NAPAKA:
        print('VBOX NAPAKA: ' + str(NAPAKA), file=sys.stderr)
        sys.exit(1)
