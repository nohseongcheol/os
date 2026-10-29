import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

និយមន័យ_តំលៃ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ម៉ូឌុល_តំលៃ_6d2d8bf4 = importlib.util.module_from_spec(និយមន័យ_តំលៃ)
និយមន័យ_តំលៃ.loader.exec_module(ម៉ូឌុល_តំលៃ_6d2d8bf4)


class 가짜상자:
    def __init__(self, ឬស_តំលៃ):
        self.ឬស_តំលៃ = ឬស_តំលៃ
        self.명령들 = []
        self.가상기계들 = {}
        self.បរាជ័យ_តំលៃ = None

    def __call__(self, អាគុយម៉ង់):
        អាគុយម៉ង់ = list(map(str, អាគុយម៉ង់))
        self.명령들.append(អាគុយម៉ង់)
        if self.បរាជ័យ_តំលៃ == អាគុយម៉ង់[1] or (អាគុយម៉ង់[0] == 'make' and self.បរាជ័យ_តំលៃ == 'make'):
            self.បរាជ័យ_តំលៃ = None
            raise ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류('시험용 បរាជ័យ_តំលៃ')
        if អាគុយម៉ង់[0] == 'make':
            ផ្លូវ = self.ឬស_តំលៃ / 'os/build/kernel.iso'
            ផ្លូវ.parent.mkdir(parents=True, exist_ok=True)
            ផ្លូវ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        អំពើ = អាគុយម៉ង់[1]
        if អំពើ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(តំលៃ['name'], សន្ទស្សន៏) for សន្ទស្សន៏, តំលៃ in self.가상기계들.items())
        if អំពើ == 'createvm':
            សន្ទស្សន៏, ឈ្មោះ = អាគុយម៉ង់[អាគុយម៉ង់.index('--uuid') + 1], អាគុយម៉ង់[អាគុយម៉ង់.index('--name') + 1]
            self.가상기계들[សន្ទស្សន៏] = {'UUID': សន្ទស្សន៏, 'name': ឈ្មោះ, 'VMState': 'poweroff',
                'CfgFile': str(self.ឬស_តំលៃ / '.vbox/machines' / ឈ្មោះ / (ឈ្មោះ + '.vbox')), 'owner': None}
            return ''
        ម៉ាស៊ីន = self.가상기계들[អាគុយម៉ង់[2]]
        if អំពើ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ឈ្មោះ), json.dumps(តំលៃ)) for ឈ្មោះ, តំលៃ in ម៉ាស៊ីន.items() if ឈ្មោះ != 'owner')
        if អំពើ == 'getextradata': return 'Value: ' + ម៉ាស៊ីន['owner'] if ម៉ាស៊ីន['owner'] else 'No value set!'
        if អំពើ == 'setextradata': ម៉ាស៊ីន['owner'] = អាគុយម៉ង់[4]
        elif អំពើ == 'storagectl': ម៉ាស៊ីន['storagecontrollername0'] = 'JKOROS IDE'
        elif អំពើ == 'storageattach': ម៉ាស៊ីន['JKOROS IDE-0-0'] = អាគុយម៉ង់[អាគុយម៉ង់.index('--medium') + 1]
        elif អំពើ == 'startvm': ម៉ាស៊ីន['VMState'] = 'running'
        elif អំពើ == 'controlvm':
            assert អាគុយម៉ង់[3] == 'resume'
            ម៉ាស៊ីន['VMState'] = 'running'
        elif អំពើ != 'modifyvm': raise AssertionError(អាគុយម៉ង់)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ឬស_តំលៃ = Path(self.임시.name)
        (self.ឬស_តំលៃ / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ឬស_តំលៃ)
        self.អនុវត្ត_ពាក្យបញ្ជា = ម៉ូឌុល_តំលៃ_6d2d8bf4.កម្មវិធី_ថត_កម្មវិធី(self.ឬស_តំលៃ, 'jkoros operating system', ពាក្យ_បញ្ជា=self.상자)

    def បង្កើត_ការបញ្ចូល(self):
        ការវាស់វែង = self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ការវាស់វែង['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ពាក្យ_បញ្ជា[0] == 'VBoxManage' and ពាក្យ_បញ្ជា[1] in ('list', 'showvminfo', 'getextradata') for ពាក្យ_បញ្ជា in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ការវាស់វែង = self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.assertEqual(ការវាស់វែង['state'], 'running')
        self.assertTrue(Path(ការវាស់វែង['iso']).is_file())
        self.assertTrue(any('--nic1' in ពាក្យ_បញ្ជា and 'none' in ពាក្យ_បញ្ជា for ពាក្យ_បញ្ជា in self.상자.명령들))
        self.assertFalse(any('hdd' in ពាក្យ_បញ្ជា or 'discardstate' in ពាក្យ_បញ្ជា or 'createmedium' in ពាក្យ_បញ្ជា for ពាក្យ_បញ្ជា in self.상자.명령들))

    def test_실행중유지(self):
        self.បង្កើត_ការបញ្ចូល()
        self.assertEqual(self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ម៉ាស៊ីន = self.បង្កើត_ការបញ្ចូល()
        ម៉ាស៊ីន['VMState'] = 'saved'
        កំណត់_ហេតុ_តំលៃ = self.អនុវត្ត_ពាក្យបញ្ជា.ផ្លូវ(self.អនុវត្ត_ពាក្យបញ្ជា.អាន()['serial_log'])
        កំណត់_ហេតុ_តំលៃ.write_text('saved log')
        self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.assertFalse(any(ពាក្យ_បញ្ជា[0] == 'make' or ពាក្យ_បញ្ជា[1] == 'modifyvm' for ពាក្យ_បញ្ជា in self.상자.명령들))
        self.assertEqual([ផ្លូវ.read_text() for ផ្លូវ in កំណត់_ហេតុ_តំលៃ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.បង្កើត_ការបញ្ចូល()['VMState'] = 'paused'
        self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.assertTrue(any(ពាក្យ_បញ្ជា[1] == 'controlvm' and ពាក្យ_បញ្ជា[3] == 'resume' for ពាក្យ_បញ្ជា in self.상자.명령들))
        self.assertFalse(any(ពាក្យ_បញ្ជា[0] == 'make' for ពាក្យ_បញ្ជា in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.변경없음()

    def test_소유표식거부(self):
        self.បង្កើត_ការបញ្ចូល()['owner'] = 'someone-else'
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.បង្កើត_ការបញ្ចូល()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ម៉ាស៊ីន = self.បង្កើត_ការបញ្ចូល()
        ម៉ាស៊ីន['VMState'] = 'poweroff'
        ម៉ាស៊ីន['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.변경없음()

    def test_전환중거부(self):
        self.បង្កើត_ការបញ្ចូល()['VMState'] = 'saving'
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.변경없음()

    def test_등록해제거부(self):
        self.បង្កើត_ការបញ្ចូល()
        self.상자.가상기계들.clear()
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ម៉ាស៊ីន = self.បង្កើត_ការបញ្ចូល()
        ម៉ាស៊ីន['VMState'] = 'poweroff'
        이전 = dict(ម៉ាស៊ីន)
        self.상자.បរាជ័យ_តំលៃ = 'make'
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.assertEqual(ម៉ាស៊ីន, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.បរាជ័យ_តំលៃ = 'setextradata'
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()
        self.상자.명령들.clear()
        self.assertEqual(self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()['state'], 'running')
        self.assertFalse(any(ពាក្យ_បញ្ជា[1] == 'createvm' for ពាក្យ_បញ្ជា in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ម៉ាស៊ីន = self.បង្កើត_ការបញ្ចូល()
        ម៉ាស៊ីន['VMState'] = 'poweroff'
        Path(ម៉ាស៊ីន['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា()

    def test_상태미생성(self):
        self.assertEqual(self.អនុវត្ត_ពាក្យបញ្ជា.បង្ហាញ_ភាព()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ផ្លូវ in ('../outside', '/tmp/outside'):
            with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.ផ្លូវ(ផ្លូវ)
        (self.ឬស_តំលៃ / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ម៉ូឌុល_តំលៃ_6d2d8bf4.실행오류): self.អនុវត្ត_ពាក្យបញ្ជា.ផ្លូវ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ការវាស់វែង = ម៉ូឌុល_តំលៃ_6d2d8bf4.លក្ខណះ_តំលៃ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ការវាស់វែង['VMState'], 'running')
        self.assertEqual(ការវាស់វែង['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
