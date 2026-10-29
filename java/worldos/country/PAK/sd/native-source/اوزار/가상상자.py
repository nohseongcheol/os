#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ائپ_ائپ_ڊرائر. 기존 VM/디스크/روڪيو_قدر 상태는 삭제하지 않는다."""
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


def تعميل_ڪرڻ_شيل_حڪم(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(قدر) for قدر in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    مواد_قدر = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('حڪم ناڪامي_قدر: ' + ' '.join(str(قدر) for قدر in 인수) + '\n' + مواد_قدر[-10000:])
    return مواد_قدر


def منسوب_ڪرڻ_قدر(مواد_قدر):
    결과 = {}
    for لڪير in مواد_قدر.splitlines():
        if '=' not in لڪير:
            continue
        نالو, قدر = لڪير.split('=', 1)
        if نالو.startswith('"'):
            نالو = json.loads(نالو)
        if قدر.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(قدر)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(قدر): قدر = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox منسوب_ڪرڻ_قدر وضع_قدر نقص: ' + لڪير)
        결과[نالو] = قدر
    return 결과


def 등록목록(مواد_قدر):
    결과 = {}
    for لڪير in مواد_قدر.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', لڪير)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(راههه):
    قدر = hashlib.sha256()
    with راههه.open('rb') as فائل:
        for ڪوائف in iter(lambda: فائل.read(1024 * 1024), b''): قدر.update(ڪوائف)
    return قدر.hexdigest()


class ائپ_ائپ_ڊرائر:
    def __init__(self, 뿌리, نالو, طريقو_موڊ='gui', حڪم=تعميل_ڪرڻ_شيل_حڪم):
        self.뿌리 = Path(뿌리).resolve()
        self.نالو, self.طريقو_موڊ, self.حڪم = نالو, طريقو_موڊ, حڪم
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', نالو) or نالو in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ڊجٽ_قدر·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if طريقو_موڊ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def راههه(self, همعصر_قدر):
        if Path(همعصر_قدر).is_absolute() or '..' in Path(همعصر_قدر).parts:
            raise 실행오류('잘못된 관리 راههه: ' + str(همعصر_قدر))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(همعصر_قدر).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('ڪنيڪٽ 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        راههه = self.راههه('state.json')
        if not راههه.exists(): return None
        حالت_قدر = json.loads(راههه.read_text(encoding='utf-8'))
        if حالت_قدر.get('version') != 1 or حالت_قدر.get('name') != self.نالو:
            raise 실행오류('관리 상태의 VM نالو/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for نالو in ('uuid', 'owner'):
            if str(uuid.UUID(حالت_قدر[نالو])) != حالت_قدر[نالو]: raise 실행오류('잘못된 VM سڃاڻپ_ڪندڙ_قدر')
        return حالت_قدر

    def روڪيو_قدر(self, حالت_قدر):
        منزل_مقصود_قدر = self.راههه('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as فائل:
            json.dump(حالت_قدر, فائل, ensure_ascii=False, indent=2)
            فائل.write('\n')
            임시 = فائل.name
        os.replace(임시, str(منزل_مقصود_قدر))

    def سسٽم_معلومات(self, حالت_قدر, 등록됨, بحال_ٿيڻ_حالت=False):
        if حالت_قدر['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        سسٽم_معلومات = منسوب_ڪرڻ_قدر(self.حڪم(['VBoxManage', 'showvminfo', حالت_قدر['uuid'], '--machinereadable']))
        위치 = Path(سسٽم_معلومات.get('CfgFile', '')).resolve()
        if self.راههه('machines').resolve() not in 위치.parents or سسٽم_معلومات.get('UUID') != حالت_قدر['uuid']:
            raise 실행오류('이 프로젝트의 VM سيٽنگون راههه/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.حڪم(['VBoxManage', 'getextradata', حالت_قدر['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + حالت_قدر['owner']:
            if بحال_ٿيڻ_حالت and حالت_قدر.get('pending') and 표식 == 'No value set!':
                self.حڪم(['VBoxManage', 'setextradata', حالت_قدر['uuid'], 'JKOROS/Owner', حالت_قدر['owner']])
            else:
                raise 실행오류('VM مالڪ_قدر 표식이 일치하지 않아 변경하지 않습니다.')
        return سسٽم_معلومات

    def پڙتال_ڪريو_ميڊيا(self, حالت_قدر, سسٽم_معلومات):
        제어기들 = [قدر for نالو, قدر in سسٽم_معلومات.items() if re.fullmatch(r'storagecontrollername\d+', نالو)]
        اجازت_ڏيو_قدر = [str(self.راههه(قدر)) for قدر in حالت_قدر.get('media', [])]
        for نالو, قدر in سسٽم_معلومات.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', نالو) for 제어기 in 제어기들):
                if قدر not in ('none', 'emptydrive') and قدر not in اجازت_ڏيو_قدر:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + قدر)

    def نمائش_ڪريو_حالت(self):
        حالت_قدر = self.읽기()
        if حالت_قدر is None: return {'name': self.نالو, 'state': 'not-created'}
        سسٽم_معلومات = self.سسٽم_معلومات(حالت_قدر, 등록목록(self.حڪم(['VBoxManage', 'list', 'vms'])))
        return {'name': سسٽم_معلومات.get('name', حالت_قدر['name']), 'uuid': حالت_قدر['uuid'], 'state': سسٽم_معلومات.get('VMState'),
                'iso': str(self.راههه(حالت_قدر['iso'])) if حالت_قدر.get('iso') else None,
                'serial_log': str(self.راههه(حالت_قدر['serial_log'])) if حالت_قدر.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def تعميل_ڪرڻ_حڪم(self):
        حالت_قدر = self.읽기()
        등록됨 = 등록목록(self.حڪم(['VBoxManage', 'list', 'vms']))
        سسٽم_معلومات = None
        if حالت_قدر is not None and حالت_قدر['uuid'] in 등록됨:
            سسٽم_معلومات = self.سسٽم_معلومات(حالت_قدر, 등록됨, بحال_ٿيڻ_حالت=True)
            현재 = سسٽم_معلومات.get('VMState')
            if 현재 == 'running':
                print('이미 تعميل_ڪرڻ_حڪم 중입니다. 재빌드·재시작하지 않습니다.')
                return self.نمائش_ڪريو_حالت()
            self.پڙتال_ڪريو_ميڊيا(حالت_قدر, سسٽم_معلومات)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 روڪيو_قدر 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.حڪم(['VBoxManage', 'controlvm', حالت_قدر['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ٺاھيو 전에 기존 기록도 보관한다.
                    if حالت_قدر.get('serial_log'):
                        원본 = self.راههه(حالت_قدر['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.راههه('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.حڪم(['VBoxManage', 'startvm', حالت_قدر['uuid'], '--type', self.طريقو_موڊ])
                return self.نمائش_ڪريو_حالت()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 سوئچ_موڊ 중입니다 ({}). 작업이 끝난 واپس_قدر 다시 실행하세요.'.format(현재))
        elif حالت_قدر is not None and not حالت_قدر.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.نالو in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # روڪيو_قدر/تعميل_ڪرڻ_حڪم 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.حڪم(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        ميڊيا_قدر = 'media/kernel-' + 검사합(원본) + '.iso'
        منزل_مقصود_قدر = self.راههه(ميڊيا_قدر)
        منزل_مقصود_قدر.parent.mkdir(exist_ok=True)
        if منزل_مقصود_قدر.exists():
            if 검사합(منزل_مقصود_قدر) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(منزل_مقصود_قدر))
        else:
            with tempfile.NamedTemporaryFile(dir=str(منزل_مقصود_قدر.parent)) as فائل:
                shutil.copyfile(str(원본), فائل.name)
                os.link(فائل.name, str(منزل_مقصود_قدر))

        if حالت_قدر is None:
            حالت_قدر = {'version': 1, 'name': self.نالو, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.روڪيو_قدر(حالت_قدر)
        if سسٽم_معلومات is None:
            self.حڪم(['VBoxManage', 'createvm', '--name', حالت_قدر['name'], '--uuid', حالت_قدر['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.راههه('machines')), '--register'])
            self.حڪم(['VBoxManage', 'setextradata', حالت_قدر['uuid'], 'JKOROS/Owner', حالت_قدر['owner']])
        # گڏ_ڪريو_سسٽم 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        سسٽم_معلومات = self.سسٽم_معلومات(حالت_قدر, 등록목록(self.حڪم(['VBoxManage', 'list', 'vms'])))
        if سسٽم_معلومات.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('گڏ_ڪريو_سسٽم 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.پڙتال_ڪريو_ميڊيا(حالت_قدر, سسٽم_معلومات)
        حالت_قدر['iso'] = ميڊيا_قدر
        if ميڊيا_قدر not in حالت_قدر['media']: حالت_قدر['media'].append(ميڊيا_قدر)
        حالت_قدر['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        لاگ_قدر = self.راههه(حالت_قدر['serial_log'])
        لاگ_قدر.parent.mkdir(exist_ok=True)
        self.روڪيو_قدر(حالت_قدر)
        self.حڪم(['VBoxManage', 'modifyvm', حالت_قدر['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(لاگ_قدر)])
        제어기들 = [قدر for نالو, قدر in سسٽم_معلومات.items() if re.fullmatch(r'storagecontrollername\d+', نالو)]
        if 'JKOROS IDE' not in 제어기들:
            self.حڪم(['VBoxManage', 'storagectl', حالت_قدر['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.حڪم(['VBoxManage', 'storageattach', حالت_قدر['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(منزل_مقصود_قدر)])
        حالت_قدر['pending'] = False
        self.روڪيو_قدر(حالت_قدر)
        self.حڪم(['VBoxManage', 'startvm', حالت_قدر['uuid'], '--type', self.طريقو_موڊ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.نمائش_ڪريو_حالت()


def هلائڻ():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox تعميل_ڪرڻ_حڪم 및 حالت_قدر سوال_قدر')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    تعميل_ڪرڻ_حڪم = ائپ_ائپ_ڊرائر(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(تعميل_ڪرڻ_حڪم.نمائش_ڪريو_حالت(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. مهمان 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/اجازت_قدر 변경은 하지 않습니다.')
    os.umask(0o077)
    تعميل_ڪرڻ_حڪم.راههه('lock').parent.mkdir(parents=True, exist_ok=True)
    with تعميل_ڪرڻ_حڪم.راههه('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox تعميل_ڪرڻ_حڪم 작업이 진행 중입니다.')
        print(json.dumps(تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: هلائڻ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as نقص:
        print('VBOX نقص: ' + str(نقص), file=sys.stderr)
        sys.exit(1)
