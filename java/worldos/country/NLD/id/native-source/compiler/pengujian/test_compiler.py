"""aktual_data ELF Jalankan_perintah + OpenJDK hasil 대조. 임시 pengujian 자료만 생성한다."""
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
        self.Direktori_VALUE = Path(self.임시.name)

    def bangun_sumber(self, kodeSumber, tambah_entri=None, 성공=True, target='linux', 내보냄=None):
        jalur_Daftar = []
        for Nama_2, Isi_VALUE in dict({'pengujian': kodeSumber}, **(tambah_entri or {})).items():
            jalur = self.Direktori_VALUE / (Nama_2 + '.java')
            jalur.write_text(Isi_VALUE, encoding='utf-8')
            jalur_Daftar.append(str(jalur))
        perintah = [sys.executable, str(컴파일러), '--target', target, '--entry', 'pengujian.jalankan', '-o', str(self.Direktori_VALUE / 'native')]
        if 내보냄 is not None: perintah += ['--export', 내보냄]
        hasil = subprocess.run(perintah + jalur_Daftar,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(hasil.returncode, 0, hasil.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(hasil.returncode, 0)
            self.assertIn('bangun_sumber galat'.encode(), hasil.stderr)
        return hasil

    def 실행결과(self):
        return subprocess.run([str(self.Direktori_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, kodeSumber, tambah_entri=None):
        self.bangun_sumber(kodeSumber, tambah_entri)
        (self.Direktori_VALUE / 'host.java').write_text(
            'public class host { public static void main(String[] argumen) { System.exit(pengujian.jalankan()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Direktori_VALUE)] +
                       [str(jalur) for jalur in self.Direktori_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Direktori_VALUE), 'host'], timeout=5).returncode
        aktual_data = self.실행결과()
        self.assertGreaterEqual(aktual_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 periksa)')
        self.assertEqual(aktual_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class pengujian {
            static int 섞기(int 가, int SECOND_operand) {
                return ((가 + SECOND_operand) ^ (가 - SECOND_operand) ^ (가 * SECOND_operand) ^ (가 & SECOND_operand) ^ (가 | SECOND_operand))
                    + (가 << SECOND_operand) + (가 >> SECOND_operand) + (가 >>> SECOND_operand);
            }
            public static int jalankan() {
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
        self.자바대조('''public class pengujian {
            static int[] VALUE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int jalankan() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operand = 1; SECOND_operand < VALUE.length; SECOND_operand++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operand] + VALUE[가] % VALUE[SECOND_operand];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class pengujian {
            static int[] Buat_entri(int Ukuran) { return new int[Ukuran]; }
            public static int jalankan() {
                int[] 가 = Buat_entri(8); int[] SECOND_operand = 가; int[] kosong_objek = new int[0];
                if (가 != SECOND_operand || 가 == null || kosong_objek.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + SECOND_operand[2] + SECOND_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class pengujian {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int SECOND_operand, int 다, int 라, int 마) {
                return 가 + SECOND_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int jalankan() { return 계산(1, 2, 3, 4, VALUE) + 보조.Baca(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Baca() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class pengujian {
            static int VALUE = 보조.Baca() + 1;
            public static int jalankan() { return VALUE * 10 + 보조.Baca(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = pengujian.VALUE + 2;
            static int Baca() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class pengujian {
            static String teks = "한글\\u0000😀";
            public static int jalankan() {
                if (teks != "한글\\u0000😀") return 99;
                return (teks.length() + teks.charAt(2) + teks.charAt(3) + teks.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class pengujian {
            static int faktorial(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktorial(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int jalankan() { return (faktorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklarasi_4f4f026b = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class pengujian { public static int jalankan() {' + deklarasi_4f4f026b +
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
        for isi_VALUE_c6cb974f, 기대 in 경우들:
            with self.subTest(isi_VALUE_c6cb974f=isi_VALUE_c6cb974f):
                self.bangun_sumber('public class pengujian { public static int jalankan() { ' + isi_VALUE_c6cb974f + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int jalankan() { return 0; }',
            'public static int jalankan() { Object VALUE = new Object(); return 0; }',
            'public static int jalankan() { System.out.println("hello"); return 0; }',
            'public static int jalankan() { try { return 1; } catch (Exception galat) { return 2; } }',
            'public static synchronized int jalankan() { return 0; }',
            'public static int jalankan() { return new byte[3].length; }',
            'static native int eksternal_VALUE(); public static int jalankan() { return eksternal_VALUE(); }',
            'int VALUE; public static int jalankan() { return 0; }',
        ]
        for isi_VALUE_c6cb974f in 경우들:
            with self.subTest(isi_VALUE_c6cb974f=isi_VALUE_c6cb974f):
                self.bangun_sumber('public class pengujian { ' + isi_VALUE_c6cb974f + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        keluaranTeks = self.Direktori_VALUE / 'native'
        keluaranTeks.write_bytes(b'original-output')
        self.bangun_sumber('public class pengujian { public static int jalankan() { return missing; } }', 성공=False)
        self.assertEqual(keluaranTeks.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.bangun_sumber('public class pengujian { public static int jalankan() { return 37; } }')
        self.assertEqual((self.Direktori_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_tabel = subprocess.check_output(['readelf', '-l', str(self.Direktori_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_tabel)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.bangun_sumber('public class pengujian { public static int jalankan() { return ruang_pengguna.실행권한(); } }',
                    {'ruang_pengguna': 'public class ruang_pengguna { public static native int 실행권한(); }'}, target='user')
        data = (self.Direktori_VALUE / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Direktori_VALUE / 'native')]))
        # ruang_pengguna ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.bangun_sumber('public class pengujian { public static int jalankan() { return Ponsel_VALUE.포트읽기(1); } }',
                    {'Ponsel_VALUE': 'public class Ponsel_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, target='user')

    def test_내보내기검증(self):
        kodeSumber = 'public class pengujian { public static int jalankan() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.bangun_sumber(kodeSumber, target='kernel', 내보냄='kernel_dispatch=pengujian.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Direktori_VALUE / 'native')]))
        self.bangun_sumber(kodeSumber, 성공=False, 내보냄='bad;name=pengujian.호출')
        self.bangun_sumber(kodeSumber, 성공=False, 내보냄='missing=pengujian.없음')


if __name__ == '__main__':
    unittest.main()
