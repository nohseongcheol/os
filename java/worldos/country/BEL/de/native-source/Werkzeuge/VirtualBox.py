#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ProgrammStarter. 기존 VM/디스크/ablegenDatenWert 상태는 삭제하지 않는다."""
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


class ausführungFehler(RuntimeError):
    pass


def befehlshülleBefehlAusführen(argumente):
    umgebung = dict(os.environ, LC_ALL='C')
    ergebnis = subprocess.run([str(Wert) for Wert in argumente], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=umgebung, timeout=180)
    inhaltswertWert = ergebnis.stdout.decode('utf-8', 'replace')
    if ergebnis.returncode:
        raise ausführungFehler('befehl fehlschlagWert: ' + ' '.join(str(Wert) for Wert in argumente) + '\n' + inhaltswertWert[-10000:])
    return inhaltswertWert


def attributWert(inhaltswertWert):
    ergebnis = {}
    for zeile in inhaltswertWert.splitlines():
        if '=' not in zeile:
            continue
        Name, Wert = zeile.split('=', 1)
        if Name.startswith('"'):
            Name = json.loads(Name)
        if Wert.startswith('"'):
            try:
                wertLesen, endung = json.JSONDecoder().raw_decode(Wert)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if endung == len(Wert): Wert = wertLesen
            except ValueError:
                raise ausführungFehler('VirtualBox attributWert formatWert fehler: ' + zeile)
        ergebnis[Name] = Wert
    return ergebnis


def angemeldetEinträge(inhaltswertWert):
    ergebnis = {}
    for zeile in inhaltswertWert.splitlines():
        istGleich = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', zeile)
        if istGleich: ergebnis[istGleich.group(2).lower()] = istGleich.group(1)
    return ergebnis


def kontrollsumme(pfad):
    Wert = hashlib.sha256()
    with pfad.open('rb') as Datei:
        for Daten in iter(lambda: Datei.read(1024 * 1024), b''): Wert.update(Daten)
    return Wert.hexdigest()


class ProgrammStarter:
    def __init__(self, wurzelWert, Name, methodeBetriebsart='gui', befehl=befehlshülleBefehlAusführen):
        self.wurzelWert = Path(wurzelWert).resolve()
        self.Name, self.methodeBetriebsart, self.befehl = Name, methodeBetriebsart, befehl
        self.wertBewahren = self.wurzelWert / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Name) or Name in ('.', '..'):
            raise ausführungFehler('VM 이름은 Zeichen·zifferWert·공백·밑줄·괄호·마침표·하이픈만 사용할 Zahl 있습니다.')
        if methodeBetriebsart not in ('gui', 'headless'): raise ausführungFehler('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def pfad(self, gegenstelleWert):
        if Path(gegenstelleWert).is_absolute() or '..' in Path(gegenstelleWert).parts:
            raise ausführungFehler('잘못된 관리 pfad: ' + str(gegenstelleWert))
        ergebnis = self.wertBewahren
        for unterteilWert in ['.vbox'] + list(Path(gegenstelleWert).parts):
            if unterteilWert == '.vbox': ergebnis = self.wertBewahren
            else: ergebnis = ergebnis / unterteilWert
            if ergebnis.is_symlink(): raise ausführungFehler('verbinden 경로는 사용하지 않습니다: ' + str(ergebnis))
        return ergebnis

    def lesen(self):
        pfad = self.pfad('state.json')
        if not pfad.exists(): return None
        statuswertWert = json.loads(pfad.read_text(encoding='utf-8'))
        if statuswertWert.get('version') != 1 or statuswertWert.get('name') != self.Name:
            raise ausführungFehler('관리 상태의 VM Name/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Name in ('uuid', 'owner'):
            if str(uuid.UUID(statuswertWert[Name])) != statuswertWert[Name]: raise ausführungFehler('잘못된 VM bezeichnerWert')
        return statuswertWert

    def ablegenDatenWert(self, statuswertWert):
        zielWert = self.pfad('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.wertBewahren), delete=False) as Datei:
            json.dump(statuswertWert, Datei, ensure_ascii=False, indent=2)
            Datei.write('\n')
            vorläufigWert = Datei.name
        os.replace(vorläufigWert, str(zielWert))

    def systemInformation(self, statuswertWert, angemeldetWert, statuswertWiederherstellen=False):
        if statuswertWert['uuid'] not in angemeldetWert:
            raise ausführungFehler('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        systemInformation = attributWert(self.befehl(['VBoxManage', 'showvminfo', statuswertWert['uuid'], '--machinereadable']))
        position = Path(systemInformation.get('CfgFile', '')).resolve()
        if self.pfad('machines').resolve() not in position.parents or systemInformation.get('UUID') != statuswertWert['uuid']:
            raise ausführungFehler('이 프로젝트의 VM einstellungen pfad/UUID와 일치하지 않아 변경하지 않습니다.')
        markierungWert = self.befehl(['VBoxManage', 'getextradata', statuswertWert['uuid'], 'JKOROS/Owner']).strip()
        if markierungWert != 'Value: ' + statuswertWert['owner']:
            if statuswertWiederherstellen and statuswertWert.get('pending') and markierungWert == 'No value set!':
                self.befehl(['VBoxManage', 'setextradata', statuswertWert['uuid'], 'JKOROS/Owner', statuswertWert['owner']])
            else:
                raise ausführungFehler('VM eigentümerWert 표식이 일치하지 않아 변경하지 않습니다.')
        return systemInformation

    def medienPrüfen(self, statuswertWert, systemInformation):
        steuereinheitenListe = [Wert for Name, Wert in systemInformation.items() if re.fullmatch(r'storagecontrollername\d+', Name)]
        wertErlauben = [str(self.pfad(Wert)) for Wert in statuswertWert.get('media', [])]
        for Name, Wert in systemInformation.items():
            if any(re.fullmatch(re.escape(Steuereinheit) + r'-\d+-\d+', Name) for Steuereinheit in steuereinheitenListe):
                if Wert not in ('none', 'emptydrive') and Wert not in wertErlauben:
                    raise ausführungFehler('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + Wert)

    def statuswertAnzeigen(self):
        statuswertWert = self.lesen()
        if statuswertWert is None: return {'name': self.Name, 'state': 'not-created'}
        systemInformation = self.systemInformation(statuswertWert, angemeldetEinträge(self.befehl(['VBoxManage', 'list', 'vms'])))
        return {'name': systemInformation.get('name', statuswertWert['name']), 'uuid': statuswertWert['uuid'], 'state': systemInformation.get('VMState'),
                'iso': str(self.pfad(statuswertWert['iso'])) if statuswertWert.get('iso') else None,
                'serial_log': str(self.pfad(statuswertWert['serial_log'])) if statuswertWert.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def befehlAusführen(self):
        statuswertWert = self.lesen()
        angemeldetWert = angemeldetEinträge(self.befehl(['VBoxManage', 'list', 'vms']))
        systemInformation = None
        if statuswertWert is not None and statuswertWert['uuid'] in angemeldetWert:
            systemInformation = self.systemInformation(statuswertWert, angemeldetWert, statuswertWiederherstellen=True)
            aktuellElementeintrag = systemInformation.get('VMState')
            if aktuellElementeintrag == 'running':
                print('이미 befehlAusführen 중입니다. 재빌드·재시작하지 않습니다.')
                return self.statuswertAnzeigen()
            self.medienPrüfen(statuswertWert, systemInformation)
            if aktuellElementeintrag in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ablegenDatenWert 상태를 버리지 않습니다.'.format(aktuellElementeintrag))
                if aktuellElementeintrag == 'paused':
                    self.befehl(['VBoxManage', 'controlvm', statuswertWert['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 erneutVersuchenWert öffnen 전에 기존 기록도 보관한다.
                    if statuswertWert.get('serial_log'):
                        ursprünglich = self.pfad(statuswertWert['serial_log'])
                        if ursprünglich.is_file():
                            shutil.copyfile(str(ursprünglich), str(self.pfad('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.befehl(['VBoxManage', 'startvm', statuswertWert['uuid'], '--type', self.methodeBetriebsart])
                return self.statuswertAnzeigen()
            if aktuellElementeintrag not in ('poweroff', 'aborted'):
                raise ausführungFehler('VM이 umschaltenBetriebsart 중입니다 ({}). 작업이 끝난 rückseiteWert erneutVersuchenWert 실행하세요.'.format(aktuellElementeintrag))
        elif statuswertWert is not None and not statuswertWert.get('pending'):
            raise ausführungFehler('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 erneutVersuchenWert 등록하세요.')
        elif self.Name in angemeldetWert.values():
            raise ausführungFehler('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ablegenDatenWert/befehlAusführen 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.befehl(['make', '-C', str(self.wurzelWert / 'os'), 'iso']), end='')
        ursprünglich = self.wurzelWert / 'os/build/kernel.iso'
        if not ursprünglich.is_file() or ursprünglich.stat().st_size == 0: raise ausführungFehler('Startvorgang ISO가 생성되지 않았습니다.')
        medienWert = 'media/kernel-' + kontrollsumme(ursprünglich) + '.iso'
        zielWert = self.pfad(medienWert)
        zielWert.parent.mkdir(exist_ok=True)
        if zielWert.exists():
            if kontrollsumme(zielWert) != kontrollsumme(ursprünglich): raise ausführungFehler('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(zielWert))
        else:
            with tempfile.NamedTemporaryFile(dir=str(zielWert.parent)) as Datei:
                shutil.copyfile(str(ursprünglich), Datei.name)
                os.link(Datei.name, str(zielWert))

        if statuswertWert is None:
            statuswertWert = {'version': 1, 'name': self.Name, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ablegenDatenWert(statuswertWert)
        if systemInformation is None:
            self.befehl(['VBoxManage', 'createvm', '--name', statuswertWert['name'], '--uuid', statuswertWert['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.pfad('machines')), '--register'])
            self.befehl(['VBoxManage', 'setextradata', statuswertWert['uuid'], 'JKOROS/Owner', statuswertWert['owner']])
        # systemErzeugenAbbild 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        systemInformation = self.systemInformation(statuswertWert, angemeldetEinträge(self.befehl(['VBoxManage', 'list', 'vms'])))
        if systemInformation.get('VMState') not in ('poweroff', 'aborted'):
            raise ausführungFehler('systemErzeugenAbbild 중 VM 상태가 바뀌었습니다. erneutVersuchenWert make vbox를 실행하세요.')
        self.medienPrüfen(statuswertWert, systemInformation)
        statuswertWert['iso'] = medienWert
        if medienWert not in statuswertWert['media']: statuswertWert['media'].append(medienWert)
        statuswertWert['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        protokolldateiWert = self.pfad(statuswertWert['serial_log'])
        protokolldateiWert.parent.mkdir(exist_ok=True)
        self.ablegenDatenWert(statuswertWert)
        self.befehl(['VBoxManage', 'modifyvm', statuswertWert['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(protokolldateiWert)])
        steuereinheitenListe = [Wert for Name, Wert in systemInformation.items() if re.fullmatch(r'storagecontrollername\d+', Name)]
        if 'JKOROS IDE' not in steuereinheitenListe:
            self.befehl(['VBoxManage', 'storagectl', statuswertWert['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.befehl(['VBoxManage', 'storageattach', statuswertWert['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(zielWert)])
        statuswertWert['pending'] = False
        self.ablegenDatenWert(statuswertWert)
        self.befehl(['VBoxManage', 'startvm', statuswertWert['uuid'], '--type', self.methodeBetriebsart])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.statuswertAnzeigen()


def ausführenVorgang():
    wertAnalysieren = argparse.ArgumentParser(description='jkoros 전용 VirtualBox befehlAusführen 및 statuswertWert abfragenWert')
    wertAnalysieren.add_argument('action', choices=['run', 'status'])
    parameterArgument = wertAnalysieren.parse_args()
    befehlAusführen = ProgrammStarter(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameterArgument.action == 'status':
        print(json.dumps(befehlAusführen.statuswertAnzeigen(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise ausführungFehler('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise ausführungFehler('/dev/vboxdrv에 접근할 Zahl 없습니다. Wirtssystem 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/erlaubnisWert 변경은 하지 않습니다.')
    os.umask(0o077)
    befehlAusführen.pfad('lock').parent.mkdir(parents=True, exist_ok=True)
    with befehlAusführen.pfad('lock').open('a') as sperreWert:
        try: fcntl.flock(sperreWert, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise ausführungFehler('다른 jkoros VirtualBox befehlAusführen 작업이 진행 중입니다.')
        print(json.dumps(befehlAusführen.befehlAusführen(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ausführenVorgang()
    except (ausführungFehler, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as fehler:
        print('VBOX fehler: ' + str(fehler), file=sys.stderr)
        sys.exit(1)
