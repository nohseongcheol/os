"""стваран_подаци ELF 실행 + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.директориј_вриједност = Path(self.임시.name)

    def направити_извор(self, извор, 추가=None, 성공=True, циљ='linux', 내보냄=None):
        пут_списак = []
        for назив, Садржај_вриједност in dict({'시험': извор}, **(추가 or {})).items():
            пут = self.директориј_вриједност / (назив + '.java')
            пут.write_text(Садржај_вриједност, encoding='utf-8')
            пут_списак.append(str(пут))
        команда = [sys.executable, str(컴파일러), '--target', циљ, '--entry', '시험.시작', '-o', str(self.директориј_вриједност / 'native')]
        if 내보냄 is not None: команда += ['--export', 내보냄]
        결과 = subprocess.run(команда + пут_списак,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('направити_извор грешка'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.директориј_вриједност / 'native')], timeout=5).returncode

    def 자바대조(self, извор, 추가=None):
        self.направити_извор(извор, 추가)
        (self.директориј_вриједност / 'хост_рачунар.java').write_text(
            'public class хост_рачунар { public static void main(String[] 인수) { System.exit(시험.시작()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.директориј_вриједност)] +
                       [str(пут) for пут in self.директориј_вриједност.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.директориј_вриједност), 'хост_рачунар'], timeout=5).returncode
        стваран_подаци = self.실행결과()
        self.assertGreaterEqual(стваран_подаци, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 потврдити)')
        self.assertEqual(стваран_подаци, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int 시작() {
                int 합 = 7;
                int вриједност = 12345;
                for (int индекс = -65; индекс <= 65; индекс++) {
                    вриједност = вриједност * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(вриједност, индекс);
                    합 += (byte)вриједност + (short)вриједност + (char)вриједност;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] вриједност = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int 시작() {
                int 합 = 13;
                for (int 가 = 0; 가 < вриједност.length; 가++)
                    for (int 나 = 1; 나 < вриједност.length; 나++)
                        합 = 합 * 31 + вриједност[가] / вриједност[나] + вриједност[가] % вриједност[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int подесити_величину) { return new int[подесити_величину]; }
            public static int 시작() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int вриједност = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return вриједност + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int вриједност = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int 시작() { return 계산(1, 2, 3, 4, вриједност) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int вриједност = 3;
            static int 초기값() { return ++вриједност; }
            static int 읽기() { return вриједност; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int вриједност = 보조.읽기() + 1;
            public static int 시작() { return вриједност * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int вриједност = 시험.вриједност + 2;
            static int 읽기() { return вриједност; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String текст = "한글\\u0000😀";
            public static int 시작() {
                if (текст != "한글\\u0000😀") return 99;
                return (текст.length() + текст.charAt(2) + текст.charAt(3) + текст.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int вриједност) { return вриједност <= 1 ? 1 : вриједност * 계승(вриједност - 1); }
            static int 연속(int вриједност) {
                switch (вриједност) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int вриједност) {
                switch (вриједност) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int 시작() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int вриједност{} = {};'.format(индекс, индекс) for индекс in range(270))
        덧셈 = '+'.join('вриједност{}'.format(индекс) for индекс in range(270))
        self.자바대조('public class 시험 { public static int 시작() {' + 선언 +
                    'вриједност_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] вриједност = null; return вриједност.length;', 102),
            ('int[] вриједност = new int[1]; return вриједност[1];', 103),
            ('int[] вриједност = new int[1]; вриједност[-1] = 3; return 0;', 103),
            ('int вриједност = -1; return new int[вриједност].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.направити_извор('public class 시험 { public static int 시작() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long вриједност; public static int 시작() { return 0; }',
            'public static int 시작() { Object вриједност = new Object(); return 0; }',
            'public static int 시작() { System.out.println("hello"); return 0; }',
            'public static int 시작() { try { return 1; } catch (Exception грешка) { return 2; } }',
            'public static synchronized int 시작() { return 0; }',
            'public static int 시작() { return new byte[3].length; }',
            'static native int 외부(); public static int 시작() { return 외부(); }',
            'int вриједност; public static int 시작() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.направити_извор('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.директориј_вриједност / 'native'
        출력.write_bytes(b'original-output')
        self.направити_извор('public class 시험 { public static int 시작() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.направити_извор('public class 시험 { public static int 시작() { return 37; } }')
        self.assertEqual((self.директориј_вриједност / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.директориј_вриједност / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.направити_извор('public class 시험 { public static int 시작() { return корисник.실행권한(); } }',
                    {'корисник': 'public class корисник { public static native int 실행권한(); }'}, циљ='user')
        подаци = (self.директориј_вриједност / 'native').read_bytes()
        self.assertEqual(подаци[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', подаци, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.директориј_вриједност / 'native')]))
        # корисник ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.направити_извор('public class 시험 { public static int 시작() { return уређај_вриједност.포트읽기(1); } }',
                    {'уређај_вриједност': 'public class уређај_вриједност { public static native int 포트읽기(int вриједност); }'}, 성공=False, циљ='user')

    def test_내보내기검증(self):
        извор = 'public class 시험 { public static int 시작() { return 0; } static int 호출(int вриједност) { return вриједност; } }'
        self.направити_извор(извор, циљ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.директориј_вриједност / 'native')]))
        self.направити_извор(извор, 성공=False, 내보냄='bad;name=시험.호출')
        self.направити_извор(извор, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
