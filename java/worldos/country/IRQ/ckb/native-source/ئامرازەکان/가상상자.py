#!/usr/bin/env python3
"""jkoros 전용 VirtualBox بەرنامە_ئەندامی_ستاف. 기존 VM/디스크/Store_نرخ 상태는 삭제하지 않는다."""
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


def جێبەجێکردن_توێکڵ_فەرمان(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(نرخ) for نرخ in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ناوەرۆک_نرخ = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('فەرمان شکستهێنان_نرخ: ' + ' '.join(str(نرخ) for نرخ in 인수) + '\n' + ناوەرۆک_نرخ[-10000:])
    return ناوەرۆک_نرخ


def تایبەتمەندی_نرخ(ناوەرۆک_نرخ):
    결과 = {}
    for دێڕ in ناوەرۆک_نرخ.splitlines():
        if '=' not in دێڕ:
            continue
        ناو, نرخ = دێڕ.split('=', 1)
        if ناو.startswith('"'):
            ناو = json.loads(ناو)
        if نرخ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(نرخ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(نرخ): نرخ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox تایبەتمەندی_نرخ بیچم_نرخ هەڵە: ' + دێڕ)
        결과[ناو] = نرخ
    return 결과


def 등록목록(ناوەرۆک_نرخ):
    결과 = {}
    for دێڕ in ناوەرۆک_نرخ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', دێڕ)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(گوزەر):
    نرخ = hashlib.sha256()
    with گوزەر.open('rb') as فایل:
        for دەیتا in iter(lambda: فایل.read(1024 * 1024), b''): نرخ.update(دەیتا)
    return نرخ.hexdigest()


class بەرنامە_ئەندامی_ستاف:
    def __init__(self, 뿌리, ناو, ڕێگا_دۆخ='gui', فەرمان=جێبەجێکردن_توێکڵ_فەرمان):
        self.뿌리 = Path(뿌리).resolve()
        self.ناو, self.ڕێگا_دۆخ, self.فەرمان = ناو, ڕێگا_دۆخ, فەرمان
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ناو) or ناو in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ڕه_نووس_نرخ·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ڕێگا_دۆخ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def گوزەر(self, هاوتا_نرخ):
        if Path(هاوتا_نرخ).is_absolute() or '..' in Path(هاوتا_نرخ).parts:
            raise 실행오류('잘못된 관리 گوزەر: ' + str(هاوتا_نرخ))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(هاوتا_نرخ).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('لكاندن 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        گوزەر = self.گوزەر('state.json')
        if not گوزەر.exists(): return None
        دۆخ_نرخ = json.loads(گوزەر.read_text(encoding='utf-8'))
        if دۆخ_نرخ.get('version') != 1 or دۆخ_نرخ.get('name') != self.ناو:
            raise 실행오류('관리 상태의 VM ناو/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ناو in ('uuid', 'owner'):
            if str(uuid.UUID(دۆخ_نرخ[ناو])) != دۆخ_نرخ[ناو]: raise 실행오류('잘못된 VM ناسێنەر_نرخ')
        return دۆخ_نرخ

    def Store_نرخ(self, دۆخ_نرخ):
        جێمەبەست_نرخ = self.گوزەر('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as فایل:
            json.dump(دۆخ_نرخ, فایل, ensure_ascii=False, indent=2)
            فایل.write('\n')
            임시 = فایل.name
        os.replace(임시, str(جێمەبەست_نرخ))

    def msinfo32_exe(self, دۆخ_نرخ, 등록됨, گەڕاندنەوە_دۆخ=False):
        if دۆخ_نرخ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = تایبەتمەندی_نرخ(self.فەرمان(['VBoxManage', 'showvminfo', دۆخ_نرخ['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.گوزەر('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != دۆخ_نرخ['uuid']:
            raise 실행오류('이 프로젝트의 VM ڕێكبەندەكان گوزەر/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.فەرمان(['VBoxManage', 'getextradata', دۆخ_نرخ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + دۆخ_نرخ['owner']:
            if گەڕاندنەوە_دۆخ and دۆخ_نرخ.get('pending') and 표식 == 'No value set!':
                self.فەرمان(['VBoxManage', 'setextradata', دۆخ_نرخ['uuid'], 'JKOROS/Owner', دۆخ_نرخ['owner']])
            else:
                raise 실행오류('VM خاوەن_نرخ 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def پشکنین_میدیا(self, دۆخ_نرخ, msinfo32_exe):
        제어기들 = [نرخ for ناو, نرخ in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', ناو)]
        ڕێپێدان_نرخ_688200c4 = [str(self.گوزەر(نرخ)) for نرخ in دۆخ_نرخ.get('media', [])]
        for ناو, نرخ in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', ناو) for 제어기 in 제어기들):
                if نرخ not in ('none', 'emptydrive') and نرخ not in ڕێپێدان_نرخ_688200c4:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + نرخ)

    def نیشاندان_دۆخ(self):
        دۆخ_نرخ = self.읽기()
        if دۆخ_نرخ is None: return {'name': self.ناو, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(دۆخ_نرخ, 등록목록(self.فەرمان(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', دۆخ_نرخ['name']), 'uuid': دۆخ_نرخ['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.گوزەر(دۆخ_نرخ['iso'])) if دۆخ_نرخ.get('iso') else None,
                'serial_log': str(self.گوزەر(دۆخ_نرخ['serial_log'])) if دۆخ_نرخ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def جێبەجێکردن_فەرمان(self):
        دۆخ_نرخ = self.읽기()
        등록됨 = 등록목록(self.فەرمان(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if دۆخ_نرخ is not None and دۆخ_نرخ['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(دۆخ_نرخ, 등록됨, گەڕاندنەوە_دۆخ=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 جێبەجێکردن_فەرمان 중입니다. 재빌드·재시작하지 않습니다.')
                return self.نیشاندان_دۆخ()
            self.پشکنین_میدیا(دۆخ_نرخ, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_نرخ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.فەرمان(['VBoxManage', 'controlvm', دۆخ_نرخ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 کردنەوە 전에 기존 기록도 보관한다.
                    if دۆخ_نرخ.get('serial_log'):
                        원본 = self.گوزەر(دۆخ_نرخ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.گوزەر('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.فەرمان(['VBoxManage', 'startvm', دۆخ_نرخ['uuid'], '--type', self.ڕێگا_دۆخ])
                return self.نیشاندان_دۆخ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 گۆڕین_دۆخ 중입니다 ({}). 작업이 끝난 دواوە_نرخ 다시 실행하세요.'.format(현재))
        elif دۆخ_نرخ is not None and not دۆخ_نرخ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ناو in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_نرخ/جێبەجێکردن_فەرمان 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.فەرمان(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        میدیا_نرخ = 'media/kernel-' + 검사합(원본) + '.iso'
        جێمەبەست_نرخ = self.گوزەر(میدیا_نرخ)
        جێمەبەست_نرخ.parent.mkdir(exist_ok=True)
        if جێمەبەست_نرخ.exists():
            if 검사합(جێمەبەست_نرخ) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(جێمەبەست_نرخ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(جێمەبەست_نرخ.parent)) as فایل:
                shutil.copyfile(str(원본), فایل.name)
                os.link(فایل.name, str(جێمەبەست_نرخ))

        if دۆخ_نرخ is None:
            دۆخ_نرخ = {'version': 1, 'name': self.ناو, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_نرخ(دۆخ_نرخ)
        if msinfo32_exe is None:
            self.فەرمان(['VBoxManage', 'createvm', '--name', دۆخ_نرخ['name'], '--uuid', دۆخ_نرخ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.گوزەر('machines')), '--register'])
            self.فەرمان(['VBoxManage', 'setextradata', دۆخ_نرخ['uuid'], 'JKOROS/Owner', دۆخ_نرخ['owner']])
        # دروستکراو_سیستم 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(دۆخ_نرخ, 등록목록(self.فەرمان(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('دروستکراو_سیستم 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.پشکنین_میدیا(دۆخ_نرخ, msinfo32_exe)
        دۆخ_نرخ['iso'] = میدیا_نرخ
        if میدیا_نرخ not in دۆخ_نرخ['media']: دۆخ_نرخ['media'].append(میدیا_نرخ)
        دۆخ_نرخ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        تۆمار_نرخ = self.گوزەر(دۆخ_نرخ['serial_log'])
        تۆمار_نرخ.parent.mkdir(exist_ok=True)
        self.Store_نرخ(دۆخ_نرخ)
        self.فەرمان(['VBoxManage', 'modifyvm', دۆخ_نرخ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(تۆمار_نرخ)])
        제어기들 = [نرخ for ناو, نرخ in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', ناو)]
        if 'JKOROS IDE' not in 제어기들:
            self.فەرمان(['VBoxManage', 'storagectl', دۆخ_نرخ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.فەرمان(['VBoxManage', 'storageattach', دۆخ_نرخ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(جێمەبەست_نرخ)])
        دۆخ_نرخ['pending'] = False
        self.Store_نرخ(دۆخ_نرخ)
        self.فەرمان(['VBoxManage', 'startvm', دۆخ_نرخ['uuid'], '--type', self.ڕێگا_دۆخ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.نیشاندان_دۆخ()


def ڕادان():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox جێبەجێکردن_فەرمان 및 دۆخ_نرخ پرس_نرخ')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    جێبەجێکردن_فەرمان = بەرنامە_ئەندامی_ستاف(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(جێبەجێکردن_فەرمان.نیشاندان_دۆخ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. جێدەر 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ڕێپێدان_نرخ 변경은 하지 않습니다.')
    os.umask(0o077)
    جێبەجێکردن_فەرمان.گوزەر('lock').parent.mkdir(parents=True, exist_ok=True)
    with جێبەجێکردن_فەرمان.گوزەر('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox جێبەجێکردن_فەرمان 작업이 진행 중입니다.')
        print(json.dumps(جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ڕادان()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as هەڵە:
        print('VBOX هەڵە: ' + str(هەڵە), file=sys.stderr)
        sys.exit(1)
