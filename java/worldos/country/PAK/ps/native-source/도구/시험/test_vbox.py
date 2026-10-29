import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

정의 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(정의)
정의.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.پاتېينه_ارزښت = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.پاتېينه_ارزښت == 인수[1] or (인수[0] == 'make' and self.پاتېينه_ارزښت == 'make'):
            self.پاتېينه_ارزښت = None
            raise 모듈.실행오류('시험용 پاتېينه_ارزښت')
        if 인수[0] == 'make':
            يونلور = self.뿌리 / 'os/build/kernel.iso'
            يونلور.parent.mkdir(parents=True, exist_ok=True)
            يونلور.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        چار = 인수[1]
        if چار == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ارزښت['name'], لړیال) for لړیال, ارزښت in self.가상기계들.items())
        if چار == 'createvm':
            لړیال, نوم = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[لړیال] = {'UUID': لړیال, 'name': نوم, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / نوم / (نوم + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[인수[2]]
        if چار == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(نوم), json.dumps(ارزښت)) for نوم, ارزښت in 기계.items() if نوم != 'owner')
        if چار == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if چار == 'setextradata': 기계['owner'] = 인수[4]
        elif چار == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif چار == 'storageattach': 기계['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif چار == 'startvm': 기계['VMState'] = 'running'
        elif چار == 'controlvm':
            assert 인수[3] == 'resume'
            기계['VMState'] = 'running'
        elif چار != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.실행 = 모듈.실행기(self.뿌리, 'jkoros operating system', بولۍ=self.상자)

    def 만들기(self):
        결과 = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(بولۍ[0] == 'VBoxManage' and بولۍ[1] in ('list', 'showvminfo', 'getextradata') for بولۍ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.실행.실행()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in بولۍ and 'none' in بولۍ for بولۍ in self.상자.명령들))
        self.assertFalse(any('hdd' in بولۍ or 'discardstate' in بولۍ or 'createmedium' in بولۍ for بولۍ in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        خبرال_ارزښت = self.실행.يونلور(self.실행.لوستل()['serial_log'])
        خبرال_ارزښت.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(بولۍ[0] == 'make' or بولۍ[1] == 'modifyvm' for بولۍ in self.상자.명령들))
        self.assertEqual([يونلور.read_text() for يونلور in خبرال_ارزښت.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(بولۍ[1] == 'controlvm' and بولۍ[3] == 'resume' for بولۍ in self.상자.명령들))
        self.assertFalse(any(بولۍ[0] == 'make' for بولۍ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_소유표식거부(self):
        self.만들기()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.만들기()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        기계['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_전환중거부(self):
        self.만들기()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_등록해제거부(self):
        self.만들기()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        이전 = dict(기계)
        self.상자.پاتېينه_ارزښت = 'make'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.assertEqual(기계, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.پاتېينه_ارزښت = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.상자.명령들.clear()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.assertFalse(any(بولۍ[1] == 'createvm' for بولۍ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.상태보기()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for يونلور in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.실행.يونلور(يونلور)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.실행.يونلور('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.ځانتیا_ارزښت('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
