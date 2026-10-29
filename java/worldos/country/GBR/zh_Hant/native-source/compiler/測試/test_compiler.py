"""實際資料 ELF 執行命令 + OpenJDK 結果 대조. 臨時值 測試 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

編譯器 = Path(__file__).resolve().parents[1] / '編譯器.py'


class 測試原生(unittest.TestCase):
    def setUp(self):
        self.臨時值 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.臨時值.cleanup)
        self.目錄值 = Path(self.臨時值.name)

    def 編譯原始碼(self, 原始碼, 追加條目=None, 成功值=True, 目標值='linux', 已導出值=None):
        路徑列表 = []
        for 名稱, 內容值 in dict({'測試': 原始碼}, **(追加條目 or {})).items():
            路徑 = self.目錄值 / (名稱 + '.java')
            路徑.write_text(內容值, encoding='utf-8')
            路徑列表.append(str(路徑))
        命令 = [sys.executable, str(編譯器), '--target', 目標值, '--entry', '測試.運行', '-o', str(self.目錄值 / 'native')]
        if 已導出值 is not None: 命令 += ['--export', 已導出值]
        結果 = subprocess.run(命令 + 路徑列表,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 成功值:
            self.assertEqual(結果.returncode, 0, 結果.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(結果.returncode, 0)
            self.assertIn('編譯原始碼 錯誤'.encode(), 結果.stderr)
        return 結果

    def 執行狀態結果(self):
        return subprocess.run([str(self.目錄值 / 'native')], timeout=5).returncode

    def Java比較(self, 原始碼, 追加條目=None):
        self.編譯原始碼(原始碼, 追加條目)
        (self.目錄值 / '宿主.java').write_text(
            'public class 宿主 { public static void main(String[] 實參) { System.exit(測試.運行()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.目錄值)] +
                       [str(路徑) for 路徑 in self.目錄值.glob('*.java')], check=True, timeout=30)
        期望狀態 = subprocess.run(['java', '-cp', str(self.目錄值), '宿主'], timeout=5).returncode
        實際資料 = self.執行狀態結果()
        self.assertGreaterEqual(實際資料, 0, '신호로 擁有已退出 (샌드박스의 32비트 syscall 限制值 여부 驗證)')
        self.assertEqual(實際資料, 期望狀態)

    def 測試整數算術與移位列(self):
        self.Java比較('''public class 測試 {
            static int 混合算術(int 首位操作數, int 第二操作數) {
                return ((首位操作數 + 第二操作數) ^ (首位操作數 - 第二操作數) ^ (首位操作數 * 第二操作數) ^ (首位操作數 & 第二操作數) ^ (首位操作數 | 第二操作數))
                    + (首位操作數 << 第二操作數) + (首位操作數 >> 第二操作數) + (首位操作數 >>> 第二操作數);
            }
            public static int 運行() {
                int 總和值 = 7;
                int 值 = 12345;
                for (int 編號 = -65; 編號 <= 65; 編號++) {
                    值 = 值 * 1664525 + 1013904223;
                    總和值 = 總和值 * 31 + 混合算術(值, 編號);
                    總和值 += (byte)值 + (short)值 + (char)值;
                }
                return (總和值 & 0x7fffffff) % 251;
            }
        }''')

    def 測試除法極值值列(self):
        self.Java比較('''public class 測試 {
            static int[] 值 = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int 運行() {
                int 總和值 = 13;
                for (int 首位操作數 = 0; 首位操作數 < 值.length; 首位操作數++)
                    for (int 第二操作數 = 1; 第二操作數 < 值.length; 第二操作數++)
                        總和值 = 總和值 * 31 + 值[首位操作數] / 值[第二操作數] + 值[首位操作數] % 值[第二操作數];
                return (總和值 & 0x7fffffff) % 251;
            }
        }''')

    def 測試陣列集與引用列(self):
        self.Java比較('''public class 測試 {
            static int[] 創建條目(int 大小) { return new int[大小]; }
            public static int 運行() {
                int[] 首位操作數 = 創建條目(8); int[] 第二操作數 = 首位操作數; int[] 空物件 = new int[0];
                if (首位操作數 != 第二操作數 || 首位操作數 == null || 空物件.length != 0 || 首位操作數[7] != 0) return 99;
                int 值 = (首位操作數[2] = 40); 首位操作數[2]++; ++首位操作數[3]; 首位操作數[2] += 7;
                return 值 + 第二操作數[2] + 第二操作數[3];
            }
        }''')

    def 測試靜態字段列與實際參數排序(self):
        self.Java比較('''public class 測試 {
            static int 值 = 輔助值.初始值();
            static int 計算結果(int 首位操作數, int 第二操作數, int 第三操作數, int 第四操作數, int 第五操作數) {
                return 首位操作數 + 第二操作數 * 2 + 第三操作數 * 3 + 第四操作數 * 4 + 第五操作數 * 5;
            }
            public static int 運行() { return 計算結果(1, 2, 3, 4, 值) + 輔助值.讀取(); }
        }''', {'輔助值': '''public class 輔助值 {
            static int 值 = 3;
            static int 初始值() { return ++值; }
            static int 讀取() { return 值; }
        }'''})

    def 測試初始化週期(self):
        self.Java比較('''public class 測試 {
            static int 值 = 輔助值.讀取() + 1;
            public static int 運行() { return 值 * 10 + 輔助值.讀取(); }
        }''', {'輔助值': '''public class 輔助值 {
            static int 值 = 測試.值 + 2;
            static int 讀取() { return 值; }
        }'''})

    def 測試已修改UTF8字符串集(self):
        self.Java比較('''public class 測試 {
            static String 文本 = "한글\\u0000😀";
            public static int 運行() {
                if (文本 != "한글\\u0000😀") return 99;
                return (文本.length() + 文本.charAt(2) + 文本.charAt(3) + 文本.charAt(4)) % 251;
            }
        }''')

    def 測試切換與遞歸(self):
        self.Java比較('''public class 測試 {
            static int 階乘(int 值) { return 值 <= 1 ? 1 : 值 * 階乘(值 - 1); }
            static int 稠密切換分支項集(int 值) {
                switch (值) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 稀疏切換分支項集(int 值) {
                switch (值) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int 運行() { return (階乘(5) + 稠密切換分支項集(0) + 稠密切換分支項集(2) + 稠密切換分支項集(9) + 稀疏切換分支項集(-1000) + 稀疏切換分支項集(0)) % 251; }
        }''')

    def 測試寬幅局部變量列(self):
        聲明 = '\n'.join('int 值{} = {};'.format(編號, 編號) for 編號 in range(270))
        加法結果結果 = '+'.join('值{}'.format(編號) for 編號 in range(270))
        self.Java比較('public class 測試 { public static int 運行() {' + 聲明 +
                    '值269 += 300; return (' + 加法結果結果 + ') % 251; } }')

    def 測試運行時錯誤編號列(self):
        情況條目列 = [
            ('int 零操作數 = 0; return 1 / 零操作數;', 101),
            ('int[] 值 = null; return 值.length;', 102),
            ('int[] 值 = new int[1]; return 值[1];', 103),
            ('int[] 值 = new int[1]; 值[-1] = 3; return 0;', 103),
            ('int 值 = -1; return new int[值].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 首位操作數 = new int[65535]; return new int[1].length;', 105),
        ]
        for 主體值, 期望狀態 in 情況條目列:
            with self.subTest(主體值=主體值):
                self.編譯原始碼('public class 測試 { public static int 運行() { ' + 主體值 + ' } }')
                self.assertEqual(self.執行狀態結果(), 期望狀態)

    def 測試不支持功能已拒絕(self):
        情況條目列 = [
            'static long 值; public static int 運行() { return 0; }',
            'public static int 運行() { Object 值 = new Object(); return 0; }',
            'public static int 運行() { System.out.println("hello"); return 0; }',
            'public static int 運行() { try { return 1; } catch (Exception 錯誤) { return 2; } }',
            'public static synchronized int 運行() { return 0; }',
            'public static int 運行() { return new byte[3].length; }',
            'static native int 外部值(); public static int 運行() { return 外部值(); }',
            'int 值; public static int 運行() { return 0; }',
        ]
        for 主體值 in 情況條目列:
            with self.subTest(主體值=主體值):
                self.編譯原始碼('public class 測試 { ' + 主體值 + ' }', 成功值=False)

    def 測試現有輸出已保留啓用側失敗(self):
        輸出 = self.目錄值 / 'native'
        輸出.write_bytes(b'original-output')
        self.編譯原始碼('public class 測試 { public static int 運行() { return missing; } }', 成功值=False)
        self.assertEqual(輸出.read_bytes(), b'original-output')

    def 測試ELF與獨立執行狀態(self):
        self.編譯原始碼('public class 測試 { public static int 運行() { return 37; } }')
        self.assertEqual((self.目錄值 / 'native').read_bytes()[:5], b'\x7fELF\x01')
        表 = subprocess.check_output(['readelf', '-l', str(self.目錄值 / 'native')])
        self.assertNotIn(b'INTERP', 表)
        self.assertEqual(self.執行狀態結果(), 37)

    def 測試用戶ELF與ABI分離(self):
        self.編譯原始碼('public class 測試 { public static int 運行() { return 使用者.執行狀態權限(); } }',
                    {'使用者': 'public class 使用者 { public static native int 執行狀態權限(); }'}, 目標值='user')
        資料 = (self.目錄值 / 'native').read_bytes()
        self.assertEqual(資料[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', 資料, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.目錄值 / 'native')]))
        # 使用者 ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.編譯原始碼('public class 測試 { public static int 運行() { return 設備.讀取硬件埠(1); } }',
                    {'設備': 'public class 設備 { public static native int 讀取硬件埠(int 值); }'}, 成功值=False, 目標值='user')

    def 測試導出有效性驗證(self):
        原始碼 = 'public class 測試 { public static int 運行() { return 0; } static int 調用(int 值) { return 值; } }'
        self.編譯原始碼(原始碼, 目標值='kernel', 已導出值='kernel_dispatch=測試.調用')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.目錄值 / 'native')]))
        self.編譯原始碼(原始碼, 成功值=False, 已導出值='bad;name=測試.調用')
        self.編譯原始碼(原始碼, 成功值=False, 已導出值='missing=測試.缺失方法')


if __name__ == '__main__':
    unittest.main()
