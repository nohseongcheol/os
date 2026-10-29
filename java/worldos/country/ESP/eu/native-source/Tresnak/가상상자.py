#!/usr/bin/env python3
"""jkoros 전용 VirtualBox aplik_abiarazle. 기존 VM/디스크/Store_balio 상태는 삭제하지 않는다."""
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


def exekutatu_shell_komando(Argumentuak):
    환경 = dict(os.environ, LC_ALL='C')
    EMAITZA = subprocess.run([str(balio) for balio in Argumentuak], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    eduki_balio = EMAITZA.stdout.decode('utf-8', 'replace')
    if EMAITZA.returncode:
        raise 실행오류('Komandoa hutsegite_balio: ' + ' '.join(str(balio) for balio in Argumentuak) + '\n' + eduki_balio[-10000:])
    return eduki_balio


def atributu_balio(eduki_balio):
    EMAITZA = {}
    for Marra in eduki_balio.splitlines():
        if '=' not in Marra:
            continue
        Izena, balio = Marra.split('=', 1)
        if Izena.startswith('"'):
            Izena = json.loads(Izena)
        if balio.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(balio)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(balio): balio = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atributu_balio formatu_balio errorea: ' + Marra)
        EMAITZA[Izena] = balio
    return EMAITZA


def 등록목록(eduki_balio):
    EMAITZA = {}
    for Marra in eduki_balio.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Marra)
        if 일치: EMAITZA[일치.group(2).lower()] = 일치.group(1)
    return EMAITZA


def kontroleko_batura(Bide_izena):
    balio = hashlib.sha256()
    with Bide_izena.open('rb') as Fitxategia:
        for datuak in iter(lambda: Fitxategia.read(1024 * 1024), b''): balio.update(datuak)
    return balio.hexdigest()


class aplik_abiarazle:
    def __init__(self, erro_balio, Izena, 방식='gui', Komandoa=exekutatu_shell_komando):
        self.erro_balio = Path(erro_balio).resolve()
        self.Izena, self.방식, self.Komandoa = Izena, 방식, Komandoa
        self.보관 = self.erro_balio / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Izena) or Izena in ('.', '..'):
            raise 실행오류('VM 이름은 문자·digitu_balio·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Bide_izena(self, pareko_balio):
        if Path(pareko_balio).is_absolute() or '..' in Path(pareko_balio).parts:
            raise 실행오류('잘못된 관리 Bide_izena: ' + str(pareko_balio))
        EMAITZA = self.보관
        for 부분 in ['.vbox'] + list(Path(pareko_balio).parts):
            if 부분 == '.vbox': EMAITZA = self.보관
            else: EMAITZA = EMAITZA / 부분
            if EMAITZA.is_symlink(): raise 실행오류('Konektatu 경로는 사용하지 않습니다: ' + str(EMAITZA))
        return EMAITZA

    def Irakurri(self):
        Bide_izena = self.Bide_izena('state.json')
        if not Bide_izena.exists(): return None
        Egoera_balio = json.loads(Bide_izena.read_text(encoding='utf-8'))
        if Egoera_balio.get('version') != 1 or Egoera_balio.get('name') != self.Izena:
            raise 실행오류('관리 상태의 VM Izena/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Izena in ('uuid', 'owner'):
            if str(uuid.UUID(Egoera_balio[Izena])) != Egoera_balio[Izena]: raise 실행오류('잘못된 VM identifikatzaile_balio')
        return Egoera_balio

    def Store_balio(self, Egoera_balio):
        helburu_balio_a0fbc067 = self.Bide_izena('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fitxategia:
            json.dump(Egoera_balio, Fitxategia, ensure_ascii=False, indent=2)
            Fitxategia.write('\n')
            임시 = Fitxategia.name
        os.replace(임시, str(helburu_balio_a0fbc067))

    def msinfo32_exe(self, Egoera_balio, 등록됨, oneratu_Egoera=False):
        if Egoera_balio['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atributu_balio(self.Komandoa(['VBoxManage', 'showvminfo', Egoera_balio['uuid'], '--machinereadable']))
        Posizioa = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Bide_izena('machines').resolve() not in Posizioa.parents or msinfo32_exe.get('UUID') != Egoera_balio['uuid']:
            raise 실행오류('이 프로젝트의 VM Ezarpenak Bide_izena/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Komandoa(['VBoxManage', 'getextradata', Egoera_balio['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + Egoera_balio['owner']:
            if oneratu_Egoera and Egoera_balio.get('pending') and 표식 == 'No value set!':
                self.Komandoa(['VBoxManage', 'setextradata', Egoera_balio['uuid'], 'JKOROS/Owner', Egoera_balio['owner']])
            else:
                raise 실행오류('VM jabe_balio 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, Egoera_balio, msinfo32_exe):
        제어기들 = [balio for Izena, balio in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Izena)]
        Onartu_balio = [str(self.Bide_izena(balio)) for balio in Egoera_balio.get('media', [])]
        for Izena, balio in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontrolatzaile) + r'-\d+-\d+', Izena) for kontrolatzaile in 제어기들):
                if balio not in ('none', 'emptydrive') and balio not in Onartu_balio:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + balio)

    def erakutsi_Egoera(self):
        Egoera_balio = self.Irakurri()
        if Egoera_balio is None: return {'name': self.Izena, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Egoera_balio, 등록목록(self.Komandoa(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Egoera_balio['name']), 'uuid': Egoera_balio['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Bide_izena(Egoera_balio['iso'])) if Egoera_balio.get('iso') else None,
                'serial_log': str(self.Bide_izena(Egoera_balio['serial_log'])) if Egoera_balio.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def exekutatu_komando(self):
        Egoera_balio = self.Irakurri()
        등록됨 = 등록목록(self.Komandoa(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Egoera_balio is not None and Egoera_balio['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Egoera_balio, 등록됨, oneratu_Egoera=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 exekutatu_komando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.erakutsi_Egoera()
            self.매체검사(Egoera_balio, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_balio 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Komandoa(['VBoxManage', 'controlvm', Egoera_balio['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Ireki 전에 기존 기록도 보관한다.
                    if Egoera_balio.get('serial_log'):
                        원본 = self.Bide_izena(Egoera_balio['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Bide_izena('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Komandoa(['VBoxManage', 'startvm', Egoera_balio['uuid'], '--type', self.방식])
                return self.erakutsi_Egoera()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ALDATU_MODA 중입니다 ({}). 작업이 끝난 ATZERA_balio 다시 실행하세요.'.format(현재))
        elif Egoera_balio is not None and not Egoera_balio.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Izena in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_balio/exekutatu_komando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Komandoa(['make', '-C', str(self.erro_balio / 'os'), 'iso']), end='')
        원본 = self.erro_balio / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + kontroleko_batura(원본) + '.iso'
        helburu_balio_a0fbc067 = self.Bide_izena(매체)
        helburu_balio_a0fbc067.parent.mkdir(exist_ok=True)
        if helburu_balio_a0fbc067.exists():
            if kontroleko_batura(helburu_balio_a0fbc067) != kontroleko_batura(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(helburu_balio_a0fbc067))
        else:
            with tempfile.NamedTemporaryFile(dir=str(helburu_balio_a0fbc067.parent)) as Fitxategia:
                shutil.copyfile(str(원본), Fitxategia.name)
                os.link(Fitxategia.name, str(helburu_balio_a0fbc067))

        if Egoera_balio is None:
            Egoera_balio = {'version': 1, 'name': self.Izena, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_balio(Egoera_balio)
        if msinfo32_exe is None:
            self.Komandoa(['VBoxManage', 'createvm', '--name', Egoera_balio['name'], '--uuid', Egoera_balio['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Bide_izena('machines')), '--register'])
            self.Komandoa(['VBoxManage', 'setextradata', Egoera_balio['uuid'], 'JKOROS/Owner', Egoera_balio['owner']])
        # eraiki_sistema 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Egoera_balio, 등록목록(self.Komandoa(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('eraiki_sistema 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(Egoera_balio, msinfo32_exe)
        Egoera_balio['iso'] = 매체
        if 매체 not in Egoera_balio['media']: Egoera_balio['media'].append(매체)
        Egoera_balio['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_balio = self.Bide_izena(Egoera_balio['serial_log'])
        LOG_balio.parent.mkdir(exist_ok=True)
        self.Store_balio(Egoera_balio)
        self.Komandoa(['VBoxManage', 'modifyvm', Egoera_balio['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_balio)])
        제어기들 = [balio for Izena, balio in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Izena)]
        if 'JKOROS IDE' not in 제어기들:
            self.Komandoa(['VBoxManage', 'storagectl', Egoera_balio['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Komandoa(['VBoxManage', 'storageattach', Egoera_balio['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(helburu_balio_a0fbc067)])
        Egoera_balio['pending'] = False
        self.Store_balio(Egoera_balio)
        self.Komandoa(['VBoxManage', 'startvm', Egoera_balio['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.erakutsi_Egoera()


def Exekutatu_2():
    analizatu_balio = argparse.ArgumentParser(description='jkoros 전용 VirtualBox exekutatu_komando 및 Egoera_balio kontsulta_balio')
    analizatu_balio.add_argument('action', choices=['run', 'status'])
    parametro_arg = analizatu_balio.parse_args()
    exekutatu_komando = aplik_abiarazle(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametro_arg.action == 'status':
        print(json.dumps(exekutatu_komando.erakutsi_Egoera(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. Ostalari 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/baimen_balio 변경은 하지 않습니다.')
    os.umask(0o077)
    exekutatu_komando.Bide_izena('lock').parent.mkdir(parents=True, exist_ok=True)
    with exekutatu_komando.Bide_izena('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox exekutatu_komando 작업이 진행 중입니다.')
        print(json.dumps(exekutatu_komando.exekutatu_komando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Exekutatu_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as errorea:
        print('VBOX errorea: ' + str(errorea), file=sys.stderr)
        sys.exit(1)
