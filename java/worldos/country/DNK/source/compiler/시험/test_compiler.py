"""faktisk_data ELF Udfør_kommando + OpenJDK KR 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

compiler = Path(__file__).resolve().parents[1] / 'compiler.py'


class test_oprindelig(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.mappe_VÆRDI = Path(self.임시.name)

    def kompilere_kilde(self, KILDE, tilføj_post=None, 성공=True, mål='linux', 내보냄=None):
        sti_Liste = []
        for Navn, Indhold_VÆRDI in dict({'시험': KILDE}, **(tilføj_post or {})).items():
            Sti = self.mappe_VÆRDI / (Navn + '.java')
            Sti.write_text(Indhold_VÆRDI, encoding='utf-8')
            sti_Liste.append(str(Sti))
        Kommando = [sys.executable, str(compiler), '--target', mål, '--entry', '시험.Kør_2', '-o', str(self.mappe_VÆRDI / 'native')]
        if 내보냄 is not None: Kommando += ['--export', 내보냄]
        KR = subprocess.run(Kommando + sti_Liste,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(KR.returncode, 0, KR.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(KR.returncode, 0)
            self.assertIn('kompilere_kilde fejl'.encode(), KR.stderr)
        return KR

    def udførelse_KR(self):
        return subprocess.run([str(self.mappe_VÆRDI / 'native')], timeout=5).returncode

    def 자바대조(self, KILDE, tilføj_post=None):
        self.kompilere_kilde(KILDE, tilføj_post)
        (self.mappe_VÆRDI / 'vært.java').write_text(
            'public class vært { public static void main(String[] Argumenter) { System.exit(시험.Kør_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.mappe_VÆRDI)] +
                       [str(Sti) for Sti in self.mappe_VÆRDI.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.mappe_VÆRDI), 'vært'], timeout=5).returncode
        faktisk_data = self.udførelse_KR()
        self.assertGreaterEqual(faktisk_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 bekræfte)')
        self.assertEqual(faktisk_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SEKUND_operand) {
                return ((가 + SEKUND_operand) ^ (가 - SEKUND_operand) ^ (가 * SEKUND_operand) ^ (가 & SEKUND_operand) ^ (가 | SEKUND_operand))
                    + (가 << SEKUND_operand) + (가 >> SEKUND_operand) + (가 >>> SEKUND_operand);
            }
            public static int Kør_2() {
                int SUM_VÆRDI = 7;
                int VÆRDI = 12345;
                for (int INDEKS = -65; INDEKS <= 65; INDEKS++) {
                    VÆRDI = VÆRDI * 1664525 + 1013904223;
                    SUM_VÆRDI = SUM_VÆRDI * 31 + 섞기(VÆRDI, INDEKS);
                    SUM_VÆRDI += (byte)VÆRDI + (short)VÆRDI + (char)VÆRDI;
                }
                return (SUM_VÆRDI & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] VÆRDI = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Kør_2() {
                int SUM_VÆRDI = 13;
                for (int 가 = 0; 가 < VÆRDI.length; 가++)
                    for (int SEKUND_operand = 1; SEKUND_operand < VÆRDI.length; SEKUND_operand++)
                        SUM_VÆRDI = SUM_VÆRDI * 31 + VÆRDI[가] / VÆRDI[SEKUND_operand] + VÆRDI[가] % VÆRDI[SEKUND_operand];
                return (SUM_VÆRDI & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] åbne_post_81b8d99b(int Størrelse) { return new int[Størrelse]; }
            public static int Kør_2() {
                int[] 가 = åbne_post_81b8d99b(8); int[] SEKUND_operand = 가; int[] 빈것 = new int[0];
                if (가 != SEKUND_operand || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VÆRDI = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VÆRDI + SEKUND_operand[2] + SEKUND_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VÆRDI = 보조.초기값();
            static int 계산(int 가, int SEKUND_operand, int 다, int 라, int 마) {
                return 가 + SEKUND_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Kør_2() { return 계산(1, 2, 3, 4, VÆRDI) + 보조.Læse(); }
        }''', {'보조': '''public class 보조 {
            static int VÆRDI = 3;
            static int 초기값() { return ++VÆRDI; }
            static int Læse() { return VÆRDI; }
        }'''})

    def test_initialisering_Cyklus(self):
        self.자바대조('''public class 시험 {
            static int VÆRDI = 보조.Læse() + 1;
            public static int Kør_2() { return VÆRDI * 10 + 보조.Læse(); }
        }''', {'보조': '''public class 보조 {
            static int VÆRDI = 시험.VÆRDI + 2;
            static int Læse() { return VÆRDI; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tekst = "한글\\u0000😀";
            public static int Kør_2() {
                if (Tekst != "한글\\u0000😀") return 99;
                return (Tekst.length() + Tekst.charAt(2) + Tekst.charAt(3) + Tekst.charAt(4)) % 251;
            }
        }''')

    def test_SKIFT_OG_rekursion(self):
        self.자바대조('''public class 시험 {
            static int fakultet(int VÆRDI) { return VÆRDI <= 1 ? 1 : VÆRDI * fakultet(VÆRDI - 1); }
            static int 연속(int VÆRDI) {
                switch (VÆRDI) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VÆRDI) {
                switch (VÆRDI) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Kør_2() { return (fakultet(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        erklæring = '\n'.join('int VÆRDI{} = {};'.format(INDEKS, INDEKS) for INDEKS in range(270))
        덧셈 = '+'.join('VÆRDI{}'.format(INDEKS) for INDEKS in range(270))
        self.자바대조('public class 시험 { public static int Kør_2() {' + erklæring +
                    'VÆRDI_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nul_operand = 0; return 1 / nul_operand;', 101),
            ('int[] VÆRDI = null; return VÆRDI.length;', 102),
            ('int[] VÆRDI = new int[1]; return VÆRDI[1];', 103),
            ('int[] VÆRDI = new int[1]; VÆRDI[-1] = 3; return 0;', 103),
            ('int VÆRDI = -1; return new int[VÆRDI].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for brødtekst_VÆRDI, 기대 in 경우들:
            with self.subTest(brødtekst_VÆRDI=brødtekst_VÆRDI):
                self.kompilere_kilde('public class 시험 { public static int Kør_2() { ' + brødtekst_VÆRDI + ' } }')
                self.assertEqual(self.udførelse_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VÆRDI; public static int Kør_2() { return 0; }',
            'public static int Kør_2() { Object VÆRDI = new Object(); return 0; }',
            'public static int Kør_2() { System.out.println("hello"); return 0; }',
            'public static int Kør_2() { try { return 1; } catch (Exception fejl) { return 2; } }',
            'public static synchronized int Kør_2() { return 0; }',
            'public static int Kør_2() { return new byte[3].length; }',
            'static native int ekstern_VÆRDI(); public static int Kør_2() { return ekstern_VÆRDI(); }',
            'int VÆRDI; public static int Kør_2() { return 0; }',
        ]
        for brødtekst_VÆRDI in 경우들:
            with self.subTest(brødtekst_VÆRDI=brødtekst_VÆRDI):
                self.kompilere_kilde('public class 시험 { ' + brødtekst_VÆRDI + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Udgang = self.mappe_VÆRDI / 'native'
        Udgang.write_bytes(b'original-output')
        self.kompilere_kilde('public class 시험 { public static int Kør_2() { return missing; } }', 성공=False)
        self.assertEqual(Udgang.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompilere_kilde('public class 시험 { public static int Kør_2() { return 37; } }')
        self.assertEqual((self.mappe_VÆRDI / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Opslag_tabel = subprocess.check_output(['readelf', '-l', str(self.mappe_VÆRDI / 'native')])
        self.assertNotIn(b'INTERP', Opslag_tabel)
        self.assertEqual(self.udførelse_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompilere_kilde('public class 시험 { public static int Kør_2() { return bruger.udførelse_rettighed(); } }',
                    {'bruger': 'public class bruger { public static native int udførelse_rettighed(); }'}, mål='user')
        data = (self.mappe_VÆRDI / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.mappe_VÆRDI / 'native')]))
        # bruger ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompilere_kilde('public class 시험 { public static int Kør_2() { return enhed_VÆRDI.포트읽기(1); } }',
                    {'enhed_VÆRDI': 'public class enhed_VÆRDI { public static native int 포트읽기(int VÆRDI); }'}, 성공=False, mål='user')

    def test_eksportere_validering(self):
        KILDE = 'public class 시험 { public static int Kør_2() { return 0; } static int 호출(int VÆRDI) { return VÆRDI; } }'
        self.kompilere_kilde(KILDE, mål='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.mappe_VÆRDI / 'native')]))
        self.kompilere_kilde(KILDE, 성공=False, 내보냄='bad;name=시험.호출')
        self.kompilere_kilde(KILDE, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
