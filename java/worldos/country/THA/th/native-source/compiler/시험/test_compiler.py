"""ค่าจริง_ข้อมูล ELF ดําเนินการ_คําสั่ง + OpenJDK ผลลัพธ์ 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

คอมไพเลอร์ = Path(__file__).resolve().parents[1] / 'คอมไพเลอร์.py'


class การทดสอบ_ดั้งเดิม(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.ไดเรกทอรี_ค่า = Path(self.임시.name)

    def คอมไพล์_แหล่ง(self, รหัสต้นฉบับ, ผนวก_รายการ=None, 성공=True, เป้าหมาย='linux', 내보냄=None):
        พาธ_รายการ = []
        for ชื่อ, เนื้อหา_ค่า in dict({'시험': รหัสต้นฉบับ}, **(ผนวก_รายการ or {})).items():
            เส้นทาง = self.ไดเรกทอรี_ค่า / (ชื่อ + '.java')
            เส้นทาง.write_text(เนื้อหา_ค่า, encoding='utf-8')
            พาธ_รายการ.append(str(เส้นทาง))
        คําสั่ง = [sys.executable, str(คอมไพเลอร์), '--target', เป้าหมาย, '--entry', '시험.เรียกใช้งาน', '-o', str(self.ไดเรกทอรี_ค่า / 'native')]
        if 내보냄 is not None: คําสั่ง += ['--export', 내보냄]
        ผลลัพธ์ = subprocess.run(คําสั่ง + พาธ_รายการ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ผลลัพธ์.returncode, 0, ผลลัพธ์.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ผลลัพธ์.returncode, 0)
            self.assertIn('คอมไพล์_แหล่ง ข้อผิดพลาด'.encode(), ผลลัพธ์.stderr)
        return ผลลัพธ์

    def 실행결과(self):
        return subprocess.run([str(self.ไดเรกทอรี_ค่า / 'native')], timeout=5).returncode

    def 자바대조(self, รหัสต้นฉบับ, ผนวก_รายการ=None):
        self.คอมไพล์_แหล่ง(รหัสต้นฉบับ, ผนวก_รายการ)
        (self.ไดเรกทอรี_ค่า / 'โฮสต์.java').write_text(
            'public class โฮสต์ { public static void main(String[] อาร์กิวเมนต์) { System.exit(시험.เรียกใช้งาน()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ไดเรกทอรี_ค่า)] +
                       [str(เส้นทาง) for เส้นทาง in self.ไดเรกทอรี_ค่า.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ไดเรกทอรี_ค่า), 'โฮสต์'], timeout=5).returncode
        ค่าจริง_ข้อมูล = self.실행결과()
        self.assertGreaterEqual(ค่าจริง_ข้อมูล, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ยืนยัน)')
        self.assertEqual(ค่าจริง_ข้อมูล, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int เรียกใช้งาน() {
                int 합 = 7;
                int ค่า = 12345;
                for (int ดัชนี = -65; ดัชนี <= 65; ดัชนี++) {
                    ค่า = ค่า * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ค่า, ดัชนี);
                    합 += (byte)ค่า + (short)ค่า + (char)ค่า;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ค่า = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int เรียกใช้งาน() {
                int 합 = 13;
                for (int 가 = 0; 가 < ค่า.length; 가++)
                    for (int 나 = 1; 나 < ค่า.length; 나++)
                        합 = 합 * 31 + ค่า[가] / ค่า[나] + ค่า[가] % ค่า[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] เปิด_รายการ(int ขนาด) { return new int[ขนาด]; }
            public static int เรียกใช้งาน() {
                int[] 가 = เปิด_รายการ(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int ค่า = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ค่า + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ค่า = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int เรียกใช้งาน() { return 계산(1, 2, 3, 4, ค่า) + 보조.อ่าน(); }
        }''', {'보조': '''public class 보조 {
            static int ค่า = 3;
            static int 초기값() { return ++ค่า; }
            static int อ่าน() { return ค่า; }
        }'''})

    def การทดสอบ_การเตรียมใช้งาน_วงกลม(self):
        self.자바대조('''public class 시험 {
            static int ค่า = 보조.อ่าน() + 1;
            public static int เรียกใช้งาน() { return ค่า * 10 + 보조.อ่าน(); }
        }''', {'보조': '''public class 보조 {
            static int ค่า = 시험.ค่า + 2;
            static int อ่าน() { return ค่า; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ข้อความ = "한글\\u0000😀";
            public static int เรียกใช้งาน() {
                if (ข้อความ != "한글\\u0000😀") return 99;
                return (ข้อความ.length() + ข้อความ.charAt(2) + ข้อความ.charAt(3) + ข้อความ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int แฟกทอเรียล(int ค่า) { return ค่า <= 1 ? 1 : ค่า * แฟกทอเรียล(ค่า - 1); }
            static int 연속(int ค่า) {
                switch (ค่า) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ค่า) {
                switch (ค่า) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int เรียกใช้งาน() { return (แฟกทอเรียล(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        การประกาศ = '\n'.join('int ค่า{} = {};'.format(ดัชนี, ดัชนี) for ดัชนี in range(270))
        덧셈 = '+'.join('ค่า{}'.format(ดัชนี) for ดัชนี in range(270))
        self.자바대조('public class 시험 { public static int เรียกใช้งาน() {' + การประกาศ +
                    'ค่า_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int ศูนย์_ตัวถูกดําเนินการ = 0; return 1 / ศูนย์_ตัวถูกดําเนินการ;', 101),
            ('int[] ค่า = null; return ค่า.length;', 102),
            ('int[] ค่า = new int[1]; return ค่า[1];', 103),
            ('int[] ค่า = new int[1]; ค่า[-1] = 3; return 0;', 103),
            ('int ค่า = -1; return new int[ค่า].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for เนื้อความ_ค่า, 기대 in 경우들:
            with self.subTest(เนื้อความ_ค่า=เนื้อความ_ค่า):
                self.คอมไพล์_แหล่ง('public class 시험 { public static int เรียกใช้งาน() { ' + เนื้อความ_ค่า + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ค่า; public static int เรียกใช้งาน() { return 0; }',
            'public static int เรียกใช้งาน() { Object ค่า = new Object(); return 0; }',
            'public static int เรียกใช้งาน() { System.out.println("hello"); return 0; }',
            'public static int เรียกใช้งาน() { try { return 1; } catch (Exception ข้อผิดพลาด) { return 2; } }',
            'public static synchronized int เรียกใช้งาน() { return 0; }',
            'public static int เรียกใช้งาน() { return new byte[3].length; }',
            'static native int ภายนอก_ค่า(); public static int เรียกใช้งาน() { return ภายนอก_ค่า(); }',
            'int ค่า; public static int เรียกใช้งาน() { return 0; }',
        ]
        for เนื้อความ_ค่า in 경우들:
            with self.subTest(เนื้อความ_ค่า=เนื้อความ_ค่า):
                self.คอมไพล์_แหล่ง('public class 시험 { ' + เนื้อความ_ค่า + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        ข้อความออก = self.ไดเรกทอรี_ค่า / 'native'
        ข้อความออก.write_bytes(b'original-output')
        self.คอมไพล์_แหล่ง('public class 시험 { public static int เรียกใช้งาน() { return missing; } }', 성공=False)
        self.assertEqual(ข้อความออก.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.คอมไพล์_แหล่ง('public class 시험 { public static int เรียกใช้งาน() { return 37; } }')
        self.assertEqual((self.ไดเรกทอรี_ค่า / 'native').read_bytes()[:5], b'\x7fELF\x01')
        การค้นหา_ตาราง = subprocess.check_output(['readelf', '-l', str(self.ไดเรกทอรี_ค่า / 'native')])
        self.assertNotIn(b'INTERP', การค้นหา_ตาราง)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.คอมไพล์_แหล่ง('public class 시험 { public static int เรียกใช้งาน() { return ผู้ใช้.실행권한(); } }',
                    {'ผู้ใช้': 'public class ผู้ใช้ { public static native int 실행권한(); }'}, เป้าหมาย='user')
        ข้อมูล = (self.ไดเรกทอรี_ค่า / 'native').read_bytes()
        self.assertEqual(ข้อมูล[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ข้อมูล, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ไดเรกทอรี_ค่า / 'native')]))
        # ผู้ใช้ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.คอมไพล์_แหล่ง('public class 시험 { public static int เรียกใช้งาน() { return อุปกรณ์_ค่า.포트읽기(1); } }',
                    {'อุปกรณ์_ค่า': 'public class อุปกรณ์_ค่า { public static native int 포트읽기(int ค่า); }'}, 성공=False, เป้าหมาย='user')

    def การทดสอบ_ส่งออก_การตรวจสอบความถูกต้อง(self):
        รหัสต้นฉบับ = 'public class 시험 { public static int เรียกใช้งาน() { return 0; } static int 호출(int ค่า) { return ค่า; } }'
        self.คอมไพล์_แหล่ง(รหัสต้นฉบับ, เป้าหมาย='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ไดเรกทอรี_ค่า / 'native')]))
        self.คอมไพล์_แหล่ง(รหัสต้นฉบับ, 성공=False, 내보냄='bad;name=시험.호출')
        self.คอมไพล์_แหล่ง(รหัสต้นฉบับ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
