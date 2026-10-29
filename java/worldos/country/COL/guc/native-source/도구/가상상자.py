#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 실행기. 기존 VM/디스크/저장 상태는 삭제하지 않는다."""
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


def 명령실행(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(ajutuu) for ajutuu in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    alu_ujatüü_ajutuu = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('aluwataaya ajachitia_ajutuu: ' + ' '.join(str(ajutuu) for ajutuu in 인수) + '\n' + alu_ujatüü_ajutuu[-10000:])
    return alu_ujatüü_ajutuu


def anaajaalaakua_ipa_ajutuu(alu_ujatüü_ajutuu):
    결과 = {}
    for liinia in alu_ujatüü_ajutuu.splitlines():
        if '=' not in liinia:
            continue
        이름, ajutuu = liinia.split('=', 1)
        if 이름.startswith('"'):
            이름 = json.loads(이름)
        if ajutuu.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ajutuu)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ajutuu): ajutuu = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox anaajaalaakua_ipa_ajutuu akua_ipaa_ajutuu ajachitia: ' + liinia)
        결과[이름] = ajutuu
    return 결과


def 등록목록(alu_ujatüü_ajutuu):
    결과 = {}
    for liinia in alu_ujatüü_ajutuu.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', liinia)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(wopu_a_ttaaleemüin):
    ajutuu = hashlib.sha256()
    with wopu_a_ttaaleemüin.open('rb') as anaajaalaa:
        for atijaaya in iter(lambda: anaajaalaa.read(1024 * 1024), b''): ajutuu.update(atijaaya)
    return ajutuu.hexdigest()


class 실행기:
    def __init__(self, 뿌리, 이름, 방식='gui', aluwataaya=명령실행):
        self.뿌리 = Path(뿌리).resolve()
        self.이름, self.방식, self.aluwataaya = 이름, 방식, aluwataaya
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', 이름) or 이름 in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def wopu_a_ttaaleemüin(self, wanaawasü_ajutuu):
        if Path(wanaawasü_ajutuu).is_absolute() or '..' in Path(wanaawasü_ajutuu).parts:
            raise 실행오류('잘못된 관리 wopu_a_ttaaleemüin: ' + str(wanaawasü_ajutuu))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(wanaawasü_ajutuu).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('a_ataa 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        wopu_a_ttaaleemüin = self.wopu_a_ttaaleemüin('state.json')
        if not wopu_a_ttaaleemüin.exists(): return None
        jamakua_iparülein_ajutuu = json.loads(wopu_a_ttaaleemüin.read_text(encoding='utf-8'))
        if jamakua_iparülein_ajutuu.get('version') != 1 or jamakua_iparülein_ajutuu.get('name') != self.이름:
            raise 실행오류('관리 상태의 VM 이름/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for 이름 in ('uuid', 'owner'):
            if str(uuid.UUID(jamakua_iparülein_ajutuu[이름])) != jamakua_iparülein_ajutuu[이름]: raise 실행오류('잘못된 VM 식별자')
        return jamakua_iparülein_ajutuu

    def 저장(self, jamakua_iparülein_ajutuu):
        jalamüinjatü_ajutuu = self.wopu_a_ttaaleemüin('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as anaajaalaa:
            json.dump(jamakua_iparülein_ajutuu, anaajaalaa, ensure_ascii=False, indent=2)
            anaajaalaa.write('\n')
            임시 = anaajaalaa.name
        os.replace(임시, str(jalamüinjatü_ajutuu))

    def 정보(self, jamakua_iparülein_ajutuu, 등록됨, 복구=False):
        if jamakua_iparülein_ajutuu['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        정보 = anaajaalaakua_ipa_ajutuu(self.aluwataaya(['VBoxManage', 'showvminfo', jamakua_iparülein_ajutuu['uuid'], '--machinereadable']))
        위치 = Path(정보.get('CfgFile', '')).resolve()
        if self.wopu_a_ttaaleemüin('machines').resolve() not in 위치.parents or 정보.get('UUID') != jamakua_iparülein_ajutuu['uuid']:
            raise 실행오류('이 프로젝트의 VM 설정 wopu_a_ttaaleemüin/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.aluwataaya(['VBoxManage', 'getextradata', jamakua_iparülein_ajutuu['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + jamakua_iparülein_ajutuu['owner']:
            if 복구 and jamakua_iparülein_ajutuu.get('pending') and 표식 == 'No value set!':
                self.aluwataaya(['VBoxManage', 'setextradata', jamakua_iparülein_ajutuu['uuid'], 'JKOROS/Owner', jamakua_iparülein_ajutuu['owner']])
            else:
                raise 실행오류('VM 소유 표식이 일치하지 않아 변경하지 않습니다.')
        return 정보

    def cheeke_anaajaaleeirua(self, jamakua_iparülein_ajutuu, 정보):
        제어기들 = [ajutuu for 이름, ajutuu in 정보.items() if re.fullmatch(r'storagecontrollername\d+', 이름)]
        A_tte_eraa_ajutuu = [str(self.wopu_a_ttaaleemüin(ajutuu)) for ajutuu in jamakua_iparülein_ajutuu.get('media', [])]
        for 이름, ajutuu in 정보.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', 이름) for 제어기 in 제어기들):
                if ajutuu not in ('none', 'emptydrive') and ajutuu not in A_tte_eraa_ajutuu:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ajutuu)

    def 상태보기(self):
        jamakua_iparülein_ajutuu = self.읽기()
        if jamakua_iparülein_ajutuu is None: return {'name': self.이름, 'state': 'not-created'}
        정보 = self.정보(jamakua_iparülein_ajutuu, 등록목록(self.aluwataaya(['VBoxManage', 'list', 'vms'])))
        return {'name': 정보.get('name', jamakua_iparülein_ajutuu['name']), 'uuid': jamakua_iparülein_ajutuu['uuid'], 'state': 정보.get('VMState'),
                'iso': str(self.wopu_a_ttaaleemüin(jamakua_iparülein_ajutuu['iso'])) if jamakua_iparülein_ajutuu.get('iso') else None,
                'serial_log': str(self.wopu_a_ttaaleemüin(jamakua_iparülein_ajutuu['serial_log'])) if jamakua_iparülein_ajutuu.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        jamakua_iparülein_ajutuu = self.읽기()
        등록됨 = 등록목록(self.aluwataaya(['VBoxManage', 'list', 'vms']))
        정보 = None
        if jamakua_iparülein_ajutuu is not None and jamakua_iparülein_ajutuu['uuid'] in 등록됨:
            정보 = self.정보(jamakua_iparülein_ajutuu, 등록됨, 복구=True)
            현재 = 정보.get('VMState')
            if 현재 == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.상태보기()
            self.cheeke_anaajaaleeirua(jamakua_iparülein_ajutuu, 정보)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 저장 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.aluwataaya(['VBoxManage', 'controlvm', jamakua_iparülein_ajutuu['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 열기 전에 기존 기록도 보관한다.
                    if jamakua_iparülein_ajutuu.get('serial_log'):
                        원본 = self.wopu_a_ttaaleemüin(jamakua_iparülein_ajutuu['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.wopu_a_ttaaleemüin('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.aluwataaya(['VBoxManage', 'startvm', jamakua_iparülein_ajutuu['uuid'], '--type', self.방식])
                return self.상태보기()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 전환 중입니다 ({}). 작업이 끝난 뒤 다시 실행하세요.'.format(현재))
        elif jamakua_iparülein_ajutuu is not None and not jamakua_iparülein_ajutuu.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.이름 in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # 저장/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.aluwataaya(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        anaajaaleeirua_ajutuu = 'media/kernel-' + 검사합(원본) + '.iso'
        jalamüinjatü_ajutuu = self.wopu_a_ttaaleemüin(anaajaaleeirua_ajutuu)
        jalamüinjatü_ajutuu.parent.mkdir(exist_ok=True)
        if jalamüinjatü_ajutuu.exists():
            if 검사합(jalamüinjatü_ajutuu) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(jalamüinjatü_ajutuu))
        else:
            with tempfile.NamedTemporaryFile(dir=str(jalamüinjatü_ajutuu.parent)) as anaajaalaa:
                shutil.copyfile(str(원본), anaajaalaa.name)
                os.link(anaajaalaa.name, str(jalamüinjatü_ajutuu))

        if jamakua_iparülein_ajutuu is None:
            jamakua_iparülein_ajutuu = {'version': 1, 'name': self.이름, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.저장(jamakua_iparülein_ajutuu)
        if 정보 is None:
            self.aluwataaya(['VBoxManage', 'createvm', '--name', jamakua_iparülein_ajutuu['name'], '--uuid', jamakua_iparülein_ajutuu['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.wopu_a_ttaaleemüin('machines')), '--register'])
            self.aluwataaya(['VBoxManage', 'setextradata', jamakua_iparülein_ajutuu['uuid'], 'JKOROS/Owner', jamakua_iparülein_ajutuu['owner']])
        # akompiraajaa_a_yatawaajiraaya 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        정보 = self.정보(jamakua_iparülein_ajutuu, 등록목록(self.aluwataaya(['VBoxManage', 'list', 'vms'])))
        if 정보.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('akompiraajaa_a_yatawaajiraaya 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.cheeke_anaajaaleeirua(jamakua_iparülein_ajutuu, 정보)
        jamakua_iparülein_ajutuu['iso'] = anaajaaleeirua_ajutuu
        if anaajaaleeirua_ajutuu not in jamakua_iparülein_ajutuu['media']: jamakua_iparülein_ajutuu['media'].append(anaajaaleeirua_ajutuu)
        jamakua_iparülein_ajutuu['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        aa_innachikimaajatü_ajutuu = self.wopu_a_ttaaleemüin(jamakua_iparülein_ajutuu['serial_log'])
        aa_innachikimaajatü_ajutuu.parent.mkdir(exist_ok=True)
        self.저장(jamakua_iparülein_ajutuu)
        self.aluwataaya(['VBoxManage', 'modifyvm', jamakua_iparülein_ajutuu['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(aa_innachikimaajatü_ajutuu)])
        제어기들 = [ajutuu for 이름, ajutuu in 정보.items() if re.fullmatch(r'storagecontrollername\d+', 이름)]
        if 'JKOROS IDE' not in 제어기들:
            self.aluwataaya(['VBoxManage', 'storagectl', jamakua_iparülein_ajutuu['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.aluwataaya(['VBoxManage', 'storageattach', jamakua_iparülein_ajutuu['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(jalamüinjatü_ajutuu)])
        jamakua_iparülein_ajutuu['pending'] = False
        self.저장(jamakua_iparülein_ajutuu)
        self.aluwataaya(['VBoxManage', 'startvm', jamakua_iparülein_ajutuu['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.상태보기()


def 시작():
    akatajaa_ajutuu = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 jamakua_iparülein_ajutuu asakiriaa_ajutuu')
    akatajaa_ajutuu.add_argument('action', choices=['run', 'status'])
    인자 = akatajaa_ajutuu.parse_args()
    실행 = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(실행.상태보기(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. epiajatü 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/권한 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.wopu_a_ttaaleemüin('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.wopu_a_ttaaleemüin('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: 시작()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ajachitia:
        print('VBOX ajachitia: ' + str(ajachitia), file=sys.stderr)
        sys.exit(1)
