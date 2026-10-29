#!/usr/bin/env python3
"""jkoros 전용 VirtualBox εφαρμογή_εκκίνηση. 기존 VM/디스크/αποθηκεύω_τιμή 상태는 삭제하지 않는다."""
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


class εκτέλεση_σφάλμα(RuntimeError):
    pass


def εκτελώ_κέλυφος_εντολή(Παράμετροι):
    περιβάλλον_5d36e09c = dict(os.environ, LC_ALL='C')
    μέτρηση = subprocess.run([str(τιμή) for τιμή in Παράμετροι], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=περιβάλλον_5d36e09c, timeout=180)
    Περιεχόμενο_τιμή = μέτρηση.stdout.decode('utf-8', 'replace')
    if μέτρηση.returncode:
        raise εκτέλεση_σφάλμα('Εντολή αποτυχία_τιμή: ' + ' '.join(str(τιμή) for τιμή in Παράμετροι) + '\n' + Περιεχόμενο_τιμή[-10000:])
    return Περιεχόμενο_τιμή


def χαρακτηριστικό_τιμή_286d43f0(Περιεχόμενο_τιμή):
    μέτρηση = {}
    for Γραμμή in Περιεχόμενο_τιμή.splitlines():
        if '=' not in Γραμμή:
            continue
        Όνομα, τιμή = Γραμμή.split('=', 1)
        if Όνομα.startswith('"'):
            Όνομα = json.loads(Όνομα)
        if τιμή.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(τιμή)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(τιμή): τιμή = 읽은값
            except ValueError:
                raise εκτέλεση_σφάλμα('VirtualBox χαρακτηριστικό_τιμή_286d43f0 μορφή_τιμή ΣΦΑΛΜΑ: ' + Γραμμή)
        μέτρηση[Όνομα] = τιμή
    return μέτρηση


def 등록목록(Περιεχόμενο_τιμή):
    μέτρηση = {}
    for Γραμμή in Περιεχόμενο_τιμή.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Γραμμή)
        if 일치: μέτρηση[일치.group(2).lower()] = 일치.group(1)
    return μέτρηση


def άθροισμα_ελέγχου(ΔΙΑΔΡΟΜΗ):
    τιμή = hashlib.sha256()
    with ΔΙΑΔΡΟΜΗ.open('rb') as Αρχείο:
        for δεδομένα in iter(lambda: Αρχείο.read(1024 * 1024), b''): τιμή.update(δεδομένα)
    return τιμή.hexdigest()


class εφαρμογή_εκκίνηση:
    def __init__(self, ρίζα_τιμή, Όνομα, μέθοδος_λειτουργία='gui', Εντολή=εκτελώ_κέλυφος_εντολή):
        self.ρίζα_τιμή = Path(ρίζα_τιμή).resolve()
        self.Όνομα, self.μέθοδος_λειτουργία, self.Εντολή = Όνομα, μέθοδος_λειτουργία, Εντολή
        self.보관 = self.ρίζα_τιμή / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Όνομα) or Όνομα in ('.', '..'):
            raise εκτέλεση_σφάλμα('VM 이름은 문자·ψηφίο_τιμή·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if μέθοδος_λειτουργία not in ('gui', 'headless'): raise εκτέλεση_σφάλμα('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ΔΙΑΔΡΟΜΗ(self, ομότιμος_τιμή):
        if Path(ομότιμος_τιμή).is_absolute() or '..' in Path(ομότιμος_τιμή).parts:
            raise εκτέλεση_σφάλμα('잘못된 관리 ΔΙΑΔΡΟΜΗ: ' + str(ομότιμος_τιμή))
        μέτρηση = self.보관
        for 부분 in ['.vbox'] + list(Path(ομότιμος_τιμή).parts):
            if 부분 == '.vbox': μέτρηση = self.보관
            else: μέτρηση = μέτρηση / 부분
            if μέτρηση.is_symlink(): raise εκτέλεση_σφάλμα('Σύνδεση 경로는 사용하지 않습니다: ' + str(μέτρηση))
        return μέτρηση

    def Ανάγνωση(self):
        ΔΙΑΔΡΟΜΗ = self.ΔΙΑΔΡΟΜΗ('state.json')
        if not ΔΙΑΔΡΟΜΗ.exists(): return None
        Κατάσταση_τιμή = json.loads(ΔΙΑΔΡΟΜΗ.read_text(encoding='utf-8'))
        if Κατάσταση_τιμή.get('version') != 1 or Κατάσταση_τιμή.get('name') != self.Όνομα:
            raise εκτέλεση_σφάλμα('관리 상태의 VM Όνομα/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Όνομα in ('uuid', 'owner'):
            if str(uuid.UUID(Κατάσταση_τιμή[Όνομα])) != Κατάσταση_τιμή[Όνομα]: raise εκτέλεση_σφάλμα('잘못된 VM αναγνωριστικό_τιμή')
        return Κατάσταση_τιμή

    def αποθηκεύω_τιμή(self, Κατάσταση_τιμή):
        προορισμός_τιμή = self.ΔΙΑΔΡΟΜΗ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Αρχείο:
            json.dump(Κατάσταση_τιμή, Αρχείο, ensure_ascii=False, indent=2)
            Αρχείο.write('\n')
            임시 = Αρχείο.name
        os.replace(임시, str(προορισμός_τιμή))

    def Πληροφορίες_συστήματος(self, Κατάσταση_τιμή, 등록됨, αποκαθιστώ_Κατάσταση=False):
        if Κατάσταση_τιμή['uuid'] not in 등록됨:
            raise εκτέλεση_σφάλμα('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Πληροφορίες_συστήματος = χαρακτηριστικό_τιμή_286d43f0(self.Εντολή(['VBoxManage', 'showvminfo', Κατάσταση_τιμή['uuid'], '--machinereadable']))
        Θέση = Path(Πληροφορίες_συστήματος.get('CfgFile', '')).resolve()
        if self.ΔΙΑΔΡΟΜΗ('machines').resolve() not in Θέση.parents or Πληροφορίες_συστήματος.get('UUID') != Κατάσταση_τιμή['uuid']:
            raise εκτέλεση_σφάλμα('이 프로젝트의 VM Ρυθμίσεις ΔΙΑΔΡΟΜΗ/UUID와 일치하지 않아 변경하지 않습니다.')
        δείκτης_τιμή_7e8f90bd = self.Εντολή(['VBoxManage', 'getextradata', Κατάσταση_τιμή['uuid'], 'JKOROS/Owner']).strip()
        if δείκτης_τιμή_7e8f90bd != 'Value: ' + Κατάσταση_τιμή['owner']:
            if αποκαθιστώ_Κατάσταση and Κατάσταση_τιμή.get('pending') and δείκτης_τιμή_7e8f90bd == 'No value set!':
                self.Εντολή(['VBoxManage', 'setextradata', Κατάσταση_τιμή['uuid'], 'JKOROS/Owner', Κατάσταση_τιμή['owner']])
            else:
                raise εκτέλεση_σφάλμα('VM κάτοχος_τιμή 표식이 일치하지 않아 변경하지 않습니다.')
        return Πληροφορίες_συστήματος

    def ελέγχω_μέσα(self, Κατάσταση_τιμή, Πληροφορίες_συστήματος):
        제어기들 = [τιμή for Όνομα, τιμή in Πληροφορίες_συστήματος.items() if re.fullmatch(r'storagecontrollername\d+', Όνομα)]
        Αποδοχή_τιμή = [str(self.ΔΙΑΔΡΟΜΗ(τιμή)) for τιμή in Κατάσταση_τιμή.get('media', [])]
        for Όνομα, τιμή in Πληροφορίες_συστήματος.items():
            if any(re.fullmatch(re.escape(ελεγκτής) + r'-\d+-\d+', Όνομα) for ελεγκτής in 제어기들):
                if τιμή not in ('none', 'emptydrive') and τιμή not in Αποδοχή_τιμή:
                    raise εκτέλεση_σφάλμα('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + τιμή)

    def εμφανίζω_Κατάσταση(self):
        Κατάσταση_τιμή = self.Ανάγνωση()
        if Κατάσταση_τιμή is None: return {'name': self.Όνομα, 'state': 'not-created'}
        Πληροφορίες_συστήματος = self.Πληροφορίες_συστήματος(Κατάσταση_τιμή, 등록목록(self.Εντολή(['VBoxManage', 'list', 'vms'])))
        return {'name': Πληροφορίες_συστήματος.get('name', Κατάσταση_τιμή['name']), 'uuid': Κατάσταση_τιμή['uuid'], 'state': Πληροφορίες_συστήματος.get('VMState'),
                'iso': str(self.ΔΙΑΔΡΟΜΗ(Κατάσταση_τιμή['iso'])) if Κατάσταση_τιμή.get('iso') else None,
                'serial_log': str(self.ΔΙΑΔΡΟΜΗ(Κατάσταση_τιμή['serial_log'])) if Κατάσταση_τιμή.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def εκτελώ_εντολή(self):
        Κατάσταση_τιμή = self.Ανάγνωση()
        등록됨 = 등록목록(self.Εντολή(['VBoxManage', 'list', 'vms']))
        Πληροφορίες_συστήματος = None
        if Κατάσταση_τιμή is not None and Κατάσταση_τιμή['uuid'] in 등록됨:
            Πληροφορίες_συστήματος = self.Πληροφορίες_συστήματος(Κατάσταση_τιμή, 등록됨, αποκαθιστώ_Κατάσταση=True)
            τρέχων_στοιχείο = Πληροφορίες_συστήματος.get('VMState')
            if τρέχων_στοιχείο == 'running':
                print('이미 εκτελώ_εντολή 중입니다. 재빌드·재시작하지 않습니다.')
                return self.εμφανίζω_Κατάσταση()
            self.ελέγχω_μέσα(Κατάσταση_τιμή, Πληροφορίες_συστήματος)
            if τρέχων_στοιχείο in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 αποθηκεύω_τιμή 상태를 버리지 않습니다.'.format(τρέχων_στοιχείο))
                if τρέχων_στοιχείο == 'paused':
                    self.Εντολή(['VBoxManage', 'controlvm', Κατάσταση_τιμή['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 δοκιμάζω_ξανά_τιμή Άνοιγμα 전에 기존 기록도 보관한다.
                    if Κατάσταση_τιμή.get('serial_log'):
                        원본 = self.ΔΙΑΔΡΟΜΗ(Κατάσταση_τιμή['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ΔΙΑΔΡΟΜΗ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Εντολή(['VBoxManage', 'startvm', Κατάσταση_τιμή['uuid'], '--type', self.μέθοδος_λειτουργία])
                return self.εμφανίζω_Κατάσταση()
            if τρέχων_στοιχείο not in ('poweroff', 'aborted'):
                raise εκτέλεση_σφάλμα('VM이 αλλάζω_λειτουργία 중입니다 ({}). 작업이 끝난 Πίσω_τιμή δοκιμάζω_ξανά_τιμή 실행하세요.'.format(τρέχων_στοιχείο))
        elif Κατάσταση_τιμή is not None and not Κατάσταση_τιμή.get('pending'):
            raise εκτέλεση_σφάλμα('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 δοκιμάζω_ξανά_τιμή 등록하세요.')
        elif self.Όνομα in 등록됨.values():
            raise εκτέλεση_σφάλμα('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # αποθηκεύω_τιμή/εκτελώ_εντολή 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Εντολή(['make', '-C', str(self.ρίζα_τιμή / 'os'), 'iso']), end='')
        원본 = self.ρίζα_τιμή / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise εκτέλεση_σφάλμα('부팅 ISO가 생성되지 않았습니다.')
        μέσα_τιμή = 'media/kernel-' + άθροισμα_ελέγχου(원본) + '.iso'
        προορισμός_τιμή = self.ΔΙΑΔΡΟΜΗ(μέσα_τιμή)
        προορισμός_τιμή.parent.mkdir(exist_ok=True)
        if προορισμός_τιμή.exists():
            if άθροισμα_ελέγχου(προορισμός_τιμή) != άθροισμα_ελέγχου(원본): raise εκτέλεση_σφάλμα('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(προορισμός_τιμή))
        else:
            with tempfile.NamedTemporaryFile(dir=str(προορισμός_τιμή.parent)) as Αρχείο:
                shutil.copyfile(str(원본), Αρχείο.name)
                os.link(Αρχείο.name, str(προορισμός_τιμή))

        if Κατάσταση_τιμή is None:
            Κατάσταση_τιμή = {'version': 1, 'name': self.Όνομα, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.αποθηκεύω_τιμή(Κατάσταση_τιμή)
        if Πληροφορίες_συστήματος is None:
            self.Εντολή(['VBoxManage', 'createvm', '--name', Κατάσταση_τιμή['name'], '--uuid', Κατάσταση_τιμή['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ΔΙΑΔΡΟΜΗ('machines')), '--register'])
            self.Εντολή(['VBoxManage', 'setextradata', Κατάσταση_τιμή['uuid'], 'JKOROS/Owner', Κατάσταση_τιμή['owner']])
        # δομή_Σύστημα 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Πληροφορίες_συστήματος = self.Πληροφορίες_συστήματος(Κατάσταση_τιμή, 등록목록(self.Εντολή(['VBoxManage', 'list', 'vms'])))
        if Πληροφορίες_συστήματος.get('VMState') not in ('poweroff', 'aborted'):
            raise εκτέλεση_σφάλμα('δομή_Σύστημα 중 VM 상태가 바뀌었습니다. δοκιμάζω_ξανά_τιμή make vbox를 실행하세요.')
        self.ελέγχω_μέσα(Κατάσταση_τιμή, Πληροφορίες_συστήματος)
        Κατάσταση_τιμή['iso'] = μέσα_τιμή
        if μέσα_τιμή not in Κατάσταση_τιμή['media']: Κατάσταση_τιμή['media'].append(μέσα_τιμή)
        Κατάσταση_τιμή['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        καταγράφω_τιμή = self.ΔΙΑΔΡΟΜΗ(Κατάσταση_τιμή['serial_log'])
        καταγράφω_τιμή.parent.mkdir(exist_ok=True)
        self.αποθηκεύω_τιμή(Κατάσταση_τιμή)
        self.Εντολή(['VBoxManage', 'modifyvm', Κατάσταση_τιμή['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(καταγράφω_τιμή)])
        제어기들 = [τιμή for Όνομα, τιμή in Πληροφορίες_συστήματος.items() if re.fullmatch(r'storagecontrollername\d+', Όνομα)]
        if 'JKOROS IDE' not in 제어기들:
            self.Εντολή(['VBoxManage', 'storagectl', Κατάσταση_τιμή['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Εντολή(['VBoxManage', 'storageattach', Κατάσταση_τιμή['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(προορισμός_τιμή)])
        Κατάσταση_τιμή['pending'] = False
        self.αποθηκεύω_τιμή(Κατάσταση_τιμή)
        self.Εντολή(['VBoxManage', 'startvm', Κατάσταση_τιμή['uuid'], '--type', self.μέθοδος_λειτουργία])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.εμφανίζω_Κατάσταση()


def Εκτέλεση_2():
    ανάλυση_τιμή_7cebddfb = argparse.ArgumentParser(description='jkoros 전용 VirtualBox εκτελώ_εντολή 및 Κατάσταση_τιμή ερώτημα_τιμή')
    ανάλυση_τιμή_7cebddfb.add_argument('action', choices=['run', 'status'])
    παράμετρος_όρισμα = ανάλυση_τιμή_7cebddfb.parse_args()
    εκτελώ_εντολή = εφαρμογή_εκκίνηση(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if παράμετρος_όρισμα.action == 'status':
        print(json.dumps(εκτελώ_εντολή.εμφανίζω_Κατάσταση(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise εκτέλεση_σφάλμα('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise εκτέλεση_σφάλμα('/dev/vboxdrv에 접근할 수 없습니다. φιλοξενώ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/άδεια_τιμή 변경은 하지 않습니다.')
    os.umask(0o077)
    εκτελώ_εντολή.ΔΙΑΔΡΟΜΗ('lock').parent.mkdir(parents=True, exist_ok=True)
    with εκτελώ_εντολή.ΔΙΑΔΡΟΜΗ('lock').open('a') as κλείδωμα_τιμή:
        try: fcntl.flock(κλείδωμα_τιμή, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise εκτέλεση_σφάλμα('다른 jkoros VirtualBox εκτελώ_εντολή 작업이 진행 중입니다.')
        print(json.dumps(εκτελώ_εντολή.εκτελώ_εντολή(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Εκτέλεση_2()
    except (εκτέλεση_σφάλμα, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ΣΦΑΛΜΑ:
        print('VBOX ΣΦΑΛΜΑ: ' + str(ΣΦΑΛΜΑ), file=sys.stderr)
        sys.exit(1)
