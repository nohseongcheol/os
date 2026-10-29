"""ପ୍ରକୃତ_ଡାଟା ELF ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ + OpenJDK ମାପ 대조. 임시 시험 자료만 생성한다."""
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
        self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ = Path(self.임시.name)

    def ସଙ୍କଳନ_ଉତ୍ସ(self, ଉତ୍ସ, 추가=None, 성공=True, ଲକ୍ଷ୍ୟସ୍ଥଳ='linux', 내보냄=None):
        ପଥ_ତାଲିକା = []
        for ନାମ, ବିଷୟ_ମୂଲ୍ୟ in dict({'시험': ଉତ୍ସ}, **(추가 or {})).items():
            ପଥ = self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.java')
            ପଥ.write_text(ବିଷୟ_ମୂଲ୍ୟ, encoding='utf-8')
            ପଥ_ତାଲିକା.append(str(ପଥ))
        ନିର୍ଦ୍ଦେଶ = [sys.executable, str(컴파일러), '--target', ଲକ୍ଷ୍ୟସ୍ଥଳ, '--entry', '시험.ଚଳାନ୍ତୁ', '-o', str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native')]
        if 내보냄 is not None: ନିର୍ଦ୍ଦେଶ += ['--export', 내보냄]
        ମାପ = subprocess.run(ନିର୍ଦ୍ଦେଶ + ପଥ_ତାଲିକା,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ମାପ.returncode, 0, ମାପ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ମାପ.returncode, 0)
            self.assertIn('ସଙ୍କଳନ_ଉତ୍ସ ତ୍ରୁଟି'.encode(), ମାପ.stderr)
        return ମାପ

    def 실행결과(self):
        return subprocess.run([str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native')], timeout=5).returncode

    def 자바대조(self, ଉତ୍ସ, 추가=None):
        self.ସଙ୍କଳନ_ଉତ୍ସ(ଉତ୍ସ, 추가)
        (self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'ଆୟୋଜକ.java').write_text(
            'public class ଆୟୋଜକ { public static void main(String[] 인수) { System.exit(시험.ଚଳାନ୍ତୁ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)] +
                       [str(ପଥ) for ପଥ in self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ), 'ଆୟୋଜକ'], timeout=5).returncode
        ପ୍ରକୃତ_ଡାଟା = self.실행결과()
        self.assertGreaterEqual(ପ୍ରକୃତ_ଡାଟା, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ଯାଞ୍ଚ୍_କରିବା)')
        self.assertEqual(ପ୍ରକୃତ_ଡାଟା, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ଚଳାନ୍ତୁ() {
                int 합 = 7;
                int ମୂଲ୍ୟ = 12345;
                for (int ଅନୁକ୍ରମଣିକା = -65; ଅନୁକ୍ରମଣିକା <= 65; ଅନୁକ୍ରମଣିକା++) {
                    ମୂଲ୍ୟ = ମୂଲ୍ୟ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ମୂଲ୍ୟ, ଅନୁକ୍ରମଣିକା);
                    합 += (byte)ମୂଲ୍ୟ + (short)ମୂଲ୍ୟ + (char)ମୂଲ୍ୟ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ମୂଲ୍ୟ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ଚଳାନ୍ତୁ() {
                int 합 = 13;
                for (int 가 = 0; 가 < ମୂଲ୍ୟ.length; 가++)
                    for (int 나 = 1; 나 < ମୂଲ୍ୟ.length; 나++)
                        합 = 합 * 31 + ମୂଲ୍ୟ[가] / ମୂଲ୍ୟ[나] + ମୂଲ୍ୟ[가] % ମୂଲ୍ୟ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(int ଆକାର) { return new int[ଆକାର]; }
            public static int ଚଳାନ୍ତୁ() {
                int[] 가 = ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(8); int[] 나 = 가; int[] ଖାଲି_ଅବଜେକ୍ଟ = new int[0];
                if (가 != 나 || 가 == null || ଖାଲି_ଅବଜେକ୍ଟ.length != 0 || 가[7] != 0) return 99;
                int ମୂଲ୍ୟ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ମୂଲ୍ୟ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ମୂଲ୍ୟ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ଚଳାନ୍ତୁ() { return 계산(1, 2, 3, 4, ମୂଲ୍ୟ) + 보조.ପଢନ୍ତୁ(); }
        }''', {'보조': '''public class 보조 {
            static int ମୂଲ୍ୟ = 3;
            static int 초기값() { return ++ମୂଲ୍ୟ; }
            static int ପଢନ୍ତୁ() { return ମୂଲ୍ୟ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ମୂଲ୍ୟ = 보조.ପଢନ୍ତୁ() + 1;
            public static int ଚଳାନ୍ତୁ() { return ମୂଲ୍ୟ * 10 + 보조.ପଢନ୍ତୁ(); }
        }''', {'보조': '''public class 보조 {
            static int ମୂଲ୍ୟ = 시험.ମୂଲ୍ୟ + 2;
            static int ପଢନ୍ତୁ() { return ମୂଲ୍ୟ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ପାଠ୍ଯ = "한글\\u0000😀";
            public static int ଚଳାନ୍ତୁ() {
                if (ପାଠ୍ଯ != "한글\\u0000😀") return 99;
                return (ପାଠ୍ଯ.length() + ପାଠ୍ଯ.charAt(2) + ପାଠ୍ଯ.charAt(3) + ପାଠ୍ଯ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ଫ୍ୟାକ୍ଟୋରିଆଲ୍(int ମୂଲ୍ୟ) { return ମୂଲ୍ୟ <= 1 ? 1 : ମୂଲ୍ୟ * ଫ୍ୟାକ୍ଟୋରିଆଲ୍(ମୂଲ୍ୟ - 1); }
            static int 연속(int ମୂଲ୍ୟ) {
                switch (ମୂଲ୍ୟ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ମୂଲ୍ୟ) {
                switch (ମୂଲ୍ୟ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ଚଳାନ୍ତୁ() { return (ଫ୍ୟାକ୍ଟୋରିଆଲ୍(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int ମୂଲ୍ୟ{} = {};'.format(ଅନୁକ୍ରମଣିକା, ଅନୁକ୍ରମଣିକା) for ଅନୁକ୍ରମଣିକା in range(270))
        덧셈 = '+'.join('ମୂଲ୍ୟ{}'.format(ଅନୁକ୍ରମଣିକା) for ଅନୁକ୍ରମଣିକା in range(270))
        self.자바대조('public class 시험 { public static int ଚଳାନ୍ତୁ() {' + 선언 +
                    'ମୂଲ୍ୟ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ମୂଲ୍ୟ = null; return ମୂଲ୍ୟ.length;', 102),
            ('int[] ମୂଲ୍ୟ = new int[1]; return ମୂଲ୍ୟ[1];', 103),
            ('int[] ମୂଲ୍ୟ = new int[1]; ମୂଲ୍ୟ[-1] = 3; return 0;', 103),
            ('int ମୂଲ୍ୟ = -1; return new int[ମୂଲ୍ୟ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for ଅବୟବ_ମୂଲ୍ୟ, 기대 in 경우들:
            with self.subTest(ଅବୟବ_ମୂଲ୍ୟ=ଅବୟବ_ମୂଲ୍ୟ):
                self.ସଙ୍କଳନ_ଉତ୍ସ('public class 시험 { public static int ଚଳାନ୍ତୁ() { ' + ଅବୟବ_ମୂଲ୍ୟ + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ମୂଲ୍ୟ; public static int ଚଳାନ୍ତୁ() { return 0; }',
            'public static int ଚଳାନ୍ତୁ() { Object ମୂଲ୍ୟ = new Object(); return 0; }',
            'public static int ଚଳାନ୍ତୁ() { System.out.println("hello"); return 0; }',
            'public static int ଚଳାନ୍ତୁ() { try { return 1; } catch (Exception ତ୍ରୁଟି) { return 2; } }',
            'public static synchronized int ଚଳାନ୍ତୁ() { return 0; }',
            'public static int ଚଳାନ୍ତୁ() { return new byte[3].length; }',
            'static native int 외부(); public static int ଚଳାନ୍ତୁ() { return 외부(); }',
            'int ମୂଲ୍ୟ; public static int ଚଳାନ୍ତୁ() { return 0; }',
        ]
        for ଅବୟବ_ମୂଲ୍ୟ in 경우들:
            with self.subTest(ଅବୟବ_ମୂଲ୍ୟ=ଅବୟବ_ମୂଲ୍ୟ):
                self.ସଙ୍କଳନ_ଉତ୍ସ('public class 시험 { ' + ଅବୟବ_ମୂଲ୍ୟ + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        ନିର୍ଗମ = self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native'
        ନିର୍ଗମ.write_bytes(b'original-output')
        self.ସଙ୍କଳନ_ଉତ୍ସ('public class 시험 { public static int ଚଳାନ୍ତୁ() { return missing; } }', 성공=False)
        self.assertEqual(ନିର୍ଗମ.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ସଙ୍କଳନ_ଉତ୍ସ('public class 시험 { public static int ଚଳାନ୍ତୁ() { return 37; } }')
        self.assertEqual((self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ଦୃଷ୍ଟିପାତ_ସାରଣୀ = subprocess.check_output(['readelf', '-l', str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native')])
        self.assertNotIn(b'INTERP', ଦୃଷ୍ଟିପାତ_ସାରଣୀ)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ସଙ୍କଳନ_ଉତ୍ସ('public class 시험 { public static int ଚଳାନ୍ତୁ() { return ଉପଭୋକ୍ତା.실행권한(); } }',
                    {'ଉପଭୋକ୍ତା': 'public class ଉପଭୋକ୍ତା { public static native int 실행권한(); }'}, ଲକ୍ଷ୍ୟସ୍ଥଳ='user')
        ଡାଟା = (self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native').read_bytes()
        self.assertEqual(ଡାଟା[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ଡାଟା, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native')]))
        # ଉପଭୋକ୍ତା ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ସଙ୍କଳନ_ଉତ୍ସ('public class 시험 { public static int ଚଳାନ୍ତୁ() { return ଡିଭାଇସ_ମୂଲ୍ୟ.포트읽기(1); } }',
                    {'ଡିଭାଇସ_ମୂଲ୍ୟ': 'public class ଡିଭାଇସ_ମୂଲ୍ୟ { public static native int 포트읽기(int ମୂଲ୍ୟ); }'}, 성공=False, ଲକ୍ଷ୍ୟସ୍ଥଳ='user')

    def test_내보내기검증(self):
        ଉତ୍ସ = 'public class 시험 { public static int ଚଳାନ୍ତୁ() { return 0; } static int 호출(int ମୂଲ୍ୟ) { return ମୂଲ୍ୟ; } }'
        self.ସଙ୍କଳନ_ଉତ୍ସ(ଉତ୍ସ, ଲକ୍ଷ୍ୟସ୍ଥଳ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'native')]))
        self.ସଙ୍କଳନ_ଉତ୍ସ(ଉତ୍ସ, 성공=False, 내보냄='bad;name=시험.호출')
        self.ସଙ୍କଳନ_ଉତ୍ସ(ଉତ୍ସ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
