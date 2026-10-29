import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

ବ୍ୟାଖ୍ୟା_ମୂଲ୍ୟ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ = importlib.util.module_from_spec(ବ୍ୟାଖ୍ୟା_ମୂଲ୍ୟ)
ବ୍ୟାଖ୍ୟା_ମୂଲ୍ୟ.loader.exec_module(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ)


class 가짜상자:
    def __init__(self, ରୁଟ୍_ମୂଲ୍ୟ):
        self.ରୁଟ୍_ମୂଲ୍ୟ = ରୁଟ୍_ମୂଲ୍ୟ
        self.명령들 = []
        self.가상기계들 = {}
        self.ବିଫଳତା_ମୂଲ୍ୟ = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ବିଫଳତା_ମୂଲ୍ୟ == 인수[1] or (인수[0] == 'make' and self.ବିଫଳତା_ମୂଲ୍ୟ == 'make'):
            self.ବିଫଳତା_ମୂଲ୍ୟ = None
            raise ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류('시험용 ବିଫଳତା_ମୂଲ୍ୟ')
        if 인수[0] == 'make':
            ପଥ = self.ରୁଟ୍_ମୂଲ୍ୟ / 'os/build/kernel.iso'
            ପଥ.parent.mkdir(parents=True, exist_ok=True)
            ପଥ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        କାମ = 인수[1]
        if କାମ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ମୂଲ୍ୟ['name'], ଅନୁକ୍ରମଣିକା) for ଅନୁକ୍ରମଣିକା, ମୂଲ୍ୟ in self.가상기계들.items())
        if କାମ == 'createvm':
            ଅନୁକ୍ରମଣିକା, ନାମ = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ଅନୁକ୍ରମଣିକା] = {'UUID': ଅନୁକ୍ରମଣିକା, 'name': ନାମ, 'VMState': 'poweroff',
                'CfgFile': str(self.ରୁଟ୍_ମୂଲ୍ୟ / '.vbox/machines' / ନାମ / (ନାମ + '.vbox')), 'owner': None}
            return ''
        ମେସିନ୍ = self.가상기계들[인수[2]]
        if କାମ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ନାମ), json.dumps(ମୂଲ୍ୟ)) for ନାମ, ମୂଲ୍ୟ in ମେସିନ୍.items() if ନାମ != 'owner')
        if କାମ == 'getextradata': return 'Value: ' + ମେସିନ୍['owner'] if ମେସିନ୍['owner'] else 'No value set!'
        if କାମ == 'setextradata': ମେସିନ୍['owner'] = 인수[4]
        elif କାମ == 'storagectl': ମେସିନ୍['storagecontrollername0'] = 'JKOROS IDE'
        elif କାମ == 'storageattach': ମେସିନ୍['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif କାମ == 'startvm': ମେସିନ୍['VMState'] = 'running'
        elif କାମ == 'controlvm':
            assert 인수[3] == 'resume'
            ମେସିନ୍['VMState'] = 'running'
        elif କାମ != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ରୁଟ୍_ମୂଲ୍ୟ = Path(self.임시.name)
        (self.ରୁଟ୍_ମୂଲ୍ୟ / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ରୁଟ୍_ମୂଲ୍ୟ)
        self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ = ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍(self.ରୁଟ୍_ମୂଲ୍ୟ, 'jkoros operating system', ନିର୍ଦ୍ଦେଶ=self.상자)

    def ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(self):
        ମାପ = self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ମାପ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ନିର୍ଦ୍ଦେଶ[0] == 'VBoxManage' and ନିର୍ଦ୍ଦେଶ[1] in ('list', 'showvminfo', 'getextradata') for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ମାପ = self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.assertEqual(ମାପ['state'], 'running')
        self.assertTrue(Path(ମାପ['iso']).is_file())
        self.assertTrue(any('--nic1' in ନିର୍ଦ୍ଦେଶ and 'none' in ନିର୍ଦ୍ଦେଶ for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))
        self.assertFalse(any('hdd' in ନିର୍ଦ୍ଦେଶ or 'discardstate' in ନିର୍ଦ୍ଦେଶ or 'createmedium' in ନିର୍ଦ୍ଦେଶ for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))

    def test_실행중유지(self):
        self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()
        self.assertEqual(self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ମେସିନ୍ = self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()
        ମେସିନ୍['VMState'] = 'saved'
        ଲଗ୍_ମୂଲ୍ୟ = self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପଥ(self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପଢନ୍ତୁ()['serial_log'])
        ଲଗ୍_ମୂଲ୍ୟ.write_text('saved log')
        self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.assertFalse(any(ନିର୍ଦ୍ଦେଶ[0] == 'make' or ନିର୍ଦ୍ଦେଶ[1] == 'modifyvm' for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))
        self.assertEqual([ପଥ.read_text() for ପଥ in ଲଗ୍_ମୂଲ୍ୟ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()['VMState'] = 'paused'
        self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.assertTrue(any(ନିର୍ଦ୍ଦେଶ[1] == 'controlvm' and ନିର୍ଦ୍ଦେଶ[3] == 'resume' for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))
        self.assertFalse(any(ନିର୍ଦ୍ଦେଶ[0] == 'make' for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()['owner'] = 'someone-else'
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ମେସିନ୍ = self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()
        ମେସିନ୍['VMState'] = 'poweroff'
        ମେସିନ୍['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.변경없음()

    def test_전환중거부(self):
        self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()['VMState'] = 'saving'
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()
        self.상자.가상기계들.clear()
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ମେସିନ୍ = self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()
        ମେସିନ୍['VMState'] = 'poweroff'
        이전 = dict(ମେସିନ୍)
        self.상자.ବିଫଳତା_ମୂଲ୍ୟ = 'make'
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.assertEqual(ମେସିନ୍, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ବିଫଳତା_ମୂଲ୍ୟ = 'setextradata'
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
        self.상자.명령들.clear()
        self.assertEqual(self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()['state'], 'running')
        self.assertFalse(any(ନିର୍ଦ୍ଦେଶ[1] == 'createvm' for ନିର୍ଦ୍ଦେଶ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ମେସିନ୍ = self.ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି()
        ମେସିନ୍['VMState'] = 'poweroff'
        Path(ମେସିନ୍['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()

    def test_상태미생성(self):
        self.assertEqual(self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପ୍ରଦର୍ଶନ_କରିବା_ସ୍ଥିତି()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ପଥ in ('../outside', '/tmp/outside'):
            with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପଥ(ପଥ)
        (self.ରୁଟ୍_ମୂଲ୍ୟ / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.실행오류): self.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପଥ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ମାପ = ମଡ୍ୟୁଲ୍_ମୂଲ୍ୟ.ଗୁଣ_ମୂଲ୍ୟ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ମାପ['VMState'], 'running')
        self.assertEqual(ମାପ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
