#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_indító. 기존 VM/디스크/tár_ÉRTÉK 상태는 삭제하지 않는다."""
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


class végrehajtás_hiba(RuntimeError):
    pass


def végrehajt_felület_parancs(Argumentumok):
    környezet_5d36e09c = dict(os.environ, LC_ALL='C')
    KR = subprocess.run([str(ÉRTÉK) for ÉRTÉK in Argumentumok], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=környezet_5d36e09c, timeout=180)
    Tartalom_ÉRTÉK = KR.stdout.decode('utf-8', 'replace')
    if KR.returncode:
        raise végrehajtás_hiba('Parancs hiba_ÉRTÉK: ' + ' '.join(str(ÉRTÉK) for ÉRTÉK in Argumentumok) + '\n' + Tartalom_ÉRTÉK[-10000:])
    return Tartalom_ÉRTÉK


def attribútum_ÉRTÉK(Tartalom_ÉRTÉK):
    KR = {}
    for Vonal in Tartalom_ÉRTÉK.splitlines():
        if '=' not in Vonal:
            continue
        Név, ÉRTÉK = Vonal.split('=', 1)
        if Név.startswith('"'):
            Név = json.loads(Név)
        if ÉRTÉK.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ÉRTÉK)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ÉRTÉK): ÉRTÉK = 읽은값
            except ValueError:
                raise végrehajtás_hiba('VirtualBox attribútum_ÉRTÉK formáz_ÉRTÉK HIBA: ' + Vonal)
        KR[Név] = ÉRTÉK
    return KR


def 등록목록(Tartalom_ÉRTÉK):
    KR = {}
    for Vonal in Tartalom_ÉRTÉK.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Vonal)
        if 일치: KR[일치.group(2).lower()] = 일치.group(1)
    return KR


def ellenőrzőösszeg(ÚTVONAL):
    ÉRTÉK = hashlib.sha256()
    with ÚTVONAL.open('rb') as Fájl:
        for adat in iter(lambda: Fájl.read(1024 * 1024), b''): ÉRTÉK.update(adat)
    return ÉRTÉK.hexdigest()


class app_indító:
    def __init__(self, gyök_ÉRTÉK, Név, metódus_mód='gui', Parancs=végrehajt_felület_parancs):
        self.gyök_ÉRTÉK = Path(gyök_ÉRTÉK).resolve()
        self.Név, self.metódus_mód, self.Parancs = Név, metódus_mód, Parancs
        self.보관 = self.gyök_ÉRTÉK / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Név) or Név in ('.', '..'):
            raise végrehajtás_hiba('VM 이름은 문자·számjegy_ÉRTÉK·공백·밑줄·괄호·마침표·하이픈만 사용할 szám 있습니다.')
        if metódus_mód not in ('gui', 'headless'): raise végrehajtás_hiba('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ÚTVONAL(self, társ_ÉRTÉK):
        if Path(társ_ÉRTÉK).is_absolute() or '..' in Path(társ_ÉRTÉK).parts:
            raise végrehajtás_hiba('잘못된 관리 ÚTVONAL: ' + str(társ_ÉRTÉK))
        KR = self.보관
        for 부분 in ['.vbox'] + list(Path(társ_ÉRTÉK).parts):
            if 부분 == '.vbox': KR = self.보관
            else: KR = KR / 부분
            if KR.is_symlink(): raise végrehajtás_hiba('Kapcsolódás 경로는 사용하지 않습니다: ' + str(KR))
        return KR

    def Olvasás(self):
        ÚTVONAL = self.ÚTVONAL('state.json')
        if not ÚTVONAL.exists(): return None
        Állapot_ÉRTÉK = json.loads(ÚTVONAL.read_text(encoding='utf-8'))
        if Állapot_ÉRTÉK.get('version') != 1 or Állapot_ÉRTÉK.get('name') != self.Név:
            raise végrehajtás_hiba('관리 상태의 VM Név/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Név in ('uuid', 'owner'):
            if str(uuid.UUID(Állapot_ÉRTÉK[Név])) != Állapot_ÉRTÉK[Név]: raise végrehajtás_hiba('잘못된 VM azonosító_ÉRTÉK')
        return Állapot_ÉRTÉK

    def tár_ÉRTÉK(self, Állapot_ÉRTÉK):
        cél_ÉRTÉK = self.ÚTVONAL('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fájl:
            json.dump(Állapot_ÉRTÉK, Fájl, ensure_ascii=False, indent=2)
            Fájl.write('\n')
            임시 = Fájl.name
        os.replace(임시, str(cél_ÉRTÉK))

    def msinfo32_exe(self, Állapot_ÉRTÉK, 등록됨, helyreállít_Állapot=False):
        if Állapot_ÉRTÉK['uuid'] not in 등록됨:
            raise végrehajtás_hiba('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = attribútum_ÉRTÉK(self.Parancs(['VBoxManage', 'showvminfo', Állapot_ÉRTÉK['uuid'], '--machinereadable']))
        Pozíció = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.ÚTVONAL('machines').resolve() not in Pozíció.parents or msinfo32_exe.get('UUID') != Állapot_ÉRTÉK['uuid']:
            raise végrehajtás_hiba('이 프로젝트의 VM Beállítások ÚTVONAL/UUID와 일치하지 않아 변경하지 않습니다.')
        jelölő_ÉRTÉK = self.Parancs(['VBoxManage', 'getextradata', Állapot_ÉRTÉK['uuid'], 'JKOROS/Owner']).strip()
        if jelölő_ÉRTÉK != 'Value: ' + Állapot_ÉRTÉK['owner']:
            if helyreállít_Állapot and Állapot_ÉRTÉK.get('pending') and jelölő_ÉRTÉK == 'No value set!':
                self.Parancs(['VBoxManage', 'setextradata', Állapot_ÉRTÉK['uuid'], 'JKOROS/Owner', Állapot_ÉRTÉK['owner']])
            else:
                raise végrehajtás_hiba('VM tulajdonos_ÉRTÉK 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def csekk_Multimédia(self, Állapot_ÉRTÉK, msinfo32_exe):
        제어기들 = [ÉRTÉK for Név, ÉRTÉK in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Név)]
        engedélyez_ÉRTÉK = [str(self.ÚTVONAL(ÉRTÉK)) for ÉRTÉK in Állapot_ÉRTÉK.get('media', [])]
        for Név, ÉRTÉK in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(vezérlő_8bff480f) + r'-\d+-\d+', Név) for vezérlő_8bff480f in 제어기들):
                if ÉRTÉK not in ('none', 'emptydrive') and ÉRTÉK not in engedélyez_ÉRTÉK:
                    raise végrehajtás_hiba('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ÉRTÉK)

    def bemutató_Állapot(self):
        Állapot_ÉRTÉK = self.Olvasás()
        if Állapot_ÉRTÉK is None: return {'name': self.Név, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Állapot_ÉRTÉK, 등록목록(self.Parancs(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Állapot_ÉRTÉK['name']), 'uuid': Állapot_ÉRTÉK['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.ÚTVONAL(Állapot_ÉRTÉK['iso'])) if Állapot_ÉRTÉK.get('iso') else None,
                'serial_log': str(self.ÚTVONAL(Állapot_ÉRTÉK['serial_log'])) if Állapot_ÉRTÉK.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def végrehajt_parancs(self):
        Állapot_ÉRTÉK = self.Olvasás()
        등록됨 = 등록목록(self.Parancs(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Állapot_ÉRTÉK is not None and Állapot_ÉRTÉK['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Állapot_ÉRTÉK, 등록됨, helyreállít_Állapot=True)
            aktuális_cikk = msinfo32_exe.get('VMState')
            if aktuális_cikk == 'running':
                print('이미 végrehajt_parancs 중입니다. 재빌드·재시작하지 않습니다.')
                return self.bemutató_Állapot()
            self.csekk_Multimédia(Állapot_ÉRTÉK, msinfo32_exe)
            if aktuális_cikk in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 tár_ÉRTÉK 상태를 버리지 않습니다.'.format(aktuális_cikk))
                if aktuális_cikk == 'paused':
                    self.Parancs(['VBoxManage', 'controlvm', Állapot_ÉRTÉK['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 újrapróbál_ÉRTÉK Megnyitás 전에 기존 기록도 보관한다.
                    if Állapot_ÉRTÉK.get('serial_log'):
                        원본 = self.ÚTVONAL(Állapot_ÉRTÉK['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ÚTVONAL('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Parancs(['VBoxManage', 'startvm', Állapot_ÉRTÉK['uuid'], '--type', self.metódus_mód])
                return self.bemutató_Állapot()
            if aktuális_cikk not in ('poweroff', 'aborted'):
                raise végrehajtás_hiba('VM이 vált_mód 중입니다 ({}). 작업이 끝난 BACK_ÉRTÉK újrapróbál_ÉRTÉK 실행하세요.'.format(aktuális_cikk))
        elif Állapot_ÉRTÉK is not None and not Állapot_ÉRTÉK.get('pending'):
            raise végrehajtás_hiba('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 újrapróbál_ÉRTÉK 등록하세요.')
        elif self.Név in 등록됨.values():
            raise végrehajtás_hiba('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # tár_ÉRTÉK/végrehajt_parancs 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Parancs(['make', '-C', str(self.gyök_ÉRTÉK / 'os'), 'iso']), end='')
        원본 = self.gyök_ÉRTÉK / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise végrehajtás_hiba('부팅 ISO가 생성되지 않았습니다.')
        Multimédia_ÉRTÉK = 'media/kernel-' + ellenőrzőösszeg(원본) + '.iso'
        cél_ÉRTÉK = self.ÚTVONAL(Multimédia_ÉRTÉK)
        cél_ÉRTÉK.parent.mkdir(exist_ok=True)
        if cél_ÉRTÉK.exists():
            if ellenőrzőösszeg(cél_ÉRTÉK) != ellenőrzőösszeg(원본): raise végrehajtás_hiba('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(cél_ÉRTÉK))
        else:
            with tempfile.NamedTemporaryFile(dir=str(cél_ÉRTÉK.parent)) as Fájl:
                shutil.copyfile(str(원본), Fájl.name)
                os.link(Fájl.name, str(cél_ÉRTÉK))

        if Állapot_ÉRTÉK is None:
            Állapot_ÉRTÉK = {'version': 1, 'name': self.Név, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.tár_ÉRTÉK(Állapot_ÉRTÉK)
        if msinfo32_exe is None:
            self.Parancs(['VBoxManage', 'createvm', '--name', Állapot_ÉRTÉK['name'], '--uuid', Állapot_ÉRTÉK['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ÚTVONAL('machines')), '--register'])
            self.Parancs(['VBoxManage', 'setextradata', Állapot_ÉRTÉK['uuid'], 'JKOROS/Owner', Állapot_ÉRTÉK['owner']])
        # épít_Rendszer 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Állapot_ÉRTÉK, 등록목록(self.Parancs(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise végrehajtás_hiba('épít_Rendszer 중 VM 상태가 바뀌었습니다. újrapróbál_ÉRTÉK make vbox를 실행하세요.')
        self.csekk_Multimédia(Állapot_ÉRTÉK, msinfo32_exe)
        Állapot_ÉRTÉK['iso'] = Multimédia_ÉRTÉK
        if Multimédia_ÉRTÉK not in Állapot_ÉRTÉK['media']: Állapot_ÉRTÉK['media'].append(Multimédia_ÉRTÉK)
        Állapot_ÉRTÉK['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_ÉRTÉK = self.ÚTVONAL(Állapot_ÉRTÉK['serial_log'])
        LOG_ÉRTÉK.parent.mkdir(exist_ok=True)
        self.tár_ÉRTÉK(Állapot_ÉRTÉK)
        self.Parancs(['VBoxManage', 'modifyvm', Állapot_ÉRTÉK['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_ÉRTÉK)])
        제어기들 = [ÉRTÉK for Név, ÉRTÉK in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Név)]
        if 'JKOROS IDE' not in 제어기들:
            self.Parancs(['VBoxManage', 'storagectl', Állapot_ÉRTÉK['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Parancs(['VBoxManage', 'storageattach', Állapot_ÉRTÉK['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(cél_ÉRTÉK)])
        Állapot_ÉRTÉK['pending'] = False
        self.tár_ÉRTÉK(Állapot_ÉRTÉK)
        self.Parancs(['VBoxManage', 'startvm', Állapot_ÉRTÉK['uuid'], '--type', self.metódus_mód])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.bemutató_Állapot()


def Futtatás():
    elemez_ÉRTÉK = argparse.ArgumentParser(description='jkoros 전용 VirtualBox végrehajt_parancs 및 Állapot_ÉRTÉK lekérdez_ÉRTÉK')
    elemez_ÉRTÉK.add_argument('action', choices=['run', 'status'])
    paraméter_argumentum = elemez_ÉRTÉK.parse_args()
    végrehajt_parancs = app_indító(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if paraméter_argumentum.action == 'status':
        print(json.dumps(végrehajt_parancs.bemutató_Állapot(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise végrehajtás_hiba('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise végrehajtás_hiba('/dev/vboxdrv에 접근할 szám 없습니다. gazda 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/engedély_ÉRTÉK 변경은 하지 않습니다.')
    os.umask(0o077)
    végrehajt_parancs.ÚTVONAL('lock').parent.mkdir(parents=True, exist_ok=True)
    with végrehajt_parancs.ÚTVONAL('lock').open('a') as lezár_ÉRTÉK:
        try: fcntl.flock(lezár_ÉRTÉK, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise végrehajtás_hiba('다른 jkoros VirtualBox végrehajt_parancs 작업이 진행 중입니다.')
        print(json.dumps(végrehajt_parancs.végrehajt_parancs(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Futtatás()
    except (végrehajtás_hiba, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as HIBA:
        print('VBOX HIBA: ' + str(HIBA), file=sys.stderr)
        sys.exit(1)
