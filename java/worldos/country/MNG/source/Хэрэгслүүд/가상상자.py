#!/usr/bin/env python3
"""jkoros 전용 VirtualBox програм_гишүүн. 기존 VM/디스크/хадгалах_утга 상태는 삭제하지 않는다."""
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


def Гүйцэтгэх_бүрхүүл_команд(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(утга) for утга in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Агуулга_утга = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Тушаал гэмтэл_утга: ' + ' '.join(str(утга) for утга in 인수) + '\n' + Агуулга_утга[-10000:])
    return Агуулга_утга


def аттрибут_утга(Агуулга_утга):
    결과 = {}
    for Шугам in Агуулга_утга.splitlines():
        if '=' not in Шугам:
            continue
        Нэр, утга = Шугам.split('=', 1)
        if Нэр.startswith('"'):
            Нэр = json.loads(Нэр)
        if утга.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(утга)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(утга): утга = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox аттрибут_утга формат_утга Алдаа: ' + Шугам)
        결과[Нэр] = утга
    return 결과


def 등록목록(Агуулга_утга):
    결과 = {}
    for Шугам in Агуулга_утга.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Шугам)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(ЗАМ):
    утга = hashlib.sha256()
    with ЗАМ.open('rb') as Файл:
        for өгөгдөл in iter(lambda: Файл.read(1024 * 1024), b''): утга.update(өгөгдөл)
    return утга.hexdigest()


class програм_гишүүн:
    def __init__(self, 뿌리, Нэр, арга_горим='gui', Тушаал=Гүйцэтгэх_бүрхүүл_команд):
        self.뿌리 = Path(뿌리).resolve()
        self.Нэр, self.арга_горим, self.Тушаал = Нэр, арга_горим, Тушаал
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Нэр) or Нэр in ('.', '..'):
            raise 실행오류('VM 이름은 문자·тоо_утга·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if арга_горим not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ЗАМ(self, ижил_түвшин_утга):
        if Path(ижил_түвшин_утга).is_absolute() or '..' in Path(ижил_түвшин_утга).parts:
            raise 실행오류('잘못된 관리 ЗАМ: ' + str(ижил_түвшин_утга))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(ижил_түвшин_утга).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Холбох 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Унших(self):
        ЗАМ = self.ЗАМ('state.json')
        if not ЗАМ.exists(): return None
        төлөв_утга = json.loads(ЗАМ.read_text(encoding='utf-8'))
        if төлөв_утга.get('version') != 1 or төлөв_утга.get('name') != self.Нэр:
            raise 실행오류('관리 상태의 VM Нэр/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Нэр in ('uuid', 'owner'):
            if str(uuid.UUID(төлөв_утга[Нэр])) != төлөв_утга[Нэр]: raise 실행오류('잘못된 VM танигч_утга')
        return төлөв_утга

    def хадгалах_утга(self, төлөв_утга):
        товлосон_газар_утга = self.ЗАМ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Файл:
            json.dump(төлөв_утга, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
            임시 = Файл.name
        os.replace(임시, str(товлосон_газар_утга))

    def системийн_мэдээлэл(self, төлөв_утга, 등록됨, сэргээх_төлөв=False):
        if төлөв_утга['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        системийн_мэдээлэл = аттрибут_утга(self.Тушаал(['VBoxManage', 'showvminfo', төлөв_утга['uuid'], '--machinereadable']))
        위치 = Path(системийн_мэдээлэл.get('CfgFile', '')).resolve()
        if self.ЗАМ('machines').resolve() not in 위치.parents or системийн_мэдээлэл.get('UUID') != төлөв_утга['uuid']:
            raise 실행오류('이 프로젝트의 VM Тохиргоо ЗАМ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Тушаал(['VBoxManage', 'getextradata', төлөв_утга['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + төлөв_утга['owner']:
            if сэргээх_төлөв and төлөв_утга.get('pending') and 표식 == 'No value set!':
                self.Тушаал(['VBoxManage', 'setextradata', төлөв_утга['uuid'], 'JKOROS/Owner', төлөв_утга['owner']])
            else:
                raise 실행오류('VM эзэмшигч_утга 표식이 일치하지 않아 변경하지 않습니다.')
        return системийн_мэдээлэл

    def 매체검사(self, төлөв_утга, системийн_мэдээлэл):
        제어기들 = [утга for Нэр, утга in системийн_мэдээлэл.items() if re.fullmatch(r'storagecontrollername\d+', Нэр)]
        Зөвшөөрөх_утга = [str(self.ЗАМ(утга)) for утга in төлөв_утга.get('media', [])]
        for Нэр, утга in системийн_мэдээлэл.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Нэр) for 제어기 in 제어기들):
                if утга not in ('none', 'emptydrive') and утга not in Зөвшөөрөх_утга:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + утга)

    def үзүүлэх_төлөв(self):
        төлөв_утга = self.Унших()
        if төлөв_утга is None: return {'name': self.Нэр, 'state': 'not-created'}
        системийн_мэдээлэл = self.системийн_мэдээлэл(төлөв_утга, 등록목록(self.Тушаал(['VBoxManage', 'list', 'vms'])))
        return {'name': системийн_мэдээлэл.get('name', төлөв_утга['name']), 'uuid': төлөв_утга['uuid'], 'state': системийн_мэдээлэл.get('VMState'),
                'iso': str(self.ЗАМ(төлөв_утга['iso'])) if төлөв_утга.get('iso') else None,
                'serial_log': str(self.ЗАМ(төлөв_утга['serial_log'])) if төлөв_утга.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Гүйцэтгэх_команд(self):
        төлөв_утга = self.Унших()
        등록됨 = 등록목록(self.Тушаал(['VBoxManage', 'list', 'vms']))
        системийн_мэдээлэл = None
        if төлөв_утга is not None and төлөв_утга['uuid'] in 등록됨:
            системийн_мэдээлэл = self.системийн_мэдээлэл(төлөв_утга, 등록됨, сэргээх_төлөв=True)
            현재 = системийн_мэдээлэл.get('VMState')
            if 현재 == 'running':
                print('이미 Гүйцэтгэх_команд 중입니다. 재빌드·재시작하지 않습니다.')
                return self.үзүүлэх_төлөв()
            self.매체검사(төлөв_утга, системийн_мэдээлэл)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 хадгалах_утга 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Тушаал(['VBoxManage', 'controlvm', төлөв_утга['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Нээх 전에 기존 기록도 보관한다.
                    if төлөв_утга.get('serial_log'):
                        원본 = self.ЗАМ(төлөв_утга['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ЗАМ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Тушаал(['VBoxManage', 'startvm', төлөв_утга['uuid'], '--type', self.арга_горим])
                return self.үзүүлэх_төлөв()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 шилжих_горим 중입니다 ({}). 작업이 끝난 Буцах_утга 다시 실행하세요.'.format(현재))
        elif төлөв_утга is not None and not төлөв_утга.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Нэр in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # хадгалах_утга/Гүйцэтгэх_команд 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Тушаал(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        товлосон_газар_утга = self.ЗАМ(매체)
        товлосон_газар_утга.parent.mkdir(exist_ok=True)
        if товлосон_газар_утга.exists():
            if 검사합(товлосон_газар_утга) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(товлосон_газар_утга))
        else:
            with tempfile.NamedTemporaryFile(dir=str(товлосон_газар_утга.parent)) as Файл:
                shutil.copyfile(str(원본), Файл.name)
                os.link(Файл.name, str(товлосон_газар_утга))

        if төлөв_утга is None:
            төлөв_утга = {'version': 1, 'name': self.Нэр, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.хадгалах_утга(төлөв_утга)
        if системийн_мэдээлэл is None:
            self.Тушаал(['VBoxManage', 'createvm', '--name', төлөв_утга['name'], '--uuid', төлөв_утга['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ЗАМ('machines')), '--register'])
            self.Тушаал(['VBoxManage', 'setextradata', төлөв_утга['uuid'], 'JKOROS/Owner', төлөв_утга['owner']])
        # хувилбар_систем 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        системийн_мэдээлэл = self.системийн_мэдээлэл(төлөв_утга, 등록목록(self.Тушаал(['VBoxManage', 'list', 'vms'])))
        if системийн_мэдээлэл.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('хувилбар_систем 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(төлөв_утга, системийн_мэдээлэл)
        төлөв_утга['iso'] = 매체
        if 매체 not in төлөв_утга['media']: төлөв_утга['media'].append(매체)
        төлөв_утга['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        бичих_утга_e0918eb0 = self.ЗАМ(төлөв_утга['serial_log'])
        бичих_утга_e0918eb0.parent.mkdir(exist_ok=True)
        self.хадгалах_утга(төлөв_утга)
        self.Тушаал(['VBoxManage', 'modifyvm', төлөв_утга['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(бичих_утга_e0918eb0)])
        제어기들 = [утга for Нэр, утга in системийн_мэдээлэл.items() if re.fullmatch(r'storagecontrollername\d+', Нэр)]
        if 'JKOROS IDE' not in 제어기들:
            self.Тушаал(['VBoxManage', 'storagectl', төлөв_утга['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Тушаал(['VBoxManage', 'storageattach', төлөв_утга['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(товлосон_газар_утга)])
        төлөв_утга['pending'] = False
        self.хадгалах_утга(төлөв_утга)
        self.Тушаал(['VBoxManage', 'startvm', төлөв_утга['uuid'], '--type', self.арга_горим])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.үзүүлэх_төлөв()


def Ажиллуулах():
    задлан_ялгал_хийх_утга = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Гүйцэтгэх_команд 및 төлөв_утга асуулга_утга')
    задлан_ялгал_хийх_утга.add_argument('action', choices=['run', 'status'])
    인자 = задлан_ялгал_хийх_утга.parse_args()
    Гүйцэтгэх_команд = програм_гишүүн(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(Гүйцэтгэх_команд.үзүүлэх_төлөв(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. хост 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/зөвшөөрөл_утга 변경은 하지 않습니다.')
    os.umask(0o077)
    Гүйцэтгэх_команд.ЗАМ('lock').parent.mkdir(parents=True, exist_ok=True)
    with Гүйцэтгэх_команд.ЗАМ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Гүйцэтгэх_команд 작업이 진행 중입니다.')
        print(json.dumps(Гүйцэтгэх_команд.Гүйцэтгэх_команд(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Ажиллуулах()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Алдаа:
        print('VBOX Алдаа: ' + str(Алдаа), file=sys.stderr)
        sys.exit(1)
