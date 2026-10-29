"""প্রকৃত_ডাটা ELF কার্যকর_করুন_আদেশ + OpenJDK পরিমাপ 대조. 임시 시험 자료만 생성한다."""
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
        self.ডিরেক্টরি_মান = Path(self.임시.name)

    def গঠন_উত্স(self, উৎস_নথি, 추가=None, 성공=True, লক্ষ্য='linux', 내보냄=None):
        পথ_তালিকা = []
        for নাম, সামগ্রি_মান in dict({'시험': উৎস_নথি}, **(추가 or {})).items():
            পথ_2 = self.ডিরেক্টরি_মান / (নাম + '.java')
            পথ_2.write_text(সামগ্রি_মান, encoding='utf-8')
            পথ_তালিকা.append(str(পথ_2))
        আদেশ = [sys.executable, str(컴파일러), '--target', লক্ষ্য, '--entry', '시험.চালনা', '-o', str(self.ডিরেক্টরি_মান / 'native')]
        if 내보냄 is not None: আদেশ += ['--export', 내보냄]
        পরিমাপ = subprocess.run(আদেশ + পথ_তালিকা,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(পরিমাপ.returncode, 0, পরিমাপ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(পরিমাপ.returncode, 0)
            self.assertIn('গঠন_উত্স ত্রুটি'.encode(), পরিমাপ.stderr)
        return পরিমাপ

    def 실행결과(self):
        return subprocess.run([str(self.ডিরেক্টরি_মান / 'native')], timeout=5).returncode

    def 자바대조(self, উৎস_নথি, 추가=None):
        self.গঠন_উত্স(উৎস_নথি, 추가)
        (self.ডিরেক্টরি_মান / 'হোস্ট.java').write_text(
            'public class হোস্ট { public static void main(String[] আর্গুমেন্ট_তালিকা) { System.exit(시험.চালনা()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ডিরেক্টরি_মান)] +
                       [str(পথ_2) for পথ_2 in self.ডিরেক্টরি_মান.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ডিরেক্টরি_মান), 'হোস্ট'], timeout=5).returncode
        প্রকৃত_ডাটা = self.실행결과()
        self.assertGreaterEqual(প্রকৃত_ডাটা, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 যাচাই_করা)')
        self.assertEqual(প্রকৃত_ডাটা, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int চালনা() {
                int 합 = 7;
                int মান = 12345;
                for (int সূচি = -65; সূচি <= 65; সূচি++) {
                    মান = মান * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(মান, সূচি);
                    합 += (byte)মান + (short)মান + (char)মান;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] মান = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int চালনা() {
                int 합 = 13;
                for (int 가 = 0; 가 < মান.length; 가++)
                    for (int 나 = 1; 나 < মান.length; 나++)
                        합 = 합 * 31 + মান[가] / মান[나] + মান[가] % মান[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ক্রিয়েট_ভুক্তি(int আকার) { return new int[আকার]; }
            public static int চালনা() {
                int[] 가 = ক্রিয়েট_ভুক্তি(8); int[] 나 = 가; int[] খালি_বস্তু = new int[0];
                if (가 != 나 || 가 == null || খালি_বস্তু.length != 0 || 가[7] != 0) return 99;
                int মান = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return মান + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int মান = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int চালনা() { return 계산(1, 2, 3, 4, মান) + 보조.পড়া(); }
        }''', {'보조': '''public class 보조 {
            static int মান = 3;
            static int 초기값() { return ++মান; }
            static int পড়া() { return মান; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int মান = 보조.পড়া() + 1;
            public static int চালনা() { return মান * 10 + 보조.পড়া(); }
        }''', {'보조': '''public class 보조 {
            static int মান = 시험.মান + 2;
            static int পড়া() { return মান; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String পাঠ = "한글\\u0000😀";
            public static int চালনা() {
                if (পাঠ != "한글\\u0000😀") return 99;
                return (পাঠ.length() + পাঠ.charAt(2) + পাঠ.charAt(3) + পাঠ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int গৌণিক(int মান) { return মান <= 1 ? 1 : মান * গৌণিক(মান - 1); }
            static int 연속(int মান) {
                switch (মান) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int মান) {
                switch (মান) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int চালনা() { return (গৌণিক(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        ঘোষণা = '\n'.join('int মান{} = {};'.format(সূচি, সূচি) for সূচি in range(270))
        덧셈 = '+'.join('মান{}'.format(সূচি) for সূচি in range(270))
        self.자바대조('public class 시험 { public static int চালনা() {' + ঘোষণা +
                    'মান_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] মান = null; return মান.length;', 102),
            ('int[] মান = new int[1]; return মান[1];', 103),
            ('int[] মান = new int[1]; মান[-1] = 3; return 0;', 103),
            ('int মান = -1; return new int[মান].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for বডি_মান, 기대 in 경우들:
            with self.subTest(বডি_মান=বডি_মান):
                self.গঠন_উত্স('public class 시험 { public static int চালনা() { ' + বডি_মান + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long মান; public static int চালনা() { return 0; }',
            'public static int চালনা() { Object মান = new Object(); return 0; }',
            'public static int চালনা() { System.out.println("hello"); return 0; }',
            'public static int চালনা() { try { return 1; } catch (Exception ত্রুটি) { return 2; } }',
            'public static synchronized int চালনা() { return 0; }',
            'public static int চালনা() { return new byte[3].length; }',
            'static native int 외부(); public static int চালনা() { return 외부(); }',
            'int মান; public static int চালনা() { return 0; }',
        ]
        for বডি_মান in 경우들:
            with self.subTest(বডি_মান=বডি_মান):
                self.গঠন_উত্স('public class 시험 { ' + বডি_মান + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        নির্গম = self.ডিরেক্টরি_মান / 'native'
        নির্গম.write_bytes(b'original-output')
        self.গঠন_উত্স('public class 시험 { public static int চালনা() { return missing; } }', 성공=False)
        self.assertEqual(নির্গম.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.গঠন_উত্স('public class 시험 { public static int চালনা() { return 37; } }')
        self.assertEqual((self.ডিরেক্টরি_মান / 'native').read_bytes()[:5], b'\x7fELF\x01')
        লুকআপ_সারণি = subprocess.check_output(['readelf', '-l', str(self.ডিরেক্টরি_মান / 'native')])
        self.assertNotIn(b'INTERP', লুকআপ_সারণি)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.গঠন_উত্স('public class 시험 { public static int চালনা() { return ব্যবহারকারী.실행권한(); } }',
                    {'ব্যবহারকারী': 'public class ব্যবহারকারী { public static native int 실행권한(); }'}, লক্ষ্য='user')
        ডাটা = (self.ডিরেক্টরি_মান / 'native').read_bytes()
        self.assertEqual(ডাটা[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ডাটা, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ডিরেক্টরি_মান / 'native')]))
        # ব্যবহারকারী ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.গঠন_উত্স('public class 시험 { public static int চালনা() { return ডিভাইস_মান.포트읽기(1); } }',
                    {'ডিভাইস_মান': 'public class ডিভাইস_মান { public static native int 포트읽기(int মান); }'}, 성공=False, লক্ষ্য='user')

    def test_내보내기검증(self):
        উৎস_নথি = 'public class 시험 { public static int চালনা() { return 0; } static int 호출(int মান) { return মান; } }'
        self.গঠন_উত্স(উৎস_নথি, লক্ষ্য='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ডিরেক্টরি_মান / 'native')]))
        self.গঠন_উত্স(উৎস_নথি, 성공=False, 내보냄='bad;name=시험.호출')
        self.গঠন_উত্স(উৎস_নথি, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
