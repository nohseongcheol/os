#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_Startbild. 기존 VM/디스크/Store_värde 상태는 삭제하지 않는다."""
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


class körning_fel_3f02a041(RuntimeError):
    pass


def köra_Shell_kommando(argument):
    miljö = dict(os.environ, LC_ALL='C')
    RESULTAT = subprocess.run([str(värde) for värde in argument], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=miljö, timeout=180)
    Innehåll_värde = RESULTAT.stdout.decode('utf-8', 'replace')
    if RESULTAT.returncode:
        raise körning_fel_3f02a041('kommando fel_värde: ' + ' '.join(str(värde) for värde in argument) + '\n' + Innehåll_värde[-10000:])
    return Innehåll_värde


def attribut_värde(Innehåll_värde):
    RESULTAT = {}
    for inmatningsrad in Innehåll_värde.splitlines():
        if '=' not in inmatningsrad:
            continue
        Namn, värde = inmatningsrad.split('=', 1)
        if Namn.startswith('"'):
            Namn = json.loads(Namn)
        if värde.startswith('"'):
            try:
                läsa_värde, 끝 = json.JSONDecoder().raw_decode(värde)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(värde): värde = läsa_värde
            except ValueError:
                raise körning_fel_3f02a041('VirtualBox attribut_värde format_värde fel: ' + inmatningsrad)
        RESULTAT[Namn] = värde
    return RESULTAT


def 등록목록(Innehåll_värde):
    RESULTAT = {}
    for inmatningsrad in Innehåll_värde.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', inmatningsrad)
        if 일치: RESULTAT[일치.group(2).lower()] = 일치.group(1)
    return RESULTAT


def kontrollsumma(sökväg_2):
    värde = hashlib.sha256()
    with sökväg_2.open('rb') as filnamn:
        for data in iter(lambda: filnamn.read(1024 * 1024), b''): värde.update(data)
    return värde.hexdigest()


class app_Startbild:
    def __init__(self, rot_värde, Namn, metod_läge='gui', kommando=köra_Shell_kommando):
        self.rot_värde = Path(rot_värde).resolve()
        self.Namn, self.metod_läge, self.kommando = Namn, metod_läge, kommando
        self.보관 = self.rot_värde / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Namn) or Namn in ('.', '..'):
            raise körning_fel_3f02a041('VM 이름은 문자·siffra_värde·공백·밑줄·괄호·마침표·하이픈만 사용할 nummer 있습니다.')
        if metod_läge not in ('gui', 'headless'): raise körning_fel_3f02a041('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def sökväg_2(self, peer_värde):
        if Path(peer_värde).is_absolute() or '..' in Path(peer_värde).parts:
            raise körning_fel_3f02a041('잘못된 관리 sökväg_2: ' + str(peer_värde))
        RESULTAT = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_värde).parts):
            if 부분 == '.vbox': RESULTAT = self.보관
            else: RESULTAT = RESULTAT / 부분
            if RESULTAT.is_symlink(): raise körning_fel_3f02a041('Anslut 경로는 사용하지 않습니다: ' + str(RESULTAT))
        return RESULTAT

    def Läs(self):
        sökväg_2 = self.sökväg_2('state.json')
        if not sökväg_2.exists(): return None
        status_värde = json.loads(sökväg_2.read_text(encoding='utf-8'))
        if status_värde.get('version') != 1 or status_värde.get('name') != self.Namn:
            raise körning_fel_3f02a041('관리 상태의 VM Namn/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Namn in ('uuid', 'owner'):
            if str(uuid.UUID(status_värde[Namn])) != status_värde[Namn]: raise körning_fel_3f02a041('잘못된 VM identifierare_värde')
        return status_värde

    def Store_värde(self, status_värde):
        mål_värde = self.sökväg_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as filnamn:
            json.dump(status_värde, filnamn, ensure_ascii=False, indent=2)
            filnamn.write('\n')
            임시 = filnamn.name
        os.replace(임시, str(mål_värde))

    def msinfo32_exe(self, status_värde, 등록됨, återställa_status=False):
        if status_värde['uuid'] not in 등록됨:
            raise körning_fel_3f02a041('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = attribut_värde(self.kommando(['VBoxManage', 'showvminfo', status_värde['uuid'], '--machinereadable']))
        position = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.sökväg_2('machines').resolve() not in position.parents or msinfo32_exe.get('UUID') != status_värde['uuid']:
            raise körning_fel_3f02a041('이 프로젝트의 VM Inställningar sökväg_2/UUID와 일치하지 않아 변경하지 않습니다.')
        markör_värde = self.kommando(['VBoxManage', 'getextradata', status_värde['uuid'], 'JKOROS/Owner']).strip()
        if markör_värde != 'Value: ' + status_värde['owner']:
            if återställa_status and status_värde.get('pending') and markör_värde == 'No value set!':
                self.kommando(['VBoxManage', 'setextradata', status_värde['uuid'], 'JKOROS/Owner', status_värde['owner']])
            else:
                raise körning_fel_3f02a041('VM ägare_värde 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def check_Media(self, status_värde, msinfo32_exe):
        제어기들 = [värde for Namn, värde in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Namn)]
        Tillåt_värde = [str(self.sökväg_2(värde)) for värde in status_värde.get('media', [])]
        for Namn, värde in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontroll_8bff480f) + r'-\d+-\d+', Namn) for kontroll_8bff480f in 제어기들):
                if värde not in ('none', 'emptydrive') and värde not in Tillåt_värde:
                    raise körning_fel_3f02a041('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + värde)

    def visa_status(self):
        status_värde = self.Läs()
        if status_värde is None: return {'name': self.Namn, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(status_värde, 등록목록(self.kommando(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', status_värde['name']), 'uuid': status_värde['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.sökväg_2(status_värde['iso'])) if status_värde.get('iso') else None,
                'serial_log': str(self.sökväg_2(status_värde['serial_log'])) if status_värde.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def köra_kommando(self):
        status_värde = self.Läs()
        등록됨 = 등록목록(self.kommando(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if status_värde is not None and status_värde['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(status_värde, 등록됨, återställa_status=True)
            aktuellt_objekt = msinfo32_exe.get('VMState')
            if aktuellt_objekt == 'running':
                print('이미 köra_kommando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.visa_status()
            self.check_Media(status_värde, msinfo32_exe)
            if aktuellt_objekt in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_värde 상태를 버리지 않습니다.'.format(aktuellt_objekt))
                if aktuellt_objekt == 'paused':
                    self.kommando(['VBoxManage', 'controlvm', status_värde['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 försöka_igen_värde Öppna 전에 기존 기록도 보관한다.
                    if status_värde.get('serial_log'):
                        원본 = self.sökväg_2(status_värde['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.sökväg_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.kommando(['VBoxManage', 'startvm', status_värde['uuid'], '--type', self.metod_läge])
                return self.visa_status()
            if aktuellt_objekt not in ('poweroff', 'aborted'):
                raise körning_fel_3f02a041('VM이 byta_läge 중입니다 ({}). 작업이 끝난 BACK_värde försöka_igen_värde 실행하세요.'.format(aktuellt_objekt))
        elif status_värde is not None and not status_värde.get('pending'):
            raise körning_fel_3f02a041('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 försöka_igen_värde 등록하세요.')
        elif self.Namn in 등록됨.values():
            raise körning_fel_3f02a041('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_värde/köra_kommando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.kommando(['make', '-C', str(self.rot_värde / 'os'), 'iso']), end='')
        원본 = self.rot_värde / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise körning_fel_3f02a041('maskinstart ISO가 생성되지 않았습니다.')
        Media_värde = 'media/kernel-' + kontrollsumma(원본) + '.iso'
        mål_värde = self.sökväg_2(Media_värde)
        mål_värde.parent.mkdir(exist_ok=True)
        if mål_värde.exists():
            if kontrollsumma(mål_värde) != kontrollsumma(원본): raise körning_fel_3f02a041('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(mål_värde))
        else:
            with tempfile.NamedTemporaryFile(dir=str(mål_värde.parent)) as filnamn:
                shutil.copyfile(str(원본), filnamn.name)
                os.link(filnamn.name, str(mål_värde))

        if status_värde is None:
            status_värde = {'version': 1, 'name': self.Namn, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_värde(status_värde)
        if msinfo32_exe is None:
            self.kommando(['VBoxManage', 'createvm', '--name', status_värde['name'], '--uuid', status_värde['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.sökväg_2('machines')), '--register'])
            self.kommando(['VBoxManage', 'setextradata', status_värde['uuid'], 'JKOROS/Owner', status_värde['owner']])
        # version_System 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(status_värde, 등록목록(self.kommando(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise körning_fel_3f02a041('version_System 중 VM 상태가 바뀌었습니다. försöka_igen_värde make vbox를 실행하세요.')
        self.check_Media(status_värde, msinfo32_exe)
        status_värde['iso'] = Media_värde
        if Media_värde not in status_värde['media']: status_värde['media'].append(Media_värde)
        status_värde['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_värde = self.sökväg_2(status_värde['serial_log'])
        LOG_värde.parent.mkdir(exist_ok=True)
        self.Store_värde(status_värde)
        self.kommando(['VBoxManage', 'modifyvm', status_värde['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_värde)])
        제어기들 = [värde for Namn, värde in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Namn)]
        if 'JKOROS IDE' not in 제어기들:
            self.kommando(['VBoxManage', 'storagectl', status_värde['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.kommando(['VBoxManage', 'storageattach', status_värde['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(mål_värde)])
        status_värde['pending'] = False
        self.Store_värde(status_värde)
        self.kommando(['VBoxManage', 'startvm', status_värde['uuid'], '--type', self.metod_läge])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.visa_status()


def Kör():
    parsa_värde = argparse.ArgumentParser(description='jkoros 전용 VirtualBox köra_kommando 및 status_värde fråga_värde')
    parsa_värde.add_argument('action', choices=['run', 'status'])
    parameter_argument = parsa_värde.parse_args()
    köra_kommando = app_Startbild(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(köra_kommando.visa_status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise körning_fel_3f02a041('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise körning_fel_3f02a041('/dev/vboxdrv에 접근할 nummer 없습니다. värd 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/behörighet_värde 변경은 하지 않습니다.')
    os.umask(0o077)
    köra_kommando.sökväg_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with köra_kommando.sökväg_2('lock').open('a') as lås_värde:
        try: fcntl.flock(lås_värde, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise körning_fel_3f02a041('다른 jkoros VirtualBox köra_kommando 작업이 진행 중입니다.')
        print(json.dumps(köra_kommando.köra_kommando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Kör()
    except (körning_fel_3f02a041, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as fel:
        print('VBOX fel: ' + str(fel), file=sys.stderr)
        sys.exit(1)
