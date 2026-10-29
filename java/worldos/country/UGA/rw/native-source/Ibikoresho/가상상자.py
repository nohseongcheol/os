#!/usr/bin/env python3
"""jkoros 전용 VirtualBox porogaramu_umukozi. 기존 VM/디스크/Store_agaciro 상태는 삭제하지 않는다."""
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


def gukora_insomamabwiriza_ibwiriza(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(agaciro) for agaciro in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Ibirimo_agaciro = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Icyo_wifuza kudakora_agaciro: ' + ' '.join(str(agaciro) for agaciro in 인수) + '\n' + Ibirimo_agaciro[-10000:])
    return Ibirimo_agaciro


def ikiranga_agaciro(Ibirimo_agaciro):
    결과 = {}
    for umurongo in Ibirimo_agaciro.splitlines():
        if '=' not in umurongo:
            continue
        Izina, agaciro = umurongo.split('=', 1)
        if Izina.startswith('"'):
            Izina = json.loads(Izina)
        if agaciro.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(agaciro)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(agaciro): agaciro = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ikiranga_agaciro imiterere_agaciro IKOSA: ' + umurongo)
        결과[Izina] = agaciro
    return 결과


def 등록목록(Ibirimo_agaciro):
    결과 = {}
    for umurongo in Ibirimo_agaciro.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', umurongo)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(Inzira):
    agaciro = hashlib.sha256()
    with Inzira.open('rb') as Idosiye:
        for amakurushingiro in iter(lambda: Idosiye.read(1024 * 1024), b''): agaciro.update(amakurushingiro)
    return agaciro.hexdigest()


class porogaramu_umukozi:
    def __init__(self, 뿌리, Izina, uburyo_uburyo='gui', Icyo_wifuza=gukora_insomamabwiriza_ibwiriza):
        self.뿌리 = Path(뿌리).resolve()
        self.Izina, self.uburyo_uburyo, self.Icyo_wifuza = Izina, uburyo_uburyo, Icyo_wifuza
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Izina) or Izina in ('.', '..'):
            raise 실행오류('VM 이름은 문자·umubare_agaciro·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if uburyo_uburyo not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Inzira(self, Mugenzi_agaciro):
        if Path(Mugenzi_agaciro).is_absolute() or '..' in Path(Mugenzi_agaciro).parts:
            raise 실행오류('잘못된 관리 Inzira: ' + str(Mugenzi_agaciro))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(Mugenzi_agaciro).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Guhuza 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        Inzira = self.Inzira('state.json')
        if not Inzira.exists(): return None
        imimerere_agaciro = json.loads(Inzira.read_text(encoding='utf-8'))
        if imimerere_agaciro.get('version') != 1 or imimerere_agaciro.get('name') != self.Izina:
            raise 실행오류('관리 상태의 VM Izina/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Izina in ('uuid', 'owner'):
            if str(uuid.UUID(imimerere_agaciro[Izina])) != imimerere_agaciro[Izina]: raise 실행오류('잘못된 VM indanga_agaciro')
        return imimerere_agaciro

    def Store_agaciro(self, imimerere_agaciro):
        aho_ijya_agaciro = self.Inzira('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Idosiye:
            json.dump(imimerere_agaciro, Idosiye, ensure_ascii=False, indent=2)
            Idosiye.write('\n')
            임시 = Idosiye.name
        os.replace(임시, str(aho_ijya_agaciro))

    def msinfo32_exe(self, imimerere_agaciro, 등록됨, kugarura_imimerere=False):
        if imimerere_agaciro['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = ikiranga_agaciro(self.Icyo_wifuza(['VBoxManage', 'showvminfo', imimerere_agaciro['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Inzira('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != imimerere_agaciro['uuid']:
            raise 실행오류('이 프로젝트의 VM Amagenamiterere Inzira/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Icyo_wifuza(['VBoxManage', 'getextradata', imimerere_agaciro['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + imimerere_agaciro['owner']:
            if kugarura_imimerere and imimerere_agaciro.get('pending') and 표식 == 'No value set!':
                self.Icyo_wifuza(['VBoxManage', 'setextradata', imimerere_agaciro['uuid'], 'JKOROS/Owner', imimerere_agaciro['owner']])
            else:
                raise 실행오류('VM nyirayo_agaciro 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, imimerere_agaciro, msinfo32_exe):
        제어기들 = [agaciro for Izina, agaciro in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Izina)]
        Kwemerera_agaciro = [str(self.Inzira(agaciro)) for agaciro in imimerere_agaciro.get('media', [])]
        for Izina, agaciro in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Izina) for 제어기 in 제어기들):
                if agaciro not in ('none', 'emptydrive') and agaciro not in Kwemerera_agaciro:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + agaciro)

    def kugaragaza_imimerere(self):
        imimerere_agaciro = self.읽기()
        if imimerere_agaciro is None: return {'name': self.Izina, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(imimerere_agaciro, 등록목록(self.Icyo_wifuza(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', imimerere_agaciro['name']), 'uuid': imimerere_agaciro['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Inzira(imimerere_agaciro['iso'])) if imimerere_agaciro.get('iso') else None,
                'serial_log': str(self.Inzira(imimerere_agaciro['serial_log'])) if imimerere_agaciro.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def gukora_ibwiriza(self):
        imimerere_agaciro = self.읽기()
        등록됨 = 등록목록(self.Icyo_wifuza(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if imimerere_agaciro is not None and imimerere_agaciro['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(imimerere_agaciro, 등록됨, kugarura_imimerere=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 gukora_ibwiriza 중입니다. 재빌드·재시작하지 않습니다.')
                return self.kugaragaza_imimerere()
            self.매체검사(imimerere_agaciro, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_agaciro 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Icyo_wifuza(['VBoxManage', 'controlvm', imimerere_agaciro['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Gufungura 전에 기존 기록도 보관한다.
                    if imimerere_agaciro.get('serial_log'):
                        원본 = self.Inzira(imimerere_agaciro['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Inzira('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Icyo_wifuza(['VBoxManage', 'startvm', imimerere_agaciro['uuid'], '--type', self.uburyo_uburyo])
                return self.kugaragaza_imimerere()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 guhinduranya_uburyo 중입니다 ({}). 작업이 끝난 Ikibanza_agaciro 다시 실행하세요.'.format(현재))
        elif imimerere_agaciro is not None and not imimerere_agaciro.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Izina in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_agaciro/gukora_ibwiriza 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Icyo_wifuza(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        aho_ijya_agaciro = self.Inzira(매체)
        aho_ijya_agaciro.parent.mkdir(exist_ok=True)
        if aho_ijya_agaciro.exists():
            if 검사합(aho_ijya_agaciro) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(aho_ijya_agaciro))
        else:
            with tempfile.NamedTemporaryFile(dir=str(aho_ijya_agaciro.parent)) as Idosiye:
                shutil.copyfile(str(원본), Idosiye.name)
                os.link(Idosiye.name, str(aho_ijya_agaciro))

        if imimerere_agaciro is None:
            imimerere_agaciro = {'version': 1, 'name': self.Izina, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_agaciro(imimerere_agaciro)
        if msinfo32_exe is None:
            self.Icyo_wifuza(['VBoxManage', 'createvm', '--name', imimerere_agaciro['name'], '--uuid', imimerere_agaciro['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Inzira('machines')), '--register'])
            self.Icyo_wifuza(['VBoxManage', 'setextradata', imimerere_agaciro['uuid'], 'JKOROS/Owner', imimerere_agaciro['owner']])
        # gusohora_sisitemu 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(imimerere_agaciro, 등록목록(self.Icyo_wifuza(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('gusohora_sisitemu 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(imimerere_agaciro, msinfo32_exe)
        imimerere_agaciro['iso'] = 매체
        if 매체 not in imimerere_agaciro['media']: imimerere_agaciro['media'].append(매체)
        imimerere_agaciro['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        kubika_agaciro = self.Inzira(imimerere_agaciro['serial_log'])
        kubika_agaciro.parent.mkdir(exist_ok=True)
        self.Store_agaciro(imimerere_agaciro)
        self.Icyo_wifuza(['VBoxManage', 'modifyvm', imimerere_agaciro['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(kubika_agaciro)])
        제어기들 = [agaciro for Izina, agaciro in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Izina)]
        if 'JKOROS IDE' not in 제어기들:
            self.Icyo_wifuza(['VBoxManage', 'storagectl', imimerere_agaciro['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Icyo_wifuza(['VBoxManage', 'storageattach', imimerere_agaciro['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(aho_ijya_agaciro)])
        imimerere_agaciro['pending'] = False
        self.Store_agaciro(imimerere_agaciro)
        self.Icyo_wifuza(['VBoxManage', 'startvm', imimerere_agaciro['uuid'], '--type', self.uburyo_uburyo])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.kugaragaza_imimerere()


def ihuriro():
    gusesengura_agaciro = argparse.ArgumentParser(description='jkoros 전용 VirtualBox gukora_ibwiriza 및 imimerere_agaciro isaba_agaciro')
    gusesengura_agaciro.add_argument('action', choices=['run', 'status'])
    인자 = gusesengura_agaciro.parse_args()
    gukora_ibwiriza = porogaramu_umukozi(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(gukora_ibwiriza.kugaragaza_imimerere(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. gucumbikira 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/권한 변경은 하지 않습니다.')
    os.umask(0o077)
    gukora_ibwiriza.Inzira('lock').parent.mkdir(parents=True, exist_ok=True)
    with gukora_ibwiriza.Inzira('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox gukora_ibwiriza 작업이 진행 중입니다.')
        print(json.dumps(gukora_ibwiriza.gukora_ibwiriza(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ihuriro()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as IKOSA:
        print('VBOX IKOSA: ' + str(IKOSA), file=sys.stderr)
        sys.exit(1)
