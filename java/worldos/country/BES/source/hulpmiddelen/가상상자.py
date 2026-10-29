#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_app_lade. 기존 VM/디스크/Store_WAARDE 상태는 삭제하지 않는다."""
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


class uitvoerbewerking_fout(RuntimeError):
    pass


def Uitvoeren_Shell_opdracht(argumenten):
    omgeving = dict(os.environ, LC_ALL='C')
    resultaat = subprocess.run([str(WAARDE) for WAARDE in argumenten], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=omgeving, timeout=180)
    Inhoud_WAARDE = resultaat.stdout.decode('utf-8', 'replace')
    if resultaat.returncode:
        raise uitvoerbewerking_fout('opdracht fout_WAARDE: ' + ' '.join(str(WAARDE) for WAARDE in argumenten) + '\n' + Inhoud_WAARDE[-10000:])
    return Inhoud_WAARDE


def kenmerkwaarde(Inhoud_WAARDE):
    resultaat = {}
    for invoerregel in Inhoud_WAARDE.splitlines():
        if '=' not in invoerregel:
            continue
        Naam, WAARDE = invoerregel.split('=', 1)
        if Naam.startswith('"'):
            Naam = json.loads(Naam)
        if WAARDE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(WAARDE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(WAARDE): WAARDE = 읽은값
            except ValueError:
                raise uitvoerbewerking_fout('VirtualBox kenmerkwaarde opmaak_WAARDE fout: ' + invoerregel)
        resultaat[Naam] = WAARDE
    return resultaat


def 등록목록(Inhoud_WAARDE):
    resultaat = {}
    for invoerregel in Inhoud_WAARDE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', invoerregel)
        if 일치: resultaat[일치.group(2).lower()] = 일치.group(1)
    return resultaat


def controlesom(pad):
    WAARDE = hashlib.sha256()
    with pad.open('rb') as bestand:
        for gegevens in iter(lambda: bestand.read(1024 * 1024), b''): WAARDE.update(gegevens)
    return WAARDE.hexdigest()


class app_app_lade:
    def __init__(self, wortel_WAARDE, Naam, methode_MODUS='gui', opdracht=Uitvoeren_Shell_opdracht):
        self.wortel_WAARDE = Path(wortel_WAARDE).resolve()
        self.Naam, self.methode_MODUS, self.opdracht = Naam, methode_MODUS, opdracht
        self.보관 = self.wortel_WAARDE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Naam) or Naam in ('.', '..'):
            raise uitvoerbewerking_fout('VM 이름은 문자·cijfer_WAARDE·공백·밑줄·괄호·마침표·하이픈만 사용할 nummer 있습니다.')
        if methode_MODUS not in ('gui', 'headless'): raise uitvoerbewerking_fout('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def pad(self, peer_WAARDE):
        if Path(peer_WAARDE).is_absolute() or '..' in Path(peer_WAARDE).parts:
            raise uitvoerbewerking_fout('잘못된 관리 pad: ' + str(peer_WAARDE))
        resultaat = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_WAARDE).parts):
            if 부분 == '.vbox': resultaat = self.보관
            else: resultaat = resultaat / 부분
            if resultaat.is_symlink(): raise uitvoerbewerking_fout('Verbinden 경로는 사용하지 않습니다: ' + str(resultaat))
        return resultaat

    def Lezen(self):
        pad = self.pad('state.json')
        if not pad.exists(): return None
        Status_WAARDE = json.loads(pad.read_text(encoding='utf-8'))
        if Status_WAARDE.get('version') != 1 or Status_WAARDE.get('name') != self.Naam:
            raise uitvoerbewerking_fout('관리 상태의 VM Naam/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Naam in ('uuid', 'owner'):
            if str(uuid.UUID(Status_WAARDE[Naam])) != Status_WAARDE[Naam]: raise uitvoerbewerking_fout('잘못된 VM id_WAARDE')
        return Status_WAARDE

    def Store_WAARDE(self, Status_WAARDE):
        doel_WAARDE = self.pad('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as bestand:
            json.dump(Status_WAARDE, bestand, ensure_ascii=False, indent=2)
            bestand.write('\n')
            임시 = bestand.name
        os.replace(임시, str(doel_WAARDE))

    def msinfo32_exe(self, Status_WAARDE, 등록됨, herstellen_Status=False):
        if Status_WAARDE['uuid'] not in 등록됨:
            raise uitvoerbewerking_fout('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = kenmerkwaarde(self.opdracht(['VBoxManage', 'showvminfo', Status_WAARDE['uuid'], '--machinereadable']))
        positie = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.pad('machines').resolve() not in positie.parents or msinfo32_exe.get('UUID') != Status_WAARDE['uuid']:
            raise uitvoerbewerking_fout('이 프로젝트의 VM Instellingen pad/UUID와 일치하지 않아 변경하지 않습니다.')
        markering_WAARDE = self.opdracht(['VBoxManage', 'getextradata', Status_WAARDE['uuid'], 'JKOROS/Owner']).strip()
        if markering_WAARDE != 'Value: ' + Status_WAARDE['owner']:
            if herstellen_Status and Status_WAARDE.get('pending') and markering_WAARDE == 'No value set!':
                self.opdracht(['VBoxManage', 'setextradata', Status_WAARDE['uuid'], 'JKOROS/Owner', Status_WAARDE['owner']])
            else:
                raise uitvoerbewerking_fout('VM eigenaar_WAARDE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def cheque_Media(self, Status_WAARDE, msinfo32_exe):
        제어기들 = [WAARDE for Naam, WAARDE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Naam)]
        Toestaan_WAARDE = [str(self.pad(WAARDE)) for WAARDE in Status_WAARDE.get('media', [])]
        for Naam, WAARDE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(controller) + r'-\d+-\d+', Naam) for controller in 제어기들):
                if WAARDE not in ('none', 'emptydrive') and WAARDE not in Toestaan_WAARDE:
                    raise uitvoerbewerking_fout('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + WAARDE)

    def weergeven_Status(self):
        Status_WAARDE = self.Lezen()
        if Status_WAARDE is None: return {'name': self.Naam, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Status_WAARDE, 등록목록(self.opdracht(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Status_WAARDE['name']), 'uuid': Status_WAARDE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.pad(Status_WAARDE['iso'])) if Status_WAARDE.get('iso') else None,
                'serial_log': str(self.pad(Status_WAARDE['serial_log'])) if Status_WAARDE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Uitvoeren_opdracht(self):
        Status_WAARDE = self.Lezen()
        등록됨 = 등록목록(self.opdracht(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Status_WAARDE is not None and Status_WAARDE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Status_WAARDE, 등록됨, herstellen_Status=True)
            actueel_item = msinfo32_exe.get('VMState')
            if actueel_item == 'running':
                print('이미 Uitvoeren_opdracht 중입니다. 재빌드·재시작하지 않습니다.')
                return self.weergeven_Status()
            self.cheque_Media(Status_WAARDE, msinfo32_exe)
            if actueel_item in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_WAARDE 상태를 버리지 않습니다.'.format(actueel_item))
                if actueel_item == 'paused':
                    self.opdracht(['VBoxManage', 'controlvm', Status_WAARDE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 opnieuw_proberen_WAARDE Openen 전에 기존 기록도 보관한다.
                    if Status_WAARDE.get('serial_log'):
                        원본 = self.pad(Status_WAARDE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.pad('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.opdracht(['VBoxManage', 'startvm', Status_WAARDE['uuid'], '--type', self.methode_MODUS])
                return self.weergeven_Status()
            if actueel_item not in ('poweroff', 'aborted'):
                raise uitvoerbewerking_fout('VM이 switch_MODUS 중입니다 ({}). 작업이 끝난 BACK_WAARDE opnieuw_proberen_WAARDE 실행하세요.'.format(actueel_item))
        elif Status_WAARDE is not None and not Status_WAARDE.get('pending'):
            raise uitvoerbewerking_fout('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 opnieuw_proberen_WAARDE 등록하세요.')
        elif self.Naam in 등록됨.values():
            raise uitvoerbewerking_fout('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_WAARDE/Uitvoeren_opdracht 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.opdracht(['make', '-C', str(self.wortel_WAARDE / 'os'), 'iso']), end='')
        원본 = self.wortel_WAARDE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise uitvoerbewerking_fout('machineopstart ISO가 생성되지 않았습니다.')
        Media_WAARDE = 'media/kernel-' + controlesom(원본) + '.iso'
        doel_WAARDE = self.pad(Media_WAARDE)
        doel_WAARDE.parent.mkdir(exist_ok=True)
        if doel_WAARDE.exists():
            if controlesom(doel_WAARDE) != controlesom(원본): raise uitvoerbewerking_fout('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(doel_WAARDE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(doel_WAARDE.parent)) as bestand:
                shutil.copyfile(str(원본), bestand.name)
                os.link(bestand.name, str(doel_WAARDE))

        if Status_WAARDE is None:
            Status_WAARDE = {'version': 1, 'name': self.Naam, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_WAARDE(Status_WAARDE)
        if msinfo32_exe is None:
            self.opdracht(['VBoxManage', 'createvm', '--name', Status_WAARDE['name'], '--uuid', Status_WAARDE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.pad('machines')), '--register'])
            self.opdracht(['VBoxManage', 'setextradata', Status_WAARDE['uuid'], 'JKOROS/Owner', Status_WAARDE['owner']])
        # bouwen 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Status_WAARDE, 등록목록(self.opdracht(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise uitvoerbewerking_fout('bouwen 중 VM 상태가 바뀌었습니다. opnieuw_proberen_WAARDE make vbox를 실행하세요.')
        self.cheque_Media(Status_WAARDE, msinfo32_exe)
        Status_WAARDE['iso'] = Media_WAARDE
        if Media_WAARDE not in Status_WAARDE['media']: Status_WAARDE['media'].append(Media_WAARDE)
        Status_WAARDE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_WAARDE = self.pad(Status_WAARDE['serial_log'])
        LOG_WAARDE.parent.mkdir(exist_ok=True)
        self.Store_WAARDE(Status_WAARDE)
        self.opdracht(['VBoxManage', 'modifyvm', Status_WAARDE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_WAARDE)])
        제어기들 = [WAARDE for Naam, WAARDE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Naam)]
        if 'JKOROS IDE' not in 제어기들:
            self.opdracht(['VBoxManage', 'storagectl', Status_WAARDE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.opdracht(['VBoxManage', 'storageattach', Status_WAARDE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(doel_WAARDE)])
        Status_WAARDE['pending'] = False
        self.Store_WAARDE(Status_WAARDE)
        self.opdracht(['VBoxManage', 'startvm', Status_WAARDE['uuid'], '--type', self.methode_MODUS])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.weergeven_Status()


def starten():
    parseren_WAARDE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Uitvoeren_opdracht 및 Status_WAARDE query_WAARDE')
    parseren_WAARDE.add_argument('action', choices=['run', 'status'])
    parameter_argument = parseren_WAARDE.parse_args()
    Uitvoeren_opdracht = app_app_lade(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(Uitvoeren_opdracht.weergeven_Status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise uitvoerbewerking_fout('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise uitvoerbewerking_fout('/dev/vboxdrv에 접근할 nummer 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/machtiging_WAARDE 변경은 하지 않습니다.')
    os.umask(0o077)
    Uitvoeren_opdracht.pad('lock').parent.mkdir(parents=True, exist_ok=True)
    with Uitvoeren_opdracht.pad('lock').open('a') as vergrendelen_WAARDE:
        try: fcntl.flock(vergrendelen_WAARDE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise uitvoerbewerking_fout('다른 jkoros VirtualBox Uitvoeren_opdracht 작업이 진행 중입니다.')
        print(json.dumps(Uitvoeren_opdracht.Uitvoeren_opdracht(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: starten()
    except (uitvoerbewerking_fout, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as fout:
        print('VBOX fout: ' + str(fout), file=sys.stderr)
        sys.exit(1)
