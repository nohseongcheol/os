"""sebenar_data ELF laksanakan_perintah + OpenJDK ukuran 대조. 임시 ujian 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class ujian_asal(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.direktori_VALUE = Path(self.임시.name)

    def bina_sumber(self, SUMBER, Tambah_pemasukan=None, 성공=True, sasaran='linux', 내보냄=None):
        laluan_Senarai = []
        for Nama, Kandungan_VALUE in dict({'ujian': SUMBER}, **(Tambah_pemasukan or {})).items():
            LALUAN = self.direktori_VALUE / (Nama + '.java')
            LALUAN.write_text(Kandungan_VALUE, encoding='utf-8')
            laluan_Senarai.append(str(LALUAN))
        Perintah = [sys.executable, str(컴파일러), '--target', sasaran, '--entry', 'ujian.Jalan', '-o', str(self.direktori_VALUE / 'native')]
        if 내보냄 is not None: Perintah += ['--export', 내보냄]
        ukuran = subprocess.run(Perintah + laluan_Senarai,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ukuran.returncode, 0, ukuran.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ukuran.returncode, 0)
            self.assertIn('bina_sumber RALAT'.encode(), ukuran.stderr)
        return ukuran

    def 실행결과(self):
        return subprocess.run([str(self.direktori_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, SUMBER, Tambah_pemasukan=None):
        self.bina_sumber(SUMBER, Tambah_pemasukan)
        (self.direktori_VALUE / 'hos.java').write_text(
            'public class hos { public static void main(String[] 인수) { System.exit(ujian.Jalan()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.direktori_VALUE)] +
                       [str(LALUAN) for LALUAN in self.direktori_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.direktori_VALUE), 'hos'], timeout=5).returncode
        sebenar_data = self.실행결과()
        self.assertGreaterEqual(sebenar_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 tentu_sahkan)')
        self.assertEqual(sebenar_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class ujian {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Jalan() {
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
        self.자바대조('''public class ujian {
            static int[] VALUE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Jalan() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int 나 = 1; 나 < VALUE.length; 나++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[나] + VALUE[가] % VALUE[나];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class ujian {
            static int[] cipta_pemasukan(int Saiz) { return new int[Saiz]; }
            public static int Jalan() {
                int[] 가 = cipta_pemasukan(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class ujian {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Jalan() { return 계산(1, 2, 3, 4, VALUE) + 보조.Baca(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Baca() { return VALUE; }
        }'''})

    def ujian_pengawalan_Kitaran(self):
        self.자바대조('''public class ujian {
            static int VALUE = 보조.Baca() + 1;
            public static int Jalan() { return VALUE * 10 + 보조.Baca(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = ujian.VALUE + 2;
            static int Baca() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class ujian {
            static String Teks = "한글\\u0000😀";
            public static int Jalan() {
                if (Teks != "한글\\u0000😀") return 99;
                return (Teks.length() + Teks.charAt(2) + Teks.charAt(3) + Teks.charAt(4)) % 251;
            }
        }''')

    def ujian_tukar_AND_rekursi(self):
        self.자바대조('''public class ujian {
            static int faktorial(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktorial(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Jalan() { return (faktorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        pengisytiharan_4f4f026b = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class ujian { public static int Jalan() {' + pengisytiharan_4f4f026b +
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
                self.bina_sumber('public class ujian { public static int Jalan() { ' + isi_VALUE_c6cb974f + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Jalan() { return 0; }',
            'public static int Jalan() { Object VALUE = new Object(); return 0; }',
            'public static int Jalan() { System.out.println("hello"); return 0; }',
            'public static int Jalan() { try { return 1; } catch (Exception RALAT) { return 2; } }',
            'public static synchronized int Jalan() { return 0; }',
            'public static int Jalan() { return new byte[3].length; }',
            'static native int 외부(); public static int Jalan() { return 외부(); }',
            'int VALUE; public static int Jalan() { return 0; }',
        ]
        for isi_VALUE_c6cb974f in 경우들:
            with self.subTest(isi_VALUE_c6cb974f=isi_VALUE_c6cb974f):
                self.bina_sumber('public class ujian { ' + isi_VALUE_c6cb974f + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.direktori_VALUE / 'native'
        출력.write_bytes(b'original-output')
        self.bina_sumber('public class ujian { public static int Jalan() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.bina_sumber('public class ujian { public static int Jalan() { return 37; } }')
        self.assertEqual((self.direktori_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Carian_jadual = subprocess.check_output(['readelf', '-l', str(self.direktori_VALUE / 'native')])
        self.assertNotIn(b'INTERP', Carian_jadual)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.bina_sumber('public class ujian { public static int Jalan() { return ruang_pengguna.실행권한(); } }',
                    {'ruang_pengguna': 'public class ruang_pengguna { public static native int 실행권한(); }'}, sasaran='user')
        data = (self.direktori_VALUE / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.direktori_VALUE / 'native')]))
        # ruang_pengguna ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.bina_sumber('public class ujian { public static int Jalan() { return peranti_VALUE.포트읽기(1); } }',
                    {'peranti_VALUE': 'public class peranti_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, sasaran='user')

    def ujian_Eksport_pensahihan(self):
        SUMBER = 'public class ujian { public static int Jalan() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.bina_sumber(SUMBER, sasaran='kernel', 내보냄='kernel_dispatch=ujian.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.direktori_VALUE / 'native')]))
        self.bina_sumber(SUMBER, 성공=False, 내보냄='bad;name=ujian.호출')
        self.bina_sumber(SUMBER, 성공=False, 내보냄='missing=ujian.없음')


if __name__ == '__main__':
    unittest.main()
