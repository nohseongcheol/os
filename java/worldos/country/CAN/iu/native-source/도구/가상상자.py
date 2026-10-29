#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 실행기. 기존 VM/디스크/tuqqurli_atuutilik 상태는 삭제하지 않는다."""
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
    결과 = subprocess.run([str(atuutilik) for atuutilik in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Ilulingit_atuutilik = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('piqujijjut itigaqtuq_atuutilik: ' + ' '.join(str(atuutilik) for atuutilik in 인수) + '\n' + Ilulingit_atuutilik[-10000:])
    return Ilulingit_atuutilik


def piuluqqutit_atuutilik(Ilulingit_atuutilik):
    결과 = {}
    for titikutaak in Ilulingit_atuutilik.splitlines():
        if '=' not in titikutaak:
            continue
        atiq, atuutilik = titikutaak.split('=', 1)
        if atiq.startswith('"'):
            atiq = json.loads(atiq)
        if atuutilik.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(atuutilik)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(atuutilik): atuutilik = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox piuluqqutit_atuutilik aaqqisurli_atuutilik tammarniq: ' + titikutaak)
        결과[atiq] = atuutilik
    return 결과


def 등록목록(Ilulingit_atuutilik):
    결과 = {}
    for titikutaak in Ilulingit_atuutilik.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', titikutaak)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(aqqut):
    atuutilik = hashlib.sha256()
    with aqqut.open('rb') as ini:
        for titiqqat in iter(lambda: ini.read(1024 * 1024), b''): atuutilik.update(titiqqat)
    return atuutilik.hexdigest()


class 실행기:
    def __init__(self, 뿌리, atiq, 방식='gui', piqujijjut=명령실행):
        self.뿌리 = Path(뿌리).resolve()
        self.atiq, self.방식, self.piqujijjut = atiq, 방식, piqujijjut
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', atiq) or atiq in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def aqqut(self, ilagijaujuq_atuutilik):
        if Path(ilagijaujuq_atuutilik).is_absolute() or '..' in Path(ilagijaujuq_atuutilik).parts:
            raise 실행오류('잘못된 관리 aqqut: ' + str(ilagijaujuq_atuutilik))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(ilagijaujuq_atuutilik).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('kasurli 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        aqqut = self.aqqut('state.json')
        if not aqqut.exists(): return None
        qanuilinganiq_atuutilik = json.loads(aqqut.read_text(encoding='utf-8'))
        if qanuilinganiq_atuutilik.get('version') != 1 or qanuilinganiq_atuutilik.get('name') != self.atiq:
            raise 실행오류('관리 상태의 VM atiq/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for atiq in ('uuid', 'owner'):
            if str(uuid.UUID(qanuilinganiq_atuutilik[atiq])) != qanuilinganiq_atuutilik[atiq]: raise 실행오류('잘못된 VM 식별자')
        return qanuilinganiq_atuutilik

    def tuqqurli_atuutilik(self, qanuilinganiq_atuutilik):
        namunngarvik_atuutilik = self.aqqut('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ini:
            json.dump(qanuilinganiq_atuutilik, ini, ensure_ascii=False, indent=2)
            ini.write('\n')
            임시 = ini.name
        os.replace(임시, str(namunngarvik_atuutilik))

    def msinfo32_exe(self, qanuilinganiq_atuutilik, 등록됨, 복구=False):
        if qanuilinganiq_atuutilik['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = piuluqqutit_atuutilik(self.piqujijjut(['VBoxManage', 'showvminfo', qanuilinganiq_atuutilik['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.aqqut('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != qanuilinganiq_atuutilik['uuid']:
            raise 실행오류('이 프로젝트의 VM 설정 aqqut/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.piqujijjut(['VBoxManage', 'getextradata', qanuilinganiq_atuutilik['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + qanuilinganiq_atuutilik['owner']:
            if 복구 and qanuilinganiq_atuutilik.get('pending') and 표식 == 'No value set!':
                self.piqujijjut(['VBoxManage', 'setextradata', qanuilinganiq_atuutilik['uuid'], 'JKOROS/Owner', qanuilinganiq_atuutilik['owner']])
            else:
                raise 실행오류('VM 소유 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, qanuilinganiq_atuutilik, msinfo32_exe):
        제어기들 = [atuutilik for atiq, atuutilik in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', atiq)]
        Pijunnaqtilli_atuutilik = [str(self.aqqut(atuutilik)) for atuutilik in qanuilinganiq_atuutilik.get('media', [])]
        for atiq, atuutilik in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', atiq) for 제어기 in 제어기들):
                if atuutilik not in ('none', 'emptydrive') and atuutilik not in Pijunnaqtilli_atuutilik:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + atuutilik)

    def saqqilli_qanuilinganiq(self):
        qanuilinganiq_atuutilik = self.읽기()
        if qanuilinganiq_atuutilik is None: return {'name': self.atiq, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(qanuilinganiq_atuutilik, 등록목록(self.piqujijjut(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', qanuilinganiq_atuutilik['name']), 'uuid': qanuilinganiq_atuutilik['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.aqqut(qanuilinganiq_atuutilik['iso'])) if qanuilinganiq_atuutilik.get('iso') else None,
                'serial_log': str(self.aqqut(qanuilinganiq_atuutilik['serial_log'])) if qanuilinganiq_atuutilik.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        qanuilinganiq_atuutilik = self.읽기()
        등록됨 = 등록목록(self.piqujijjut(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if qanuilinganiq_atuutilik is not None and qanuilinganiq_atuutilik['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(qanuilinganiq_atuutilik, 등록됨, 복구=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.saqqilli_qanuilinganiq()
            self.매체검사(qanuilinganiq_atuutilik, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 tuqqurli_atuutilik 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.piqujijjut(['VBoxManage', 'controlvm', qanuilinganiq_atuutilik['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 matuirli 전에 기존 기록도 보관한다.
                    if qanuilinganiq_atuutilik.get('serial_log'):
                        원본 = self.aqqut(qanuilinganiq_atuutilik['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.aqqut('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.piqujijjut(['VBoxManage', 'startvm', qanuilinganiq_atuutilik['uuid'], '--type', self.방식])
                return self.saqqilli_qanuilinganiq()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 kipulli_mode 중입니다 ({}). 작업이 끝난 Utimut_atuutilik 다시 실행하세요.'.format(현재))
        elif qanuilinganiq_atuutilik is not None and not qanuilinganiq_atuutilik.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.atiq in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # tuqqurli_atuutilik/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.piqujijjut(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        namunngarvik_atuutilik = self.aqqut(매체)
        namunngarvik_atuutilik.parent.mkdir(exist_ok=True)
        if namunngarvik_atuutilik.exists():
            if 검사합(namunngarvik_atuutilik) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(namunngarvik_atuutilik))
        else:
            with tempfile.NamedTemporaryFile(dir=str(namunngarvik_atuutilik.parent)) as ini:
                shutil.copyfile(str(원본), ini.name)
                os.link(ini.name, str(namunngarvik_atuutilik))

        if qanuilinganiq_atuutilik is None:
            qanuilinganiq_atuutilik = {'version': 1, 'name': self.atiq, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.tuqqurli_atuutilik(qanuilinganiq_atuutilik)
        if msinfo32_exe is None:
            self.piqujijjut(['VBoxManage', 'createvm', '--name', qanuilinganiq_atuutilik['name'], '--uuid', qanuilinganiq_atuutilik['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.aqqut('machines')), '--register'])
            self.piqujijjut(['VBoxManage', 'setextradata', qanuilinganiq_atuutilik['uuid'], 'JKOROS/Owner', qanuilinganiq_atuutilik['owner']])
        # sanali_qarasaujaq 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(qanuilinganiq_atuutilik, 등록목록(self.piqujijjut(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('sanali_qarasaujaq 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(qanuilinganiq_atuutilik, msinfo32_exe)
        qanuilinganiq_atuutilik['iso'] = 매체
        if 매체 not in qanuilinganiq_atuutilik['media']: qanuilinganiq_atuutilik['media'].append(매체)
        qanuilinganiq_atuutilik['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        papattivik_atuutilik = self.aqqut(qanuilinganiq_atuutilik['serial_log'])
        papattivik_atuutilik.parent.mkdir(exist_ok=True)
        self.tuqqurli_atuutilik(qanuilinganiq_atuutilik)
        self.piqujijjut(['VBoxManage', 'modifyvm', qanuilinganiq_atuutilik['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(papattivik_atuutilik)])
        제어기들 = [atuutilik for atiq, atuutilik in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', atiq)]
        if 'JKOROS IDE' not in 제어기들:
            self.piqujijjut(['VBoxManage', 'storagectl', qanuilinganiq_atuutilik['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.piqujijjut(['VBoxManage', 'storageattach', qanuilinganiq_atuutilik['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(namunngarvik_atuutilik)])
        qanuilinganiq_atuutilik['pending'] = False
        self.tuqqurli_atuutilik(qanuilinganiq_atuutilik)
        self.piqujijjut(['VBoxManage', 'startvm', qanuilinganiq_atuutilik['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.saqqilli_qanuilinganiq()


def 시작():
    agguqtuut_atuutilik = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 qanuilinganiq_atuutilik kiggusiqarialik_atuutilik')
    agguqtuut_atuutilik.add_argument('action', choices=['run', 'status'])
    인자 = agguqtuut_atuutilik.parse_args()
    실행 = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(실행.saqqilli_qanuilinganiq(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. tuttarvik 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/pijunnaqtittijjut_atuutilik 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.aqqut('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.aqqut('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: 시작()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as tammarniq:
        print('VBOX tammarniq: ' + str(tammarniq), file=sys.stderr)
        sys.exit(1)
