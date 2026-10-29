"""tota_tshedimosetso ELF diragatsa_Taelo + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.Lenaneofaele_Boleng = Path(self.임시.name)

    def aga_Motswedi(self, Motswedi, 추가=None, 성공=True, setotwa='linux', 내보냄=None):
        tsela_lenaane = []
        for leina, Diteng_Boleng in dict({'시험': Motswedi}, **(추가 or {})).items():
            tsela = self.Lenaneofaele_Boleng / (leina + '.java')
            tsela.write_text(Diteng_Boleng, encoding='utf-8')
            tsela_lenaane.append(str(tsela))
        Taelo = [sys.executable, str(컴파일러), '--target', setotwa, '--entry', '시험.dirisa', '-o', str(self.Lenaneofaele_Boleng / 'native')]
        if 내보냄 is not None: Taelo += ['--export', 내보냄]
        결과 = subprocess.run(Taelo + tsela_lenaane,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('aga_Motswedi phoso'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.Lenaneofaele_Boleng / 'native')], timeout=5).returncode

    def 자바대조(self, Motswedi, 추가=None):
        self.aga_Motswedi(Motswedi, 추가)
        (self.Lenaneofaele_Boleng / 'pinagare.java').write_text(
            'public class pinagare { public static void main(String[] 인수) { System.exit(시험.dirisa()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Lenaneofaele_Boleng)] +
                       [str(tsela) for tsela in self.Lenaneofaele_Boleng.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Lenaneofaele_Boleng), 'pinagare'], timeout=5).returncode
        tota_tshedimosetso = self.실행결과()
        self.assertGreaterEqual(tota_tshedimosetso, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 netefatsa)')
        self.assertEqual(tota_tshedimosetso, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int dirisa() {
                int 합 = 7;
                int Boleng = 12345;
                for (int tshupane = -65; tshupane <= 65; tshupane++) {
                    Boleng = Boleng * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(Boleng, tshupane);
                    합 += (byte)Boleng + (short)Boleng + (char)Boleng;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] Boleng = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int dirisa() {
                int 합 = 13;
                for (int 가 = 0; 가 < Boleng.length; 가++)
                    for (int 나 = 1; 나 < Boleng.length; 나++)
                        합 = 합 * 31 + Boleng[가] / Boleng[나] + Boleng[가] % Boleng[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] tlhama_tsenyo(int lekanya) { return new int[lekanya]; }
            public static int dirisa() {
                int[] 가 = tlhama_tsenyo(8); int[] 나 = 가; int[] lolea_selwana = new int[0];
                if (가 != 나 || 가 == null || lolea_selwana.length != 0 || 가[7] != 0) return 99;
                int Boleng = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return Boleng + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int Boleng = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int dirisa() { return 계산(1, 2, 3, 4, Boleng) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int Boleng = 3;
            static int 초기값() { return ++Boleng; }
            static int 읽기() { return Boleng; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int Boleng = 보조.읽기() + 1;
            public static int dirisa() { return Boleng * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int Boleng = 시험.Boleng + 2;
            static int 읽기() { return Boleng; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int dirisa() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int dipalo_tsa_feketoriale(int Boleng) { return Boleng <= 1 ? 1 : Boleng * dipalo_tsa_feketoriale(Boleng - 1); }
            static int 연속(int Boleng) {
                switch (Boleng) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int Boleng) {
                switch (Boleng) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int dirisa() { return (dipalo_tsa_feketoriale(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int Boleng{} = {};'.format(tshupane, tshupane) for tshupane in range(270))
        덧셈 = '+'.join('Boleng{}'.format(tshupane) for tshupane in range(270))
        self.자바대조('public class 시험 { public static int dirisa() {' + 선언 +
                    'Boleng_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] Boleng = null; return Boleng.length;', 102),
            ('int[] Boleng = new int[1]; return Boleng[1];', 103),
            ('int[] Boleng = new int[1]; Boleng[-1] = 3; return 0;', 103),
            ('int Boleng = -1; return new int[Boleng].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.aga_Motswedi('public class 시험 { public static int dirisa() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long Boleng; public static int dirisa() { return 0; }',
            'public static int dirisa() { Object Boleng = new Object(); return 0; }',
            'public static int dirisa() { System.out.println("hello"); return 0; }',
            'public static int dirisa() { try { return 1; } catch (Exception phoso) { return 2; } }',
            'public static synchronized int dirisa() { return 0; }',
            'public static int dirisa() { return new byte[3].length; }',
            'static native int 외부(); public static int dirisa() { return 외부(); }',
            'int Boleng; public static int dirisa() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.aga_Motswedi('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.Lenaneofaele_Boleng / 'native'
        출력.write_bytes(b'original-output')
        self.aga_Motswedi('public class 시험 { public static int dirisa() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.aga_Motswedi('public class 시험 { public static int dirisa() { return 37; } }')
        self.assertEqual((self.Lenaneofaele_Boleng / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.Lenaneofaele_Boleng / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.aga_Motswedi('public class 시험 { public static int dirisa() { return modirisi.실행권한(); } }',
                    {'modirisi': 'public class modirisi { public static native int 실행권한(); }'}, setotwa='user')
        tshedimosetso = (self.Lenaneofaele_Boleng / 'native').read_bytes()
        self.assertEqual(tshedimosetso[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', tshedimosetso, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Lenaneofaele_Boleng / 'native')]))
        # modirisi ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.aga_Motswedi('public class 시험 { public static int dirisa() { return mobaele_Boleng.포트읽기(1); } }',
                    {'mobaele_Boleng': 'public class mobaele_Boleng { public static native int 포트읽기(int Boleng); }'}, 성공=False, setotwa='user')

    def test_내보내기검증(self):
        Motswedi = 'public class 시험 { public static int dirisa() { return 0; } static int 호출(int Boleng) { return Boleng; } }'
        self.aga_Motswedi(Motswedi, setotwa='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Lenaneofaele_Boleng / 'native')]))
        self.aga_Motswedi(Motswedi, 성공=False, 내보냄='bad;name=시험.호출')
        self.aga_Motswedi(Motswedi, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
