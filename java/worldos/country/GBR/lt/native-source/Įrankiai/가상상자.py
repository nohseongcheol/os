#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programa_programų_skydelis. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Vykdyti_apvalkalas_komanda(Argumentai):
    환경 = dict(os.environ, LC_ALL='C')
    REZULTATAS = subprocess.run([str(VALUE) for VALUE in Argumentai], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Turinys_VALUE = REZULTATAS.stdout.decode('utf-8', 'replace')
    if REZULTATAS.returncode:
        raise 실행오류('Komanda triktis_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumentai) + '\n' + Turinys_VALUE[-10000:])
    return Turinys_VALUE


def atributas_VALUE(Turinys_VALUE):
    REZULTATAS = {}
    for Eilutė in Turinys_VALUE.splitlines():
        if '=' not in Eilutė:
            continue
        Pavadinimas_2, VALUE = Eilutė.split('=', 1)
        if Pavadinimas_2.startswith('"'):
            Pavadinimas_2 = json.loads(Pavadinimas_2)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atributas_VALUE formatas_VALUE KLAIDA: ' + Eilutė)
        REZULTATAS[Pavadinimas_2] = VALUE
    return REZULTATAS


def 등록목록(Turinys_VALUE):
    REZULTATAS = {}
    for Eilutė in Turinys_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Eilutė)
        if 일치: REZULTATAS[일치.group(2).lower()] = 일치.group(1)
    return REZULTATAS


def kontrolinė_suma(KELIAS):
    VALUE = hashlib.sha256()
    with KELIAS.open('rb') as Failas:
        for duomenys in iter(lambda: Failas.read(1024 * 1024), b''): VALUE.update(duomenys)
    return VALUE.hexdigest()


class programa_programų_skydelis:
    def __init__(self, šaknis_VALUE, Pavadinimas_2, metodas_MODE='gui', Komanda=Vykdyti_apvalkalas_komanda):
        self.šaknis_VALUE = Path(šaknis_VALUE).resolve()
        self.Pavadinimas_2, self.metodas_MODE, self.Komanda = Pavadinimas_2, metodas_MODE, Komanda
        self.보관 = self.šaknis_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Pavadinimas_2) or Pavadinimas_2 in ('.', '..'):
            raise 실행오류('VM 이름은 문자·skaitmuo_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 numeris 있습니다.')
        if metodas_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def KELIAS(self, lygiavertis_mazgas_VALUE):
        if Path(lygiavertis_mazgas_VALUE).is_absolute() or '..' in Path(lygiavertis_mazgas_VALUE).parts:
            raise 실행오류('잘못된 관리 KELIAS: ' + str(lygiavertis_mazgas_VALUE))
        REZULTATAS = self.보관
        for 부분 in ['.vbox'] + list(Path(lygiavertis_mazgas_VALUE).parts):
            if 부분 == '.vbox': REZULTATAS = self.보관
            else: REZULTATAS = REZULTATAS / 부분
            if REZULTATAS.is_symlink(): raise 실행오류('Prisijungti 경로는 사용하지 않습니다: ' + str(REZULTATAS))
        return REZULTATAS

    def Skaitymas(self):
        KELIAS = self.KELIAS('state.json')
        if not KELIAS.exists(): return None
        Būsena_VALUE = json.loads(KELIAS.read_text(encoding='utf-8'))
        if Būsena_VALUE.get('version') != 1 or Būsena_VALUE.get('name') != self.Pavadinimas_2:
            raise 실행오류('관리 상태의 VM Pavadinimas_2/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Pavadinimas_2 in ('uuid', 'owner'):
            if str(uuid.UUID(Būsena_VALUE[Pavadinimas_2])) != Būsena_VALUE[Pavadinimas_2]: raise 실행오류('잘못된 VM identifikatorius_VALUE')
        return Būsena_VALUE

    def Store_VALUE(self, Būsena_VALUE):
        vieta_VALUE = self.KELIAS('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Failas:
            json.dump(Būsena_VALUE, Failas, ensure_ascii=False, indent=2)
            Failas.write('\n')
            임시 = Failas.name
        os.replace(임시, str(vieta_VALUE))

    def msinfo32_exe(self, Būsena_VALUE, 등록됨, atkurti_Būsena=False):
        if Būsena_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atributas_VALUE(self.Komanda(['VBoxManage', 'showvminfo', Būsena_VALUE['uuid'], '--machinereadable']))
        Pozicija = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.KELIAS('machines').resolve() not in Pozicija.parents or msinfo32_exe.get('UUID') != Būsena_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Nustatymai KELIAS/UUID와 일치하지 않아 변경하지 않습니다.')
        žymeklis_VALUE = self.Komanda(['VBoxManage', 'getextradata', Būsena_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if žymeklis_VALUE != 'Value: ' + Būsena_VALUE['owner']:
            if atkurti_Būsena and Būsena_VALUE.get('pending') and žymeklis_VALUE == 'No value set!':
                self.Komanda(['VBoxManage', 'setextradata', Būsena_VALUE['uuid'], 'JKOROS/Owner', Būsena_VALUE['owner']])
            else:
                raise 실행오류('VM savininkas_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def čekis_medija(self, Būsena_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Pavadinimas_2, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Pavadinimas_2)]
        Leisti_VALUE = [str(self.KELIAS(VALUE)) for VALUE in Būsena_VALUE.get('media', [])]
        for Pavadinimas_2, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(valdiklis_8bff480f) + r'-\d+-\d+', Pavadinimas_2) for valdiklis_8bff480f in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Leisti_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def laida_Būsena(self):
        Būsena_VALUE = self.Skaitymas()
        if Būsena_VALUE is None: return {'name': self.Pavadinimas_2, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Būsena_VALUE, 등록목록(self.Komanda(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Būsena_VALUE['name']), 'uuid': Būsena_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.KELIAS(Būsena_VALUE['iso'])) if Būsena_VALUE.get('iso') else None,
                'serial_log': str(self.KELIAS(Būsena_VALUE['serial_log'])) if Būsena_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Vykdyti_komanda(self):
        Būsena_VALUE = self.Skaitymas()
        등록됨 = 등록목록(self.Komanda(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Būsena_VALUE is not None and Būsena_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Būsena_VALUE, 등록됨, atkurti_Būsena=True)
            dabartinis_prekė = msinfo32_exe.get('VMState')
            if dabartinis_prekė == 'running':
                print('이미 Vykdyti_komanda 중입니다. 재빌드·재시작하지 않습니다.')
                return self.laida_Būsena()
            self.čekis_medija(Būsena_VALUE, msinfo32_exe)
            if dabartinis_prekė in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(dabartinis_prekė))
                if dabartinis_prekė == 'paused':
                    self.Komanda(['VBoxManage', 'controlvm', Būsena_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 kartoti_VALUE Atverti 전에 기존 기록도 보관한다.
                    if Būsena_VALUE.get('serial_log'):
                        원본 = self.KELIAS(Būsena_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.KELIAS('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Komanda(['VBoxManage', 'startvm', Būsena_VALUE['uuid'], '--type', self.metodas_MODE])
                return self.laida_Būsena()
            if dabartinis_prekė not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 ATGAL_VALUE kartoti_VALUE 실행하세요.'.format(dabartinis_prekė))
        elif Būsena_VALUE is not None and not Būsena_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 kartoti_VALUE 등록하세요.')
        elif self.Pavadinimas_2 in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Vykdyti_komanda 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Komanda(['make', '-C', str(self.šaknis_VALUE / 'os'), 'iso']), end='')
        원본 = self.šaknis_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        medija_VALUE = 'media/kernel-' + kontrolinė_suma(원본) + '.iso'
        vieta_VALUE = self.KELIAS(medija_VALUE)
        vieta_VALUE.parent.mkdir(exist_ok=True)
        if vieta_VALUE.exists():
            if kontrolinė_suma(vieta_VALUE) != kontrolinė_suma(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(vieta_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(vieta_VALUE.parent)) as Failas:
                shutil.copyfile(str(원본), Failas.name)
                os.link(Failas.name, str(vieta_VALUE))

        if Būsena_VALUE is None:
            Būsena_VALUE = {'version': 1, 'name': self.Pavadinimas_2, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Būsena_VALUE)
        if msinfo32_exe is None:
            self.Komanda(['VBoxManage', 'createvm', '--name', Būsena_VALUE['name'], '--uuid', Būsena_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.KELIAS('machines')), '--register'])
            self.Komanda(['VBoxManage', 'setextradata', Būsena_VALUE['uuid'], 'JKOROS/Owner', Būsena_VALUE['owner']])
        # kompiliuoti_sistema 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Būsena_VALUE, 등록목록(self.Komanda(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('kompiliuoti_sistema 중 VM 상태가 바뀌었습니다. kartoti_VALUE make vbox를 실행하세요.')
        self.čekis_medija(Būsena_VALUE, msinfo32_exe)
        Būsena_VALUE['iso'] = medija_VALUE
        if medija_VALUE not in Būsena_VALUE['media']: Būsena_VALUE['media'].append(medija_VALUE)
        Būsena_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.KELIAS(Būsena_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Būsena_VALUE)
        self.Komanda(['VBoxManage', 'modifyvm', Būsena_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Pavadinimas_2, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Pavadinimas_2)]
        if 'JKOROS IDE' not in 제어기들:
            self.Komanda(['VBoxManage', 'storagectl', Būsena_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Komanda(['VBoxManage', 'storageattach', Būsena_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(vieta_VALUE)])
        Būsena_VALUE['pending'] = False
        self.Store_VALUE(Būsena_VALUE)
        self.Komanda(['VBoxManage', 'startvm', Būsena_VALUE['uuid'], '--type', self.metodas_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.laida_Būsena()


def Paleisti():
    analizuoti_sintaksę_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Vykdyti_komanda 및 Būsena_VALUE užklausa_VALUE')
    analizuoti_sintaksę_VALUE.add_argument('action', choices=['run', 'status'])
    parametras_argumentas = analizuoti_sintaksę_VALUE.parse_args()
    Vykdyti_komanda = programa_programų_skydelis(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametras_argumentas.action == 'status':
        print(json.dumps(Vykdyti_komanda.laida_Būsena(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 numeris 없습니다. organizuoti 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/teisė_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Vykdyti_komanda.KELIAS('lock').parent.mkdir(parents=True, exist_ok=True)
    with Vykdyti_komanda.KELIAS('lock').open('a') as užraktas_VALUE:
        try: fcntl.flock(užraktas_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Vykdyti_komanda 작업이 진행 중입니다.')
        print(json.dumps(Vykdyti_komanda.Vykdyti_komanda(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Paleisti()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as KLAIDA:
        print('VBOX KLAIDA: ' + str(KLAIDA), file=sys.stderr)
        sys.exit(1)
