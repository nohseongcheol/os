"""ដែលពិត_ទិន្នន័យ ELF អនុវត្ត_ពាក្យបញ្ជា + OpenJDK ការវាស់វែង 대조. 임시 시험 자료만 생성한다."""
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
        self.បញ្ជី_តំលៃ = Path(self.임시.name)

    def ចងក្រង_ប្រភព(self, ប្រភព, 추가=None, 성공=True, គោលដៅ='linux', 내보냄=None):
        ផ្លូវ_បញ្ជី = []
        for ឈ្មោះ, មាតិកា_តំលៃ in dict({'시험': ប្រភព}, **(추가 or {})).items():
            ផ្លូវ = self.បញ្ជី_តំលៃ / (ឈ្មោះ + '.java')
            ផ្លូវ.write_text(មាតិកា_តំលៃ, encoding='utf-8')
            ផ្លូវ_បញ្ជី.append(str(ផ្លូវ))
        ពាក្យ_បញ្ជា = [sys.executable, str(컴파일러), '--target', គោលដៅ, '--entry', '시험.រត់', '-o', str(self.បញ្ជី_តំលៃ / 'native')]
        if 내보냄 is not None: ពាក្យ_បញ្ជា += ['--export', 내보냄]
        ការវាស់វែង = subprocess.run(ពាក្យ_បញ្ជា + ផ្លូវ_បញ្ជី,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ការវាស់វែង.returncode, 0, ការវាស់វែង.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ការវាស់វែង.returncode, 0)
            self.assertIn('ចងក្រង_ប្រភព កំហុស'.encode(), ការវាស់វែង.stderr)
        return ការវាស់វែង

    def 실행결과(self):
        return subprocess.run([str(self.បញ្ជី_តំលៃ / 'native')], timeout=5).returncode

    def 자바대조(self, ប្រភព, 추가=None):
        self.ចងក្រង_ប្រភព(ប្រភព, 추가)
        (self.បញ្ជី_តំលៃ / 'ហូស.java').write_text(
            'public class ហូស { public static void main(String[] អាគុយម៉ង់) { System.exit(시험.រត់()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.បញ្ជី_តំលៃ)] +
                       [str(ផ្លូវ) for ផ្លូវ in self.បញ្ជី_តំលៃ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.បញ្ជី_តំលៃ), 'ហូស'], timeout=5).returncode
        ដែលពិត_ទិន្នន័យ = self.실행결과()
        self.assertGreaterEqual(ដែលពិត_ទិន្នន័យ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ផ្ទៀងផ្ទាត់)')
        self.assertEqual(ដែលពិត_ទិន្នន័យ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int រត់() {
                int 합 = 7;
                int តំលៃ = 12345;
                for (int សន្ទស្សន៏ = -65; សន្ទស្សន៏ <= 65; សន្ទស្សន៏++) {
                    តំលៃ = តំលៃ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(តំលៃ, សន្ទស្សន៏);
                    합 += (byte)តំលៃ + (short)តំលៃ + (char)តំលៃ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] តំលៃ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int រត់() {
                int 합 = 13;
                for (int 가 = 0; 가 < តំលៃ.length; 가++)
                    for (int 나 = 1; 나 < តំលៃ.length; 나++)
                        합 = 합 * 31 + តំលៃ[가] / តំលៃ[나] + តំលៃ[가] % តំលៃ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] បង្កើត_ការបញ្ចូល(int ដាក់ទំហំ) { return new int[ដាក់ទំហំ]; }
            public static int រត់() {
                int[] 가 = បង្កើត_ការបញ្ចូល(8); int[] 나 = 가; int[] ទទេរ_វត្ថុ = new int[0];
                if (가 != 나 || 가 == null || ទទេរ_វត្ថុ.length != 0 || 가[7] != 0) return 99;
                int តំលៃ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return តំលៃ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int តំលៃ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int រត់() { return 계산(1, 2, 3, 4, តំលៃ) + 보조.អាន(); }
        }''', {'보조': '''public class 보조 {
            static int តំលៃ = 3;
            static int 초기값() { return ++តំលៃ; }
            static int អាន() { return តំលៃ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int តំលៃ = 보조.អាន() + 1;
            public static int រត់() { return តំលៃ * 10 + 보조.អាន(); }
        }''', {'보조': '''public class 보조 {
            static int តំលៃ = 시험.តំលៃ + 2;
            static int អាន() { return តំលៃ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String អត្ថបទ = "한글\\u0000😀";
            public static int រត់() {
                if (អត្ថបទ != "한글\\u0000😀") return 99;
                return (អត្ថបទ.length() + អត្ថបទ.charAt(2) + អត្ថបទ.charAt(3) + អត្ថបទ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ហ្វាក់តូរីយែ្យល(int តំលៃ) { return តំលៃ <= 1 ? 1 : តំលៃ * ហ្វាក់តូរីយែ្យល(តំលៃ - 1); }
            static int 연속(int តំលៃ) {
                switch (តំលៃ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int តំលៃ) {
                switch (តំលៃ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int រត់() { return (ហ្វាក់តូរីយែ្យល(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        ការប្រកាស = '\n'.join('int តំលៃ{} = {};'.format(សន្ទស្សន៏, សន្ទស្សន៏) for សន្ទស្សន៏ in range(270))
        덧셈 = '+'.join('តំលៃ{}'.format(សន្ទស្សន៏) for សន្ទស្សន៏ in range(270))
        self.자바대조('public class 시험 { public static int រត់() {' + ការប្រកាស +
                    'តំលៃ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] តំលៃ = null; return តំលៃ.length;', 102),
            ('int[] តំលៃ = new int[1]; return តំលៃ[1];', 103),
            ('int[] តំលៃ = new int[1]; តំលៃ[-1] = 3; return 0;', 103),
            ('int តំលៃ = -1; return new int[តំលៃ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for តួ_តំលៃ, 기대 in 경우들:
            with self.subTest(តួ_តំលៃ=តួ_តំលៃ):
                self.ចងក្រង_ប្រភព('public class 시험 { public static int រត់() { ' + តួ_តំលៃ + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long តំលៃ; public static int រត់() { return 0; }',
            'public static int រត់() { Object តំលៃ = new Object(); return 0; }',
            'public static int រត់() { System.out.println("hello"); return 0; }',
            'public static int រត់() { try { return 1; } catch (Exception កំហុស) { return 2; } }',
            'public static synchronized int រត់() { return 0; }',
            'public static int រត់() { return new byte[3].length; }',
            'static native int 외부(); public static int រត់() { return 외부(); }',
            'int តំលៃ; public static int រត់() { return 0; }',
        ]
        for តួ_តំលៃ in 경우들:
            with self.subTest(តួ_តំលៃ=តួ_តំលៃ):
                self.ចងក្រង_ប្រភព('public class 시험 { ' + តួ_តំលៃ + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        លទ្ធផល = self.បញ្ជី_តំលៃ / 'native'
        លទ្ធផល.write_bytes(b'original-output')
        self.ចងក្រង_ប្រភព('public class 시험 { public static int រត់() { return missing; } }', 성공=False)
        self.assertEqual(លទ្ធផល.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ចងក្រង_ប្រភព('public class 시험 { public static int រត់() { return 37; } }')
        self.assertEqual((self.បញ្ជី_តំលៃ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        រុករក_តារាង = subprocess.check_output(['readelf', '-l', str(self.បញ្ជី_តំលៃ / 'native')])
        self.assertNotIn(b'INTERP', រុករក_តារាង)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ចងក្រង_ប្រភព('public class 시험 { public static int រត់() { return អ្នកប្រើ.실행권한(); } }',
                    {'អ្នកប្រើ': 'public class អ្នកប្រើ { public static native int 실행권한(); }'}, គោលដៅ='user')
        ទិន្នន័យ = (self.បញ្ជី_តំលៃ / 'native').read_bytes()
        self.assertEqual(ទិន្នន័យ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ទិន្នន័យ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.បញ្ជី_តំលៃ / 'native')]))
        # អ្នកប្រើ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ចងក្រង_ប្រភព('public class 시험 { public static int រត់() { return ឧបករណ៍_តំលៃ.포트읽기(1); } }',
                    {'ឧបករណ៍_តំលៃ': 'public class ឧបករណ៍_តំលៃ { public static native int 포트읽기(int តំលៃ); }'}, 성공=False, គោលដៅ='user')

    def test_내보내기검증(self):
        ប្រភព = 'public class 시험 { public static int រត់() { return 0; } static int 호출(int តំលៃ) { return តំលៃ; } }'
        self.ចងក្រង_ប្រភព(ប្រភព, គោលដៅ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.បញ្ជី_តំលៃ / 'native')]))
        self.ចងក្រង_ប្រភព(ប្រភព, 성공=False, 내보냄='bad;name=시험.호출')
        self.ចងក្រង_ប្រភព(ប្រភព, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
