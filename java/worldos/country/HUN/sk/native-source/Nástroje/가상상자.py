#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_spúšťač. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def 명령실행(Argumenty):
    환경 = dict(os.environ, LC_ALL='C')
    KR = subprocess.run([str(VALUE) for VALUE in Argumenty], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    obsah_VALUE = KR.stdout.decode('utf-8', 'replace')
    if KR.returncode:
        raise 실행오류('Príkaz zlyhanie_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumenty) + '\n' + obsah_VALUE[-10000:])
    return obsah_VALUE


def atribút_VALUE(obsah_VALUE):
    KR = {}
    for riadok in obsah_VALUE.splitlines():
        if '=' not in riadok:
            continue
        Názov, VALUE = riadok.split('=', 1)
        if Názov.startswith('"'):
            Názov = json.loads(Názov)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribút_VALUE formát_VALUE chyba: ' + riadok)
        KR[Názov] = VALUE
    return KR


def 등록목록(obsah_VALUE):
    KR = {}
    for riadok in obsah_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', riadok)
        if 일치: KR[일치.group(2).lower()] = 일치.group(1)
    return KR


def kontrolný_súčet(Cesta):
    VALUE = hashlib.sha256()
    with Cesta.open('rb') as Súbor:
        for údaje in iter(lambda: Súbor.read(1024 * 1024), b''): VALUE.update(údaje)
    return VALUE.hexdigest()


class program_spúšťač:
    def __init__(self, koreň_VALUE, Názov, metóda_MODE='gui', Príkaz=명령실행):
        self.koreň_VALUE = Path(koreň_VALUE).resolve()
        self.Názov, self.metóda_MODE, self.Príkaz = Názov, metóda_MODE, Príkaz
        self.보관 = self.koreň_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Názov) or Názov in ('.', '..'):
            raise 실행오류('VM 이름은 문자·číslica_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metóda_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Cesta(self, partnerský_uzol_VALUE):
        if Path(partnerský_uzol_VALUE).is_absolute() or '..' in Path(partnerský_uzol_VALUE).parts:
            raise 실행오류('잘못된 관리 Cesta: ' + str(partnerský_uzol_VALUE))
        KR = self.보관
        for 부분 in ['.vbox'] + list(Path(partnerský_uzol_VALUE).parts):
            if 부분 == '.vbox': KR = self.보관
            else: KR = KR / 부분
            if KR.is_symlink(): raise 실행오류('Pripojiť 경로는 사용하지 않습니다: ' + str(KR))
        return KR

    def Čítanie(self):
        Cesta = self.Cesta('state.json')
        if not Cesta.exists(): return None
        Stav_VALUE = json.loads(Cesta.read_text(encoding='utf-8'))
        if Stav_VALUE.get('version') != 1 or Stav_VALUE.get('name') != self.Názov:
            raise 실행오류('관리 상태의 VM Názov/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Názov in ('uuid', 'owner'):
            if str(uuid.UUID(Stav_VALUE[Názov])) != Stav_VALUE[Názov]: raise 실행오류('잘못된 VM identifikátor_VALUE')
        return Stav_VALUE

    def Store_VALUE(self, Stav_VALUE):
        cieľ_VALUE = self.Cesta('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Súbor:
            json.dump(Stav_VALUE, Súbor, ensure_ascii=False, indent=2)
            Súbor.write('\n')
            임시 = Súbor.name
        os.replace(임시, str(cieľ_VALUE))

    def Systémové_informácie(self, Stav_VALUE, 등록됨, obnoviť_Stav=False):
        if Stav_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Systémové_informácie = atribút_VALUE(self.Príkaz(['VBoxManage', 'showvminfo', Stav_VALUE['uuid'], '--machinereadable']))
        Pozícia = Path(Systémové_informácie.get('CfgFile', '')).resolve()
        if self.Cesta('machines').resolve() not in Pozícia.parents or Systémové_informácie.get('UUID') != Stav_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Nastavenia Cesta/UUID와 일치하지 않아 변경하지 않습니다.')
        fixka_VALUE = self.Príkaz(['VBoxManage', 'getextradata', Stav_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if fixka_VALUE != 'Value: ' + Stav_VALUE['owner']:
            if obnoviť_Stav and Stav_VALUE.get('pending') and fixka_VALUE == 'No value set!':
                self.Príkaz(['VBoxManage', 'setextradata', Stav_VALUE['uuid'], 'JKOROS/Owner', Stav_VALUE['owner']])
            else:
                raise 실행오류('VM vlastník_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return Systémové_informácie

    def skontrolovať_médiá(self, Stav_VALUE, Systémové_informácie):
        제어기들 = [VALUE for Názov, VALUE in Systémové_informácie.items() if re.fullmatch(r'storagecontrollername\d+', Názov)]
        Povoliť_VALUE = [str(self.Cesta(VALUE)) for VALUE in Stav_VALUE.get('media', [])]
        for Názov, VALUE in Systémové_informácie.items():
            if any(re.fullmatch(re.escape(ovládač) + r'-\d+-\d+', Názov) for ovládač in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Povoliť_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def zobraziť_Stav(self):
        Stav_VALUE = self.Čítanie()
        if Stav_VALUE is None: return {'name': self.Názov, 'state': 'not-created'}
        Systémové_informácie = self.Systémové_informácie(Stav_VALUE, 등록목록(self.Príkaz(['VBoxManage', 'list', 'vms'])))
        return {'name': Systémové_informácie.get('name', Stav_VALUE['name']), 'uuid': Stav_VALUE['uuid'], 'state': Systémové_informácie.get('VMState'),
                'iso': str(self.Cesta(Stav_VALUE['iso'])) if Stav_VALUE.get('iso') else None,
                'serial_log': str(self.Cesta(Stav_VALUE['serial_log'])) if Stav_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Vykonať_príkaz(self):
        Stav_VALUE = self.Čítanie()
        등록됨 = 등록목록(self.Príkaz(['VBoxManage', 'list', 'vms']))
        Systémové_informácie = None
        if Stav_VALUE is not None and Stav_VALUE['uuid'] in 등록됨:
            Systémové_informácie = self.Systémové_informácie(Stav_VALUE, 등록됨, obnoviť_Stav=True)
            v_termíne_splatnosti_položka = Systémové_informácie.get('VMState')
            if v_termíne_splatnosti_položka == 'running':
                print('이미 Vykonať_príkaz 중입니다. 재빌드·재시작하지 않습니다.')
                return self.zobraziť_Stav()
            self.skontrolovať_médiá(Stav_VALUE, Systémové_informácie)
            if v_termíne_splatnosti_položka in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(v_termíne_splatnosti_položka))
                if v_termíne_splatnosti_položka == 'paused':
                    self.Príkaz(['VBoxManage', 'controlvm', Stav_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 skúsiť_znova_VALUE Otvoriť 전에 기존 기록도 보관한다.
                    if Stav_VALUE.get('serial_log'):
                        원본 = self.Cesta(Stav_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Cesta('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Príkaz(['VBoxManage', 'startvm', Stav_VALUE['uuid'], '--type', self.metóda_MODE])
                return self.zobraziť_Stav()
            if v_termíne_splatnosti_položka not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 BACK_VALUE skúsiť_znova_VALUE 실행하세요.'.format(v_termíne_splatnosti_položka))
        elif Stav_VALUE is not None and not Stav_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 skúsiť_znova_VALUE 등록하세요.')
        elif self.Názov in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Vykonať_príkaz 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Príkaz(['make', '-C', str(self.koreň_VALUE / 'os'), 'iso']), end='')
        원본 = self.koreň_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        médiá_VALUE = 'media/kernel-' + kontrolný_súčet(원본) + '.iso'
        cieľ_VALUE = self.Cesta(médiá_VALUE)
        cieľ_VALUE.parent.mkdir(exist_ok=True)
        if cieľ_VALUE.exists():
            if kontrolný_súčet(cieľ_VALUE) != kontrolný_súčet(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(cieľ_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(cieľ_VALUE.parent)) as Súbor:
                shutil.copyfile(str(원본), Súbor.name)
                os.link(Súbor.name, str(cieľ_VALUE))

        if Stav_VALUE is None:
            Stav_VALUE = {'version': 1, 'name': self.Názov, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Stav_VALUE)
        if Systémové_informácie is None:
            self.Príkaz(['VBoxManage', 'createvm', '--name', Stav_VALUE['name'], '--uuid', Stav_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Cesta('machines')), '--register'])
            self.Príkaz(['VBoxManage', 'setextradata', Stav_VALUE['uuid'], 'JKOROS/Owner', Stav_VALUE['owner']])
        # zostava_systém 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Systémové_informácie = self.Systémové_informácie(Stav_VALUE, 등록목록(self.Príkaz(['VBoxManage', 'list', 'vms'])))
        if Systémové_informácie.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('zostava_systém 중 VM 상태가 바뀌었습니다. skúsiť_znova_VALUE make vbox를 실행하세요.')
        self.skontrolovať_médiá(Stav_VALUE, Systémové_informácie)
        Stav_VALUE['iso'] = médiá_VALUE
        if médiá_VALUE not in Stav_VALUE['media']: Stav_VALUE['media'].append(médiá_VALUE)
        Stav_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Cesta(Stav_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Stav_VALUE)
        self.Príkaz(['VBoxManage', 'modifyvm', Stav_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Názov, VALUE in Systémové_informácie.items() if re.fullmatch(r'storagecontrollername\d+', Názov)]
        if 'JKOROS IDE' not in 제어기들:
            self.Príkaz(['VBoxManage', 'storagectl', Stav_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Príkaz(['VBoxManage', 'storageattach', Stav_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(cieľ_VALUE)])
        Stav_VALUE['pending'] = False
        self.Store_VALUE(Stav_VALUE)
        self.Príkaz(['VBoxManage', 'startvm', Stav_VALUE['uuid'], '--type', self.metóda_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.zobraziť_Stav()


def Spustiť_2():
    analyzovať_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Vykonať_príkaz 및 Stav_VALUE dotaz_VALUE')
    analyzovať_VALUE.add_argument('action', choices=['run', 'status'])
    parameter_argument = analyzovať_VALUE.parse_args()
    Vykonať_príkaz = program_spúšťač(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(Vykonať_príkaz.zobraziť_Stav(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. hostiteľ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/povolenie_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Vykonať_príkaz.Cesta('lock').parent.mkdir(parents=True, exist_ok=True)
    with Vykonať_príkaz.Cesta('lock').open('a') as zámok_VALUE:
        try: fcntl.flock(zámok_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Vykonať_príkaz 작업이 진행 중입니다.')
        print(json.dumps(Vykonať_príkaz.Vykonať_príkaz(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Spustiť_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as chyba:
        print('VBOX chyba: ' + str(chyba), file=sys.stderr)
        sys.exit(1)
