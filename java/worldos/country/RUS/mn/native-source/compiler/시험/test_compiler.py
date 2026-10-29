"""бодит_өгөгдөл ELF Гүйцэтгэх_команд + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.лавлах_утга = Path(self.임시.name)

    def хөрвүүлэх_эх(self, ЭХ, 추가=None, 성공=True, зорилго='linux', 내보냄=None):
        зам_Жагсаалт = []
        for Нэр, Агуулга_утга in dict({'시험': ЭХ}, **(추가 or {})).items():
            ЗАМ = self.лавлах_утга / (Нэр + '.java')
            ЗАМ.write_text(Агуулга_утга, encoding='utf-8')
            зам_Жагсаалт.append(str(ЗАМ))
        Тушаал = [sys.executable, str(컴파일러), '--target', зорилго, '--entry', '시험.Ажиллуулах', '-o', str(self.лавлах_утга / 'native')]
        if 내보냄 is not None: Тушаал += ['--export', 내보냄]
        결과 = subprocess.run(Тушаал + зам_Жагсаалт,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('хөрвүүлэх_эх Алдаа'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.лавлах_утга / 'native')], timeout=5).returncode

    def 자바대조(self, ЭХ, 추가=None):
        self.хөрвүүлэх_эх(ЭХ, 추가)
        (self.лавлах_утга / 'хост.java').write_text(
            'public class хост { public static void main(String[] 인수) { System.exit(시험.Ажиллуулах()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.лавлах_утга)] +
                       [str(ЗАМ) for ЗАМ in self.лавлах_утга.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.лавлах_утга), 'хост'], timeout=5).returncode
        бодит_өгөгдөл = self.실행결과()
        self.assertGreaterEqual(бодит_өгөгдөл, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 шалгах)')
        self.assertEqual(бодит_өгөгдөл, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Ажиллуулах() {
                int 합 = 7;
                int утга = 12345;
                for (int индекс = -65; индекс <= 65; индекс++) {
                    утга = утга * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(утга, индекс);
                    합 += (byte)утга + (short)утга + (char)утга;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] утга = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Ажиллуулах() {
                int 합 = 13;
                for (int 가 = 0; 가 < утга.length; 가++)
                    for (int 나 = 1; 나 < утга.length; 나++)
                        합 = 합 * 31 + утга[가] / утга[나] + утга[가] % утга[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] үүсгэх_оролт(int Хэмжээ) { return new int[Хэмжээ]; }
            public static int Ажиллуулах() {
                int[] 가 = үүсгэх_оролт(8); int[] 나 = 가; int[] хоосон_объект = new int[0];
                if (가 != 나 || 가 == null || хоосон_объект.length != 0 || 가[7] != 0) return 99;
                int утга = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return утга + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int утга = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Ажиллуулах() { return 계산(1, 2, 3, 4, утга) + 보조.Унших(); }
        }''', {'보조': '''public class 보조 {
            static int утга = 3;
            static int 초기값() { return ++утга; }
            static int Унших() { return утга; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int утга = 보조.Унших() + 1;
            public static int Ажиллуулах() { return утга * 10 + 보조.Унших(); }
        }''', {'보조': '''public class 보조 {
            static int утга = 시험.утга + 2;
            static int Унших() { return утга; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Бичвэр = "한글\\u0000😀";
            public static int Ажиллуулах() {
                if (Бичвэр != "한글\\u0000😀") return 99;
                return (Бичвэр.length() + Бичвэр.charAt(2) + Бичвэр.charAt(3) + Бичвэр.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int хүчин_зүйлийн(int утга) { return утга <= 1 ? 1 : утга * хүчин_зүйлийн(утга - 1); }
            static int 연속(int утга) {
                switch (утга) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int утга) {
                switch (утга) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Ажиллуулах() { return (хүчин_зүйлийн(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int утга{} = {};'.format(индекс, индекс) for индекс in range(270))
        덧셈 = '+'.join('утга{}'.format(индекс) for индекс in range(270))
        self.자바대조('public class 시험 { public static int Ажиллуулах() {' + 선언 +
                    'утга_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] утга = null; return утга.length;', 102),
            ('int[] утга = new int[1]; return утга[1];', 103),
            ('int[] утга = new int[1]; утга[-1] = 3; return 0;', 103),
            ('int утга = -1; return new int[утга].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.хөрвүүлэх_эх('public class 시험 { public static int Ажиллуулах() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long утга; public static int Ажиллуулах() { return 0; }',
            'public static int Ажиллуулах() { Object утга = new Object(); return 0; }',
            'public static int Ажиллуулах() { System.out.println("hello"); return 0; }',
            'public static int Ажиллуулах() { try { return 1; } catch (Exception Алдаа) { return 2; } }',
            'public static synchronized int Ажиллуулах() { return 0; }',
            'public static int Ажиллуулах() { return new byte[3].length; }',
            'static native int 외부(); public static int Ажиллуулах() { return 외부(); }',
            'int утга; public static int Ажиллуулах() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.хөрвүүлэх_эх('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.лавлах_утга / 'native'
        출력.write_bytes(b'original-output')
        self.хөрвүүлэх_эх('public class 시험 { public static int Ажиллуулах() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.хөрвүүлэх_эх('public class 시험 { public static int Ажиллуулах() { return 37; } }')
        self.assertEqual((self.лавлах_утга / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.лавлах_утга / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.хөрвүүлэх_эх('public class 시험 { public static int Ажиллуулах() { return хэрэглэгч.실행권한(); } }',
                    {'хэрэглэгч': 'public class хэрэглэгч { public static native int 실행권한(); }'}, зорилго='user')
        өгөгдөл = (self.лавлах_утга / 'native').read_bytes()
        self.assertEqual(өгөгдөл[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', өгөгдөл, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.лавлах_утга / 'native')]))
        # хэрэглэгч ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.хөрвүүлэх_эх('public class 시험 { public static int Ажиллуулах() { return гар_утас_утга.포트읽기(1); } }',
                    {'гар_утас_утга': 'public class гар_утас_утга { public static native int 포트읽기(int утга); }'}, 성공=False, зорилго='user')

    def test_내보내기검증(self):
        ЭХ = 'public class 시험 { public static int Ажиллуулах() { return 0; } static int 호출(int утга) { return утга; } }'
        self.хөрвүүлэх_эх(ЭХ, зорилго='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.лавлах_утга / 'native')]))
        self.хөрвүүлэх_эх(ЭХ, 성공=False, 내보냄='bad;name=시험.호출')
        self.хөрвүүлэх_эх(ЭХ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
