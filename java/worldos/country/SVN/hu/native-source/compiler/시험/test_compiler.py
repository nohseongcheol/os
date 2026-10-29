"""tényleges_adat ELF végrehajt_parancs + OpenJDK KR 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

fordítóprogram = Path(__file__).resolve().parents[1] / 'fordítóprogram.py'


class teszt_natív(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.címtár_ÉRTÉK = Path(self.임시.name)

    def épít_forrás(self, FORRÁS, hozzáfűz_bejegyzés=None, 성공=True, cél='linux', 내보냄=None):
        útvonal_Lista = []
        for Név, Tartalom_ÉRTÉK in dict({'시험': FORRÁS}, **(hozzáfűz_bejegyzés or {})).items():
            ÚTVONAL = self.címtár_ÉRTÉK / (Név + '.java')
            ÚTVONAL.write_text(Tartalom_ÉRTÉK, encoding='utf-8')
            útvonal_Lista.append(str(ÚTVONAL))
        Parancs = [sys.executable, str(fordítóprogram), '--target', cél, '--entry', '시험.Futtatás', '-o', str(self.címtár_ÉRTÉK / 'native')]
        if 내보냄 is not None: Parancs += ['--export', 내보냄]
        KR = subprocess.run(Parancs + útvonal_Lista,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(KR.returncode, 0, KR.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(KR.returncode, 0)
            self.assertIn('épít_forrás HIBA'.encode(), KR.stderr)
        return KR

    def végrehajtás_KR(self):
        return subprocess.run([str(self.címtár_ÉRTÉK / 'native')], timeout=5).returncode

    def 자바대조(self, FORRÁS, hozzáfűz_bejegyzés=None):
        self.épít_forrás(FORRÁS, hozzáfűz_bejegyzés)
        (self.címtár_ÉRTÉK / 'gazda.java').write_text(
            'public class gazda { public static void main(String[] Argumentumok) { System.exit(시험.Futtatás()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.címtár_ÉRTÉK)] +
                       [str(ÚTVONAL) for ÚTVONAL in self.címtár_ÉRTÉK.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.címtár_ÉRTÉK), 'gazda'], timeout=5).returncode
        tényleges_adat = self.végrehajtás_KR()
        self.assertGreaterEqual(tényleges_adat, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 igazol)')
        self.assertEqual(tényleges_adat, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int MPERC_operandus) {
                return ((가 + MPERC_operandus) ^ (가 - MPERC_operandus) ^ (가 * MPERC_operandus) ^ (가 & MPERC_operandus) ^ (가 | MPERC_operandus))
                    + (가 << MPERC_operandus) + (가 >> MPERC_operandus) + (가 >>> MPERC_operandus);
            }
            public static int Futtatás() {
                int SUM_ÉRTÉK = 7;
                int ÉRTÉK = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    ÉRTÉK = ÉRTÉK * 1664525 + 1013904223;
                    SUM_ÉRTÉK = SUM_ÉRTÉK * 31 + 섞기(ÉRTÉK, INDEX);
                    SUM_ÉRTÉK += (byte)ÉRTÉK + (short)ÉRTÉK + (char)ÉRTÉK;
                }
                return (SUM_ÉRTÉK & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ÉRTÉK = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Futtatás() {
                int SUM_ÉRTÉK = 13;
                for (int 가 = 0; 가 < ÉRTÉK.length; 가++)
                    for (int MPERC_operandus = 1; MPERC_operandus < ÉRTÉK.length; MPERC_operandus++)
                        SUM_ÉRTÉK = SUM_ÉRTÉK * 31 + ÉRTÉK[가] / ÉRTÉK[MPERC_operandus] + ÉRTÉK[가] % ÉRTÉK[MPERC_operandus];
                return (SUM_ÉRTÉK & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] készít_bejegyzés(int Méret) { return new int[Méret]; }
            public static int Futtatás() {
                int[] 가 = készít_bejegyzés(8); int[] MPERC_operandus = 가; int[] üres_objektum = new int[0];
                if (가 != MPERC_operandus || 가 == null || üres_objektum.length != 0 || 가[7] != 0) return 99;
                int ÉRTÉK = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ÉRTÉK + MPERC_operandus[2] + MPERC_operandus[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ÉRTÉK = 보조.초기값();
            static int 계산(int 가, int MPERC_operandus, int 다, int 라, int 마) {
                return 가 + MPERC_operandus * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Futtatás() { return 계산(1, 2, 3, 4, ÉRTÉK) + 보조.Olvasás(); }
        }''', {'보조': '''public class 보조 {
            static int ÉRTÉK = 3;
            static int 초기값() { return ++ÉRTÉK; }
            static int Olvasás() { return ÉRTÉK; }
        }'''})

    def teszt_inicializálás_Ciklus(self):
        self.자바대조('''public class 시험 {
            static int ÉRTÉK = 보조.Olvasás() + 1;
            public static int Futtatás() { return ÉRTÉK * 10 + 보조.Olvasás(); }
        }''', {'보조': '''public class 보조 {
            static int ÉRTÉK = 시험.ÉRTÉK + 2;
            static int Olvasás() { return ÉRTÉK; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Szöveg = "한글\\u0000😀";
            public static int Futtatás() {
                if (Szöveg != "한글\\u0000😀") return 99;
                return (Szöveg.length() + Szöveg.charAt(2) + Szöveg.charAt(3) + Szöveg.charAt(4)) % 251;
            }
        }''')

    def teszt_vált_ÉS_rekurzió(self):
        self.자바대조('''public class 시험 {
            static int faktoriális(int ÉRTÉK) { return ÉRTÉK <= 1 ? 1 : ÉRTÉK * faktoriális(ÉRTÉK - 1); }
            static int 연속(int ÉRTÉK) {
                switch (ÉRTÉK) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ÉRTÉK) {
                switch (ÉRTÉK) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Futtatás() { return (faktoriális(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        bevallás = '\n'.join('int ÉRTÉK{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('ÉRTÉK{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Futtatás() {' + bevallás +
                    'ÉRTÉK_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nulla_operandus = 0; return 1 / nulla_operandus;', 101),
            ('int[] ÉRTÉK = null; return ÉRTÉK.length;', 102),
            ('int[] ÉRTÉK = new int[1]; return ÉRTÉK[1];', 103),
            ('int[] ÉRTÉK = new int[1]; ÉRTÉK[-1] = 3; return 0;', 103),
            ('int ÉRTÉK = -1; return new int[ÉRTÉK].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for törzs_ÉRTÉK, 기대 in 경우들:
            with self.subTest(törzs_ÉRTÉK=törzs_ÉRTÉK):
                self.épít_forrás('public class 시험 { public static int Futtatás() { ' + törzs_ÉRTÉK + ' } }')
                self.assertEqual(self.végrehajtás_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ÉRTÉK; public static int Futtatás() { return 0; }',
            'public static int Futtatás() { Object ÉRTÉK = new Object(); return 0; }',
            'public static int Futtatás() { System.out.println("hello"); return 0; }',
            'public static int Futtatás() { try { return 1; } catch (Exception HIBA) { return 2; } }',
            'public static synchronized int Futtatás() { return 0; }',
            'public static int Futtatás() { return new byte[3].length; }',
            'static native int külső_ÉRTÉK(); public static int Futtatás() { return külső_ÉRTÉK(); }',
            'int ÉRTÉK; public static int Futtatás() { return 0; }',
        ]
        for törzs_ÉRTÉK in 경우들:
            with self.subTest(törzs_ÉRTÉK=törzs_ÉRTÉK):
                self.épít_forrás('public class 시험 { ' + törzs_ÉRTÉK + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Kimenet = self.címtár_ÉRTÉK / 'native'
        Kimenet.write_bytes(b'original-output')
        self.épít_forrás('public class 시험 { public static int Futtatás() { return missing; } }', 성공=False)
        self.assertEqual(Kimenet.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.épít_forrás('public class 시험 { public static int Futtatás() { return 37; } }')
        self.assertEqual((self.címtár_ÉRTÉK / 'native').read_bytes()[:5], b'\x7fELF\x01')
        keresőtáblázat = subprocess.check_output(['readelf', '-l', str(self.címtár_ÉRTÉK / 'native')])
        self.assertNotIn(b'INTERP', keresőtáblázat)
        self.assertEqual(self.végrehajtás_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.épít_forrás('public class 시험 { public static int Futtatás() { return felhasználó.végrehajtás_engedély(); } }',
                    {'felhasználó': 'public class felhasználó { public static native int végrehajtás_engedély(); }'}, cél='user')
        adat = (self.címtár_ÉRTÉK / 'native').read_bytes()
        self.assertEqual(adat[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', adat, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.címtár_ÉRTÉK / 'native')]))
        # felhasználó ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.épít_forrás('public class 시험 { public static int Futtatás() { return mobil_ÉRTÉK.포트읽기(1); } }',
                    {'mobil_ÉRTÉK': 'public class mobil_ÉRTÉK { public static native int 포트읽기(int ÉRTÉK); }'}, 성공=False, cél='user')

    def teszt_exportál_ellenőrzés(self):
        FORRÁS = 'public class 시험 { public static int Futtatás() { return 0; } static int 호출(int ÉRTÉK) { return ÉRTÉK; } }'
        self.épít_forrás(FORRÁS, cél='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.címtár_ÉRTÉK / 'native')]))
        self.épít_forrás(FORRÁS, 성공=False, 내보냄='bad;name=시험.호출')
        self.épít_forrás(FORRÁS, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
