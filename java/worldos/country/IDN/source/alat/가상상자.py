#!/usr/bin/env python3
"""jkoros 전용 VirtualBox apl_peluncur. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Jalankan_shell_perintah(argumen):
    lingkungan = dict(os.environ, LC_ALL='C')
    hasil = subprocess.run([str(VALUE) for VALUE in argumen], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=lingkungan, timeout=180)
    Isi_VALUE = hasil.stdout.decode('utf-8', 'replace')
    if hasil.returncode:
        raise 실행오류('perintah kegagalan_VALUE: ' + ' '.join(str(VALUE) for VALUE in argumen) + '\n' + Isi_VALUE[-10000:])
    return Isi_VALUE


def nilai_atribut(Isi_VALUE):
    hasil = {}
    for baris_masukan in Isi_VALUE.splitlines():
        if '=' not in baris_masukan:
            continue
        Nama_2, VALUE = baris_masukan.split('=', 1)
        if Nama_2.startswith('"'):
            Nama_2 = json.loads(Nama_2)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox nilai_atribut format_VALUE galat: ' + baris_masukan)
        hasil[Nama_2] = VALUE
    return hasil


def 등록목록(Isi_VALUE):
    hasil = {}
    for baris_masukan in Isi_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', baris_masukan)
        if 일치: hasil[일치.group(2).lower()] = 일치.group(1)
    return hasil


def checksum(jalur):
    VALUE = hashlib.sha256()
    with jalur.open('rb') as berkas:
        for data in iter(lambda: berkas.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class apl_peluncur:
    def __init__(self, akar_VALUE, Nama_2, metode_MODE='gui', perintah=Jalankan_shell_perintah):
        self.akar_VALUE = Path(akar_VALUE).resolve()
        self.Nama_2, self.metode_MODE, self.perintah = Nama_2, metode_MODE, perintah
        self.보관 = self.akar_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nama_2) or Nama_2 in ('.', '..'):
            raise 실행오류('VM 이름은 문자·angka_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metode_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def jalur(self, serekan_VALUE):
        if Path(serekan_VALUE).is_absolute() or '..' in Path(serekan_VALUE).parts:
            raise 실행오류('잘못된 관리 jalur: ' + str(serekan_VALUE))
        hasil = self.보관
        for 부분 in ['.vbox'] + list(Path(serekan_VALUE).parts):
            if 부분 == '.vbox': hasil = self.보관
            else: hasil = hasil / 부분
            if hasil.is_symlink(): raise 실행오류('Sambung 경로는 사용하지 않습니다: ' + str(hasil))
        return hasil

    def Baca(self):
        jalur = self.jalur('state.json')
        if not jalur.exists(): return None
        Status_VALUE = json.loads(jalur.read_text(encoding='utf-8'))
        if Status_VALUE.get('version') != 1 or Status_VALUE.get('name') != self.Nama_2:
            raise 실행오류('관리 상태의 VM Nama_2/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nama_2 in ('uuid', 'owner'):
            if str(uuid.UUID(Status_VALUE[Nama_2])) != Status_VALUE[Nama_2]: raise 실행오류('잘못된 VM pengidentifikasi_VALUE')
        return Status_VALUE

    def Store_VALUE(self, Status_VALUE):
        tujuan_VALUE = self.jalur('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as berkas:
            json.dump(Status_VALUE, berkas, ensure_ascii=False, indent=2)
            berkas.write('\n')
            임시 = berkas.name
        os.replace(임시, str(tujuan_VALUE))

    def msinfo32_exe(self, Status_VALUE, 등록됨, pulihkan_Status=False):
        if Status_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = nilai_atribut(self.perintah(['VBoxManage', 'showvminfo', Status_VALUE['uuid'], '--machinereadable']))
        posisi = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.jalur('machines').resolve() not in posisi.parents or msinfo32_exe.get('UUID') != Status_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Konfigurasi jalur/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.perintah(['VBoxManage', 'getextradata', Status_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + Status_VALUE['owner']:
            if pulihkan_Status and Status_VALUE.get('pending') and 표식 == 'No value set!':
                self.perintah(['VBoxManage', 'setextradata', Status_VALUE['uuid'], 'JKOROS/Owner', Status_VALUE['owner']])
            else:
                raise 실행오류('VM pemilik_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def cek_media(self, Status_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Nama_2, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nama_2)]
        Perbolehkan_VALUE = [str(self.jalur(VALUE)) for VALUE in Status_VALUE.get('media', [])]
        for Nama_2, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(pengontrol) + r'-\d+-\d+', Nama_2) for pengontrol in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Perbolehkan_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def show_Status(self):
        Status_VALUE = self.Baca()
        if Status_VALUE is None: return {'name': self.Nama_2, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Status_VALUE, 등록목록(self.perintah(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Status_VALUE['name']), 'uuid': Status_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.jalur(Status_VALUE['iso'])) if Status_VALUE.get('iso') else None,
                'serial_log': str(self.jalur(Status_VALUE['serial_log'])) if Status_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Jalankan_perintah(self):
        Status_VALUE = self.Baca()
        등록됨 = 등록목록(self.perintah(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Status_VALUE is not None and Status_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Status_VALUE, 등록됨, pulihkan_Status=True)
            saat_ini_item = msinfo32_exe.get('VMState')
            if saat_ini_item == 'running':
                print('이미 Jalankan_perintah 중입니다. 재빌드·재시작하지 않습니다.')
                return self.show_Status()
            self.cek_media(Status_VALUE, msinfo32_exe)
            if saat_ini_item in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(saat_ini_item))
                if saat_ini_item == 'paused':
                    self.perintah(['VBoxManage', 'controlvm', Status_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 coba_lagi_VALUE Buka 전에 기존 기록도 보관한다.
                    if Status_VALUE.get('serial_log'):
                        원본 = self.jalur(Status_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.jalur('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.perintah(['VBoxManage', 'startvm', Status_VALUE['uuid'], '--type', self.metode_MODE])
                return self.show_Status()
            if saat_ini_item not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 BACK_VALUE coba_lagi_VALUE 실행하세요.'.format(saat_ini_item))
        elif Status_VALUE is not None and not Status_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 coba_lagi_VALUE 등록하세요.')
        elif self.Nama_2 in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Jalankan_perintah 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.perintah(['make', '-C', str(self.akar_VALUE / 'os'), 'iso']), end='')
        원본 = self.akar_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('awal_mesin ISO가 생성되지 않았습니다.')
        media_VALUE = 'media/kernel-' + checksum(원본) + '.iso'
        tujuan_VALUE = self.jalur(media_VALUE)
        tujuan_VALUE.parent.mkdir(exist_ok=True)
        if tujuan_VALUE.exists():
            if checksum(tujuan_VALUE) != checksum(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(tujuan_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(tujuan_VALUE.parent)) as berkas:
                shutil.copyfile(str(원본), berkas.name)
                os.link(berkas.name, str(tujuan_VALUE))

        if Status_VALUE is None:
            Status_VALUE = {'version': 1, 'name': self.Nama_2, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Status_VALUE)
        if msinfo32_exe is None:
            self.perintah(['VBoxManage', 'createvm', '--name', Status_VALUE['name'], '--uuid', Status_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.jalur('machines')), '--register'])
            self.perintah(['VBoxManage', 'setextradata', Status_VALUE['uuid'], 'JKOROS/Owner', Status_VALUE['owner']])
        # bangun 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Status_VALUE, 등록목록(self.perintah(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('bangun 중 VM 상태가 바뀌었습니다. coba_lagi_VALUE make vbox를 실행하세요.')
        self.cek_media(Status_VALUE, msinfo32_exe)
        Status_VALUE['iso'] = media_VALUE
        if media_VALUE not in Status_VALUE['media']: Status_VALUE['media'].append(media_VALUE)
        Status_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.jalur(Status_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Status_VALUE)
        self.perintah(['VBoxManage', 'modifyvm', Status_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Nama_2, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nama_2)]
        if 'JKOROS IDE' not in 제어기들:
            self.perintah(['VBoxManage', 'storagectl', Status_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.perintah(['VBoxManage', 'storageattach', Status_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(tujuan_VALUE)])
        Status_VALUE['pending'] = False
        self.Store_VALUE(Status_VALUE)
        self.perintah(['VBoxManage', 'startvm', Status_VALUE['uuid'], '--type', self.metode_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.show_Status()


def jalankan():
    urai_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Jalankan_perintah 및 Status_VALUE kueri_VALUE')
    urai_VALUE.add_argument('action', choices=['run', 'status'])
    parameter_argumen = urai_VALUE.parse_args()
    Jalankan_perintah = apl_peluncur(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argumen.action == 'status':
        print(json.dumps(Jalankan_perintah.show_Status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/izin_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Jalankan_perintah.jalur('lock').parent.mkdir(parents=True, exist_ok=True)
    with Jalankan_perintah.jalur('lock').open('a') as kunci_VALUE:
        try: fcntl.flock(kunci_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Jalankan_perintah 작업이 진행 중입니다.')
        print(json.dumps(Jalankan_perintah.Jalankan_perintah(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: jalankan()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as galat:
        print('VBOX galat: ' + str(galat), file=sys.stderr)
        sys.exit(1)
