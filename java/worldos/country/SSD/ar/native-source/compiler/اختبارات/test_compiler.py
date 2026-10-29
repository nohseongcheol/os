"""الفعلي_بيانات ELF ينفذ_أمر + OpenJDK نتيجة 대조. 임시 اختبارات 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

محول_برمجي = Path(__file__).resolve().parents[1] / 'محول_برمجي.py'


class يختبر_أصلي(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.دليل_قيمة = Path(self.임시.name)

    def يحول_برمجياً_مصدر(self, مصدر, إلحاق_إدخال=None, 성공=True, الهدف='linux', 내보냄=None):
        مسار_قائمة = []
        for اسم, محتوى_قيمة in dict({'اختبارات': مصدر}, **(إلحاق_إدخال or {})).items():
            مسار = self.دليل_قيمة / (اسم + '.java')
            مسار.write_text(محتوى_قيمة, encoding='utf-8')
            مسار_قائمة.append(str(مسار))
        أمر = [sys.executable, str(محول_برمجي), '--target', الهدف, '--entry', 'اختبارات.تشغيل', '-o', str(self.دليل_قيمة / 'native')]
        if 내보냄 is not None: أمر += ['--export', 내보냄]
        نتيجة = subprocess.run(أمر + مسار_قائمة,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(نتيجة.returncode, 0, نتيجة.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(نتيجة.returncode, 0)
            self.assertIn('يحول_برمجياً_مصدر خطأ'.encode(), نتيجة.stderr)
        return نتيجة

    def 실행결과(self):
        return subprocess.run([str(self.دليل_قيمة / 'native')], timeout=5).returncode

    def 자바대조(self, مصدر, إلحاق_إدخال=None):
        self.يحول_برمجياً_مصدر(مصدر, إلحاق_إدخال)
        (self.دليل_قيمة / 'مضيف.java').write_text(
            'public class مضيف { public static void main(String[] وسائط) { System.exit(اختبارات.تشغيل()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.دليل_قيمة)] +
                       [str(مسار) for مسار in self.دليل_قيمة.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.دليل_قيمة), 'مضيف'], timeout=5).returncode
        الفعلي_بيانات = self.실행결과()
        self.assertGreaterEqual(الفعلي_بيانات, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 يتحقق)')
        self.assertEqual(الفعلي_بيانات, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class اختبارات {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int تشغيل() {
                int 합 = 7;
                int قيمة = 12345;
                for (int فهرس = -65; فهرس <= 65; فهرس++) {
                    قيمة = قيمة * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(قيمة, فهرس);
                    합 += (byte)قيمة + (short)قيمة + (char)قيمة;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class اختبارات {
            static int[] قيمة = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int تشغيل() {
                int 합 = 13;
                for (int 가 = 0; 가 < قيمة.length; 가++)
                    for (int 나 = 1; 나 < قيمة.length; 나++)
                        합 = 합 * 31 + قيمة[가] / قيمة[나] + قيمة[가] % قيمة[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class اختبارات {
            static int[] فتح_إدخال(int حجم) { return new int[حجم]; }
            public static int تشغيل() {
                int[] 가 = فتح_إدخال(8); int[] 나 = 가; int[] فارغ_عنصر = new int[0];
                if (가 != 나 || 가 == null || فارغ_عنصر.length != 0 || 가[7] != 0) return 99;
                int قيمة = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return قيمة + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class اختبارات {
            static int قيمة = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int تشغيل() { return 계산(1, 2, 3, 4, قيمة) + 보조.قراءة(); }
        }''', {'보조': '''public class 보조 {
            static int قيمة = 3;
            static int 초기값() { return ++قيمة; }
            static int قراءة() { return قيمة; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class اختبارات {
            static int قيمة = 보조.قراءة() + 1;
            public static int تشغيل() { return قيمة * 10 + 보조.قراءة(); }
        }''', {'보조': '''public class 보조 {
            static int قيمة = اختبارات.قيمة + 2;
            static int قراءة() { return قيمة; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class اختبارات {
            static String نص = "한글\\u0000😀";
            public static int تشغيل() {
                if (نص != "한글\\u0000😀") return 99;
                return (نص.length() + نص.charAt(2) + نص.charAt(3) + نص.charAt(4)) % 251;
            }
        }''')

    def يختبر_تبديل_و_الإعادة(self):
        self.자바대조('''public class اختبارات {
            static int مضروب(int قيمة) { return قيمة <= 1 ? 1 : قيمة * مضروب(قيمة - 1); }
            static int 연속(int قيمة) {
                switch (قيمة) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int قيمة) {
                switch (قيمة) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int تشغيل() { return (مضروب(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        إعلان = '\n'.join('int قيمة{} = {};'.format(فهرس, فهرس) for فهرس in range(270))
        덧셈 = '+'.join('قيمة{}'.format(فهرس) for فهرس in range(270))
        self.자바대조('public class اختبارات { public static int تشغيل() {' + إعلان +
                    'قيمة_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int صفر_مُعامل = 0; return 1 / صفر_مُعامل;', 101),
            ('int[] قيمة = null; return قيمة.length;', 102),
            ('int[] قيمة = new int[1]; return قيمة[1];', 103),
            ('int[] قيمة = new int[1]; قيمة[-1] = 3; return 0;', 103),
            ('int قيمة = -1; return new int[قيمة].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for نص_أساسي_قيمة, 기대 in 경우들:
            with self.subTest(نص_أساسي_قيمة=نص_أساسي_قيمة):
                self.يحول_برمجياً_مصدر('public class اختبارات { public static int تشغيل() { ' + نص_أساسي_قيمة + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long قيمة; public static int تشغيل() { return 0; }',
            'public static int تشغيل() { Object قيمة = new Object(); return 0; }',
            'public static int تشغيل() { System.out.println("hello"); return 0; }',
            'public static int تشغيل() { try { return 1; } catch (Exception خطأ) { return 2; } }',
            'public static synchronized int تشغيل() { return 0; }',
            'public static int تشغيل() { return new byte[3].length; }',
            'static native int خارجي_قيمة(); public static int تشغيل() { return خارجي_قيمة(); }',
            'int قيمة; public static int تشغيل() { return 0; }',
        ]
        for نص_أساسي_قيمة in 경우들:
            with self.subTest(نص_أساسي_قيمة=نص_أساسي_قيمة):
                self.يحول_برمجياً_مصدر('public class اختبارات { ' + نص_أساسي_قيمة + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        مخرجات = self.دليل_قيمة / 'native'
        مخرجات.write_bytes(b'original-output')
        self.يحول_برمجياً_مصدر('public class اختبارات { public static int تشغيل() { return missing; } }', 성공=False)
        self.assertEqual(مخرجات.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.يحول_برمجياً_مصدر('public class اختبارات { public static int تشغيل() { return 37; } }')
        self.assertEqual((self.دليل_قيمة / 'native').read_bytes()[:5], b'\x7fELF\x01')
        جدول_البحث = subprocess.check_output(['readelf', '-l', str(self.دليل_قيمة / 'native')])
        self.assertNotIn(b'INTERP', جدول_البحث)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.يحول_برمجياً_مصدر('public class اختبارات { public static int تشغيل() { return فضاء_المستخدم.실행권한(); } }',
                    {'فضاء_المستخدم': 'public class فضاء_المستخدم { public static native int 실행권한(); }'}, الهدف='user')
        بيانات = (self.دليل_قيمة / 'native').read_bytes()
        self.assertEqual(بيانات[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', بيانات, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.دليل_قيمة / 'native')]))
        # فضاء_المستخدم ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.يحول_برمجياً_مصدر('public class اختبارات { public static int تشغيل() { return جهاز_قيمة.يقرأ_أجهزة_منفذ(1); } }',
                    {'جهاز_قيمة': 'public class جهاز_قيمة { public static native int يقرأ_أجهزة_منفذ(int قيمة); }'}, 성공=False, الهدف='user')

    def يختبر_تصدير_التحقق_من_صحة(self):
        مصدر = 'public class اختبارات { public static int تشغيل() { return 0; } static int 호출(int قيمة) { return قيمة; } }'
        self.يحول_برمجياً_مصدر(مصدر, الهدف='kernel', 내보냄='kernel_dispatch=اختبارات.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.دليل_قيمة / 'native')]))
        self.يحول_برمجياً_مصدر(مصدر, 성공=False, 내보냄='bad;name=اختبارات.호출')
        self.يحول_برمجياً_مصدر(مصدر, 성공=False, 내보냄='missing=اختبارات.없음')


if __name__ == '__main__':
    unittest.main()
