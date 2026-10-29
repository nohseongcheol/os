"""ਅਸਲ_ਸਮੱਗਰੀ ELF ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ + OpenJDK ਮਾਪ 대조. 임시 시험 자료만 생성한다."""
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
        self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ = Path(self.임시.name)

    def ਬਣਾਊਣਾ_ਸਰੋਤ(self, ਸਰੋਤ, 추가=None, 성공=True, ਟੀਚਾ='linux', 내보냄=None):
        ਰਸਤਾ_ਸੂਚੀ = []
        for ਨਾਂ, ਤਤਕਰਾ_ਕੀਮਤ in dict({'시험': ਸਰੋਤ}, **(추가 or {})).items():
            ਮਾਰਗ = self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.java')
            ਮਾਰਗ.write_text(ਤਤਕਰਾ_ਕੀਮਤ, encoding='utf-8')
            ਰਸਤਾ_ਸੂਚੀ.append(str(ਮਾਰਗ))
        ਕਮਾਂਡ = [sys.executable, str(컴파일러), '--target', ਟੀਚਾ, '--entry', '시험.ਚਲਾਓ_2', '-o', str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native')]
        if 내보냄 is not None: ਕਮਾਂਡ += ['--export', 내보냄]
        ਮਾਪ = subprocess.run(ਕਮਾਂਡ + ਰਸਤਾ_ਸੂਚੀ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ਮਾਪ.returncode, 0, ਮਾਪ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ਮਾਪ.returncode, 0)
            self.assertIn('ਬਣਾਊਣਾ_ਸਰੋਤ ਗਲਤੀ'.encode(), ਮਾਪ.stderr)
        return ਮਾਪ

    def 실행결과(self):
        return subprocess.run([str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native')], timeout=5).returncode

    def 자바대조(self, ਸਰੋਤ, 추가=None):
        self.ਬਣਾਊਣਾ_ਸਰੋਤ(ਸਰੋਤ, 추가)
        (self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'ਹੋਸਟ.java').write_text(
            'public class ਹੋਸਟ { public static void main(String[] ਆਰਗੂਮੈਂਟ) { System.exit(시험.ਚਲਾਓ_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)] +
                       [str(ਮਾਰਗ) for ਮਾਰਗ in self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ), 'ਹੋਸਟ'], timeout=5).returncode
        ਅਸਲ_ਸਮੱਗਰੀ = self.실행결과()
        self.assertGreaterEqual(ਅਸਲ_ਸਮੱਗਰੀ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ਤਸਦੀਕ)')
        self.assertEqual(ਅਸਲ_ਸਮੱਗਰੀ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ਚਲਾਓ_2() {
                int 합 = 7;
                int ਕੀਮਤ = 12345;
                for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = -65; ਅਨੁਕ੍ਰਮਣਿਕਾ <= 65; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
                    ਕੀਮਤ = ਕੀਮਤ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ਕੀਮਤ, ਅਨੁਕ੍ਰਮਣਿਕਾ);
                    합 += (byte)ਕੀਮਤ + (short)ਕੀਮਤ + (char)ਕੀਮਤ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ਕੀਮਤ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ਚਲਾਓ_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < ਕੀਮਤ.length; 가++)
                    for (int 나 = 1; 나 < ਕੀਮਤ.length; 나++)
                        합 = 합 * 31 + ਕੀਮਤ[가] / ਕੀਮਤ[나] + ਕੀਮਤ[가] % ਕੀਮਤ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ਬਣਾਓ_ਦਾਖਲਾ(int ਆਕਾਰ) { return new int[ਆਕਾਰ]; }
            public static int ਚਲਾਓ_2() {
                int[] 가 = ਬਣਾਓ_ਦਾਖਲਾ(8); int[] 나 = 가; int[] ਖਾਲੀ_ਔਬਜੈਕਟ = new int[0];
                if (가 != 나 || 가 == null || ਖਾਲੀ_ਔਬਜੈਕਟ.length != 0 || 가[7] != 0) return 99;
                int ਕੀਮਤ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ਕੀਮਤ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ਕੀਮਤ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ਚਲਾਓ_2() { return 계산(1, 2, 3, 4, ਕੀਮਤ) + 보조.ਪੜ੍ਹਨ(); }
        }''', {'보조': '''public class 보조 {
            static int ਕੀਮਤ = 3;
            static int 초기값() { return ++ਕੀਮਤ; }
            static int ਪੜ੍ਹਨ() { return ਕੀਮਤ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ਕੀਮਤ = 보조.ਪੜ੍ਹਨ() + 1;
            public static int ਚਲਾਓ_2() { return ਕੀਮਤ * 10 + 보조.ਪੜ੍ਹਨ(); }
        }''', {'보조': '''public class 보조 {
            static int ਕੀਮਤ = 시험.ਕੀਮਤ + 2;
            static int ਪੜ੍ਹਨ() { return ਕੀਮਤ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ਟੈਕਸਟ = "한글\\u0000😀";
            public static int ਚਲਾਓ_2() {
                if (ਟੈਕਸਟ != "한글\\u0000😀") return 99;
                return (ਟੈਕਸਟ.length() + ਟੈਕਸਟ.charAt(2) + ਟੈਕਸਟ.charAt(3) + ਟੈਕਸਟ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ਗੁਣਨਖੰਡ(int ਕੀਮਤ) { return ਕੀਮਤ <= 1 ? 1 : ਕੀਮਤ * ਗੁਣਨਖੰਡ(ਕੀਮਤ - 1); }
            static int 연속(int ਕੀਮਤ) {
                switch (ਕੀਮਤ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ਕੀਮਤ) {
                switch (ਕੀਮਤ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ਚਲਾਓ_2() { return (ਗੁਣਨਖੰਡ(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int ਕੀਮਤ{} = {};'.format(ਅਨੁਕ੍ਰਮਣਿਕਾ, ਅਨੁਕ੍ਰਮਣਿਕਾ) for ਅਨੁਕ੍ਰਮਣਿਕਾ in range(270))
        덧셈 = '+'.join('ਕੀਮਤ{}'.format(ਅਨੁਕ੍ਰਮਣਿਕਾ) for ਅਨੁਕ੍ਰਮਣਿਕਾ in range(270))
        self.자바대조('public class 시험 { public static int ਚਲਾਓ_2() {' + 선언 +
                    'ਕੀਮਤ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ਕੀਮਤ = null; return ਕੀਮਤ.length;', 102),
            ('int[] ਕੀਮਤ = new int[1]; return ਕੀਮਤ[1];', 103),
            ('int[] ਕੀਮਤ = new int[1]; ਕੀਮਤ[-1] = 3; return 0;', 103),
            ('int ਕੀਮਤ = -1; return new int[ਕੀਮਤ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.ਬਣਾਊਣਾ_ਸਰੋਤ('public class 시험 { public static int ਚਲਾਓ_2() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ਕੀਮਤ; public static int ਚਲਾਓ_2() { return 0; }',
            'public static int ਚਲਾਓ_2() { Object ਕੀਮਤ = new Object(); return 0; }',
            'public static int ਚਲਾਓ_2() { System.out.println("hello"); return 0; }',
            'public static int ਚਲਾਓ_2() { try { return 1; } catch (Exception ਗਲਤੀ) { return 2; } }',
            'public static synchronized int ਚਲਾਓ_2() { return 0; }',
            'public static int ਚਲਾਓ_2() { return new byte[3].length; }',
            'static native int 외부(); public static int ਚਲਾਓ_2() { return 외부(); }',
            'int ਕੀਮਤ; public static int ਚਲਾਓ_2() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.ਬਣਾਊਣਾ_ਸਰੋਤ('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        ਆਉਟਪੁੱਟ = self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native'
        ਆਉਟਪੁੱਟ.write_bytes(b'original-output')
        self.ਬਣਾਊਣਾ_ਸਰੋਤ('public class 시험 { public static int ਚਲਾਓ_2() { return missing; } }', 성공=False)
        self.assertEqual(ਆਉਟਪੁੱਟ.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ਬਣਾਊਣਾ_ਸਰੋਤ('public class 시험 { public static int ਚਲਾਓ_2() { return 37; } }')
        self.assertEqual((self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ਲੱਭਣਾ_ਤਾਲਿਕਾ = subprocess.check_output(['readelf', '-l', str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native')])
        self.assertNotIn(b'INTERP', ਲੱਭਣਾ_ਤਾਲਿਕਾ)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ਬਣਾਊਣਾ_ਸਰੋਤ('public class 시험 { public static int ਚਲਾਓ_2() { return ਉਪਭੋਗਤਾ.실행권한(); } }',
                    {'ਉਪਭੋਗਤਾ': 'public class ਉਪਭੋਗਤਾ { public static native int 실행권한(); }'}, ਟੀਚਾ='user')
        ਸਮੱਗਰੀ = (self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native').read_bytes()
        self.assertEqual(ਸਮੱਗਰੀ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ਸਮੱਗਰੀ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native')]))
        # ਉਪਭੋਗਤਾ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ਬਣਾਊਣਾ_ਸਰੋਤ('public class 시험 { public static int ਚਲਾਓ_2() { return ਤਜਵੀਜ_ਕੀਮਤ.포트읽기(1); } }',
                    {'ਤਜਵੀਜ_ਕੀਮਤ': 'public class ਤਜਵੀਜ_ਕੀਮਤ { public static native int 포트읽기(int ਕੀਮਤ); }'}, 성공=False, ਟੀਚਾ='user')

    def test_내보내기검증(self):
        ਸਰੋਤ = 'public class 시험 { public static int ਚਲਾਓ_2() { return 0; } static int 호출(int ਕੀਮਤ) { return ਕੀਮਤ; } }'
        self.ਬਣਾਊਣਾ_ਸਰੋਤ(ਸਰੋਤ, ਟੀਚਾ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'native')]))
        self.ਬਣਾਊਣਾ_ਸਰੋਤ(ਸਰੋਤ, 성공=False, 내보냄='bad;name=시험.호출')
        self.ਬਣਾਊਣਾ_ਸਰੋਤ(ਸਰੋਤ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
