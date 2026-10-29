"""واقعی_داده_ها ELF اجرا_فرمان + OpenJDK سنجش 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.فهرست_مقدار_e5561a2b = Path(self.임시.name)

    def ساختن_منبع(self, مبداء, 추가=None, 성공=True, هدف='linux', 내보냄=None):
        مسیر_لیست = []
        for نام, محتوا_مقدار in dict({'시험': مبداء}, **(추가 or {})).items():
            مسیر = self.فهرست_مقدار_e5561a2b / (نام + '.java')
            مسیر.write_text(محتوا_مقدار, encoding='utf-8')
            مسیر_لیست.append(str(مسیر))
        فرمان = [sys.executable, str(컴파일러), '--target', هدف, '--entry', '시험.اجرا_2', '-o', str(self.فهرست_مقدار_e5561a2b / 'native')]
        if 내보냄 is not None: فرمان += ['--export', 내보냄]
        سنجش = subprocess.run(فرمان + مسیر_لیست,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(سنجش.returncode, 0, سنجش.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(سنجش.returncode, 0)
            self.assertIn('ساختن_منبع خطا'.encode(), سنجش.stderr)
        return سنجش

    def 실행결과(self):
        return subprocess.run([str(self.فهرست_مقدار_e5561a2b / 'native')], timeout=5).returncode

    def 자바대조(self, مبداء, 추가=None):
        self.ساختن_منبع(مبداء, 추가)
        (self.فهرست_مقدار_e5561a2b / 'میزبان.java').write_text(
            'public class میزبان { public static void main(String[] نشانوندها) { System.exit(시험.اجرا_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.فهرست_مقدار_e5561a2b)] +
                       [str(مسیر) for مسیر in self.فهرست_مقدار_e5561a2b.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.فهرست_مقدار_e5561a2b), 'میزبان'], timeout=5).returncode
        واقعی_داده_ها = self.실행결과()
        self.assertGreaterEqual(واقعی_داده_ها, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 تأیید_صحت)')
        self.assertEqual(واقعی_داده_ها, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int اجرا_2() {
                int 합 = 7;
                int مقدار = 12345;
                for (int فهرست = -65; فهرست <= 65; فهرست++) {
                    مقدار = مقدار * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(مقدار, فهرست);
                    합 += (byte)مقدار + (short)مقدار + (char)مقدار;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] مقدار = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int اجرا_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < مقدار.length; 가++)
                    for (int 나 = 1; 나 < مقدار.length; 나++)
                        합 = 합 * 31 + مقدار[가] / مقدار[나] + مقدار[가] % مقدار[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ایجاد_ورودی(int اندازه) { return new int[اندازه]; }
            public static int اجرا_2() {
                int[] 가 = ایجاد_ورودی(8); int[] 나 = 가; int[] خالی_شئ = new int[0];
                if (가 != 나 || 가 == null || خالی_شئ.length != 0 || 가[7] != 0) return 99;
                int مقدار = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return مقدار + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int مقدار = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int اجرا_2() { return 계산(1, 2, 3, 4, مقدار) + 보조.خواندن(); }
        }''', {'보조': '''public class 보조 {
            static int مقدار = 3;
            static int 초기값() { return ++مقدار; }
            static int خواندن() { return مقدار; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int مقدار = 보조.خواندن() + 1;
            public static int اجرا_2() { return مقدار * 10 + 보조.خواندن(); }
        }''', {'보조': '''public class 보조 {
            static int مقدار = 시험.مقدار + 2;
            static int خواندن() { return مقدار; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String متن = "한글\\u0000😀";
            public static int اجرا_2() {
                if (متن != "한글\\u0000😀") return 99;
                return (متن.length() + متن.charAt(2) + متن.charAt(3) + متن.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int فاکتوریل(int مقدار) { return مقدار <= 1 ? 1 : مقدار * فاکتوریل(مقدار - 1); }
            static int 연속(int مقدار) {
                switch (مقدار) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int مقدار) {
                switch (مقدار) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int اجرا_2() { return (فاکتوریل(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        اعلامیه = '\n'.join('int مقدار{} = {};'.format(فهرست, فهرست) for فهرست in range(270))
        덧셈 = '+'.join('مقدار{}'.format(فهرست) for فهرست in range(270))
        self.자바대조('public class 시험 { public static int اجرا_2() {' + اعلامیه +
                    'مقدار_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] مقدار = null; return مقدار.length;', 102),
            ('int[] مقدار = new int[1]; return مقدار[1];', 103),
            ('int[] مقدار = new int[1]; مقدار[-1] = 3; return 0;', 103),
            ('int مقدار = -1; return new int[مقدار].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for متن_مقدار, 기대 in 경우들:
            with self.subTest(متن_مقدار=متن_مقدار):
                self.ساختن_منبع('public class 시험 { public static int اجرا_2() { ' + متن_مقدار + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long مقدار; public static int اجرا_2() { return 0; }',
            'public static int اجرا_2() { Object مقدار = new Object(); return 0; }',
            'public static int اجرا_2() { System.out.println("hello"); return 0; }',
            'public static int اجرا_2() { try { return 1; } catch (Exception خطا) { return 2; } }',
            'public static synchronized int اجرا_2() { return 0; }',
            'public static int اجرا_2() { return new byte[3].length; }',
            'static native int 외부(); public static int اجرا_2() { return 외부(); }',
            'int مقدار; public static int اجرا_2() { return 0; }',
        ]
        for متن_مقدار in 경우들:
            with self.subTest(متن_مقدار=متن_مقدار):
                self.ساختن_منبع('public class 시험 { ' + متن_مقدار + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        خروجی = self.فهرست_مقدار_e5561a2b / 'native'
        خروجی.write_bytes(b'original-output')
        self.ساختن_منبع('public class 시험 { public static int اجرا_2() { return missing; } }', 성공=False)
        self.assertEqual(خروجی.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ساختن_منبع('public class 시험 { public static int اجرا_2() { return 37; } }')
        self.assertEqual((self.فهرست_مقدار_e5561a2b / 'native').read_bytes()[:5], b'\x7fELF\x01')
        جستجو_جدول = subprocess.check_output(['readelf', '-l', str(self.فهرست_مقدار_e5561a2b / 'native')])
        self.assertNotIn(b'INTERP', جستجو_جدول)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ساختن_منبع('public class 시험 { public static int اجرا_2() { return کاربر.실행권한(); } }',
                    {'کاربر': 'public class کاربر { public static native int 실행권한(); }'}, هدف='user')
        داده_ها = (self.فهرست_مقدار_e5561a2b / 'native').read_bytes()
        self.assertEqual(داده_ها[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', داده_ها, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.فهرست_مقدار_e5561a2b / 'native')]))
        # کاربر ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ساختن_منبع('public class 시험 { public static int اجرا_2() { return دستگاه_مقدار.포트읽기(1); } }',
                    {'دستگاه_مقدار': 'public class دستگاه_مقدار { public static native int 포트읽기(int مقدار); }'}, 성공=False, هدف='user')

    def test_내보내기검증(self):
        مبداء = 'public class 시험 { public static int اجرا_2() { return 0; } static int 호출(int مقدار) { return مقدار; } }'
        self.ساختن_منبع(مبداء, هدف='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.فهرست_مقدار_e5561a2b / 'native')]))
        self.ساختن_منبع(مبداء, 성공=False, 내보냄='bad;name=시험.호출')
        self.ساختن_منبع(مبداء, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
