#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_ecrane_de_lansare. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


class executare_eroare(RuntimeError):
    pass


def executa_shell_comandă(Argumente):
    환경 = dict(os.environ, LC_ALL='C')
    KR = subprocess.run([str(VALUE) for VALUE in Argumente], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Conținut_VALUE = KR.stdout.decode('utf-8', 'replace')
    if KR.returncode:
        raise executare_eroare('Comandă eroare_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumente) + '\n' + Conținut_VALUE[-10000:])
    return Conținut_VALUE


def atribut_VALUE(Conținut_VALUE):
    KR = {}
    for Linie in Conținut_VALUE.splitlines():
        if '=' not in Linie:
            continue
        Nume, VALUE = Linie.split('=', 1)
        if Nume.startswith('"'):
            Nume = json.loads(Nume)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise executare_eroare('VirtualBox atribut_VALUE format_VALUE eroare: ' + Linie)
        KR[Nume] = VALUE
    return KR


def 등록목록(Conținut_VALUE):
    KR = {}
    for Linie in Conținut_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Linie)
        if 일치: KR[일치.group(2).lower()] = 일치.group(1)
    return KR


def sumă_de_verificare(Cale):
    VALUE = hashlib.sha256()
    with Cale.open('rb') as Fișier:
        for date in iter(lambda: Fișier.read(1024 * 1024), b''): VALUE.update(date)
    return VALUE.hexdigest()


class program_ecrane_de_lansare:
    def __init__(self, rădăcină_VALUE, Nume, metodă_mod='gui', Comandă=executa_shell_comandă):
        self.rădăcină_VALUE = Path(rădăcină_VALUE).resolve()
        self.Nume, self.metodă_mod, self.Comandă = Nume, metodă_mod, Comandă
        self.보관 = self.rădăcină_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nume) or Nume in ('.', '..'):
            raise executare_eroare('VM 이름은 문자·cifră_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metodă_mod not in ('gui', 'headless'): raise executare_eroare('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Cale(self, pereche_VALUE):
        if Path(pereche_VALUE).is_absolute() or '..' in Path(pereche_VALUE).parts:
            raise executare_eroare('잘못된 관리 Cale: ' + str(pereche_VALUE))
        KR = self.보관
        for 부분 in ['.vbox'] + list(Path(pereche_VALUE).parts):
            if 부분 == '.vbox': KR = self.보관
            else: KR = KR / 부분
            if KR.is_symlink(): raise executare_eroare('Conectează 경로는 사용하지 않습니다: ' + str(KR))
        return KR

    def Citire(self):
        Cale = self.Cale('state.json')
        if not Cale.exists(): return None
        Stare_VALUE = json.loads(Cale.read_text(encoding='utf-8'))
        if Stare_VALUE.get('version') != 1 or Stare_VALUE.get('name') != self.Nume:
            raise executare_eroare('관리 상태의 VM Nume/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nume in ('uuid', 'owner'):
            if str(uuid.UUID(Stare_VALUE[Nume])) != Stare_VALUE[Nume]: raise executare_eroare('잘못된 VM identificator_VALUE')
        return Stare_VALUE

    def Store_VALUE(self, Stare_VALUE):
        destinație_VALUE = self.Cale('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fișier:
            json.dump(Stare_VALUE, Fișier, ensure_ascii=False, indent=2)
            Fișier.write('\n')
            임시 = Fișier.name
        os.replace(임시, str(destinație_VALUE))

    def msinfo32_exe(self, Stare_VALUE, 등록됨, recupera_Stare=False):
        if Stare_VALUE['uuid'] not in 등록됨:
            raise executare_eroare('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribut_VALUE(self.Comandă(['VBoxManage', 'showvminfo', Stare_VALUE['uuid'], '--machinereadable']))
        Poziție = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Cale('machines').resolve() not in Poziție.parents or msinfo32_exe.get('UUID') != Stare_VALUE['uuid']:
            raise executare_eroare('이 프로젝트의 VM Setări Cale/UUID와 일치하지 않아 변경하지 않습니다.')
        marcaj_VALUE = self.Comandă(['VBoxManage', 'getextradata', Stare_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if marcaj_VALUE != 'Value: ' + Stare_VALUE['owner']:
            if recupera_Stare and Stare_VALUE.get('pending') and marcaj_VALUE == 'No value set!':
                self.Comandă(['VBoxManage', 'setextradata', Stare_VALUE['uuid'], 'JKOROS/Owner', Stare_VALUE['owner']])
            else:
                raise executare_eroare('VM proprietar_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def verifica_suport_fizic(self, Stare_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Nume, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nume)]
        permite_VALUE = [str(self.Cale(VALUE)) for VALUE in Stare_VALUE.get('media', [])]
        for Nume, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Nume) for 제어기 in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in permite_VALUE:
                    raise executare_eroare('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def afișa_Stare(self):
        Stare_VALUE = self.Citire()
        if Stare_VALUE is None: return {'name': self.Nume, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Stare_VALUE, 등록목록(self.Comandă(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Stare_VALUE['name']), 'uuid': Stare_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Cale(Stare_VALUE['iso'])) if Stare_VALUE.get('iso') else None,
                'serial_log': str(self.Cale(Stare_VALUE['serial_log'])) if Stare_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def executa_comandă(self):
        Stare_VALUE = self.Citire()
        등록됨 = 등록목록(self.Comandă(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Stare_VALUE is not None and Stare_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Stare_VALUE, 등록됨, recupera_Stare=True)
            curent_element = msinfo32_exe.get('VMState')
            if curent_element == 'running':
                print('이미 executa_comandă 중입니다. 재빌드·재시작하지 않습니다.')
                return self.afișa_Stare()
            self.verifica_suport_fizic(Stare_VALUE, msinfo32_exe)
            if curent_element in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(curent_element))
                if curent_element == 'paused':
                    self.Comandă(['VBoxManage', 'controlvm', Stare_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 reîncerca_VALUE Deschide 전에 기존 기록도 보관한다.
                    if Stare_VALUE.get('serial_log'):
                        원본 = self.Cale(Stare_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Cale('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Comandă(['VBoxManage', 'startvm', Stare_VALUE['uuid'], '--type', self.metodă_mod])
                return self.afișa_Stare()
            if curent_element not in ('poweroff', 'aborted'):
                raise executare_eroare('VM이 SWITCH_mod 중입니다 ({}). 작업이 끝난 ÎNAPOI_VALUE reîncerca_VALUE 실행하세요.'.format(curent_element))
        elif Stare_VALUE is not None and not Stare_VALUE.get('pending'):
            raise executare_eroare('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 reîncerca_VALUE 등록하세요.')
        elif self.Nume in 등록됨.values():
            raise executare_eroare('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/executa_comandă 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Comandă(['make', '-C', str(self.rădăcină_VALUE / 'os'), 'iso']), end='')
        원본 = self.rădăcină_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise executare_eroare('부팅 ISO가 생성되지 않았습니다.')
        suport_fizic_VALUE = 'media/kernel-' + sumă_de_verificare(원본) + '.iso'
        destinație_VALUE = self.Cale(suport_fizic_VALUE)
        destinație_VALUE.parent.mkdir(exist_ok=True)
        if destinație_VALUE.exists():
            if sumă_de_verificare(destinație_VALUE) != sumă_de_verificare(원본): raise executare_eroare('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destinație_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destinație_VALUE.parent)) as Fișier:
                shutil.copyfile(str(원본), Fișier.name)
                os.link(Fișier.name, str(destinație_VALUE))

        if Stare_VALUE is None:
            Stare_VALUE = {'version': 1, 'name': self.Nume, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Stare_VALUE)
        if msinfo32_exe is None:
            self.Comandă(['VBoxManage', 'createvm', '--name', Stare_VALUE['name'], '--uuid', Stare_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Cale('machines')), '--register'])
            self.Comandă(['VBoxManage', 'setextradata', Stare_VALUE['uuid'], 'JKOROS/Owner', Stare_VALUE['owner']])
        # generare_sistem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Stare_VALUE, 등록목록(self.Comandă(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise executare_eroare('generare_sistem 중 VM 상태가 바뀌었습니다. reîncerca_VALUE make vbox를 실행하세요.')
        self.verifica_suport_fizic(Stare_VALUE, msinfo32_exe)
        Stare_VALUE['iso'] = suport_fizic_VALUE
        if suport_fizic_VALUE not in Stare_VALUE['media']: Stare_VALUE['media'].append(suport_fizic_VALUE)
        Stare_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Cale(Stare_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Stare_VALUE)
        self.Comandă(['VBoxManage', 'modifyvm', Stare_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Nume, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nume)]
        if 'JKOROS IDE' not in 제어기들:
            self.Comandă(['VBoxManage', 'storagectl', Stare_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Comandă(['VBoxManage', 'storageattach', Stare_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destinație_VALUE)])
        Stare_VALUE['pending'] = False
        self.Store_VALUE(Stare_VALUE)
        self.Comandă(['VBoxManage', 'startvm', Stare_VALUE['uuid'], '--type', self.metodă_mod])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.afișa_Stare()


def Pornește():
    analiza_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox executa_comandă 및 Stare_VALUE interoga_VALUE')
    analiza_VALUE.add_argument('action', choices=['run', 'status'])
    parametru_argument = analiza_VALUE.parse_args()
    executa_comandă = program_ecrane_de_lansare(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametru_argument.action == 'status':
        print(json.dumps(executa_comandă.afișa_Stare(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise executare_eroare('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise executare_eroare('/dev/vboxdrv에 접근할 수 없습니다. gazdă 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/permisiune_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    executa_comandă.Cale('lock').parent.mkdir(parents=True, exist_ok=True)
    with executa_comandă.Cale('lock').open('a') as blocare_VALUE:
        try: fcntl.flock(blocare_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise executare_eroare('다른 jkoros VirtualBox executa_comandă 작업이 진행 중입니다.')
        print(json.dumps(executa_comandă.executa_comandă(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Pornește()
    except (executare_eroare, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as eroare:
        print('VBOX eroare: ' + str(eroare), file=sys.stderr)
        sys.exit(1)
