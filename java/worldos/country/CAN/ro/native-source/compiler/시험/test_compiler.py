"""real_date ELF executa_comandă + OpenJDK KR 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

compilator = Path(__file__).resolve().parents[1] / 'compilator.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Director_VALUE = Path(self.임시.name)

    def compilare_sursă(self, SURSĂ, adăuga_intrare=None, 성공=True, țintă='linux', 내보냄=None):
        cale_Listă = []
        for Nume, Conținut_VALUE in dict({'시험': SURSĂ}, **(adăuga_intrare or {})).items():
            Cale = self.Director_VALUE / (Nume + '.java')
            Cale.write_text(Conținut_VALUE, encoding='utf-8')
            cale_Listă.append(str(Cale))
        Comandă = [sys.executable, str(compilator), '--target', țintă, '--entry', '시험.Pornește', '-o', str(self.Director_VALUE / 'native')]
        if 내보냄 is not None: Comandă += ['--export', 내보냄]
        KR = subprocess.run(Comandă + cale_Listă,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(KR.returncode, 0, KR.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(KR.returncode, 0)
            self.assertIn('compilare_sursă eroare'.encode(), KR.stderr)
        return KR

    def executare_KR(self):
        return subprocess.run([str(self.Director_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, SURSĂ, adăuga_intrare=None):
        self.compilare_sursă(SURSĂ, adăuga_intrare)
        (self.Director_VALUE / 'gazdă.java').write_text(
            'public class gazdă { public static void main(String[] Argumente) { System.exit(시험.Pornește()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Director_VALUE)] +
                       [str(Cale) for Cale in self.Director_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Director_VALUE), 'gazdă'], timeout=5).returncode
        real_date = self.executare_KR()
        self.assertGreaterEqual(real_date, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verifica)')
        self.assertEqual(real_date, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SECOND_operand) {
                return ((가 + SECOND_operand) ^ (가 - SECOND_operand) ^ (가 * SECOND_operand) ^ (가 & SECOND_operand) ^ (가 | SECOND_operand))
                    + (가 << SECOND_operand) + (가 >> SECOND_operand) + (가 >>> SECOND_operand);
            }
            public static int Pornește() {
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
            public static int Pornește() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operand = 1; SECOND_operand < VALUE.length; SECOND_operand++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operand] + VALUE[가] % VALUE[SECOND_operand];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] crea_intrare(int Mărime) { return new int[Mărime]; }
            public static int Pornește() {
                int[] 가 = crea_intrare(8); int[] SECOND_operand = 가; int[] 빈것 = new int[0];
                if (가 != SECOND_operand || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + SECOND_operand[2] + SECOND_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int SECOND_operand, int 다, int 라, int 마) {
                return 가 + SECOND_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Pornește() { return 계산(1, 2, 3, 4, VALUE) + 보조.Citire(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Citire() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Citire() + 1;
            public static int Pornește() { return VALUE * 10 + 보조.Citire(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Citire() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int Pornește() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int factorial(int VALUE) { return VALUE <= 1 ? 1 : VALUE * factorial(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Pornește() { return (factorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        declarație = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Pornește() {' + declarație +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int zero_operand = 0; return 1 / zero_operand;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for corp_VALUE, 기대 in 경우들:
            with self.subTest(corp_VALUE=corp_VALUE):
                self.compilare_sursă('public class 시험 { public static int Pornește() { ' + corp_VALUE + ' } }')
                self.assertEqual(self.executare_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Pornește() { return 0; }',
            'public static int Pornește() { Object VALUE = new Object(); return 0; }',
            'public static int Pornește() { System.out.println("hello"); return 0; }',
            'public static int Pornește() { try { return 1; } catch (Exception eroare) { return 2; } }',
            'public static synchronized int Pornește() { return 0; }',
            'public static int Pornește() { return new byte[3].length; }',
            'static native int extern_VALUE(); public static int Pornește() { return extern_VALUE(); }',
            'int VALUE; public static int Pornește() { return 0; }',
        ]
        for corp_VALUE in 경우들:
            with self.subTest(corp_VALUE=corp_VALUE):
                self.compilare_sursă('public class 시험 { ' + corp_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Rezultat = self.Director_VALUE / 'native'
        Rezultat.write_bytes(b'original-output')
        self.compilare_sursă('public class 시험 { public static int Pornește() { return missing; } }', 성공=False)
        self.assertEqual(Rezultat.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.compilare_sursă('public class 시험 { public static int Pornește() { return 37; } }')
        self.assertEqual((self.Director_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        tabel_de_căutare = subprocess.check_output(['readelf', '-l', str(self.Director_VALUE / 'native')])
        self.assertNotIn(b'INTERP', tabel_de_căutare)
        self.assertEqual(self.executare_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.compilare_sursă('public class 시험 { public static int Pornește() { return utilizator.executare_permisiune(); } }',
                    {'utilizator': 'public class utilizator { public static native int executare_permisiune(); }'}, țintă='user')
        date = (self.Director_VALUE / 'native').read_bytes()
        self.assertEqual(date[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', date, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Director_VALUE / 'native')]))
        # utilizator ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compilare_sursă('public class 시험 { public static int Pornește() { return mobil_VALUE.포트읽기(1); } }',
                    {'mobil_VALUE': 'public class mobil_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, țintă='user')

    def test_내보내기검증(self):
        SURSĂ = 'public class 시험 { public static int Pornește() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.compilare_sursă(SURSĂ, țintă='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Director_VALUE / 'native')]))
        self.compilare_sursă(SURSĂ, 성공=False, 내보냄='bad;name=시험.호출')
        self.compilare_sursă(SURSĂ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
