#!/usr/bin/env python3
"""jkoros 전용 VirtualBox நிரல்_துவக்குநர். 기존 VM/디스크/சேகரி_மதிப்பு 상태는 삭제하지 않는다."""
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


def இயக்கு_கூடு_கட்டளை(செயலுருபுகள்):
    환경 = dict(os.environ, LC_ALL='C')
    அளவிடக்கூடியது = subprocess.run([str(மதிப்பு) for மதிப்பு in செயலுருபுகள்], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    உள்ளடக்கம்_மதிப்பு = அளவிடக்கூடியது.stdout.decode('utf-8', 'replace')
    if அளவிடக்கூடியது.returncode:
        raise 실행오류('கட்டளை செயலிழப்பு_மதிப்பு: ' + ' '.join(str(மதிப்பு) for மதிப்பு in செயலுருபுகள்) + '\n' + உள்ளடக்கம்_மதிப்பு[-10000:])
    return உள்ளடக்கம்_மதிப்பு


def பண்புக்கூறு_மதிப்பு(உள்ளடக்கம்_மதிப்பு):
    அளவிடக்கூடியது = {}
    for உள்ளீட்டு_வரி in உள்ளடக்கம்_மதிப்பு.splitlines():
        if '=' not in உள்ளீட்டு_வரி:
            continue
        பெயர், மதிப்பு = உள்ளீட்டு_வரி.split('=', 1)
        if பெயர்.startswith('"'):
            பெயர் = json.loads(பெயர்)
        if மதிப்பு.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(மதிப்பு)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(மதிப்பு): மதிப்பு = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox பண்புக்கூறு_மதிப்பு வடிவமை_மதிப்பு பிழை: ' + உள்ளீட்டு_வரி)
        அளவிடக்கூடியது[பெயர்] = மதிப்பு
    return அளவிடக்கூடியது


def 등록목록(உள்ளடக்கம்_மதிப்பு):
    அளவிடக்கூடியது = {}
    for உள்ளீட்டு_வரி in உள்ளடக்கம்_மதிப்பு.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', உள்ளீட்டு_வரி)
        if 일치: அளவிடக்கூடியது[일치.group(2).lower()] = 일치.group(1)
    return அளவிடக்கூடியது


def சொதனைக்_கணக்கு(பாதை_2):
    மதிப்பு = hashlib.sha256()
    with பாதை_2.open('rb') as கோப்பின்_பெயர்:
        for தரவு in iter(lambda: கோப்பின்_பெயர்.read(1024 * 1024), b''): மதிப்பு.update(தரவு)
    return மதிப்பு.hexdigest()


class நிரல்_துவக்குநர்:
    def __init__(self, மூலம்_மதிப்பு, பெயர், முறை_பயன்முறை='gui', கட்டளை=இயக்கு_கூடு_கட்டளை):
        self.மூலம்_மதிப்பு = Path(மூலம்_மதிப்பு).resolve()
        self.பெயர், self.முறை_பயன்முறை, self.கட்டளை = பெயர், முறை_பயன்முறை, கட்டளை
        self.보관 = self.மூலம்_மதிப்பு / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', பெயர்) or பெயர் in ('.', '..'):
            raise 실행오류('VM 이름은 문자·இலக்கம்_மதிப்பு·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if முறை_பயன்முறை not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def பாதை_2(self, பியர்_மதிப்பு):
        if Path(பியர்_மதிப்பு).is_absolute() or '..' in Path(பியர்_மதிப்பு).parts:
            raise 실행오류('잘못된 관리 பாதை_2: ' + str(பியர்_மதிப்பு))
        அளவிடக்கூடியது = self.보관
        for 부분 in ['.vbox'] + list(Path(பியர்_மதிப்பு).parts):
            if 부분 == '.vbox': அளவிடக்கூடியது = self.보관
            else: அளவிடக்கூடியது = அளவிடக்கூடியது / 부분
            if அளவிடக்கூடியது.is_symlink(): raise 실행오류('இணைக்க 경로는 사용하지 않습니다: ' + str(அளவிடக்கூடியது))
        return அளவிடக்கூடியது

    def படி(self):
        பாதை_2 = self.பாதை_2('state.json')
        if not பாதை_2.exists(): return None
        நிலை_மதிப்பு_e10195a1 = json.loads(பாதை_2.read_text(encoding='utf-8'))
        if நிலை_மதிப்பு_e10195a1.get('version') != 1 or நிலை_மதிப்பு_e10195a1.get('name') != self.பெயர்:
            raise 실행오류('관리 상태의 VM பெயர்/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for பெயர் in ('uuid', 'owner'):
            if str(uuid.UUID(நிலை_மதிப்பு_e10195a1[பெயர்])) != நிலை_மதிப்பு_e10195a1[பெயர்]: raise 실행오류('잘못된 VM அடையாளங்காட்டி_மதிப்பு')
        return நிலை_மதிப்பு_e10195a1

    def சேகரி_மதிப்பு(self, நிலை_மதிப்பு_e10195a1):
        இலக்கு_மதிப்பு = self.பாதை_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as கோப்பின்_பெயர்:
            json.dump(நிலை_மதிப்பு_e10195a1, கோப்பின்_பெயர், ensure_ascii=False, indent=2)
            கோப்பின்_பெயர்.write('\n')
            임시 = கோப்பின்_பெயர்.name
        os.replace(임시, str(இலக்கு_மதிப்பு))

    def கணினித்_தகவல்(self, நிலை_மதிப்பு_e10195a1, 등록됨, மீட்டெடு_நிலை=False):
        if நிலை_மதிப்பு_e10195a1['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        கணினித்_தகவல் = பண்புக்கூறு_மதிப்பு(self.கட்டளை(['VBoxManage', 'showvminfo', நிலை_மதிப்பு_e10195a1['uuid'], '--machinereadable']))
        இடம் = Path(கணினித்_தகவல்.get('CfgFile', '')).resolve()
        if self.பாதை_2('machines').resolve() not in இடம்.parents or கணினித்_தகவல்.get('UUID') != நிலை_மதிப்பு_e10195a1['uuid']:
            raise 실행오류('이 프로젝트의 VM அமைப்புகள் பாதை_2/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.கட்டளை(['VBoxManage', 'getextradata', நிலை_மதிப்பு_e10195a1['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + நிலை_மதிப்பு_e10195a1['owner']:
            if மீட்டெடு_நிலை and நிலை_மதிப்பு_e10195a1.get('pending') and 표식 == 'No value set!':
                self.கட்டளை(['VBoxManage', 'setextradata', நிலை_மதிப்பு_e10195a1['uuid'], 'JKOROS/Owner', நிலை_மதிப்பு_e10195a1['owner']])
            else:
                raise 실행오류('VM உரிமையாளர்_மதிப்பு 표식이 일치하지 않아 변경하지 않습니다.')
        return கணினித்_தகவல்

    def 매체검사(self, நிலை_மதிப்பு_e10195a1, கணினித்_தகவல்):
        제어기들 = [மதிப்பு for பெயர், மதிப்பு in கணினித்_தகவல்.items() if re.fullmatch(r'storagecontrollername\d+', பெயர்)]
        அனுமதி_மதிப்பு_688200c4 = [str(self.பாதை_2(மதிப்பு)) for மதிப்பு in நிலை_மதிப்பு_e10195a1.get('media', [])]
        for பெயர், மதிப்பு in கணினித்_தகவல்.items():
            if any(re.fullmatch(re.escape(கண்ட்ரோலர்) + r'-\d+-\d+', பெயர்) for கண்ட்ரோலர் in 제어기들):
                if மதிப்பு not in ('none', 'emptydrive') and மதிப்பு not in அனுமதி_மதிப்பு_688200c4:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + மதிப்பு)

    def காட்சி_நிலை(self):
        நிலை_மதிப்பு_e10195a1 = self.படி()
        if நிலை_மதிப்பு_e10195a1 is None: return {'name': self.பெயர், 'state': 'not-created'}
        கணினித்_தகவல் = self.கணினித்_தகவல்(நிலை_மதிப்பு_e10195a1, 등록목록(self.கட்டளை(['VBoxManage', 'list', 'vms'])))
        return {'name': கணினித்_தகவல்.get('name', நிலை_மதிப்பு_e10195a1['name']), 'uuid': நிலை_மதிப்பு_e10195a1['uuid'], 'state': கணினித்_தகவல்.get('VMState'),
                'iso': str(self.பாதை_2(நிலை_மதிப்பு_e10195a1['iso'])) if நிலை_மதிப்பு_e10195a1.get('iso') else None,
                'serial_log': str(self.பாதை_2(நிலை_மதிப்பு_e10195a1['serial_log'])) if நிலை_மதிப்பு_e10195a1.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def இயக்கு_கட்டளை(self):
        நிலை_மதிப்பு_e10195a1 = self.படி()
        등록됨 = 등록목록(self.கட்டளை(['VBoxManage', 'list', 'vms']))
        கணினித்_தகவல் = None
        if நிலை_மதிப்பு_e10195a1 is not None and நிலை_மதிப்பு_e10195a1['uuid'] in 등록됨:
            கணினித்_தகவல் = self.கணினித்_தகவல்(நிலை_மதிப்பு_e10195a1, 등록됨, மீட்டெடு_நிலை=True)
            현재 = கணினித்_தகவல்.get('VMState')
            if 현재 == 'running':
                print('이미 இயக்கு_கட்டளை 중입니다. 재빌드·재시작하지 않습니다.')
                return self.காட்சி_நிலை()
            self.매체검사(நிலை_மதிப்பு_e10195a1, கணினித்_தகவல்)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 சேகரி_மதிப்பு 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.கட்டளை(['VBoxManage', 'controlvm', நிலை_மதிப்பு_e10195a1['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 திற 전에 기존 기록도 보관한다.
                    if நிலை_மதிப்பு_e10195a1.get('serial_log'):
                        원본 = self.பாதை_2(நிலை_மதிப்பு_e10195a1['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.பாதை_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.கட்டளை(['VBoxManage', 'startvm', நிலை_மதிப்பு_e10195a1['uuid'], '--type', self.முறை_பயன்முறை])
                return self.காட்சி_நிலை()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 சுவிட்ச்_பயன்முறை 중입니다 ({}). 작업이 끝난 பின்_மதிப்பு 다시 실행하세요.'.format(현재))
        elif நிலை_மதிப்பு_e10195a1 is not None and not நிலை_மதிப்பு_e10195a1.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.பெயர் in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # சேகரி_மதிப்பு/இயக்கு_கட்டளை 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.கட்டளை(['make', '-C', str(self.மூலம்_மதிப்பு / 'os'), 'iso']), end='')
        원본 = self.மூலம்_மதிப்பு / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + சொதனைக்_கணக்கு(원본) + '.iso'
        இலக்கு_மதிப்பு = self.பாதை_2(매체)
        இலக்கு_மதிப்பு.parent.mkdir(exist_ok=True)
        if இலக்கு_மதிப்பு.exists():
            if சொதனைக்_கணக்கு(இலக்கு_மதிப்பு) != சொதனைக்_கணக்கு(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(இலக்கு_மதிப்பு))
        else:
            with tempfile.NamedTemporaryFile(dir=str(இலக்கு_மதிப்பு.parent)) as கோப்பின்_பெயர்:
                shutil.copyfile(str(원본), கோப்பின்_பெயர்.name)
                os.link(கோப்பின்_பெயர்.name, str(இலக்கு_மதிப்பு))

        if நிலை_மதிப்பு_e10195a1 is None:
            நிலை_மதிப்பு_e10195a1 = {'version': 1, 'name': self.பெயர், 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.சேகரி_மதிப்பு(நிலை_மதிப்பு_e10195a1)
        if கணினித்_தகவல் is None:
            self.கட்டளை(['VBoxManage', 'createvm', '--name', நிலை_மதிப்பு_e10195a1['name'], '--uuid', நிலை_மதிப்பு_e10195a1['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.பாதை_2('machines')), '--register'])
            self.கட்டளை(['VBoxManage', 'setextradata', நிலை_மதிப்பு_e10195a1['uuid'], 'JKOROS/Owner', நிலை_மதிப்பு_e10195a1['owner']])
        # தொகு_முறைமை 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        கணினித்_தகவல் = self.கணினித்_தகவல்(நிலை_மதிப்பு_e10195a1, 등록목록(self.கட்டளை(['VBoxManage', 'list', 'vms'])))
        if கணினித்_தகவல்.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('தொகு_முறைமை 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(நிலை_மதிப்பு_e10195a1, கணினித்_தகவல்)
        நிலை_மதிப்பு_e10195a1['iso'] = 매체
        if 매체 not in நிலை_மதிப்பு_e10195a1['media']: நிலை_மதிப்பு_e10195a1['media'].append(매체)
        நிலை_மதிப்பு_e10195a1['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        பதிவு_மதிப்பு = self.பாதை_2(நிலை_மதிப்பு_e10195a1['serial_log'])
        பதிவு_மதிப்பு.parent.mkdir(exist_ok=True)
        self.சேகரி_மதிப்பு(நிலை_மதிப்பு_e10195a1)
        self.கட்டளை(['VBoxManage', 'modifyvm', நிலை_மதிப்பு_e10195a1['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(பதிவு_மதிப்பு)])
        제어기들 = [மதிப்பு for பெயர், மதிப்பு in கணினித்_தகவல்.items() if re.fullmatch(r'storagecontrollername\d+', பெயர்)]
        if 'JKOROS IDE' not in 제어기들:
            self.கட்டளை(['VBoxManage', 'storagectl', நிலை_மதிப்பு_e10195a1['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.கட்டளை(['VBoxManage', 'storageattach', நிலை_மதிப்பு_e10195a1['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(இலக்கு_மதிப்பு)])
        நிலை_மதிப்பு_e10195a1['pending'] = False
        self.சேகரி_மதிப்பு(நிலை_மதிப்பு_e10195a1)
        self.கட்டளை(['VBoxManage', 'startvm', நிலை_மதிப்பு_e10195a1['uuid'], '--type', self.முறை_பயன்முறை])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.காட்சி_நிலை()


def செயல்படுத்துக():
    அலகிடு_மதிப்பு = argparse.ArgumentParser(description='jkoros 전용 VirtualBox இயக்கு_கட்டளை 및 நிலை_மதிப்பு_e10195a1 வினவல்_மதிப்பு')
    அலகிடு_மதிப்பு.add_argument('action', choices=['run', 'status'])
    அளவுரு_மதிப்புரு = அலகிடு_மதிப்பு.parse_args()
    இயக்கு_கட்டளை = நிரல்_துவக்குநர்(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if அளவுரு_மதிப்புரு.action == 'status':
        print(json.dumps(இயக்கு_கட்டளை.காட்சி_நிலை(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ஓம்பு 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/அனுமதி_மதிப்பு 변경은 하지 않습니다.')
    os.umask(0o077)
    இயக்கு_கட்டளை.பாதை_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with இயக்கு_கட்டளை.பாதை_2('lock').open('a') as பூட்டு_மதிப்பு:
        try: fcntl.flock(பூட்டு_மதிப்பு, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox இயக்கு_கட்டளை 작업이 진행 중입니다.')
        print(json.dumps(இயக்கு_கட்டளை.இயக்கு_கட்டளை(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: செயல்படுத்துக()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as பிழை:
        print('VBOX பிழை: ' + str(பிழை), file=sys.stderr)
        sys.exit(1)
