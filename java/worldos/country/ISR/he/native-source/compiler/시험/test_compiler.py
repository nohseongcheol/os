"""בפועל_נתונים ELF לבצע_פקודה + OpenJDK תוצאה 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

מהדר = Path(__file__).resolve().parents[1] / 'מהדר.py'


class נסה_מקורי(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.מדריך_ערך = Path(self.임시.name)

    def בנה_מקור(self, קודמקור, צירוף_ערך_b73accca=None, 성공=True, יעד='linux', 내보냄=None):
        נתיב_רשימה = []
        for שם, תוכן_ערך in dict({'시험': קודמקור}, **(צירוף_ערך_b73accca or {})).items():
            נתיב = self.מדריך_ערך / (שם + '.java')
            נתיב.write_text(תוכן_ערך, encoding='utf-8')
            נתיב_רשימה.append(str(נתיב))
        פקודה = [sys.executable, str(מהדר), '--target', יעד, '--entry', '시험.הפעלה', '-o', str(self.מדריך_ערך / 'native')]
        if 내보냄 is not None: פקודה += ['--export', 내보냄]
        תוצאה = subprocess.run(פקודה + נתיב_רשימה,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(תוצאה.returncode, 0, תוצאה.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(תוצאה.returncode, 0)
            self.assertIn('בנה_מקור שגיאה'.encode(), תוצאה.stderr)
        return תוצאה

    def 실행결과(self):
        return subprocess.run([str(self.מדריך_ערך / 'native')], timeout=5).returncode

    def 자바대조(self, קודמקור, צירוף_ערך_b73accca=None):
        self.בנה_מקור(קודמקור, צירוף_ערך_b73accca)
        (self.מדריך_ערך / 'ארח.java').write_text(
            'public class ארח { public static void main(String[] ארגומנטים) { System.exit(시험.הפעלה()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.מדריך_ערך)] +
                       [str(נתיב) for נתיב in self.מדריך_ערך.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.מדריך_ערך), 'ארח'], timeout=5).returncode
        בפועל_נתונים = self.실행결과()
        self.assertGreaterEqual(בפועל_נתונים, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ודא_אמת)')
        self.assertEqual(בפועל_נתונים, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int הפעלה() {
                int 합 = 7;
                int ערך = 12345;
                for (int מדד = -65; מדד <= 65; מדד++) {
                    ערך = ערך * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ערך, מדד);
                    합 += (byte)ערך + (short)ערך + (char)ערך;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ערך = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int הפעלה() {
                int 합 = 13;
                for (int 가 = 0; 가 < ערך.length; 가++)
                    for (int 나 = 1; 나 < ערך.length; 나++)
                        합 = 합 * 31 + ערך[가] / ערך[나] + ערך[가] % ערך[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ליצור_ערך(int גודל) { return new int[גודל]; }
            public static int הפעלה() {
                int[] 가 = ליצור_ערך(8); int[] 나 = 가; int[] ריק_אובייקט = new int[0];
                if (가 != 나 || 가 == null || ריק_אובייקט.length != 0 || 가[7] != 0) return 99;
                int ערך = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ערך + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ערך = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int הפעלה() { return 계산(1, 2, 3, 4, ערך) + 보조.קרא(); }
        }''', {'보조': '''public class 보조 {
            static int ערך = 3;
            static int 초기값() { return ++ערך; }
            static int קרא() { return ערך; }
        }'''})

    def נסה_יורש_מחזור(self):
        self.자바대조('''public class 시험 {
            static int ערך = 보조.קרא() + 1;
            public static int הפעלה() { return ערך * 10 + 보조.קרא(); }
        }''', {'보조': '''public class 보조 {
            static int ערך = 시험.ערך + 2;
            static int קרא() { return ערך; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String טקסט = "한글\\u0000😀";
            public static int הפעלה() {
                if (טקסט != "한글\\u0000😀") return 99;
                return (טקסט.length() + טקסט.charAt(2) + טקסט.charAt(3) + טקסט.charAt(4)) % 251;
            }
        }''')

    def נסה_מתג_פעולת_גם_רקורסיה(self):
        self.자바대조('''public class 시험 {
            static int עצרת(int ערך) { return ערך <= 1 ? 1 : ערך * עצרת(ערך - 1); }
            static int 연속(int ערך) {
                switch (ערך) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ערך) {
                switch (ערך) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int הפעלה() { return (עצרת(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        הצהרה = '\n'.join('int ערך{} = {};'.format(מדד, מדד) for מדד in range(270))
        덧셈 = '+'.join('ערך{}'.format(מדד) for מדד in range(270))
        self.자바대조('public class 시험 { public static int הפעלה() {' + הצהרה +
                    'ערך_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int אפס_אופרנד = 0; return 1 / אפס_אופרנד;', 101),
            ('int[] ערך = null; return ערך.length;', 102),
            ('int[] ערך = new int[1]; return ערך[1];', 103),
            ('int[] ערך = new int[1]; ערך[-1] = 3; return 0;', 103),
            ('int ערך = -1; return new int[ערך].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for גוף_ההודעה_ערך, 기대 in 경우들:
            with self.subTest(גוף_ההודעה_ערך=גוף_ההודעה_ערך):
                self.בנה_מקור('public class 시험 { public static int הפעלה() { ' + גוף_ההודעה_ערך + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ערך; public static int הפעלה() { return 0; }',
            'public static int הפעלה() { Object ערך = new Object(); return 0; }',
            'public static int הפעלה() { System.out.println("hello"); return 0; }',
            'public static int הפעלה() { try { return 1; } catch (Exception שגיאה) { return 2; } }',
            'public static synchronized int הפעלה() { return 0; }',
            'public static int הפעלה() { return new byte[3].length; }',
            'static native int חיצוני_ערך(); public static int הפעלה() { return חיצוני_ערך(); }',
            'int ערך; public static int הפעלה() { return 0; }',
        ]
        for גוף_ההודעה_ערך in 경우들:
            with self.subTest(גוף_ההודעה_ערך=גוף_ההודעה_ערך):
                self.בנה_מקור('public class 시험 { ' + גוף_ההודעה_ערך + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        פלטטקסט = self.מדריך_ערך / 'native'
        פלטטקסט.write_bytes(b'original-output')
        self.בנה_מקור('public class 시험 { public static int הפעלה() { return missing; } }', 성공=False)
        self.assertEqual(פלטטקסט.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.בנה_מקור('public class 시험 { public static int הפעלה() { return 37; } }')
        self.assertEqual((self.מדריך_ערך / 'native').read_bytes()[:5], b'\x7fELF\x01')
        טבלת_בדיקת_מידע = subprocess.check_output(['readelf', '-l', str(self.מדריך_ערך / 'native')])
        self.assertNotIn(b'INTERP', טבלת_בדיקת_מידע)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.בנה_מקור('public class 시험 { public static int הפעלה() { return משתמש.실행권한(); } }',
                    {'משתמש': 'public class משתמש { public static native int 실행권한(); }'}, יעד='user')
        נתונים = (self.מדריך_ערך / 'native').read_bytes()
        self.assertEqual(נתונים[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', נתונים, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.מדריך_ערך / 'native')]))
        # משתמש ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.בנה_מקור('public class 시험 { public static int הפעלה() { return התקן_ערך_e13f0cd9.포트읽기(1); } }',
                    {'התקן_ערך_e13f0cd9': 'public class התקן_ערך_e13f0cd9 { public static native int 포트읽기(int ערך); }'}, 성공=False, יעד='user')

    def נסה_ייצא_אימות(self):
        קודמקור = 'public class 시험 { public static int הפעלה() { return 0; } static int 호출(int ערך) { return ערך; } }'
        self.בנה_מקור(קודמקור, יעד='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.מדריך_ערך / 'native')]))
        self.בנה_מקור(קודמקור, 성공=False, 내보냄='bad;name=시험.호출')
        self.בנה_מקור(קודמקור, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
