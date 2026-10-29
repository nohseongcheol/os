import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

คําจํากัดความ_ค่า = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
มอดูล_ค่า = importlib.util.module_from_spec(คําจํากัดความ_ค่า)
คําจํากัดความ_ค่า.loader.exec_module(มอดูล_ค่า)


class 가짜상자:
    def __init__(self, ราก_ค่า):
        self.ราก_ค่า = ราก_ค่า
        self.명령들 = []
        self.가상기계들 = {}
        self.ความล้มเหลว_ค่า = None

    def __call__(self, อาร์กิวเมนต์):
        อาร์กิวเมนต์ = list(map(str, อาร์กิวเมนต์))
        self.명령들.append(อาร์กิวเมนต์)
        if self.ความล้มเหลว_ค่า == อาร์กิวเมนต์[1] or (อาร์กิวเมนต์[0] == 'make' and self.ความล้มเหลว_ค่า == 'make'):
            self.ความล้มเหลว_ค่า = None
            raise มอดูล_ค่า.실행오류('시험용 ความล้มเหลว_ค่า')
        if อาร์กิวเมนต์[0] == 'make':
            เส้นทาง = self.ราก_ค่า / 'os/build/kernel.iso'
            เส้นทาง.parent.mkdir(parents=True, exist_ok=True)
            เส้นทาง.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        การกระทํา = อาร์กิวเมนต์[1]
        if การกระทํา == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ค่า['name'], ดัชนี) for ดัชนี, ค่า in self.가상기계들.items())
        if การกระทํา == 'createvm':
            ดัชนี, ชื่อ = อาร์กิวเมนต์[อาร์กิวเมนต์.index('--uuid') + 1], อาร์กิวเมนต์[อาร์กิวเมนต์.index('--name') + 1]
            self.가상기계들[ดัชนี] = {'UUID': ดัชนี, 'name': ชื่อ, 'VMState': 'poweroff',
                'CfgFile': str(self.ราก_ค่า / '.vbox/machines' / ชื่อ / (ชื่อ + '.vbox')), 'owner': None}
            return ''
        เครื่อง = self.가상기계들[อาร์กิวเมนต์[2]]
        if การกระทํา == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ชื่อ), json.dumps(ค่า)) for ชื่อ, ค่า in เครื่อง.items() if ชื่อ != 'owner')
        if การกระทํา == 'getextradata': return 'Value: ' + เครื่อง['owner'] if เครื่อง['owner'] else 'No value set!'
        if การกระทํา == 'setextradata': เครื่อง['owner'] = อาร์กิวเมนต์[4]
        elif การกระทํา == 'storagectl': เครื่อง['storagecontrollername0'] = 'JKOROS IDE'
        elif การกระทํา == 'storageattach': เครื่อง['JKOROS IDE-0-0'] = อาร์กิวเมนต์[อาร์กิวเมนต์.index('--medium') + 1]
        elif การกระทํา == 'startvm': เครื่อง['VMState'] = 'running'
        elif การกระทํา == 'controlvm':
            assert อาร์กิวเมนต์[3] == 'resume'
            เครื่อง['VMState'] = 'running'
        elif การกระทํา != 'modifyvm': raise AssertionError(อาร์กิวเมนต์)
        return ''


class การทดสอบการใช้งาน(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ราก_ค่า = Path(self.임시.name)
        (self.ราก_ค่า / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ราก_ค่า)
        self.ดําเนินการ_คําสั่ง = มอดูล_ค่า.แอป_ลิ้นชักแอป(self.ราก_ค่า, 'jkoros operating system', คําสั่ง=self.상자)

    def เปิด_รายการ(self):
        ผลลัพธ์ = self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ผลลัพธ์['uuid']]

    def 변경없음(self):
        self.assertTrue(all(คําสั่ง[0] == 'VBoxManage' and คําสั่ง[1] in ('list', 'showvminfo', 'getextradata') for คําสั่ง in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ผลลัพธ์ = self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.assertEqual(ผลลัพธ์['state'], 'running')
        self.assertTrue(Path(ผลลัพธ์['iso']).is_file())
        self.assertTrue(any('--nic1' in คําสั่ง and 'none' in คําสั่ง for คําสั่ง in self.상자.명령들))
        self.assertFalse(any('hdd' in คําสั่ง or 'discardstate' in คําสั่ง or 'createmedium' in คําสั่ง for คําสั่ง in self.상자.명령들))

    def test_실행중유지(self):
        self.เปิด_รายการ()
        self.assertEqual(self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        เครื่อง = self.เปิด_รายการ()
        เครื่อง['VMState'] = 'saved'
        บันทึก_ค่า = self.ดําเนินการ_คําสั่ง.เส้นทาง(self.ดําเนินการ_คําสั่ง.อ่าน()['serial_log'])
        บันทึก_ค่า.write_text('saved log')
        self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.assertFalse(any(คําสั่ง[0] == 'make' or คําสั่ง[1] == 'modifyvm' for คําสั่ง in self.상자.명령들))
        self.assertEqual([เส้นทาง.read_text() for เส้นทาง in บันทึก_ค่า.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.เปิด_รายการ()['VMState'] = 'paused'
        self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.assertTrue(any(คําสั่ง[1] == 'controlvm' and คําสั่ง[3] == 'resume' for คําสั่ง in self.상자.명령들))
        self.assertFalse(any(คําสั่ง[0] == 'make' for คําสั่ง in self.상자.명령들))

    def การทดสอบ_อัทเธอร์_เครื่องเสมือน_ชื่อ_ความขัดแย้ง(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.변경없음()

    def test_소유표식거부(self):
        self.เปิด_รายการ()['owner'] = 'someone-else'
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.เปิด_รายการ()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        เครื่อง = self.เปิด_รายการ()
        เครื่อง['VMState'] = 'poweroff'
        เครื่อง['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.변경없음()

    def test_전환중거부(self):
        self.เปิด_รายการ()['VMState'] = 'saving'
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.변경없음()

    def test_등록해제거부(self):
        self.เปิด_รายการ()
        self.상자.가상기계들.clear()
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        เครื่อง = self.เปิด_รายการ()
        เครื่อง['VMState'] = 'poweroff'
        이전 = dict(เครื่อง)
        self.상자.ความล้มเหลว_ค่า = 'make'
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.assertEqual(เครื่อง, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ความล้มเหลว_ค่า = 'setextradata'
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()
        self.상자.명령들.clear()
        self.assertEqual(self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()['state'], 'running')
        self.assertFalse(any(คําสั่ง[1] == 'createvm' for คําสั่ง in self.상자.명령들))

    def test_보존ISO변조거부(self):
        เครื่อง = self.เปิด_รายการ()
        เครื่อง['VMState'] = 'poweroff'
        Path(เครื่อง['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง()

    def test_상태미생성(self):
        self.assertEqual(self.ดําเนินการ_คําสั่ง.แสดง_สถานะ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for เส้นทาง in ('../outside', '/tmp/outside'):
            with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.เส้นทาง(เส้นทาง)
        (self.ราก_ค่า / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(มอดูล_ค่า.실행오류): self.ดําเนินการ_คําสั่ง.เส้นทาง('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ผลลัพธ์ = มอดูล_ค่า.แอตทริบิวต์_ค่า('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ผลลัพธ์['VMState'], 'running')
        self.assertEqual(ผลลัพธ์['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
