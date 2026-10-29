"""нақты_деректер ELF орындау_пәрмен + OpenJDK НӘТИЖЕ 대조. 임시 시험 자료만 생성한다."""
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
        self.каталог_мән = Path(self.임시.name)

    def құрастыру_көз(self, Неден, қосу_енгізу=None, 성공=True, мақсатты_мән='linux', 내보냄=None):
        жол_Тізім_4d1a5003 = []
        for Аты, мазмұн_мән in dict({'시험': Неден}, **(қосу_енгізу or {})).items():
            Жол_2 = self.каталог_мән / (Аты + '.java')
            Жол_2.write_text(мазмұн_мән, encoding='utf-8')
            жол_Тізім_4d1a5003.append(str(Жол_2))
        Команда = [sys.executable, str(컴파일러), '--target', мақсатты_мән, '--entry', '시험.Орындау_2', '-o', str(self.каталог_мән / 'native')]
        if 내보냄 is not None: Команда += ['--export', 내보냄]
        НӘТИЖЕ = subprocess.run(Команда + жол_Тізім_4d1a5003,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(НӘТИЖЕ.returncode, 0, НӘТИЖЕ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(НӘТИЖЕ.returncode, 0)
            self.assertIn('құрастыру_көз Қате'.encode(), НӘТИЖЕ.stderr)
        return НӘТИЖЕ

    def 실행결과(self):
        return subprocess.run([str(self.каталог_мән / 'native')], timeout=5).returncode

    def 자바대조(self, Неден, қосу_енгізу=None):
        self.құрастыру_көз(Неден, қосу_енгізу)
        (self.каталог_мән / 'орналастыру.java').write_text(
            'public class орналастыру { public static void main(String[] Аргументтер) { System.exit(시험.Орындау_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.каталог_мән)] +
                       [str(Жол_2) for Жол_2 in self.каталог_мән.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.каталог_мән), 'орналастыру'], timeout=5).returncode
        нақты_деректер = self.실행결과()
        self.assertGreaterEqual(нақты_деректер, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 тексеру)')
        self.assertEqual(нақты_деректер, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Орындау_2() {
                int 합 = 7;
                int мән = 12345;
                for (int индекс = -65; индекс <= 65; индекс++) {
                    мән = мән * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(мән, индекс);
                    합 += (byte)мән + (short)мән + (char)мән;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] мән = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Орындау_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < мән.length; 가++)
                    for (int 나 = 1; 나 < мән.length; 나++)
                        합 = 합 * 31 + мән[가] / мән[나] + мән[가] % мән[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] жасау_енгізу(int Өлшемі) { return new int[Өлшемі]; }
            public static int Орындау_2() {
                int[] 가 = жасау_енгізу(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int мән = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return мән + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int мән = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Орындау_2() { return 계산(1, 2, 3, 4, мән) + 보조.Оқу(); }
        }''', {'보조': '''public class 보조 {
            static int мән = 3;
            static int 초기값() { return ++мән; }
            static int Оқу() { return мән; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int мән = 보조.Оқу() + 1;
            public static int Орындау_2() { return мән * 10 + 보조.Оқу(); }
        }''', {'보조': '''public class 보조 {
            static int мән = 시험.мән + 2;
            static int Оқу() { return мән; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Мәтін = "한글\\u0000😀";
            public static int Орындау_2() {
                if (Мәтін != "한글\\u0000😀") return 99;
                return (Мәтін.length() + Мәтін.charAt(2) + Мәтін.charAt(3) + Мәтін.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int факториал(int мән) { return мән <= 1 ? 1 : мән * факториал(мән - 1); }
            static int 연속(int мән) {
                switch (мән) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int мән) {
                switch (мән) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Орындау_2() { return (факториал(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        мәлімдеме = '\n'.join('int мән{} = {};'.format(индекс, индекс) for индекс in range(270))
        덧셈 = '+'.join('мән{}'.format(индекс) for индекс in range(270))
        self.자바대조('public class 시험 { public static int Орындау_2() {' + мәлімдеме +
                    'мән_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] мән = null; return мән.length;', 102),
            ('int[] мән = new int[1]; return мән[1];', 103),
            ('int[] мән = new int[1]; мән[-1] = 3; return 0;', 103),
            ('int мән = -1; return new int[мән].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for негізгі_мәтін_мән, 기대 in 경우들:
            with self.subTest(негізгі_мәтін_мән=негізгі_мәтін_мән):
                self.құрастыру_көз('public class 시험 { public static int Орындау_2() { ' + негізгі_мәтін_мән + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long мән; public static int Орындау_2() { return 0; }',
            'public static int Орындау_2() { Object мән = new Object(); return 0; }',
            'public static int Орындау_2() { System.out.println("hello"); return 0; }',
            'public static int Орындау_2() { try { return 1; } catch (Exception Қате) { return 2; } }',
            'public static synchronized int Орындау_2() { return 0; }',
            'public static int Орындау_2() { return new byte[3].length; }',
            'static native int сыртқы_мән(); public static int Орындау_2() { return сыртқы_мән(); }',
            'int мән; public static int Орындау_2() { return 0; }',
        ]
        for негізгі_мәтін_мән in 경우들:
            with self.subTest(негізгі_мәтін_мән=негізгі_мәтін_мән):
                self.құрастыру_көз('public class 시험 { ' + негізгі_мәтін_мән + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Шығысы = self.каталог_мән / 'native'
        Шығысы.write_bytes(b'original-output')
        self.құрастыру_көз('public class 시험 { public static int Орындау_2() { return missing; } }', 성공=False)
        self.assertEqual(Шығысы.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.құрастыру_көз('public class 시험 { public static int Орындау_2() { return 37; } }')
        self.assertEqual((self.каталог_мән / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Іздеу_кесте = subprocess.check_output(['readelf', '-l', str(self.каталог_мән / 'native')])
        self.assertNotIn(b'INTERP', Іздеу_кесте)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.құрастыру_көз('public class 시험 { public static int Орындау_2() { return пайдаланушы.실행권한(); } }',
                    {'пайдаланушы': 'public class пайдаланушы { public static native int 실행권한(); }'}, мақсатты_мән='user')
        деректер = (self.каталог_мән / 'native').read_bytes()
        self.assertEqual(деректер[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', деректер, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.каталог_мән / 'native')]))
        # пайдаланушы ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.құрастыру_көз('public class 시험 { public static int Орындау_2() { return құрылғы_мән.포트읽기(1); } }',
                    {'құрылғы_мән': 'public class құрылғы_мән { public static native int 포트읽기(int мән); }'}, 성공=False, мақсатты_мән='user')

    def test_내보내기검증(self):
        Неден = 'public class 시험 { public static int Орындау_2() { return 0; } static int 호출(int мән) { return мән; } }'
        self.құрастыру_көз(Неден, мақсатты_мән='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.каталог_мән / 'native')]))
        self.құрастыру_көз(Неден, 성공=False, 내보냄='bad;name=시험.호출')
        self.құрастыру_көз(Неден, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
