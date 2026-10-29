"""faktisk_data ELF Utfør_kommando + OpenJDK KR 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilator = Path(__file__).resolve().parents[1] / 'kompilator.py'


class test_opprinnelig(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.katalog_VERDI = Path(self.임시.name)

    def kompilere_kilde(self, KILDE, Tilføye_oppføring=None, 성공=True, mål='linux', 내보냄=None):
        bane_Liste = []
        for Navn, Innhold_VERDI in dict({'시험': KILDE}, **(Tilføye_oppføring or {})).items():
            Sti = self.katalog_VERDI / (Navn + '.java')
            Sti.write_text(Innhold_VERDI, encoding='utf-8')
            bane_Liste.append(str(Sti))
        Kommando = [sys.executable, str(kompilator), '--target', mål, '--entry', '시험.Kjør_2', '-o', str(self.katalog_VERDI / 'native')]
        if 내보냄 is not None: Kommando += ['--export', 내보냄]
        KR = subprocess.run(Kommando + bane_Liste,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(KR.returncode, 0, KR.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(KR.returncode, 0)
            self.assertIn('kompilere_kilde feil'.encode(), KR.stderr)
        return KR

    def kjøring_KR(self):
        return subprocess.run([str(self.katalog_VERDI / 'native')], timeout=5).returncode

    def 자바대조(self, KILDE, Tilføye_oppføring=None):
        self.kompilere_kilde(KILDE, Tilføye_oppføring)
        (self.katalog_VERDI / 'vert.java').write_text(
            'public class vert { public static void main(String[] Argumenter) { System.exit(시험.Kjør_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.katalog_VERDI)] +
                       [str(Sti) for Sti in self.katalog_VERDI.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.katalog_VERDI), 'vert'], timeout=5).returncode
        faktisk_data = self.kjøring_KR()
        self.assertGreaterEqual(faktisk_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 bekrefte)')
        self.assertEqual(faktisk_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SEKUND_operand) {
                return ((가 + SEKUND_operand) ^ (가 - SEKUND_operand) ^ (가 * SEKUND_operand) ^ (가 & SEKUND_operand) ^ (가 | SEKUND_operand))
                    + (가 << SEKUND_operand) + (가 >> SEKUND_operand) + (가 >>> SEKUND_operand);
            }
            public static int Kjør_2() {
                int SUMMER_VERDI = 7;
                int VERDI = 12345;
                for (int INDEKS = -65; INDEKS <= 65; INDEKS++) {
                    VERDI = VERDI * 1664525 + 1013904223;
                    SUMMER_VERDI = SUMMER_VERDI * 31 + 섞기(VERDI, INDEKS);
                    SUMMER_VERDI += (byte)VERDI + (short)VERDI + (char)VERDI;
                }
                return (SUMMER_VERDI & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] VERDI = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Kjør_2() {
                int SUMMER_VERDI = 13;
                for (int 가 = 0; 가 < VERDI.length; 가++)
                    for (int SEKUND_operand = 1; SEKUND_operand < VERDI.length; SEKUND_operand++)
                        SUMMER_VERDI = SUMMER_VERDI * 31 + VERDI[가] / VERDI[SEKUND_operand] + VERDI[가] % VERDI[SEKUND_operand];
                return (SUMMER_VERDI & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] åpne_oppføring(int Størrelse) { return new int[Størrelse]; }
            public static int Kjør_2() {
                int[] 가 = åpne_oppføring(8); int[] SEKUND_operand = 가; int[] tom_objekt = new int[0];
                if (가 != SEKUND_operand || 가 == null || tom_objekt.length != 0 || 가[7] != 0) return 99;
                int VERDI = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VERDI + SEKUND_operand[2] + SEKUND_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VERDI = 보조.초기값();
            static int 계산(int 가, int SEKUND_operand, int 다, int 라, int 마) {
                return 가 + SEKUND_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Kjør_2() { return 계산(1, 2, 3, 4, VERDI) + 보조.Les(); }
        }''', {'보조': '''public class 보조 {
            static int VERDI = 3;
            static int 초기값() { return ++VERDI; }
            static int Les() { return VERDI; }
        }'''})

    def test_initialisering_Krets(self):
        self.자바대조('''public class 시험 {
            static int VERDI = 보조.Les() + 1;
            public static int Kjør_2() { return VERDI * 10 + 보조.Les(); }
        }''', {'보조': '''public class 보조 {
            static int VERDI = 시험.VERDI + 2;
            static int Les() { return VERDI; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tekst = "한글\\u0000😀";
            public static int Kjør_2() {
                if (Tekst != "한글\\u0000😀") return 99;
                return (Tekst.length() + Tekst.charAt(2) + Tekst.charAt(3) + Tekst.charAt(4)) % 251;
            }
        }''')

    def test_bytt_OG_rekursjon(self):
        self.자바대조('''public class 시험 {
            static int fakultet(int VERDI) { return VERDI <= 1 ? 1 : VERDI * fakultet(VERDI - 1); }
            static int 연속(int VERDI) {
                switch (VERDI) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VERDI) {
                switch (VERDI) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Kjør_2() { return (fakultet(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        erklæring = '\n'.join('int VERDI{} = {};'.format(INDEKS, INDEKS) for INDEKS in range(270))
        덧셈 = '+'.join('VERDI{}'.format(INDEKS) for INDEKS in range(270))
        self.자바대조('public class 시험 { public static int Kjør_2() {' + erklæring +
                    'VERDI_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int null_operand = 0; return 1 / null_operand;', 101),
            ('int[] VERDI = null; return VERDI.length;', 102),
            ('int[] VERDI = new int[1]; return VERDI[1];', 103),
            ('int[] VERDI = new int[1]; VERDI[-1] = 3; return 0;', 103),
            ('int VERDI = -1; return new int[VERDI].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for brødtekst_VERDI, 기대 in 경우들:
            with self.subTest(brødtekst_VERDI=brødtekst_VERDI):
                self.kompilere_kilde('public class 시험 { public static int Kjør_2() { ' + brødtekst_VERDI + ' } }')
                self.assertEqual(self.kjøring_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VERDI; public static int Kjør_2() { return 0; }',
            'public static int Kjør_2() { Object VERDI = new Object(); return 0; }',
            'public static int Kjør_2() { System.out.println("hello"); return 0; }',
            'public static int Kjør_2() { try { return 1; } catch (Exception feil) { return 2; } }',
            'public static synchronized int Kjør_2() { return 0; }',
            'public static int Kjør_2() { return new byte[3].length; }',
            'static native int ekstern_VERDI(); public static int Kjør_2() { return ekstern_VERDI(); }',
            'int VERDI; public static int Kjør_2() { return 0; }',
        ]
        for brødtekst_VERDI in 경우들:
            with self.subTest(brødtekst_VERDI=brødtekst_VERDI):
                self.kompilere_kilde('public class 시험 { ' + brødtekst_VERDI + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Utgang = self.katalog_VERDI / 'native'
        Utgang.write_bytes(b'original-output')
        self.kompilere_kilde('public class 시험 { public static int Kjør_2() { return missing; } }', 성공=False)
        self.assertEqual(Utgang.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompilere_kilde('public class 시험 { public static int Kjør_2() { return 37; } }')
        self.assertEqual((self.katalog_VERDI / 'native').read_bytes()[:5], b'\x7fELF\x01')
        oppslagstabell = subprocess.check_output(['readelf', '-l', str(self.katalog_VERDI / 'native')])
        self.assertNotIn(b'INTERP', oppslagstabell)
        self.assertEqual(self.kjøring_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompilere_kilde('public class 시험 { public static int Kjør_2() { return bruker.kjøring_tillatelse(); } }',
                    {'bruker': 'public class bruker { public static native int kjøring_tillatelse(); }'}, mål='user')
        data = (self.katalog_VERDI / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.katalog_VERDI / 'native')]))
        # bruker ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompilere_kilde('public class 시험 { public static int Kjør_2() { return enhet_VERDI.포트읽기(1); } }',
                    {'enhet_VERDI': 'public class enhet_VERDI { public static native int 포트읽기(int VERDI); }'}, 성공=False, mål='user')

    def test_eksportere_validering(self):
        KILDE = 'public class 시험 { public static int Kjør_2() { return 0; } static int 호출(int VERDI) { return VERDI; } }'
        self.kompilere_kilde(KILDE, mål='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.katalog_VERDI / 'native')]))
        self.kompilere_kilde(KILDE, 성공=False, 내보냄='bad;name=시험.호출')
        self.kompilere_kilde(KILDE, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
