#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_appskuff. 기존 VM/디스크/Store_VERDI 상태는 삭제하지 않는다."""
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


class kjøring_feil(RuntimeError):
    pass


def Utfør_Shell_kommando(Argumenter):
    miljø = dict(os.environ, LC_ALL='C')
    KR = subprocess.run([str(VERDI) for VERDI in Argumenter], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=miljø, timeout=180)
    Innhold_VERDI = KR.stdout.decode('utf-8', 'replace')
    if KR.returncode:
        raise kjøring_feil('Kommando feil_VERDI: ' + ' '.join(str(VERDI) for VERDI in Argumenter) + '\n' + Innhold_VERDI[-10000:])
    return Innhold_VERDI


def attributtverdi(Innhold_VERDI):
    KR = {}
    for Linje in Innhold_VERDI.splitlines():
        if '=' not in Linje:
            continue
        Navn, VERDI = Linje.split('=', 1)
        if Navn.startswith('"'):
            Navn = json.loads(Navn)
        if VERDI.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VERDI)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VERDI): VERDI = 읽은값
            except ValueError:
                raise kjøring_feil('VirtualBox attributtverdi format_VERDI feil: ' + Linje)
        KR[Navn] = VERDI
    return KR


def 등록목록(Innhold_VERDI):
    KR = {}
    for Linje in Innhold_VERDI.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Linje)
        if 일치: KR[일치.group(2).lower()] = 일치.group(1)
    return KR


def kontrollsum(Sti):
    VERDI = hashlib.sha256()
    with Sti.open('rb') as Fil:
        for data in iter(lambda: Fil.read(1024 * 1024), b''): VERDI.update(data)
    return VERDI.hexdigest()


class app_appskuff:
    def __init__(self, rot_VERDI, Navn, metode_MODUS='gui', Kommando=Utfør_Shell_kommando):
        self.rot_VERDI = Path(rot_VERDI).resolve()
        self.Navn, self.metode_MODUS, self.Kommando = Navn, metode_MODUS, Kommando
        self.보관 = self.rot_VERDI / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Navn) or Navn in ('.', '..'):
            raise kjøring_feil('VM 이름은 문자·siffer_VERDI·공백·밑줄·괄호·마침표·하이픈만 사용할 nummer 있습니다.')
        if metode_MODUS not in ('gui', 'headless'): raise kjøring_feil('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Sti(self, node_VERDI_6a3b6fa7):
        if Path(node_VERDI_6a3b6fa7).is_absolute() or '..' in Path(node_VERDI_6a3b6fa7).parts:
            raise kjøring_feil('잘못된 관리 Sti: ' + str(node_VERDI_6a3b6fa7))
        KR = self.보관
        for 부분 in ['.vbox'] + list(Path(node_VERDI_6a3b6fa7).parts):
            if 부분 == '.vbox': KR = self.보관
            else: KR = KR / 부분
            if KR.is_symlink(): raise kjøring_feil('Koble_til 경로는 사용하지 않습니다: ' + str(KR))
        return KR

    def Les(self):
        Sti = self.Sti('state.json')
        if not Sti.exists(): return None
        status_VERDI = json.loads(Sti.read_text(encoding='utf-8'))
        if status_VERDI.get('version') != 1 or status_VERDI.get('name') != self.Navn:
            raise kjøring_feil('관리 상태의 VM Navn/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Navn in ('uuid', 'owner'):
            if str(uuid.UUID(status_VERDI[Navn])) != status_VERDI[Navn]: raise kjøring_feil('잘못된 VM identifikator_VERDI')
        return status_VERDI

    def Store_VERDI(self, status_VERDI):
        mål_VERDI = self.Sti('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fil:
            json.dump(status_VERDI, Fil, ensure_ascii=False, indent=2)
            Fil.write('\n')
            임시 = Fil.name
        os.replace(임시, str(mål_VERDI))

    def msinfo32_exe(self, status_VERDI, 등록됨, gjenopprette_status=False):
        if status_VERDI['uuid'] not in 등록됨:
            raise kjøring_feil('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = attributtverdi(self.Kommando(['VBoxManage', 'showvminfo', status_VERDI['uuid'], '--machinereadable']))
        Posisjon = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Sti('machines').resolve() not in Posisjon.parents or msinfo32_exe.get('UUID') != status_VERDI['uuid']:
            raise kjøring_feil('이 프로젝트의 VM Innstillinger Sti/UUID와 일치하지 않아 변경하지 않습니다.')
        tusj_VERDI = self.Kommando(['VBoxManage', 'getextradata', status_VERDI['uuid'], 'JKOROS/Owner']).strip()
        if tusj_VERDI != 'Value: ' + status_VERDI['owner']:
            if gjenopprette_status and status_VERDI.get('pending') and tusj_VERDI == 'No value set!':
                self.Kommando(['VBoxManage', 'setextradata', status_VERDI['uuid'], 'JKOROS/Owner', status_VERDI['owner']])
            else:
                raise kjøring_feil('VM eier_VERDI 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def sjekk_media(self, status_VERDI, msinfo32_exe):
        제어기들 = [VERDI for Navn, VERDI in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Navn)]
        Tillat_VERDI = [str(self.Sti(VERDI)) for VERDI in status_VERDI.get('media', [])]
        for Navn, VERDI in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontroller) + r'-\d+-\d+', Navn) for kontroller in 제어기들):
                if VERDI not in ('none', 'emptydrive') and VERDI not in Tillat_VERDI:
                    raise kjøring_feil('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VERDI)

    def vise_status(self):
        status_VERDI = self.Les()
        if status_VERDI is None: return {'name': self.Navn, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(status_VERDI, 등록목록(self.Kommando(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', status_VERDI['name']), 'uuid': status_VERDI['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Sti(status_VERDI['iso'])) if status_VERDI.get('iso') else None,
                'serial_log': str(self.Sti(status_VERDI['serial_log'])) if status_VERDI.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Utfør_kommando(self):
        status_VERDI = self.Les()
        등록됨 = 등록목록(self.Kommando(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if status_VERDI is not None and status_VERDI['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(status_VERDI, 등록됨, gjenopprette_status=True)
            betalt_vare = msinfo32_exe.get('VMState')
            if betalt_vare == 'running':
                print('이미 Utfør_kommando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.vise_status()
            self.sjekk_media(status_VERDI, msinfo32_exe)
            if betalt_vare in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VERDI 상태를 버리지 않습니다.'.format(betalt_vare))
                if betalt_vare == 'paused':
                    self.Kommando(['VBoxManage', 'controlvm', status_VERDI['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 prøve_på_nytt_VERDI Åpne 전에 기존 기록도 보관한다.
                    if status_VERDI.get('serial_log'):
                        원본 = self.Sti(status_VERDI['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Sti('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Kommando(['VBoxManage', 'startvm', status_VERDI['uuid'], '--type', self.metode_MODUS])
                return self.vise_status()
            if betalt_vare not in ('poweroff', 'aborted'):
                raise kjøring_feil('VM이 bytt_MODUS 중입니다 ({}). 작업이 끝난 TILBAKE_VERDI prøve_på_nytt_VERDI 실행하세요.'.format(betalt_vare))
        elif status_VERDI is not None and not status_VERDI.get('pending'):
            raise kjøring_feil('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 prøve_på_nytt_VERDI 등록하세요.')
        elif self.Navn in 등록됨.values():
            raise kjøring_feil('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VERDI/Utfør_kommando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Kommando(['make', '-C', str(self.rot_VERDI / 'os'), 'iso']), end='')
        원본 = self.rot_VERDI / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise kjøring_feil('부팅 ISO가 생성되지 않았습니다.')
        media_VERDI = 'media/kernel-' + kontrollsum(원본) + '.iso'
        mål_VERDI = self.Sti(media_VERDI)
        mål_VERDI.parent.mkdir(exist_ok=True)
        if mål_VERDI.exists():
            if kontrollsum(mål_VERDI) != kontrollsum(원본): raise kjøring_feil('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(mål_VERDI))
        else:
            with tempfile.NamedTemporaryFile(dir=str(mål_VERDI.parent)) as Fil:
                shutil.copyfile(str(원본), Fil.name)
                os.link(Fil.name, str(mål_VERDI))

        if status_VERDI is None:
            status_VERDI = {'version': 1, 'name': self.Navn, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VERDI(status_VERDI)
        if msinfo32_exe is None:
            self.Kommando(['VBoxManage', 'createvm', '--name', status_VERDI['name'], '--uuid', status_VERDI['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Sti('machines')), '--register'])
            self.Kommando(['VBoxManage', 'setextradata', status_VERDI['uuid'], 'JKOROS/Owner', status_VERDI['owner']])
        # bygg_System 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(status_VERDI, 등록목록(self.Kommando(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise kjøring_feil('bygg_System 중 VM 상태가 바뀌었습니다. prøve_på_nytt_VERDI make vbox를 실행하세요.')
        self.sjekk_media(status_VERDI, msinfo32_exe)
        status_VERDI['iso'] = media_VERDI
        if media_VERDI not in status_VERDI['media']: status_VERDI['media'].append(media_VERDI)
        status_VERDI['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VERDI = self.Sti(status_VERDI['serial_log'])
        LOG_VERDI.parent.mkdir(exist_ok=True)
        self.Store_VERDI(status_VERDI)
        self.Kommando(['VBoxManage', 'modifyvm', status_VERDI['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VERDI)])
        제어기들 = [VERDI for Navn, VERDI in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Navn)]
        if 'JKOROS IDE' not in 제어기들:
            self.Kommando(['VBoxManage', 'storagectl', status_VERDI['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Kommando(['VBoxManage', 'storageattach', status_VERDI['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(mål_VERDI)])
        status_VERDI['pending'] = False
        self.Store_VERDI(status_VERDI)
        self.Kommando(['VBoxManage', 'startvm', status_VERDI['uuid'], '--type', self.metode_MODUS])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.vise_status()


def Kjør_2():
    dele_opp_VERDI = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Utfør_kommando 및 status_VERDI spørre_VERDI')
    dele_opp_VERDI.add_argument('action', choices=['run', 'status'])
    parameter_argument = dele_opp_VERDI.parse_args()
    Utfør_kommando = app_appskuff(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(Utfør_kommando.vise_status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise kjøring_feil('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise kjøring_feil('/dev/vboxdrv에 접근할 nummer 없습니다. vert 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/tillatelse_VERDI 변경은 하지 않습니다.')
    os.umask(0o077)
    Utfør_kommando.Sti('lock').parent.mkdir(parents=True, exist_ok=True)
    with Utfør_kommando.Sti('lock').open('a') as blokkere_VERDI:
        try: fcntl.flock(blokkere_VERDI, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise kjøring_feil('다른 jkoros VirtualBox Utfør_kommando 작업이 진행 중입니다.')
        print(json.dumps(Utfør_kommando.Utfør_kommando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Kjør_2()
    except (kjøring_feil, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as feil:
        print('VBOX feil: ' + str(feil), file=sys.stderr)
        sys.exit(1)
