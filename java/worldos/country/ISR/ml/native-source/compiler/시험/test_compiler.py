"""വാസ്തവമായ_ഡാറ്റാ ELF നടപ്പാക്കുക_കമാന്_ഡ് + OpenJDK അളവ് 대조. 임시 시험 자료만 생성한다."""
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
        self.ഡയറക്ടറി_മൂല്യം = Path(self.임시.name)

    def കംപൈല്_ചെയ്യുക_ഉറവിടം(self, ഉറവിടം, 추가=None, 성공=True, ലക്_ഷ്യം='linux', 내보냄=None):
        പാത_ലിസ്റ്റ് = []
        for പേരു്, ഉള്ളടക്കം_മൂല്യം in dict({'시험': ഉറവിടം}, **(추가 or {})).items():
            വഴി = self.ഡയറക്ടറി_മൂല്യം / (പേരു് + '.java')
            വഴി.write_text(ഉള്ളടക്കം_മൂല്യം, encoding='utf-8')
            പാത_ലിസ്റ്റ്.append(str(വഴി))
        ആജ്ഞ = [sys.executable, str(컴파일러), '--target', ലക്_ഷ്യം, '--entry', '시험.നടപ്പിലാക്കുക', '-o', str(self.ഡയറക്ടറി_മൂല്യം / 'native')]
        if 내보냄 is not None: ആജ്ഞ += ['--export', 내보냄]
        അളവ് = subprocess.run(ആജ്ഞ + പാത_ലിസ്റ്റ്,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(അളവ്.returncode, 0, അളവ്.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(അളവ്.returncode, 0)
            self.assertIn('കംപൈല്_ചെയ്യുക_ഉറവിടം പിശക്'.encode(), അളവ്.stderr)
        return അളവ്

    def 실행결과(self):
        return subprocess.run([str(self.ഡയറക്ടറി_മൂല്യം / 'native')], timeout=5).returncode

    def 자바대조(self, ഉറവിടം, 추가=None):
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം(ഉറവിടം, 추가)
        (self.ഡയറക്ടറി_മൂല്യം / 'ഹോസ്റ്റ്.java').write_text(
            'public class ഹോസ്റ്റ് { public static void main(String[] 인수) { System.exit(시험.നടപ്പിലാക്കുക()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ഡയറക്ടറി_മൂല്യം)] +
                       [str(വഴി) for വഴി in self.ഡയറക്ടറി_മൂല്യം.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ഡയറക്ടറി_മൂല്യം), 'ഹോസ്റ്റ്'], timeout=5).returncode
        വാസ്തവമായ_ഡാറ്റാ = self.실행결과()
        self.assertGreaterEqual(വാസ്തവമായ_ഡാറ്റാ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 പരിശോധിക്കുക)')
        self.assertEqual(വാസ്തവമായ_ഡാറ്റാ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int നടപ്പിലാക്കുക() {
                int 합 = 7;
                int മൂല്യം = 12345;
                for (int സൂചിക = -65; സൂചിക <= 65; സൂചിക++) {
                    മൂല്യം = മൂല്യം * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(മൂല്യം, സൂചിക);
                    합 += (byte)മൂല്യം + (short)മൂല്യം + (char)മൂല്യം;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] മൂല്യം = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int നടപ്പിലാക്കുക() {
                int 합 = 13;
                for (int 가 = 0; 가 < മൂല്യം.length; 가++)
                    for (int 나 = 1; 나 < മൂല്യം.length; 나++)
                        합 = 합 * 31 + മൂല്യം[가] / മൂല്യം[나] + മൂല്യം[가] % മൂല്യം[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] സൃഷ്_ടിക്കുക_എന്_ട്രി(int വലിപ്പം) { return new int[വലിപ്പം]; }
            public static int നടപ്പിലാക്കുക() {
                int[] 가 = സൃഷ്_ടിക്കുക_എന്_ട്രി(8); int[] 나 = 가; int[] ശൂന്യം_ഓബ്ജക്റ്റ് = new int[0];
                if (가 != 나 || 가 == null || ശൂന്യം_ഓബ്ജക്റ്റ്.length != 0 || 가[7] != 0) return 99;
                int മൂല്യം = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return മൂല്യം + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int മൂല്യം = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int നടപ്പിലാക്കുക() { return 계산(1, 2, 3, 4, മൂല്യം) + 보조.വായന(); }
        }''', {'보조': '''public class 보조 {
            static int മൂല്യം = 3;
            static int 초기값() { return ++മൂല്യം; }
            static int വായന() { return മൂല്യം; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int മൂല്യം = 보조.വായന() + 1;
            public static int നടപ്പിലാക്കുക() { return മൂല്യം * 10 + 보조.വായന(); }
        }''', {'보조': '''public class 보조 {
            static int മൂല്യം = 시험.മൂല്യം + 2;
            static int വായന() { return മൂല്യം; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String പദാവലി = "한글\\u0000😀";
            public static int നടപ്പിലാക്കുക() {
                if (പദാവലി != "한글\\u0000😀") return 99;
                return (പദാവലി.length() + പദാവലി.charAt(2) + പദാവലി.charAt(3) + പദാവലി.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ക്രമഗുണിതം(int മൂല്യം) { return മൂല്യം <= 1 ? 1 : മൂല്യം * ക്രമഗുണിതം(മൂല്യം - 1); }
            static int 연속(int മൂല്യം) {
                switch (മൂല്യം) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int മൂല്യം) {
                switch (മൂല്യം) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int നടപ്പിലാക്കുക() { return (ക്രമഗുണിതം(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        പ്രസ്താവം = '\n'.join('int മൂല്യം{} = {};'.format(സൂചിക, സൂചിക) for സൂചിക in range(270))
        덧셈 = '+'.join('മൂല്യം{}'.format(സൂചിക) for സൂചിക in range(270))
        self.자바대조('public class 시험 { public static int നടപ്പിലാക്കുക() {' + പ്രസ്താവം +
                    'മൂല്യം_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] മൂല്യം = null; return മൂല്യം.length;', 102),
            ('int[] മൂല്യം = new int[1]; return മൂല്യം[1];', 103),
            ('int[] മൂല്യം = new int[1]; മൂല്യം[-1] = 3; return 0;', 103),
            ('int മൂല്യം = -1; return new int[മൂല്യം].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for ബോഡി_മൂല്യം, 기대 in 경우들:
            with self.subTest(ബോഡി_മൂല്യം=ബോഡി_മൂല്യം):
                self.കംപൈല്_ചെയ്യുക_ഉറവിടം('public class 시험 { public static int നടപ്പിലാക്കുക() { ' + ബോഡി_മൂല്യം + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long മൂല്യം; public static int നടപ്പിലാക്കുക() { return 0; }',
            'public static int നടപ്പിലാക്കുക() { Object മൂല്യം = new Object(); return 0; }',
            'public static int നടപ്പിലാക്കുക() { System.out.println("hello"); return 0; }',
            'public static int നടപ്പിലാക്കുക() { try { return 1; } catch (Exception പിശക്) { return 2; } }',
            'public static synchronized int നടപ്പിലാക്കുക() { return 0; }',
            'public static int നടപ്പിലാക്കുക() { return new byte[3].length; }',
            'static native int 외부(); public static int നടപ്പിലാക്കുക() { return 외부(); }',
            'int മൂല്യം; public static int നടപ്പിലാക്കുക() { return 0; }',
        ]
        for ബോഡി_മൂല്യം in 경우들:
            with self.subTest(ബോഡി_മൂല്യം=ബോഡി_മൂല്യം):
                self.കംപൈല്_ചെയ്യുക_ഉറവിടം('public class 시험 { ' + ബോഡി_മൂല്യം + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        ഫലം = self.ഡയറക്ടറി_മൂല്യം / 'native'
        ഫലം.write_bytes(b'original-output')
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം('public class 시험 { public static int നടപ്പിലാക്കുക() { return missing; } }', 성공=False)
        self.assertEqual(ഫലം.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം('public class 시험 { public static int നടപ്പിലാക്കുക() { return 37; } }')
        self.assertEqual((self.ഡയറക്ടറി_മൂല്യം / 'native').read_bytes()[:5], b'\x7fELF\x01')
        തിരഞ്ഞു_നോക്കൽ_పట్టిక = subprocess.check_output(['readelf', '-l', str(self.ഡയറക്ടറി_മൂല്യം / 'native')])
        self.assertNotIn(b'INTERP', തിരഞ്ഞു_നോക്കൽ_పట్టిక)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം('public class 시험 { public static int നടപ്പിലാക്കുക() { return ഉപയോക്താവ്.실행권한(); } }',
                    {'ഉപയോക്താവ്': 'public class ഉപയോക്താവ് { public static native int 실행권한(); }'}, ലക്_ഷ്യം='user')
        ഡാറ്റാ = (self.ഡയറക്ടറി_മൂല്യം / 'native').read_bytes()
        self.assertEqual(ഡാറ്റാ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ഡാറ്റാ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ഡയറക്ടറി_മൂല്യം / 'native')]))
        # ഉപയോക്താവ് ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം('public class 시험 { public static int നടപ്പിലാക്കുക() { return മൊബൈൽ_മൂല്യം.포트읽기(1); } }',
                    {'മൊബൈൽ_മൂല്യം': 'public class മൊബൈൽ_മൂല്യം { public static native int 포트읽기(int മൂല്യം); }'}, 성공=False, ലക്_ഷ്യം='user')

    def test_내보내기검증(self):
        ഉറവിടം = 'public class 시험 { public static int നടപ്പിലാക്കുക() { return 0; } static int 호출(int മൂല്യം) { return മൂല്യം; } }'
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം(ഉറവിടം, ലക്_ഷ്യം='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ഡയറക്ടറി_മൂല്യം / 'native')]))
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം(ഉറവിടം, 성공=False, 내보냄='bad;name=시험.호출')
        self.കംപൈല്_ചെയ്യുക_ഉറവിടം(ഉറവിടം, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
