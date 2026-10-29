import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

ຄໍານິຍາມ_ຄ່າ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ໂມດູນ_ຄ່າ = importlib.util.module_from_spec(ຄໍານິຍາມ_ຄ່າ)
ຄໍານິຍາມ_ຄ່າ.loader.exec_module(ໂມດູນ_ຄ່າ)


class 가짜상자:
    def __init__(self, ເລກຮາກ_ຄ່າ):
        self.ເລກຮາກ_ຄ່າ = ເລກຮາກ_ຄ່າ
        self.명령들 = []
        self.가상기계들 = {}
        self.ຫຼົ້ມເຫຼວ_ຄ່າ = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ຫຼົ້ມເຫຼວ_ຄ່າ == 인수[1] or (인수[0] == 'make' and self.ຫຼົ້ມເຫຼວ_ຄ່າ == 'make'):
            self.ຫຼົ້ມເຫຼວ_ຄ່າ = None
            raise ໂມດູນ_ຄ່າ.실행오류('시험용 ຫຼົ້ມເຫຼວ_ຄ່າ')
        if 인수[0] == 'make':
            ທາງໂຄຈອນ = self.ເລກຮາກ_ຄ່າ / 'os/build/kernel.iso'
            ທາງໂຄຈອນ.parent.mkdir(parents=True, exist_ok=True)
            ທາງໂຄຈອນ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ຄໍາສັ່ງ = 인수[1]
        if ຄໍາສັ່ງ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ຄ່າ['name'], ດັດຊະນີ) for ດັດຊະນີ, ຄ່າ in self.가상기계들.items())
        if ຄໍາສັ່ງ == 'createvm':
            ດັດຊະນີ, ຊື່ = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ດັດຊະນີ] = {'UUID': ດັດຊະນີ, 'name': ຊື່, 'VMState': 'poweroff',
                'CfgFile': str(self.ເລກຮາກ_ຄ່າ / '.vbox/machines' / ຊື່ / (ຊື່ + '.vbox')), 'owner': None}
            return ''
        ເຄື່ອງຈັກ = self.가상기계들[인수[2]]
        if ຄໍາສັ່ງ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ຊື່), json.dumps(ຄ່າ)) for ຊື່, ຄ່າ in ເຄື່ອງຈັກ.items() if ຊື່ != 'owner')
        if ຄໍາສັ່ງ == 'getextradata': return 'Value: ' + ເຄື່ອງຈັກ['owner'] if ເຄື່ອງຈັກ['owner'] else 'No value set!'
        if ຄໍາສັ່ງ == 'setextradata': ເຄື່ອງຈັກ['owner'] = 인수[4]
        elif ຄໍາສັ່ງ == 'storagectl': ເຄື່ອງຈັກ['storagecontrollername0'] = 'JKOROS IDE'
        elif ຄໍາສັ່ງ == 'storageattach': ເຄື່ອງຈັກ['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ຄໍາສັ່ງ == 'startvm': ເຄື່ອງຈັກ['VMState'] = 'running'
        elif ຄໍາສັ່ງ == 'controlvm':
            assert 인수[3] == 'resume'
            ເຄື່ອງຈັກ['VMState'] = 'running'
        elif ຄໍາສັ່ງ != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ເລກຮາກ_ຄ່າ = Path(self.임시.name)
        (self.ເລກຮາກ_ຄ່າ / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ເລກຮາກ_ຄ່າ)
        self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ = ໂມດູນ_ຄ່າ.ແອັບ_ຕົວເປີດໃຊ້(self.ເລກຮາກ_ຄ່າ, 'jkoros operating system', ຄໍາສັ່ງ_1f12b8e2=self.상자)

    def ສ້າງ_ເຂົ້າໃນ(self):
        ມາດຕະການ = self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ມາດຕະການ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ຄໍາສັ່ງ_1f12b8e2[0] == 'VBoxManage' and ຄໍາສັ່ງ_1f12b8e2[1] in ('list', 'showvminfo', 'getextradata') for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ມາດຕະການ = self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.assertEqual(ມາດຕະການ['state'], 'running')
        self.assertTrue(Path(ມາດຕະການ['iso']).is_file())
        self.assertTrue(any('--nic1' in ຄໍາສັ່ງ_1f12b8e2 and 'none' in ຄໍາສັ່ງ_1f12b8e2 for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))
        self.assertFalse(any('hdd' in ຄໍາສັ່ງ_1f12b8e2 or 'discardstate' in ຄໍາສັ່ງ_1f12b8e2 or 'createmedium' in ຄໍາສັ່ງ_1f12b8e2 for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))

    def test_실행중유지(self):
        self.ສ້າງ_ເຂົ້າໃນ()
        self.assertEqual(self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ເຄື່ອງຈັກ = self.ສ້າງ_ເຂົ້າໃນ()
        ເຄື່ອງຈັກ['VMState'] = 'saved'
        ບັນທຶກ_ຄ່າ = self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ທາງໂຄຈອນ(self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.읽기()['serial_log'])
        ບັນທຶກ_ຄ່າ.write_text('saved log')
        self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.assertFalse(any(ຄໍາສັ່ງ_1f12b8e2[0] == 'make' or ຄໍາສັ່ງ_1f12b8e2[1] == 'modifyvm' for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))
        self.assertEqual([ທາງໂຄຈອນ.read_text() for ທາງໂຄຈອນ in ບັນທຶກ_ຄ່າ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ສ້າງ_ເຂົ້າໃນ()['VMState'] = 'paused'
        self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.assertTrue(any(ຄໍາສັ່ງ_1f12b8e2[1] == 'controlvm' and ຄໍາສັ່ງ_1f12b8e2[3] == 'resume' for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))
        self.assertFalse(any(ຄໍາສັ່ງ_1f12b8e2[0] == 'make' for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ສ້າງ_ເຂົ້າໃນ()['owner'] = 'someone-else'
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ສ້າງ_ເຂົ້າໃນ()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ເຄື່ອງຈັກ = self.ສ້າງ_ເຂົ້າໃນ()
        ເຄື່ອງຈັກ['VMState'] = 'poweroff'
        ເຄື່ອງຈັກ['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.변경없음()

    def test_전환중거부(self):
        self.ສ້າງ_ເຂົ້າໃນ()['VMState'] = 'saving'
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ສ້າງ_ເຂົ້າໃນ()
        self.상자.가상기계들.clear()
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ເຄື່ອງຈັກ = self.ສ້າງ_ເຂົ້າໃນ()
        ເຄື່ອງຈັກ['VMState'] = 'poweroff'
        이전 = dict(ເຄື່ອງຈັກ)
        self.상자.ຫຼົ້ມເຫຼວ_ຄ່າ = 'make'
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.assertEqual(ເຄື່ອງຈັກ, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ຫຼົ້ມເຫຼວ_ຄ່າ = 'setextradata'
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
        self.상자.명령들.clear()
        self.assertEqual(self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()['state'], 'running')
        self.assertFalse(any(ຄໍາສັ່ງ_1f12b8e2[1] == 'createvm' for ຄໍາສັ່ງ_1f12b8e2 in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ເຄື່ອງຈັກ = self.ສ້າງ_ເຂົ້າໃນ()
        ເຄື່ອງຈັກ['VMState'] = 'poweroff'
        Path(ເຄື່ອງຈັກ['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()

    def test_상태미생성(self):
        self.assertEqual(self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ລາຍການ_ສະຖານະ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ທາງໂຄຈອນ in ('../outside', '/tmp/outside'):
            with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ທາງໂຄຈອນ(ທາງໂຄຈອນ)
        (self.ເລກຮາກ_ຄ່າ / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ໂມດູນ_ຄ່າ.실행오류): self.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ທາງໂຄຈອນ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ມາດຕະການ = ໂມດູນ_ຄ່າ.ຄຸນສົມບັດ_ຄ່າ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ມາດຕະການ['VMState'], 'running')
        self.assertEqual(ມາດຕະການ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
