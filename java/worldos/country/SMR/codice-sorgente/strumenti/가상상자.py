#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_Launcher. 기존 VM/디스크/Store_VALORE 상태는 삭제하지 않는다."""
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


class esecuzione_errore(RuntimeError):
    pass


def Esegui_Shell_comando(argomenti):
    ambiente = dict(os.environ, LC_ALL='C')
    risultato = subprocess.run([str(VALORE) for VALORE in argomenti], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=ambiente, timeout=180)
    Contenuto_VALORE = risultato.stdout.decode('utf-8', 'replace')
    if risultato.returncode:
        raise esecuzione_errore('comando errore_VALORE: ' + ' '.join(str(VALORE) for VALORE in argomenti) + '\n' + Contenuto_VALORE[-10000:])
    return Contenuto_VALORE


def valore_dell_attributo(Contenuto_VALORE):
    risultato = {}
    for riga_di_ingresso in Contenuto_VALORE.splitlines():
        if '=' not in riga_di_ingresso:
            continue
        Nome, VALORE = riga_di_ingresso.split('=', 1)
        if Nome.startswith('"'):
            Nome = json.loads(Nome)
        if VALORE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALORE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALORE): VALORE = 읽은값
            except ValueError:
                raise esecuzione_errore('VirtualBox valore_dell_attributo formato_VALORE errore: ' + riga_di_ingresso)
        risultato[Nome] = VALORE
    return risultato


def 등록목록(Contenuto_VALORE):
    risultato = {}
    for riga_di_ingresso in Contenuto_VALORE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', riga_di_ingresso)
        if 일치: risultato[일치.group(2).lower()] = 일치.group(1)
    return risultato


def checksum(percorso):
    VALORE = hashlib.sha256()
    with percorso.open('rb') as file:
        for dati in iter(lambda: file.read(1024 * 1024), b''): VALORE.update(dati)
    return VALORE.hexdigest()


class app_Launcher:
    def __init__(self, radice_VALORE, Nome, metodo_MODA='gui', comando=Esegui_Shell_comando):
        self.radice_VALORE = Path(radice_VALORE).resolve()
        self.Nome, self.metodo_MODA, self.comando = Nome, metodo_MODA, comando
        self.보관 = self.radice_VALORE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nome) or Nome in ('.', '..'):
            raise esecuzione_errore('VM 이름은 문자·cifra_VALORE·공백·밑줄·괄호·마침표·하이픈만 사용할 numero 있습니다.')
        if metodo_MODA not in ('gui', 'headless'): raise esecuzione_errore('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def percorso(self, peer_VALORE):
        if Path(peer_VALORE).is_absolute() or '..' in Path(peer_VALORE).parts:
            raise esecuzione_errore('잘못된 관리 percorso: ' + str(peer_VALORE))
        risultato = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_VALORE).parts):
            if 부분 == '.vbox': risultato = self.보관
            else: risultato = risultato / 부분
            if risultato.is_symlink(): raise esecuzione_errore('Connetti 경로는 사용하지 않습니다: ' + str(risultato))
        return risultato

    def Lettura(self):
        percorso = self.percorso('state.json')
        if not percorso.exists(): return None
        Stato_VALORE = json.loads(percorso.read_text(encoding='utf-8'))
        if Stato_VALORE.get('version') != 1 or Stato_VALORE.get('name') != self.Nome:
            raise esecuzione_errore('관리 상태의 VM Nome/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nome in ('uuid', 'owner'):
            if str(uuid.UUID(Stato_VALORE[Nome])) != Stato_VALORE[Nome]: raise esecuzione_errore('잘못된 VM identificatore_VALORE')
        return Stato_VALORE

    def Store_VALORE(self, Stato_VALORE):
        meta_VALORE = self.percorso('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as file:
            json.dump(Stato_VALORE, file, ensure_ascii=False, indent=2)
            file.write('\n')
            임시 = file.name
        os.replace(임시, str(meta_VALORE))

    def msinfo32_exe(self, Stato_VALORE, 등록됨, recuperare_Stato=False):
        if Stato_VALORE['uuid'] not in 등록됨:
            raise esecuzione_errore('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = valore_dell_attributo(self.comando(['VBoxManage', 'showvminfo', Stato_VALORE['uuid'], '--machinereadable']))
        posizione = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.percorso('machines').resolve() not in posizione.parents or msinfo32_exe.get('UUID') != Stato_VALORE['uuid']:
            raise esecuzione_errore('이 프로젝트의 VM Impostazioni percorso/UUID와 일치하지 않아 변경하지 않습니다.')
        marcatore_VALORE = self.comando(['VBoxManage', 'getextradata', Stato_VALORE['uuid'], 'JKOROS/Owner']).strip()
        if marcatore_VALORE != 'Value: ' + Stato_VALORE['owner']:
            if recuperare_Stato and Stato_VALORE.get('pending') and marcatore_VALORE == 'No value set!':
                self.comando(['VBoxManage', 'setextradata', Stato_VALORE['uuid'], 'JKOROS/Owner', Stato_VALORE['owner']])
            else:
                raise esecuzione_errore('VM proprietario_VALORE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def assegno_supporti(self, Stato_VALORE, msinfo32_exe):
        제어기들 = [VALORE for Nome, VALORE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nome)]
        Consenti_VALORE = [str(self.percorso(VALORE)) for VALORE in Stato_VALORE.get('media', [])]
        for Nome, VALORE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(titolare) + r'-\d+-\d+', Nome) for titolare in 제어기들):
                if VALORE not in ('none', 'emptydrive') and VALORE not in Consenti_VALORE:
                    raise esecuzione_errore('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALORE)

    def mostrare_Stato(self):
        Stato_VALORE = self.Lettura()
        if Stato_VALORE is None: return {'name': self.Nome, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Stato_VALORE, 등록목록(self.comando(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Stato_VALORE['name']), 'uuid': Stato_VALORE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.percorso(Stato_VALORE['iso'])) if Stato_VALORE.get('iso') else None,
                'serial_log': str(self.percorso(Stato_VALORE['serial_log'])) if Stato_VALORE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Esegui_comando(self):
        Stato_VALORE = self.Lettura()
        등록됨 = 등록목록(self.comando(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Stato_VALORE is not None and Stato_VALORE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Stato_VALORE, 등록됨, recuperare_Stato=True)
            Regolari_articolo = msinfo32_exe.get('VMState')
            if Regolari_articolo == 'running':
                print('이미 Esegui_comando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.mostrare_Stato()
            self.assegno_supporti(Stato_VALORE, msinfo32_exe)
            if Regolari_articolo in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALORE 상태를 버리지 않습니다.'.format(Regolari_articolo))
                if Regolari_articolo == 'paused':
                    self.comando(['VBoxManage', 'controlvm', Stato_VALORE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 retry_VALORE Apri 전에 기존 기록도 보관한다.
                    if Stato_VALORE.get('serial_log'):
                        원본 = self.percorso(Stato_VALORE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.percorso('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.comando(['VBoxManage', 'startvm', Stato_VALORE['uuid'], '--type', self.metodo_MODA])
                return self.mostrare_Stato()
            if Regolari_articolo not in ('poweroff', 'aborted'):
                raise esecuzione_errore('VM이 SWITCH_MODA 중입니다 ({}). 작업이 끝난 BACK_VALORE retry_VALORE 실행하세요.'.format(Regolari_articolo))
        elif Stato_VALORE is not None and not Stato_VALORE.get('pending'):
            raise esecuzione_errore('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 retry_VALORE 등록하세요.')
        elif self.Nome in 등록됨.values():
            raise esecuzione_errore('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALORE/Esegui_comando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.comando(['make', '-C', str(self.radice_VALORE / 'os'), 'iso']), end='')
        원본 = self.radice_VALORE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise esecuzione_errore('avvio_macchina ISO가 생성되지 않았습니다.')
        supporti_VALORE = 'media/kernel-' + checksum(원본) + '.iso'
        meta_VALORE = self.percorso(supporti_VALORE)
        meta_VALORE.parent.mkdir(exist_ok=True)
        if meta_VALORE.exists():
            if checksum(meta_VALORE) != checksum(원본): raise esecuzione_errore('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(meta_VALORE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(meta_VALORE.parent)) as file:
                shutil.copyfile(str(원본), file.name)
                os.link(file.name, str(meta_VALORE))

        if Stato_VALORE is None:
            Stato_VALORE = {'version': 1, 'name': self.Nome, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALORE(Stato_VALORE)
        if msinfo32_exe is None:
            self.comando(['VBoxManage', 'createvm', '--name', Stato_VALORE['name'], '--uuid', Stato_VALORE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.percorso('machines')), '--register'])
            self.comando(['VBoxManage', 'setextradata', Stato_VALORE['uuid'], 'JKOROS/Owner', Stato_VALORE['owner']])
        # costruire 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Stato_VALORE, 등록목록(self.comando(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise esecuzione_errore('costruire 중 VM 상태가 바뀌었습니다. retry_VALORE make vbox를 실행하세요.')
        self.assegno_supporti(Stato_VALORE, msinfo32_exe)
        Stato_VALORE['iso'] = supporti_VALORE
        if supporti_VALORE not in Stato_VALORE['media']: Stato_VALORE['media'].append(supporti_VALORE)
        Stato_VALORE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALORE = self.percorso(Stato_VALORE['serial_log'])
        LOG_VALORE.parent.mkdir(exist_ok=True)
        self.Store_VALORE(Stato_VALORE)
        self.comando(['VBoxManage', 'modifyvm', Stato_VALORE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALORE)])
        제어기들 = [VALORE for Nome, VALORE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nome)]
        if 'JKOROS IDE' not in 제어기들:
            self.comando(['VBoxManage', 'storagectl', Stato_VALORE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.comando(['VBoxManage', 'storageattach', Stato_VALORE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(meta_VALORE)])
        Stato_VALORE['pending'] = False
        self.Store_VALORE(Stato_VALORE)
        self.comando(['VBoxManage', 'startvm', Stato_VALORE['uuid'], '--type', self.metodo_MODA])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.mostrare_Stato()


def avvia():
    analizzare_VALORE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Esegui_comando 및 Stato_VALORE query_VALORE')
    analizzare_VALORE.add_argument('action', choices=['run', 'status'])
    parametro_argomento = analizzare_VALORE.parse_args()
    Esegui_comando = app_Launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametro_argomento.action == 'status':
        print(json.dumps(Esegui_comando.mostrare_Stato(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise esecuzione_errore('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise esecuzione_errore('/dev/vboxdrv에 접근할 numero 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/privilegio_VALORE 변경은 하지 않습니다.')
    os.umask(0o077)
    Esegui_comando.percorso('lock').parent.mkdir(parents=True, exist_ok=True)
    with Esegui_comando.percorso('lock').open('a') as blocco_VALORE_978a15a5:
        try: fcntl.flock(blocco_VALORE_978a15a5, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise esecuzione_errore('다른 jkoros VirtualBox Esegui_comando 작업이 진행 중입니다.')
        print(json.dumps(Esegui_comando.Esegui_comando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: avvia()
    except (esecuzione_errore, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as errore:
        print('VBOX errore: ' + str(errore), file=sys.stderr)
        sys.exit(1)
