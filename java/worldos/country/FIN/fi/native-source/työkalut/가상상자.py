#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ohjelma_sovellusvalikko. 기존 VM/디스크/Store_ARVO 상태는 삭제하지 않는다."""
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


class suoritus_virhe(RuntimeError):
    pass


def Suorita_liittymä_komento(argumentit):
    ympäristö = dict(os.environ, LC_ALL='C')
    TULOS = subprocess.run([str(ARVO) for ARVO in argumentit], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=ympäristö, timeout=180)
    Sisältö_ARVO = TULOS.stdout.decode('utf-8', 'replace')
    if TULOS.returncode:
        raise suoritus_virhe('komento virhe_ARVO: ' + ' '.join(str(ARVO) for ARVO in argumentit) + '\n' + Sisältö_ARVO[-10000:])
    return Sisältö_ARVO


def määritteen_arvo(Sisältö_ARVO):
    TULOS = {}
    for syöterivi in Sisältö_ARVO.splitlines():
        if '=' not in syöterivi:
            continue
        Nimi, ARVO = syöterivi.split('=', 1)
        if Nimi.startswith('"'):
            Nimi = json.loads(Nimi)
        if ARVO.startswith('"'):
            try:
                lukea_ARVO, 끝 = json.JSONDecoder().raw_decode(ARVO)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ARVO): ARVO = lukea_ARVO
            except ValueError:
                raise suoritus_virhe('VirtualBox määritteen_arvo muoto_ARVO VIRHE: ' + syöterivi)
        TULOS[Nimi] = ARVO
    return TULOS


def 등록목록(Sisältö_ARVO):
    TULOS = {}
    for syöterivi in Sisältö_ARVO.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', syöterivi)
        if 일치: TULOS[일치.group(2).lower()] = 일치.group(1)
    return TULOS


def tarkistussumma(polku_2):
    ARVO = hashlib.sha256()
    with polku_2.open('rb') as tiedoston_nimi:
        for data in iter(lambda: tiedoston_nimi.read(1024 * 1024), b''): ARVO.update(data)
    return ARVO.hexdigest()


class ohjelma_sovellusvalikko:
    def __init__(self, juuri_ARVO, Nimi, menetelmä_tila='gui', komento=Suorita_liittymä_komento):
        self.juuri_ARVO = Path(juuri_ARVO).resolve()
        self.Nimi, self.menetelmä_tila, self.komento = Nimi, menetelmä_tila, komento
        self.보관 = self.juuri_ARVO / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nimi) or Nimi in ('.', '..'):
            raise suoritus_virhe('VM 이름은 문자·numero_ARVO·공백·밑줄·괄호·마침표·하이픈만 사용할 numero 있습니다.')
        if menetelmä_tila not in ('gui', 'headless'): raise suoritus_virhe('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def polku_2(self, vertaissolmu_ARVO):
        if Path(vertaissolmu_ARVO).is_absolute() or '..' in Path(vertaissolmu_ARVO).parts:
            raise suoritus_virhe('잘못된 관리 polku_2: ' + str(vertaissolmu_ARVO))
        TULOS = self.보관
        for 부분 in ['.vbox'] + list(Path(vertaissolmu_ARVO).parts):
            if 부분 == '.vbox': TULOS = self.보관
            else: TULOS = TULOS / 부분
            if TULOS.is_symlink(): raise suoritus_virhe('Yhdistä 경로는 사용하지 않습니다: ' + str(TULOS))
        return TULOS

    def Luku(self):
        polku_2 = self.polku_2('state.json')
        if not polku_2.exists(): return None
        Tila_ARVO = json.loads(polku_2.read_text(encoding='utf-8'))
        if Tila_ARVO.get('version') != 1 or Tila_ARVO.get('name') != self.Nimi:
            raise suoritus_virhe('관리 상태의 VM Nimi/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nimi in ('uuid', 'owner'):
            if str(uuid.UUID(Tila_ARVO[Nimi])) != Tila_ARVO[Nimi]: raise suoritus_virhe('잘못된 VM tunniste_ARVO')
        return Tila_ARVO

    def Store_ARVO(self, Tila_ARVO):
        kohde_ARVO = self.polku_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as tiedoston_nimi:
            json.dump(Tila_ARVO, tiedoston_nimi, ensure_ascii=False, indent=2)
            tiedoston_nimi.write('\n')
            임시 = tiedoston_nimi.name
        os.replace(임시, str(kohde_ARVO))

    def msinfo32_exe(self, Tila_ARVO, 등록됨, pelastaa_Tila=False):
        if Tila_ARVO['uuid'] not in 등록됨:
            raise suoritus_virhe('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = määritteen_arvo(self.komento(['VBoxManage', 'showvminfo', Tila_ARVO['uuid'], '--machinereadable']))
        paikka = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.polku_2('machines').resolve() not in paikka.parents or msinfo32_exe.get('UUID') != Tila_ARVO['uuid']:
            raise suoritus_virhe('이 프로젝트의 VM Asetukset polku_2/UUID와 일치하지 않아 변경하지 않습니다.')
        merkintä_ARVO = self.komento(['VBoxManage', 'getextradata', Tila_ARVO['uuid'], 'JKOROS/Owner']).strip()
        if merkintä_ARVO != 'Value: ' + Tila_ARVO['owner']:
            if pelastaa_Tila and Tila_ARVO.get('pending') and merkintä_ARVO == 'No value set!':
                self.komento(['VBoxManage', 'setextradata', Tila_ARVO['uuid'], 'JKOROS/Owner', Tila_ARVO['owner']])
            else:
                raise suoritus_virhe('VM omistaja_ARVO 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def sekki_tietoväline(self, Tila_ARVO, msinfo32_exe):
        제어기들 = [ARVO for Nimi, ARVO in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nimi)]
        Salli_ARVO = [str(self.polku_2(ARVO)) for ARVO in Tila_ARVO.get('media', [])]
        for Nimi, ARVO in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(ohjain_8bff480f) + r'-\d+-\d+', Nimi) for ohjain_8bff480f in 제어기들):
                if ARVO not in ('none', 'emptydrive') and ARVO not in Salli_ARVO:
                    raise suoritus_virhe('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ARVO)

    def näyttää_Tila(self):
        Tila_ARVO = self.Luku()
        if Tila_ARVO is None: return {'name': self.Nimi, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Tila_ARVO, 등록목록(self.komento(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Tila_ARVO['name']), 'uuid': Tila_ARVO['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.polku_2(Tila_ARVO['iso'])) if Tila_ARVO.get('iso') else None,
                'serial_log': str(self.polku_2(Tila_ARVO['serial_log'])) if Tila_ARVO.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Suorita_komento(self):
        Tila_ARVO = self.Luku()
        등록됨 = 등록목록(self.komento(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Tila_ARVO is not None and Tila_ARVO['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Tila_ARVO, 등록됨, pelastaa_Tila=True)
            nykyinen_kohde = msinfo32_exe.get('VMState')
            if nykyinen_kohde == 'running':
                print('이미 Suorita_komento 중입니다. 재빌드·재시작하지 않습니다.')
                return self.näyttää_Tila()
            self.sekki_tietoväline(Tila_ARVO, msinfo32_exe)
            if nykyinen_kohde in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_ARVO 상태를 버리지 않습니다.'.format(nykyinen_kohde))
                if nykyinen_kohde == 'paused':
                    self.komento(['VBoxManage', 'controlvm', Tila_ARVO['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 yrittää_uudelleen_ARVO Avaa 전에 기존 기록도 보관한다.
                    if Tila_ARVO.get('serial_log'):
                        원본 = self.polku_2(Tila_ARVO['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.polku_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.komento(['VBoxManage', 'startvm', Tila_ARVO['uuid'], '--type', self.menetelmä_tila])
                return self.näyttää_Tila()
            if nykyinen_kohde not in ('poweroff', 'aborted'):
                raise suoritus_virhe('VM이 MUUTA_tila 중입니다 ({}). 작업이 끝난 BACK_ARVO yrittää_uudelleen_ARVO 실행하세요.'.format(nykyinen_kohde))
        elif Tila_ARVO is not None and not Tila_ARVO.get('pending'):
            raise suoritus_virhe('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 yrittää_uudelleen_ARVO 등록하세요.')
        elif self.Nimi in 등록됨.values():
            raise suoritus_virhe('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_ARVO/Suorita_komento 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.komento(['make', '-C', str(self.juuri_ARVO / 'os'), 'iso']), end='')
        원본 = self.juuri_ARVO / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise suoritus_virhe('koneen_käynnistys ISO가 생성되지 않았습니다.')
        tietoväline_ARVO = 'media/kernel-' + tarkistussumma(원본) + '.iso'
        kohde_ARVO = self.polku_2(tietoväline_ARVO)
        kohde_ARVO.parent.mkdir(exist_ok=True)
        if kohde_ARVO.exists():
            if tarkistussumma(kohde_ARVO) != tarkistussumma(원본): raise suoritus_virhe('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(kohde_ARVO))
        else:
            with tempfile.NamedTemporaryFile(dir=str(kohde_ARVO.parent)) as tiedoston_nimi:
                shutil.copyfile(str(원본), tiedoston_nimi.name)
                os.link(tiedoston_nimi.name, str(kohde_ARVO))

        if Tila_ARVO is None:
            Tila_ARVO = {'version': 1, 'name': self.Nimi, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_ARVO(Tila_ARVO)
        if msinfo32_exe is None:
            self.komento(['VBoxManage', 'createvm', '--name', Tila_ARVO['name'], '--uuid', Tila_ARVO['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.polku_2('machines')), '--register'])
            self.komento(['VBoxManage', 'setextradata', Tila_ARVO['uuid'], 'JKOROS/Owner', Tila_ARVO['owner']])
        # kääntää_Järjestelmä 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Tila_ARVO, 등록목록(self.komento(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise suoritus_virhe('kääntää_Järjestelmä 중 VM 상태가 바뀌었습니다. yrittää_uudelleen_ARVO make vbox를 실행하세요.')
        self.sekki_tietoväline(Tila_ARVO, msinfo32_exe)
        Tila_ARVO['iso'] = tietoväline_ARVO
        if tietoväline_ARVO not in Tila_ARVO['media']: Tila_ARVO['media'].append(tietoväline_ARVO)
        Tila_ARVO['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_ARVO = self.polku_2(Tila_ARVO['serial_log'])
        LOG_ARVO.parent.mkdir(exist_ok=True)
        self.Store_ARVO(Tila_ARVO)
        self.komento(['VBoxManage', 'modifyvm', Tila_ARVO['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_ARVO)])
        제어기들 = [ARVO for Nimi, ARVO in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nimi)]
        if 'JKOROS IDE' not in 제어기들:
            self.komento(['VBoxManage', 'storagectl', Tila_ARVO['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.komento(['VBoxManage', 'storageattach', Tila_ARVO['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(kohde_ARVO)])
        Tila_ARVO['pending'] = False
        self.Store_ARVO(Tila_ARVO)
        self.komento(['VBoxManage', 'startvm', Tila_ARVO['uuid'], '--type', self.menetelmä_tila])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.näyttää_Tila()


def Suorita_2():
    jäsentää_ARVO = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Suorita_komento 및 Tila_ARVO kysely_ARVO')
    jäsentää_ARVO.add_argument('action', choices=['run', 'status'])
    parametri_argumentti = jäsentää_ARVO.parse_args()
    Suorita_komento = ohjelma_sovellusvalikko(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametri_argumentti.action == 'status':
        print(json.dumps(Suorita_komento.näyttää_Tila(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise suoritus_virhe('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise suoritus_virhe('/dev/vboxdrv에 접근할 numero 없습니다. isäntä 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/lupa_ARVO 변경은 하지 않습니다.')
    os.umask(0o077)
    Suorita_komento.polku_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with Suorita_komento.polku_2('lock').open('a') as lukita_ARVO:
        try: fcntl.flock(lukita_ARVO, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise suoritus_virhe('다른 jkoros VirtualBox Suorita_komento 작업이 진행 중입니다.')
        print(json.dumps(Suorita_komento.Suorita_komento(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Suorita_2()
    except (suoritus_virhe, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as VIRHE:
        print('VBOX VIRHE: ' + str(VIRHE), file=sys.stderr)
        sys.exit(1)
