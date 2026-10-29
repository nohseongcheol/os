"""Na_hakika_Tarin_bayani ELF gudanar_Umarni + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.ma_ajiya_Daraja = Path(self.임시.name)

    def Gina_tushe(self, tushe, 추가=None, 성공=True, tageti='linux', 내보냄=None):
        Hanyar_shiga_Jeri = []
        for Suna, kunshiya_Daraja in dict({'시험': tushe}, **(추가 or {})).items():
            Hanyar_shiga = self.ma_ajiya_Daraja / (Suna + '.java')
            Hanyar_shiga.write_text(kunshiya_Daraja, encoding='utf-8')
            Hanyar_shiga_Jeri.append(str(Hanyar_shiga))
        Umarni = [sys.executable, str(컴파일러), '--target', tageti, '--entry', '시험.Tafiyar_da', '-o', str(self.ma_ajiya_Daraja / 'native')]
        if 내보냄 is not None: Umarni += ['--export', 내보냄]
        결과 = subprocess.run(Umarni + Hanyar_shiga_Jeri,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('Gina_tushe Kuskure'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.ma_ajiya_Daraja / 'native')], timeout=5).returncode

    def 자바대조(self, tushe, 추가=None):
        self.Gina_tushe(tushe, 추가)
        (self.ma_ajiya_Daraja / 'sauka.java').write_text(
            'public class sauka { public static void main(String[] 인수) { System.exit(시험.Tafiyar_da()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ma_ajiya_Daraja)] +
                       [str(Hanyar_shiga) for Hanyar_shiga in self.ma_ajiya_Daraja.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ma_ajiya_Daraja), 'sauka'], timeout=5).returncode
        Na_hakika_Tarin_bayani = self.실행결과()
        self.assertGreaterEqual(Na_hakika_Tarin_bayani, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 Tabbatar_da)')
        self.assertEqual(Na_hakika_Tarin_bayani, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Tafiyar_da() {
                int 합 = 7;
                int Daraja = 12345;
                for (int Indes = -65; Indes <= 65; Indes++) {
                    Daraja = Daraja * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(Daraja, Indes);
                    합 += (byte)Daraja + (short)Daraja + (char)Daraja;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] Daraja = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Tafiyar_da() {
                int 합 = 13;
                for (int 가 = 0; 가 < Daraja.length; 가++)
                    for (int 나 = 1; 나 < Daraja.length; 나++)
                        합 = 합 * 31 + Daraja[가] / Daraja[나] + Daraja[가] % Daraja[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ƙirƙíra_Mashigar_bayanai(int Girma) { return new int[Girma]; }
            public static int Tafiyar_da() {
                int[] 가 = ƙirƙíra_Mashigar_bayanai(8); int[] 나 = 가; int[] holoko_abu = new int[0];
                if (가 != 나 || 가 == null || holoko_abu.length != 0 || 가[7] != 0) return 99;
                int Daraja = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return Daraja + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int Daraja = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Tafiyar_da() { return 계산(1, 2, 3, 4, Daraja) + 보조.Yi_Karatu(); }
        }''', {'보조': '''public class 보조 {
            static int Daraja = 3;
            static int 초기값() { return ++Daraja; }
            static int Yi_Karatu() { return Daraja; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int Daraja = 보조.Yi_Karatu() + 1;
            public static int Tafiyar_da() { return Daraja * 10 + 보조.Yi_Karatu(); }
        }''', {'보조': '''public class 보조 {
            static int Daraja = 시험.Daraja + 2;
            static int Yi_Karatu() { return Daraja; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int Tafiyar_da() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktoriyal(int Daraja) { return Daraja <= 1 ? 1 : Daraja * faktoriyal(Daraja - 1); }
            static int 연속(int Daraja) {
                switch (Daraja) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int Daraja) {
                switch (Daraja) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Tafiyar_da() { return (faktoriyal(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        bayyanarwa = '\n'.join('int Daraja{} = {};'.format(Indes, Indes) for Indes in range(270))
        덧셈 = '+'.join('Daraja{}'.format(Indes) for Indes in range(270))
        self.자바대조('public class 시험 { public static int Tafiyar_da() {' + bayyanarwa +
                    'Daraja_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] Daraja = null; return Daraja.length;', 102),
            ('int[] Daraja = new int[1]; return Daraja[1];', 103),
            ('int[] Daraja = new int[1]; Daraja[-1] = 3; return 0;', 103),
            ('int Daraja = -1; return new int[Daraja].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for jiki_Daraja, 기대 in 경우들:
            with self.subTest(jiki_Daraja=jiki_Daraja):
                self.Gina_tushe('public class 시험 { public static int Tafiyar_da() { ' + jiki_Daraja + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long Daraja; public static int Tafiyar_da() { return 0; }',
            'public static int Tafiyar_da() { Object Daraja = new Object(); return 0; }',
            'public static int Tafiyar_da() { System.out.println("hello"); return 0; }',
            'public static int Tafiyar_da() { try { return 1; } catch (Exception Kuskure) { return 2; } }',
            'public static synchronized int Tafiyar_da() { return 0; }',
            'public static int Tafiyar_da() { return new byte[3].length; }',
            'static native int 외부(); public static int Tafiyar_da() { return 외부(); }',
            'int Daraja; public static int Tafiyar_da() { return 0; }',
        ]
        for jiki_Daraja in 경우들:
            with self.subTest(jiki_Daraja=jiki_Daraja):
                self.Gina_tushe('public class 시험 { ' + jiki_Daraja + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ma_ajiya_Daraja / 'native'
        출력.write_bytes(b'original-output')
        self.Gina_tushe('public class 시험 { public static int Tafiyar_da() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.Gina_tushe('public class 시험 { public static int Tafiyar_da() { return 37; } }')
        self.assertEqual((self.ma_ajiya_Daraja / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.ma_ajiya_Daraja / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.Gina_tushe('public class 시험 { public static int Tafiyar_da() { return Mai_anfani_da_kwamfuta.실행권한(); } }',
                    {'Mai_anfani_da_kwamfuta': 'public class Mai_anfani_da_kwamfuta { public static native int 실행권한(); }'}, tageti='user')
        Tarin_bayani = (self.ma_ajiya_Daraja / 'native').read_bytes()
        self.assertEqual(Tarin_bayani[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', Tarin_bayani, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ma_ajiya_Daraja / 'native')]))
        # Mai_anfani_da_kwamfuta ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.Gina_tushe('public class 시험 { public static int Tafiyar_da() { return na_ura_Daraja.포트읽기(1); } }',
                    {'na_ura_Daraja': 'public class na_ura_Daraja { public static native int 포트읽기(int Daraja); }'}, 성공=False, tageti='user')

    def test_내보내기검증(self):
        tushe = 'public class 시험 { public static int Tafiyar_da() { return 0; } static int 호출(int Daraja) { return Daraja; } }'
        self.Gina_tushe(tushe, tageti='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ma_ajiya_Daraja / 'native')]))
        self.Gina_tushe(tushe, 성공=False, 내보냄='bad;name=시험.호출')
        self.Gina_tushe(tushe, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
