"""实际数据 ELF 执行命令 + OpenJDK 结果 대조. 临时值 测试 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

编译器 = Path(__file__).resolve().parents[1] / '编译器.py'


class 测试原生(unittest.TestCase):
    def setUp(self):
        self.临时值 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.临时值.cleanup)
        self.目录值 = Path(self.临时值.name)

    def 编译源代码(self, 源代码, 追加条目=None, 成功值=True, 目标值='linux', 已导出值=None):
        路径列表 = []
        for 名称, 内容值 in dict({'测试': 源代码}, **(追加条目 or {})).items():
            路径 = self.目录值 / (名称 + '.java')
            路径.write_text(内容值, encoding='utf-8')
            路径列表.append(str(路径))
        命令 = [sys.executable, str(编译器), '--target', 目标值, '--entry', '测试.运行', '-o', str(self.目录值 / 'native')]
        if 已导出值 is not None: 命令 += ['--export', 已导出值]
        结果 = subprocess.run(命令 + 路径列表,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 成功值:
            self.assertEqual(结果.returncode, 0, 结果.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(结果.returncode, 0)
            self.assertIn('编译源代码 错误'.encode(), 结果.stderr)
        return 结果

    def 执行状态结果(self):
        return subprocess.run([str(self.目录值 / 'native')], timeout=5).returncode

    def Java比较(self, 源代码, 追加条目=None):
        self.编译源代码(源代码, 追加条目)
        (self.目录值 / '宿主.java').write_text(
            'public class 宿主 { public static void main(String[] 实参) { System.exit(测试.运行()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.目录值)] +
                       [str(路径) for 路径 in self.目录值.glob('*.java')], check=True, timeout=30)
        期望状态 = subprocess.run(['java', '-cp', str(self.目录值), '宿主'], timeout=5).returncode
        实际数据 = self.执行状态结果()
        self.assertGreaterEqual(实际数据, 0, '신호로 拥有已退出 (샌드박스의 32비트 syscall 限制值 여부 验证)')
        self.assertEqual(实际数据, 期望状态)

    def 测试整数算术与移位列(self):
        self.Java比较('''public class 测试 {
            static int 混合算术(int 首位操作数, int 第二操作数) {
                return ((首位操作数 + 第二操作数) ^ (首位操作数 - 第二操作数) ^ (首位操作数 * 第二操作数) ^ (首位操作数 & 第二操作数) ^ (首位操作数 | 第二操作数))
                    + (首位操作数 << 第二操作数) + (首位操作数 >> 第二操作数) + (首位操作数 >>> 第二操作数);
            }
            public static int 运行() {
                int 总和值 = 7;
                int 值 = 12345;
                for (int 编号 = -65; 编号 <= 65; 编号++) {
                    值 = 值 * 1664525 + 1013904223;
                    总和值 = 总和值 * 31 + 混合算术(值, 编号);
                    总和值 += (byte)值 + (short)值 + (char)值;
                }
                return (总和值 & 0x7fffffff) % 251;
            }
        }''')

    def 测试除法极值值列(self):
        self.Java比较('''public class 测试 {
            static int[] 值 = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int 运行() {
                int 总和值 = 13;
                for (int 首位操作数 = 0; 首位操作数 < 值.length; 首位操作数++)
                    for (int 第二操作数 = 1; 第二操作数 < 值.length; 第二操作数++)
                        总和值 = 总和值 * 31 + 值[首位操作数] / 值[第二操作数] + 值[首位操作数] % 值[第二操作数];
                return (总和值 & 0x7fffffff) % 251;
            }
        }''')

    def 测试数组集与引用列(self):
        self.Java比较('''public class 测试 {
            static int[] 创建条目(int 大小) { return new int[大小]; }
            public static int 运行() {
                int[] 首位操作数 = 创建条目(8); int[] 第二操作数 = 首位操作数; int[] 空对象 = new int[0];
                if (首位操作数 != 第二操作数 || 首位操作数 == null || 空对象.length != 0 || 首位操作数[7] != 0) return 99;
                int 值 = (首位操作数[2] = 40); 首位操作数[2]++; ++首位操作数[3]; 首位操作数[2] += 7;
                return 值 + 第二操作数[2] + 第二操作数[3];
            }
        }''')

    def 测试静态字段列与参数排序(self):
        self.Java比较('''public class 测试 {
            static int 值 = 辅助值.初始值();
            static int 计算结果(int 首位操作数, int 第二操作数, int 第三操作数, int 第四操作数, int 第五操作数) {
                return 首位操作数 + 第二操作数 * 2 + 第三操作数 * 3 + 第四操作数 * 4 + 第五操作数 * 5;
            }
            public static int 运行() { return 计算结果(1, 2, 3, 4, 值) + 辅助值.读取(); }
        }''', {'辅助值': '''public class 辅助值 {
            static int 值 = 3;
            static int 初始值() { return ++值; }
            static int 读取() { return 值; }
        }'''})

    def 测试初始化周期(self):
        self.Java比较('''public class 测试 {
            static int 值 = 辅助值.读取() + 1;
            public static int 运行() { return 值 * 10 + 辅助值.读取(); }
        }''', {'辅助值': '''public class 辅助值 {
            static int 值 = 测试.值 + 2;
            static int 读取() { return 值; }
        }'''})

    def 测试已修改UTF8字符串集(self):
        self.Java比较('''public class 测试 {
            static String 文本 = "한글\\u0000😀";
            public static int 运行() {
                if (文本 != "한글\\u0000😀") return 99;
                return (文本.length() + 文本.charAt(2) + 文本.charAt(3) + 文本.charAt(4)) % 251;
            }
        }''')

    def 测试切换与递归(self):
        self.Java比较('''public class 测试 {
            static int 阶乘(int 值) { return 值 <= 1 ? 1 : 值 * 阶乘(值 - 1); }
            static int 稠密切换分支项集(int 值) {
                switch (值) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 稀疏切换分支项集(int 值) {
                switch (值) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int 运行() { return (阶乘(5) + 稠密切换分支项集(0) + 稠密切换分支项集(2) + 稠密切换分支项集(9) + 稀疏切换分支项集(-1000) + 稀疏切换分支项集(0)) % 251; }
        }''')

    def 测试宽幅局部变量列(self):
        声明 = '\n'.join('int 值{} = {};'.format(编号, 编号) for 编号 in range(270))
        加法结果结果 = '+'.join('值{}'.format(编号) for 编号 in range(270))
        self.Java比较('public class 测试 { public static int 运行() {' + 声明 +
                    '值269 += 300; return (' + 加法结果结果 + ') % 251; } }')

    def 测试运行时错误编号列(self):
        情况条目列 = [
            ('int 零操作数 = 0; return 1 / 零操作数;', 101),
            ('int[] 值 = null; return 值.length;', 102),
            ('int[] 值 = new int[1]; return 值[1];', 103),
            ('int[] 值 = new int[1]; 值[-1] = 3; return 0;', 103),
            ('int 值 = -1; return new int[值].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 首位操作数 = new int[65535]; return new int[1].length;', 105),
        ]
        for 主体值, 期望状态 in 情况条目列:
            with self.subTest(主体值=主体值):
                self.编译源代码('public class 测试 { public static int 运行() { ' + 主体值 + ' } }')
                self.assertEqual(self.执行状态结果(), 期望状态)

    def 测试不支持功能已拒绝(self):
        情况条目列 = [
            'static long 值; public static int 运行() { return 0; }',
            'public static int 运行() { Object 值 = new Object(); return 0; }',
            'public static int 运行() { System.out.println("hello"); return 0; }',
            'public static int 运行() { try { return 1; } catch (Exception 错误) { return 2; } }',
            'public static synchronized int 运行() { return 0; }',
            'public static int 运行() { return new byte[3].length; }',
            'static native int 外部值(); public static int 运行() { return 外部值(); }',
            'int 值; public static int 运行() { return 0; }',
        ]
        for 主体值 in 情况条目列:
            with self.subTest(主体值=主体值):
                self.编译源代码('public class 测试 { ' + 主体值 + ' }', 成功值=False)

    def 测试现有输出已保留启用侧失败(self):
        输出 = self.目录值 / 'native'
        输出.write_bytes(b'original-output')
        self.编译源代码('public class 测试 { public static int 运行() { return missing; } }', 成功值=False)
        self.assertEqual(输出.read_bytes(), b'original-output')

    def 测试ELF与独立执行状态(self):
        self.编译源代码('public class 测试 { public static int 运行() { return 37; } }')
        self.assertEqual((self.目录值 / 'native').read_bytes()[:5], b'\x7fELF\x01')
        表 = subprocess.check_output(['readelf', '-l', str(self.目录值 / 'native')])
        self.assertNotIn(b'INTERP', 表)
        self.assertEqual(self.执行状态结果(), 37)

    def 测试用户ELF与ABI分离(self):
        self.编译源代码('public class 测试 { public static int 运行() { return 用户.执行状态权限(); } }',
                    {'用户': 'public class 用户 { public static native int 执行状态权限(); }'}, 目标值='user')
        数据 = (self.目录值 / 'native').read_bytes()
        self.assertEqual(数据[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', 数据, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.目录值 / 'native')]))
        # 用户 ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.编译源代码('public class 测试 { public static int 运行() { return 设备.读取硬件端口(1); } }',
                    {'设备': 'public class 设备 { public static native int 读取硬件端口(int 值); }'}, 成功值=False, 目标值='user')

    def 测试导出有效性验证(self):
        源代码 = 'public class 测试 { public static int 运行() { return 0; } static int 调用(int 值) { return 值; } }'
        self.编译源代码(源代码, 目标值='kernel', 已导出值='kernel_dispatch=测试.调用')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.目录值 / 'native')]))
        self.编译源代码(源代码, 成功值=False, 已导出值='bad;name=测试.调用')
        self.编译源代码(源代码, 成功值=False, 已导出值='missing=测试.缺失方法')


if __name__ == '__main__':
    unittest.main()
