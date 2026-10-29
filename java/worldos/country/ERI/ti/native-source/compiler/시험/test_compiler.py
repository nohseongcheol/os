"""ትኽክለኛ_ሓበሬታ ELF ተግብር_ትእዛዝ + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.ሓባሪ_ማህደር_ዋጋ = Path(self.임시.name)

    def ህነጽ_ምንጪ(self, ምንጪ, 추가=None, 성공=True, ዕላማ='linux', 내보냄=None):
        መገዲ_ዝርዝር = []
        for ሽም, ትሕዝቶ_ዋጋ in dict({'시험': ምንጪ}, **(추가 or {})).items():
            መገዲ = self.ሓባሪ_ማህደር_ዋጋ / (ሽም + '.java')
            መገዲ.write_text(ትሕዝቶ_ዋጋ, encoding='utf-8')
            መገዲ_ዝርዝር.append(str(መገዲ))
        ትእዛዝ = [sys.executable, str(컴파일러), '--target', ዕላማ, '--entry', '시험.ኣኺድ', '-o', str(self.ሓባሪ_ማህደር_ዋጋ / 'native')]
        if 내보냄 is not None: ትእዛዝ += ['--export', 내보냄]
        결과 = subprocess.run(ትእዛዝ + መገዲ_ዝርዝር,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('ህነጽ_ምንጪ ጌጋ'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.ሓባሪ_ማህደር_ዋጋ / 'native')], timeout=5).returncode

    def 자바대조(self, ምንጪ, 추가=None):
        self.ህነጽ_ምንጪ(ምንጪ, 추가)
        (self.ሓባሪ_ማህደር_ዋጋ / 'አዐንግድ.java').write_text(
            'public class አዐንግድ { public static void main(String[] 인수) { System.exit(시험.ኣኺድ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ሓባሪ_ማህደር_ዋጋ)] +
                       [str(መገዲ) for መገዲ in self.ሓባሪ_ማህደር_ዋጋ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ሓባሪ_ማህደር_ዋጋ), 'አዐንግድ'], timeout=5).returncode
        ትኽክለኛ_ሓበሬታ = self.실행결과()
        self.assertGreaterEqual(ትኽክለኛ_ሓበሬታ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ኣረጋግጽ)')
        self.assertEqual(ትኽክለኛ_ሓበሬታ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ኣኺድ() {
                int 합 = 7;
                int ዋጋ = 12345;
                for (int መሐበሪ = -65; መሐበሪ <= 65; መሐበሪ++) {
                    ዋጋ = ዋጋ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ዋጋ, መሐበሪ);
                    합 += (byte)ዋጋ + (short)ዋጋ + (char)ዋጋ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ዋጋ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ኣኺድ() {
                int 합 = 13;
                for (int 가 = 0; 가 < ዋጋ.length; 가++)
                    for (int 나 = 1; 나 < ዋጋ.length; 나++)
                        합 = 합 * 31 + ዋጋ[가] / ዋጋ[나] + ዋጋ[가] % ዋጋ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ፍጠር_ምእታው(int መጠን) { return new int[መጠን]; }
            public static int ኣኺድ() {
                int[] 가 = ፍጠር_ምእታው(8); int[] 나 = 가; int[] ባዶ_ነገር = new int[0];
                if (가 != 나 || 가 == null || ባዶ_ነገር.length != 0 || 가[7] != 0) return 99;
                int ዋጋ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ዋጋ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ዋጋ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ኣኺድ() { return 계산(1, 2, 3, 4, ዋጋ) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ዋጋ = 3;
            static int 초기값() { return ++ዋጋ; }
            static int 읽기() { return ዋጋ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ዋጋ = 보조.읽기() + 1;
            public static int ኣኺድ() { return ዋጋ * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ዋጋ = 시험.ዋጋ + 2;
            static int 읽기() { return ዋጋ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ጽሑፍ = "한글\\u0000😀";
            public static int ኣኺድ() {
                if (ጽሑፍ != "한글\\u0000😀") return 99;
                return (ጽሑፍ.length() + ጽሑፍ.charAt(2) + ጽሑፍ.charAt(3) + ጽሑፍ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int ዋጋ) { return ዋጋ <= 1 ? 1 : ዋጋ * 계승(ዋጋ - 1); }
            static int 연속(int ዋጋ) {
                switch (ዋጋ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ዋጋ) {
                switch (ዋጋ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ኣኺድ() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int ዋጋ{} = {};'.format(መሐበሪ, መሐበሪ) for መሐበሪ in range(270))
        덧셈 = '+'.join('ዋጋ{}'.format(መሐበሪ) for መሐበሪ in range(270))
        self.자바대조('public class 시험 { public static int ኣኺድ() {' + 선언 +
                    'ዋጋ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ዋጋ = null; return ዋጋ.length;', 102),
            ('int[] ዋጋ = new int[1]; return ዋጋ[1];', 103),
            ('int[] ዋጋ = new int[1]; ዋጋ[-1] = 3; return 0;', 103),
            ('int ዋጋ = -1; return new int[ዋጋ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.ህነጽ_ምንጪ('public class 시험 { public static int ኣኺድ() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ዋጋ; public static int ኣኺድ() { return 0; }',
            'public static int ኣኺድ() { Object ዋጋ = new Object(); return 0; }',
            'public static int ኣኺድ() { System.out.println("hello"); return 0; }',
            'public static int ኣኺድ() { try { return 1; } catch (Exception ጌጋ) { return 2; } }',
            'public static synchronized int ኣኺድ() { return 0; }',
            'public static int ኣኺድ() { return new byte[3].length; }',
            'static native int 외부(); public static int ኣኺድ() { return 외부(); }',
            'int ዋጋ; public static int ኣኺድ() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.ህነጽ_ምንጪ('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ሓባሪ_ማህደር_ዋጋ / 'native'
        출력.write_bytes(b'original-output')
        self.ህነጽ_ምንጪ('public class 시험 { public static int ኣኺድ() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ህነጽ_ምንጪ('public class 시험 { public static int ኣኺድ() { return 37; } }')
        self.assertEqual((self.ሓባሪ_ማህደር_ዋጋ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.ሓባሪ_ማህደር_ዋጋ / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ህነጽ_ምንጪ('public class 시험 { public static int ኣኺድ() { return ተጠቃሚ.실행권한(); } }',
                    {'ተጠቃሚ': 'public class ተጠቃሚ { public static native int 실행권한(); }'}, ዕላማ='user')
        ሓበሬታ = (self.ሓባሪ_ማህደር_ዋጋ / 'native').read_bytes()
        self.assertEqual(ሓበሬታ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ሓበሬታ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ሓባሪ_ማህደር_ዋጋ / 'native')]))
        # ተጠቃሚ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ህነጽ_ምንጪ('public class 시험 { public static int ኣኺድ() { return መሳርሒ_ዋጋ.포트읽기(1); } }',
                    {'መሳርሒ_ዋጋ': 'public class መሳርሒ_ዋጋ { public static native int 포트읽기(int ዋጋ); }'}, 성공=False, ዕላማ='user')

    def test_내보내기검증(self):
        ምንጪ = 'public class 시험 { public static int ኣኺድ() { return 0; } static int 호출(int ዋጋ) { return ዋጋ; } }'
        self.ህነጽ_ምንጪ(ምንጪ, ዕላማ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ሓባሪ_ማህደር_ዋጋ / 'native')]))
        self.ህነጽ_ምንጪ(ምንጪ, 성공=False, 내보냄='bad;name=시험.호출')
        self.ህነጽ_ምንጪ(ምንጪ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
