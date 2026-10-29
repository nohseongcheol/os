"""фактычны_дадзеныя ELF выканаць_каманда + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.каталог_значэнне = Path(self.임시.name)

    def будаваць_крыніца(self, КРЫНІЦА, 추가=None, 성공=True, мэтавы_паказчык='linux', 내보냄=None):
        шлях_Спіс = []
        for Назва, кантэнт_значэнне in dict({'시험': КРЫНІЦА}, **(추가 or {})).items():
            ШЛЯХ = self.каталог_значэнне / (Назва + '.java')
            ШЛЯХ.write_text(кантэнт_значэнне, encoding='utf-8')
            шлях_Спіс.append(str(ШЛЯХ))
        Загад = [sys.executable, str(컴파일러), '--target', мэтавы_паказчык, '--entry', '시험.Выканаць', '-o', str(self.каталог_значэнне / 'native')]
        if 내보냄 is not None: Загад += ['--export', 내보냄]
        결과 = subprocess.run(Загад + шлях_Спіс,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('будаваць_крыніца ПАМЫЛКА'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.каталог_значэнне / 'native')], timeout=5).returncode

    def 자바대조(self, КРЫНІЦА, 추가=None):
        self.будаваць_крыніца(КРЫНІЦА, 추가)
        (self.каталог_значэнне / 'вузел.java').write_text(
            'public class вузел { public static void main(String[] 인수) { System.exit(시험.Выканаць()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.каталог_значэнне)] +
                       [str(ШЛЯХ) for ШЛЯХ in self.каталог_значэнне.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.каталог_значэнне), 'вузел'], timeout=5).returncode
        фактычны_дадзеныя = self.실행결과()
        self.assertGreaterEqual(фактычны_дадзеныя, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 праверыць)')
        self.assertEqual(фактычны_дадзеныя, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Выканаць() {
                int 합 = 7;
                int значэнне = 12345;
                for (int індэкс = -65; індэкс <= 65; індэкс++) {
                    значэнне = значэнне * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(значэнне, індэкс);
                    합 += (byte)значэнне + (short)значэнне + (char)значэнне;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] значэнне = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Выканаць() {
                int 합 = 13;
                for (int 가 = 0; 가 < значэнне.length; 가++)
                    for (int 나 = 1; 나 < значэнне.length; 나++)
                        합 = 합 * 31 + значэнне[가] / значэнне[나] + значэнне[가] % значэнне[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] стварыць_увядзенне(int Памер) { return new int[Памер]; }
            public static int Выканаць() {
                int[] 가 = стварыць_увядзенне(8); int[] 나 = 가; int[] нулявая_аб_ект = new int[0];
                if (가 != 나 || 가 == null || нулявая_аб_ект.length != 0 || 가[7] != 0) return 99;
                int значэнне = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return значэнне + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int значэнне = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Выканаць() { return 계산(1, 2, 3, 4, значэнне) + 보조.Чытанне(); }
        }''', {'보조': '''public class 보조 {
            static int значэнне = 3;
            static int 초기값() { return ++значэнне; }
            static int Чытанне() { return значэнне; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int значэнне = 보조.Чытанне() + 1;
            public static int Выканаць() { return значэнне * 10 + 보조.Чытанне(); }
        }''', {'보조': '''public class 보조 {
            static int значэнне = 시험.значэнне + 2;
            static int Чытанне() { return значэнне; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Тэкст = "한글\\u0000😀";
            public static int Выканаць() {
                if (Тэкст != "한글\\u0000😀") return 99;
                return (Тэкст.length() + Тэкст.charAt(2) + Тэкст.charAt(3) + Тэкст.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int фактарыял(int значэнне) { return значэнне <= 1 ? 1 : значэнне * фактарыял(значэнне - 1); }
            static int 연속(int значэнне) {
                switch (значэнне) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int значэнне) {
                switch (значэнне) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Выканаць() { return (фактарыял(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        абвяшчэнне = '\n'.join('int значэнне{} = {};'.format(індэкс, індэкс) for індэкс in range(270))
        덧셈 = '+'.join('значэнне{}'.format(індэкс) for індэкс in range(270))
        self.자바대조('public class 시험 { public static int Выканаць() {' + абвяшчэнне +
                    'значэнне_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] значэнне = null; return значэнне.length;', 102),
            ('int[] значэнне = new int[1]; return значэнне[1];', 103),
            ('int[] значэнне = new int[1]; значэнне[-1] = 3; return 0;', 103),
            ('int значэнне = -1; return new int[значэнне].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for тэкст_паведамлення_значэнне, 기대 in 경우들:
            with self.subTest(тэкст_паведамлення_значэнне=тэкст_паведамлення_значэнне):
                self.будаваць_крыніца('public class 시험 { public static int Выканаць() { ' + тэкст_паведамлення_значэнне + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long значэнне; public static int Выканаць() { return 0; }',
            'public static int Выканаць() { Object значэнне = new Object(); return 0; }',
            'public static int Выканаць() { System.out.println("hello"); return 0; }',
            'public static int Выканаць() { try { return 1; } catch (Exception ПАМЫЛКА) { return 2; } }',
            'public static synchronized int Выканаць() { return 0; }',
            'public static int Выканаць() { return new byte[3].length; }',
            'static native int 외부(); public static int Выканаць() { return 외부(); }',
            'int значэнне; public static int Выканаць() { return 0; }',
        ]
        for тэкст_паведамлення_значэнне in 경우들:
            with self.subTest(тэкст_паведамлення_значэнне=тэкст_паведамлення_значэнне):
                self.будаваць_крыніца('public class 시험 { ' + тэкст_паведамлення_значэнне + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Выхад = self.каталог_значэнне / 'native'
        Выхад.write_bytes(b'original-output')
        self.будаваць_крыніца('public class 시험 { public static int Выканаць() { return missing; } }', 성공=False)
        self.assertEqual(Выхад.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.будаваць_крыніца('public class 시험 { public static int Выканаць() { return 37; } }')
        self.assertEqual((self.каталог_значэнне / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.каталог_значэнне / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.будаваць_крыніца('public class 시험 { public static int Выканаць() { return карыстальнік.실행권한(); } }',
                    {'карыстальнік': 'public class карыстальнік { public static native int 실행권한(); }'}, мэтавы_паказчык='user')
        дадзеныя = (self.каталог_значэнне / 'native').read_bytes()
        self.assertEqual(дадзеныя[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', дадзеныя, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.каталог_значэнне / 'native')]))
        # карыстальнік ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.будаваць_крыніца('public class 시험 { public static int Выканаць() { return прылада_значэнне.포트읽기(1); } }',
                    {'прылада_значэнне': 'public class прылада_значэнне { public static native int 포트읽기(int значэнне); }'}, 성공=False, мэтавы_паказчык='user')

    def test_내보내기검증(self):
        КРЫНІЦА = 'public class 시험 { public static int Выканаць() { return 0; } static int 호출(int значэнне) { return значэнне; } }'
        self.будаваць_крыніца(КРЫНІЦА, мэтавы_паказчык='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.каталог_значэнне / 'native')]))
        self.будаваць_крыніца(КРЫНІЦА, 성공=False, 내보냄='bad;name=시험.호출')
        self.будаваць_крыніца(КРЫНІЦА, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
