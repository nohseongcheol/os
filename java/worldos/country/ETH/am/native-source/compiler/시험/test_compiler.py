"""ትክክለኛ_ውሂብ ELF ፈጽም_ትእዛዝ + OpenJDK ልኬት 대조. 임시 시험 자료만 생성한다."""
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
        self.ማውጫ_እሴት = Path(self.임시.name)

    def መገንባት_ምንጭ(self, ምንጭ, 추가=None, 성공=True, ዓላማ='linux', 내보냄=None):
        ዱካ_ዝርዝር = []
        for ስም, ይዘት_እሴት in dict({'시험': ምንጭ}, **(추가 or {})).items():
            መተላለፊያ = self.ማውጫ_እሴት / (ስም + '.java')
            መተላለፊያ.write_text(ይዘት_እሴት, encoding='utf-8')
            ዱካ_ዝርዝር.append(str(መተላለፊያ))
        ትእዛዝ = [sys.executable, str(컴파일러), '--target', ዓላማ, '--entry', '시험.ማስኬጃ', '-o', str(self.ማውጫ_እሴት / 'native')]
        if 내보냄 is not None: ትእዛዝ += ['--export', 내보냄]
        ልኬት = subprocess.run(ትእዛዝ + ዱካ_ዝርዝር,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ልኬት.returncode, 0, ልኬት.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ልኬት.returncode, 0)
            self.assertIn('መገንባት_ምንጭ ስህተት'.encode(), ልኬት.stderr)
        return ልኬት

    def 실행결과(self):
        return subprocess.run([str(self.ማውጫ_እሴት / 'native')], timeout=5).returncode

    def 자바대조(self, ምንጭ, 추가=None):
        self.መገንባት_ምንጭ(ምንጭ, 추가)
        (self.ማውጫ_እሴት / 'አዘጋጅ_b78e430d.java').write_text(
            'public class አዘጋጅ_b78e430d { public static void main(String[] 인수) { System.exit(시험.ማስኬጃ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ማውጫ_እሴት)] +
                       [str(መተላለፊያ) for መተላለፊያ in self.ማውጫ_እሴት.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ማውጫ_እሴት), 'አዘጋጅ_b78e430d'], timeout=5).returncode
        ትክክለኛ_ውሂብ = self.실행결과()
        self.assertGreaterEqual(ትክክለኛ_ውሂብ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 አረጋግጥ)')
        self.assertEqual(ትክክለኛ_ውሂብ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ማስኬጃ() {
                int 합 = 7;
                int እሴት = 12345;
                for (int መረጃ_ጠቆመ = -65; መረጃ_ጠቆመ <= 65; መረጃ_ጠቆመ++) {
                    እሴት = እሴት * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(እሴት, መረጃ_ጠቆመ);
                    합 += (byte)እሴት + (short)እሴት + (char)እሴት;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] እሴት = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ማስኬጃ() {
                int 합 = 13;
                for (int 가 = 0; 가 < እሴት.length; 가++)
                    for (int 나 = 1; 나 < እሴት.length; 나++)
                        합 = 합 * 31 + እሴት[가] / እሴት[나] + እሴት[가] % እሴት[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ፍጠር_ምዝግብ(int መጠን) { return new int[መጠን]; }
            public static int ማስኬጃ() {
                int[] 가 = ፍጠር_ምዝግብ(8); int[] 나 = 가; int[] ባዶ_ነገር = new int[0];
                if (가 != 나 || 가 == null || ባዶ_ነገር.length != 0 || 가[7] != 0) return 99;
                int እሴት = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return እሴት + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int እሴት = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ማስኬጃ() { return 계산(1, 2, 3, 4, እሴት) + 보조.ማንበቢያ(); }
        }''', {'보조': '''public class 보조 {
            static int እሴት = 3;
            static int 초기값() { return ++እሴት; }
            static int ማንበቢያ() { return እሴት; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int እሴት = 보조.ማንበቢያ() + 1;
            public static int ማስኬጃ() { return እሴት * 10 + 보조.ማንበቢያ(); }
        }''', {'보조': '''public class 보조 {
            static int እሴት = 시험.እሴት + 2;
            static int ማንበቢያ() { return እሴት; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ጽሁፍ = "한글\\u0000😀";
            public static int ማስኬጃ() {
                if (ጽሁፍ != "한글\\u0000😀") return 99;
                return (ጽሁፍ.length() + ጽሁፍ.charAt(2) + ጽሁፍ.charAt(3) + ጽሁፍ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ብዜት(int እሴት) { return እሴት <= 1 ? 1 : እሴት * ብዜት(እሴት - 1); }
            static int 연속(int እሴት) {
                switch (እሴት) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int እሴት) {
                switch (እሴት) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ማስኬጃ() { return (ብዜት(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        እወጃ = '\n'.join('int እሴት{} = {};'.format(መረጃ_ጠቆመ, መረጃ_ጠቆመ) for መረጃ_ጠቆመ in range(270))
        덧셈 = '+'.join('እሴት{}'.format(መረጃ_ጠቆመ) for መረጃ_ጠቆመ in range(270))
        self.자바대조('public class 시험 { public static int ማስኬጃ() {' + እወጃ +
                    'እሴት_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] እሴት = null; return እሴት.length;', 102),
            ('int[] እሴት = new int[1]; return እሴት[1];', 103),
            ('int[] እሴት = new int[1]; እሴት[-1] = 3; return 0;', 103),
            ('int እሴት = -1; return new int[እሴት].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for አካል_እሴት, 기대 in 경우들:
            with self.subTest(አካል_እሴት=አካል_እሴት):
                self.መገንባት_ምንጭ('public class 시험 { public static int ማስኬጃ() { ' + አካል_እሴት + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long እሴት; public static int ማስኬጃ() { return 0; }',
            'public static int ማስኬጃ() { Object እሴት = new Object(); return 0; }',
            'public static int ማስኬጃ() { System.out.println("hello"); return 0; }',
            'public static int ማስኬጃ() { try { return 1; } catch (Exception ስህተት) { return 2; } }',
            'public static synchronized int ማስኬጃ() { return 0; }',
            'public static int ማስኬጃ() { return new byte[3].length; }',
            'static native int 외부(); public static int ማስኬጃ() { return 외부(); }',
            'int እሴት; public static int ማስኬጃ() { return 0; }',
        ]
        for አካል_እሴት in 경우들:
            with self.subTest(አካል_እሴት=አካል_እሴት):
                self.መገንባት_ምንጭ('public class 시험 { ' + አካል_እሴት + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        ውጤት = self.ማውጫ_እሴት / 'native'
        ውጤት.write_bytes(b'original-output')
        self.መገንባት_ምንጭ('public class 시험 { public static int ማስኬጃ() { return missing; } }', 성공=False)
        self.assertEqual(ውጤት.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.መገንባት_ምንጭ('public class 시험 { public static int ማስኬጃ() { return 37; } }')
        self.assertEqual((self.ማውጫ_እሴት / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ፍለጋ_ሰንጠረዥ = subprocess.check_output(['readelf', '-l', str(self.ማውጫ_እሴት / 'native')])
        self.assertNotIn(b'INTERP', ፍለጋ_ሰንጠረዥ)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.መገንባት_ምንጭ('public class 시험 { public static int ማስኬጃ() { return ተጠቃሚ.실행권한(); } }',
                    {'ተጠቃሚ': 'public class ተጠቃሚ { public static native int 실행권한(); }'}, ዓላማ='user')
        ውሂብ = (self.ማውጫ_እሴት / 'native').read_bytes()
        self.assertEqual(ውሂብ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ውሂብ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ማውጫ_እሴት / 'native')]))
        # ተጠቃሚ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.መገንባት_ምንጭ('public class 시험 { public static int ማስኬጃ() { return መሳሪያ_እሴት.포트읽기(1); } }',
                    {'መሳሪያ_እሴት': 'public class መሳሪያ_እሴት { public static native int 포트읽기(int እሴት); }'}, 성공=False, ዓላማ='user')

    def test_내보내기검증(self):
        ምንጭ = 'public class 시험 { public static int ማስኬጃ() { return 0; } static int 호출(int እሴት) { return እሴት; } }'
        self.መገንባት_ምንጭ(ምንጭ, ዓላማ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ማውጫ_እሴት / 'native')]))
        self.መገንባት_ምንጭ(ምንጭ, 성공=False, 내보냄='bad;name=시험.호출')
        self.መገንባት_ምንጭ(ምንጭ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
