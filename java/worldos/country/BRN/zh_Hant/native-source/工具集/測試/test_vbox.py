import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

定義值 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
模塊值 = importlib.util.module_from_spec(定義值)
定義值.loader.exec_module(模塊值)


class 模擬框:
    def __init__(self, 根值):
        self.根值 = 根值
        self.命令列列表 = []
        self.虛擬機器列 = {}
        self.失敗值 = None

    def __call__(self, 實參):
        實參 = list(map(str, 實參))
        self.命令列列表.append(實參)
        if self.失敗值 == 實參[1] or (實參[0] == 'make' and self.失敗值 == 'make'):
            self.失敗值 = None
            raise 模塊值.執行狀態錯誤('시험용 失敗值')
        if 實參[0] == 'make':
            路徑 = self.根值 / 'os/build/kernel.iso'
            路徑.parent.mkdir(parents=True, exist_ok=True)
            路徑.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        動作 = 實參[1]
        if 動作 == 'list':
            return '\n'.join('"{}" {{{}}}'.format(值['name'], 編號) for 編號, 值 in self.虛擬機器列.items())
        if 動作 == 'createvm':
            編號, 名稱 = 實參[實參.index('--uuid') + 1], 實參[實參.index('--name') + 1]
            self.虛擬機器列[編號] = {'UUID': 編號, 'name': 名稱, 'VMState': 'poweroff',
                'CfgFile': str(self.根值 / '.vbox/machines' / 名稱 / (名稱 + '.vbox')), 'owner': None}
            return ''
        計算機 = self.虛擬機器列[實參[2]]
        if 動作 == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(名稱), json.dumps(值)) for 名稱, 值 in 計算機.items() if 名稱 != 'owner')
        if 動作 == 'getextradata': return 'Value: ' + 計算機['owner'] if 計算機['owner'] else 'No value set!'
        if 動作 == 'setextradata': 計算機['owner'] = 實參[4]
        elif 動作 == 'storagectl': 計算機['storagecontrollername0'] = 'JKOROS IDE'
        elif 動作 == 'storageattach': 計算機['JKOROS IDE-0-0'] = 實參[實參.index('--medium') + 1]
        elif 動作 == 'startvm': 計算機['VMState'] = 'running'
        elif 動作 == 'controlvm':
            assert 實參[3] == 'resume'
            計算機['VMState'] = 'running'
        elif 動作 != 'modifyvm': raise AssertionError(實參)
        return ''


class 測試運行(unittest.TestCase):
    def setUp(self):
        self.臨時值 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.臨時值.cleanup)
        self.根值 = Path(self.臨時值.name)
        (self.根值 / '.vbox').mkdir()
        self.框值 = 模擬框(self.根值)
        self.執行命令 = 模塊值.運行器(self.根值, 'jkoros operating system', 命令=self.框值)

    def 創建條目(self):
        結果 = self.執行命令.執行命令()
        self.框值.命令列列表.clear()
        return self.框值.虛擬機器列[結果['uuid']]

    def 是否未變(self):
        self.assertTrue(all(命令[0] == 'VBoxManage' and 命令[1] in ('list', 'showvminfo', 'getextradata') for 命令 in self.框值.命令列列表))

    def 測試初始創建過程與光學啓動(self):
        結果 = self.執行命令.執行命令()
        self.assertEqual(結果['state'], 'running')
        self.assertTrue(Path(結果['iso']).is_file())
        self.assertTrue(any('--nic1' in 命令 and 'none' in 命令 for 命令 in self.框值.命令列列表))
        self.assertFalse(any('hdd' in 命令 or 'discardstate' in 命令 or 'createmedium' in 命令 for 命令 in self.框值.命令列列表))

    def 測試運行中虛擬機已保留(self):
        self.創建條目()
        self.assertEqual(self.執行命令.執行命令()['state'], 'running')
        self.是否未變()

    def 測試已保存狀態恢復執行與日誌保留狀態(self):
        計算機 = self.創建條目()
        計算機['VMState'] = 'saved'
        日誌值 = self.執行命令.路徑(self.執行命令.讀取()['serial_log'])
        日誌值.write_text('saved log')
        self.執行命令.執行命令()
        self.assertFalse(any(命令[0] == 'make' or 命令[1] == 'modifyvm' for 命令 in self.框值.命令列列表))
        self.assertEqual([路徑.read_text() for 路徑 in 日誌值.parent.glob('before-resume-*.log')], ['saved log'])

    def 測試暫停與恢復執行(self):
        self.創建條目()['VMState'] = 'paused'
        self.執行命令.執行命令()
        self.assertTrue(any(命令[1] == 'controlvm' and 命令[3] == 'resume' for 命令 in self.框值.命令列列表))
        self.assertFalse(any(命令[0] == 'make' for 命令 in self.框值.命令列列表))

    def 測試其他虛擬機名稱衝突(self):
        self.框值.虛擬機器列[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.是否未變()

    def 測試所有權標記已拒絕(self):
        self.創建條目()['owner'] = 'someone-else'
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.是否未變()

    def 測試其他設置路徑已拒絕(self):
        self.創建條目()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.是否未變()

    def 測試附加用戶磁盤已保留(self):
        計算機 = self.創建條目()
        計算機['VMState'] = 'poweroff'
        計算機['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.是否未變()

    def 測試遷移已拒絕(self):
        self.創建條目()['VMState'] = 'saving'
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.是否未變()

    def 測試註銷已拒絕(self):
        self.創建條目()
        self.框值.虛擬機器列.clear()
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.是否未變()

    def 測試虛擬機已保留啓用側構建失敗(self):
        計算機 = self.創建條目()
        計算機['VMState'] = 'poweroff'
        上一個項目 = dict(計算機)
        self.框值.失敗值 = 'make'
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.assertEqual(計算機, 上一個項目)

    def 測試已中斷所有權標記恢復過程(self):
        self.框值.失敗值 = 'setextradata'
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()
        self.框值.命令列列表.clear()
        self.assertEqual(self.執行命令.執行命令()['state'], 'running')
        self.assertFalse(any(命令[1] == 'createvm' for 命令 in self.框值.命令列列表))

    def 測試已保留國際標準化組織篡改已拒絕(self):
        計算機 = self.創建條目()
        計算機['VMState'] = 'poweroff'
        Path(計算機['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.執行命令()

    def 測試無狀態已創建(self):
        self.assertEqual(self.執行命令.顯示狀態()['state'], 'not-created')
        self.assertFalse(self.框值.命令列列表)

    def 測試路徑轉義已拒絕(self):
        for 路徑 in ('../outside', '/tmp/outside'):
            with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.路徑(路徑)
        (self.根值 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(模塊值.執行狀態錯誤): self.執行命令.路徑('media/kernel.iso')

    def 測試VirtualBox52複合特性列(self):
        結果 = 模塊值.屬性值('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(結果['VMState'], 'running')
        self.assertEqual(結果['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
