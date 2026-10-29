#!/usr/bin/env python3
"""jkoros 전용 VirtualBox àtòjọ_ètò_aṣàfilọ́lẹ̀. 기존 VM/디스크/Store_iye 상태는 삭제하지 않는다."""
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


def ṣiṣẹ́_ṣẹ́ẹ̀lì_àṣẹ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(iye) for iye in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Àkóónú_iye = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Àṣẹ ìkùnà_iye: ' + ' '.join(str(iye) for iye in 인수) + '\n' + Àkóónú_iye[-10000:])
    return Àkóónú_iye


def àwòmọ́_iye(Àkóónú_iye):
    결과 = {}
    for ìlà in Àkóónú_iye.splitlines():
        if '=' not in ìlà:
            continue
        Orúkọ, iye = ìlà.split('=', 1)
        if Orúkọ.startswith('"'):
            Orúkọ = json.loads(Orúkọ)
        if iye.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(iye)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(iye): iye = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox àwòmọ́_iye ìgúnrégé_iye àṣìṣe: ' + ìlà)
        결과[Orúkọ] = iye
    return 결과


def 등록목록(Àkóónú_iye):
    결과 = {}
    for ìlà in Àkóónú_iye.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ìlà)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(ọ̀nà):
    iye = hashlib.sha256()
    with ọ̀nà.open('rb') as Fáìlì:
        for détà in iter(lambda: Fáìlì.read(1024 * 1024), b''): iye.update(détà)
    return iye.hexdigest()


class àtòjọ_ètò_aṣàfilọ́lẹ̀:
    def __init__(self, 뿌리, Orúkọ, ìlànà_móòdù='gui', Àṣẹ=ṣiṣẹ́_ṣẹ́ẹ̀lì_àṣẹ):
        self.뿌리 = Path(뿌리).resolve()
        self.Orúkọ, self.ìlànà_móòdù, self.Àṣẹ = Orúkọ, ìlànà_móòdù, Àṣẹ
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Orúkọ) or Orúkọ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·díjììtì_iye·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ìlànà_móòdù not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ọ̀nà(self, ọ̀gbà_iye):
        if Path(ọ̀gbà_iye).is_absolute() or '..' in Path(ọ̀gbà_iye).parts:
            raise 실행오류('잘못된 관리 ọ̀nà: ' + str(ọ̀gbà_iye))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(ọ̀gbà_iye).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Darapọ̀ 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Kàá(self):
        ọ̀nà = self.ọ̀nà('state.json')
        if not ọ̀nà.exists(): return None
        ipò_iye = json.loads(ọ̀nà.read_text(encoding='utf-8'))
        if ipò_iye.get('version') != 1 or ipò_iye.get('name') != self.Orúkọ:
            raise 실행오류('관리 상태의 VM Orúkọ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Orúkọ in ('uuid', 'owner'):
            if str(uuid.UUID(ipò_iye[Orúkọ])) != ipò_iye[Orúkọ]: raise 실행오류('잘못된 VM Àfidámọ̀_iye')
        return ipò_iye

    def Store_iye(self, ipò_iye):
        èbúté_iye = self.ọ̀nà('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fáìlì:
            json.dump(ipò_iye, Fáìlì, ensure_ascii=False, indent=2)
            Fáìlì.write('\n')
            임시 = Fáìlì.name
        os.replace(임시, str(èbúté_iye))

    def msinfo32_exe(self, ipò_iye, 등록됨, ràpadà_ipò=False):
        if ipò_iye['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = àwòmọ́_iye(self.Àṣẹ(['VBoxManage', 'showvminfo', ipò_iye['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.ọ̀nà('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != ipò_iye['uuid']:
            raise 실행오류('이 프로젝트의 VM Àwọn_ààtò ọ̀nà/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Àṣẹ(['VBoxManage', 'getextradata', ipò_iye['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ipò_iye['owner']:
            if ràpadà_ipò and ipò_iye.get('pending') and 표식 == 'No value set!':
                self.Àṣẹ(['VBoxManage', 'setextradata', ipò_iye['uuid'], 'JKOROS/Owner', ipò_iye['owner']])
            else:
                raise 실행오류('VM Oníǹkan_iye 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, ipò_iye, msinfo32_exe):
        제어기들 = [iye for Orúkọ, iye in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Orúkọ)]
        Fún_Lááyè_iye = [str(self.ọ̀nà(iye)) for iye in ipò_iye.get('media', [])]
        for Orúkọ, iye in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Orúkọ) for 제어기 in 제어기들):
                if iye not in ('none', 'emptydrive') and iye not in Fún_Lááyè_iye:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + iye)

    def ṣàfihàn_ipò(self):
        ipò_iye = self.Kàá()
        if ipò_iye is None: return {'name': self.Orúkọ, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(ipò_iye, 등록목록(self.Àṣẹ(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', ipò_iye['name']), 'uuid': ipò_iye['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.ọ̀nà(ipò_iye['iso'])) if ipò_iye.get('iso') else None,
                'serial_log': str(self.ọ̀nà(ipò_iye['serial_log'])) if ipò_iye.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ṣiṣẹ́_àṣẹ(self):
        ipò_iye = self.Kàá()
        등록됨 = 등록목록(self.Àṣẹ(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if ipò_iye is not None and ipò_iye['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(ipò_iye, 등록됨, ràpadà_ipò=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 ṣiṣẹ́_àṣẹ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ṣàfihàn_ipò()
            self.매체검사(ipò_iye, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_iye 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Àṣẹ(['VBoxManage', 'controlvm', ipò_iye['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Ṣi 전에 기존 기록도 보관한다.
                    if ipò_iye.get('serial_log'):
                        원본 = self.ọ̀nà(ipò_iye['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ọ̀nà('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Àṣẹ(['VBoxManage', 'startvm', ipò_iye['uuid'], '--type', self.ìlànà_móòdù])
                return self.ṣàfihàn_ipò()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ṣèpapòdà_móòdù 중입니다 ({}). 작업이 끝난 Padà_sẹ́yìn_iye 다시 실행하세요.'.format(현재))
        elif ipò_iye is not None and not ipò_iye.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Orúkọ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_iye/ṣiṣẹ́_àṣẹ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Àṣẹ(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        èbúté_iye = self.ọ̀nà(매체)
        èbúté_iye.parent.mkdir(exist_ok=True)
        if èbúté_iye.exists():
            if 검사합(èbúté_iye) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(èbúté_iye))
        else:
            with tempfile.NamedTemporaryFile(dir=str(èbúté_iye.parent)) as Fáìlì:
                shutil.copyfile(str(원본), Fáìlì.name)
                os.link(Fáìlì.name, str(èbúté_iye))

        if ipò_iye is None:
            ipò_iye = {'version': 1, 'name': self.Orúkọ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_iye(ipò_iye)
        if msinfo32_exe is None:
            self.Àṣẹ(['VBoxManage', 'createvm', '--name', ipò_iye['name'], '--uuid', ipò_iye['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ọ̀nà('machines')), '--register'])
            self.Àṣẹ(['VBoxManage', 'setextradata', ipò_iye['uuid'], 'JKOROS/Owner', ipò_iye['owner']])
        # àtòpọ̀_ètò 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(ipò_iye, 등록목록(self.Àṣẹ(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('àtòpọ̀_ètò 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ipò_iye, msinfo32_exe)
        ipò_iye['iso'] = 매체
        if 매체 not in ipò_iye['media']: ipò_iye['media'].append(매체)
        ipò_iye['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        àkọsílẹ̀_ìṣe_iye = self.ọ̀nà(ipò_iye['serial_log'])
        àkọsílẹ̀_ìṣe_iye.parent.mkdir(exist_ok=True)
        self.Store_iye(ipò_iye)
        self.Àṣẹ(['VBoxManage', 'modifyvm', ipò_iye['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(àkọsílẹ̀_ìṣe_iye)])
        제어기들 = [iye for Orúkọ, iye in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Orúkọ)]
        if 'JKOROS IDE' not in 제어기들:
            self.Àṣẹ(['VBoxManage', 'storagectl', ipò_iye['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Àṣẹ(['VBoxManage', 'storageattach', ipò_iye['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(èbúté_iye)])
        ipò_iye['pending'] = False
        self.Store_iye(ipò_iye)
        self.Àṣẹ(['VBoxManage', 'startvm', ipò_iye['uuid'], '--type', self.ìlànà_móòdù])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ṣàfihàn_ipò()


def Rọ́ọ̀nù():
    ìpínsíwẹ́wẹ́_iye = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ṣiṣẹ́_àṣẹ 및 ipò_iye aṣèbéèré_iye')
    ìpínsíwẹ́wẹ́_iye.add_argument('action', choices=['run', 'status'])
    인자 = ìpínsíwẹ́wẹ́_iye.parse_args()
    ṣiṣẹ́_àṣẹ = àtòjọ_ètò_aṣàfilọ́lẹ̀(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ṣiṣẹ́_àṣẹ.ṣàfihàn_ipò(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. olùpèsè 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/Ìyànda_iye 변경은 하지 않습니다.')
    os.umask(0o077)
    ṣiṣẹ́_àṣẹ.ọ̀nà('lock').parent.mkdir(parents=True, exist_ok=True)
    with ṣiṣẹ́_àṣẹ.ọ̀nà('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ṣiṣẹ́_àṣẹ 작업이 진행 중입니다.')
        print(json.dumps(ṣiṣẹ́_àṣẹ.ṣiṣẹ́_àṣẹ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Rọ́ọ̀nù()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as àṣìṣe:
        print('VBOX àṣìṣe: ' + str(àṣìṣe), file=sys.stderr)
        sys.exit(1)
