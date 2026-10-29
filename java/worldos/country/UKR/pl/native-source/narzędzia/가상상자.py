#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_Launcher. 기존 VM/디스크/Store_WARTOŚĆ 상태는 삭제하지 않는다."""
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


class wykonanie_błąd(RuntimeError):
    pass


def Wykonaj_powłoka_polecenie(argumenty):
    środowisko = dict(os.environ, LC_ALL='C')
    WYNIK = subprocess.run([str(WARTOŚĆ) for WARTOŚĆ in argumenty], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=środowisko, timeout=180)
    treść_WARTOŚĆ_cb0f2404 = WYNIK.stdout.decode('utf-8', 'replace')
    if WYNIK.returncode:
        raise wykonanie_błąd('polecenie awaria_WARTOŚĆ: ' + ' '.join(str(WARTOŚĆ) for WARTOŚĆ in argumenty) + '\n' + treść_WARTOŚĆ_cb0f2404[-10000:])
    return treść_WARTOŚĆ_cb0f2404


def wartość_atrybutu(treść_WARTOŚĆ_cb0f2404):
    WYNIK = {}
    for wiersz_wejścia in treść_WARTOŚĆ_cb0f2404.splitlines():
        if '=' not in wiersz_wejścia:
            continue
        Nazwa, WARTOŚĆ = wiersz_wejścia.split('=', 1)
        if Nazwa.startswith('"'):
            Nazwa = json.loads(Nazwa)
        if WARTOŚĆ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(WARTOŚĆ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(WARTOŚĆ): WARTOŚĆ = 읽은값
            except ValueError:
                raise wykonanie_błąd('VirtualBox wartość_atrybutu format_WARTOŚĆ błąd: ' + wiersz_wejścia)
        WYNIK[Nazwa] = WARTOŚĆ
    return WYNIK


def 등록목록(treść_WARTOŚĆ_cb0f2404):
    WYNIK = {}
    for wiersz_wejścia in treść_WARTOŚĆ_cb0f2404.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', wiersz_wejścia)
        if 일치: WYNIK[일치.group(2).lower()] = 일치.group(1)
    return WYNIK


def suma_kontrolna(ścieżka_2):
    WARTOŚĆ = hashlib.sha256()
    with ścieżka_2.open('rb') as nazwa_pliku:
        for dane in iter(lambda: nazwa_pliku.read(1024 * 1024), b''): WARTOŚĆ.update(dane)
    return WARTOŚĆ.hexdigest()


class program_Launcher:
    def __init__(self, korzeń_WARTOŚĆ, Nazwa, metoda_tryb='gui', polecenie=Wykonaj_powłoka_polecenie):
        self.korzeń_WARTOŚĆ = Path(korzeń_WARTOŚĆ).resolve()
        self.Nazwa, self.metoda_tryb, self.polecenie = Nazwa, metoda_tryb, polecenie
        self.보관 = self.korzeń_WARTOŚĆ / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nazwa) or Nazwa in ('.', '..'):
            raise wykonanie_błąd('VM 이름은 문자·cyfra_WARTOŚĆ·공백·밑줄·괄호·마침표·하이픈만 사용할 identyfikator 있습니다.')
        if metoda_tryb not in ('gui', 'headless'): raise wykonanie_błąd('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ścieżka_2(self, węzeł_równorzędny_WARTOŚĆ):
        if Path(węzeł_równorzędny_WARTOŚĆ).is_absolute() or '..' in Path(węzeł_równorzędny_WARTOŚĆ).parts:
            raise wykonanie_błąd('잘못된 관리 ścieżka_2: ' + str(węzeł_równorzędny_WARTOŚĆ))
        WYNIK = self.보관
        for 부분 in ['.vbox'] + list(Path(węzeł_równorzędny_WARTOŚĆ).parts):
            if 부분 == '.vbox': WYNIK = self.보관
            else: WYNIK = WYNIK / 부분
            if WYNIK.is_symlink(): raise wykonanie_błąd('Połącz 경로는 사용하지 않습니다: ' + str(WYNIK))
        return WYNIK

    def Odczyt(self):
        ścieżka_2 = self.ścieżka_2('state.json')
        if not ścieżka_2.exists(): return None
        Stan_WARTOŚĆ = json.loads(ścieżka_2.read_text(encoding='utf-8'))
        if Stan_WARTOŚĆ.get('version') != 1 or Stan_WARTOŚĆ.get('name') != self.Nazwa:
            raise wykonanie_błąd('관리 상태의 VM Nazwa/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nazwa in ('uuid', 'owner'):
            if str(uuid.UUID(Stan_WARTOŚĆ[Nazwa])) != Stan_WARTOŚĆ[Nazwa]: raise wykonanie_błąd('잘못된 VM identyfikator_WARTOŚĆ')
        return Stan_WARTOŚĆ

    def Store_WARTOŚĆ(self, Stan_WARTOŚĆ):
        cel_WARTOŚĆ = self.ścieżka_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as nazwa_pliku:
            json.dump(Stan_WARTOŚĆ, nazwa_pliku, ensure_ascii=False, indent=2)
            nazwa_pliku.write('\n')
            임시 = nazwa_pliku.name
        os.replace(임시, str(cel_WARTOŚĆ))

    def msinfo32_exe(self, Stan_WARTOŚĆ, 등록됨, odzyskać_Stan=False):
        if Stan_WARTOŚĆ['uuid'] not in 등록됨:
            raise wykonanie_błąd('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = wartość_atrybutu(self.polecenie(['VBoxManage', 'showvminfo', Stan_WARTOŚĆ['uuid'], '--machinereadable']))
        pozycja = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.ścieżka_2('machines').resolve() not in pozycja.parents or msinfo32_exe.get('UUID') != Stan_WARTOŚĆ['uuid']:
            raise wykonanie_błąd('이 프로젝트의 VM Ustawienia ścieżka_2/UUID와 일치하지 않아 변경하지 않습니다.')
        pisak_WARTOŚĆ = self.polecenie(['VBoxManage', 'getextradata', Stan_WARTOŚĆ['uuid'], 'JKOROS/Owner']).strip()
        if pisak_WARTOŚĆ != 'Value: ' + Stan_WARTOŚĆ['owner']:
            if odzyskać_Stan and Stan_WARTOŚĆ.get('pending') and pisak_WARTOŚĆ == 'No value set!':
                self.polecenie(['VBoxManage', 'setextradata', Stan_WARTOŚĆ['uuid'], 'JKOROS/Owner', Stan_WARTOŚĆ['owner']])
            else:
                raise wykonanie_błąd('VM właściciel_WARTOŚĆ 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def czek_nośnik(self, Stan_WARTOŚĆ, msinfo32_exe):
        제어기들 = [WARTOŚĆ for Nazwa, WARTOŚĆ in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nazwa)]
        Zezwalaj_WARTOŚĆ = [str(self.ścieżka_2(WARTOŚĆ)) for WARTOŚĆ in Stan_WARTOŚĆ.get('media', [])]
        for Nazwa, WARTOŚĆ in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontroler) + r'-\d+-\d+', Nazwa) for kontroler in 제어기들):
                if WARTOŚĆ not in ('none', 'emptydrive') and WARTOŚĆ not in Zezwalaj_WARTOŚĆ:
                    raise wykonanie_błąd('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + WARTOŚĆ)

    def program_Stan(self):
        Stan_WARTOŚĆ = self.Odczyt()
        if Stan_WARTOŚĆ is None: return {'name': self.Nazwa, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Stan_WARTOŚĆ, 등록목록(self.polecenie(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Stan_WARTOŚĆ['name']), 'uuid': Stan_WARTOŚĆ['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.ścieżka_2(Stan_WARTOŚĆ['iso'])) if Stan_WARTOŚĆ.get('iso') else None,
                'serial_log': str(self.ścieżka_2(Stan_WARTOŚĆ['serial_log'])) if Stan_WARTOŚĆ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Wykonaj_polecenie(self):
        Stan_WARTOŚĆ = self.Odczyt()
        등록됨 = 등록목록(self.polecenie(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Stan_WARTOŚĆ is not None and Stan_WARTOŚĆ['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Stan_WARTOŚĆ, 등록됨, odzyskać_Stan=True)
            bieżący_towar = msinfo32_exe.get('VMState')
            if bieżący_towar == 'running':
                print('이미 Wykonaj_polecenie 중입니다. 재빌드·재시작하지 않습니다.')
                return self.program_Stan()
            self.czek_nośnik(Stan_WARTOŚĆ, msinfo32_exe)
            if bieżący_towar in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_WARTOŚĆ 상태를 버리지 않습니다.'.format(bieżący_towar))
                if bieżący_towar == 'paused':
                    self.polecenie(['VBoxManage', 'controlvm', Stan_WARTOŚĆ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Otwórz 전에 기존 기록도 보관한다.
                    if Stan_WARTOŚĆ.get('serial_log'):
                        원본 = self.ścieżka_2(Stan_WARTOŚĆ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ścieżka_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.polecenie(['VBoxManage', 'startvm', Stan_WARTOŚĆ['uuid'], '--type', self.metoda_tryb])
                return self.program_Stan()
            if bieżący_towar not in ('poweroff', 'aborted'):
                raise wykonanie_błąd('VM이 zmiana_tryb 중입니다 ({}). 작업이 끝난 BACK_WARTOŚĆ 다시 실행하세요.'.format(bieżący_towar))
        elif Stan_WARTOŚĆ is not None and not Stan_WARTOŚĆ.get('pending'):
            raise wykonanie_błąd('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Nazwa in 등록됨.values():
            raise wykonanie_błąd('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_WARTOŚĆ/Wykonaj_polecenie 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.polecenie(['make', '-C', str(self.korzeń_WARTOŚĆ / 'os'), 'iso']), end='')
        원본 = self.korzeń_WARTOŚĆ / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise wykonanie_błąd('rozruch_maszyny ISO가 생성되지 않았습니다.')
        nośnik_WARTOŚĆ = 'media/kernel-' + suma_kontrolna(원본) + '.iso'
        cel_WARTOŚĆ = self.ścieżka_2(nośnik_WARTOŚĆ)
        cel_WARTOŚĆ.parent.mkdir(exist_ok=True)
        if cel_WARTOŚĆ.exists():
            if suma_kontrolna(cel_WARTOŚĆ) != suma_kontrolna(원본): raise wykonanie_błąd('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(cel_WARTOŚĆ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(cel_WARTOŚĆ.parent)) as nazwa_pliku:
                shutil.copyfile(str(원본), nazwa_pliku.name)
                os.link(nazwa_pliku.name, str(cel_WARTOŚĆ))

        if Stan_WARTOŚĆ is None:
            Stan_WARTOŚĆ = {'version': 1, 'name': self.Nazwa, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_WARTOŚĆ(Stan_WARTOŚĆ)
        if msinfo32_exe is None:
            self.polecenie(['VBoxManage', 'createvm', '--name', Stan_WARTOŚĆ['name'], '--uuid', Stan_WARTOŚĆ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ścieżka_2('machines')), '--register'])
            self.polecenie(['VBoxManage', 'setextradata', Stan_WARTOŚĆ['uuid'], 'JKOROS/Owner', Stan_WARTOŚĆ['owner']])
        # BLD_System 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Stan_WARTOŚĆ, 등록목록(self.polecenie(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise wykonanie_błąd('BLD_System 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.czek_nośnik(Stan_WARTOŚĆ, msinfo32_exe)
        Stan_WARTOŚĆ['iso'] = nośnik_WARTOŚĆ
        if nośnik_WARTOŚĆ not in Stan_WARTOŚĆ['media']: Stan_WARTOŚĆ['media'].append(nośnik_WARTOŚĆ)
        Stan_WARTOŚĆ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_WARTOŚĆ = self.ścieżka_2(Stan_WARTOŚĆ['serial_log'])
        LOG_WARTOŚĆ.parent.mkdir(exist_ok=True)
        self.Store_WARTOŚĆ(Stan_WARTOŚĆ)
        self.polecenie(['VBoxManage', 'modifyvm', Stan_WARTOŚĆ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_WARTOŚĆ)])
        제어기들 = [WARTOŚĆ for Nazwa, WARTOŚĆ in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nazwa)]
        if 'JKOROS IDE' not in 제어기들:
            self.polecenie(['VBoxManage', 'storagectl', Stan_WARTOŚĆ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.polecenie(['VBoxManage', 'storageattach', Stan_WARTOŚĆ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(cel_WARTOŚĆ)])
        Stan_WARTOŚĆ['pending'] = False
        self.Store_WARTOŚĆ(Stan_WARTOŚĆ)
        self.polecenie(['VBoxManage', 'startvm', Stan_WARTOŚĆ['uuid'], '--type', self.metoda_tryb])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.program_Stan()


def Uruchom_2():
    analizować_WARTOŚĆ = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Wykonaj_polecenie 및 Stan_WARTOŚĆ zapytanie_WARTOŚĆ')
    analizować_WARTOŚĆ.add_argument('action', choices=['run', 'status'])
    parametr_argument = analizować_WARTOŚĆ.parse_args()
    Wykonaj_polecenie = program_Launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametr_argument.action == 'status':
        print(json.dumps(Wykonaj_polecenie.program_Stan(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise wykonanie_błąd('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise wykonanie_błąd('/dev/vboxdrv에 접근할 identyfikator 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/pozwolenie_WARTOŚĆ 변경은 하지 않습니다.')
    os.umask(0o077)
    Wykonaj_polecenie.ścieżka_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with Wykonaj_polecenie.ścieżka_2('lock').open('a') as blokada_WARTOŚĆ:
        try: fcntl.flock(blokada_WARTOŚĆ, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise wykonanie_błąd('다른 jkoros VirtualBox Wykonaj_polecenie 작업이 진행 중입니다.')
        print(json.dumps(Wykonaj_polecenie.Wykonaj_polecenie(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Uruchom_2()
    except (wykonanie_błąd, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as błąd:
        print('VBOX błąd: ' + str(błąd), file=sys.stderr)
        sys.exit(1)
