"""gangan_détà ELF ṣiṣẹ́_àṣẹ + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.àkójọpọ̀_fáìlì_iye = Path(self.임시.name)

    def ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun(self, orísun, 추가=None, 성공=True, àfojúsùn='linux', 내보냄=None):
        ọ̀nà_Àtòkọ = []
        for Orúkọ, Àkóónú_iye in dict({'시험': orísun}, **(추가 or {})).items():
            ọ̀nà = self.àkójọpọ̀_fáìlì_iye / (Orúkọ + '.java')
            ọ̀nà.write_text(Àkóónú_iye, encoding='utf-8')
            ọ̀nà_Àtòkọ.append(str(ọ̀nà))
        Àṣẹ = [sys.executable, str(컴파일러), '--target', àfojúsùn, '--entry', '시험.Rọ́ọ̀nù', '-o', str(self.àkójọpọ̀_fáìlì_iye / 'native')]
        if 내보냄 is not None: Àṣẹ += ['--export', 내보냄]
        결과 = subprocess.run(Àṣẹ + ọ̀nà_Àtòkọ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun àṣìṣe'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.àkójọpọ̀_fáìlì_iye / 'native')], timeout=5).returncode

    def 자바대조(self, orísun, 추가=None):
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun(orísun, 추가)
        (self.àkójọpọ̀_fáìlì_iye / 'olùpèsè.java').write_text(
            'public class olùpèsè { public static void main(String[] 인수) { System.exit(시험.Rọ́ọ̀nù()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.àkójọpọ̀_fáìlì_iye)] +
                       [str(ọ̀nà) for ọ̀nà in self.àkójọpọ̀_fáìlì_iye.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.àkójọpọ̀_fáìlì_iye), 'olùpèsè'], timeout=5).returncode
        gangan_détà = self.실행결과()
        self.assertGreaterEqual(gangan_détà, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ridájú)')
        self.assertEqual(gangan_détà, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Rọ́ọ̀nù() {
                int 합 = 7;
                int iye = 12345;
                for (int wá_atọ̀ka_àkóónú = -65; wá_atọ̀ka_àkóónú <= 65; wá_atọ̀ka_àkóónú++) {
                    iye = iye * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(iye, wá_atọ̀ka_àkóónú);
                    합 += (byte)iye + (short)iye + (char)iye;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] iye = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Rọ́ọ̀nù() {
                int 합 = 13;
                for (int 가 = 0; 가 < iye.length; 가++)
                    for (int 나 = 1; 나 < iye.length; 나++)
                        합 = 합 * 31 + iye[가] / iye[나] + iye[가] % iye[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Ṣẹ̀dá_ìgbéwọlé(int Ìwọ̀n) { return new int[Ìwọ̀n]; }
            public static int Rọ́ọ̀nù() {
                int[] 가 = Ṣẹ̀dá_ìgbéwọlé(8); int[] 나 = 가; int[] òfìfo_nǹkan = new int[0];
                if (가 != 나 || 가 == null || òfìfo_nǹkan.length != 0 || 가[7] != 0) return 99;
                int iye = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return iye + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int iye = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Rọ́ọ̀nù() { return 계산(1, 2, 3, 4, iye) + 보조.Kàá(); }
        }''', {'보조': '''public class 보조 {
            static int iye = 3;
            static int 초기값() { return ++iye; }
            static int Kàá() { return iye; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int iye = 보조.Kàá() + 1;
            public static int Rọ́ọ̀nù() { return iye * 10 + 보조.Kàá(); }
        }''', {'보조': '''public class 보조 {
            static int iye = 시험.iye + 2;
            static int Kàá() { return iye; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int Rọ́ọ̀nù() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ìsọdipúpọ̀(int iye) { return iye <= 1 ? 1 : iye * ìsọdipúpọ̀(iye - 1); }
            static int 연속(int iye) {
                switch (iye) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int iye) {
                switch (iye) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Rọ́ọ̀nù() { return (ìsọdipúpọ̀(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int iye{} = {};'.format(wá_atọ̀ka_àkóónú, wá_atọ̀ka_àkóónú) for wá_atọ̀ka_àkóónú in range(270))
        덧셈 = '+'.join('iye{}'.format(wá_atọ̀ka_àkóónú) for wá_atọ̀ka_àkóónú in range(270))
        self.자바대조('public class 시험 { public static int Rọ́ọ̀nù() {' + 선언 +
                    'iye_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] iye = null; return iye.length;', 102),
            ('int[] iye = new int[1]; return iye[1];', 103),
            ('int[] iye = new int[1]; iye[-1] = 3; return 0;', 103),
            ('int iye = -1; return new int[iye].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun('public class 시험 { public static int Rọ́ọ̀nù() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long iye; public static int Rọ́ọ̀nù() { return 0; }',
            'public static int Rọ́ọ̀nù() { Object iye = new Object(); return 0; }',
            'public static int Rọ́ọ̀nù() { System.out.println("hello"); return 0; }',
            'public static int Rọ́ọ̀nù() { try { return 1; } catch (Exception àṣìṣe) { return 2; } }',
            'public static synchronized int Rọ́ọ̀nù() { return 0; }',
            'public static int Rọ́ọ̀nù() { return new byte[3].length; }',
            'static native int 외부(); public static int Rọ́ọ̀nù() { return 외부(); }',
            'int iye; public static int Rọ́ọ̀nù() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.àkójọpọ̀_fáìlì_iye / 'native'
        출력.write_bytes(b'original-output')
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun('public class 시험 { public static int Rọ́ọ̀nù() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun('public class 시험 { public static int Rọ́ọ̀nù() { return 37; } }')
        self.assertEqual((self.àkójọpọ̀_fáìlì_iye / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.àkójọpọ̀_fáìlì_iye / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun('public class 시험 { public static int Rọ́ọ̀nù() { return aṣàmúlò.실행권한(); } }',
                    {'aṣàmúlò': 'public class aṣàmúlò { public static native int 실행권한(); }'}, àfojúsùn='user')
        détà = (self.àkójọpọ̀_fáìlì_iye / 'native').read_bytes()
        self.assertEqual(détà[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', détà, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.àkójọpọ̀_fáìlì_iye / 'native')]))
        # aṣàmúlò ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun('public class 시험 { public static int Rọ́ọ̀nù() { return ohun_èlò_iye.포트읽기(1); } }',
                    {'ohun_èlò_iye': 'public class ohun_èlò_iye { public static native int 포트읽기(int iye); }'}, 성공=False, àfojúsùn='user')

    def test_내보내기검증(self):
        orísun = 'public class 시험 { public static int Rọ́ọ̀nù() { return 0; } static int 호출(int iye) { return iye; } }'
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun(orísun, àfojúsùn='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.àkójọpọ̀_fáìlì_iye / 'native')]))
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun(orísun, 성공=False, 내보냄='bad;name=시험.호출')
        self.ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_orísun(orísun, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
