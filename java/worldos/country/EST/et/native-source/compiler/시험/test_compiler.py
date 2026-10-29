"""tegelik_andmed ELF Täida_käsk + OpenJDK TULEMUS 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilaator = Path(__file__).resolve().parents[1] / 'kompilaator.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.kaust_VALUE = Path(self.임시.name)

    def kompileerima_lähe(self, ALLIKAS, Lisa_kirje=None, 성공=True, siht='linux', 내보냄=None):
        tee_Loend = []
        for Nimi_2, Sisu_VALUE in dict({'시험': ALLIKAS}, **(Lisa_kirje or {})).items():
            RADA = self.kaust_VALUE / (Nimi_2 + '.java')
            RADA.write_text(Sisu_VALUE, encoding='utf-8')
            tee_Loend.append(str(RADA))
        Käsk = [sys.executable, str(kompilaator), '--target', siht, '--entry', '시험.Käivita_2', '-o', str(self.kaust_VALUE / 'native')]
        if 내보냄 is not None: Käsk += ['--export', 내보냄]
        TULEMUS = subprocess.run(Käsk + tee_Loend,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(TULEMUS.returncode, 0, TULEMUS.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(TULEMUS.returncode, 0)
            self.assertIn('kompileerima_lähe VIGA'.encode(), TULEMUS.stderr)
        return TULEMUS

    def 실행결과(self):
        return subprocess.run([str(self.kaust_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, ALLIKAS, Lisa_kirje=None):
        self.kompileerima_lähe(ALLIKAS, Lisa_kirje)
        (self.kaust_VALUE / 'host.java').write_text(
            'public class host { public static void main(String[] Argumendid) { System.exit(시험.Käivita_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.kaust_VALUE)] +
                       [str(RADA) for RADA in self.kaust_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.kaust_VALUE), 'host'], timeout=5).returncode
        tegelik_andmed = self.실행결과()
        self.assertGreaterEqual(tegelik_andmed, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 kinnitama)')
        self.assertEqual(tegelik_andmed, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SECOND_operand) {
                return ((가 + SECOND_operand) ^ (가 - SECOND_operand) ^ (가 * SECOND_operand) ^ (가 & SECOND_operand) ^ (가 | SECOND_operand))
                    + (가 << SECOND_operand) + (가 >> SECOND_operand) + (가 >>> SECOND_operand);
            }
            public static int Käivita_2() {
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
            public static int Käivita_2() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operand = 1; SECOND_operand < VALUE.length; SECOND_operand++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operand] + VALUE[가] % VALUE[SECOND_operand];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] avama_kirje(int Suurus) { return new int[Suurus]; }
            public static int Käivita_2() {
                int[] 가 = avama_kirje(8); int[] SECOND_operand = 가; int[] 빈것 = new int[0];
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
            public static int Käivita_2() { return 계산(1, 2, 3, 4, VALUE) + 보조.Lugemine(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Lugemine() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Lugemine() + 1;
            public static int Käivita_2() { return VALUE * 10 + 보조.Lugemine(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Lugemine() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tekst = "한글\\u0000😀";
            public static int Käivita_2() {
                if (Tekst != "한글\\u0000😀") return 99;
                return (Tekst.length() + Tekst.charAt(2) + Tekst.charAt(3) + Tekst.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktoriaal(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktoriaal(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Käivita_2() { return (faktoriaal(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklaratsioon = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Käivita_2() {' + deklaratsioon +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int null_operand = 0; return 1 / null_operand;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for sisu_VALUE, 기대 in 경우들:
            with self.subTest(sisu_VALUE=sisu_VALUE):
                self.kompileerima_lähe('public class 시험 { public static int Käivita_2() { ' + sisu_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Käivita_2() { return 0; }',
            'public static int Käivita_2() { Object VALUE = new Object(); return 0; }',
            'public static int Käivita_2() { System.out.println("hello"); return 0; }',
            'public static int Käivita_2() { try { return 1; } catch (Exception VIGA) { return 2; } }',
            'public static synchronized int Käivita_2() { return 0; }',
            'public static int Käivita_2() { return new byte[3].length; }',
            'static native int väline_VALUE(); public static int Käivita_2() { return väline_VALUE(); }',
            'int VALUE; public static int Käivita_2() { return 0; }',
        ]
        for sisu_VALUE in 경우들:
            with self.subTest(sisu_VALUE=sisu_VALUE):
                self.kompileerima_lähe('public class 시험 { ' + sisu_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Väljund = self.kaust_VALUE / 'native'
        Väljund.write_bytes(b'original-output')
        self.kompileerima_lähe('public class 시험 { public static int Käivita_2() { return missing; } }', 성공=False)
        self.assertEqual(Väljund.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompileerima_lähe('public class 시험 { public static int Käivita_2() { return 37; } }')
        self.assertEqual((self.kaust_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_tabel = subprocess.check_output(['readelf', '-l', str(self.kaust_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_tabel)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompileerima_lähe('public class 시험 { public static int Käivita_2() { return kasutaja.실행권한(); } }',
                    {'kasutaja': 'public class kasutaja { public static native int 실행권한(); }'}, siht='user')
        andmed = (self.kaust_VALUE / 'native').read_bytes()
        self.assertEqual(andmed[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', andmed, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.kaust_VALUE / 'native')]))
        # kasutaja ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompileerima_lähe('public class 시험 { public static int Käivita_2() { return seade_VALUE.포트읽기(1); } }',
                    {'seade_VALUE': 'public class seade_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, siht='user')

    def test_내보내기검증(self):
        ALLIKAS = 'public class 시험 { public static int Käivita_2() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.kompileerima_lähe(ALLIKAS, siht='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.kaust_VALUE / 'native')]))
        self.kompileerima_lähe(ALLIKAS, 성공=False, 내보냄='bad;name=시험.호출')
        self.kompileerima_lähe(ALLIKAS, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
