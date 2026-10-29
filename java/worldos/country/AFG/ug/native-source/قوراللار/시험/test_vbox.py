import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

ئېنىقلىما_قىممىتى = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
بۆلەك_قىممىتى_6d2d8bf4 = importlib.util.module_from_spec(ئېنىقلىما_قىممىتى)
ئېنىقلىما_قىممىتى.loader.exec_module(بۆلەك_قىممىتى_6d2d8bf4)


class 가짜상자:
    def __init__(self, يىلتىز_قىممىتى):
        self.يىلتىز_قىممىتى = يىلتىز_قىممىتى
        self.명령들 = []
        self.가상기계들 = {}
        self.مەغلۇپ_بولۇش_قىممىتى = None

    def __call__(self, ئۆزگەرگۈچىلەر):
        ئۆزگەرگۈچىلەر = list(map(str, ئۆزگەرگۈچىلەر))
        self.명령들.append(ئۆزگەرگۈچىلەر)
        if self.مەغلۇپ_بولۇش_قىممىتى == ئۆزگەرگۈچىلەر[1] or (ئۆزگەرگۈچىلەر[0] == 'make' and self.مەغلۇپ_بولۇش_قىممىتى == 'make'):
            self.مەغلۇپ_بولۇش_قىممىتى = None
            raise بۆلەك_قىممىتى_6d2d8bf4.실행오류('시험용 مەغلۇپ_بولۇش_قىممىتى')
        if ئۆزگەرگۈچىلەر[0] == 'make':
            يول = self.يىلتىز_قىممىتى / 'os/build/kernel.iso'
            يول.parent.mkdir(parents=True, exist_ok=True)
            يول.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        مەشغۇلات = ئۆزگەرگۈچىلەر[1]
        if مەشغۇلات == 'list':
            return '\n'.join('"{}" {{{}}}'.format(قىممىتى['name'], ئىندېكس) for ئىندېكس, قىممىتى in self.가상기계들.items())
        if مەشغۇلات == 'createvm':
            ئىندېكس, ئاتى = ئۆزگەرگۈچىلەر[ئۆزگەرگۈچىلەر.index('--uuid') + 1], ئۆزگەرگۈچىلەر[ئۆزگەرگۈچىلەر.index('--name') + 1]
            self.가상기계들[ئىندېكس] = {'UUID': ئىندېكس, 'name': ئاتى, 'VMState': 'poweroff',
                'CfgFile': str(self.يىلتىز_قىممىتى / '.vbox/machines' / ئاتى / (ئاتى + '.vbox')), 'owner': None}
            return ''
        ماشىنا = self.가상기계들[ئۆزگەرگۈچىلەر[2]]
        if مەشغۇلات == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ئاتى), json.dumps(قىممىتى)) for ئاتى, قىممىتى in ماشىنا.items() if ئاتى != 'owner')
        if مەشغۇلات == 'getextradata': return 'Value: ' + ماشىنا['owner'] if ماشىنا['owner'] else 'No value set!'
        if مەشغۇلات == 'setextradata': ماشىنا['owner'] = ئۆزگەرگۈچىلەر[4]
        elif مەشغۇلات == 'storagectl': ماشىنا['storagecontrollername0'] = 'JKOROS IDE'
        elif مەشغۇلات == 'storageattach': ماشىنا['JKOROS IDE-0-0'] = ئۆزگەرگۈچىلەر[ئۆزگەرگۈچىلەر.index('--medium') + 1]
        elif مەشغۇلات == 'startvm': ماشىنا['VMState'] = 'running'
        elif مەشغۇلات == 'controlvm':
            assert ئۆزگەرگۈچىلەر[3] == 'resume'
            ماشىنا['VMState'] = 'running'
        elif مەشغۇلات != 'modifyvm': raise AssertionError(ئۆزگەرگۈچىلەر)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.يىلتىز_قىممىتى = Path(self.임시.name)
        (self.يىلتىز_قىممىتى / '.vbox').mkdir()
        self.상자 = 가짜상자(self.يىلتىز_قىممىتى)
        self.ئىجرا_قىلىش_بۇيرۇق = بۆلەك_قىممىتى_6d2d8bf4.ئەپ_خادىم(self.يىلتىز_قىممىتى, 'jkoros operating system', بۇيرۇق=self.상자)

    def قۇرۇش_كىرگۈزۈش(self):
        ئۆلچەم = self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ئۆلچەم['uuid']]

    def 변경없음(self):
        self.assertTrue(all(بۇيرۇق[0] == 'VBoxManage' and بۇيرۇق[1] in ('list', 'showvminfo', 'getextradata') for بۇيرۇق in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ئۆلچەم = self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.assertEqual(ئۆلچەم['state'], 'running')
        self.assertTrue(Path(ئۆلچەم['iso']).is_file())
        self.assertTrue(any('--nic1' in بۇيرۇق and 'none' in بۇيرۇق for بۇيرۇق in self.상자.명령들))
        self.assertFalse(any('hdd' in بۇيرۇق or 'discardstate' in بۇيرۇق or 'createmedium' in بۇيرۇق for بۇيرۇق in self.상자.명령들))

    def test_실행중유지(self):
        self.قۇرۇش_كىرگۈزۈش()
        self.assertEqual(self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ماشىنا = self.قۇرۇش_كىرگۈزۈش()
        ماشىنا['VMState'] = 'saved'
        خاتىرە_قىممىتى = self.ئىجرا_قىلىش_بۇيرۇق.يول(self.ئىجرا_قىلىش_بۇيرۇق.ئوقۇ()['serial_log'])
        خاتىرە_قىممىتى.write_text('saved log')
        self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.assertFalse(any(بۇيرۇق[0] == 'make' or بۇيرۇق[1] == 'modifyvm' for بۇيرۇق in self.상자.명령들))
        self.assertEqual([يول.read_text() for يول in خاتىرە_قىممىتى.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.قۇرۇش_كىرگۈزۈش()['VMState'] = 'paused'
        self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.assertTrue(any(بۇيرۇق[1] == 'controlvm' and بۇيرۇق[3] == 'resume' for بۇيرۇق in self.상자.명령들))
        self.assertFalse(any(بۇيرۇق[0] == 'make' for بۇيرۇق in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.변경없음()

    def test_소유표식거부(self):
        self.قۇرۇش_كىرگۈزۈش()['owner'] = 'someone-else'
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.قۇرۇش_كىرگۈزۈش()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ماشىنا = self.قۇرۇش_كىرگۈزۈش()
        ماشىنا['VMState'] = 'poweroff'
        ماشىنا['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.변경없음()

    def test_전환중거부(self):
        self.قۇرۇش_كىرگۈزۈش()['VMState'] = 'saving'
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.변경없음()

    def test_등록해제거부(self):
        self.قۇرۇش_كىرگۈزۈش()
        self.상자.가상기계들.clear()
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ماشىنا = self.قۇرۇش_كىرگۈزۈش()
        ماشىنا['VMState'] = 'poweroff'
        이전 = dict(ماشىنا)
        self.상자.مەغلۇپ_بولۇش_قىممىتى = 'make'
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.assertEqual(ماشىنا, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.مەغلۇپ_بولۇش_قىممىتى = 'setextradata'
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()
        self.상자.명령들.clear()
        self.assertEqual(self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()['state'], 'running')
        self.assertFalse(any(بۇيرۇق[1] == 'createvm' for بۇيرۇق in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ماشىنا = self.قۇرۇش_كىرگۈزۈش()
        ماشىنا['VMState'] = 'poweroff'
        Path(ماشىنا['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق()

    def test_상태미생성(self):
        self.assertEqual(self.ئىجرا_قىلىش_بۇيرۇق.كۆرسەتمەك_ھالەت()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for يول in ('../outside', '/tmp/outside'):
            with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.يول(يول)
        (self.يىلتىز_قىممىتى / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(بۆلەك_قىممىتى_6d2d8bf4.실행오류): self.ئىجرا_قىلىش_بۇيرۇق.يول('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ئۆلچەم = بۆلەك_قىممىتى_6d2d8bf4.خاسلىق_قىممىتى('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ئۆلچەم['VMState'], 'running')
        self.assertEqual(ئۆلچەم['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
