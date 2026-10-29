"""faktisks_dati ELF Izpildīt_komanda + OpenJDK mērs 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilators = Path(__file__).resolve().parents[1] / 'kompilators.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Direktorijs_VALUE = Path(self.임시.name)

    def kompilēt_avots(self, AVOTS, Pievienot_ievade=None, 성공=True, mērķis='linux', 내보냄=None):
        ceļš_Saraksts = []
        for Nosaukums, Saturs_VALUE in dict({'시험': AVOTS}, **(Pievienot_ievade or {})).items():
            CEĻŠ = self.Direktorijs_VALUE / (Nosaukums + '.java')
            CEĻŠ.write_text(Saturs_VALUE, encoding='utf-8')
            ceļš_Saraksts.append(str(CEĻŠ))
        Komanda = [sys.executable, str(kompilators), '--target', mērķis, '--entry', '시험.Palaist', '-o', str(self.Direktorijs_VALUE / 'native')]
        if 내보냄 is not None: Komanda += ['--export', 내보냄]
        mērs = subprocess.run(Komanda + ceļš_Saraksts,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(mērs.returncode, 0, mērs.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(mērs.returncode, 0)
            self.assertIn('kompilēt_avots Kļūda'.encode(), mērs.stderr)
        return mērs

    def 실행결과(self):
        return subprocess.run([str(self.Direktorijs_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, AVOTS, Pievienot_ievade=None):
        self.kompilēt_avots(AVOTS, Pievienot_ievade)
        (self.Direktorijs_VALUE / 'viesot.java').write_text(
            'public class viesot { public static void main(String[] Parametri) { System.exit(시험.Palaist()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Direktorijs_VALUE)] +
                       [str(CEĻŠ) for CEĻŠ in self.Direktorijs_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Direktorijs_VALUE), 'viesot'], timeout=5).returncode
        faktisks_dati = self.실행결과()
        self.assertGreaterEqual(faktisks_dati, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verificēt)')
        self.assertEqual(faktisks_dati, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SECOND_operands) {
                return ((가 + SECOND_operands) ^ (가 - SECOND_operands) ^ (가 * SECOND_operands) ^ (가 & SECOND_operands) ^ (가 | SECOND_operands))
                    + (가 << SECOND_operands) + (가 >> SECOND_operands) + (가 >>> SECOND_operands);
            }
            public static int Palaist() {
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
            public static int Palaist() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operands = 1; SECOND_operands < VALUE.length; SECOND_operands++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operands] + VALUE[가] % VALUE[SECOND_operands];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] atvērt_ievade(int Izmērs) { return new int[Izmērs]; }
            public static int Palaist() {
                int[] 가 = atvērt_ievade(8); int[] SECOND_operands = 가; int[] 빈것 = new int[0];
                if (가 != SECOND_operands || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + SECOND_operands[2] + SECOND_operands[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int SECOND_operands, int 다, int 라, int 마) {
                return 가 + SECOND_operands * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Palaist() { return 계산(1, 2, 3, 4, VALUE) + 보조.Lasīt(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Lasīt() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Lasīt() + 1;
            public static int Palaist() { return VALUE * 10 + 보조.Lasīt(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Lasīt() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Teksts = "한글\\u0000😀";
            public static int Palaist() {
                if (Teksts != "한글\\u0000😀") return 99;
                return (Teksts.length() + Teksts.charAt(2) + Teksts.charAt(3) + Teksts.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktoriāls(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktoriāls(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Palaist() { return (faktoriāls(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklarācija = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Palaist() {' + deklarācija +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nulle_operands = 0; return 1 / nulle_operands;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for pamatteksts_VALUE, 기대 in 경우들:
            with self.subTest(pamatteksts_VALUE=pamatteksts_VALUE):
                self.kompilēt_avots('public class 시험 { public static int Palaist() { ' + pamatteksts_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Palaist() { return 0; }',
            'public static int Palaist() { Object VALUE = new Object(); return 0; }',
            'public static int Palaist() { System.out.println("hello"); return 0; }',
            'public static int Palaist() { try { return 1; } catch (Exception Kļūda) { return 2; } }',
            'public static synchronized int Palaist() { return 0; }',
            'public static int Palaist() { return new byte[3].length; }',
            'static native int ārējs_VALUE(); public static int Palaist() { return ārējs_VALUE(); }',
            'int VALUE; public static int Palaist() { return 0; }',
        ]
        for pamatteksts_VALUE in 경우들:
            with self.subTest(pamatteksts_VALUE=pamatteksts_VALUE):
                self.kompilēt_avots('public class 시험 { ' + pamatteksts_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Izvade = self.Direktorijs_VALUE / 'native'
        Izvade.write_bytes(b'original-output')
        self.kompilēt_avots('public class 시험 { public static int Palaist() { return missing; } }', 성공=False)
        self.assertEqual(Izvade.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompilēt_avots('public class 시험 { public static int Palaist() { return 37; } }')
        self.assertEqual((self.Direktorijs_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_tabula = subprocess.check_output(['readelf', '-l', str(self.Direktorijs_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_tabula)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompilēt_avots('public class 시험 { public static int Palaist() { return lietotājs.실행권한(); } }',
                    {'lietotājs': 'public class lietotājs { public static native int 실행권한(); }'}, mērķis='user')
        dati = (self.Direktorijs_VALUE / 'native').read_bytes()
        self.assertEqual(dati[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', dati, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Direktorijs_VALUE / 'native')]))
        # lietotājs ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompilēt_avots('public class 시험 { public static int Palaist() { return ierīce_VALUE.포트읽기(1); } }',
                    {'ierīce_VALUE': 'public class ierīce_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, mērķis='user')

    def test_내보내기검증(self):
        AVOTS = 'public class 시험 { public static int Palaist() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.kompilēt_avots(AVOTS, mērķis='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Direktorijs_VALUE / 'native')]))
        self.kompilēt_avots(AVOTS, 성공=False, 내보냄='bad;name=시험.호출')
        self.kompilēt_avots(AVOTS, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
