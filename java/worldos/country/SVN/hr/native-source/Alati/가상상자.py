#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_pokretač. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Izvrši_ljuska_naredba(Argumenti):
    okruženje = dict(os.environ, LC_ALL='C')
    REZULTAT = subprocess.run([str(VALUE) for VALUE in Argumenti], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=okruženje, timeout=180)
    Sadržaj_VALUE = REZULTAT.stdout.decode('utf-8', 'replace')
    if REZULTAT.returncode:
        raise 실행오류('Naredba kvar_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumenti) + '\n' + Sadržaj_VALUE[-10000:])
    return Sadržaj_VALUE


def atribut_VALUE(Sadržaj_VALUE):
    REZULTAT = {}
    for red in Sadržaj_VALUE.splitlines():
        if '=' not in red:
            continue
        Ime, VALUE = red.split('=', 1)
        if Ime.startswith('"'):
            Ime = json.loads(Ime)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribut_VALUE oblik_VALUE GREŠKA: ' + red)
        REZULTAT[Ime] = VALUE
    return REZULTAT


def 등록목록(Sadržaj_VALUE):
    REZULTAT = {}
    for red in Sadržaj_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', red)
        if 일치: REZULTAT[일치.group(2).lower()] = 일치.group(1)
    return REZULTAT


def kontrolni_zbroj(PUTANJA):
    VALUE = hashlib.sha256()
    with PUTANJA.open('rb') as Datoteka:
        for podaci in iter(lambda: Datoteka.read(1024 * 1024), b''): VALUE.update(podaci)
    return VALUE.hexdigest()


class program_pokretač:
    def __init__(self, korijen_VALUE, Ime, postupak_MODE='gui', Naredba=Izvrši_ljuska_naredba):
        self.korijen_VALUE = Path(korijen_VALUE).resolve()
        self.Ime, self.postupak_MODE, self.Naredba = Ime, postupak_MODE, Naredba
        self.보관 = self.korijen_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ime) or Ime in ('.', '..'):
            raise 실행오류('VM 이름은 문자·znamenka_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if postupak_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def PUTANJA(self, ravnopravan_član_VALUE):
        if Path(ravnopravan_član_VALUE).is_absolute() or '..' in Path(ravnopravan_član_VALUE).parts:
            raise 실행오류('잘못된 관리 PUTANJA: ' + str(ravnopravan_član_VALUE))
        REZULTAT = self.보관
        for 부분 in ['.vbox'] + list(Path(ravnopravan_član_VALUE).parts):
            if 부분 == '.vbox': REZULTAT = self.보관
            else: REZULTAT = REZULTAT / 부분
            if REZULTAT.is_symlink(): raise 실행오류('Spoji_se 경로는 사용하지 않습니다: ' + str(REZULTAT))
        return REZULTAT

    def Čitaj(self):
        PUTANJA = self.PUTANJA('state.json')
        if not PUTANJA.exists(): return None
        Stanje_VALUE = json.loads(PUTANJA.read_text(encoding='utf-8'))
        if Stanje_VALUE.get('version') != 1 or Stanje_VALUE.get('name') != self.Ime:
            raise 실행오류('관리 상태의 VM Ime/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ime in ('uuid', 'owner'):
            if str(uuid.UUID(Stanje_VALUE[Ime])) != Stanje_VALUE[Ime]: raise 실행오류('잘못된 VM identifikator_VALUE')
        return Stanje_VALUE

    def Store_VALUE(self, Stanje_VALUE):
        odredište_VALUE = self.PUTANJA('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Datoteka:
            json.dump(Stanje_VALUE, Datoteka, ensure_ascii=False, indent=2)
            Datoteka.write('\n')
            임시 = Datoteka.name
        os.replace(임시, str(odredište_VALUE))

    def Podaci_o_sustavu(self, Stanje_VALUE, 등록됨, oporaviti_Stanje=False):
        if Stanje_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Podaci_o_sustavu = atribut_VALUE(self.Naredba(['VBoxManage', 'showvminfo', Stanje_VALUE['uuid'], '--machinereadable']))
        Položaj = Path(Podaci_o_sustavu.get('CfgFile', '')).resolve()
        if self.PUTANJA('machines').resolve() not in Položaj.parents or Podaci_o_sustavu.get('UUID') != Stanje_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Postavke PUTANJA/UUID와 일치하지 않아 변경하지 않습니다.')
        marker_VALUE = self.Naredba(['VBoxManage', 'getextradata', Stanje_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if marker_VALUE != 'Value: ' + Stanje_VALUE['owner']:
            if oporaviti_Stanje and Stanje_VALUE.get('pending') and marker_VALUE == 'No value set!':
                self.Naredba(['VBoxManage', 'setextradata', Stanje_VALUE['uuid'], 'JKOROS/Owner', Stanje_VALUE['owner']])
            else:
                raise 실행오류('VM vlasnik_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return Podaci_o_sustavu

    def 매체검사(self, Stanje_VALUE, Podaci_o_sustavu):
        제어기들 = [VALUE for Ime, VALUE in Podaci_o_sustavu.items() if re.fullmatch(r'storagecontrollername\d+', Ime)]
        Dopusti_VALUE = [str(self.PUTANJA(VALUE)) for VALUE in Stanje_VALUE.get('media', [])]
        for Ime, VALUE in Podaci_o_sustavu.items():
            if any(re.fullmatch(re.escape(kontroler) + r'-\d+-\d+', Ime) for kontroler in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Dopusti_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def emisija_Stanje(self):
        Stanje_VALUE = self.Čitaj()
        if Stanje_VALUE is None: return {'name': self.Ime, 'state': 'not-created'}
        Podaci_o_sustavu = self.Podaci_o_sustavu(Stanje_VALUE, 등록목록(self.Naredba(['VBoxManage', 'list', 'vms'])))
        return {'name': Podaci_o_sustavu.get('name', Stanje_VALUE['name']), 'uuid': Stanje_VALUE['uuid'], 'state': Podaci_o_sustavu.get('VMState'),
                'iso': str(self.PUTANJA(Stanje_VALUE['iso'])) if Stanje_VALUE.get('iso') else None,
                'serial_log': str(self.PUTANJA(Stanje_VALUE['serial_log'])) if Stanje_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Izvrši_naredba(self):
        Stanje_VALUE = self.Čitaj()
        등록됨 = 등록목록(self.Naredba(['VBoxManage', 'list', 'vms']))
        Podaci_o_sustavu = None
        if Stanje_VALUE is not None and Stanje_VALUE['uuid'] in 등록됨:
            Podaci_o_sustavu = self.Podaci_o_sustavu(Stanje_VALUE, 등록됨, oporaviti_Stanje=True)
            redovno_artikl = Podaci_o_sustavu.get('VMState')
            if redovno_artikl == 'running':
                print('이미 Izvrši_naredba 중입니다. 재빌드·재시작하지 않습니다.')
                return self.emisija_Stanje()
            self.매체검사(Stanje_VALUE, Podaci_o_sustavu)
            if redovno_artikl in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(redovno_artikl))
                if redovno_artikl == 'paused':
                    self.Naredba(['VBoxManage', 'controlvm', Stanje_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 pokušati_ponovno_VALUE Otvori 전에 기존 기록도 보관한다.
                    if Stanje_VALUE.get('serial_log'):
                        원본 = self.PUTANJA(Stanje_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.PUTANJA('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Naredba(['VBoxManage', 'startvm', Stanje_VALUE['uuid'], '--type', self.postupak_MODE])
                return self.emisija_Stanje()
            if redovno_artikl not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 TRAG_VALUE pokušati_ponovno_VALUE 실행하세요.'.format(redovno_artikl))
        elif Stanje_VALUE is not None and not Stanje_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 pokušati_ponovno_VALUE 등록하세요.')
        elif self.Ime in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Izvrši_naredba 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Naredba(['make', '-C', str(self.korijen_VALUE / 'os'), 'iso']), end='')
        원본 = self.korijen_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        medij_VALUE = 'media/kernel-' + kontrolni_zbroj(원본) + '.iso'
        odredište_VALUE = self.PUTANJA(medij_VALUE)
        odredište_VALUE.parent.mkdir(exist_ok=True)
        if odredište_VALUE.exists():
            if kontrolni_zbroj(odredište_VALUE) != kontrolni_zbroj(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(odredište_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(odredište_VALUE.parent)) as Datoteka:
                shutil.copyfile(str(원본), Datoteka.name)
                os.link(Datoteka.name, str(odredište_VALUE))

        if Stanje_VALUE is None:
            Stanje_VALUE = {'version': 1, 'name': self.Ime, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Stanje_VALUE)
        if Podaci_o_sustavu is None:
            self.Naredba(['VBoxManage', 'createvm', '--name', Stanje_VALUE['name'], '--uuid', Stanje_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.PUTANJA('machines')), '--register'])
            self.Naredba(['VBoxManage', 'setextradata', Stanje_VALUE['uuid'], 'JKOROS/Owner', Stanje_VALUE['owner']])
        # međuverzija_sustav 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Podaci_o_sustavu = self.Podaci_o_sustavu(Stanje_VALUE, 등록목록(self.Naredba(['VBoxManage', 'list', 'vms'])))
        if Podaci_o_sustavu.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('međuverzija_sustav 중 VM 상태가 바뀌었습니다. pokušati_ponovno_VALUE make vbox를 실행하세요.')
        self.매체검사(Stanje_VALUE, Podaci_o_sustavu)
        Stanje_VALUE['iso'] = medij_VALUE
        if medij_VALUE not in Stanje_VALUE['media']: Stanje_VALUE['media'].append(medij_VALUE)
        Stanje_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.PUTANJA(Stanje_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Stanje_VALUE)
        self.Naredba(['VBoxManage', 'modifyvm', Stanje_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Ime, VALUE in Podaci_o_sustavu.items() if re.fullmatch(r'storagecontrollername\d+', Ime)]
        if 'JKOROS IDE' not in 제어기들:
            self.Naredba(['VBoxManage', 'storagectl', Stanje_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Naredba(['VBoxManage', 'storageattach', Stanje_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(odredište_VALUE)])
        Stanje_VALUE['pending'] = False
        self.Store_VALUE(Stanje_VALUE)
        self.Naredba(['VBoxManage', 'startvm', Stanje_VALUE['uuid'], '--type', self.postupak_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.emisija_Stanje()


def Pokreni():
    rastavljati_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Izvrši_naredba 및 Stanje_VALUE upit_VALUE')
    rastavljati_VALUE.add_argument('action', choices=['run', 'status'])
    parametar_argument = rastavljati_VALUE.parse_args()
    Izvrši_naredba = program_pokretač(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametar_argument.action == 'status':
        print(json.dumps(Izvrši_naredba.emisija_Stanje(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. domaćin 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/dozvola_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Izvrši_naredba.PUTANJA('lock').parent.mkdir(parents=True, exist_ok=True)
    with Izvrši_naredba.PUTANJA('lock').open('a') as zaključati_VALUE:
        try: fcntl.flock(zaključati_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Izvrši_naredba 작업이 진행 중입니다.')
        print(json.dumps(Izvrši_naredba.Izvrši_naredba(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Pokreni()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as GREŠKA:
        print('VBOX GREŠKA: ' + str(GREŠKA), file=sys.stderr)
        sys.exit(1)
