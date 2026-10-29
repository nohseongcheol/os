import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

সংজ্ঞা_মান = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
মডিউল_মান = importlib.util.module_from_spec(সংজ্ঞা_মান)
সংজ্ঞা_মান.loader.exec_module(মডিউল_মান)


class 가짜상자:
    def __init__(self, ৰুট_মান):
        self.ৰুট_মান = ৰুট_মান
        self.명령들 = []
        self.가상기계들 = {}
        self.বিফলতা_মান = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.বিফলতা_মান == 인수[1] or (인수[0] == 'make' and self.বিফলতা_মান == 'make'):
            self.বিফলতা_মান = None
            raise মডিউল_মান.실행오류('시험용 বিফলতা_মান')
        if 인수[0] == 'make':
            পথ = self.ৰুট_মান / 'os/build/kernel.iso'
            পথ.parent.mkdir(parents=True, exist_ok=True)
            পথ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        কাৰ্য্য = 인수[1]
        if কাৰ্য্য == 'list':
            return '\n'.join('"{}" {{{}}}'.format(মান['name'], ইনডেক্স) for ইনডেক্স, মান in self.가상기계들.items())
        if কাৰ্য্য == 'createvm':
            ইনডেক্স, নাম = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ইনডেক্স] = {'UUID': ইনডেক্স, 'name': নাম, 'VMState': 'poweroff',
                'CfgFile': str(self.ৰুট_মান / '.vbox/machines' / নাম / (নাম + '.vbox')), 'owner': None}
            return ''
        মেচিন = self.가상기계들[인수[2]]
        if কাৰ্য্য == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(নাম), json.dumps(মান)) for নাম, মান in মেচিন.items() if নাম != 'owner')
        if কাৰ্য্য == 'getextradata': return 'Value: ' + মেচিন['owner'] if মেচিন['owner'] else 'No value set!'
        if কাৰ্য্য == 'setextradata': মেচিন['owner'] = 인수[4]
        elif কাৰ্য্য == 'storagectl': মেচিন['storagecontrollername0'] = 'JKOROS IDE'
        elif কাৰ্য্য == 'storageattach': মেচিন['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif কাৰ্য্য == 'startvm': মেচিন['VMState'] = 'running'
        elif কাৰ্য্য == 'controlvm':
            assert 인수[3] == 'resume'
            মেচিন['VMState'] = 'running'
        elif কাৰ্য্য != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ৰুট_মান = Path(self.임시.name)
        (self.ৰুট_মান / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ৰুট_মান)
        self.নিষ্পাদন_আদেশ = মডিউল_মান.এপ্প্_এপ্প্_ড্ৰৱাৰ(self.ৰুট_মান, 'jkoros operating system', কমান্ড=self.상자)

    def ক্ৰিয়েট_প্রবিষ্ট(self):
        পৰিমাপ = self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[পৰিমাপ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(কমান্ড[0] == 'VBoxManage' and কমান্ড[1] in ('list', 'showvminfo', 'getextradata') for কমান্ড in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        পৰিমাপ = self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.assertEqual(পৰিমাপ['state'], 'running')
        self.assertTrue(Path(পৰিমাপ['iso']).is_file())
        self.assertTrue(any('--nic1' in কমান্ড and 'none' in কমান্ড for কমান্ড in self.상자.명령들))
        self.assertFalse(any('hdd' in কমান্ড or 'discardstate' in কমান্ড or 'createmedium' in কমান্ড for কমান্ড in self.상자.명령들))

    def test_실행중유지(self):
        self.ক্ৰিয়েট_প্রবিষ্ট()
        self.assertEqual(self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        মেচিন = self.ক্ৰিয়েট_প্রবিষ্ট()
        মেচিন['VMState'] = 'saved'
        লগ_মান = self.নিষ্পাদন_আদেশ.পথ(self.নিষ্পাদন_আদেশ.পড়া()['serial_log'])
        লগ_মান.write_text('saved log')
        self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.assertFalse(any(কমান্ড[0] == 'make' or কমান্ড[1] == 'modifyvm' for কমান্ড in self.상자.명령들))
        self.assertEqual([পথ.read_text() for পথ in লগ_মান.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ক্ৰিয়েট_প্রবিষ্ট()['VMState'] = 'paused'
        self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.assertTrue(any(কমান্ড[1] == 'controlvm' and কমান্ড[3] == 'resume' for কমান্ড in self.상자.명령들))
        self.assertFalse(any(কমান্ড[0] == 'make' for কমান্ড in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ক্ৰিয়েট_প্রবিষ্ট()['owner'] = 'someone-else'
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ক্ৰিয়েট_প্রবিষ্ট()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        মেচিন = self.ক্ৰিয়েট_প্রবিষ্ট()
        মেচিন['VMState'] = 'poweroff'
        মেচিন['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.변경없음()

    def test_전환중거부(self):
        self.ক্ৰিয়েট_প্রবিষ্ট()['VMState'] = 'saving'
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ক্ৰিয়েট_প্রবিষ্ট()
        self.상자.가상기계들.clear()
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        মেচিন = self.ক্ৰিয়েট_প্রবিষ্ট()
        মেচিন['VMState'] = 'poweroff'
        이전 = dict(মেচিন)
        self.상자.বিফলতা_মান = 'make'
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.assertEqual(মেচিন, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.বিফলতা_মান = 'setextradata'
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()
        self.상자.명령들.clear()
        self.assertEqual(self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()['state'], 'running')
        self.assertFalse(any(কমান্ড[1] == 'createvm' for কমান্ড in self.상자.명령들))

    def test_보존ISO변조거부(self):
        মেচিন = self.ক্ৰিয়েট_প্রবিষ্ট()
        মেচিন['VMState'] = 'poweroff'
        Path(মেচিন['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ()

    def test_상태미생성(self):
        self.assertEqual(self.নিষ্পাদন_আদেশ.শ্ব_অৱস্থা()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for পথ in ('../outside', '/tmp/outside'):
            with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.পথ(পথ)
        (self.ৰুট_মান / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(মডিউল_মান.실행오류): self.নিষ্পাদন_আদেশ.পথ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        পৰিমাপ = মডিউল_মান.গুণাগুণ_মান('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(পৰিমাপ['VMState'], 'running')
        self.assertEqual(পৰিমাপ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
