"""ulwazi_ngokwenzekile_imininingwane ELF yenza_umyalo + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.umkhombandlela_inani = Path(self.임시.name)

    def akha_umthombo(self, umthombo, 추가=None, 성공=True, impokophelo='linux', 내보냄=None):
        umzila_Uhlu = []
        for Igama, Okuqukethwe_inani in dict({'시험': umthombo}, **(추가 or {})).items():
            Indlela_2 = self.umkhombandlela_inani / (Igama + '.java')
            Indlela_2.write_text(Okuqukethwe_inani, encoding='utf-8')
            umzila_Uhlu.append(str(Indlela_2))
        Umlayelo = [sys.executable, str(컴파일러), '--target', impokophelo, '--entry', '시험.Sebenzisa', '-o', str(self.umkhombandlela_inani / 'native')]
        if 내보냄 is not None: Umlayelo += ['--export', 내보냄]
        결과 = subprocess.run(Umlayelo + umzila_Uhlu,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('akha_umthombo Iphutha'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.umkhombandlela_inani / 'native')], timeout=5).returncode

    def 자바대조(self, umthombo, 추가=None):
        self.akha_umthombo(umthombo, 추가)
        (self.umkhombandlela_inani / 'singatha.java').write_text(
            'public class singatha { public static void main(String[] 인수) { System.exit(시험.Sebenzisa()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.umkhombandlela_inani)] +
                       [str(Indlela_2) for Indlela_2 in self.umkhombandlela_inani.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.umkhombandlela_inani), 'singatha'], timeout=5).returncode
        ulwazi_ngokwenzekile_imininingwane = self.실행결과()
        self.assertGreaterEqual(ulwazi_ngokwenzekile_imininingwane, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 qiniseka)')
        self.assertEqual(ulwazi_ngokwenzekile_imininingwane, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Sebenzisa() {
                int 합 = 7;
                int inani = 12345;
                for (int thola_inkomba = -65; thola_inkomba <= 65; thola_inkomba++) {
                    inani = inani * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(inani, thola_inkomba);
                    합 += (byte)inani + (short)inani + (char)inani;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] inani = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Sebenzisa() {
                int 합 = 13;
                for (int 가 = 0; 가 < inani.length; 가++)
                    for (int 나 = 1; 나 < inani.length; 나++)
                        합 = 합 * 31 + inani[가] / inani[나] + inani[가] % inani[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] yakha_okufakwayo(int Ubungako) { return new int[Ubungako]; }
            public static int Sebenzisa() {
                int[] 가 = yakha_okufakwayo(8); int[] 나 = 가; int[] okungasho_lutho_into = new int[0];
                if (가 != 나 || 가 == null || okungasho_lutho_into.length != 0 || 가[7] != 0) return 99;
                int inani = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return inani + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int inani = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Sebenzisa() { return 계산(1, 2, 3, 4, inani) + 보조.Funda(); }
        }''', {'보조': '''public class 보조 {
            static int inani = 3;
            static int 초기값() { return ++inani; }
            static int Funda() { return inani; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int inani = 보조.Funda() + 1;
            public static int Sebenzisa() { return inani * 10 + 보조.Funda(); }
        }''', {'보조': '''public class 보조 {
            static int inani = 시험.inani + 2;
            static int Funda() { return inani; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Itekisi = "한글\\u0000😀";
            public static int Sebenzisa() {
                if (Itekisi != "한글\\u0000😀") return 99;
                return (Itekisi.length() + Itekisi.charAt(2) + Itekisi.charAt(3) + Itekisi.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ifakthoriyali(int inani) { return inani <= 1 ? 1 : inani * ifakthoriyali(inani - 1); }
            static int 연속(int inani) {
                switch (inani) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int inani) {
                switch (inani) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Sebenzisa() { return (ifakthoriyali(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int inani{} = {};'.format(thola_inkomba, thola_inkomba) for thola_inkomba in range(270))
        덧셈 = '+'.join('inani{}'.format(thola_inkomba) for thola_inkomba in range(270))
        self.자바대조('public class 시험 { public static int Sebenzisa() {' + 선언 +
                    'inani_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] inani = null; return inani.length;', 102),
            ('int[] inani = new int[1]; return inani[1];', 103),
            ('int[] inani = new int[1]; inani[-1] = 3; return 0;', 103),
            ('int inani = -1; return new int[inani].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.akha_umthombo('public class 시험 { public static int Sebenzisa() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long inani; public static int Sebenzisa() { return 0; }',
            'public static int Sebenzisa() { Object inani = new Object(); return 0; }',
            'public static int Sebenzisa() { System.out.println("hello"); return 0; }',
            'public static int Sebenzisa() { try { return 1; } catch (Exception Iphutha) { return 2; } }',
            'public static synchronized int Sebenzisa() { return 0; }',
            'public static int Sebenzisa() { return new byte[3].length; }',
            'static native int 외부(); public static int Sebenzisa() { return 외부(); }',
            'int inani; public static int Sebenzisa() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.akha_umthombo('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.umkhombandlela_inani / 'native'
        출력.write_bytes(b'original-output')
        self.akha_umthombo('public class 시험 { public static int Sebenzisa() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.akha_umthombo('public class 시험 { public static int Sebenzisa() { return 37; } }')
        self.assertEqual((self.umkhombandlela_inani / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.umkhombandlela_inani / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.akha_umthombo('public class 시험 { public static int Sebenzisa() { return umsebenzisi.실행권한(); } }',
                    {'umsebenzisi': 'public class umsebenzisi { public static native int 실행권한(); }'}, impokophelo='user')
        imininingwane = (self.umkhombandlela_inani / 'native').read_bytes()
        self.assertEqual(imininingwane[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', imininingwane, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.umkhombandlela_inani / 'native')]))
        # umsebenzisi ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.akha_umthombo('public class 시험 { public static int Sebenzisa() { return idivayisi_inani.포트읽기(1); } }',
                    {'idivayisi_inani': 'public class idivayisi_inani { public static native int 포트읽기(int inani); }'}, 성공=False, impokophelo='user')

    def test_내보내기검증(self):
        umthombo = 'public class 시험 { public static int Sebenzisa() { return 0; } static int 호출(int inani) { return inani; } }'
        self.akha_umthombo(umthombo, impokophelo='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.umkhombandlela_inani / 'native')]))
        self.akha_umthombo(umthombo, 성공=False, 내보냄='bad;name=시험.호출')
        self.akha_umthombo(umthombo, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
