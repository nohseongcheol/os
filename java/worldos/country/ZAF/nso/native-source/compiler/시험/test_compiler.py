"""kgonthe_data ELF phethagatša_taelo + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.lelokelelo_boleng = Path(self.임시.name)

    def aga_mohlodi(self, mohlodi, 추가=None, 성공=True, nepo='linux', 내보냄=None):
        tsela_Lenaneo = []
        for Leina, Diteng_boleng in dict({'시험': mohlodi}, **(추가 or {})).items():
            Tsejana = self.lelokelelo_boleng / (Leina + '.java')
            Tsejana.write_text(Diteng_boleng, encoding='utf-8')
            tsela_Lenaneo.append(str(Tsejana))
        Taelo = [sys.executable, str(컴파일러), '--target', nepo, '--entry', '시험.Diriša', '-o', str(self.lelokelelo_boleng / 'native')]
        if 내보냄 is not None: Taelo += ['--export', 내보냄]
        결과 = subprocess.run(Taelo + tsela_Lenaneo,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('aga_mohlodi Phošo'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.lelokelelo_boleng / 'native')], timeout=5).returncode

    def 자바대조(self, mohlodi, 추가=None):
        self.aga_mohlodi(mohlodi, 추가)
        (self.lelokelelo_boleng / 'go_nea_ditirelo.java').write_text(
            'public class go_nea_ditirelo { public static void main(String[] 인수) { System.exit(시험.Diriša()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.lelokelelo_boleng)] +
                       [str(Tsejana) for Tsejana in self.lelokelelo_boleng.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.lelokelelo_boleng), 'go_nea_ditirelo'], timeout=5).returncode
        kgonthe_data = self.실행결과()
        self.assertGreaterEqual(kgonthe_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 kgonthiša)')
        self.assertEqual(kgonthe_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Diriša() {
                int 합 = 7;
                int boleng = 12345;
                for (int lokela = -65; lokela <= 65; lokela++) {
                    boleng = boleng * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(boleng, lokela);
                    합 += (byte)boleng + (short)boleng + (char)boleng;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] boleng = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Diriša() {
                int 합 = 13;
                for (int 가 = 0; 가 < boleng.length; 가++)
                    for (int 나 = 1; 나 < boleng.length; 나++)
                        합 = 합 * 31 + boleng[가] / boleng[나] + boleng[가] % boleng[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int Bogolo) { return new int[Bogolo]; }
            public static int Diriša() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] hloka_selo_selo = new int[0];
                if (가 != 나 || 가 == null || hloka_selo_selo.length != 0 || 가[7] != 0) return 99;
                int boleng = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return boleng + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int boleng = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Diriša() { return 계산(1, 2, 3, 4, boleng) + 보조.Bala(); }
        }''', {'보조': '''public class 보조 {
            static int boleng = 3;
            static int 초기값() { return ++boleng; }
            static int Bala() { return boleng; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int boleng = 보조.Bala() + 1;
            public static int Diriša() { return boleng * 10 + 보조.Bala(); }
        }''', {'보조': '''public class 보조 {
            static int boleng = 시험.boleng + 2;
            static int Bala() { return boleng; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Sengwalwa = "한글\\u0000😀";
            public static int Diriša() {
                if (Sengwalwa != "한글\\u0000😀") return 99;
                return (Sengwalwa.length() + Sengwalwa.charAt(2) + Sengwalwa.charAt(3) + Sengwalwa.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ya_dintlha(int boleng) { return boleng <= 1 ? 1 : boleng * ya_dintlha(boleng - 1); }
            static int 연속(int boleng) {
                switch (boleng) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int boleng) {
                switch (boleng) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Diriša() { return (ya_dintlha(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int boleng{} = {};'.format(lokela, lokela) for lokela in range(270))
        덧셈 = '+'.join('boleng{}'.format(lokela) for lokela in range(270))
        self.자바대조('public class 시험 { public static int Diriša() {' + 선언 +
                    'boleng_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] boleng = null; return boleng.length;', 102),
            ('int[] boleng = new int[1]; return boleng[1];', 103),
            ('int[] boleng = new int[1]; boleng[-1] = 3; return 0;', 103),
            ('int boleng = -1; return new int[boleng].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.aga_mohlodi('public class 시험 { public static int Diriša() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long boleng; public static int Diriša() { return 0; }',
            'public static int Diriša() { Object boleng = new Object(); return 0; }',
            'public static int Diriša() { System.out.println("hello"); return 0; }',
            'public static int Diriša() { try { return 1; } catch (Exception Phošo) { return 2; } }',
            'public static synchronized int Diriša() { return 0; }',
            'public static int Diriša() { return new byte[3].length; }',
            'static native int 외부(); public static int Diriša() { return 외부(); }',
            'int boleng; public static int Diriša() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.aga_mohlodi('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.lelokelelo_boleng / 'native'
        출력.write_bytes(b'original-output')
        self.aga_mohlodi('public class 시험 { public static int Diriša() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.aga_mohlodi('public class 시험 { public static int Diriša() { return 37; } }')
        self.assertEqual((self.lelokelelo_boleng / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.lelokelelo_boleng / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.aga_mohlodi('public class 시험 { public static int Diriša() { return mošomiši.실행권한(); } }',
                    {'mošomiši': 'public class mošomiši { public static native int 실행권한(); }'}, nepo='user')
        data = (self.lelokelelo_boleng / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.lelokelelo_boleng / 'native')]))
        # mošomiši ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.aga_mohlodi('public class 시험 { public static int Diriša() { return sedirišwa_boleng.포트읽기(1); } }',
                    {'sedirišwa_boleng': 'public class sedirišwa_boleng { public static native int 포트읽기(int boleng); }'}, 성공=False, nepo='user')

    def test_내보내기검증(self):
        mohlodi = 'public class 시험 { public static int Diriša() { return 0; } static int 호출(int boleng) { return boleng; } }'
        self.aga_mohlodi(mohlodi, nepo='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.lelokelelo_boleng / 'native')]))
        self.aga_mohlodi(mohlodi, 성공=False, 내보냄='bad;name=시험.호출')
        self.aga_mohlodi(mohlodi, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
