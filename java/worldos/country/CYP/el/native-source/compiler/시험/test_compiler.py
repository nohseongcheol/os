"""πραγματικός_δεδομένα ELF εκτελώ_εντολή + OpenJDK μέτρηση 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

πρόγραμμα_μεταγλώττισης = Path(__file__).resolve().parents[1] / 'πρόγραμμα_μεταγλώττισης.py'


class δοκιμή_εγγενής(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Κατάλογος_τιμή = Path(self.임시.name)

    def δόμηση_προέλευση(self, ΠΗΓΗ, προσαρτώ_καταχώρηση=None, 성공=True, τιμή_στόχος='linux', 내보냄=None):
        διαδρομή_Λίστα = []
        for Όνομα, Περιεχόμενο_τιμή in dict({'시험': ΠΗΓΗ}, **(προσαρτώ_καταχώρηση or {})).items():
            ΔΙΑΔΡΟΜΗ = self.Κατάλογος_τιμή / (Όνομα + '.java')
            ΔΙΑΔΡΟΜΗ.write_text(Περιεχόμενο_τιμή, encoding='utf-8')
            διαδρομή_Λίστα.append(str(ΔΙΑΔΡΟΜΗ))
        Εντολή = [sys.executable, str(πρόγραμμα_μεταγλώττισης), '--target', τιμή_στόχος, '--entry', '시험.Εκτέλεση_2', '-o', str(self.Κατάλογος_τιμή / 'native')]
        if 내보냄 is not None: Εντολή += ['--export', 내보냄]
        μέτρηση = subprocess.run(Εντολή + διαδρομή_Λίστα,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(μέτρηση.returncode, 0, μέτρηση.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(μέτρηση.returncode, 0)
            self.assertIn('δόμηση_προέλευση ΣΦΑΛΜΑ'.encode(), μέτρηση.stderr)
        return μέτρηση

    def εκτέλεση_μέτρηση(self):
        return subprocess.run([str(self.Κατάλογος_τιμή / 'native')], timeout=5).returncode

    def 자바대조(self, ΠΗΓΗ, προσαρτώ_καταχώρηση=None):
        self.δόμηση_προέλευση(ΠΗΓΗ, προσαρτώ_καταχώρηση)
        (self.Κατάλογος_τιμή / 'φιλοξενώ.java').write_text(
            'public class φιλοξενώ { public static void main(String[] Παράμετροι) { System.exit(시험.Εκτέλεση_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Κατάλογος_τιμή)] +
                       [str(ΔΙΑΔΡΟΜΗ) for ΔΙΑΔΡΟΜΗ in self.Κατάλογος_τιμή.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Κατάλογος_τιμή), 'φιλοξενώ'], timeout=5).returncode
        πραγματικός_δεδομένα = self.εκτέλεση_μέτρηση()
        self.assertGreaterEqual(πραγματικός_δεδομένα, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 επαληθεύω)')
        self.assertEqual(πραγματικός_δεδομένα, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Εκτέλεση_2() {
                int Διαχείριση_ενημερώσεων_λογισμικού_τιμή = 7;
                int τιμή = 12345;
                for (int Ευρετήριο = -65; Ευρετήριο <= 65; Ευρετήριο++) {
                    τιμή = τιμή * 1664525 + 1013904223;
                    Διαχείριση_ενημερώσεων_λογισμικού_τιμή = Διαχείριση_ενημερώσεων_λογισμικού_τιμή * 31 + 섞기(τιμή, Ευρετήριο);
                    Διαχείριση_ενημερώσεων_λογισμικού_τιμή += (byte)τιμή + (short)τιμή + (char)τιμή;
                }
                return (Διαχείριση_ενημερώσεων_λογισμικού_τιμή & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] τιμή = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Εκτέλεση_2() {
                int Διαχείριση_ενημερώσεων_λογισμικού_τιμή = 13;
                for (int 가 = 0; 가 < τιμή.length; 가++)
                    for (int 나 = 1; 나 < τιμή.length; 나++)
                        Διαχείριση_ενημερώσεων_λογισμικού_τιμή = Διαχείριση_ενημερώσεων_λογισμικού_τιμή * 31 + τιμή[가] / τιμή[나] + τιμή[가] % τιμή[나];
                return (Διαχείριση_ενημερώσεων_λογισμικού_τιμή & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ανοίγω_καταχώρηση(int Μέγεθος) { return new int[Μέγεθος]; }
            public static int Εκτέλεση_2() {
                int[] 가 = ανοίγω_καταχώρηση(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int τιμή = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return τιμή + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int τιμή = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Εκτέλεση_2() { return 계산(1, 2, 3, 4, τιμή) + 보조.Ανάγνωση(); }
        }''', {'보조': '''public class 보조 {
            static int τιμή = 3;
            static int 초기값() { return ++τιμή; }
            static int Ανάγνωση() { return τιμή; }
        }'''})

    def δοκιμή_προετοιμασία_Κύκλος(self):
        self.자바대조('''public class 시험 {
            static int τιμή = 보조.Ανάγνωση() + 1;
            public static int Εκτέλεση_2() { return τιμή * 10 + 보조.Ανάγνωση(); }
        }''', {'보조': '''public class 보조 {
            static int τιμή = 시험.τιμή + 2;
            static int Ανάγνωση() { return τιμή; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Κείμενο = "한글\\u0000😀";
            public static int Εκτέλεση_2() {
                if (Κείμενο != "한글\\u0000😀") return 99;
                return (Κείμενο.length() + Κείμενο.charAt(2) + Κείμενο.charAt(3) + Κείμενο.charAt(4)) % 251;
            }
        }''')

    def δοκιμή_αλλάζω_λογικό_ΚΑΙ_αναδρομή(self):
        self.자바대조('''public class 시험 {
            static int παραγοντικό(int τιμή) { return τιμή <= 1 ? 1 : τιμή * παραγοντικό(τιμή - 1); }
            static int 연속(int τιμή) {
                switch (τιμή) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int τιμή) {
                switch (τιμή) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Εκτέλεση_2() { return (παραγοντικό(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        δήλωση = '\n'.join('int τιμή{} = {};'.format(Ευρετήριο, Ευρετήριο) for Ευρετήριο in range(270))
        덧셈 = '+'.join('τιμή{}'.format(Ευρετήριο) for Ευρετήριο in range(270))
        self.자바대조('public class 시험 { public static int Εκτέλεση_2() {' + δήλωση +
                    'τιμή_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int μηδέν_τελεστέος = 0; return 1 / μηδέν_τελεστέος;', 101),
            ('int[] τιμή = null; return τιμή.length;', 102),
            ('int[] τιμή = new int[1]; return τιμή[1];', 103),
            ('int[] τιμή = new int[1]; τιμή[-1] = 3; return 0;', 103),
            ('int τιμή = -1; return new int[τιμή].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for σώμα_τιμή, 기대 in 경우들:
            with self.subTest(σώμα_τιμή=σώμα_τιμή):
                self.δόμηση_προέλευση('public class 시험 { public static int Εκτέλεση_2() { ' + σώμα_τιμή + ' } }')
                self.assertEqual(self.εκτέλεση_μέτρηση(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long τιμή; public static int Εκτέλεση_2() { return 0; }',
            'public static int Εκτέλεση_2() { Object τιμή = new Object(); return 0; }',
            'public static int Εκτέλεση_2() { System.out.println("hello"); return 0; }',
            'public static int Εκτέλεση_2() { try { return 1; } catch (Exception ΣΦΑΛΜΑ) { return 2; } }',
            'public static synchronized int Εκτέλεση_2() { return 0; }',
            'public static int Εκτέλεση_2() { return new byte[3].length; }',
            'static native int εξωτερικός_τιμή(); public static int Εκτέλεση_2() { return εξωτερικός_τιμή(); }',
            'int τιμή; public static int Εκτέλεση_2() { return 0; }',
        ]
        for σώμα_τιμή in 경우들:
            with self.subTest(σώμα_τιμή=σώμα_τιμή):
                self.δόμηση_προέλευση('public class 시험 { ' + σώμα_τιμή + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Έξοδος = self.Κατάλογος_τιμή / 'native'
        Έξοδος.write_bytes(b'original-output')
        self.δόμηση_προέλευση('public class 시험 { public static int Εκτέλεση_2() { return missing; } }', 성공=False)
        self.assertEqual(Έξοδος.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.δόμηση_προέλευση('public class 시험 { public static int Εκτέλεση_2() { return 37; } }')
        self.assertEqual((self.Κατάλογος_τιμή / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Αναζήτηση_πίνακας = subprocess.check_output(['readelf', '-l', str(self.Κατάλογος_τιμή / 'native')])
        self.assertNotIn(b'INTERP', Αναζήτηση_πίνακας)
        self.assertEqual(self.εκτέλεση_μέτρηση(), 37)

    def test_사용자ELF와ABI분리(self):
        self.δόμηση_προέλευση('public class 시험 { public static int Εκτέλεση_2() { return χρήστης.εκτέλεση_άδεια(); } }',
                    {'χρήστης': 'public class χρήστης { public static native int εκτέλεση_άδεια(); }'}, τιμή_στόχος='user')
        δεδομένα = (self.Κατάλογος_τιμή / 'native').read_bytes()
        self.assertEqual(δεδομένα[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', δεδομένα, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Κατάλογος_τιμή / 'native')]))
        # χρήστης ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.δόμηση_προέλευση('public class 시험 { public static int Εκτέλεση_2() { return συσκευή_τιμή.포트읽기(1); } }',
                    {'συσκευή_τιμή': 'public class συσκευή_τιμή { public static native int 포트읽기(int τιμή); }'}, 성공=False, τιμή_στόχος='user')

    def δοκιμή_εξάγω_επικύρωση(self):
        ΠΗΓΗ = 'public class 시험 { public static int Εκτέλεση_2() { return 0; } static int 호출(int τιμή) { return τιμή; } }'
        self.δόμηση_προέλευση(ΠΗΓΗ, τιμή_στόχος='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Κατάλογος_τιμή / 'native')]))
        self.δόμηση_προέλευση(ΠΗΓΗ, 성공=False, 내보냄='bad;name=시험.호출')
        self.δόμηση_προέλευση(ΠΗΓΗ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
