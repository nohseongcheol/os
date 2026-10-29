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


def Izvrši_ljuska_komanda(Argumenti):
    operativno_okruženje = dict(os.environ, LC_ALL='C')
    mjera = subprocess.run([str(VALUE) for VALUE in Argumenti], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=operativno_okruženje, timeout=180)
    Sadržaj_VALUE = mjera.stdout.decode('utf-8', 'replace')
    if mjera.returncode:
        raise 실행오류('Naredba neuspjeh_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumenti) + '\n' + Sadržaj_VALUE[-10000:])
    return Sadržaj_VALUE


def atribut_VALUE(Sadržaj_VALUE):
    mjera = {}
    for Linija in Sadržaj_VALUE.splitlines():
        if '=' not in Linija:
            continue
        Naziv, VALUE = Linija.split('=', 1)
        if Naziv.startswith('"'):
            Naziv = json.loads(Naziv)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribut_VALUE format_VALUE GRESKA: ' + Linija)
        mjera[Naziv] = VALUE
    return mjera


def 등록목록(Sadržaj_VALUE):
    mjera = {}
    for Linija in Sadržaj_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Linija)
        if 일치: mjera[일치.group(2).lower()] = 일치.group(1)
    return mjera


def kontrolni_zbir(Putanja):
    VALUE = hashlib.sha256()
    with Putanja.open('rb') as Fajl:
        for podaci in iter(lambda: Fajl.read(1024 * 1024), b''): VALUE.update(podaci)
    return VALUE.hexdigest()


class program_pokretač:
    def __init__(self, koijen_VALUE, Naziv, metoda_mod='gui', Naredba=Izvrši_ljuska_komanda):
        self.koijen_VALUE = Path(koijen_VALUE).resolve()
        self.Naziv, self.metoda_mod, self.Naredba = Naziv, metoda_mod, Naredba
        self.보관 = self.koijen_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Naziv) or Naziv in ('.', '..'):
            raise 실행오류('VM 이름은 문자·cifra_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metoda_mod not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Putanja(self, peer_VALUE):
        if Path(peer_VALUE).is_absolute() or '..' in Path(peer_VALUE).parts:
            raise 실행오류('잘못된 관리 Putanja: ' + str(peer_VALUE))
        mjera = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_VALUE).parts):
            if 부분 == '.vbox': mjera = self.보관
            else: mjera = mjera / 부분
            if mjera.is_symlink(): raise 실행오류('Spoji_se 경로는 사용하지 않습니다: ' + str(mjera))
        return mjera

    def Čitaj(self):
        Putanja = self.Putanja('state.json')
        if not Putanja.exists(): return None
        stanje_VALUE = json.loads(Putanja.read_text(encoding='utf-8'))
        if stanje_VALUE.get('version') != 1 or stanje_VALUE.get('name') != self.Naziv:
            raise 실행오류('관리 상태의 VM Naziv/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Naziv in ('uuid', 'owner'):
            if str(uuid.UUID(stanje_VALUE[Naziv])) != stanje_VALUE[Naziv]: raise 실행오류('잘못된 VM identifikator_VALUE')
        return stanje_VALUE

    def Store_VALUE(self, stanje_VALUE):
        odredište_VALUE = self.Putanja('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fajl:
            json.dump(stanje_VALUE, Fajl, ensure_ascii=False, indent=2)
            Fajl.write('\n')
            임시 = Fajl.name
        os.replace(임시, str(odredište_VALUE))

    def msinfo32_exe(self, stanje_VALUE, 등록됨, oporaviti_stanje=False):
        if stanje_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribut_VALUE(self.Naredba(['VBoxManage', 'showvminfo', stanje_VALUE['uuid'], '--machinereadable']))
        Pozicija = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Putanja('machines').resolve() not in Pozicija.parents or msinfo32_exe.get('UUID') != stanje_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Postavke Putanja/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Naredba(['VBoxManage', 'getextradata', stanje_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + stanje_VALUE['owner']:
            if oporaviti_stanje and stanje_VALUE.get('pending') and 표식 == 'No value set!':
                self.Naredba(['VBoxManage', 'setextradata', stanje_VALUE['uuid'], 'JKOROS/Owner', stanje_VALUE['owner']])
            else:
                raise 실행오류('VM vlasnik_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, stanje_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Naziv, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Naziv)]
        Dozvoliti_VALUE = [str(self.Putanja(VALUE)) for VALUE in stanje_VALUE.get('media', [])]
        for Naziv, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontroler) + r'-\d+-\d+', Naziv) for kontroler in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Dozvoliti_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def program_stanje(self):
        stanje_VALUE = self.Čitaj()
        if stanje_VALUE is None: return {'name': self.Naziv, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(stanje_VALUE, 등록목록(self.Naredba(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', stanje_VALUE['name']), 'uuid': stanje_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Putanja(stanje_VALUE['iso'])) if stanje_VALUE.get('iso') else None,
                'serial_log': str(self.Putanja(stanje_VALUE['serial_log'])) if stanje_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Izvrši_komanda(self):
        stanje_VALUE = self.Čitaj()
        등록됨 = 등록목록(self.Naredba(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if stanje_VALUE is not None and stanje_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(stanje_VALUE, 등록됨, oporaviti_stanje=True)
            trenutno_stavka = msinfo32_exe.get('VMState')
            if trenutno_stavka == 'running':
                print('이미 Izvrši_komanda 중입니다. 재빌드·재시작하지 않습니다.')
                return self.program_stanje()
            self.매체검사(stanje_VALUE, msinfo32_exe)
            if trenutno_stavka in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(trenutno_stavka))
                if trenutno_stavka == 'paused':
                    self.Naredba(['VBoxManage', 'controlvm', stanje_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Otvori 전에 기존 기록도 보관한다.
                    if stanje_VALUE.get('serial_log'):
                        원본 = self.Putanja(stanje_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Putanja('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Naredba(['VBoxManage', 'startvm', stanje_VALUE['uuid'], '--type', self.metoda_mod])
                return self.program_stanje()
            if trenutno_stavka not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_mod 중입니다 ({}). 작업이 끝난 ZAD_VALUE 다시 실행하세요.'.format(trenutno_stavka))
        elif stanje_VALUE is not None and not stanje_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Naziv in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Izvrši_komanda 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Naredba(['make', '-C', str(self.koijen_VALUE / 'os'), 'iso']), end='')
        원본 = self.koijen_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + kontrolni_zbir(원본) + '.iso'
        odredište_VALUE = self.Putanja(매체)
        odredište_VALUE.parent.mkdir(exist_ok=True)
        if odredište_VALUE.exists():
            if kontrolni_zbir(odredište_VALUE) != kontrolni_zbir(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(odredište_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(odredište_VALUE.parent)) as Fajl:
                shutil.copyfile(str(원본), Fajl.name)
                os.link(Fajl.name, str(odredište_VALUE))

        if stanje_VALUE is None:
            stanje_VALUE = {'version': 1, 'name': self.Naziv, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(stanje_VALUE)
        if msinfo32_exe is None:
            self.Naredba(['VBoxManage', 'createvm', '--name', stanje_VALUE['name'], '--uuid', stanje_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Putanja('machines')), '--register'])
            self.Naredba(['VBoxManage', 'setextradata', stanje_VALUE['uuid'], 'JKOROS/Owner', stanje_VALUE['owner']])
        # verzija_sistem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(stanje_VALUE, 등록목록(self.Naredba(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('verzija_sistem 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(stanje_VALUE, msinfo32_exe)
        stanje_VALUE['iso'] = 매체
        if 매체 not in stanje_VALUE['media']: stanje_VALUE['media'].append(매체)
        stanje_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Putanja(stanje_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(stanje_VALUE)
        self.Naredba(['VBoxManage', 'modifyvm', stanje_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Naziv, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Naziv)]
        if 'JKOROS IDE' not in 제어기들:
            self.Naredba(['VBoxManage', 'storagectl', stanje_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Naredba(['VBoxManage', 'storageattach', stanje_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(odredište_VALUE)])
        stanje_VALUE['pending'] = False
        self.Store_VALUE(stanje_VALUE)
        self.Naredba(['VBoxManage', 'startvm', stanje_VALUE['uuid'], '--type', self.metoda_mod])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.program_stanje()


def Pokreni():
    raščlanjivati_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Izvrši_komanda 및 stanje_VALUE upit_VALUE')
    raščlanjivati_VALUE.add_argument('action', choices=['run', 'status'])
    parametar_argument = raščlanjivati_VALUE.parse_args()
    Izvrši_komanda = program_pokretač(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametar_argument.action == 'status':
        print(json.dumps(Izvrši_komanda.program_stanje(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. organizator 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/dozvola_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Izvrši_komanda.Putanja('lock').parent.mkdir(parents=True, exist_ok=True)
    with Izvrši_komanda.Putanja('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Izvrši_komanda 작업이 진행 중입니다.')
        print(json.dumps(Izvrši_komanda.Izvrši_komanda(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Pokreni()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as GRESKA:
        print('VBOX GRESKA: ' + str(GRESKA), file=sys.stderr)
        sys.exit(1)
