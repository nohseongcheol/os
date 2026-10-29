import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

定义值 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
模块值 = importlib.util.module_from_spec(定义值)
定义值.loader.exec_module(模块值)


class 模拟框:
    def __init__(self, 根值):
        self.根值 = 根值
        self.命令列列表 = []
        self.虚拟机器列 = {}
        self.失败值 = None

    def __call__(self, 实参):
        实参 = list(map(str, 实参))
        self.命令列列表.append(实参)
        if self.失败值 == 实参[1] or (实参[0] == 'make' and self.失败值 == 'make'):
            self.失败值 = None
            raise 模块值.执行状态错误('시험용 失败值')
        if 实参[0] == 'make':
            路径 = self.根值 / 'os/build/kernel.iso'
            路径.parent.mkdir(parents=True, exist_ok=True)
            路径.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        动作 = 实参[1]
        if 动作 == 'list':
            return '\n'.join('"{}" {{{}}}'.format(值['name'], 编号) for 编号, 值 in self.虚拟机器列.items())
        if 动作 == 'createvm':
            编号, 名称 = 实参[实参.index('--uuid') + 1], 实参[实参.index('--name') + 1]
            self.虚拟机器列[编号] = {'UUID': 编号, 'name': 名称, 'VMState': 'poweroff',
                'CfgFile': str(self.根值 / '.vbox/machines' / 名称 / (名称 + '.vbox')), 'owner': None}
            return ''
        计算机 = self.虚拟机器列[实参[2]]
        if 动作 == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(名称), json.dumps(值)) for 名称, 值 in 计算机.items() if 名称 != 'owner')
        if 动作 == 'getextradata': return 'Value: ' + 计算机['owner'] if 计算机['owner'] else 'No value set!'
        if 动作 == 'setextradata': 计算机['owner'] = 实参[4]
        elif 动作 == 'storagectl': 计算机['storagecontrollername0'] = 'JKOROS IDE'
        elif 动作 == 'storageattach': 计算机['JKOROS IDE-0-0'] = 实参[实参.index('--medium') + 1]
        elif 动作 == 'startvm': 计算机['VMState'] = 'running'
        elif 动作 == 'controlvm':
            assert 实参[3] == 'resume'
            计算机['VMState'] = 'running'
        elif 动作 != 'modifyvm': raise AssertionError(实参)
        return ''


class 测试运行(unittest.TestCase):
    def setUp(self):
        self.临时值 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.临时值.cleanup)
        self.根值 = Path(self.临时值.name)
        (self.根值 / '.vbox').mkdir()
        self.框值 = 模拟框(self.根值)
        self.执行命令 = 模块值.运行器(self.根值, 'jkoros operating system', 命令=self.框值)

    def 创建条目(self):
        结果 = self.执行命令.执行命令()
        self.框值.命令列列表.clear()
        return self.框值.虚拟机器列[结果['uuid']]

    def 是否未变(self):
        self.assertTrue(all(命令[0] == 'VBoxManage' and 命令[1] in ('list', 'showvminfo', 'getextradata') for 命令 in self.框值.命令列列表))

    def 测试初始创建过程与光学启动(self):
        结果 = self.执行命令.执行命令()
        self.assertEqual(结果['state'], 'running')
        self.assertTrue(Path(结果['iso']).is_file())
        self.assertTrue(any('--nic1' in 命令 and 'none' in 命令 for 命令 in self.框值.命令列列表))
        self.assertFalse(any('hdd' in 命令 or 'discardstate' in 命令 or 'createmedium' in 命令 for 命令 in self.框值.命令列列表))

    def 测试运行中虚拟机已保留(self):
        self.创建条目()
        self.assertEqual(self.执行命令.执行命令()['state'], 'running')
        self.是否未变()

    def 测试已保存状态恢复执行与日志保留状态(self):
        计算机 = self.创建条目()
        计算机['VMState'] = 'saved'
        日志值 = self.执行命令.路径(self.执行命令.读取()['serial_log'])
        日志值.write_text('saved log')
        self.执行命令.执行命令()
        self.assertFalse(any(命令[0] == 'make' or 命令[1] == 'modifyvm' for 命令 in self.框值.命令列列表))
        self.assertEqual([路径.read_text() for 路径 in 日志值.parent.glob('before-resume-*.log')], ['saved log'])

    def 测试暂停与恢复执行(self):
        self.创建条目()['VMState'] = 'paused'
        self.执行命令.执行命令()
        self.assertTrue(any(命令[1] == 'controlvm' and 命令[3] == 'resume' for 命令 in self.框值.命令列列表))
        self.assertFalse(any(命令[0] == 'make' for 命令 in self.框值.命令列列表))

    def 测试其他虚拟机名称冲突(self):
        self.框值.虚拟机器列[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.是否未变()

    def 测试所有权标记已拒绝(self):
        self.创建条目()['owner'] = 'someone-else'
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.是否未变()

    def 测试其他设置路径已拒绝(self):
        self.创建条目()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.是否未变()

    def 测试附加用户磁盘已保留(self):
        计算机 = self.创建条目()
        计算机['VMState'] = 'poweroff'
        计算机['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.是否未变()

    def 测试迁移已拒绝(self):
        self.创建条目()['VMState'] = 'saving'
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.是否未变()

    def 测试注销已拒绝(self):
        self.创建条目()
        self.框值.虚拟机器列.clear()
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.是否未变()

    def 测试虚拟机已保留启用侧构建失败(self):
        计算机 = self.创建条目()
        计算机['VMState'] = 'poweroff'
        上一个项目 = dict(计算机)
        self.框值.失败值 = 'make'
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.assertEqual(计算机, 上一个项目)

    def 测试已中断所有权标记恢复过程(self):
        self.框值.失败值 = 'setextradata'
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()
        self.框值.命令列列表.clear()
        self.assertEqual(self.执行命令.执行命令()['state'], 'running')
        self.assertFalse(any(命令[1] == 'createvm' for 命令 in self.框值.命令列列表))

    def 测试已保留国际标准化组织篡改已拒绝(self):
        计算机 = self.创建条目()
        计算机['VMState'] = 'poweroff'
        Path(计算机['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(模块值.执行状态错误): self.执行命令.执行命令()

    def 测试无状态已创建(self):
        self.assertEqual(self.执行命令.显示状态()['state'], 'not-created')
        self.assertFalse(self.框值.命令列列表)

    def 测试路径转义已拒绝(self):
        for 路径 in ('../outside', '/tmp/outside'):
            with self.assertRaises(模块值.执行状态错误): self.执行命令.路径(路径)
        (self.根值 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(模块值.执行状态错误): self.执行命令.路径('media/kernel.iso')

    def 测试VirtualBox52复合特性列(self):
        结果 = 模块值.属性值('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(结果['VMState'], 'running')
        self.assertEqual(结果['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
