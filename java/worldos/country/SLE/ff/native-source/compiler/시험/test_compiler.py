"""laatii_keɓe ELF 실행 + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.mooftordu_njaru = Path(self.임시.name)

    def tafde_sewnde(self, sewnde, 추가=None, 성공=True, faandaare='linux', 내보냄=None):
        laawol_Doggol = []
        for innde, loowdi_njaru in dict({'시험': sewnde}, **(추가 or {})).items():
            laawol = self.mooftordu_njaru / (innde + '.java')
            laawol.write_text(loowdi_njaru, encoding='utf-8')
            laawol_Doggol.append(str(laawol))
        ginol = [sys.executable, str(컴파일러), '--target', faandaare, '--entry', '시험.huutoraade', '-o', str(self.mooftordu_njaru / 'native')]
        if 내보냄 is not None: ginol += ['--export', 내보냄]
        결과 = subprocess.run(ginol + laawol_Doggol,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('tafde_sewnde juumre'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.mooftordu_njaru / 'native')], timeout=5).returncode

    def 자바대조(self, sewnde, 추가=None):
        self.tafde_sewnde(sewnde, 추가)
        (self.mooftordu_njaru / 'njaatigi.java').write_text(
            'public class njaatigi { public static void main(String[] 인수) { System.exit(시험.huutoraade()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.mooftordu_njaru)] +
                       [str(laawol) for laawol in self.mooftordu_njaru.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.mooftordu_njaru), 'njaatigi'], timeout=5).returncode
        laatii_keɓe = self.실행결과()
        self.assertGreaterEqual(laatii_keɓe, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ƴeewtaade)')
        self.assertEqual(laatii_keɓe, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int huutoraade() {
                int 합 = 7;
                int njaru = 12345;
                for (int joopirdu = -65; joopirdu <= 65; joopirdu++) {
                    njaru = njaru * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(njaru, joopirdu);
                    합 += (byte)njaru + (short)njaru + (char)njaru;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] njaru = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int huutoraade() {
                int 합 = 13;
                for (int 가 = 0; 가 < njaru.length; 가++)
                    for (int 나 = 1; 나 < njaru.length; 나++)
                        합 = 합 * 31 + njaru[가] / njaru[나] + njaru[가] % njaru[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int waylude_etannde) { return new int[waylude_etannde]; }
            public static int huutoraade() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int njaru = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return njaru + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int njaru = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int huutoraade() { return 계산(1, 2, 3, 4, njaru) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int njaru = 3;
            static int 초기값() { return ++njaru; }
            static int 읽기() { return njaru; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int njaru = 보조.읽기() + 1;
            public static int huutoraade() { return njaru * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int njaru = 시험.njaru + 2;
            static int 읽기() { return njaru; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String binndi = "한글\\u0000😀";
            public static int huutoraade() {
                if (binndi != "한글\\u0000😀") return 99;
                return (binndi.length() + binndi.charAt(2) + binndi.charAt(3) + binndi.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int njaru) { return njaru <= 1 ? 1 : njaru * 계승(njaru - 1); }
            static int 연속(int njaru) {
                switch (njaru) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int njaru) {
                switch (njaru) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int huutoraade() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int njaru{} = {};'.format(joopirdu, joopirdu) for joopirdu in range(270))
        덧셈 = '+'.join('njaru{}'.format(joopirdu) for joopirdu in range(270))
        self.자바대조('public class 시험 { public static int huutoraade() {' + 선언 +
                    'njaru_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] njaru = null; return njaru.length;', 102),
            ('int[] njaru = new int[1]; return njaru[1];', 103),
            ('int[] njaru = new int[1]; njaru[-1] = 3; return 0;', 103),
            ('int njaru = -1; return new int[njaru].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.tafde_sewnde('public class 시험 { public static int huutoraade() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long njaru; public static int huutoraade() { return 0; }',
            'public static int huutoraade() { Object njaru = new Object(); return 0; }',
            'public static int huutoraade() { System.out.println("hello"); return 0; }',
            'public static int huutoraade() { try { return 1; } catch (Exception juumre) { return 2; } }',
            'public static synchronized int huutoraade() { return 0; }',
            'public static int huutoraade() { return new byte[3].length; }',
            'static native int 외부(); public static int huutoraade() { return 외부(); }',
            'int njaru; public static int huutoraade() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.tafde_sewnde('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.mooftordu_njaru / 'native'
        출력.write_bytes(b'original-output')
        self.tafde_sewnde('public class 시험 { public static int huutoraade() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.tafde_sewnde('public class 시험 { public static int huutoraade() { return 37; } }')
        self.assertEqual((self.mooftordu_njaru / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.mooftordu_njaru / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.tafde_sewnde('public class 시험 { public static int huutoraade() { return kuutoro.실행권한(); } }',
                    {'kuutoro': 'public class kuutoro { public static native int 실행권한(); }'}, faandaare='user')
        keɓe = (self.mooftordu_njaru / 'native').read_bytes()
        self.assertEqual(keɓe[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', keɓe, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.mooftordu_njaru / 'native')]))
        # kuutoro ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.tafde_sewnde('public class 시험 { public static int huutoraade() { return kaɓirgal_njaru.포트읽기(1); } }',
                    {'kaɓirgal_njaru': 'public class kaɓirgal_njaru { public static native int 포트읽기(int njaru); }'}, 성공=False, faandaare='user')

    def test_내보내기검증(self):
        sewnde = 'public class 시험 { public static int huutoraade() { return 0; } static int 호출(int njaru) { return njaru; } }'
        self.tafde_sewnde(sewnde, faandaare='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.mooftordu_njaru / 'native')]))
        self.tafde_sewnde(sewnde, 성공=False, 내보냄='bad;name=시험.호출')
        self.tafde_sewnde(sewnde, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
