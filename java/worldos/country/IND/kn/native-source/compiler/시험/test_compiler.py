"""ನಿಜವಾದ_ಡೇಟಾ ELF ಪೂರೈಸು_ಆದೇಶ + OpenJDK ಮಾಪನ 대조. 임시 시험 자료만 생성한다."""
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
        self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ = Path(self.임시.name)

    def ಸಂಕಲಿಸು_ಮೂಲ(self, ಮೂಲ, 추가=None, 성공=True, ಲಕ್ಷ್ಯ='linux', 내보냄=None):
        ಹಾದಿ_ಪಟ್ಟಿ = []
        for ಹೆಸರು, ವಿಷಯ_ಮೌಲ್ಯ in dict({'시험': ಮೂಲ}, **(추가 or {})).items():
            ಮಾರ್ಗ = self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.java')
            ಮಾರ್ಗ.write_text(ವಿಷಯ_ಮೌಲ್ಯ, encoding='utf-8')
            ಹಾದಿ_ಪಟ್ಟಿ.append(str(ಮಾರ್ಗ))
        ಆಜ್ಞೆ = [sys.executable, str(컴파일러), '--target', ಲಕ್ಷ್ಯ, '--entry', '시험.ಚಲಾಯಿಸು_2', '-o', str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native')]
        if 내보냄 is not None: ಆಜ್ಞೆ += ['--export', 내보냄]
        ಮಾಪನ = subprocess.run(ಆಜ್ಞೆ + ಹಾದಿ_ಪಟ್ಟಿ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ಮಾಪನ.returncode, 0, ಮಾಪನ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ಮಾಪನ.returncode, 0)
            self.assertIn('ಸಂಕಲಿಸು_ಮೂಲ ದೋಷ'.encode(), ಮಾಪನ.stderr)
        return ಮಾಪನ

    def 실행결과(self):
        return subprocess.run([str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native')], timeout=5).returncode

    def 자바대조(self, ಮೂಲ, 추가=None):
        self.ಸಂಕಲಿಸು_ಮೂಲ(ಮೂಲ, 추가)
        (self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'ಹೋಸ್ಟ್.java').write_text(
            'public class ಹೋಸ್ಟ್ { public static void main(String[] 인수) { System.exit(시험.ಚಲಾಯಿಸು_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)] +
                       [str(ಮಾರ್ಗ) for ಮಾರ್ಗ in self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ), 'ಹೋಸ್ಟ್'], timeout=5).returncode
        ನಿಜವಾದ_ಡೇಟಾ = self.실행결과()
        self.assertGreaterEqual(ನಿಜವಾದ_ಡೇಟಾ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು)')
        self.assertEqual(ನಿಜವಾದ_ಡೇಟಾ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ಚಲಾಯಿಸು_2() {
                int 합 = 7;
                int ಮೌಲ್ಯ = 12345;
                for (int ಪದಸೂಚಿ = -65; ಪದಸೂಚಿ <= 65; ಪದಸೂಚಿ++) {
                    ಮೌಲ್ಯ = ಮೌಲ್ಯ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ಮೌಲ್ಯ, ಪದಸೂಚಿ);
                    합 += (byte)ಮೌಲ್ಯ + (short)ಮೌಲ್ಯ + (char)ಮೌಲ್ಯ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ಮೌಲ್ಯ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ಚಲಾಯಿಸು_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < ಮೌಲ್ಯ.length; 가++)
                    for (int 나 = 1; 나 < ಮೌಲ್ಯ.length; 나++)
                        합 = 합 * 31 + ಮೌಲ್ಯ[가] / ಮೌಲ್ಯ[나] + ಮೌಲ್ಯ[가] % ಮೌಲ್ಯ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ರಚಿಸು_ನಮೂದು(int ಗಾತ್ರ) { return new int[ಗಾತ್ರ]; }
            public static int ಚಲಾಯಿಸು_2() {
                int[] 가 = ರಚಿಸು_ನಮೂದು(8); int[] 나 = 가; int[] ಖಾಲಿ_ಆಬ್ಜೆಕ್ಟ್ = new int[0];
                if (가 != 나 || 가 == null || ಖಾಲಿ_ಆಬ್ಜೆಕ್ಟ್.length != 0 || 가[7] != 0) return 99;
                int ಮೌಲ್ಯ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ಮೌಲ್ಯ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ಮೌಲ್ಯ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ಚಲಾಯಿಸು_2() { return 계산(1, 2, 3, 4, ಮೌಲ್ಯ) + 보조.ಓದು(); }
        }''', {'보조': '''public class 보조 {
            static int ಮೌಲ್ಯ = 3;
            static int 초기값() { return ++ಮೌಲ್ಯ; }
            static int ಓದು() { return ಮೌಲ್ಯ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ಮೌಲ್ಯ = 보조.ಓದು() + 1;
            public static int ಚಲಾಯಿಸು_2() { return ಮೌಲ್ಯ * 10 + 보조.ಓದು(); }
        }''', {'보조': '''public class 보조 {
            static int ಮೌಲ್ಯ = 시험.ಮೌಲ್ಯ + 2;
            static int ಓದು() { return ಮೌಲ್ಯ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ಪಠ್ಯ = "한글\\u0000😀";
            public static int ಚಲಾಯಿಸು_2() {
                if (ಪಠ್ಯ != "한글\\u0000😀") return 99;
                return (ಪಠ್ಯ.length() + ಪಠ್ಯ.charAt(2) + ಪಠ್ಯ.charAt(3) + ಪಠ್ಯ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ಗುಣಲಬ್ಧ(int ಮೌಲ್ಯ) { return ಮೌಲ್ಯ <= 1 ? 1 : ಮೌಲ್ಯ * ಗುಣಲಬ್ಧ(ಮೌಲ್ಯ - 1); }
            static int 연속(int ಮೌಲ್ಯ) {
                switch (ಮೌಲ್ಯ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ಮೌಲ್ಯ) {
                switch (ಮೌಲ್ಯ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ಚಲಾಯಿಸು_2() { return (ಗುಣಲಬ್ಧ(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        ದೃಢೀಕರಣ = '\n'.join('int ಮೌಲ್ಯ{} = {};'.format(ಪದಸೂಚಿ, ಪದಸೂಚಿ) for ಪದಸೂಚಿ in range(270))
        덧셈 = '+'.join('ಮೌಲ್ಯ{}'.format(ಪದಸೂಚಿ) for ಪದಸೂಚಿ in range(270))
        self.자바대조('public class 시험 { public static int ಚಲಾಯಿಸು_2() {' + ದೃಢೀಕರಣ +
                    'ಮೌಲ್ಯ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ಮೌಲ್ಯ = null; return ಮೌಲ್ಯ.length;', 102),
            ('int[] ಮೌಲ್ಯ = new int[1]; return ಮೌಲ್ಯ[1];', 103),
            ('int[] ಮೌಲ್ಯ = new int[1]; ಮೌಲ್ಯ[-1] = 3; return 0;', 103),
            ('int ಮೌಲ್ಯ = -1; return new int[ಮೌಲ್ಯ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ, 기대 in 경우들:
            with self.subTest(ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ=ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ):
                self.ಸಂಕಲಿಸು_ಮೂಲ('public class 시험 { public static int ಚಲಾಯಿಸು_2() { ' + ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ಮೌಲ್ಯ; public static int ಚಲಾಯಿಸು_2() { return 0; }',
            'public static int ಚಲಾಯಿಸು_2() { Object ಮೌಲ್ಯ = new Object(); return 0; }',
            'public static int ಚಲಾಯಿಸು_2() { System.out.println("hello"); return 0; }',
            'public static int ಚಲಾಯಿಸು_2() { try { return 1; } catch (Exception ದೋಷ) { return 2; } }',
            'public static synchronized int ಚಲಾಯಿಸು_2() { return 0; }',
            'public static int ಚಲಾಯಿಸು_2() { return new byte[3].length; }',
            'static native int 외부(); public static int ಚಲಾಯಿಸು_2() { return 외부(); }',
            'int ಮೌಲ್ಯ; public static int ಚಲಾಯಿಸು_2() { return 0; }',
        ]
        for ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ in 경우들:
            with self.subTest(ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ=ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ):
                self.ಸಂಕಲಿಸು_ಮೂಲ('public class 시험 { ' + ಮುಖ್ಯ_ಸಂದೇಶ_ಮೌಲ್ಯ + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        ಔಟ್_ಪುಟ್ = self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native'
        ಔಟ್_ಪುಟ್.write_bytes(b'original-output')
        self.ಸಂಕಲಿಸು_ಮೂಲ('public class 시험 { public static int ಚಲಾಯಿಸು_2() { return missing; } }', 성공=False)
        self.assertEqual(ಔಟ್_ಪುಟ್.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ಸಂಕಲಿಸು_ಮೂಲ('public class 시험 { public static int ಚಲಾಯಿಸು_2() { return 37; } }')
        self.assertEqual((self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ನೋಡುವ_ಕೋಷ್ಟಕ = subprocess.check_output(['readelf', '-l', str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native')])
        self.assertNotIn(b'INTERP', ನೋಡುವ_ಕೋಷ್ಟಕ)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ಸಂಕಲಿಸು_ಮೂಲ('public class 시험 { public static int ಚಲಾಯಿಸು_2() { return ಬಳಕೆದಾರ.실행권한(); } }',
                    {'ಬಳಕೆದಾರ': 'public class ಬಳಕೆದಾರ { public static native int 실행권한(); }'}, ಲಕ್ಷ್ಯ='user')
        ಡೇಟಾ = (self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native').read_bytes()
        self.assertEqual(ಡೇಟಾ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ಡೇಟಾ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native')]))
        # ಬಳಕೆದಾರ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ಸಂಕಲಿಸು_ಮೂಲ('public class 시험 { public static int ಚಲಾಯಿಸು_2() { return ಸಾಧನ_ಮೌಲ್ಯ.포트읽기(1); } }',
                    {'ಸಾಧನ_ಮೌಲ್ಯ': 'public class ಸಾಧನ_ಮೌಲ್ಯ { public static native int 포트읽기(int ಮೌಲ್ಯ); }'}, 성공=False, ಲಕ್ಷ್ಯ='user')

    def test_내보내기검증(self):
        ಮೂಲ = 'public class 시험 { public static int ಚಲಾಯಿಸು_2() { return 0; } static int 호출(int ಮೌಲ್ಯ) { return ಮೌಲ್ಯ; } }'
        self.ಸಂಕಲಿಸು_ಮೂಲ(ಮೂಲ, ಲಕ್ಷ್ಯ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'native')]))
        self.ಸಂಕಲಿಸು_ಮೂಲ(ಮೂಲ, 성공=False, 내보냄='bad;name=시험.호출')
        self.ಸಂಕಲಿಸು_ಮೂಲ(ಮೂಲ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
