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
        self.폴더 = Path(self.임시.name)

    def 컴파일(self, Sourdant, 추가=None, 성공=True, 대상='linux', 내보냄=None):
        경로들 = []
        for No, 내용 in dict({'시험': Sourdant}, **(추가 or {})).items():
            Tchimin = self.폴더 / (No + '.java')
            Tchimin.write_text(내용, encoding='utf-8')
            경로들.append(str(Tchimin))
        Comande = [sys.executable, str(컴파일러), '--target', 대상, '--entry', '시험.Enonder_2', '-o', str(self.폴더 / 'native')]
        if 내보냄 is not None: Comande += ['--export', 내보냄]
        결과 = subprocess.run(Comande + 경로들,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('컴파일 AROKE'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.폴더 / 'native')], timeout=5).returncode

    def 자바대조(self, Sourdant, 추가=None):
        self.컴파일(Sourdant, 추가)
        (self.폴더 / '호스트.java').write_text(
            'public class 호스트 { public static void main(String[] Årgumints) { System.exit(시험.Enonder_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.폴더)] +
                       [str(Tchimin) for Tchimin in self.폴더.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.폴더), '호스트'], timeout=5).returncode
        실제 = self.실행결과()
        self.assertGreaterEqual(실제, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 확인)')
        self.assertEqual(실제, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Enonder_2() {
                int 합 = 7;
                int 값 = 12345;
                for (int 번호 = -65; 번호 <= 65; 번호++) {
                    값 = 값 * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(값, 번호);
                    합 += (byte)값 + (short)값 + (char)값;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] 값 = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Enonder_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < 값.length; 가++)
                    for (int 나 = 1; 나 < 값.length; 나++)
                        합 = 합 * 31 + 값[가] / 값[나] + 값[가] % 값[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int Grandeu) { return new int[Grandeu]; }
            public static int Enonder_2() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int 값 = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return 값 + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int 값 = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Enonder_2() { return 계산(1, 2, 3, 4, 값) + 보조.Lére(); }
        }''', {'보조': '''public class 보조 {
            static int 값 = 3;
            static int 초기값() { return ++값; }
            static int Lére() { return 값; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int 값 = 보조.Lére() + 1;
            public static int Enonder_2() { return 값 * 10 + 보조.Lére(); }
        }''', {'보조': '''public class 보조 {
            static int 값 = 시험.값 + 2;
            static int Lére() { return 값; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tecse = "한글\\u0000😀";
            public static int Enonder_2() {
                if (Tecse != "한글\\u0000😀") return 99;
                return (Tecse.length() + Tecse.charAt(2) + Tecse.charAt(3) + Tecse.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int 값) { return 값 <= 1 ? 1 : 값 * 계승(값 - 1); }
            static int 연속(int 값) {
                switch (값) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int 값) {
                switch (값) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Enonder_2() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int 값{} = {};'.format(번호, 번호) for 번호 in range(270))
        덧셈 = '+'.join('값{}'.format(번호) for 번호 in range(270))
        self.자바대조('public class 시험 { public static int Enonder_2() {' + 선언 +
                    '값269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] 값 = null; return 값.length;', 102),
            ('int[] 값 = new int[1]; return 값[1];', 103),
            ('int[] 값 = new int[1]; 값[-1] = 3; return 0;', 103),
            ('int 값 = -1; return new int[값].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.컴파일('public class 시험 { public static int Enonder_2() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long 값; public static int Enonder_2() { return 0; }',
            'public static int Enonder_2() { Object 값 = new Object(); return 0; }',
            'public static int Enonder_2() { System.out.println("hello"); return 0; }',
            'public static int Enonder_2() { try { return 1; } catch (Exception AROKE) { return 2; } }',
            'public static synchronized int Enonder_2() { return 0; }',
            'public static int Enonder_2() { return new byte[3].length; }',
            'static native int 외부(); public static int Enonder_2() { return 외부(); }',
            'int 값; public static int Enonder_2() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.컴파일('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.폴더 / 'native'
        출력.write_bytes(b'original-output')
        self.컴파일('public class 시험 { public static int Enonder_2() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.컴파일('public class 시험 { public static int Enonder_2() { return 37; } }')
        self.assertEqual((self.폴더 / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.폴더 / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.컴파일('public class 시험 { public static int Enonder_2() { return 사용자.실행권한(); } }',
                    {'사용자': 'public class 사용자 { public static native int 실행권한(); }'}, 대상='user')
        자료 = (self.폴더 / 'native').read_bytes()
        self.assertEqual(자료[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', 자료, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.폴더 / 'native')]))
        # 사용자 ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.컴파일('public class 시험 { public static int Enonder_2() { return 장치.포트읽기(1); } }',
                    {'장치': 'public class 장치 { public static native int 포트읽기(int 값); }'}, 성공=False, 대상='user')

    def test_내보내기검증(self):
        Sourdant = 'public class 시험 { public static int Enonder_2() { return 0; } static int 호출(int 값) { return 값; } }'
        self.컴파일(Sourdant, 대상='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.폴더 / 'native')]))
        self.컴파일(Sourdant, 성공=False, 내보냄='bad;name=시험.호출')
        self.컴파일(Sourdant, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
