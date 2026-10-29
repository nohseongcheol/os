"""nyakuri_amakurushingiro ELF gukora_ibwiriza + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.ububiko_agaciro_e5561a2b = Path(self.임시.name)

    def gusohora_inkomoko(self, Inkomoko, 추가=None, 성공=True, gusimbuza_igishya='linux', 내보냄=None):
        inzira_Urutonde = []
        for Izina, Ibirimo_agaciro in dict({'시험': Inkomoko}, **(추가 or {})).items():
            Inzira = self.ububiko_agaciro_e5561a2b / (Izina + '.java')
            Inzira.write_text(Ibirimo_agaciro, encoding='utf-8')
            inzira_Urutonde.append(str(Inzira))
        Icyo_wifuza = [sys.executable, str(컴파일러), '--target', gusimbuza_igishya, '--entry', '시험.ihuriro', '-o', str(self.ububiko_agaciro_e5561a2b / 'native')]
        if 내보냄 is not None: Icyo_wifuza += ['--export', 내보냄]
        결과 = subprocess.run(Icyo_wifuza + inzira_Urutonde,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('gusohora_inkomoko IKOSA'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.ububiko_agaciro_e5561a2b / 'native')], timeout=5).returncode

    def 자바대조(self, Inkomoko, 추가=None):
        self.gusohora_inkomoko(Inkomoko, 추가)
        (self.ububiko_agaciro_e5561a2b / 'gucumbikira.java').write_text(
            'public class gucumbikira { public static void main(String[] 인수) { System.exit(시험.ihuriro()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ububiko_agaciro_e5561a2b)] +
                       [str(Inzira) for Inzira in self.ububiko_agaciro_e5561a2b.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ububiko_agaciro_e5561a2b), 'gucumbikira'], timeout=5).returncode
        nyakuri_amakurushingiro = self.실행결과()
        self.assertGreaterEqual(nyakuri_amakurushingiro, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 gusuzuma)')
        self.assertEqual(nyakuri_amakurushingiro, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ihuriro() {
                int 합 = 7;
                int agaciro = 12345;
                for (int umugerekashakiro = -65; umugerekashakiro <= 65; umugerekashakiro++) {
                    agaciro = agaciro * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(agaciro, umugerekashakiro);
                    합 += (byte)agaciro + (short)agaciro + (char)agaciro;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] agaciro = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ihuriro() {
                int 합 = 13;
                for (int 가 = 0; 가 < agaciro.length; 가++)
                    for (int 나 = 1; 나 < agaciro.length; 나++)
                        합 = 합 * 31 + agaciro[가] / agaciro[나] + agaciro[가] % agaciro[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] kurema_icyinjizwa(int Ingano) { return new int[Ingano]; }
            public static int ihuriro() {
                int[] 가 = kurema_icyinjizwa(8); int[] 나 = 가; int[] irimo_ubusa_ikintu = new int[0];
                if (가 != 나 || 가 == null || irimo_ubusa_ikintu.length != 0 || 가[7] != 0) return 99;
                int agaciro = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return agaciro + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int agaciro = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ihuriro() { return 계산(1, 2, 3, 4, agaciro) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int agaciro = 3;
            static int 초기값() { return ++agaciro; }
            static int 읽기() { return agaciro; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int agaciro = 보조.읽기() + 1;
            public static int ihuriro() { return agaciro * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int agaciro = 시험.agaciro + 2;
            static int 읽기() { return agaciro; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Umwandiko = "한글\\u0000😀";
            public static int ihuriro() {
                if (Umwandiko != "한글\\u0000😀") return 99;
                return (Umwandiko.length() + Umwandiko.charAt(2) + Umwandiko.charAt(3) + Umwandiko.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int fagitoriyeli(int agaciro) { return agaciro <= 1 ? 1 : agaciro * fagitoriyeli(agaciro - 1); }
            static int 연속(int agaciro) {
                switch (agaciro) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int agaciro) {
                switch (agaciro) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ihuriro() { return (fagitoriyeli(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int agaciro{} = {};'.format(umugerekashakiro, umugerekashakiro) for umugerekashakiro in range(270))
        덧셈 = '+'.join('agaciro{}'.format(umugerekashakiro) for umugerekashakiro in range(270))
        self.자바대조('public class 시험 { public static int ihuriro() {' + 선언 +
                    'agaciro_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] agaciro = null; return agaciro.length;', 102),
            ('int[] agaciro = new int[1]; return agaciro[1];', 103),
            ('int[] agaciro = new int[1]; agaciro[-1] = 3; return 0;', 103),
            ('int agaciro = -1; return new int[agaciro].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.gusohora_inkomoko('public class 시험 { public static int ihuriro() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long agaciro; public static int ihuriro() { return 0; }',
            'public static int ihuriro() { Object agaciro = new Object(); return 0; }',
            'public static int ihuriro() { System.out.println("hello"); return 0; }',
            'public static int ihuriro() { try { return 1; } catch (Exception IKOSA) { return 2; } }',
            'public static synchronized int ihuriro() { return 0; }',
            'public static int ihuriro() { return new byte[3].length; }',
            'static native int 외부(); public static int ihuriro() { return 외부(); }',
            'int agaciro; public static int ihuriro() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.gusohora_inkomoko('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ububiko_agaciro_e5561a2b / 'native'
        출력.write_bytes(b'original-output')
        self.gusohora_inkomoko('public class 시험 { public static int ihuriro() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.gusohora_inkomoko('public class 시험 { public static int ihuriro() { return 37; } }')
        self.assertEqual((self.ububiko_agaciro_e5561a2b / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.ububiko_agaciro_e5561a2b / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.gusohora_inkomoko('public class 시험 { public static int ihuriro() { return ukoresha.실행권한(); } }',
                    {'ukoresha': 'public class ukoresha { public static native int 실행권한(); }'}, gusimbuza_igishya='user')
        amakurushingiro = (self.ububiko_agaciro_e5561a2b / 'native').read_bytes()
        self.assertEqual(amakurushingiro[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', amakurushingiro, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ububiko_agaciro_e5561a2b / 'native')]))
        # ukoresha ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.gusohora_inkomoko('public class 시험 { public static int ihuriro() { return igendanwa_agaciro.포트읽기(1); } }',
                    {'igendanwa_agaciro': 'public class igendanwa_agaciro { public static native int 포트읽기(int agaciro); }'}, 성공=False, gusimbuza_igishya='user')

    def test_내보내기검증(self):
        Inkomoko = 'public class 시험 { public static int ihuriro() { return 0; } static int 호출(int agaciro) { return agaciro; } }'
        self.gusohora_inkomoko(Inkomoko, gusimbuza_igishya='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ububiko_agaciro_e5561a2b / 'native')]))
        self.gusohora_inkomoko(Inkomoko, 성공=False, 내보냄='bad;name=시험.호출')
        self.gusohora_inkomoko(Inkomoko, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
