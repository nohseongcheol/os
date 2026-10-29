import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

定義値 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
モジュール値 = importlib.util.module_from_spec(定義値)
定義値.loader.exec_module(モジュール値)


class 模擬枠:
    def __init__(self, 根値):
        self.根値 = 根値
        self.命令一覧一覧 = []
        self.仮想機械一覧 = {}
        self.失敗値 = None

    def __call__(self, 引数):
        引数 = list(map(str, 引数))
        self.命令一覧一覧.append(引数)
        if self.失敗値 == 引数[1] or (引数[0] == 'make' and self.失敗値 == 'make'):
            self.失敗値 = None
            raise モジュール値.実行状態エラー('시험용 失敗値')
        if 引数[0] == 'make':
            経路 = self.根値 / 'os/build/kernel.iso'
            経路.parent.mkdir(parents=True, exist_ok=True)
            経路.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        動作 = 引数[1]
        if 動作 == 'list':
            return '\n'.join('"{}" {{{}}}'.format(値['name'], 番号) for 番号, 値 in self.仮想機械一覧.items())
        if 動作 == 'createvm':
            番号, 名前 = 引数[引数.index('--uuid') + 1], 引数[引数.index('--name') + 1]
            self.仮想機械一覧[番号] = {'UUID': 番号, 'name': 名前, 'VMState': 'poweroff',
                'CfgFile': str(self.根値 / '.vbox/machines' / 名前 / (名前 + '.vbox')), 'owner': None}
            return ''
        機械 = self.仮想機械一覧[引数[2]]
        if 動作 == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(名前), json.dumps(値)) for 名前, 値 in 機械.items() if 名前 != 'owner')
        if 動作 == 'getextradata': return 'Value: ' + 機械['owner'] if 機械['owner'] else 'No value set!'
        if 動作 == 'setextradata': 機械['owner'] = 引数[4]
        elif 動作 == 'storagectl': 機械['storagecontrollername0'] = 'JKOROS IDE'
        elif 動作 == 'storageattach': 機械['JKOROS IDE-0-0'] = 引数[引数.index('--medium') + 1]
        elif 動作 == 'startvm': 機械['VMState'] = 'running'
        elif 動作 == 'controlvm':
            assert 引数[3] == 'resume'
            機械['VMState'] = 'running'
        elif 動作 != 'modifyvm': raise AssertionError(引数)
        return ''


class 起動処理試験(unittest.TestCase):
    def setUp(self):
        self.一時値 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.一時値.cleanup)
        self.根値 = Path(self.一時値.name)
        (self.根値 / '.vbox').mkdir()
        self.枠値 = 模擬枠(self.根値)
        self.命令実行 = モジュール値.プログラム実行器(self.根値, 'jkoros operating system', 命令=self.枠値)

    def 入口作成(self):
        結果 = self.命令実行.命令実行()
        self.枠値.命令一覧一覧.clear()
        return self.枠値.仮想機械一覧[結果['uuid']]

    def 判定未変更(self):
        self.assertTrue(all(命令[0] == 'VBoxManage' and 命令[1] in ('list', 'showvminfo', 'getextradata') for 命令 in self.枠値.命令一覧一覧))

    def 初期作成状態論理積光学起動試験(self):
        結果 = self.命令実行.命令実行()
        self.assertEqual(結果['state'], 'running')
        self.assertTrue(Path(結果['iso']).is_file())
        self.assertTrue(any('--nic1' in 命令 and 'none' in 命令 for 命令 in self.枠値.命令一覧一覧))
        self.assertFalse(any('hdd' in 命令 or 'discardstate' in 命令 or 'createmedium' in 命令 for 命令 in self.枠値.命令一覧一覧))

    def 稼働状態仮想機械保持済み試験(self):
        self.入口作成()
        self.assertEqual(self.命令実行.命令実行()['state'], 'running')
        self.判定未変更()

    def 保存済み状況再開論理積履歴記録保持状態試験(self):
        機械 = self.入口作成()
        機械['VMState'] = 'saved'
        履歴記録値 = self.命令実行.経路(self.命令実行.読取()['serial_log'])
        履歴記録値.write_text('saved log')
        self.命令実行.命令実行()
        self.assertFalse(any(命令[0] == 'make' or 命令[1] == 'modifyvm' for 命令 in self.枠値.命令一覧一覧))
        self.assertEqual([経路.read_text() for 経路 in 履歴記録値.parent.glob('before-resume-*.log')], ['saved log'])

    def 一時停止論理積再開試験(self):
        self.入口作成()['VMState'] = 'paused'
        self.命令実行.命令実行()
        self.assertTrue(any(命令[1] == 'controlvm' and 命令[3] == 'resume' for 命令 in self.枠値.命令一覧一覧))
        self.assertFalse(any(命令[0] == 'make' for 命令 in self.枠値.命令一覧一覧))

    def 他方仮想機械名前衝突試験(self):
        self.枠値.仮想機械一覧[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.判定未変更()

    def 所有状態標識却下済み試験(self):
        self.入口作成()['owner'] = 'someone-else'
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.判定未変更()

    def 他方設定値経路却下済み試験(self):
        self.入口作成()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.判定未変更()

    def 追加分利用者ディスク保持済み試験(self):
        機械 = self.入口作成()
        機械['VMState'] = 'poweroff'
        機械['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.判定未変更()

    def 遷移却下済み試験(self):
        self.入口作成()['VMState'] = 'saving'
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.判定未変更()

    def 登録解除却下済み試験(self):
        self.入口作成()
        self.枠値.仮想機械一覧.clear()
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.判定未変更()

    def 仮想機械保持済み有効側構築失敗試験(self):
        機械 = self.入口作成()
        機械['VMState'] = 'poweroff'
        前回項目 = dict(機械)
        self.枠値.失敗値 = 'make'
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.assertEqual(機械, 前回項目)

    def 中断済み所有状態標識回復試験(self):
        self.枠値.失敗値 = 'setextradata'
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()
        self.枠値.命令一覧一覧.clear()
        self.assertEqual(self.命令実行.命令実行()['state'], 'running')
        self.assertFalse(any(命令[1] == 'createvm' for 命令 in self.枠値.命令一覧一覧))

    def 保持済みISO改竄却下済み試験(self):
        機械 = self.入口作成()
        機械['VMState'] = 'poweroff'
        Path(機械['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.命令実行()

    def 不在状況作成済み試験(self):
        self.assertEqual(self.命令実行.状況表示()['state'], 'not-created')
        self.assertFalse(self.枠値.命令一覧一覧)

    def 経路エスケープ却下済み試験(self):
        for 経路 in ('../outside', '/tmp/outside'):
            with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.経路(経路)
        (self.根値 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(モジュール値.実行状態エラー): self.命令実行.経路('media/kernel.iso')

    def VirtualBox52複合特性一覧試験(self):
        結果 = モジュール値.属性値('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(結果['VMState'], 'running')
        self.assertEqual(結果['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
