#!/usr/bin/env python3
"""jkoros 전용 VirtualBox برنامه_راه_انداز. 기존 VM/디스크/ذخیره_مقدار 상태는 삭제하지 않는다."""
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


def اجرا_واسط_فرمان(نشانوندها):
    환경 = dict(os.environ, LC_ALL='C')
    سنجش = subprocess.run([str(مقدار) for مقدار in نشانوندها], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    محتوا_مقدار = سنجش.stdout.decode('utf-8', 'replace')
    if سنجش.returncode:
        raise 실행오류('فرمان عدم_موفقیت_مقدار: ' + ' '.join(str(مقدار) for مقدار in نشانوندها) + '\n' + محتوا_مقدار[-10000:])
    return محتوا_مقدار


def مشخصه_مقدار(محتوا_مقدار):
    سنجش = {}
    for خط in محتوا_مقدار.splitlines():
        if '=' not in خط:
            continue
        نام, مقدار = خط.split('=', 1)
        if نام.startswith('"'):
            نام = json.loads(نام)
        if مقدار.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(مقدار)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(مقدار): مقدار = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox مشخصه_مقدار قالب_مقدار خطا: ' + خط)
        سنجش[نام] = مقدار
    return سنجش


def 등록목록(محتوا_مقدار):
    سنجش = {}
    for خط in محتوا_مقدار.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', خط)
        if 일치: سنجش[일치.group(2).lower()] = 일치.group(1)
    return سنجش


def مجموع_مقابله_ای(مسیر):
    مقدار = hashlib.sha256()
    with مسیر.open('rb') as پرونده:
        for داده_ها in iter(lambda: پرونده.read(1024 * 1024), b''): مقدار.update(داده_ها)
    return مقدار.hexdigest()


class برنامه_راه_انداز:
    def __init__(self, جذر_مقدار, نام, روش_حالت='gui', فرمان=اجرا_واسط_فرمان):
        self.جذر_مقدار = Path(جذر_مقدار).resolve()
        self.نام, self.روش_حالت, self.فرمان = نام, روش_حالت, فرمان
        self.보관 = self.جذر_مقدار / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', نام) or نام in ('.', '..'):
            raise 실행오류('VM 이름은 문자·رقم_مقدار·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if روش_حالت not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def مسیر(self, مشابه_مقدار):
        if Path(مشابه_مقدار).is_absolute() or '..' in Path(مشابه_مقدار).parts:
            raise 실행오류('잘못된 관리 مسیر: ' + str(مشابه_مقدار))
        سنجش = self.보관
        for 부분 in ['.vbox'] + list(Path(مشابه_مقدار).parts):
            if 부분 == '.vbox': سنجش = self.보관
            else: سنجش = سنجش / 부분
            if سنجش.is_symlink(): raise 실행오류('اتصال 경로는 사용하지 않습니다: ' + str(سنجش))
        return سنجش

    def خواندن(self):
        مسیر = self.مسیر('state.json')
        if not مسیر.exists(): return None
        وضعیت_مقدار = json.loads(مسیر.read_text(encoding='utf-8'))
        if وضعیت_مقدار.get('version') != 1 or وضعیت_مقدار.get('name') != self.نام:
            raise 실행오류('관리 상태의 VM نام/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for نام in ('uuid', 'owner'):
            if str(uuid.UUID(وضعیت_مقدار[نام])) != وضعیت_مقدار[نام]: raise 실행오류('잘못된 VM شناسه_مقدار')
        return وضعیت_مقدار

    def ذخیره_مقدار(self, وضعیت_مقدار):
        مقصد_مقدار = self.مسیر('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as پرونده:
            json.dump(وضعیت_مقدار, پرونده, ensure_ascii=False, indent=2)
            پرونده.write('\n')
            임시 = پرونده.name
        os.replace(임시, str(مقصد_مقدار))

    def اطلاعات_سیستم(self, وضعیت_مقدار, 등록됨, بازیابی_وضعیت=False):
        if وضعیت_مقدار['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        اطلاعات_سیستم = مشخصه_مقدار(self.فرمان(['VBoxManage', 'showvminfo', وضعیت_مقدار['uuid'], '--machinereadable']))
        مرتب_کردن = Path(اطلاعات_سیستم.get('CfgFile', '')).resolve()
        if self.مسیر('machines').resolve() not in مرتب_کردن.parents or اطلاعات_سیستم.get('UUID') != وضعیت_مقدار['uuid']:
            raise 실행오류('이 프로젝트의 VM تنظیمات مسیر/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.فرمان(['VBoxManage', 'getextradata', وضعیت_مقدار['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + وضعیت_مقدار['owner']:
            if بازیابی_وضعیت and وضعیت_مقدار.get('pending') and 표식 == 'No value set!':
                self.فرمان(['VBoxManage', 'setextradata', وضعیت_مقدار['uuid'], 'JKOROS/Owner', وضعیت_مقدار['owner']])
            else:
                raise 실행오류('VM مالک_مقدار 표식이 일치하지 않아 변경하지 않습니다.')
        return اطلاعات_سیستم

    def 매체검사(self, وضعیت_مقدار, اطلاعات_سیستم):
        제어기들 = [مقدار for نام, مقدار in اطلاعات_سیستم.items() if re.fullmatch(r'storagecontrollername\d+', نام)]
        اجازه_مقدار = [str(self.مسیر(مقدار)) for مقدار in وضعیت_مقدار.get('media', [])]
        for نام, مقدار in اطلاعات_سیستم.items():
            if any(re.fullmatch(re.escape(کنترلگر) + r'-\d+-\d+', نام) for کنترلگر in 제어기들):
                if مقدار not in ('none', 'emptydrive') and مقدار not in اجازه_مقدار:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + مقدار)

    def نمایش_وضعیت(self):
        وضعیت_مقدار = self.خواندن()
        if وضعیت_مقدار is None: return {'name': self.نام, 'state': 'not-created'}
        اطلاعات_سیستم = self.اطلاعات_سیستم(وضعیت_مقدار, 등록목록(self.فرمان(['VBoxManage', 'list', 'vms'])))
        return {'name': اطلاعات_سیستم.get('name', وضعیت_مقدار['name']), 'uuid': وضعیت_مقدار['uuid'], 'state': اطلاعات_سیستم.get('VMState'),
                'iso': str(self.مسیر(وضعیت_مقدار['iso'])) if وضعیت_مقدار.get('iso') else None,
                'serial_log': str(self.مسیر(وضعیت_مقدار['serial_log'])) if وضعیت_مقدار.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def اجرا_فرمان(self):
        وضعیت_مقدار = self.خواندن()
        등록됨 = 등록목록(self.فرمان(['VBoxManage', 'list', 'vms']))
        اطلاعات_سیستم = None
        if وضعیت_مقدار is not None and وضعیت_مقدار['uuid'] in 등록됨:
            اطلاعات_سیستم = self.اطلاعات_سیستم(وضعیت_مقدار, 등록됨, بازیابی_وضعیت=True)
            현재 = اطلاعات_سیستم.get('VMState')
            if 현재 == 'running':
                print('이미 اجرا_فرمان 중입니다. 재빌드·재시작하지 않습니다.')
                return self.نمایش_وضعیت()
            self.매체검사(وضعیت_مقدار, اطلاعات_سیستم)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ذخیره_مقدار 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.فرمان(['VBoxManage', 'controlvm', وضعیت_مقدار['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 باز_کردن 전에 기존 기록도 보관한다.
                    if وضعیت_مقدار.get('serial_log'):
                        원본 = self.مسیر(وضعیت_مقدار['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.مسیر('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.فرمان(['VBoxManage', 'startvm', وضعیت_مقدار['uuid'], '--type', self.روش_حالت])
                return self.نمایش_وضعیت()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 جابجایی_حالت 중입니다 ({}). 작업이 끝난 برگشت_مقدار 다시 실행하세요.'.format(현재))
        elif وضعیت_مقدار is not None and not وضعیت_مقدار.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.نام in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ذخیره_مقدار/اجرا_فرمان 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.فرمان(['make', '-C', str(self.جذر_مقدار / 'os'), 'iso']), end='')
        원본 = self.جذر_مقدار / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + مجموع_مقابله_ای(원본) + '.iso'
        مقصد_مقدار = self.مسیر(매체)
        مقصد_مقدار.parent.mkdir(exist_ok=True)
        if مقصد_مقدار.exists():
            if مجموع_مقابله_ای(مقصد_مقدار) != مجموع_مقابله_ای(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(مقصد_مقدار))
        else:
            with tempfile.NamedTemporaryFile(dir=str(مقصد_مقدار.parent)) as پرونده:
                shutil.copyfile(str(원본), پرونده.name)
                os.link(پرونده.name, str(مقصد_مقدار))

        if وضعیت_مقدار is None:
            وضعیت_مقدار = {'version': 1, 'name': self.نام, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ذخیره_مقدار(وضعیت_مقدار)
        if اطلاعات_سیستم is None:
            self.فرمان(['VBoxManage', 'createvm', '--name', وضعیت_مقدار['name'], '--uuid', وضعیت_مقدار['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.مسیر('machines')), '--register'])
            self.فرمان(['VBoxManage', 'setextradata', وضعیت_مقدار['uuid'], 'JKOROS/Owner', وضعیت_مقدار['owner']])
        # ساخت_سیستم 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        اطلاعات_سیستم = self.اطلاعات_سیستم(وضعیت_مقدار, 등록목록(self.فرمان(['VBoxManage', 'list', 'vms'])))
        if اطلاعات_سیستم.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ساخت_سیستم 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(وضعیت_مقدار, اطلاعات_سیستم)
        وضعیت_مقدار['iso'] = 매체
        if 매체 not in وضعیت_مقدار['media']: وضعیت_مقدار['media'].append(매체)
        وضعیت_مقدار['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        واقعه_نگار_مقدار = self.مسیر(وضعیت_مقدار['serial_log'])
        واقعه_نگار_مقدار.parent.mkdir(exist_ok=True)
        self.ذخیره_مقدار(وضعیت_مقدار)
        self.فرمان(['VBoxManage', 'modifyvm', وضعیت_مقدار['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(واقعه_نگار_مقدار)])
        제어기들 = [مقدار for نام, مقدار in اطلاعات_سیستم.items() if re.fullmatch(r'storagecontrollername\d+', نام)]
        if 'JKOROS IDE' not in 제어기들:
            self.فرمان(['VBoxManage', 'storagectl', وضعیت_مقدار['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.فرمان(['VBoxManage', 'storageattach', وضعیت_مقدار['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(مقصد_مقدار)])
        وضعیت_مقدار['pending'] = False
        self.ذخیره_مقدار(وضعیت_مقدار)
        self.فرمان(['VBoxManage', 'startvm', وضعیت_مقدار['uuid'], '--type', self.روش_حالت])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.نمایش_وضعیت()


def اجرا_2():
    تفسیر_مقدار = argparse.ArgumentParser(description='jkoros 전용 VirtualBox اجرا_فرمان 및 وضعیت_مقدار جستار_مقدار')
    تفسیر_مقدار.add_argument('action', choices=['run', 'status'])
    پارامتر_آرگومان = تفسیر_مقدار.parse_args()
    اجرا_فرمان = برنامه_راه_انداز(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if پارامتر_آرگومان.action == 'status':
        print(json.dumps(اجرا_فرمان.نمایش_وضعیت(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. میزبان 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/مجوز_مقدار 변경은 하지 않습니다.')
    os.umask(0o077)
    اجرا_فرمان.مسیر('lock').parent.mkdir(parents=True, exist_ok=True)
    with اجرا_فرمان.مسیر('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox اجرا_فرمان 작업이 진행 중입니다.')
        print(json.dumps(اجرا_فرمان.اجرا_فرمان(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: اجرا_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as خطا:
        print('VBOX خطا: ' + str(خطا), file=sys.stderr)
        sys.exit(1)
