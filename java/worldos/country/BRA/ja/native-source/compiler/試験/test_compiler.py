"""実際データ ELF 命令実行 + OpenJDK 結果 대조. 一時値 試験 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

コンパイラ = Path(__file__).resolve().parents[1] / 'コンパイラ.py'


class 自前試験(unittest.TestCase):
    def setUp(self):
        self.一時値 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.一時値.cleanup)
        self.ディレクトリ値 = Path(self.一時値.name)

    def ソースコンパイル(self, ソース, 入口追記=None, 成功値=True, 対象値='linux', 公開済み値=None):
        経路一覧 = []
        for 名前, 内容物値 in dict({'試験': ソース}, **(入口追記 or {})).items():
            経路 = self.ディレクトリ値 / (名前 + '.java')
            経路.write_text(内容物値, encoding='utf-8')
            経路一覧.append(str(経路))
        命令 = [sys.executable, str(コンパイラ), '--target', 対象値, '--entry', '試験.起動処理', '-o', str(self.ディレクトリ値 / 'native')]
        if 公開済み値 is not None: 命令 += ['--export', 公開済み値]
        結果 = subprocess.run(命令 + 経路一覧,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 成功値:
            self.assertEqual(結果.returncode, 0, 結果.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(結果.returncode, 0)
            self.assertIn('ソースコンパイル エラー'.encode(), 結果.stderr)
        return 結果

    def 実行状態結果(self):
        return subprocess.run([str(self.ディレクトリ値 / 'native')], timeout=5).returncode

    def Java比較状態(self, ソース, 入口追記=None):
        self.ソースコンパイル(ソース, 入口追記)
        (self.ディレクトリ値 / 'ホスト.java').write_text(
            'public class ホスト { public static void main(String[] 引数) { System.exit(試験.起動処理()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ディレクトリ値)] +
                       [str(経路) for 経路 in self.ディレクトリ値.glob('*.java')], check=True, timeout=30)
        期待状態 = subprocess.run(['java', '-cp', str(self.ディレクトリ値), 'ホスト'], timeout=5).returncode
        実際データ = self.実行状態結果()
        self.assertGreaterEqual(実際データ, 0, '신호로 保有終了済み (샌드박스의 32비트 syscall 上限値 여부 検証)')
        self.assertEqual(実際データ, 期待状態)

    def 整数値算術論理積シフト一覧試験(self):
        self.Java比較状態('''public class 試験 {
            static int 混合算術(int 先頭位置被演算子, int 第二被演算子) {
                return ((先頭位置被演算子 + 第二被演算子) ^ (先頭位置被演算子 - 第二被演算子) ^ (先頭位置被演算子 * 第二被演算子) ^ (先頭位置被演算子 & 第二被演算子) ^ (先頭位置被演算子 | 第二被演算子))
                    + (先頭位置被演算子 << 第二被演算子) + (先頭位置被演算子 >> 第二被演算子) + (先頭位置被演算子 >>> 第二被演算子);
            }
            public static int 起動処理() {
                int 総和値 = 7;
                int 値 = 12345;
                for (int 番号 = -65; 番号 <= 65; 番号++) {
                    値 = 値 * 1664525 + 1013904223;
                    総和値 = 総和値 * 31 + 混合算術(値, 番号);
                    総和値 += (byte)値 + (short)値 + (char)値;
                }
                return (総和値 & 0x7fffffff) % 251;
            }
        }''')

    def 除算極値値一覧試験(self):
        self.Java比較状態('''public class 試験 {
            static int[] 値 = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int 起動処理() {
                int 総和値 = 13;
                for (int 先頭位置被演算子 = 0; 先頭位置被演算子 < 値.length; 先頭位置被演算子++)
                    for (int 第二被演算子 = 1; 第二被演算子 < 値.length; 第二被演算子++)
                        総和値 = 総和値 * 31 + 値[先頭位置被演算子] / 値[第二被演算子] + 値[先頭位置被演算子] % 値[第二被演算子];
                return (総和値 & 0x7fffffff) % 251;
            }
        }''')

    def 配列群論理積参照一覧試験(self):
        self.Java比較状態('''public class 試験 {
            static int[] 入口作成(int 容量) { return new int[容量]; }
            public static int 起動処理() {
                int[] 先頭位置被演算子 = 入口作成(8); int[] 第二被演算子 = 先頭位置被演算子; int[] 空オブジェクト = new int[0];
                if (先頭位置被演算子 != 第二被演算子 || 先頭位置被演算子 == null || 空オブジェクト.length != 0 || 先頭位置被演算子[7] != 0) return 99;
                int 値 = (先頭位置被演算子[2] = 40); 先頭位置被演算子[2]++; ++先頭位置被演算子[3]; 先頭位置被演算子[2] += 7;
                return 値 + 第二被演算子[2] + 第二被演算子[3];
            }
        }''')

    def 静的フィールド一覧論理積引数順序試験(self):
        self.Java比較状態('''public class 試験 {
            static int 値 = 補助値.初期値();
            static int 計算結果(int 先頭位置被演算子, int 第二被演算子, int 第三被演算子, int 第四被演算子, int 第五被演算子) {
                return 先頭位置被演算子 + 第二被演算子 * 2 + 第三被演算子 * 3 + 第四被演算子 * 4 + 第五被演算子 * 5;
            }
            public static int 起動処理() { return 計算結果(1, 2, 3, 4, 値) + 補助値.読取(); }
        }''', {'補助値': '''public class 補助値 {
            static int 値 = 3;
            static int 初期値() { return ++値; }
            static int 読取() { return 値; }
        }'''})

    def 初期化状態周期試験(self):
        self.Java比較状態('''public class 試験 {
            static int 値 = 補助値.読取() + 1;
            public static int 起動処理() { return 値 * 10 + 補助値.読取(); }
        }''', {'補助値': '''public class 補助値 {
            static int 値 = 試験.値 + 2;
            static int 読取() { return 値; }
        }'''})

    def 改変済みUTF8文字列群試験(self):
        self.Java比較状態('''public class 試験 {
            static String 文 = "한글\\u0000😀";
            public static int 起動処理() {
                if (文 != "한글\\u0000😀") return 99;
                return (文.length() + 文.charAt(2) + 文.charAt(3) + 文.charAt(4)) % 251;
            }
        }''')

    def 切替論理積再帰試験(self):
        self.Java比較状態('''public class 試験 {
            static int 階乗(int 値) { return 値 <= 1 ? 1 : 値 * 階乗(値 - 1); }
            static int 密切替分岐一覧(int 値) {
                switch (値) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 疎切替分岐一覧(int 値) {
                switch (値) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int 起動処理() { return (階乗(5) + 密切替分岐一覧(0) + 密切替分岐一覧(2) + 密切替分岐一覧(9) + 疎切替分岐一覧(-1000) + 疎切替分岐一覧(0)) % 251; }
        }''')

    def 広幅局所変数一覧試験(self):
        宣言 = '\n'.join('int 値{} = {};'.format(番号, 番号) for 番号 in range(270))
        加算結果結果 = '+'.join('値{}'.format(番号) for 番号 in range(270))
        self.Java比較状態('public class 試験 { public static int 起動処理() {' + 宣言 +
                    '値269 += 300; return (' + 加算結果結果 + ') % 251; } }')

    def 実行環境エラー番号一覧試験(self):
        場合登録項目一覧 = [
            ('int 零被演算子 = 0; return 1 / 零被演算子;', 101),
            ('int[] 値 = null; return 値.length;', 102),
            ('int[] 値 = new int[1]; return 値[1];', 103),
            ('int[] 値 = new int[1]; 値[-1] = 3; return 0;', 103),
            ('int 値 = -1; return new int[値].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 先頭位置被演算子 = new int[65535]; return new int[1].length;', 105),
        ]
        for 本体値, 期待状態 in 場合登録項目一覧:
            with self.subTest(本体値=本体値):
                self.ソースコンパイル('public class 試験 { public static int 起動処理() { ' + 本体値 + ' } }')
                self.assertEqual(self.実行状態結果(), 期待状態)

    def 未対応機能却下済み試験(self):
        場合登録項目一覧 = [
            'static long 値; public static int 起動処理() { return 0; }',
            'public static int 起動処理() { Object 値 = new Object(); return 0; }',
            'public static int 起動処理() { System.out.println("hello"); return 0; }',
            'public static int 起動処理() { try { return 1; } catch (Exception エラー) { return 2; } }',
            'public static synchronized int 起動処理() { return 0; }',
            'public static int 起動処理() { return new byte[3].length; }',
            'static native int 外部値(); public static int 起動処理() { return 外部値(); }',
            'int 値; public static int 起動処理() { return 0; }',
        ]
        for 本体値 in 場合登録項目一覧:
            with self.subTest(本体値=本体値):
                self.ソースコンパイル('public class 試験 { ' + 本体値 + ' }', 成功値=False)

    def 既存出力保持済み有効側失敗試験(self):
        出力 = self.ディレクトリ値 / 'native'
        出力.write_bytes(b'original-output')
        self.ソースコンパイル('public class 試験 { public static int 起動処理() { return missing; } }', 成功値=False)
        self.assertEqual(出力.read_bytes(), b'original-output')

    def ELF論理積単独実行状態試験(self):
        self.ソースコンパイル('public class 試験 { public static int 起動処理() { return 37; } }')
        self.assertEqual((self.ディレクトリ値 / 'native').read_bytes()[:5], b'\x7fELF\x01')
        表 = subprocess.check_output(['readelf', '-l', str(self.ディレクトリ値 / 'native')])
        self.assertNotIn(b'INTERP', 表)
        self.assertEqual(self.実行状態結果(), 37)

    def 利用者ELF論理積ABI分離試験(self):
        self.ソースコンパイル('public class 試験 { public static int 起動処理() { return 利用者.実行状態許可(); } }',
                    {'利用者': 'public class 利用者 { public static native int 実行状態許可(); }'}, 対象値='user')
        データ = (self.ディレクトリ値 / 'native').read_bytes()
        self.assertEqual(データ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', データ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ディレクトリ値 / 'native')]))
        # 利用者 ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ソースコンパイル('public class 試験 { public static int 起動処理() { return 装置.機器ポート読取(1); } }',
                    {'装置': 'public class 装置 { public static native int 機器ポート読取(int 値); }'}, 成功値=False, 対象値='user')

    def 公開妥当性試験(self):
        ソース = 'public class 試験 { public static int 起動処理() { return 0; } static int 呼出(int 値) { return 値; } }'
        self.ソースコンパイル(ソース, 対象値='kernel', 公開済み値='kernel_dispatch=試験.呼出')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ディレクトリ値 / 'native')]))
        self.ソースコンパイル(ソース, 成功値=False, 公開済み値='bad;name=試験.呼出')
        self.ソースコンパイル(ソース, 成功値=False, 公開済み値='missing=試験.未存在メソッド')


if __name__ == '__main__':
    unittest.main()
