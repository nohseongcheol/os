"""fiili_veri ELF yürütmek_komut + OpenJDK sonuç 대조. 임시 sınamalar 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

derleyici = Path(__file__).resolve().parents[1] / 'derleyici.py'


class test_yerel(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.dizin_değer = Path(self.임시.name)

    def derlemek_kaynak(self, kaynakKod, Ekleme_girdi=None, 성공=True, hedef='linux', 내보냄=None):
        yol_Liste = []
        for İsim, içerik_değer in dict({'sınamalar': kaynakKod}, **(Ekleme_girdi or {})).items():
            yol = self.dizin_değer / (İsim + '.java')
            yol.write_text(içerik_değer, encoding='utf-8')
            yol_Liste.append(str(yol))
        komut = [sys.executable, str(derleyici), '--target', hedef, '--entry', 'sınamalar.çalıştır', '-o', str(self.dizin_değer / 'native')]
        if 내보냄 is not None: komut += ['--export', 내보냄]
        sonuç = subprocess.run(komut + yol_Liste,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(sonuç.returncode, 0, sonuç.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(sonuç.returncode, 0)
            self.assertIn('derlemek_kaynak hata'.encode(), sonuç.stderr)
        return sonuç

    def yürütme_KR(self):
        return subprocess.run([str(self.dizin_değer / 'native')], timeout=5).returncode

    def 자바대조(self, kaynakKod, Ekleme_girdi=None):
        self.derlemek_kaynak(kaynakKod, Ekleme_girdi)
        (self.dizin_değer / 'konak.java').write_text(
            'public class konak { public static void main(String[] bağımsız_değişkenler) { System.exit(sınamalar.çalıştır()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.dizin_değer)] +
                       [str(yol) for yol in self.dizin_değer.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.dizin_değer), 'konak'], timeout=5).returncode
        fiili_veri = self.yürütme_KR()
        self.assertGreaterEqual(fiili_veri, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 doğrulamak)')
        self.assertEqual(fiili_veri, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class sınamalar {
            static int 섞기(int 가, int SANİYE_işlenen) {
                return ((가 + SANİYE_işlenen) ^ (가 - SANİYE_işlenen) ^ (가 * SANİYE_işlenen) ^ (가 & SANİYE_işlenen) ^ (가 | SANİYE_işlenen))
                    + (가 << SANİYE_işlenen) + (가 >> SANİYE_işlenen) + (가 >>> SANİYE_işlenen);
            }
            public static int çalıştır() {
                int SUM_değer = 7;
                int değer = 12345;
                for (int Dizin = -65; Dizin <= 65; Dizin++) {
                    değer = değer * 1664525 + 1013904223;
                    SUM_değer = SUM_değer * 31 + 섞기(değer, Dizin);
                    SUM_değer += (byte)değer + (short)değer + (char)değer;
                }
                return (SUM_değer & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class sınamalar {
            static int[] değer = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int çalıştır() {
                int SUM_değer = 13;
                for (int 가 = 0; 가 < değer.length; 가++)
                    for (int SANİYE_işlenen = 1; SANİYE_işlenen < değer.length; SANİYE_işlenen++)
                        SUM_değer = SUM_değer * 31 + değer[가] / değer[SANİYE_işlenen] + değer[가] % değer[SANİYE_işlenen];
                return (SUM_değer & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class sınamalar {
            static int[] açmak_girdi(int Boyut) { return new int[Boyut]; }
            public static int çalıştır() {
                int[] 가 = açmak_girdi(8); int[] SANİYE_işlenen = 가; int[] boş_nesne = new int[0];
                if (가 != SANİYE_işlenen || 가 == null || boş_nesne.length != 0 || 가[7] != 0) return 99;
                int değer = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return değer + SANİYE_işlenen[2] + SANİYE_işlenen[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class sınamalar {
            static int değer = 보조.초기값();
            static int 계산(int 가, int SANİYE_işlenen, int 다, int 라, int 마) {
                return 가 + SANİYE_işlenen * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int çalıştır() { return 계산(1, 2, 3, 4, değer) + 보조.Okuma(); }
        }''', {'보조': '''public class 보조 {
            static int değer = 3;
            static int 초기값() { return ++değer; }
            static int Okuma() { return değer; }
        }'''})

    def test_başlatma_Döngü(self):
        self.자바대조('''public class sınamalar {
            static int değer = 보조.Okuma() + 1;
            public static int çalıştır() { return değer * 10 + 보조.Okuma(); }
        }''', {'보조': '''public class 보조 {
            static int değer = sınamalar.değer + 2;
            static int Okuma() { return değer; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class sınamalar {
            static String metin = "한글\\u0000😀";
            public static int çalıştır() {
                if (metin != "한글\\u0000😀") return 99;
                return (metin.length() + metin.charAt(2) + metin.charAt(3) + metin.charAt(4)) % 251;
            }
        }''')

    def test_geçiş_VE_özyineleme(self):
        self.자바대조('''public class sınamalar {
            static int çarpınım(int değer) { return değer <= 1 ? 1 : değer * çarpınım(değer - 1); }
            static int 연속(int değer) {
                switch (değer) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int değer) {
                switch (değer) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int çalıştır() { return (çarpınım(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        bildirim = '\n'.join('int değer{} = {};'.format(Dizin, Dizin) for Dizin in range(270))
        덧셈 = '+'.join('değer{}'.format(Dizin) for Dizin in range(270))
        self.자바대조('public class sınamalar { public static int çalıştır() {' + bildirim +
                    'değer_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int sıfır_işlenen = 0; return 1 / sıfır_işlenen;', 101),
            ('int[] değer = null; return değer.length;', 102),
            ('int[] değer = new int[1]; return değer[1];', 103),
            ('int[] değer = new int[1]; değer[-1] = 3; return 0;', 103),
            ('int değer = -1; return new int[değer].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for gövde_değer, 기대 in 경우들:
            with self.subTest(gövde_değer=gövde_değer):
                self.derlemek_kaynak('public class sınamalar { public static int çalıştır() { ' + gövde_değer + ' } }')
                self.assertEqual(self.yürütme_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long değer; public static int çalıştır() { return 0; }',
            'public static int çalıştır() { Object değer = new Object(); return 0; }',
            'public static int çalıştır() { System.out.println("hello"); return 0; }',
            'public static int çalıştır() { try { return 1; } catch (Exception hata) { return 2; } }',
            'public static synchronized int çalıştır() { return 0; }',
            'public static int çalıştır() { return new byte[3].length; }',
            'static native int dış_değer(); public static int çalıştır() { return dış_değer(); }',
            'int değer; public static int çalıştır() { return 0; }',
        ]
        for gövde_değer in 경우들:
            with self.subTest(gövde_değer=gövde_değer):
                self.derlemek_kaynak('public class sınamalar { ' + gövde_değer + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        metinÇıktısı = self.dizin_değer / 'native'
        metinÇıktısı.write_bytes(b'original-output')
        self.derlemek_kaynak('public class sınamalar { public static int çalıştır() { return missing; } }', 성공=False)
        self.assertEqual(metinÇıktısı.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.derlemek_kaynak('public class sınamalar { public static int çalıştır() { return 37; } }')
        self.assertEqual((self.dizin_değer / 'native').read_bytes()[:5], b'\x7fELF\x01')
        arama_tablosu = subprocess.check_output(['readelf', '-l', str(self.dizin_değer / 'native')])
        self.assertNotIn(b'INTERP', arama_tablosu)
        self.assertEqual(self.yürütme_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.derlemek_kaynak('public class sınamalar { public static int çalıştır() { return kullanıcı_alanı.yürütme_izin(); } }',
                    {'kullanıcı_alanı': 'public class kullanıcı_alanı { public static native int yürütme_izin(); }'}, hedef='user')
        veri = (self.dizin_değer / 'native').read_bytes()
        self.assertEqual(veri[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', veri, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.dizin_değer / 'native')]))
        # kullanıcı_alanı ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.derlemek_kaynak('public class sınamalar { public static int çalıştır() { return cihaz_değer.포트읽기(1); } }',
                    {'cihaz_değer': 'public class cihaz_değer { public static native int 포트읽기(int değer); }'}, 성공=False, hedef='user')

    def test_dışarı_aktarmak_doğrulama(self):
        kaynakKod = 'public class sınamalar { public static int çalıştır() { return 0; } static int 호출(int değer) { return değer; } }'
        self.derlemek_kaynak(kaynakKod, hedef='kernel', 내보냄='kernel_dispatch=sınamalar.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.dizin_değer / 'native')]))
        self.derlemek_kaynak(kaynakKod, 성공=False, 내보냄='bad;name=sınamalar.호출')
        self.derlemek_kaynak(kaynakKod, 성공=False, 내보냄='missing=sınamalar.없음')


if __name__ == '__main__':
    unittest.main()
