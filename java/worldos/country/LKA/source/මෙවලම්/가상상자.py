#!/usr/bin/env python3
"""jkoros 전용 VirtualBox යෙදු_යෙදුම්_ලාච්චුව. 기존 VM/디스크/ගබඩා_කරන්න_අගය 상태는 삭제하지 않는다."""
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


def ක්_රියාත්මක_කරන්න_කවචය_විධානය(විස්තාරක):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(අගය) for අගය in විස්තාරක], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    අන්තර්ගතය_අගය = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('විධානය අසමත්වීම_අගය: ' + ' '.join(str(අගය) for අගය in විස්තාරක) + '\n' + අන්තර්ගතය_අගය[-10000:])
    return අන්තර්ගතය_අගය


def ගුණාංගය_අගය(අන්තර්ගතය_අගය):
    결과 = {}
    for පේළිය in අන්තර්ගතය_අගය.splitlines():
        if '=' not in පේළිය:
            continue
        නම, අගය = පේළිය.split('=', 1)
        if නම.startswith('"'):
            නම = json.loads(නම)
        if අගය.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(අගය)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(අගය): අගය = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ගුණාංගය_අගය හැඩතලය_අගය දෝෂය: ' + පේළිය)
        결과[නම] = අගය
    return 결과


def 등록목록(අන්තර්ගතය_අගය):
    결과 = {}
    for පේළිය in අන්තර්ගතය_අගය.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', පේළිය)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(මාර්_ගය):
    අගය = hashlib.sha256()
    with මාර්_ගය.open('rb') as ගොනු:
        for දත්ත in iter(lambda: ගොනු.read(1024 * 1024), b''): අගය.update(දත්ත)
    return අගය.hexdigest()


class යෙදු_යෙදුම්_ලාච්චුව:
    def __init__(self, 뿌리, නම, ක්_රමය_ප්_රකාරය='gui', විධානය=ක්_රියාත්මක_කරන්න_කවචය_විධානය):
        self.뿌리 = Path(뿌리).resolve()
        self.නම, self.ක්_රමය_ප්_රකාරය, self.විධානය = නම, ක්_රමය_ප්_රකාරය, විධානය
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', නම) or නම in ('.', '..'):
            raise 실행오류('VM 이름은 문자·සංඛ්_යාංකය_අගය·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ක්_රමය_ප්_රකාරය not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def මාර්_ගය(self, සමානයා_අගය):
        if Path(සමානයා_අගය).is_absolute() or '..' in Path(සමානයා_අගය).parts:
            raise 실행오류('잘못된 관리 මාර්_ගය: ' + str(සමානයා_අගය))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(සමානයා_අගය).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('සම්බන්ද_වන්න 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def කියවීම(self):
        මාර්_ගය = self.මාර්_ගය('state.json')
        if not මාර්_ගය.exists(): return None
        තත්වය_අගය = json.loads(මාර්_ගය.read_text(encoding='utf-8'))
        if තත්වය_අගය.get('version') != 1 or තත්වය_අගය.get('name') != self.නම:
            raise 실행오류('관리 상태의 VM නම/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for නම in ('uuid', 'owner'):
            if str(uuid.UUID(තත්වය_අගය[නම])) != තත්වය_අගය[නම]: raise 실행오류('잘못된 VM හඳුන්වනය_අගය')
        return තත්වය_අගය

    def ගබඩා_කරන්න_අගය(self, තත්වය_අගය):
        ගමනාන්තය_අගය = self.මාර්_ගය('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ගොනු:
            json.dump(තත්වය_අගය, ගොනු, ensure_ascii=False, indent=2)
            ගොනු.write('\n')
            임시 = ගොනු.name
        os.replace(임시, str(ගමනාන්තය_අගය))

    def පද්ධති_තොරතුරු(self, තත්වය_අගය, 등록됨, නැවත_ලබාගන්න_තත්වය=False):
        if තත්වය_අගය['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        පද්ධති_තොරතුරු = ගුණාංගය_අගය(self.විධානය(['VBoxManage', 'showvminfo', තත්වය_අගය['uuid'], '--machinereadable']))
        පිහිටීම = Path(පද්ධති_තොරතුරු.get('CfgFile', '')).resolve()
        if self.මාර්_ගය('machines').resolve() not in පිහිටීම.parents or පද්ධති_තොරතුරු.get('UUID') != තත්වය_අගය['uuid']:
            raise 실행오류('이 프로젝트의 VM සැකසුම් මාර්_ගය/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.විධානය(['VBoxManage', 'getextradata', තත්වය_අගය['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + තත්වය_අගය['owner']:
            if නැවත_ලබාගන්න_තත්වය and තත්වය_අගය.get('pending') and 표식 == 'No value set!':
                self.විධානය(['VBoxManage', 'setextradata', තත්වය_අගය['uuid'], 'JKOROS/Owner', තත්වය_අගය['owner']])
            else:
                raise 실행오류('VM හිමිකරු_අගය 표식이 일치하지 않아 변경하지 않습니다.')
        return පද්ධති_තොරතුරු

    def 매체검사(self, තත්වය_අගය, පද්ධති_තොරතුරු):
        제어기들 = [අගය for නම, අගය in පද්ධති_තොරතුරු.items() if re.fullmatch(r'storagecontrollername\d+', නම)]
        ඉඩ_දෙන්න_අගය = [str(self.මාර්_ගය(අගය)) for අගය in තත්වය_අගය.get('media', [])]
        for නම, අගය in පද්ධති_තොරතුරු.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', නම) for 제어기 in 제어기들):
                if අගය not in ('none', 'emptydrive') and අගය not in ඉඩ_දෙන්න_අගය:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + අගය)

    def දර්ශනය_තත්වය(self):
        තත්වය_අගය = self.කියවීම()
        if තත්වය_අගය is None: return {'name': self.නම, 'state': 'not-created'}
        පද්ධති_තොරතුරු = self.පද්ධති_තොරතුරු(තත්වය_අගය, 등록목록(self.විධානය(['VBoxManage', 'list', 'vms'])))
        return {'name': පද්ධති_තොරතුරු.get('name', තත්වය_අගය['name']), 'uuid': තත්වය_අගය['uuid'], 'state': පද්ධති_තොරතුරු.get('VMState'),
                'iso': str(self.මාර්_ගය(තත්වය_අගය['iso'])) if තත්වය_අගය.get('iso') else None,
                'serial_log': str(self.මාර්_ගය(තත්වය_අගය['serial_log'])) if තත්වය_අගය.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ක්_රියාත්මක_කරන්න_විධානය(self):
        තත්වය_අගය = self.කියවීම()
        등록됨 = 등록목록(self.විධානය(['VBoxManage', 'list', 'vms']))
        පද්ධති_තොරතුරු = None
        if තත්වය_අගය is not None and තත්වය_අගය['uuid'] in 등록됨:
            පද්ධති_තොරතුරු = self.පද්ධති_තොරතුරු(තත්වය_අගය, 등록됨, නැවත_ලබාගන්න_තත්වය=True)
            현재 = පද්ධති_තොරතුරු.get('VMState')
            if 현재 == 'running':
                print('이미 ක්_රියාත්මක_කරන්න_විධානය 중입니다. 재빌드·재시작하지 않습니다.')
                return self.දර්ශනය_තත්වය()
            self.매체검사(තත්වය_අගය, පද්ධති_තොරතුරු)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ගබඩා_කරන්න_අගය 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.විධානය(['VBoxManage', 'controlvm', තත්වය_අගය['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 විවෘත_කරන්න 전에 기존 기록도 보관한다.
                    if තත්වය_අගය.get('serial_log'):
                        원본 = self.මාර්_ගය(තත්වය_අගය['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.මාර්_ගය('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.විධානය(['VBoxManage', 'startvm', තත්වය_අගය['uuid'], '--type', self.ක්_රමය_ප්_රකාරය])
                return self.දර්ශනය_තත්වය()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 මාරු_වන්න_ප්_රකාරය 중입니다 ({}). 작업이 끝난 ආපසු_අගය 다시 실행하세요.'.format(현재))
        elif තත්වය_අගය is not None and not තත්වය_අගය.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.නම in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ගබඩා_කරන්න_අගය/ක්_රියාත්මක_කරන්න_විධානය 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.විධානය(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        ගමනාන්තය_අගය = self.මාර්_ගය(매체)
        ගමනාන්තය_අගය.parent.mkdir(exist_ok=True)
        if ගමනාන්තය_අගය.exists():
            if 검사합(ගමනාන්තය_අගය) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ගමනාන්තය_අගය))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ගමනාන්තය_අගය.parent)) as ගොනු:
                shutil.copyfile(str(원본), ගොනු.name)
                os.link(ගොනු.name, str(ගමනාන්තය_අගය))

        if තත්වය_අගය is None:
            තත්වය_අගය = {'version': 1, 'name': self.නම, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ගබඩා_කරන්න_අගය(තත්වය_අගය)
        if පද්ධති_තොරතුරු is None:
            self.විධානය(['VBoxManage', 'createvm', '--name', තත්වය_අගය['name'], '--uuid', තත්වය_අගය['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.මාර්_ගය('machines')), '--register'])
            self.විධානය(['VBoxManage', 'setextradata', තත්වය_අගය['uuid'], 'JKOROS/Owner', තත්වය_අගය['owner']])
        # තැනුම_පද්ධතිය 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        පද්ධති_තොරතුරු = self.පද්ධති_තොරතුරු(තත්වය_අගය, 등록목록(self.විධානය(['VBoxManage', 'list', 'vms'])))
        if පද්ධති_තොරතුරු.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('තැනුම_පද්ධතිය 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(තත්වය_අගය, පද්ධති_තොරතුරු)
        තත්වය_අගය['iso'] = 매체
        if 매체 not in තත්වය_අගය['media']: තත්වය_අගය['media'].append(매체)
        තත්වය_අගය['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ලොගය_අගය = self.මාර්_ගය(තත්වය_අගය['serial_log'])
        ලොගය_අගය.parent.mkdir(exist_ok=True)
        self.ගබඩා_කරන්න_අගය(තත්වය_අගය)
        self.විධානය(['VBoxManage', 'modifyvm', තත්වය_අගය['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ලොගය_අගය)])
        제어기들 = [අගය for නම, අගය in පද්ධති_තොරතුරු.items() if re.fullmatch(r'storagecontrollername\d+', නම)]
        if 'JKOROS IDE' not in 제어기들:
            self.විධානය(['VBoxManage', 'storagectl', තත්වය_අගය['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.විධානය(['VBoxManage', 'storageattach', තත්වය_අගය['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ගමනාන්තය_අගය)])
        තත්වය_අගය['pending'] = False
        self.ගබඩා_කරන්න_අගය(තත්වය_අගය)
        self.විධානය(['VBoxManage', 'startvm', තත්වය_අගය['uuid'], '--type', self.ක්_රමය_ප්_රකාරය])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.දර්ශනය_තත්වය()


def ක්_රියාත්මක_කරන්න_2():
    විශ්ලේෂණය_කරන්න_අගය = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ක්_රියාත්මක_කරන්න_විධානය 및 තත්වය_අගය විමසුම_අගය')
    විශ්ලේෂණය_කරන්න_අගය.add_argument('action', choices=['run', 'status'])
    인자 = විශ්ලේෂණය_කරන්න_අගය.parse_args()
    ක්_රියාත්මක_කරන්න_විධානය = යෙදු_යෙදුම්_ලාච්චුව(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ක්_රියාත්මක_කරන්න_විධානය.දර්ශනය_තත්වය(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ධාරකය 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/අවසරය_අගය 변경은 하지 않습니다.')
    os.umask(0o077)
    ක්_රියාත්මක_කරන්න_විධානය.මාර්_ගය('lock').parent.mkdir(parents=True, exist_ok=True)
    with ක්_රියාත්මක_කරන්න_විධානය.මාර්_ගය('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ක්_රියාත්මක_කරන්න_විධානය 작업이 진행 중입니다.')
        print(json.dumps(ක්_රියාත්මක_කරන්න_විධානය.ක්_රියාත්මක_කරන්න_විධානය(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ක්_රියාත්මක_කරන්න_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as දෝෂය:
        print('VBOX දෝෂය: ' + str(දෝෂය), file=sys.stderr)
        sys.exit(1)
