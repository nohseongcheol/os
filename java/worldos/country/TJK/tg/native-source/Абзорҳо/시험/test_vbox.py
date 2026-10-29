import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Тавсиф_қимат = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(Тавсиф_қимат)
Тавсиф_қимат.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.нокомӣ_қимат = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.нокомӣ_қимат == 인수[1] or (인수[0] == 'make' and self.нокомӣ_қимат == 'make'):
            self.нокомӣ_қимат = None
            raise 모듈.실행오류('시험용 нокомӣ_қимат')
        if 인수[0] == 'make':
            масир = self.뿌리 / 'os/build/kernel.iso'
            масир.parent.mkdir(parents=True, exist_ok=True)
            масир.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Амал = 인수[1]
        if Амал == 'list':
            return '\n'.join('"{}" {{{}}}'.format(қимат['name'], индекс) for индекс, қимат in self.가상기계들.items())
        if Амал == 'createvm':
            индекс, Ном = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[индекс] = {'UUID': индекс, 'name': Ном, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Ном / (Ном + '.vbox')), 'owner': None}
            return ''
        компютер = self.가상기계들[인수[2]]
        if Амал == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ном), json.dumps(қимат)) for Ном, қимат in компютер.items() if Ном != 'owner')
        if Амал == 'getextradata': return 'Value: ' + компютер['owner'] if компютер['owner'] else 'No value set!'
        if Амал == 'setextradata': компютер['owner'] = 인수[4]
        elif Амал == 'storagectl': компютер['storagecontrollername0'] = 'JKOROS IDE'
        elif Амал == 'storageattach': компютер['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Амал == 'startvm': компютер['VMState'] = 'running'
        elif Амал == 'controlvm':
            assert 인수[3] == 'resume'
            компютер['VMState'] = 'running'
        elif Амал != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.иҷро_кардан_фармон = 모듈.барнома_панели_барномаҳо(self.뿌리, 'jkoros operating system', фармон=self.상자)

    def эҷод_кардан_ворида(self):
        결과 = self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(фармон[0] == 'VBoxManage' and фармон[1] in ('list', 'showvminfo', 'getextradata') for фармон in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in фармон and 'none' in фармон for фармон in self.상자.명령들))
        self.assertFalse(any('hdd' in фармон or 'discardstate' in фармон or 'createmedium' in фармон for фармон in self.상자.명령들))

    def test_실행중유지(self):
        self.эҷод_кардан_ворида()
        self.assertEqual(self.иҷро_кардан_фармон.иҷро_кардан_фармон()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        компютер = self.эҷод_кардан_ворида()
        компютер['VMState'] = 'saved'
        сабт_кардан_қимат = self.иҷро_кардан_фармон.масир(self.иҷро_кардан_фармон.Хондан()['serial_log'])
        сабт_кардан_қимат.write_text('saved log')
        self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.assertFalse(any(фармон[0] == 'make' or фармон[1] == 'modifyvm' for фармон in self.상자.명령들))
        self.assertEqual([масир.read_text() for масир in сабт_кардан_қимат.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.эҷод_кардан_ворида()['VMState'] = 'paused'
        self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.assertTrue(any(фармон[1] == 'controlvm' and фармон[3] == 'resume' for фармон in self.상자.명령들))
        self.assertFalse(any(фармон[0] == 'make' for фармон in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.변경없음()

    def test_소유표식거부(self):
        self.эҷод_кардан_ворида()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.эҷод_кардан_ворида()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        компютер = self.эҷод_кардан_ворида()
        компютер['VMState'] = 'poweroff'
        компютер['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.변경없음()

    def test_전환중거부(self):
        self.эҷод_кардан_ворида()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.변경없음()

    def test_등록해제거부(self):
        self.эҷод_кардан_ворида()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        компютер = self.эҷод_кардан_ворида()
        компютер['VMState'] = 'poweroff'
        이전 = dict(компютер)
        self.상자.нокомӣ_қимат = 'make'
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.assertEqual(компютер, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.нокомӣ_қимат = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()
        self.상자.명령들.clear()
        self.assertEqual(self.иҷро_кардан_фармон.иҷро_кардан_фармон()['state'], 'running')
        self.assertFalse(any(фармон[1] == 'createvm' for фармон in self.상자.명령들))

    def test_보존ISO변조거부(self):
        компютер = self.эҷод_кардан_ворида()
        компютер['VMState'] = 'poweroff'
        Path(компютер['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.иҷро_кардан_фармон()

    def test_상태미생성(self):
        self.assertEqual(self.иҷро_кардан_фармон.намоиш_додан_вазъият()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for масир in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.масир(масир)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.иҷро_кардан_фармон.масир('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.сифат_қимат('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
