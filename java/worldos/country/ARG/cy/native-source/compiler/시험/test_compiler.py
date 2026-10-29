"""go_iawn_data ELF Gweithredu_gorchymyn + OpenJDK mesur 대조. 임시 시험 자료만 생성한다."""
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
        self.cyfeiriadur_VALUE = Path(self.임시.name)

    def llunio_ffynhonnell(self, FFYNHONNELL, 추가=None, 성공=True, targed='linux', 내보냄=None):
        llwybr_Rhestr = []
        for Enw, Cynnwys_VALUE in dict({'시험': FFYNHONNELL}, **(추가 or {})).items():
            LLWYBR = self.cyfeiriadur_VALUE / (Enw + '.java')
            LLWYBR.write_text(Cynnwys_VALUE, encoding='utf-8')
            llwybr_Rhestr.append(str(LLWYBR))
        Gorchymyn = [sys.executable, str(컴파일러), '--target', targed, '--entry', '시험.Gweithredu_2', '-o', str(self.cyfeiriadur_VALUE / 'native')]
        if 내보냄 is not None: Gorchymyn += ['--export', 내보냄]
        mesur = subprocess.run(Gorchymyn + llwybr_Rhestr,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(mesur.returncode, 0, mesur.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(mesur.returncode, 0)
            self.assertIn('llunio_ffynhonnell Gwall'.encode(), mesur.stderr)
        return mesur

    def 실행결과(self):
        return subprocess.run([str(self.cyfeiriadur_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, FFYNHONNELL, 추가=None):
        self.llunio_ffynhonnell(FFYNHONNELL, 추가)
        (self.cyfeiriadur_VALUE / 'lletya.java').write_text(
            'public class lletya { public static void main(String[] 인수) { System.exit(시험.Gweithredu_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.cyfeiriadur_VALUE)] +
                       [str(LLWYBR) for LLWYBR in self.cyfeiriadur_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.cyfeiriadur_VALUE), 'lletya'], timeout=5).returncode
        go_iawn_data = self.실행결과()
        self.assertGreaterEqual(go_iawn_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 dilysu)')
        self.assertEqual(go_iawn_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Gweithredu_2() {
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
        self.자바대조('''public class 시험 {
            static int[] VALUE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Gweithredu_2() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int 나 = 1; 나 < VALUE.length; 나++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[나] + VALUE[가] % VALUE[나];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Creu_cofnod(int Maint) { return new int[Maint]; }
            public static int Gweithredu_2() {
                int[] 가 = Creu_cofnod(8); int[] 나 = 가; int[] gwag_gwrthrych = new int[0];
                if (가 != 나 || 가 == null || gwag_gwrthrych.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Gweithredu_2() { return 계산(1, 2, 3, 4, VALUE) + 보조.Darllen(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Darllen() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Darllen() + 1;
            public static int Gweithredu_2() { return VALUE * 10 + 보조.Darllen(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Darllen() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Testun = "한글\\u0000😀";
            public static int Gweithredu_2() {
                if (Testun != "한글\\u0000😀") return 99;
                return (Testun.length() + Testun.charAt(2) + Testun.charAt(3) + Testun.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ffactorol(int VALUE) { return VALUE <= 1 ? 1 : VALUE * ffactorol(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Gweithredu_2() { return (ffactorol(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Gweithredu_2() {' + 선언 +
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
        for corff_VALUE, 기대 in 경우들:
            with self.subTest(corff_VALUE=corff_VALUE):
                self.llunio_ffynhonnell('public class 시험 { public static int Gweithredu_2() { ' + corff_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Gweithredu_2() { return 0; }',
            'public static int Gweithredu_2() { Object VALUE = new Object(); return 0; }',
            'public static int Gweithredu_2() { System.out.println("hello"); return 0; }',
            'public static int Gweithredu_2() { try { return 1; } catch (Exception Gwall) { return 2; } }',
            'public static synchronized int Gweithredu_2() { return 0; }',
            'public static int Gweithredu_2() { return new byte[3].length; }',
            'static native int 외부(); public static int Gweithredu_2() { return 외부(); }',
            'int VALUE; public static int Gweithredu_2() { return 0; }',
        ]
        for corff_VALUE in 경우들:
            with self.subTest(corff_VALUE=corff_VALUE):
                self.llunio_ffynhonnell('public class 시험 { ' + corff_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Allbwn = self.cyfeiriadur_VALUE / 'native'
        Allbwn.write_bytes(b'original-output')
        self.llunio_ffynhonnell('public class 시험 { public static int Gweithredu_2() { return missing; } }', 성공=False)
        self.assertEqual(Allbwn.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.llunio_ffynhonnell('public class 시험 { public static int Gweithredu_2() { return 37; } }')
        self.assertEqual((self.cyfeiriadur_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_tabl = subprocess.check_output(['readelf', '-l', str(self.cyfeiriadur_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_tabl)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.llunio_ffynhonnell('public class 시험 { public static int Gweithredu_2() { return defnyddiwr.실행권한(); } }',
                    {'defnyddiwr': 'public class defnyddiwr { public static native int 실행권한(); }'}, targed='user')
        data = (self.cyfeiriadur_VALUE / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.cyfeiriadur_VALUE / 'native')]))
        # defnyddiwr ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.llunio_ffynhonnell('public class 시험 { public static int Gweithredu_2() { return dyfais_VALUE.포트읽기(1); } }',
                    {'dyfais_VALUE': 'public class dyfais_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, targed='user')

    def test_내보내기검증(self):
        FFYNHONNELL = 'public class 시험 { public static int Gweithredu_2() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.llunio_ffynhonnell(FFYNHONNELL, targed='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.cyfeiriadur_VALUE / 'native')]))
        self.llunio_ffynhonnell(FFYNHONNELL, 성공=False, 내보냄='bad;name=시험.호출')
        self.llunio_ffynhonnell(FFYNHONNELL, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
