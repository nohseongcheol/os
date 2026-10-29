#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_Launcher. 기존 VM/디스크/Store_HODNOTA 상태는 삭제하지 않는다."""
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


class spuštění_chyba_3f02a041(RuntimeError):
    pass


def Provést_prostředí_příkaz(argumenty):
    prostředí_5d36e09c = dict(os.environ, LC_ALL='C')
    VÝSLEDEK = subprocess.run([str(HODNOTA) for HODNOTA in argumenty], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=prostředí_5d36e09c, timeout=180)
    Obsah_HODNOTA = VÝSLEDEK.stdout.decode('utf-8', 'replace')
    if VÝSLEDEK.returncode:
        raise spuštění_chyba_3f02a041('příkaz selhání_HODNOTA: ' + ' '.join(str(HODNOTA) for HODNOTA in argumenty) + '\n' + Obsah_HODNOTA[-10000:])
    return Obsah_HODNOTA


def hodnota_atributu(Obsah_HODNOTA):
    VÝSLEDEK = {}
    for vstupní_řádek in Obsah_HODNOTA.splitlines():
        if '=' not in vstupní_řádek:
            continue
        Název, HODNOTA = vstupní_řádek.split('=', 1)
        if Název.startswith('"'):
            Název = json.loads(Název)
        if HODNOTA.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(HODNOTA)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(HODNOTA): HODNOTA = 읽은값
            except ValueError:
                raise spuštění_chyba_3f02a041('VirtualBox hodnota_atributu formát_HODNOTA chyba: ' + vstupní_řádek)
        VÝSLEDEK[Název] = HODNOTA
    return VÝSLEDEK


def 등록목록(Obsah_HODNOTA):
    VÝSLEDEK = {}
    for vstupní_řádek in Obsah_HODNOTA.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', vstupní_řádek)
        if 일치: VÝSLEDEK[일치.group(2).lower()] = 일치.group(1)
    return VÝSLEDEK


def kontrolní_součet(cesta_2):
    HODNOTA = hashlib.sha256()
    with cesta_2.open('rb') as název_souboru:
        for data in iter(lambda: název_souboru.read(1024 * 1024), b''): HODNOTA.update(data)
    return HODNOTA.hexdigest()


class program_Launcher:
    def __init__(self, kořen_HODNOTA, Název, metoda_MODE='gui', příkaz=Provést_prostředí_příkaz):
        self.kořen_HODNOTA = Path(kořen_HODNOTA).resolve()
        self.Název, self.metoda_MODE, self.příkaz = Název, metoda_MODE, příkaz
        self.보관 = self.kořen_HODNOTA / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Název) or Název in ('.', '..'):
            raise spuštění_chyba_3f02a041('VM 이름은 문자·číslice_HODNOTA·공백·밑줄·괄호·마침표·하이픈만 사용할 číslo 있습니다.')
        if metoda_MODE not in ('gui', 'headless'): raise spuštění_chyba_3f02a041('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def cesta_2(self, partner_HODNOTA):
        if Path(partner_HODNOTA).is_absolute() or '..' in Path(partner_HODNOTA).parts:
            raise spuštění_chyba_3f02a041('잘못된 관리 cesta_2: ' + str(partner_HODNOTA))
        VÝSLEDEK = self.보관
        for 부분 in ['.vbox'] + list(Path(partner_HODNOTA).parts):
            if 부분 == '.vbox': VÝSLEDEK = self.보관
            else: VÝSLEDEK = VÝSLEDEK / 부분
            if VÝSLEDEK.is_symlink(): raise spuštění_chyba_3f02a041('Připojit 경로는 사용하지 않습니다: ' + str(VÝSLEDEK))
        return VÝSLEDEK

    def Čtení(self):
        cesta_2 = self.cesta_2('state.json')
        if not cesta_2.exists(): return None
        Stav_HODNOTA = json.loads(cesta_2.read_text(encoding='utf-8'))
        if Stav_HODNOTA.get('version') != 1 or Stav_HODNOTA.get('name') != self.Název:
            raise spuštění_chyba_3f02a041('관리 상태의 VM Název/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Název in ('uuid', 'owner'):
            if str(uuid.UUID(Stav_HODNOTA[Název])) != Stav_HODNOTA[Název]: raise spuštění_chyba_3f02a041('잘못된 VM identifikátor_HODNOTA')
        return Stav_HODNOTA

    def Store_HODNOTA(self, Stav_HODNOTA):
        cíl_HODNOTA = self.cesta_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as název_souboru:
            json.dump(Stav_HODNOTA, název_souboru, ensure_ascii=False, indent=2)
            název_souboru.write('\n')
            임시 = název_souboru.name
        os.replace(임시, str(cíl_HODNOTA))

    def Informace_o_systému(self, Stav_HODNOTA, 등록됨, zotavit_Stav=False):
        if Stav_HODNOTA['uuid'] not in 등록됨:
            raise spuštění_chyba_3f02a041('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Informace_o_systému = hodnota_atributu(self.příkaz(['VBoxManage', 'showvminfo', Stav_HODNOTA['uuid'], '--machinereadable']))
        pozice = Path(Informace_o_systému.get('CfgFile', '')).resolve()
        if self.cesta_2('machines').resolve() not in pozice.parents or Informace_o_systému.get('UUID') != Stav_HODNOTA['uuid']:
            raise spuštění_chyba_3f02a041('이 프로젝트의 VM Nastavení cesta_2/UUID와 일치하지 않아 변경하지 않습니다.')
        značka_HODNOTA_7e8f90bd = self.příkaz(['VBoxManage', 'getextradata', Stav_HODNOTA['uuid'], 'JKOROS/Owner']).strip()
        if značka_HODNOTA_7e8f90bd != 'Value: ' + Stav_HODNOTA['owner']:
            if zotavit_Stav and Stav_HODNOTA.get('pending') and značka_HODNOTA_7e8f90bd == 'No value set!':
                self.příkaz(['VBoxManage', 'setextradata', Stav_HODNOTA['uuid'], 'JKOROS/Owner', Stav_HODNOTA['owner']])
            else:
                raise spuštění_chyba_3f02a041('VM vlastník_HODNOTA 표식이 일치하지 않아 변경하지 않습니다.')
        return Informace_o_systému

    def šek_média(self, Stav_HODNOTA, Informace_o_systému):
        제어기들 = [HODNOTA for Název, HODNOTA in Informace_o_systému.items() if re.fullmatch(r'storagecontrollername\d+', Název)]
        Povolit_HODNOTA = [str(self.cesta_2(HODNOTA)) for HODNOTA in Stav_HODNOTA.get('media', [])]
        for Název, HODNOTA in Informace_o_systému.items():
            if any(re.fullmatch(re.escape(ovladač) + r'-\d+-\d+', Název) for ovladač in 제어기들):
                if HODNOTA not in ('none', 'emptydrive') and HODNOTA not in Povolit_HODNOTA:
                    raise spuštění_chyba_3f02a041('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + HODNOTA)

    def zobrazit_Stav(self):
        Stav_HODNOTA = self.Čtení()
        if Stav_HODNOTA is None: return {'name': self.Název, 'state': 'not-created'}
        Informace_o_systému = self.Informace_o_systému(Stav_HODNOTA, 등록목록(self.příkaz(['VBoxManage', 'list', 'vms'])))
        return {'name': Informace_o_systému.get('name', Stav_HODNOTA['name']), 'uuid': Stav_HODNOTA['uuid'], 'state': Informace_o_systému.get('VMState'),
                'iso': str(self.cesta_2(Stav_HODNOTA['iso'])) if Stav_HODNOTA.get('iso') else None,
                'serial_log': str(self.cesta_2(Stav_HODNOTA['serial_log'])) if Stav_HODNOTA.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Provést_příkaz(self):
        Stav_HODNOTA = self.Čtení()
        등록됨 = 등록목록(self.příkaz(['VBoxManage', 'list', 'vms']))
        Informace_o_systému = None
        if Stav_HODNOTA is not None and Stav_HODNOTA['uuid'] in 등록됨:
            Informace_o_systému = self.Informace_o_systému(Stav_HODNOTA, 등록됨, zotavit_Stav=True)
            dobrá_zboží = Informace_o_systému.get('VMState')
            if dobrá_zboží == 'running':
                print('이미 Provést_příkaz 중입니다. 재빌드·재시작하지 않습니다.')
                return self.zobrazit_Stav()
            self.šek_média(Stav_HODNOTA, Informace_o_systému)
            if dobrá_zboží in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_HODNOTA 상태를 버리지 않습니다.'.format(dobrá_zboží))
                if dobrá_zboží == 'paused':
                    self.příkaz(['VBoxManage', 'controlvm', Stav_HODNOTA['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 zkusit_znovu_HODNOTA Otevřít 전에 기존 기록도 보관한다.
                    if Stav_HODNOTA.get('serial_log'):
                        원본 = self.cesta_2(Stav_HODNOTA['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.cesta_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.příkaz(['VBoxManage', 'startvm', Stav_HODNOTA['uuid'], '--type', self.metoda_MODE])
                return self.zobrazit_Stav()
            if dobrá_zboží not in ('poweroff', 'aborted'):
                raise spuštění_chyba_3f02a041('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 BACK_HODNOTA zkusit_znovu_HODNOTA 실행하세요.'.format(dobrá_zboží))
        elif Stav_HODNOTA is not None and not Stav_HODNOTA.get('pending'):
            raise spuštění_chyba_3f02a041('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 zkusit_znovu_HODNOTA 등록하세요.')
        elif self.Název in 등록됨.values():
            raise spuštění_chyba_3f02a041('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_HODNOTA/Provést_příkaz 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.příkaz(['make', '-C', str(self.kořen_HODNOTA / 'os'), 'iso']), end='')
        원본 = self.kořen_HODNOTA / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise spuštění_chyba_3f02a041('spuštění_stroje ISO가 생성되지 않았습니다.')
        média_HODNOTA = 'media/kernel-' + kontrolní_součet(원본) + '.iso'
        cíl_HODNOTA = self.cesta_2(média_HODNOTA)
        cíl_HODNOTA.parent.mkdir(exist_ok=True)
        if cíl_HODNOTA.exists():
            if kontrolní_součet(cíl_HODNOTA) != kontrolní_součet(원본): raise spuštění_chyba_3f02a041('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(cíl_HODNOTA))
        else:
            with tempfile.NamedTemporaryFile(dir=str(cíl_HODNOTA.parent)) as název_souboru:
                shutil.copyfile(str(원본), název_souboru.name)
                os.link(název_souboru.name, str(cíl_HODNOTA))

        if Stav_HODNOTA is None:
            Stav_HODNOTA = {'version': 1, 'name': self.Název, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_HODNOTA(Stav_HODNOTA)
        if Informace_o_systému is None:
            self.příkaz(['VBoxManage', 'createvm', '--name', Stav_HODNOTA['name'], '--uuid', Stav_HODNOTA['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.cesta_2('machines')), '--register'])
            self.příkaz(['VBoxManage', 'setextradata', Stav_HODNOTA['uuid'], 'JKOROS/Owner', Stav_HODNOTA['owner']])
        # BLD_Systém 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Informace_o_systému = self.Informace_o_systému(Stav_HODNOTA, 등록목록(self.příkaz(['VBoxManage', 'list', 'vms'])))
        if Informace_o_systému.get('VMState') not in ('poweroff', 'aborted'):
            raise spuštění_chyba_3f02a041('BLD_Systém 중 VM 상태가 바뀌었습니다. zkusit_znovu_HODNOTA make vbox를 실행하세요.')
        self.šek_média(Stav_HODNOTA, Informace_o_systému)
        Stav_HODNOTA['iso'] = média_HODNOTA
        if média_HODNOTA not in Stav_HODNOTA['media']: Stav_HODNOTA['media'].append(média_HODNOTA)
        Stav_HODNOTA['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOGZ_HODNOTA = self.cesta_2(Stav_HODNOTA['serial_log'])
        LOGZ_HODNOTA.parent.mkdir(exist_ok=True)
        self.Store_HODNOTA(Stav_HODNOTA)
        self.příkaz(['VBoxManage', 'modifyvm', Stav_HODNOTA['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOGZ_HODNOTA)])
        제어기들 = [HODNOTA for Název, HODNOTA in Informace_o_systému.items() if re.fullmatch(r'storagecontrollername\d+', Název)]
        if 'JKOROS IDE' not in 제어기들:
            self.příkaz(['VBoxManage', 'storagectl', Stav_HODNOTA['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.příkaz(['VBoxManage', 'storageattach', Stav_HODNOTA['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(cíl_HODNOTA)])
        Stav_HODNOTA['pending'] = False
        self.Store_HODNOTA(Stav_HODNOTA)
        self.příkaz(['VBoxManage', 'startvm', Stav_HODNOTA['uuid'], '--type', self.metoda_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.zobrazit_Stav()


def Spustit_2():
    parsovat_HODNOTA = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Provést_příkaz 및 Stav_HODNOTA dotaz_HODNOTA')
    parsovat_HODNOTA.add_argument('action', choices=['run', 'status'])
    parametr_argument = parsovat_HODNOTA.parse_args()
    Provést_příkaz = program_Launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametr_argument.action == 'status':
        print(json.dumps(Provést_příkaz.zobrazit_Stav(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise spuštění_chyba_3f02a041('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise spuštění_chyba_3f02a041('/dev/vboxdrv에 접근할 číslo 없습니다. hostit 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/oprávnění_HODNOTA 변경은 하지 않습니다.')
    os.umask(0o077)
    Provést_příkaz.cesta_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with Provést_příkaz.cesta_2('lock').open('a') as zámek_HODNOTA:
        try: fcntl.flock(zámek_HODNOTA, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise spuštění_chyba_3f02a041('다른 jkoros VirtualBox Provést_příkaz 작업이 진행 중입니다.')
        print(json.dumps(Provést_příkaz.Provést_příkaz(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Spustit_2()
    except (spuštění_chyba_3f02a041, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as chyba:
        print('VBOX chyba: ' + str(chyba), file=sys.stderr)
        sys.exit(1)
