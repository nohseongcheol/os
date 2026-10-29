"""aktual_të_dhëna ELF zbatoj_komandë + OpenJDK llogaritje 대조. 임시 시험 자료만 생성한다."""
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
        self.direktori_VALUE = Path(self.임시.name)

    def ndërtoj_burim(self, BURIMI, 추가=None, 성공=True, objektiv='linux', 내보냄=None):
        shteg_Listë = []
        for Emër, Përmbajtje_VALUE in dict({'시험': BURIMI}, **(추가 or {})).items():
            POZICIONI = self.direktori_VALUE / (Emër + '.java')
            POZICIONI.write_text(Përmbajtje_VALUE, encoding='utf-8')
            shteg_Listë.append(str(POZICIONI))
        Komanda = [sys.executable, str(컴파일러), '--target', objektiv, '--entry', '시험.Ekzekuto', '-o', str(self.direktori_VALUE / 'native')]
        if 내보냄 is not None: Komanda += ['--export', 내보냄]
        llogaritje = subprocess.run(Komanda + shteg_Listë,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(llogaritje.returncode, 0, llogaritje.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(llogaritje.returncode, 0)
            self.assertIn('ndërtoj_burim GABIM'.encode(), llogaritje.stderr)
        return llogaritje

    def 실행결과(self):
        return subprocess.run([str(self.direktori_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, BURIMI, 추가=None):
        self.ndërtoj_burim(BURIMI, 추가)
        (self.direktori_VALUE / 'pritës.java').write_text(
            'public class pritës { public static void main(String[] Argumente) { System.exit(시험.Ekzekuto()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.direktori_VALUE)] +
                       [str(POZICIONI) for POZICIONI in self.direktori_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.direktori_VALUE), 'pritës'], timeout=5).returncode
        aktual_të_dhëna = self.실행결과()
        self.assertGreaterEqual(aktual_të_dhëna, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verifikoj)')
        self.assertEqual(aktual_të_dhëna, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Ekzekuto() {
                int SUM_VALUE = 7;
                int VALUE = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    VALUE = VALUE * 1664525 + 1013904223;
                    SUM_VALUE = SUM_VALUE * 31 + 섞기(VALUE, INDEX);
                    SUM_VALUE += (byte)VALUE + (short)VALUE + (char)VALUE;
                }
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] VALUE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Ekzekuto() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int 나 = 1; 나 < VALUE.length; 나++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[나] + VALUE[가] % VALUE[나];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Krijo_futje(int Madhësi) { return new int[Madhësi]; }
            public static int Ekzekuto() {
                int[] 가 = Krijo_futje(8); int[] 나 = 가; int[] bosh_objekt = new int[0];
                if (가 != 나 || 가 == null || bosh_objekt.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Ekzekuto() { return 계산(1, 2, 3, 4, VALUE) + 보조.Leximi(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Leximi() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Leximi() + 1;
            public static int Ekzekuto() { return VALUE * 10 + 보조.Leximi(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Leximi() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Teksti = "한글\\u0000😀";
            public static int Ekzekuto() {
                if (Teksti != "한글\\u0000😀") return 99;
                return (Teksti.length() + Teksti.charAt(2) + Teksti.charAt(3) + Teksti.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktorial(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktorial(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Ekzekuto() { return (faktorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklarata = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Ekzekuto() {' + deklarata +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for trupi_VALUE, 기대 in 경우들:
            with self.subTest(trupi_VALUE=trupi_VALUE):
                self.ndërtoj_burim('public class 시험 { public static int Ekzekuto() { ' + trupi_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Ekzekuto() { return 0; }',
            'public static int Ekzekuto() { Object VALUE = new Object(); return 0; }',
            'public static int Ekzekuto() { System.out.println("hello"); return 0; }',
            'public static int Ekzekuto() { try { return 1; } catch (Exception GABIM) { return 2; } }',
            'public static synchronized int Ekzekuto() { return 0; }',
            'public static int Ekzekuto() { return new byte[3].length; }',
            'static native int 외부(); public static int Ekzekuto() { return 외부(); }',
            'int VALUE; public static int Ekzekuto() { return 0; }',
        ]
        for trupi_VALUE in 경우들:
            with self.subTest(trupi_VALUE=trupi_VALUE):
                self.ndërtoj_burim('public class 시험 { ' + trupi_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.direktori_VALUE / 'native'
        출력.write_bytes(b'original-output')
        self.ndërtoj_burim('public class 시험 { public static int Ekzekuto() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ndërtoj_burim('public class 시험 { public static int Ekzekuto() { return 37; } }')
        self.assertEqual((self.direktori_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_tabelë = subprocess.check_output(['readelf', '-l', str(self.direktori_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_tabelë)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ndërtoj_burim('public class 시험 { public static int Ekzekuto() { return përdorues.실행권한(); } }',
                    {'përdorues': 'public class përdorues { public static native int 실행권한(); }'}, objektiv='user')
        të_dhëna = (self.direktori_VALUE / 'native').read_bytes()
        self.assertEqual(të_dhëna[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', të_dhëna, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.direktori_VALUE / 'native')]))
        # përdorues ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ndërtoj_burim('public class 시험 { public static int Ekzekuto() { return pajisje_VALUE.포트읽기(1); } }',
                    {'pajisje_VALUE': 'public class pajisje_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, objektiv='user')

    def test_내보내기검증(self):
        BURIMI = 'public class 시험 { public static int Ekzekuto() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.ndërtoj_burim(BURIMI, objektiv='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.direktori_VALUE / 'native')]))
        self.ndërtoj_burim(BURIMI, 성공=False, 내보냄='bad;name=시험.호출')
        self.ndërtoj_burim(BURIMI, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
