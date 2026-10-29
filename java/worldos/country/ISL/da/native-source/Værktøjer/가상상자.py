#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_Kvikstart. 기존 VM/디스크/Store_VÆRDI 상태는 삭제하지 않는다."""
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


class udførelse_fejl(RuntimeError):
    pass


def Udfør_Shell_kommando(Argumenter):
    miljø = dict(os.environ, LC_ALL='C')
    KR = subprocess.run([str(VÆRDI) for VÆRDI in Argumenter], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=miljø, timeout=180)
    Indhold_VÆRDI = KR.stdout.decode('utf-8', 'replace')
    if KR.returncode:
        raise udførelse_fejl('Kommando fejl_VÆRDI: ' + ' '.join(str(VÆRDI) for VÆRDI in Argumenter) + '\n' + Indhold_VÆRDI[-10000:])
    return Indhold_VÆRDI


def attribut_VÆRDI(Indhold_VÆRDI):
    KR = {}
    for Linje in Indhold_VÆRDI.splitlines():
        if '=' not in Linje:
            continue
        Navn, VÆRDI = Linje.split('=', 1)
        if Navn.startswith('"'):
            Navn = json.loads(Navn)
        if VÆRDI.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VÆRDI)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VÆRDI): VÆRDI = 읽은값
            except ValueError:
                raise udførelse_fejl('VirtualBox attribut_VÆRDI format_VÆRDI fejl: ' + Linje)
        KR[Navn] = VÆRDI
    return KR


def 등록목록(Indhold_VÆRDI):
    KR = {}
    for Linje in Indhold_VÆRDI.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Linje)
        if 일치: KR[일치.group(2).lower()] = 일치.group(1)
    return KR


def kontrolsum(Sti):
    VÆRDI = hashlib.sha256()
    with Sti.open('rb') as Fil:
        for data in iter(lambda: Fil.read(1024 * 1024), b''): VÆRDI.update(data)
    return VÆRDI.hexdigest()


class app_Kvikstart:
    def __init__(self, rod_VÆRDI, Navn, metode_HYPPIGST='gui', Kommando=Udfør_Shell_kommando):
        self.rod_VÆRDI = Path(rod_VÆRDI).resolve()
        self.Navn, self.metode_HYPPIGST, self.Kommando = Navn, metode_HYPPIGST, Kommando
        self.보관 = self.rod_VÆRDI / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Navn) or Navn in ('.', '..'):
            raise udførelse_fejl('VM 이름은 문자·ciffer_VÆRDI·공백·밑줄·괄호·마침표·하이픈만 사용할 tal 있습니다.')
        if metode_HYPPIGST not in ('gui', 'headless'): raise udførelse_fejl('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Sti(self, peer_VÆRDI):
        if Path(peer_VÆRDI).is_absolute() or '..' in Path(peer_VÆRDI).parts:
            raise udførelse_fejl('잘못된 관리 Sti: ' + str(peer_VÆRDI))
        KR = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_VÆRDI).parts):
            if 부분 == '.vbox': KR = self.보관
            else: KR = KR / 부분
            if KR.is_symlink(): raise udførelse_fejl('Tilslut 경로는 사용하지 않습니다: ' + str(KR))
        return KR

    def Læse(self):
        Sti = self.Sti('state.json')
        if not Sti.exists(): return None
        status_VÆRDI = json.loads(Sti.read_text(encoding='utf-8'))
        if status_VÆRDI.get('version') != 1 or status_VÆRDI.get('name') != self.Navn:
            raise udførelse_fejl('관리 상태의 VM Navn/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Navn in ('uuid', 'owner'):
            if str(uuid.UUID(status_VÆRDI[Navn])) != status_VÆRDI[Navn]: raise udførelse_fejl('잘못된 VM identifikator_VÆRDI')
        return status_VÆRDI

    def Store_VÆRDI(self, status_VÆRDI):
        destination_VÆRDI = self.Sti('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fil:
            json.dump(status_VÆRDI, Fil, ensure_ascii=False, indent=2)
            Fil.write('\n')
            임시 = Fil.name
        os.replace(임시, str(destination_VÆRDI))

    def msinfo32_exe(self, status_VÆRDI, 등록됨, genoprette_status=False):
        if status_VÆRDI['uuid'] not in 등록됨:
            raise udførelse_fejl('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = attribut_VÆRDI(self.Kommando(['VBoxManage', 'showvminfo', status_VÆRDI['uuid'], '--machinereadable']))
        Placering = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Sti('machines').resolve() not in Placering.parents or msinfo32_exe.get('UUID') != status_VÆRDI['uuid']:
            raise udførelse_fejl('이 프로젝트의 VM Indstillinger Sti/UUID와 일치하지 않아 변경하지 않습니다.')
        mærke_VÆRDI = self.Kommando(['VBoxManage', 'getextradata', status_VÆRDI['uuid'], 'JKOROS/Owner']).strip()
        if mærke_VÆRDI != 'Value: ' + status_VÆRDI['owner']:
            if genoprette_status and status_VÆRDI.get('pending') and mærke_VÆRDI == 'No value set!':
                self.Kommando(['VBoxManage', 'setextradata', status_VÆRDI['uuid'], 'JKOROS/Owner', status_VÆRDI['owner']])
            else:
                raise udførelse_fejl('VM ejer_VÆRDI 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def check_Medie(self, status_VÆRDI, msinfo32_exe):
        제어기들 = [VÆRDI for Navn, VÆRDI in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Navn)]
        Tillad_VÆRDI = [str(self.Sti(VÆRDI)) for VÆRDI in status_VÆRDI.get('media', [])]
        for Navn, VÆRDI in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(ansvarlig) + r'-\d+-\d+', Navn) for ansvarlig in 제어기들):
                if VÆRDI not in ('none', 'emptydrive') and VÆRDI not in Tillad_VÆRDI:
                    raise udførelse_fejl('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VÆRDI)

    def vise_status(self):
        status_VÆRDI = self.Læse()
        if status_VÆRDI is None: return {'name': self.Navn, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(status_VÆRDI, 등록목록(self.Kommando(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', status_VÆRDI['name']), 'uuid': status_VÆRDI['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Sti(status_VÆRDI['iso'])) if status_VÆRDI.get('iso') else None,
                'serial_log': str(self.Sti(status_VÆRDI['serial_log'])) if status_VÆRDI.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Udfør_kommando(self):
        status_VÆRDI = self.Læse()
        등록됨 = 등록목록(self.Kommando(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if status_VÆRDI is not None and status_VÆRDI['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(status_VÆRDI, 등록됨, genoprette_status=True)
            aktuel_vare = msinfo32_exe.get('VMState')
            if aktuel_vare == 'running':
                print('이미 Udfør_kommando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.vise_status()
            self.check_Medie(status_VÆRDI, msinfo32_exe)
            if aktuel_vare in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VÆRDI 상태를 버리지 않습니다.'.format(aktuel_vare))
                if aktuel_vare == 'paused':
                    self.Kommando(['VBoxManage', 'controlvm', status_VÆRDI['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 prøve_igen_VÆRDI Åbn 전에 기존 기록도 보관한다.
                    if status_VÆRDI.get('serial_log'):
                        원본 = self.Sti(status_VÆRDI['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Sti('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Kommando(['VBoxManage', 'startvm', status_VÆRDI['uuid'], '--type', self.metode_HYPPIGST])
                return self.vise_status()
            if aktuel_vare not in ('poweroff', 'aborted'):
                raise udførelse_fejl('VM이 SKIFT_HYPPIGST 중입니다 ({}). 작업이 끝난 BACK_VÆRDI prøve_igen_VÆRDI 실행하세요.'.format(aktuel_vare))
        elif status_VÆRDI is not None and not status_VÆRDI.get('pending'):
            raise udførelse_fejl('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 prøve_igen_VÆRDI 등록하세요.')
        elif self.Navn in 등록됨.values():
            raise udførelse_fejl('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VÆRDI/Udfør_kommando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Kommando(['make', '-C', str(self.rod_VÆRDI / 'os'), 'iso']), end='')
        원본 = self.rod_VÆRDI / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise udførelse_fejl('부팅 ISO가 생성되지 않았습니다.')
        Medie_VÆRDI = 'media/kernel-' + kontrolsum(원본) + '.iso'
        destination_VÆRDI = self.Sti(Medie_VÆRDI)
        destination_VÆRDI.parent.mkdir(exist_ok=True)
        if destination_VÆRDI.exists():
            if kontrolsum(destination_VÆRDI) != kontrolsum(원본): raise udførelse_fejl('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destination_VÆRDI))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destination_VÆRDI.parent)) as Fil:
                shutil.copyfile(str(원본), Fil.name)
                os.link(Fil.name, str(destination_VÆRDI))

        if status_VÆRDI is None:
            status_VÆRDI = {'version': 1, 'name': self.Navn, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VÆRDI(status_VÆRDI)
        if msinfo32_exe is None:
            self.Kommando(['VBoxManage', 'createvm', '--name', status_VÆRDI['name'], '--uuid', status_VÆRDI['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Sti('machines')), '--register'])
            self.Kommando(['VBoxManage', 'setextradata', status_VÆRDI['uuid'], 'JKOROS/Owner', status_VÆRDI['owner']])
        # build_System 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(status_VÆRDI, 등록목록(self.Kommando(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise udførelse_fejl('build_System 중 VM 상태가 바뀌었습니다. prøve_igen_VÆRDI make vbox를 실행하세요.')
        self.check_Medie(status_VÆRDI, msinfo32_exe)
        status_VÆRDI['iso'] = Medie_VÆRDI
        if Medie_VÆRDI not in status_VÆRDI['media']: status_VÆRDI['media'].append(Medie_VÆRDI)
        status_VÆRDI['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VÆRDI = self.Sti(status_VÆRDI['serial_log'])
        LOG_VÆRDI.parent.mkdir(exist_ok=True)
        self.Store_VÆRDI(status_VÆRDI)
        self.Kommando(['VBoxManage', 'modifyvm', status_VÆRDI['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VÆRDI)])
        제어기들 = [VÆRDI for Navn, VÆRDI in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Navn)]
        if 'JKOROS IDE' not in 제어기들:
            self.Kommando(['VBoxManage', 'storagectl', status_VÆRDI['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Kommando(['VBoxManage', 'storageattach', status_VÆRDI['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destination_VÆRDI)])
        status_VÆRDI['pending'] = False
        self.Store_VÆRDI(status_VÆRDI)
        self.Kommando(['VBoxManage', 'startvm', status_VÆRDI['uuid'], '--type', self.metode_HYPPIGST])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.vise_status()


def Kør_2():
    opdele_tekst_VÆRDI = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Udfør_kommando 및 status_VÆRDI forespørge_VÆRDI')
    opdele_tekst_VÆRDI.add_argument('action', choices=['run', 'status'])
    parameter_argument = opdele_tekst_VÆRDI.parse_args()
    Udfør_kommando = app_Kvikstart(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(Udfør_kommando.vise_status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise udførelse_fejl('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise udførelse_fejl('/dev/vboxdrv에 접근할 tal 없습니다. vært 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/rettighed_VÆRDI 변경은 하지 않습니다.')
    os.umask(0o077)
    Udfør_kommando.Sti('lock').parent.mkdir(parents=True, exist_ok=True)
    with Udfør_kommando.Sti('lock').open('a') as lås_VÆRDI:
        try: fcntl.flock(lås_VÆRDI, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise udførelse_fejl('다른 jkoros VirtualBox Udfør_kommando 작업이 진행 중입니다.')
        print(json.dumps(Udfør_kommando.Udfør_kommando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Kør_2()
    except (udførelse_fejl, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as fejl:
        print('VBOX fejl: ' + str(fejl), file=sys.stderr)
        sys.exit(1)
