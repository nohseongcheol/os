#!/usr/bin/env python3
"""jkoros 전용 VirtualBox inkqubo_idrowa_yosetyenziso. 기존 VM/디스크/Store_ixabiso 상태는 삭제하지 않는다."""
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


def ukwenza_isiniki_myalelo_umyalelo(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(ixabiso) for ixabiso in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Isiqulatho_ixabiso = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Umyalelo ukungaphumeleli_ixabiso: ' + ' '.join(str(ixabiso) for ixabiso in 인수) + '\n' + Isiqulatho_ixabiso[-10000:])
    return Isiqulatho_ixabiso


def uphawu_ixabiso(Isiqulatho_ixabiso):
    결과 = {}
    for umgca in Isiqulatho_ixabiso.splitlines():
        if '=' not in umgca:
            continue
        Igama, ixabiso = umgca.split('=', 1)
        if Igama.startswith('"'):
            Igama = json.loads(Igama)
        if ixabiso.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ixabiso)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ixabiso): ixabiso = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox uphawu_ixabiso fomatha_ixabiso Impazamo: ' + umgca)
        결과[Igama] = ixabiso
    return 결과


def 등록목록(Isiqulatho_ixabiso):
    결과 = {}
    for umgca in Isiqulatho_ixabiso.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', umgca)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(INDLELA):
    ixabiso = hashlib.sha256()
    with INDLELA.open('rb') as iFayili:
        for iingcombolo in iter(lambda: iFayili.read(1024 * 1024), b''): ixabiso.update(iingcombolo)
    return ixabiso.hexdigest()


class inkqubo_idrowa_yosetyenziso:
    def __init__(self, 뿌리, Igama, imethodi_imo='gui', Umyalelo=ukwenza_isiniki_myalelo_umyalelo):
        self.뿌리 = Path(뿌리).resolve()
        self.Igama, self.imethodi_imo, self.Umyalelo = Igama, imethodi_imo, Umyalelo
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Igama) or Igama in ('.', '..'):
            raise 실행오류('VM 이름은 문자·inani_ixabiso·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if imethodi_imo not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def INDLELA(self, untanga_ixabiso):
        if Path(untanga_ixabiso).is_absolute() or '..' in Path(untanga_ixabiso).parts:
            raise 실행오류('잘못된 관리 INDLELA: ' + str(untanga_ixabiso))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(untanga_ixabiso).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Nxulumanisa 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Funda(self):
        INDLELA = self.INDLELA('state.json')
        if not INDLELA.exists(): return None
        imo_ixabiso = json.loads(INDLELA.read_text(encoding='utf-8'))
        if imo_ixabiso.get('version') != 1 or imo_ixabiso.get('name') != self.Igama:
            raise 실행오류('관리 상태의 VM Igama/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Igama in ('uuid', 'owner'):
            if str(uuid.UUID(imo_ixabiso[Igama])) != imo_ixabiso[Igama]: raise 실행오류('잘못된 VM isalathisi_ixabiso')
        return imo_ixabiso

    def Store_ixabiso(self, imo_ixabiso):
        indawo_ekuyiwa_kuyo_ixabiso = self.INDLELA('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as iFayili:
            json.dump(imo_ixabiso, iFayili, ensure_ascii=False, indent=2)
            iFayili.write('\n')
            임시 = iFayili.name
        os.replace(임시, str(indawo_ekuyiwa_kuyo_ixabiso))

    def i_msinfo32_exe(self, imo_ixabiso, 등록됨, fumana_kwakhona_imo=False):
        if imo_ixabiso['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        i_msinfo32_exe = uphawu_ixabiso(self.Umyalelo(['VBoxManage', 'showvminfo', imo_ixabiso['uuid'], '--machinereadable']))
        위치 = Path(i_msinfo32_exe.get('CfgFile', '')).resolve()
        if self.INDLELA('machines').resolve() not in 위치.parents or i_msinfo32_exe.get('UUID') != imo_ixabiso['uuid']:
            raise 실행오류('이 프로젝트의 VM Imimiselo INDLELA/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Umyalelo(['VBoxManage', 'getextradata', imo_ixabiso['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + imo_ixabiso['owner']:
            if fumana_kwakhona_imo and imo_ixabiso.get('pending') and 표식 == 'No value set!':
                self.Umyalelo(['VBoxManage', 'setextradata', imo_ixabiso['uuid'], 'JKOROS/Owner', imo_ixabiso['owner']])
            else:
                raise 실행오류('VM umnini_ixabiso 표식이 일치하지 않아 변경하지 않습니다.')
        return i_msinfo32_exe

    def 매체검사(self, imo_ixabiso, i_msinfo32_exe):
        제어기들 = [ixabiso for Igama, ixabiso in i_msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Igama)]
        vumela_ixabiso = [str(self.INDLELA(ixabiso)) for ixabiso in imo_ixabiso.get('media', [])]
        for Igama, ixabiso in i_msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Igama) for 제어기 in 제어기들):
                if ixabiso not in ('none', 'emptydrive') and ixabiso not in vumela_ixabiso:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ixabiso)

    def bonisa_imo(self):
        imo_ixabiso = self.Funda()
        if imo_ixabiso is None: return {'name': self.Igama, 'state': 'not-created'}
        i_msinfo32_exe = self.i_msinfo32_exe(imo_ixabiso, 등록목록(self.Umyalelo(['VBoxManage', 'list', 'vms'])))
        return {'name': i_msinfo32_exe.get('name', imo_ixabiso['name']), 'uuid': imo_ixabiso['uuid'], 'state': i_msinfo32_exe.get('VMState'),
                'iso': str(self.INDLELA(imo_ixabiso['iso'])) if imo_ixabiso.get('iso') else None,
                'serial_log': str(self.INDLELA(imo_ixabiso['serial_log'])) if imo_ixabiso.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ukwenza_umyalelo(self):
        imo_ixabiso = self.Funda()
        등록됨 = 등록목록(self.Umyalelo(['VBoxManage', 'list', 'vms']))
        i_msinfo32_exe = None
        if imo_ixabiso is not None and imo_ixabiso['uuid'] in 등록됨:
            i_msinfo32_exe = self.i_msinfo32_exe(imo_ixabiso, 등록됨, fumana_kwakhona_imo=True)
            현재 = i_msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 ukwenza_umyalelo 중입니다. 재빌드·재시작하지 않습니다.')
                return self.bonisa_imo()
            self.매체검사(imo_ixabiso, i_msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_ixabiso 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Umyalelo(['VBoxManage', 'controlvm', imo_ixabiso['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Vula 전에 기존 기록도 보관한다.
                    if imo_ixabiso.get('serial_log'):
                        원본 = self.INDLELA(imo_ixabiso['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.INDLELA('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Umyalelo(['VBoxManage', 'startvm', imo_ixabiso['uuid'], '--type', self.imethodi_imo])
                return self.bonisa_imo()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 tshintshela_imo 중입니다 ({}). 작업이 끝난 Emva_ixabiso 다시 실행하세요.'.format(현재))
        elif imo_ixabiso is not None and not imo_ixabiso.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Igama in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_ixabiso/ukwenza_umyalelo 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Umyalelo(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        indawo_ekuyiwa_kuyo_ixabiso = self.INDLELA(매체)
        indawo_ekuyiwa_kuyo_ixabiso.parent.mkdir(exist_ok=True)
        if indawo_ekuyiwa_kuyo_ixabiso.exists():
            if 검사합(indawo_ekuyiwa_kuyo_ixabiso) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(indawo_ekuyiwa_kuyo_ixabiso))
        else:
            with tempfile.NamedTemporaryFile(dir=str(indawo_ekuyiwa_kuyo_ixabiso.parent)) as iFayili:
                shutil.copyfile(str(원본), iFayili.name)
                os.link(iFayili.name, str(indawo_ekuyiwa_kuyo_ixabiso))

        if imo_ixabiso is None:
            imo_ixabiso = {'version': 1, 'name': self.Igama, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_ixabiso(imo_ixabiso)
        if i_msinfo32_exe is None:
            self.Umyalelo(['VBoxManage', 'createvm', '--name', imo_ixabiso['name'], '--uuid', imo_ixabiso['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.INDLELA('machines')), '--register'])
            self.Umyalelo(['VBoxManage', 'setextradata', imo_ixabiso['uuid'], 'JKOROS/Owner', imo_ixabiso['owner']])
        # yakha_inkqubo 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        i_msinfo32_exe = self.i_msinfo32_exe(imo_ixabiso, 등록목록(self.Umyalelo(['VBoxManage', 'list', 'vms'])))
        if i_msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('yakha_inkqubo 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(imo_ixabiso, i_msinfo32_exe)
        imo_ixabiso['iso'] = 매체
        if 매체 not in imo_ixabiso['media']: imo_ixabiso['media'].append(매체)
        imo_ixabiso['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ilog_ixabiso = self.INDLELA(imo_ixabiso['serial_log'])
        ilog_ixabiso.parent.mkdir(exist_ok=True)
        self.Store_ixabiso(imo_ixabiso)
        self.Umyalelo(['VBoxManage', 'modifyvm', imo_ixabiso['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ilog_ixabiso)])
        제어기들 = [ixabiso for Igama, ixabiso in i_msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Igama)]
        if 'JKOROS IDE' not in 제어기들:
            self.Umyalelo(['VBoxManage', 'storagectl', imo_ixabiso['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Umyalelo(['VBoxManage', 'storageattach', imo_ixabiso['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(indawo_ekuyiwa_kuyo_ixabiso)])
        imo_ixabiso['pending'] = False
        self.Store_ixabiso(imo_ixabiso)
        self.Umyalelo(['VBoxManage', 'startvm', imo_ixabiso['uuid'], '--type', self.imethodi_imo])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.bonisa_imo()


def Phumeza():
    ingcaciso_yegama_ixabiso = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ukwenza_umyalelo 및 imo_ixabiso umbuzo_ixabiso')
    ingcaciso_yegama_ixabiso.add_argument('action', choices=['run', 'status'])
    인자 = ingcaciso_yegama_ixabiso.parse_args()
    ukwenza_umyalelo = inkqubo_idrowa_yosetyenziso(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ukwenza_umyalelo.bonisa_imo(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. umsingathi 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/imvume_ixabiso 변경은 하지 않습니다.')
    os.umask(0o077)
    ukwenza_umyalelo.INDLELA('lock').parent.mkdir(parents=True, exist_ok=True)
    with ukwenza_umyalelo.INDLELA('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ukwenza_umyalelo 작업이 진행 중입니다.')
        print(json.dumps(ukwenza_umyalelo.ukwenza_umyalelo(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Phumeza()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Impazamo:
        print('VBOX Impazamo: ' + str(Impazamo), file=sys.stderr)
        sys.exit(1)
