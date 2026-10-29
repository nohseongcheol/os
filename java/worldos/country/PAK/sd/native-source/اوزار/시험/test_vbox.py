import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

وصف_قدر = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(وصف_قدر)
وصف_قدر.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ناڪامي_قدر = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ناڪامي_قدر == 인수[1] or (인수[0] == 'make' and self.ناڪامي_قدر == 'make'):
            self.ناڪامي_قدر = None
            raise 모듈.실행오류('시험용 ناڪامي_قدر')
        if 인수[0] == 'make':
            راههه = self.뿌리 / 'os/build/kernel.iso'
            راههه.parent.mkdir(parents=True, exist_ok=True)
            راههه.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        عمل = 인수[1]
        if عمل == 'list':
            return '\n'.join('"{}" {{{}}}'.format(قدر['name'], ابتدائي) for ابتدائي, قدر in self.가상기계들.items())
        if عمل == 'createvm':
            ابتدائي, نالو = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ابتدائي] = {'UUID': ابتدائي, 'name': نالو, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / نالو / (نالو + '.vbox')), 'owner': None}
            return ''
        مشين = self.가상기계들[인수[2]]
        if عمل == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(نالو), json.dumps(قدر)) for نالو, قدر in مشين.items() if نالو != 'owner')
        if عمل == 'getextradata': return 'Value: ' + مشين['owner'] if مشين['owner'] else 'No value set!'
        if عمل == 'setextradata': مشين['owner'] = 인수[4]
        elif عمل == 'storagectl': مشين['storagecontrollername0'] = 'JKOROS IDE'
        elif عمل == 'storageattach': مشين['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif عمل == 'startvm': مشين['VMState'] = 'running'
        elif عمل == 'controlvm':
            assert 인수[3] == 'resume'
            مشين['VMState'] = 'running'
        elif عمل != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.تعميل_ڪرڻ_حڪم = 모듈.ائپ_ائپ_ڊرائر(self.뿌리, 'jkoros operating system', حڪم=self.상자)

    def ٺاھيو_داخلا(self):
        결과 = self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(حڪم[0] == 'VBoxManage' and حڪم[1] in ('list', 'showvminfo', 'getextradata') for حڪم in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in حڪم and 'none' in حڪم for حڪم in self.상자.명령들))
        self.assertFalse(any('hdd' in حڪم or 'discardstate' in حڪم or 'createmedium' in حڪم for حڪم in self.상자.명령들))

    def test_실행중유지(self):
        self.ٺاھيو_داخلا()
        self.assertEqual(self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        مشين = self.ٺاھيو_داخلا()
        مشين['VMState'] = 'saved'
        لاگ_قدر = self.تعميل_ڪرڻ_حڪم.راههه(self.تعميل_ڪرڻ_حڪم.읽기()['serial_log'])
        لاگ_قدر.write_text('saved log')
        self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.assertFalse(any(حڪم[0] == 'make' or حڪم[1] == 'modifyvm' for حڪم in self.상자.명령들))
        self.assertEqual([راههه.read_text() for راههه in لاگ_قدر.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ٺاھيو_داخلا()['VMState'] = 'paused'
        self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.assertTrue(any(حڪم[1] == 'controlvm' and حڪم[3] == 'resume' for حڪم in self.상자.명령들))
        self.assertFalse(any(حڪم[0] == 'make' for حڪم in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.변경없음()

    def test_소유표식거부(self):
        self.ٺاھيو_داخلا()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ٺاھيو_داخلا()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        مشين = self.ٺاھيو_داخلا()
        مشين['VMState'] = 'poweroff'
        مشين['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.변경없음()

    def test_전환중거부(self):
        self.ٺاھيو_داخلا()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.변경없음()

    def test_등록해제거부(self):
        self.ٺاھيو_داخلا()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        مشين = self.ٺاھيو_داخلا()
        مشين['VMState'] = 'poweroff'
        이전 = dict(مشين)
        self.상자.ناڪامي_قدر = 'make'
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.assertEqual(مشين, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ناڪامي_قدر = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()
        self.상자.명령들.clear()
        self.assertEqual(self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()['state'], 'running')
        self.assertFalse(any(حڪم[1] == 'createvm' for حڪم in self.상자.명령들))

    def test_보존ISO변조거부(self):
        مشين = self.ٺاھيو_داخلا()
        مشين['VMState'] = 'poweroff'
        Path(مشين['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.تعميل_ڪرڻ_حڪم()

    def test_상태미생성(self):
        self.assertEqual(self.تعميل_ڪرڻ_حڪم.نمائش_ڪريو_حالت()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for راههه in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.راههه(راههه)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.تعميل_ڪرڻ_حڪم.راههه('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.منسوب_ڪرڻ_قدر('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
