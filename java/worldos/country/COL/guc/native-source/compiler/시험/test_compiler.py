"""실제 ELF 실행 + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.anaajaalee_ajutuu = Path(self.임시.name)

    def akompiraajaa_eejeejetülein(self, eejeejetülein, 추가=None, 성공=True, 대상='linux', 내보냄=None):
        경로들 = []
        for 이름, alu_ujatüü_ajutuu in dict({'시험': eejeejetülein}, **(추가 or {})).items():
            wopu_a_ttaaleemüin = self.anaajaalee_ajutuu / (이름 + '.java')
            wopu_a_ttaaleemüin.write_text(alu_ujatüü_ajutuu, encoding='utf-8')
            경로들.append(str(wopu_a_ttaaleemüin))
        aluwataaya = [sys.executable, str(컴파일러), '--target', 대상, '--entry', '시험.시작', '-o', str(self.anaajaalee_ajutuu / 'native')]
        if 내보냄 is not None: aluwataaya += ['--export', 내보냄]
        결과 = subprocess.run(aluwataaya + 경로들,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('akompiraajaa_eejeejetülein ajachitia'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.anaajaalee_ajutuu / 'native')], timeout=5).returncode

    def 자바대조(self, eejeejetülein, 추가=None):
        self.akompiraajaa_eejeejetülein(eejeejetülein, 추가)
        (self.anaajaalee_ajutuu / 'epiajatü.java').write_text(
            'public class epiajatü { public static void main(String[] 인수) { System.exit(시험.시작()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.anaajaalee_ajutuu)] +
                       [str(wopu_a_ttaaleemüin) for wopu_a_ttaaleemüin in self.anaajaalee_ajutuu.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.anaajaalee_ajutuu), 'epiajatü'], timeout=5).returncode
        실제 = self.실행결과()
        self.assertGreaterEqual(실제, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 확인)')
        self.assertEqual(실제, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int 시작() {
                int 합 = 7;
                int ajutuu = 12345;
                for (int ee_iyatialujuna = -65; ee_iyatialujuna <= 65; ee_iyatialujuna++) {
                    ajutuu = ajutuu * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ajutuu, ee_iyatialujuna);
                    합 += (byte)ajutuu + (short)ajutuu + (char)ajutuu;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ajutuu = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int 시작() {
                int 합 = 13;
                for (int 가 = 0; 가 < ajutuu.length; 가++)
                    for (int 나 = 1; 나 < ajutuu.length; 나++)
                        합 = 합 * 31 + ajutuu[가] / ajutuu[나] + ajutuu[가] % ajutuu[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int 크기) { return new int[크기]; }
            public static int 시작() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int ajutuu = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ajutuu + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ajutuu = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int 시작() { return 계산(1, 2, 3, 4, ajutuu) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ajutuu = 3;
            static int 초기값() { return ++ajutuu; }
            static int 읽기() { return ajutuu; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ajutuu = 보조.읽기() + 1;
            public static int 시작() { return ajutuu * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ajutuu = 시험.ajutuu + 2;
            static int 읽기() { return ajutuu; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String 글 = "한글\\u0000😀";
            public static int 시작() {
                if (글 != "한글\\u0000😀") return 99;
                return (글.length() + 글.charAt(2) + 글.charAt(3) + 글.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int ajutuu) { return ajutuu <= 1 ? 1 : ajutuu * 계승(ajutuu - 1); }
            static int 연속(int ajutuu) {
                switch (ajutuu) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ajutuu) {
                switch (ajutuu) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int 시작() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int ajutuu{} = {};'.format(ee_iyatialujuna, ee_iyatialujuna) for ee_iyatialujuna in range(270))
        덧셈 = '+'.join('ajutuu{}'.format(ee_iyatialujuna) for ee_iyatialujuna in range(270))
        self.자바대조('public class 시험 { public static int 시작() {' + 선언 +
                    'ajutuu_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ajutuu = null; return ajutuu.length;', 102),
            ('int[] ajutuu = new int[1]; return ajutuu[1];', 103),
            ('int[] ajutuu = new int[1]; ajutuu[-1] = 3; return 0;', 103),
            ('int ajutuu = -1; return new int[ajutuu].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.akompiraajaa_eejeejetülein('public class 시험 { public static int 시작() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ajutuu; public static int 시작() { return 0; }',
            'public static int 시작() { Object ajutuu = new Object(); return 0; }',
            'public static int 시작() { System.out.println("hello"); return 0; }',
            'public static int 시작() { try { return 1; } catch (Exception ajachitia) { return 2; } }',
            'public static synchronized int 시작() { return 0; }',
            'public static int 시작() { return new byte[3].length; }',
            'static native int 외부(); public static int 시작() { return 외부(); }',
            'int ajutuu; public static int 시작() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.akompiraajaa_eejeejetülein('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.anaajaalee_ajutuu / 'native'
        출력.write_bytes(b'original-output')
        self.akompiraajaa_eejeejetülein('public class 시험 { public static int 시작() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.akompiraajaa_eejeejetülein('public class 시험 { public static int 시작() { return 37; } }')
        self.assertEqual((self.anaajaalee_ajutuu / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.anaajaalee_ajutuu / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.akompiraajaa_eejeejetülein('public class 시험 { public static int 시작() { return ka_yataayakalü.실행권한(); } }',
                    {'ka_yataayakalü': 'public class ka_yataayakalü { public static native int 실행권한(); }'}, 대상='user')
        atijaaya = (self.anaajaalee_ajutuu / 'native').read_bytes()
        self.assertEqual(atijaaya[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', atijaaya, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.anaajaalee_ajutuu / 'native')]))
        # ka_yataayakalü ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.akompiraajaa_eejeejetülein('public class 시험 { public static int 시작() { return serulaalü_ajutuu.포트읽기(1); } }',
                    {'serulaalü_ajutuu': 'public class serulaalü_ajutuu { public static native int 포트읽기(int ajutuu); }'}, 성공=False, 대상='user')

    def test_내보내기검증(self):
        eejeejetülein = 'public class 시험 { public static int 시작() { return 0; } static int 호출(int ajutuu) { return ajutuu; } }'
        self.akompiraajaa_eejeejetülein(eejeejetülein, 대상='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.anaajaalee_ajutuu / 'native')]))
        self.akompiraajaa_eejeejetülein(eejeejetülein, 성공=False, 내보냄='bad;name=시험.호출')
        self.akompiraajaa_eejeejetülein(eejeejetülein, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
