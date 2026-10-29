import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

정의 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
မော်ဂျူးတန်ဖိုး = importlib.util.module_from_spec(정의)
정의.loader.exec_module(မော်ဂျူးတန်ဖိုး)


class 가짜상자:
    def __init__(self, အမြစ်တန်ဖိုး):
        self.အမြစ်တန်ဖိုး = အမြစ်တန်ဖိုး
        self.အမိန့်များစာရင်း = []
        self.가상기계들 = {}
        self.မအောင်မြင်မှု = None

    def __call__(self, အချက်များ):
        အချက်များ = list(map(str, အချက်များ))
        self.အမိန့်များစာရင်း.append(အချက်များ)
        if self.မအောင်မြင်မှု == အချက်များ[1] or (အချက်များ[0] == 'make' and self.မအောင်မြင်မှု == 'make'):
            self.မအောင်မြင်မှု = None
            raise မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား('시험용 မအောင်မြင်မှု')
        if အချက်များ[0] == 'make':
            လမ်း = self.အမြစ်တန်ဖိုး / 'os/build/kernel.iso'
            လမ်း.parent.mkdir(parents=True, exist_ok=True)
            လမ်း.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        လှုပ်ရှားမှု = အချက်များ[1]
        if လှုပ်ရှားမှု == 'list':
            return '\n'.join('"{}" {{{}}}'.format(တန်ဖိုး['name'], နံပါတ်) for နံပါတ်, တန်ဖိုး in self.가상기계들.items())
        if လှုပ်ရှားမှု == 'createvm':
            နံပါတ်, အမည် = အချက်များ[အချက်များ.index('--uuid') + 1], အချက်များ[အချက်များ.index('--name') + 1]
            self.가상기계들[နံပါတ်] = {'UUID': နံပါတ်, 'name': အမည်, 'VMState': 'poweroff',
                'CfgFile': str(self.အမြစ်တန်ဖိုး / '.vbox/machines' / အမည် / (အမည် + '.vbox')), 'owner': None}
            return ''
        စက် = self.가상기계들[အချက်များ[2]]
        if လှုပ်ရှားမှု == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(အမည်), json.dumps(တန်ဖိုး)) for အမည်, တန်ဖိုး in စက်.items() if အမည် != 'owner')
        if လှုပ်ရှားမှု == 'getextradata': return 'Value: ' + စက်['owner'] if စက်['owner'] else 'No value set!'
        if လှုပ်ရှားမှု == 'setextradata': စက်['owner'] = အချက်များ[4]
        elif လှုပ်ရှားမှု == 'storagectl': စက်['storagecontrollername0'] = 'JKOROS IDE'
        elif လှုပ်ရှားမှု == 'storageattach': စက်['JKOROS IDE-0-0'] = အချက်များ[အချက်များ.index('--medium') + 1]
        elif လှုပ်ရှားမှု == 'startvm': စက်['VMState'] = 'running'
        elif လှုပ်ရှားမှု == 'controlvm':
            assert အချက်များ[3] == 'resume'
            စက်['VMState'] = 'running'
        elif လှုပ်ရှားမှု != 'modifyvm': raise AssertionError(အချက်များ)
        return ''


class စက်မောင်းစမ်းသပ်(unittest.TestCase):
    def setUp(self):
        self.ယာယီတန်ဖိုး = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.ယာယီတန်ဖိုး.cleanup)
        self.အမြစ်တန်ဖိုး = Path(self.ယာယီတန်ဖိုး.name)
        (self.အမြစ်တန်ဖိုး / '.vbox').mkdir()
        self.상자 = 가짜상자(self.အမြစ်တန်ဖိုး)
        self.စက်မောင်း = မော်ဂျူးတန်ဖိုး.ပရိုဂရမ်စက်နှိုးကိရိယာ(self.အမြစ်တန်ဖိုး, 'jkoros operating system', အမိန့်=self.상자)

    def အချက်ဖန်တီး(self):
        ရလဒ် = self.စက်မောင်း.စက်မောင်း()
        self.상자.အမိန့်များစာရင်း.clear()
        return self.상자.가상기계들[ရလဒ်['uuid']]

    def 변경없음(self):
        self.assertTrue(all(အမိန့်[0] == 'VBoxManage' and အမိန့်[1] in ('list', 'showvminfo', 'getextradata') for အမိန့် in self.상자.အမိန့်များစာရင်း))

    def test_첫생성과광학부팅(self):
        ရလဒ် = self.စက်မောင်း.စက်မောင်း()
        self.assertEqual(ရလဒ်['state'], 'running')
        self.assertTrue(Path(ရလဒ်['iso']).is_file())
        self.assertTrue(any('--nic1' in အမိန့် and 'none' in အမိန့် for အမိန့် in self.상자.အမိန့်များစာရင်း))
        self.assertFalse(any('hdd' in အမိန့် or 'discardstate' in အမိန့် or 'createmedium' in အမိန့် for အမိန့် in self.상자.အမိန့်များစာရင်း))

    def test_실행중유지(self):
        self.အချက်ဖန်တီး()
        self.assertEqual(self.စက်မောင်း.စက်မောင်း()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        စက် = self.အချက်ဖန်တီး()
        စက်['VMState'] = 'saved'
        မှတ်တမ်းတန်ဖိုး = self.စက်မောင်း.လမ်း(self.စက်မောင်း.ဖတ်()['serial_log'])
        မှတ်တမ်းတန်ဖိုး.write_text('saved log')
        self.စက်မောင်း.စက်မောင်း()
        self.assertFalse(any(အမိန့်[0] == 'make' or အမိန့်[1] == 'modifyvm' for အမိန့် in self.상자.အမိန့်များစာရင်း))
        self.assertEqual([လမ်း.read_text() for လမ်း in မှတ်တမ်းတန်ဖိုး.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.အချက်ဖန်တီး()['VMState'] = 'paused'
        self.စက်မောင်း.စက်မောင်း()
        self.assertTrue(any(အမိန့်[1] == 'controlvm' and အမိန့်[3] == 'resume' for အမိန့် in self.상자.အမိန့်များစာရင်း))
        self.assertFalse(any(အမိန့်[0] == 'make' for အမိန့် in self.상자.အမိန့်များစာရင်း))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.변경없음()

    def test_소유표식거부(self):
        self.အချက်ဖန်တီး()['owner'] = 'someone-else'
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.အချက်ဖန်တီး()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        စက် = self.အချက်ဖန်တီး()
        စက်['VMState'] = 'poweroff'
        စက်['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.변경없음()

    def test_전환중거부(self):
        self.အချက်ဖန်တီး()['VMState'] = 'saving'
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.변경없음()

    def test_등록해제거부(self):
        self.အချက်ဖန်တီး()
        self.상자.가상기계들.clear()
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        စက် = self.အချက်ဖန်တီး()
        စက်['VMState'] = 'poweroff'
        ယခင်အချက်အလက်တစ်ခု = dict(စက်)
        self.상자.မအောင်မြင်မှု = 'make'
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.assertEqual(စက်, ယခင်အချက်အလက်တစ်ခု)

    def test_중단된소유표식설정복구(self):
        self.상자.မအောင်မြင်မှု = 'setextradata'
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()
        self.상자.အမိန့်များစာရင်း.clear()
        self.assertEqual(self.စက်မောင်း.စက်မောင်း()['state'], 'running')
        self.assertFalse(any(အမိန့်[1] == 'createvm' for အမိန့် in self.상자.အမိန့်များစာရင်း))

    def test_보존ISO변조거부(self):
        စက် = self.အချက်ဖန်တီး()
        စက်['VMState'] = 'poweroff'
        Path(စက်['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.စက်မောင်း()

    def test_상태미생성(self):
        self.assertEqual(self.စက်မောင်း.အခြေအနေပြသ()['state'], 'not-created')
        self.assertFalse(self.상자.အမိန့်များစာရင်း)

    def test_경로탈출거부(self):
        for လမ်း in ('../outside', '/tmp/outside'):
            with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.လမ်း(လမ်း)
        (self.အမြစ်တန်ဖိုး / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(မော်ဂျူးတန်ဖိုး.လုပ်ဆောင်မှုအမှား): self.စက်မောင်း.လမ်း('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ရလဒ် = မော်ဂျူးတန်ဖိုး.ဂုဏ်သတ္တိတန်ဖိုး('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ရလဒ်['VMState'], 'running')
        self.assertEqual(ရလဒ်['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
