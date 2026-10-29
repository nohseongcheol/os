#!/usr/bin/env python3
"""jkoros 전용 VirtualBox Tiriso_llae_ya_sediriso. 기존 VM/디스크/Store_Boleng 상태는 삭제하지 않는다."""
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


def diragatsa_setlhalosataelo_Taelo(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(Boleng) for Boleng in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Diteng_Boleng = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Taelo palelo_Boleng: ' + ' '.join(str(Boleng) for Boleng in 인수) + '\n' + Diteng_Boleng[-10000:])
    return Diteng_Boleng


def nonofo_Boleng(Diteng_Boleng):
    결과 = {}
    for Mola in Diteng_Boleng.splitlines():
        if '=' not in Mola:
            continue
        leina, Boleng = Mola.split('=', 1)
        if leina.startswith('"'):
            leina = json.loads(leina)
        if Boleng.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(Boleng)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(Boleng): Boleng = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox nonofo_Boleng fometa_Boleng phoso: ' + Mola)
        결과[leina] = Boleng
    return 결과


def 등록목록(Diteng_Boleng):
    결과 = {}
    for Mola in Diteng_Boleng.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Mola)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(tsela):
    Boleng = hashlib.sha256()
    with tsela.open('rb') as faele:
        for tshedimosetso in iter(lambda: faele.read(1024 * 1024), b''): Boleng.update(tshedimosetso)
    return Boleng.hexdigest()


class Tiriso_llae_ya_sediriso:
    def __init__(self, 뿌리, leina, mokgwa_mokgwa='gui', Taelo=diragatsa_setlhalosataelo_Taelo):
        self.뿌리 = Path(뿌리).resolve()
        self.leina, self.mokgwa_mokgwa, self.Taelo = leina, mokgwa_mokgwa, Taelo
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', leina) or leina in ('.', '..'):
            raise 실행오류('VM 이름은 문자·dijite_Boleng·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if mokgwa_mokgwa not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def tsela(self, semphato_Boleng):
        if Path(semphato_Boleng).is_absolute() or '..' in Path(semphato_Boleng).parts:
            raise 실행오류('잘못된 관리 tsela: ' + str(semphato_Boleng))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(semphato_Boleng).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Golaganya 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        tsela = self.tsela('state.json')
        if not tsela.exists(): return None
        kemo_Boleng = json.loads(tsela.read_text(encoding='utf-8'))
        if kemo_Boleng.get('version') != 1 or kemo_Boleng.get('name') != self.leina:
            raise 실행오류('관리 상태의 VM leina/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for leina in ('uuid', 'owner'):
            if str(uuid.UUID(kemo_Boleng[leina])) != kemo_Boleng[leina]: raise 실행오류('잘못된 VM setlhaodi_Boleng')
        return kemo_Boleng

    def Store_Boleng(self, kemo_Boleng):
        bogorogelo_Boleng = self.tsela('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as faele:
            json.dump(kemo_Boleng, faele, ensure_ascii=False, indent=2)
            faele.write('\n')
            임시 = faele.name
        os.replace(임시, str(bogorogelo_Boleng))

    def msinfo32_exe(self, kemo_Boleng, 등록됨, busetsa_morago_kemo=False):
        if kemo_Boleng['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = nonofo_Boleng(self.Taelo(['VBoxManage', 'showvminfo', kemo_Boleng['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.tsela('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != kemo_Boleng['uuid']:
            raise 실행오류('이 프로젝트의 VM Diseting tsela/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Taelo(['VBoxManage', 'getextradata', kemo_Boleng['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + kemo_Boleng['owner']:
            if busetsa_morago_kemo and kemo_Boleng.get('pending') and 표식 == 'No value set!':
                self.Taelo(['VBoxManage', 'setextradata', kemo_Boleng['uuid'], 'JKOROS/Owner', kemo_Boleng['owner']])
            else:
                raise 실행오류('VM mong_Boleng 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, kemo_Boleng, msinfo32_exe):
        제어기들 = [Boleng for leina, Boleng in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', leina)]
        letla_Boleng = [str(self.tsela(Boleng)) for Boleng in kemo_Boleng.get('media', [])]
        for leina, Boleng in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', leina) for 제어기 in 제어기들):
                if Boleng not in ('none', 'emptydrive') and Boleng not in letla_Boleng:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + Boleng)

    def bontsha_kemo(self):
        kemo_Boleng = self.읽기()
        if kemo_Boleng is None: return {'name': self.leina, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(kemo_Boleng, 등록목록(self.Taelo(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', kemo_Boleng['name']), 'uuid': kemo_Boleng['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.tsela(kemo_Boleng['iso'])) if kemo_Boleng.get('iso') else None,
                'serial_log': str(self.tsela(kemo_Boleng['serial_log'])) if kemo_Boleng.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def diragatsa_Taelo(self):
        kemo_Boleng = self.읽기()
        등록됨 = 등록목록(self.Taelo(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if kemo_Boleng is not None and kemo_Boleng['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(kemo_Boleng, 등록됨, busetsa_morago_kemo=True)
            ga_jaana_selwana = msinfo32_exe.get('VMState')
            if ga_jaana_selwana == 'running':
                print('이미 diragatsa_Taelo 중입니다. 재빌드·재시작하지 않습니다.')
                return self.bontsha_kemo()
            self.매체검사(kemo_Boleng, msinfo32_exe)
            if ga_jaana_selwana in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_Boleng 상태를 버리지 않습니다.'.format(ga_jaana_selwana))
                if ga_jaana_selwana == 'paused':
                    self.Taelo(['VBoxManage', 'controlvm', kemo_Boleng['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 bula 전에 기존 기록도 보관한다.
                    if kemo_Boleng.get('serial_log'):
                        원본 = self.tsela(kemo_Boleng['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.tsela('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Taelo(['VBoxManage', 'startvm', kemo_Boleng['uuid'], '--type', self.mokgwa_mokgwa])
                return self.bontsha_kemo()
            if ga_jaana_selwana not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 fetola_mokgwa 중입니다 ({}). 작업이 끝난 Morago_Boleng 다시 실행하세요.'.format(ga_jaana_selwana))
        elif kemo_Boleng is not None and not kemo_Boleng.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.leina in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_Boleng/diragatsa_Taelo 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Taelo(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        bogorogelo_Boleng = self.tsela(매체)
        bogorogelo_Boleng.parent.mkdir(exist_ok=True)
        if bogorogelo_Boleng.exists():
            if 검사합(bogorogelo_Boleng) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(bogorogelo_Boleng))
        else:
            with tempfile.NamedTemporaryFile(dir=str(bogorogelo_Boleng.parent)) as faele:
                shutil.copyfile(str(원본), faele.name)
                os.link(faele.name, str(bogorogelo_Boleng))

        if kemo_Boleng is None:
            kemo_Boleng = {'version': 1, 'name': self.leina, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_Boleng(kemo_Boleng)
        if msinfo32_exe is None:
            self.Taelo(['VBoxManage', 'createvm', '--name', kemo_Boleng['name'], '--uuid', kemo_Boleng['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.tsela('machines')), '--register'])
            self.Taelo(['VBoxManage', 'setextradata', kemo_Boleng['uuid'], 'JKOROS/Owner', kemo_Boleng['owner']])
        # aga_tsamaiso 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(kemo_Boleng, 등록목록(self.Taelo(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('aga_tsamaiso 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(kemo_Boleng, msinfo32_exe)
        kemo_Boleng['iso'] = 매체
        if 매체 not in kemo_Boleng['media']: kemo_Boleng['media'].append(매체)
        kemo_Boleng['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        rekota_Boleng = self.tsela(kemo_Boleng['serial_log'])
        rekota_Boleng.parent.mkdir(exist_ok=True)
        self.Store_Boleng(kemo_Boleng)
        self.Taelo(['VBoxManage', 'modifyvm', kemo_Boleng['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(rekota_Boleng)])
        제어기들 = [Boleng for leina, Boleng in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', leina)]
        if 'JKOROS IDE' not in 제어기들:
            self.Taelo(['VBoxManage', 'storagectl', kemo_Boleng['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Taelo(['VBoxManage', 'storageattach', kemo_Boleng['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(bogorogelo_Boleng)])
        kemo_Boleng['pending'] = False
        self.Store_Boleng(kemo_Boleng)
        self.Taelo(['VBoxManage', 'startvm', kemo_Boleng['uuid'], '--type', self.mokgwa_mokgwa])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.bontsha_kemo()


def dirisa():
    go_lokolola_Boleng = argparse.ArgumentParser(description='jkoros 전용 VirtualBox diragatsa_Taelo 및 kemo_Boleng fenenkolola_Boleng')
    go_lokolola_Boleng.add_argument('action', choices=['run', 'status'])
    인자 = go_lokolola_Boleng.parse_args()
    diragatsa_Taelo = Tiriso_llae_ya_sediriso(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(diragatsa_Taelo.bontsha_kemo(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. pinagare 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/tetla_Boleng 변경은 하지 않습니다.')
    os.umask(0o077)
    diragatsa_Taelo.tsela('lock').parent.mkdir(parents=True, exist_ok=True)
    with diragatsa_Taelo.tsela('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox diragatsa_Taelo 작업이 진행 중입니다.')
        print(json.dumps(diragatsa_Taelo.diragatsa_Taelo(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: dirisa()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as phoso:
        print('VBOX phoso: ' + str(phoso), file=sys.stderr)
        sys.exit(1)
