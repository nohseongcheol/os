#!/usr/bin/env python3
"""jkoros 전용 VirtualBox tirišo_sethala_tirišo. 기존 VM/디스크/lota_boleng 상태는 삭제하지 않는다."""
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


def phethagatša_šele_taelo(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(boleng) for boleng in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Diteng_boleng = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Taelo go_palelwa_boleng: ' + ' '.join(str(boleng) for boleng in 인수) + '\n' + Diteng_boleng[-10000:])
    return Diteng_boleng


def tlhaodi_ya_faele_boleng(Diteng_boleng):
    결과 = {}
    for mothaladi in Diteng_boleng.splitlines():
        if '=' not in mothaladi:
            continue
        Leina, boleng = mothaladi.split('=', 1)
        if Leina.startswith('"'):
            Leina = json.loads(Leina)
        if boleng.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(boleng)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(boleng): boleng = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox tlhaodi_ya_faele_boleng fomete_boleng Phošo: ' + mothaladi)
        결과[Leina] = boleng
    return 결과


def 등록목록(Diteng_boleng):
    결과 = {}
    for mothaladi in Diteng_boleng.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', mothaladi)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(Tsejana):
    boleng = hashlib.sha256()
    with Tsejana.open('rb') as Faele:
        for data in iter(lambda: Faele.read(1024 * 1024), b''): boleng.update(data)
    return boleng.hexdigest()


class tirišo_sethala_tirišo:
    def __init__(self, 뿌리, Leina, mokgwa_mokgwa='gui', Taelo=phethagatša_šele_taelo):
        self.뿌리 = Path(뿌리).resolve()
        self.Leina, self.mokgwa_mokgwa, self.Taelo = Leina, mokgwa_mokgwa, Taelo
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Leina) or Leina in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if mokgwa_mokgwa not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Tsejana(self, sedirišwa_sa_legoro_le_tee_boleng):
        if Path(sedirišwa_sa_legoro_le_tee_boleng).is_absolute() or '..' in Path(sedirišwa_sa_legoro_le_tee_boleng).parts:
            raise 실행오류('잘못된 관리 Tsejana: ' + str(sedirišwa_sa_legoro_le_tee_boleng))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(sedirišwa_sa_legoro_le_tee_boleng).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Ikgokaganye 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Bala(self):
        Tsejana = self.Tsejana('state.json')
        if not Tsejana.exists(): return None
        boemo_boleng = json.loads(Tsejana.read_text(encoding='utf-8'))
        if boemo_boleng.get('version') != 1 or boemo_boleng.get('name') != self.Leina:
            raise 실행오류('관리 상태의 VM Leina/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Leina in ('uuid', 'owner'):
            if str(uuid.UUID(boemo_boleng[Leina])) != boemo_boleng[Leina]: raise 실행오류('잘못된 VM sešupi_boleng')
        return boemo_boleng

    def lota_boleng(self, boemo_boleng):
        boyo_boleng = self.Tsejana('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Faele:
            json.dump(boemo_boleng, Faele, ensure_ascii=False, indent=2)
            Faele.write('\n')
            임시 = Faele.name
        os.replace(임시, str(boyo_boleng))

    def msinfo32_exe(self, boemo_boleng, 등록됨, boela_sekeng_boemo=False):
        if boemo_boleng['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = tlhaodi_ya_faele_boleng(self.Taelo(['VBoxManage', 'showvminfo', boemo_boleng['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Tsejana('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != boemo_boleng['uuid']:
            raise 실행오류('이 프로젝트의 VM Dipeakanyo Tsejana/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Taelo(['VBoxManage', 'getextradata', boemo_boleng['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + boemo_boleng['owner']:
            if boela_sekeng_boemo and boemo_boleng.get('pending') and 표식 == 'No value set!':
                self.Taelo(['VBoxManage', 'setextradata', boemo_boleng['uuid'], 'JKOROS/Owner', boemo_boleng['owner']])
            else:
                raise 실행오류('VM mong_boleng 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, boemo_boleng, msinfo32_exe):
        제어기들 = [boleng for Leina, boleng in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Leina)]
        Dumelela_boleng = [str(self.Tsejana(boleng)) for boleng in boemo_boleng.get('media', [])]
        for Leina, boleng in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Leina) for 제어기 in 제어기들):
                if boleng not in ('none', 'emptydrive') and boleng not in Dumelela_boleng:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + boleng)

    def bontšha_boemo(self):
        boemo_boleng = self.Bala()
        if boemo_boleng is None: return {'name': self.Leina, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(boemo_boleng, 등록목록(self.Taelo(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', boemo_boleng['name']), 'uuid': boemo_boleng['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Tsejana(boemo_boleng['iso'])) if boemo_boleng.get('iso') else None,
                'serial_log': str(self.Tsejana(boemo_boleng['serial_log'])) if boemo_boleng.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def phethagatša_taelo(self):
        boemo_boleng = self.Bala()
        등록됨 = 등록목록(self.Taelo(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if boemo_boleng is not None and boemo_boleng['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(boemo_boleng, 등록됨, boela_sekeng_boemo=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 phethagatša_taelo 중입니다. 재빌드·재시작하지 않습니다.')
                return self.bontšha_boemo()
            self.매체검사(boemo_boleng, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 lota_boleng 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Taelo(['VBoxManage', 'controlvm', boemo_boleng['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Bula 전에 기존 기록도 보관한다.
                    if boemo_boleng.get('serial_log'):
                        원본 = self.Tsejana(boemo_boleng['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Tsejana('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Taelo(['VBoxManage', 'startvm', boemo_boleng['uuid'], '--type', self.mokgwa_mokgwa])
                return self.bontšha_boemo()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 fetogela_mokgwa 중입니다 ({}). 작업이 끝난 Morago_boleng 다시 실행하세요.'.format(현재))
        elif boemo_boleng is not None and not boemo_boleng.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Leina in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # lota_boleng/phethagatša_taelo 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Taelo(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        boyo_boleng = self.Tsejana(매체)
        boyo_boleng.parent.mkdir(exist_ok=True)
        if boyo_boleng.exists():
            if 검사합(boyo_boleng) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(boyo_boleng))
        else:
            with tempfile.NamedTemporaryFile(dir=str(boyo_boleng.parent)) as Faele:
                shutil.copyfile(str(원본), Faele.name)
                os.link(Faele.name, str(boyo_boleng))

        if boemo_boleng is None:
            boemo_boleng = {'version': 1, 'name': self.Leina, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.lota_boleng(boemo_boleng)
        if msinfo32_exe is None:
            self.Taelo(['VBoxManage', 'createvm', '--name', boemo_boleng['name'], '--uuid', boemo_boleng['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Tsejana('machines')), '--register'])
            self.Taelo(['VBoxManage', 'setextradata', boemo_boleng['uuid'], 'JKOROS/Owner', boemo_boleng['owner']])
        # aga_lenaneo 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(boemo_boleng, 등록목록(self.Taelo(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('aga_lenaneo 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(boemo_boleng, msinfo32_exe)
        boemo_boleng['iso'] = 매체
        if 매체 not in boemo_boleng['media']: boemo_boleng['media'].append(매체)
        boemo_boleng['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        pego_boleng_e0918eb0 = self.Tsejana(boemo_boleng['serial_log'])
        pego_boleng_e0918eb0.parent.mkdir(exist_ok=True)
        self.lota_boleng(boemo_boleng)
        self.Taelo(['VBoxManage', 'modifyvm', boemo_boleng['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(pego_boleng_e0918eb0)])
        제어기들 = [boleng for Leina, boleng in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Leina)]
        if 'JKOROS IDE' not in 제어기들:
            self.Taelo(['VBoxManage', 'storagectl', boemo_boleng['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Taelo(['VBoxManage', 'storageattach', boemo_boleng['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(boyo_boleng)])
        boemo_boleng['pending'] = False
        self.lota_boleng(boemo_boleng)
        self.Taelo(['VBoxManage', 'startvm', boemo_boleng['uuid'], '--type', self.mokgwa_mokgwa])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.bontšha_boemo()


def Diriša():
    ripaganya_boleng = argparse.ArgumentParser(description='jkoros 전용 VirtualBox phethagatša_taelo 및 boemo_boleng kwiri_boleng')
    ripaganya_boleng.add_argument('action', choices=['run', 'status'])
    인자 = ripaganya_boleng.parse_args()
    phethagatša_taelo = tirišo_sethala_tirišo(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(phethagatša_taelo.bontšha_boemo(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. go_nea_ditirelo 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/tumelelo_boleng 변경은 하지 않습니다.')
    os.umask(0o077)
    phethagatša_taelo.Tsejana('lock').parent.mkdir(parents=True, exist_ok=True)
    with phethagatša_taelo.Tsejana('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox phethagatša_taelo 작업이 진행 중입니다.')
        print(json.dumps(phethagatša_taelo.phethagatša_taelo(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Diriša()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Phošo:
        print('VBOX Phošo: ' + str(Phošo), file=sys.stderr)
        sys.exit(1)
