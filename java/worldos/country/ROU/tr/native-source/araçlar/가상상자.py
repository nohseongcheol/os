#!/usr/bin/env python3
"""jkoros 전용 VirtualBox program_Launcher. 기존 VM/디스크/depo_değer 상태는 삭제하지 않는다."""
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


class yürütme_hata(RuntimeError):
    pass


def yürütmek_kabuk_komut(bağımsız_değişkenler):
    ortam = dict(os.environ, LC_ALL='C')
    sonuç = subprocess.run([str(değer) for değer in bağımsız_değişkenler], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=ortam, timeout=180)
    içerik_değer = sonuç.stdout.decode('utf-8', 'replace')
    if sonuç.returncode:
        raise yürütme_hata('komut hata_değer: ' + ' '.join(str(değer) for değer in bağımsız_değişkenler) + '\n' + içerik_değer[-10000:])
    return içerik_değer


def öznitelik_değer(içerik_değer):
    sonuç = {}
    for girdi_satırı in içerik_değer.splitlines():
        if '=' not in girdi_satırı:
            continue
        İsim, değer = girdi_satırı.split('=', 1)
        if İsim.startswith('"'):
            İsim = json.loads(İsim)
        if değer.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(değer)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(değer): değer = 읽은값
            except ValueError:
                raise yürütme_hata('VirtualBox öznitelik_değer biçim_değer hata: ' + girdi_satırı)
        sonuç[İsim] = değer
    return sonuç


def 등록목록(içerik_değer):
    sonuç = {}
    for girdi_satırı in içerik_değer.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', girdi_satırı)
        if 일치: sonuç[일치.group(2).lower()] = 일치.group(1)
    return sonuç


def sağlama_toplamı(yol):
    değer = hashlib.sha256()
    with yol.open('rb') as dosya:
        for veri in iter(lambda: dosya.read(1024 * 1024), b''): değer.update(veri)
    return değer.hexdigest()


class program_Launcher:
    def __init__(self, kök_değer, İsim, metot_mod='gui', komut=yürütmek_kabuk_komut):
        self.kök_değer = Path(kök_değer).resolve()
        self.İsim, self.metot_mod, self.komut = İsim, metot_mod, komut
        self.보관 = self.kök_değer / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', İsim) or İsim in ('.', '..'):
            raise yürütme_hata('VM 이름은 문자·rakam_değer·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metot_mod not in ('gui', 'headless'): raise yürütme_hata('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def yol(self, eş_değer):
        if Path(eş_değer).is_absolute() or '..' in Path(eş_değer).parts:
            raise yürütme_hata('잘못된 관리 yol: ' + str(eş_değer))
        sonuç = self.보관
        for 부분 in ['.vbox'] + list(Path(eş_değer).parts):
            if 부분 == '.vbox': sonuç = self.보관
            else: sonuç = sonuç / 부분
            if sonuç.is_symlink(): raise yürütme_hata('Bağlan 경로는 사용하지 않습니다: ' + str(sonuç))
        return sonuç

    def Okuma(self):
        yol = self.yol('state.json')
        if not yol.exists(): return None
        Durum_değer = json.loads(yol.read_text(encoding='utf-8'))
        if Durum_değer.get('version') != 1 or Durum_değer.get('name') != self.İsim:
            raise yürütme_hata('관리 상태의 VM İsim/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for İsim in ('uuid', 'owner'):
            if str(uuid.UUID(Durum_değer[İsim])) != Durum_değer[İsim]: raise yürütme_hata('잘못된 VM tanımlayıcı_değer')
        return Durum_değer

    def depo_değer(self, Durum_değer):
        hedef_değer = self.yol('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as dosya:
            json.dump(Durum_değer, dosya, ensure_ascii=False, indent=2)
            dosya.write('\n')
            임시 = dosya.name
        os.replace(임시, str(hedef_değer))

    def msinfo32_exe(self, Durum_değer, 등록됨, kurtarmak_Durum=False):
        if Durum_değer['uuid'] not in 등록됨:
            raise yürütme_hata('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = öznitelik_değer(self.komut(['VBoxManage', 'showvminfo', Durum_değer['uuid'], '--machinereadable']))
        konum = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.yol('machines').resolve() not in konum.parents or msinfo32_exe.get('UUID') != Durum_değer['uuid']:
            raise yürütme_hata('이 프로젝트의 VM Ayarlar yol/UUID와 일치하지 않아 변경하지 않습니다.')
        işaret_değer = self.komut(['VBoxManage', 'getextradata', Durum_değer['uuid'], 'JKOROS/Owner']).strip()
        if işaret_değer != 'Value: ' + Durum_değer['owner']:
            if kurtarmak_Durum and Durum_değer.get('pending') and işaret_değer == 'No value set!':
                self.komut(['VBoxManage', 'setextradata', Durum_değer['uuid'], 'JKOROS/Owner', Durum_değer['owner']])
            else:
                raise yürütme_hata('VM sahip_değer 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def çek_Medya(self, Durum_değer, msinfo32_exe):
        제어기들 = [değer for İsim, değer in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', İsim)]
        İzin_Ver_değer = [str(self.yol(değer)) for değer in Durum_değer.get('media', [])]
        for İsim, değer in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kumanda) + r'-\d+-\d+', İsim) for kumanda in 제어기들):
                if değer not in ('none', 'emptydrive') and değer not in İzin_Ver_değer:
                    raise yürütme_hata('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + değer)

    def şov_Durum(self):
        Durum_değer = self.Okuma()
        if Durum_değer is None: return {'name': self.İsim, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Durum_değer, 등록목록(self.komut(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Durum_değer['name']), 'uuid': Durum_değer['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.yol(Durum_değer['iso'])) if Durum_değer.get('iso') else None,
                'serial_log': str(self.yol(Durum_değer['serial_log'])) if Durum_değer.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def yürütmek_komut(self):
        Durum_değer = self.Okuma()
        등록됨 = 등록목록(self.komut(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Durum_değer is not None and Durum_değer['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Durum_değer, 등록됨, kurtarmak_Durum=True)
            geçerli_öğe = msinfo32_exe.get('VMState')
            if geçerli_öğe == 'running':
                print('이미 yürütmek_komut 중입니다. 재빌드·재시작하지 않습니다.')
                return self.şov_Durum()
            self.çek_Medya(Durum_değer, msinfo32_exe)
            if geçerli_öğe in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 depo_değer 상태를 버리지 않습니다.'.format(geçerli_öğe))
                if geçerli_öğe == 'paused':
                    self.komut(['VBoxManage', 'controlvm', Durum_değer['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 yeniden_denemek_değer Aç 전에 기존 기록도 보관한다.
                    if Durum_değer.get('serial_log'):
                        원본 = self.yol(Durum_değer['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.yol('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.komut(['VBoxManage', 'startvm', Durum_değer['uuid'], '--type', self.metot_mod])
                return self.şov_Durum()
            if geçerli_öğe not in ('poweroff', 'aborted'):
                raise yürütme_hata('VM이 geçiş_mod 중입니다 ({}). 작업이 끝난 BACK_değer yeniden_denemek_değer 실행하세요.'.format(geçerli_öğe))
        elif Durum_değer is not None and not Durum_değer.get('pending'):
            raise yürütme_hata('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 yeniden_denemek_değer 등록하세요.')
        elif self.İsim in 등록됨.values():
            raise yürütme_hata('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # depo_değer/yürütmek_komut 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.komut(['make', '-C', str(self.kök_değer / 'os'), 'iso']), end='')
        원본 = self.kök_değer / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise yürütme_hata('makine_başlatma ISO가 생성되지 않았습니다.')
        Medya_değer = 'media/kernel-' + sağlama_toplamı(원본) + '.iso'
        hedef_değer = self.yol(Medya_değer)
        hedef_değer.parent.mkdir(exist_ok=True)
        if hedef_değer.exists():
            if sağlama_toplamı(hedef_değer) != sağlama_toplamı(원본): raise yürütme_hata('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(hedef_değer))
        else:
            with tempfile.NamedTemporaryFile(dir=str(hedef_değer.parent)) as dosya:
                shutil.copyfile(str(원본), dosya.name)
                os.link(dosya.name, str(hedef_değer))

        if Durum_değer is None:
            Durum_değer = {'version': 1, 'name': self.İsim, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.depo_değer(Durum_değer)
        if msinfo32_exe is None:
            self.komut(['VBoxManage', 'createvm', '--name', Durum_değer['name'], '--uuid', Durum_değer['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.yol('machines')), '--register'])
            self.komut(['VBoxManage', 'setextradata', Durum_değer['uuid'], 'JKOROS/Owner', Durum_değer['owner']])
        # oluştur 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Durum_değer, 등록목록(self.komut(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise yürütme_hata('oluştur 중 VM 상태가 바뀌었습니다. yeniden_denemek_değer make vbox를 실행하세요.')
        self.çek_Medya(Durum_değer, msinfo32_exe)
        Durum_değer['iso'] = Medya_değer
        if Medya_değer not in Durum_değer['media']: Durum_değer['media'].append(Medya_değer)
        Durum_değer['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_değer = self.yol(Durum_değer['serial_log'])
        LOG_değer.parent.mkdir(exist_ok=True)
        self.depo_değer(Durum_değer)
        self.komut(['VBoxManage', 'modifyvm', Durum_değer['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_değer)])
        제어기들 = [değer for İsim, değer in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', İsim)]
        if 'JKOROS IDE' not in 제어기들:
            self.komut(['VBoxManage', 'storagectl', Durum_değer['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.komut(['VBoxManage', 'storageattach', Durum_değer['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(hedef_değer)])
        Durum_değer['pending'] = False
        self.depo_değer(Durum_değer)
        self.komut(['VBoxManage', 'startvm', Durum_değer['uuid'], '--type', self.metot_mod])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.şov_Durum()


def çalıştır():
    ayrıştırmak_değer = argparse.ArgumentParser(description='jkoros 전용 VirtualBox yürütmek_komut 및 Durum_değer sorgu_değer')
    ayrıştırmak_değer.add_argument('action', choices=['run', 'status'])
    parametre_bağımsız_değişken = ayrıştırmak_değer.parse_args()
    yürütmek_komut = program_Launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parametre_bağımsız_değişken.action == 'status':
        print(json.dumps(yürütmek_komut.şov_Durum(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise yürütme_hata('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise yürütme_hata('/dev/vboxdrv에 접근할 수 없습니다. konak 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/izin_değer 변경은 하지 않습니다.')
    os.umask(0o077)
    yürütmek_komut.yol('lock').parent.mkdir(parents=True, exist_ok=True)
    with yürütmek_komut.yol('lock').open('a') as kilit_değer:
        try: fcntl.flock(kilit_değer, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise yürütme_hata('다른 jkoros VirtualBox yürütmek_komut 작업이 진행 중입니다.')
        print(json.dumps(yürütmek_komut.yürütmek_komut(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: çalıştır()
    except (yürütme_hata, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as hata:
        print('VBOX hata: ' + str(hata), file=sys.stderr)
        sys.exit(1)
