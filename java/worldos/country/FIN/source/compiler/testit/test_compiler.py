"""todellinen_data ELF Suorita_komento + OpenJDK TULOS 대조. 임시 testit 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kääntäjä = Path(__file__).resolve().parents[1] / 'kääntäjä.py'


class testi_alkuperäinen(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Directory_ARVO = Path(self.임시.name)

    def kääntää_lähde(self, lähdetiedosto, liitä_merkintä=None, 성공=True, tavoite='linux', 내보냄=None):
        polku_luettelo = []
        for Nimi, Sisältö_ARVO in dict({'testit': lähdetiedosto}, **(liitä_merkintä or {})).items():
            polku_2 = self.Directory_ARVO / (Nimi + '.java')
            polku_2.write_text(Sisältö_ARVO, encoding='utf-8')
            polku_luettelo.append(str(polku_2))
        komento = [sys.executable, str(kääntäjä), '--target', tavoite, '--entry', 'testit.Suorita_2', '-o', str(self.Directory_ARVO / 'native')]
        if 내보냄 is not None: komento += ['--export', 내보냄]
        TULOS = subprocess.run(komento + polku_luettelo,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(TULOS.returncode, 0, TULOS.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(TULOS.returncode, 0)
            self.assertIn('kääntää_lähde VIRHE'.encode(), TULOS.stderr)
        return TULOS

    def suoritus_KR(self):
        return subprocess.run([str(self.Directory_ARVO / 'native')], timeout=5).returncode

    def 자바대조(self, lähdetiedosto, liitä_merkintä=None):
        self.kääntää_lähde(lähdetiedosto, liitä_merkintä)
        (self.Directory_ARVO / 'isäntä.java').write_text(
            'public class isäntä { public static void main(String[] argumentit) { System.exit(testit.Suorita_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Directory_ARVO)] +
                       [str(polku_2) for polku_2 in self.Directory_ARVO.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Directory_ARVO), 'isäntä'], timeout=5).returncode
        todellinen_data = self.suoritus_KR()
        self.assertGreaterEqual(todellinen_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 tarkistaa)')
        self.assertEqual(todellinen_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class testit {
            static int 섞기(int 가, int SEKUNNIT_operandi) {
                return ((가 + SEKUNNIT_operandi) ^ (가 - SEKUNNIT_operandi) ^ (가 * SEKUNNIT_operandi) ^ (가 & SEKUNNIT_operandi) ^ (가 | SEKUNNIT_operandi))
                    + (가 << SEKUNNIT_operandi) + (가 >> SEKUNNIT_operandi) + (가 >>> SEKUNNIT_operandi);
            }
            public static int Suorita_2() {
                int SUM_ARVO = 7;
                int ARVO = 12345;
                for (int INDEKSI = -65; INDEKSI <= 65; INDEKSI++) {
                    ARVO = ARVO * 1664525 + 1013904223;
                    SUM_ARVO = SUM_ARVO * 31 + 섞기(ARVO, INDEKSI);
                    SUM_ARVO += (byte)ARVO + (short)ARVO + (char)ARVO;
                }
                return (SUM_ARVO & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class testit {
            static int[] ARVO = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Suorita_2() {
                int SUM_ARVO = 13;
                for (int 가 = 0; 가 < ARVO.length; 가++)
                    for (int SEKUNNIT_operandi = 1; SEKUNNIT_operandi < ARVO.length; SEKUNNIT_operandi++)
                        SUM_ARVO = SUM_ARVO * 31 + ARVO[가] / ARVO[SEKUNNIT_operandi] + ARVO[가] % ARVO[SEKUNNIT_operandi];
                return (SUM_ARVO & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class testit {
            static int[] Luo_merkintä(int Koko) { return new int[Koko]; }
            public static int Suorita_2() {
                int[] 가 = Luo_merkintä(8); int[] SEKUNNIT_operandi = 가; int[] 빈것 = new int[0];
                if (가 != SEKUNNIT_operandi || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int ARVO = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ARVO + SEKUNNIT_operandi[2] + SEKUNNIT_operandi[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class testit {
            static int ARVO = 보조.초기값();
            static int 계산(int 가, int SEKUNNIT_operandi, int 다, int 라, int 마) {
                return 가 + SEKUNNIT_operandi * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Suorita_2() { return 계산(1, 2, 3, 4, ARVO) + 보조.Luku(); }
        }''', {'보조': '''public class 보조 {
            static int ARVO = 3;
            static int 초기값() { return ++ARVO; }
            static int Luku() { return ARVO; }
        }'''})

    def testi_valmistelu_kehä(self):
        self.자바대조('''public class testit {
            static int ARVO = 보조.Luku() + 1;
            public static int Suorita_2() { return ARVO * 10 + 보조.Luku(); }
        }''', {'보조': '''public class 보조 {
            static int ARVO = testit.ARVO + 2;
            static int Luku() { return ARVO; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class testit {
            static String teksti = "한글\\u0000😀";
            public static int Suorita_2() {
                if (teksti != "한글\\u0000😀") return 99;
                return (teksti.length() + teksti.charAt(2) + teksti.charAt(3) + teksti.charAt(4)) % 251;
            }
        }''')

    def testi_MUUTA_JA_rekursio(self):
        self.자바대조('''public class testit {
            static int kertoma(int ARVO) { return ARVO <= 1 ? 1 : ARVO * kertoma(ARVO - 1); }
            static int 연속(int ARVO) {
                switch (ARVO) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ARVO) {
                switch (ARVO) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Suorita_2() { return (kertoma(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        esittely = '\n'.join('int ARVO{} = {};'.format(INDEKSI, INDEKSI) for INDEKSI in range(270))
        덧셈 = '+'.join('ARVO{}'.format(INDEKSI) for INDEKSI in range(270))
        self.자바대조('public class testit { public static int Suorita_2() {' + esittely +
                    'ARVO_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nolla_operandi = 0; return 1 / nolla_operandi;', 101),
            ('int[] ARVO = null; return ARVO.length;', 102),
            ('int[] ARVO = new int[1]; return ARVO[1];', 103),
            ('int[] ARVO = new int[1]; ARVO[-1] = 3; return 0;', 103),
            ('int ARVO = -1; return new int[ARVO].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for teksti_ARVO, 기대 in 경우들:
            with self.subTest(teksti_ARVO=teksti_ARVO):
                self.kääntää_lähde('public class testit { public static int Suorita_2() { ' + teksti_ARVO + ' } }')
                self.assertEqual(self.suoritus_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ARVO; public static int Suorita_2() { return 0; }',
            'public static int Suorita_2() { Object ARVO = new Object(); return 0; }',
            'public static int Suorita_2() { System.out.println("hello"); return 0; }',
            'public static int Suorita_2() { try { return 1; } catch (Exception VIRHE) { return 2; } }',
            'public static synchronized int Suorita_2() { return 0; }',
            'public static int Suorita_2() { return new byte[3].length; }',
            'static native int ulkoinen_ARVO(); public static int Suorita_2() { return ulkoinen_ARVO(); }',
            'int ARVO; public static int Suorita_2() { return 0; }',
        ]
        for teksti_ARVO in 경우들:
            with self.subTest(teksti_ARVO=teksti_ARVO):
                self.kääntää_lähde('public class testit { ' + teksti_ARVO + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        tulostuspaikka = self.Directory_ARVO / 'native'
        tulostuspaikka.write_bytes(b'original-output')
        self.kääntää_lähde('public class testit { public static int Suorita_2() { return missing; } }', 성공=False)
        self.assertEqual(tulostuspaikka.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kääntää_lähde('public class testit { public static int Suorita_2() { return 37; } }')
        self.assertEqual((self.Directory_ARVO / 'native').read_bytes()[:5], b'\x7fELF\x01')
        HAKU_taulukko = subprocess.check_output(['readelf', '-l', str(self.Directory_ARVO / 'native')])
        self.assertNotIn(b'INTERP', HAKU_taulukko)
        self.assertEqual(self.suoritus_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kääntää_lähde('public class testit { public static int Suorita_2() { return käyttäjätila.suoritus_lupa(); } }',
                    {'käyttäjätila': 'public class käyttäjätila { public static native int suoritus_lupa(); }'}, tavoite='user')
        data = (self.Directory_ARVO / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Directory_ARVO / 'native')]))
        # käyttäjätila ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kääntää_lähde('public class testit { public static int Suorita_2() { return laite_ARVO.lukea_laitteisto_portti(1); } }',
                    {'laite_ARVO': 'public class laite_ARVO { public static native int lukea_laitteisto_portti(int ARVO); }'}, 성공=False, tavoite='user')

    def testi_viedä_vahvistus(self):
        lähdetiedosto = 'public class testit { public static int Suorita_2() { return 0; } static int 호출(int ARVO) { return ARVO; } }'
        self.kääntää_lähde(lähdetiedosto, tavoite='kernel', 내보냄='kernel_dispatch=testit.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Directory_ARVO / 'native')]))
        self.kääntää_lähde(lähdetiedosto, 성공=False, 내보냄='bad;name=testit.호출')
        self.kääntää_lähde(lähdetiedosto, 성공=False, 내보냄='missing=testit.없음')


if __name__ == '__main__':
    unittest.main()
