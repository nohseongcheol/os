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
    def __init__(self, মূল_মান):
        self.মূল_মান = মূল_মান
        self.명령들 = []
        self.가상기계들 = {}
        self.বিফলতা_মান = None

    def __call__(self, আর্গুমেন্ট_তালিকা):
        আর্গুমেন্ট_তালিকা = list(map(str, আর্গুমেন্ট_তালিকা))
        self.명령들.append(আর্গুমেন্ট_তালিকা)
        if self.বিফলতা_মান == আর্গুমেন্ট_তালিকা[1] or (আর্গুমেন্ট_তালিকা[0] == 'make' and self.বিফলতা_মান == 'make'):
            self.বিফলতা_মান = None
            raise মডিউল_মান.실행오류('시험용 বিফলতা_মান')
        if আর্গুমেন্ট_তালিকা[0] == 'make':
            পথ_2 = self.মূল_মান / 'os/build/kernel.iso'
            পথ_2.parent.mkdir(parents=True, exist_ok=True)
            পথ_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        কাজ = আর্গুমেন্ট_তালিকা[1]
        if কাজ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(মান['name'], সূচি) for সূচি, মান in self.가상기계들.items())
        if কাজ == 'createvm':
            সূচি, নাম = আর্গুমেন্ট_তালিকা[আর্গুমেন্ট_তালিকা.index('--uuid') + 1], আর্গুমেন্ট_তালিকা[আর্গুমেন্ট_তালিকা.index('--name') + 1]
            self.가상기계들[সূচি] = {'UUID': সূচি, 'name': নাম, 'VMState': 'poweroff',
                'CfgFile': str(self.মূল_মান / '.vbox/machines' / নাম / (নাম + '.vbox')), 'owner': None}
            return ''
        মেশিন = self.가상기계들[আর্গুমেন্ট_তালিকা[2]]
        if কাজ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(নাম), json.dumps(মান)) for নাম, মান in মেশিন.items() if নাম != 'owner')
        if কাজ == 'getextradata': return 'Value: ' + মেশিন['owner'] if মেশিন['owner'] else 'No value set!'
        if কাজ == 'setextradata': মেশিন['owner'] = আর্গুমেন্ট_তালিকা[4]
        elif কাজ == 'storagectl': মেশিন['storagecontrollername0'] = 'JKOROS IDE'
        elif কাজ == 'storageattach': মেশিন['JKOROS IDE-0-0'] = আর্গুমেন্ট_তালিকা[আর্গুমেন্ট_তালিকা.index('--medium') + 1]
        elif কাজ == 'startvm': মেশিন['VMState'] = 'running'
        elif কাজ == 'controlvm':
            assert আর্গুমেন্ট_তালিকা[3] == 'resume'
            মেশিন['VMState'] = 'running'
        elif কাজ != 'modifyvm': raise AssertionError(আর্গুমেন্ট_তালিকা)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.মূল_মান = Path(self.임시.name)
        (self.মূল_মান / '.vbox').mkdir()
        self.상자 = 가짜상자(self.মূল_মান)
        self.কার্যকর_করুন_আদেশ = মডিউল_মান.অ্যাপ_অ্যাপ_লঞ্চার(self.মূল_মান, 'jkoros operating system', আদেশ=self.상자)

    def ক্রিয়েট_ভুক্তি(self):
        পরিমাপ = self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[পরিমাপ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(আদেশ[0] == 'VBoxManage' and আদেশ[1] in ('list', 'showvminfo', 'getextradata') for আদেশ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        পরিমাপ = self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.assertEqual(পরিমাপ['state'], 'running')
        self.assertTrue(Path(পরিমাপ['iso']).is_file())
        self.assertTrue(any('--nic1' in আদেশ and 'none' in আদেশ for আদেশ in self.상자.명령들))
        self.assertFalse(any('hdd' in আদেশ or 'discardstate' in আদেশ or 'createmedium' in আদেশ for আদেশ in self.상자.명령들))

    def test_실행중유지(self):
        self.ক্রিয়েট_ভুক্তি()
        self.assertEqual(self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        মেশিন = self.ক্রিয়েট_ভুক্তি()
        মেশিন['VMState'] = 'saved'
        লগ_মান = self.কার্যকর_করুন_আদেশ.পথ_2(self.কার্যকর_করুন_আদেশ.পড়া()['serial_log'])
        লগ_মান.write_text('saved log')
        self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.assertFalse(any(আদেশ[0] == 'make' or আদেশ[1] == 'modifyvm' for আদেশ in self.상자.명령들))
        self.assertEqual([পথ_2.read_text() for পথ_2 in লগ_মান.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ক্রিয়েট_ভুক্তি()['VMState'] = 'paused'
        self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.assertTrue(any(আদেশ[1] == 'controlvm' and আদেশ[3] == 'resume' for আদেশ in self.상자.명령들))
        self.assertFalse(any(আদেশ[0] == 'make' for আদেশ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ক্রিয়েট_ভুক্তি()['owner'] = 'someone-else'
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ক্রিয়েট_ভুক্তি()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        মেশিন = self.ক্রিয়েট_ভুক্তি()
        মেশিন['VMState'] = 'poweroff'
        মেশিন['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.변경없음()

    def test_전환중거부(self):
        self.ক্রিয়েট_ভুক্তি()['VMState'] = 'saving'
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ক্রিয়েট_ভুক্তি()
        self.상자.가상기계들.clear()
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        মেশিন = self.ক্রিয়েট_ভুক্তি()
        মেশিন['VMState'] = 'poweroff'
        이전 = dict(মেশিন)
        self.상자.বিফলতা_মান = 'make'
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.assertEqual(মেশিন, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.বিফলতা_মান = 'setextradata'
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()
        self.상자.명령들.clear()
        self.assertEqual(self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()['state'], 'running')
        self.assertFalse(any(আদেশ[1] == 'createvm' for আদেশ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        মেশিন = self.ক্রিয়েট_ভুক্তি()
        মেশিন['VMState'] = 'poweroff'
        Path(মেশিন['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ()

    def test_상태미생성(self):
        self.assertEqual(self.কার্যকর_করুন_আদেশ.শো_অবস্হা()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for পথ_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.পথ_2(পথ_2)
        (self.মূল_মান / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(মডিউল_মান.실행오류): self.কার্যকর_করুন_আদেশ.পথ_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        পরিমাপ = মডিউল_মান.গুণ_মান('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(পরিমাপ['VMState'], 'running')
        self.assertEqual(পরিমাপ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
