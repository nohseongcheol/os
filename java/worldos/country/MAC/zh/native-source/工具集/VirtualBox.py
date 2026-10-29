#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 运行器. 기존 VM/디스크/存储值 상태는 삭제하지 않는다."""
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


class 执行状态错误(RuntimeError):
    pass


def 执行命令壳命令(实参):
    环境 = dict(os.environ, LC_ALL='C')
    结果 = subprocess.run([str(值) for 值 in 实参], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=环境, timeout=180)
    内容值 = 结果.stdout.decode('utf-8', 'replace')
    if 结果.returncode:
        raise 执行状态错误('命令 失败值: ' + ' '.join(str(值) for 值 in 实参) + '\n' + 内容值[-10000:])
    return 内容值


def 属性值(内容值):
    结果 = {}
    for 行 in 内容值.splitlines():
        if '=' not in 行:
            continue
        名称, 值 = 行.split('=', 1)
        if 名称.startswith('"'):
            名称 = json.loads(名称)
        if 值.startswith('"'):
            try:
                读取值, 结尾 = json.JSONDecoder().raw_decode(值)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 结尾 == len(值): 值 = 读取值
            except ValueError:
                raise 执行状态错误('VirtualBox 属性值 格式值 错误: ' + 行)
        结果[名称] = 值
    return 结果


def 已注册条目列(内容值):
    结果 = {}
    for 行 in 内容值.splitlines():
        是否相等 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', 行)
        if 是否相等: 结果[是否相等.group(2).lower()] = 是否相等.group(1)
    return 结果


def 校验和(路径):
    值 = hashlib.sha256()
    with 路径.open('rb') as 文件:
        for 数据 in iter(lambda: 文件.read(1024 * 1024), b''): 值.update(数据)
    return 值.hexdigest()


class 运行器:
    def __init__(self, 根值, 名称, 方法模式='gui', 命令=执行命令壳命令):
        self.根值 = Path(根值).resolve()
        self.名称, self.方法模式, self.命令 = 名称, 方法模式, 命令
        self.保留值 = self.根值 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', 名称) or 名称 in ('.', '..'):
            raise 执行状态错误('VM 이름은 字符·数字值·공백·밑줄·괄호·마침표·하이픈만 사용할 数 있습니다.')
        if 方法模式 not in ('gui', 'headless'): raise 执行状态错误('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def 路径(self, 对端值):
        if Path(对端值).is_absolute() or '..' in Path(对端值).parts:
            raise 执行状态错误('잘못된 관리 路径: ' + str(对端值))
        结果 = self.保留值
        for 子部分值 in ['.vbox'] + list(Path(对端值).parts):
            if 子部分值 == '.vbox': 结果 = self.保留值
            else: 结果 = 结果 / 子部分值
            if 结果.is_symlink(): raise 执行状态错误('连接 경로는 사용하지 않습니다: ' + str(结果))
        return 结果

    def 读取(self):
        路径 = self.路径('state.json')
        if not 路径.exists(): return None
        状态值 = json.loads(路径.read_text(encoding='utf-8'))
        if 状态值.get('version') != 1 or 状态值.get('name') != self.名称:
            raise 执行状态错误('관리 상태의 VM 名称/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for 名称 in ('uuid', 'owner'):
            if str(uuid.UUID(状态值[名称])) != 状态值[名称]: raise 执行状态错误('잘못된 VM 标识符值')
        return 状态值

    def 存储值(self, 状态值):
        目的地址值 = self.路径('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.保留值), delete=False) as 文件:
            json.dump(状态值, 文件, ensure_ascii=False, indent=2)
            文件.write('\n')
            临时值 = 文件.name
        os.replace(临时值, str(目的地址值))

    def 系统信息(self, 状态值, 已注册值, 恢复状态=False):
        if 状态值['uuid'] not in 已注册值:
            raise 执行状态错误('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        系统信息 = 属性值(self.命令(['VBoxManage', 'showvminfo', 状态值['uuid'], '--machinereadable']))
        位置 = Path(系统信息.get('CfgFile', '')).resolve()
        if self.路径('machines').resolve() not in 位置.parents or 系统信息.get('UUID') != 状态值['uuid']:
            raise 执行状态错误('이 프로젝트의 VM 设置 路径/UUID와 일치하지 않아 변경하지 않습니다.')
        标记值 = self.命令(['VBoxManage', 'getextradata', 状态值['uuid'], 'JKOROS/Owner']).strip()
        if 标记值 != 'Value: ' + 状态值['owner']:
            if 恢复状态 and 状态值.get('pending') and 标记值 == 'No value set!':
                self.命令(['VBoxManage', 'setextradata', 状态值['uuid'], 'JKOROS/Owner', 状态值['owner']])
            else:
                raise 执行状态错误('VM 所有者值 표식이 일치하지 않아 변경하지 않습니다.')
        return 系统信息

    def 检查介质(self, 状态值, 系统信息):
        控制器列列表 = [值 for 名称, 值 in 系统信息.items() if re.fullmatch(r'storagecontrollername\d+', 名称)]
        允许值 = [str(self.路径(值)) for 值 in 状态值.get('media', [])]
        for 名称, 值 in 系统信息.items():
            if any(re.fullmatch(re.escape(控制器) + r'-\d+-\d+', 名称) for 控制器 in 控制器列列表):
                if 值 not in ('none', 'emptydrive') and 值 not in 允许值:
                    raise 执行状态错误('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + 值)

    def 显示状态(self):
        状态值 = self.读取()
        if 状态值 is None: return {'name': self.名称, 'state': 'not-created'}
        系统信息 = self.系统信息(状态值, 已注册条目列(self.命令(['VBoxManage', 'list', 'vms'])))
        return {'name': 系统信息.get('name', 状态值['name']), 'uuid': 状态值['uuid'], 'state': 系统信息.get('VMState'),
                'iso': str(self.路径(状态值['iso'])) if 状态值.get('iso') else None,
                'serial_log': str(self.路径(状态值['serial_log'])) if 状态值.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 执行命令(self):
        状态值 = self.读取()
        已注册值 = 已注册条目列(self.命令(['VBoxManage', 'list', 'vms']))
        系统信息 = None
        if 状态值 is not None and 状态值['uuid'] in 已注册值:
            系统信息 = self.系统信息(状态值, 已注册值, 恢复状态=True)
            当前项目 = 系统信息.get('VMState')
            if 当前项目 == 'running':
                print('이미 执行命令 중입니다. 재빌드·재시작하지 않습니다.')
                return self.显示状态()
            self.检查介质(状态值, 系统信息)
            if 当前项目 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 存储值 상태를 버리지 않습니다.'.format(当前项目))
                if 当前项目 == 'paused':
                    self.命令(['VBoxManage', 'controlvm', 状态值['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 重试值 打开 전에 기존 기록도 보관한다.
                    if 状态值.get('serial_log'):
                        原始 = self.路径(状态值['serial_log'])
                        if 原始.is_file():
                            shutil.copyfile(str(原始), str(self.路径('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.命令(['VBoxManage', 'startvm', 状态值['uuid'], '--type', self.方法模式])
                return self.显示状态()
            if 当前项目 not in ('poweroff', 'aborted'):
                raise 执行状态错误('VM이 切换模式 중입니다 ({}). 작업이 끝난 后端值 重试值 실행하세요.'.format(当前项目))
        elif 状态值 is not None and not 状态值.get('pending'):
            raise 执行状态错误('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 重试值 등록하세요.')
        elif self.名称 in 已注册值.values():
            raise 执行状态错误('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # 存储值/执行命令 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.命令(['make', '-C', str(self.根值 / 'os'), 'iso']), end='')
        原始 = self.根值 / 'os/build/kernel.iso'
        if not 原始.is_file() or 原始.stat().st_size == 0: raise 执行状态错误('启动 ISO가 생성되지 않았습니다.')
        介质值 = 'media/kernel-' + 校验和(原始) + '.iso'
        目的地址值 = self.路径(介质值)
        目的地址值.parent.mkdir(exist_ok=True)
        if 目的地址值.exists():
            if 校验和(目的地址值) != 校验和(原始): raise 执行状态错误('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(目的地址值))
        else:
            with tempfile.NamedTemporaryFile(dir=str(目的地址值.parent)) as 文件:
                shutil.copyfile(str(原始), 文件.name)
                os.link(文件.name, str(目的地址值))

        if 状态值 is None:
            状态值 = {'version': 1, 'name': self.名称, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.存储值(状态值)
        if 系统信息 is None:
            self.命令(['VBoxManage', 'createvm', '--name', 状态值['name'], '--uuid', 状态值['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.路径('machines')), '--register'])
            self.命令(['VBoxManage', 'setextradata', 状态值['uuid'], 'JKOROS/Owner', 状态值['owner']])
        # 构建系统 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        系统信息 = self.系统信息(状态值, 已注册条目列(self.命令(['VBoxManage', 'list', 'vms'])))
        if 系统信息.get('VMState') not in ('poweroff', 'aborted'):
            raise 执行状态错误('构建系统 중 VM 상태가 바뀌었습니다. 重试值 make vbox를 실행하세요.')
        self.检查介质(状态值, 系统信息)
        状态值['iso'] = 介质值
        if 介质值 not in 状态值['media']: 状态值['media'].append(介质值)
        状态值['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        日志值 = self.路径(状态值['serial_log'])
        日志值.parent.mkdir(exist_ok=True)
        self.存储值(状态值)
        self.命令(['VBoxManage', 'modifyvm', 状态值['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(日志值)])
        控制器列列表 = [值 for 名称, 值 in 系统信息.items() if re.fullmatch(r'storagecontrollername\d+', 名称)]
        if 'JKOROS IDE' not in 控制器列列表:
            self.命令(['VBoxManage', 'storagectl', 状态值['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.命令(['VBoxManage', 'storageattach', 状态值['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(目的地址值)])
        状态值['pending'] = False
        self.存储值(状态值)
        self.命令(['VBoxManage', 'startvm', 状态值['uuid'], '--type', self.方法模式])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.显示状态()


def 运行():
    解析值 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 执行命令 및 状态值 查询值')
    解析值.add_argument('action', choices=['run', 'status'])
    形参参数 = 解析值.parse_args()
    执行命令 = 运行器(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 形参参数.action == 'status':
        print(json.dumps(执行命令.显示状态(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 执行状态错误('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 执行状态错误('/dev/vboxdrv에 접근할 数 없습니다. 宿主 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/权限值 변경은 하지 않습니다.')
    os.umask(0o077)
    执行命令.路径('lock').parent.mkdir(parents=True, exist_ok=True)
    with 执行命令.路径('lock').open('a') as 锁值:
        try: fcntl.flock(锁值, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 执行状态错误('다른 jkoros VirtualBox 执行命令 작업이 진행 중입니다.')
        print(json.dumps(执行命令.执行命令(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: 运行()
    except (执行状态错误, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as 错误:
        print('VBOX 错误: ' + str(错误), file=sys.stderr)
        sys.exit(1)
