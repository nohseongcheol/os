#!/usr/bin/env python3
"""jkoros 전용 VirtualBox プログラム実行器. 기존 VM/디스크/格納値 상태는 삭제하지 않는다."""
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


class 実行状態エラー(RuntimeError):
    pass


def シェル命令実行(引数):
    環境 = dict(os.environ, LC_ALL='C')
    結果 = subprocess.run([str(値) for 値 in 引数], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=環境, timeout=180)
    内容物値 = 結果.stdout.decode('utf-8', 'replace')
    if 結果.returncode:
        raise 実行状態エラー('命令 失敗値: ' + ' '.join(str(値) for 値 in 引数) + '\n' + 内容物値[-10000:])
    return 内容物値


def 属性値(内容物値):
    結果 = {}
    for 行 in 内容物値.splitlines():
        if '=' not in 行:
            continue
        名前, 値 = 行.split('=', 1)
        if 名前.startswith('"'):
            名前 = json.loads(名前)
        if 値.startswith('"'):
            try:
                値読取, 終端 = json.JSONDecoder().raw_decode(値)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 終端 == len(値): 値 = 値読取
            except ValueError:
                raise 実行状態エラー('VirtualBox 属性値 書式値 エラー: ' + 行)
        結果[名前] = 値
    return 結果


def 登録済み登録項目一覧(内容物値):
    結果 = {}
    for 行 in 内容物値.splitlines():
        判定等価 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', 行)
        if 判定等価: 結果[判定等価.group(2).lower()] = 判定等価.group(1)
    return 結果


def 検査和(経路):
    値 = hashlib.sha256()
    with 経路.open('rb') as ファイル:
        for データ in iter(lambda: ファイル.read(1024 * 1024), b''): 値.update(データ)
    return 値.hexdigest()


class プログラム実行器:
    def __init__(self, 根値, 名前, メソッド方式='gui', 命令=シェル命令実行):
        self.根値 = Path(根値).resolve()
        self.名前, self.メソッド方式, self.命令 = 名前, メソッド方式, 命令
        self.値保持 = self.根値 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', 名前) or 名前 in ('.', '..'):
            raise 実行状態エラー('VM 이름은 文字·桁値·공백·밑줄·괄호·마침표·하이픈만 사용할 数 있습니다.')
        if メソッド方式 not in ('gui', 'headless'): raise 実行状態エラー('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def 経路(self, 通信相手値):
        if Path(通信相手値).is_absolute() or '..' in Path(通信相手値).parts:
            raise 実行状態エラー('잘못된 관리 経路: ' + str(通信相手値))
        結果 = self.値保持
        for 部分要素値 in ['.vbox'] + list(Path(通信相手値).parts):
            if 部分要素値 == '.vbox': 結果 = self.値保持
            else: 結果 = 結果 / 部分要素値
            if 結果.is_symlink(): raise 実行状態エラー('接続 경로는 사용하지 않습니다: ' + str(結果))
        return 結果

    def 読取(self):
        経路 = self.経路('state.json')
        if not 経路.exists(): return None
        状況値 = json.loads(経路.read_text(encoding='utf-8'))
        if 状況値.get('version') != 1 or 状況値.get('name') != self.名前:
            raise 実行状態エラー('관리 상태의 VM 名前/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for 名前 in ('uuid', 'owner'):
            if str(uuid.UUID(状況値[名前])) != 状況値[名前]: raise 実行状態エラー('잘못된 VM 識別子値')
        return 状況値

    def 格納値(self, 状況値):
        宛先値 = self.経路('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.値保持), delete=False) as ファイル:
            json.dump(状況値, ファイル, ensure_ascii=False, indent=2)
            ファイル.write('\n')
            一時値 = ファイル.name
        os.replace(一時値, str(宛先値))

    def システム情報(self, 状況値, 登録済み値, 状況復旧=False):
        if 状況値['uuid'] not in 登録済み値:
            raise 実行状態エラー('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        システム情報 = 属性値(self.命令(['VBoxManage', 'showvminfo', 状況値['uuid'], '--machinereadable']))
        位置 = Path(システム情報.get('CfgFile', '')).resolve()
        if self.経路('machines').resolve() not in 位置.parents or システム情報.get('UUID') != 状況値['uuid']:
            raise 実行状態エラー('이 프로젝트의 VM 設定値 経路/UUID와 일치하지 않아 변경하지 않습니다.')
        標識値 = self.命令(['VBoxManage', 'getextradata', 状況値['uuid'], 'JKOROS/Owner']).strip()
        if 標識値 != 'Value: ' + 状況値['owner']:
            if 状況復旧 and 状況値.get('pending') and 標識値 == 'No value set!':
                self.命令(['VBoxManage', 'setextradata', 状況値['uuid'], 'JKOROS/Owner', 状況値['owner']])
            else:
                raise 実行状態エラー('VM 所有者値 표식이 일치하지 않아 변경하지 않습니다.')
        return システム情報

    def 媒体検査(self, 状況値, システム情報):
        制御器一覧一覧 = [値 for 名前, 値 in システム情報.items() if re.fullmatch(r'storagecontrollername\d+', 名前)]
        値許可処理 = [str(self.経路(値)) for 値 in 状況値.get('media', [])]
        for 名前, 値 in システム情報.items():
            if any(re.fullmatch(re.escape(制御器) + r'-\d+-\d+', 名前) for 制御器 in 制御器一覧一覧):
                if 値 not in ('none', 'emptydrive') and 値 not in 値許可処理:
                    raise 実行状態エラー('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + 値)

    def 状況表示(self):
        状況値 = self.読取()
        if 状況値 is None: return {'name': self.名前, 'state': 'not-created'}
        システム情報 = self.システム情報(状況値, 登録済み登録項目一覧(self.命令(['VBoxManage', 'list', 'vms'])))
        return {'name': システム情報.get('name', 状況値['name']), 'uuid': 状況値['uuid'], 'state': システム情報.get('VMState'),
                'iso': str(self.経路(状況値['iso'])) if 状況値.get('iso') else None,
                'serial_log': str(self.経路(状況値['serial_log'])) if 状況値.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 命令実行(self):
        状況値 = self.読取()
        登録済み値 = 登録済み登録項目一覧(self.命令(['VBoxManage', 'list', 'vms']))
        システム情報 = None
        if 状況値 is not None and 状況値['uuid'] in 登録済み値:
            システム情報 = self.システム情報(状況値, 登録済み値, 状況復旧=True)
            現在項目 = システム情報.get('VMState')
            if 現在項目 == 'running':
                print('이미 命令実行 중입니다. 재빌드·재시작하지 않습니다.')
                return self.状況表示()
            self.媒体検査(状況値, システム情報)
            if 現在項目 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 格納値 상태를 버리지 않습니다.'.format(現在項目))
                if 現在項目 == 'paused':
                    self.命令(['VBoxManage', 'controlvm', 状況値['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 再試行処理値 開放 전에 기존 기록도 보관한다.
                    if 状況値.get('serial_log'):
                        原本 = self.経路(状況値['serial_log'])
                        if 原本.is_file():
                            shutil.copyfile(str(原本), str(self.経路('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.命令(['VBoxManage', 'startvm', 状況値['uuid'], '--type', self.メソッド方式])
                return self.状況表示()
            if 現在項目 not in ('poweroff', 'aborted'):
                raise 実行状態エラー('VM이 切替方式 중입니다 ({}). 작업이 끝난 後端値 再試行処理値 실행하세요.'.format(現在項目))
        elif 状況値 is not None and not 状況値.get('pending'):
            raise 実行状態エラー('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 再試行処理値 등록하세요.')
        elif self.名前 in 登録済み値.values():
            raise 実行状態エラー('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # 格納値/命令実行 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.命令(['make', '-C', str(self.根値 / 'os'), 'iso']), end='')
        原本 = self.根値 / 'os/build/kernel.iso'
        if not 原本.is_file() or 原本.stat().st_size == 0: raise 実行状態エラー('起動 ISO가 생성되지 않았습니다.')
        媒体値 = 'media/kernel-' + 検査和(原本) + '.iso'
        宛先値 = self.経路(媒体値)
        宛先値.parent.mkdir(exist_ok=True)
        if 宛先値.exists():
            if 検査和(宛先値) != 検査和(原本): raise 実行状態エラー('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(宛先値))
        else:
            with tempfile.NamedTemporaryFile(dir=str(宛先値.parent)) as ファイル:
                shutil.copyfile(str(原本), ファイル.name)
                os.link(ファイル.name, str(宛先値))

        if 状況値 is None:
            状況値 = {'version': 1, 'name': self.名前, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.格納値(状況値)
        if システム情報 is None:
            self.命令(['VBoxManage', 'createvm', '--name', 状況値['name'], '--uuid', 状況値['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.経路('machines')), '--register'])
            self.命令(['VBoxManage', 'setextradata', 状況値['uuid'], 'JKOROS/Owner', 状況値['owner']])
        # システム構築 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        システム情報 = self.システム情報(状況値, 登録済み登録項目一覧(self.命令(['VBoxManage', 'list', 'vms'])))
        if システム情報.get('VMState') not in ('poweroff', 'aborted'):
            raise 実行状態エラー('システム構築 중 VM 상태가 바뀌었습니다. 再試行処理値 make vbox를 실행하세요.')
        self.媒体検査(状況値, システム情報)
        状況値['iso'] = 媒体値
        if 媒体値 not in 状況値['media']: 状況値['media'].append(媒体値)
        状況値['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        履歴記録値 = self.経路(状況値['serial_log'])
        履歴記録値.parent.mkdir(exist_ok=True)
        self.格納値(状況値)
        self.命令(['VBoxManage', 'modifyvm', 状況値['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(履歴記録値)])
        制御器一覧一覧 = [値 for 名前, 値 in システム情報.items() if re.fullmatch(r'storagecontrollername\d+', 名前)]
        if 'JKOROS IDE' not in 制御器一覧一覧:
            self.命令(['VBoxManage', 'storagectl', 状況値['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.命令(['VBoxManage', 'storageattach', 状況値['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(宛先値)])
        状況値['pending'] = False
        self.格納値(状況値)
        self.命令(['VBoxManage', 'startvm', 状況値['uuid'], '--type', self.メソッド方式])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.状況表示()


def 起動処理():
    値解析 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 命令実行 및 状況値 照会値')
    値解析.add_argument('action', choices=['run', 'status'])
    仮引数引数 = 値解析.parse_args()
    命令実行 = プログラム実行器(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 仮引数引数.action == 'status':
        print(json.dumps(命令実行.状況表示(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 実行状態エラー('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 実行状態エラー('/dev/vboxdrv에 접근할 数 없습니다. ホスト 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/許可値 변경은 하지 않습니다.')
    os.umask(0o077)
    命令実行.経路('lock').parent.mkdir(parents=True, exist_ok=True)
    with 命令実行.経路('lock').open('a') as 錠値:
        try: fcntl.flock(錠値, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 実行状態エラー('다른 jkoros VirtualBox 命令実行 작업이 진행 중입니다.')
        print(json.dumps(命令実行.命令実行(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: 起動処理()
    except (実行状態エラー, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as エラー:
        print('VBOX エラー: ' + str(エラー), file=sys.stderr)
        sys.exit(1)
