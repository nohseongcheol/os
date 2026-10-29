#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 運行器. 기존 VM/디스크/存儲值 상태는 삭제하지 않는다."""
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


class 執行狀態錯誤(RuntimeError):
    pass


def 執行命令殼命令(實參):
    環境 = dict(os.environ, LC_ALL='C')
    結果 = subprocess.run([str(值) for 值 in 實參], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=環境, timeout=180)
    內容值 = 結果.stdout.decode('utf-8', 'replace')
    if 結果.returncode:
        raise 執行狀態錯誤('命令 失敗值: ' + ' '.join(str(值) for 值 in 實參) + '\n' + 內容值[-10000:])
    return 內容值


def 屬性值(內容值):
    結果 = {}
    for 行 in 內容值.splitlines():
        if '=' not in 行:
            continue
        名稱, 值 = 行.split('=', 1)
        if 名稱.startswith('"'):
            名稱 = json.loads(名稱)
        if 值.startswith('"'):
            try:
                讀取值, 結尾 = json.JSONDecoder().raw_decode(值)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 結尾 == len(值): 值 = 讀取值
            except ValueError:
                raise 執行狀態錯誤('VirtualBox 屬性值 格式值 錯誤: ' + 行)
        結果[名稱] = 值
    return 結果


def 已註冊條目列(內容值):
    結果 = {}
    for 行 in 內容值.splitlines():
        是否相等 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', 行)
        if 是否相等: 結果[是否相等.group(2).lower()] = 是否相等.group(1)
    return 結果


def 校驗和(路徑):
    值 = hashlib.sha256()
    with 路徑.open('rb') as 檔案:
        for 資料 in iter(lambda: 檔案.read(1024 * 1024), b''): 值.update(資料)
    return 值.hexdigest()


class 運行器:
    def __init__(self, 根值, 名稱, 方法模式='gui', 命令=執行命令殼命令):
        self.根值 = Path(根值).resolve()
        self.名稱, self.方法模式, self.命令 = 名稱, 方法模式, 命令
        self.保留值 = self.根值 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', 名稱) or 名稱 in ('.', '..'):
            raise 執行狀態錯誤('VM 이름은 字元·數字值·공백·밑줄·괄호·마침표·하이픈만 사용할 數 있습니다.')
        if 方法模式 not in ('gui', 'headless'): raise 執行狀態錯誤('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def 路徑(self, 對端值):
        if Path(對端值).is_absolute() or '..' in Path(對端值).parts:
            raise 執行狀態錯誤('잘못된 관리 路徑: ' + str(對端值))
        結果 = self.保留值
        for 子部分值 in ['.vbox'] + list(Path(對端值).parts):
            if 子部分值 == '.vbox': 結果 = self.保留值
            else: 結果 = 結果 / 子部分值
            if 結果.is_symlink(): raise 執行狀態錯誤('連接 경로는 사용하지 않습니다: ' + str(結果))
        return 結果

    def 讀取(self):
        路徑 = self.路徑('state.json')
        if not 路徑.exists(): return None
        狀態值 = json.loads(路徑.read_text(encoding='utf-8'))
        if 狀態值.get('version') != 1 or 狀態值.get('name') != self.名稱:
            raise 執行狀態錯誤('관리 상태의 VM 名稱/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for 名稱 in ('uuid', 'owner'):
            if str(uuid.UUID(狀態值[名稱])) != 狀態值[名稱]: raise 執行狀態錯誤('잘못된 VM 標識符值')
        return 狀態值

    def 存儲值(self, 狀態值):
        目的地址值 = self.路徑('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.保留值), delete=False) as 檔案:
            json.dump(狀態值, 檔案, ensure_ascii=False, indent=2)
            檔案.write('\n')
            臨時值 = 檔案.name
        os.replace(臨時值, str(目的地址值))

    def 系統信息(self, 狀態值, 已註冊值, 恢復狀態=False):
        if 狀態值['uuid'] not in 已註冊值:
            raise 執行狀態錯誤('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        系統信息 = 屬性值(self.命令(['VBoxManage', 'showvminfo', 狀態值['uuid'], '--machinereadable']))
        位置 = Path(系統信息.get('CfgFile', '')).resolve()
        if self.路徑('machines').resolve() not in 位置.parents or 系統信息.get('UUID') != 狀態值['uuid']:
            raise 執行狀態錯誤('이 프로젝트의 VM 設置 路徑/UUID와 일치하지 않아 변경하지 않습니다.')
        標記值 = self.命令(['VBoxManage', 'getextradata', 狀態值['uuid'], 'JKOROS/Owner']).strip()
        if 標記值 != 'Value: ' + 狀態值['owner']:
            if 恢復狀態 and 狀態值.get('pending') and 標記值 == 'No value set!':
                self.命令(['VBoxManage', 'setextradata', 狀態值['uuid'], 'JKOROS/Owner', 狀態值['owner']])
            else:
                raise 執行狀態錯誤('VM 所有者值 표식이 일치하지 않아 변경하지 않습니다.')
        return 系統信息

    def 檢查介質(self, 狀態值, 系統信息):
        控制器列列表 = [值 for 名稱, 值 in 系統信息.items() if re.fullmatch(r'storagecontrollername\d+', 名稱)]
        允許值 = [str(self.路徑(值)) for 值 in 狀態值.get('media', [])]
        for 名稱, 值 in 系統信息.items():
            if any(re.fullmatch(re.escape(控制器) + r'-\d+-\d+', 名稱) for 控制器 in 控制器列列表):
                if 值 not in ('none', 'emptydrive') and 值 not in 允許值:
                    raise 執行狀態錯誤('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + 值)

    def 顯示狀態(self):
        狀態值 = self.讀取()
        if 狀態值 is None: return {'name': self.名稱, 'state': 'not-created'}
        系統信息 = self.系統信息(狀態值, 已註冊條目列(self.命令(['VBoxManage', 'list', 'vms'])))
        return {'name': 系統信息.get('name', 狀態值['name']), 'uuid': 狀態值['uuid'], 'state': 系統信息.get('VMState'),
                'iso': str(self.路徑(狀態值['iso'])) if 狀態值.get('iso') else None,
                'serial_log': str(self.路徑(狀態值['serial_log'])) if 狀態值.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 執行命令(self):
        狀態值 = self.讀取()
        已註冊值 = 已註冊條目列(self.命令(['VBoxManage', 'list', 'vms']))
        系統信息 = None
        if 狀態值 is not None and 狀態值['uuid'] in 已註冊值:
            系統信息 = self.系統信息(狀態值, 已註冊值, 恢復狀態=True)
            當前項目 = 系統信息.get('VMState')
            if 當前項目 == 'running':
                print('이미 執行命令 중입니다. 재빌드·재시작하지 않습니다.')
                return self.顯示狀態()
            self.檢查介質(狀態值, 系統信息)
            if 當前項目 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 存儲值 상태를 버리지 않습니다.'.format(當前項目))
                if 當前項目 == 'paused':
                    self.命令(['VBoxManage', 'controlvm', 狀態值['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 重試值 打開 전에 기존 기록도 보관한다.
                    if 狀態值.get('serial_log'):
                        原始 = self.路徑(狀態值['serial_log'])
                        if 原始.is_file():
                            shutil.copyfile(str(原始), str(self.路徑('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.命令(['VBoxManage', 'startvm', 狀態值['uuid'], '--type', self.方法模式])
                return self.顯示狀態()
            if 當前項目 not in ('poweroff', 'aborted'):
                raise 執行狀態錯誤('VM이 切換模式 중입니다 ({}). 작업이 끝난 後端值 重試值 실행하세요.'.format(當前項目))
        elif 狀態值 is not None and not 狀態值.get('pending'):
            raise 執行狀態錯誤('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 重試值 등록하세요.')
        elif self.名稱 in 已註冊值.values():
            raise 執行狀態錯誤('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # 存儲值/執行命令 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.命令(['make', '-C', str(self.根值 / 'os'), 'iso']), end='')
        原始 = self.根值 / 'os/build/kernel.iso'
        if not 原始.is_file() or 原始.stat().st_size == 0: raise 執行狀態錯誤('啓動 ISO가 생성되지 않았습니다.')
        介質值 = 'media/kernel-' + 校驗和(原始) + '.iso'
        目的地址值 = self.路徑(介質值)
        目的地址值.parent.mkdir(exist_ok=True)
        if 目的地址值.exists():
            if 校驗和(目的地址值) != 校驗和(原始): raise 執行狀態錯誤('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(目的地址值))
        else:
            with tempfile.NamedTemporaryFile(dir=str(目的地址值.parent)) as 檔案:
                shutil.copyfile(str(原始), 檔案.name)
                os.link(檔案.name, str(目的地址值))

        if 狀態值 is None:
            狀態值 = {'version': 1, 'name': self.名稱, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.存儲值(狀態值)
        if 系統信息 is None:
            self.命令(['VBoxManage', 'createvm', '--name', 狀態值['name'], '--uuid', 狀態值['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.路徑('machines')), '--register'])
            self.命令(['VBoxManage', 'setextradata', 狀態值['uuid'], 'JKOROS/Owner', 狀態值['owner']])
        # 構建系統 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        系統信息 = self.系統信息(狀態值, 已註冊條目列(self.命令(['VBoxManage', 'list', 'vms'])))
        if 系統信息.get('VMState') not in ('poweroff', 'aborted'):
            raise 執行狀態錯誤('構建系統 중 VM 상태가 바뀌었습니다. 重試值 make vbox를 실행하세요.')
        self.檢查介質(狀態值, 系統信息)
        狀態值['iso'] = 介質值
        if 介質值 not in 狀態值['media']: 狀態值['media'].append(介質值)
        狀態值['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        日誌值 = self.路徑(狀態值['serial_log'])
        日誌值.parent.mkdir(exist_ok=True)
        self.存儲值(狀態值)
        self.命令(['VBoxManage', 'modifyvm', 狀態值['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(日誌值)])
        控制器列列表 = [值 for 名稱, 值 in 系統信息.items() if re.fullmatch(r'storagecontrollername\d+', 名稱)]
        if 'JKOROS IDE' not in 控制器列列表:
            self.命令(['VBoxManage', 'storagectl', 狀態值['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.命令(['VBoxManage', 'storageattach', 狀態值['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(目的地址值)])
        狀態值['pending'] = False
        self.存儲值(狀態值)
        self.命令(['VBoxManage', 'startvm', 狀態值['uuid'], '--type', self.方法模式])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.顯示狀態()


def 運行():
    解析值 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 執行命令 및 狀態值 查詢值')
    解析值.add_argument('action', choices=['run', 'status'])
    形式參數實際參數 = 解析值.parse_args()
    執行命令 = 運行器(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 形式參數實際參數.action == 'status':
        print(json.dumps(執行命令.顯示狀態(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 執行狀態錯誤('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 執行狀態錯誤('/dev/vboxdrv에 접근할 數 없습니다. 宿主 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/權限值 변경은 하지 않습니다.')
    os.umask(0o077)
    執行命令.路徑('lock').parent.mkdir(parents=True, exist_ok=True)
    with 執行命令.路徑('lock').open('a') as 鎖值:
        try: fcntl.flock(鎖值, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 執行狀態錯誤('다른 jkoros VirtualBox 執行命令 작업이 진행 중입니다.')
        print(json.dumps(執行命令.執行命令(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: 運行()
    except (執行狀態錯誤, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as 錯誤:
        print('VBOX 錯誤: ' + str(錯誤), file=sys.stderr)
        sys.exit(1)
