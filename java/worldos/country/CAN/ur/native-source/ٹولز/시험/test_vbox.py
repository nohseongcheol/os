import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

تعریف_قدر = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ماڈیول_قدر = importlib.util.module_from_spec(تعریف_قدر)
تعریف_قدر.loader.exec_module(ماڈیول_قدر)


class 가짜상자:
    def __init__(self, روٹ_قدر):
        self.روٹ_قدر = روٹ_قدر
        self.명령들 = []
        self.가상기계들 = {}
        self.ناکامی_قدر = None

    def __call__(self, دلائل):
        دلائل = list(map(str, دلائل))
        self.명령들.append(دلائل)
        if self.ناکامی_قدر == دلائل[1] or (دلائل[0] == 'make' and self.ناکامی_قدر == 'make'):
            self.ناکامی_قدر = None
            raise ماڈیول_قدر.실행오류('시험용 ناکامی_قدر')
        if دلائل[0] == 'make':
            راستہ_2 = self.روٹ_قدر / 'os/build/kernel.iso'
            راستہ_2.parent.mkdir(parents=True, exist_ok=True)
            راستہ_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        عمل = دلائل[1]
        if عمل == 'list':
            return '\n'.join('"{}" {{{}}}'.format(قدر['name'], اشاریہ) for اشاریہ, قدر in self.가상기계들.items())
        if عمل == 'createvm':
            اشاریہ, نام = دلائل[دلائل.index('--uuid') + 1], دلائل[دلائل.index('--name') + 1]
            self.가상기계들[اشاریہ] = {'UUID': اشاریہ, 'name': نام, 'VMState': 'poweroff',
                'CfgFile': str(self.روٹ_قدر / '.vbox/machines' / نام / (نام + '.vbox')), 'owner': None}
            return ''
        مشین = self.가상기계들[دلائل[2]]
        if عمل == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(نام), json.dumps(قدر)) for نام, قدر in مشین.items() if نام != 'owner')
        if عمل == 'getextradata': return 'Value: ' + مشین['owner'] if مشین['owner'] else 'No value set!'
        if عمل == 'setextradata': مشین['owner'] = دلائل[4]
        elif عمل == 'storagectl': مشین['storagecontrollername0'] = 'JKOROS IDE'
        elif عمل == 'storageattach': مشین['JKOROS IDE-0-0'] = دلائل[دلائل.index('--medium') + 1]
        elif عمل == 'startvm': مشین['VMState'] = 'running'
        elif عمل == 'controlvm':
            assert دلائل[3] == 'resume'
            مشین['VMState'] = 'running'
        elif عمل != 'modifyvm': raise AssertionError(دلائل)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.روٹ_قدر = Path(self.임시.name)
        (self.روٹ_قدر / '.vbox').mkdir()
        self.상자 = 가짜상자(self.روٹ_قدر)
        self.نفاذ_کریں_حکم = ماڈیول_قدر.ایپ_ایپ_دراز(self.روٹ_قدر, 'jkoros operating system', حکم=self.상자)

    def بنائیں_اندراج(self):
        پیمائش = self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.상자.명령들.clear()
        return self.상자.가상기계들[پیمائش['uuid']]

    def 변경없음(self):
        self.assertTrue(all(حکم[0] == 'VBoxManage' and حکم[1] in ('list', 'showvminfo', 'getextradata') for حکم in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        پیمائش = self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.assertEqual(پیمائش['state'], 'running')
        self.assertTrue(Path(پیمائش['iso']).is_file())
        self.assertTrue(any('--nic1' in حکم and 'none' in حکم for حکم in self.상자.명령들))
        self.assertFalse(any('hdd' in حکم or 'discardstate' in حکم or 'createmedium' in حکم for حکم in self.상자.명령들))

    def test_실행중유지(self):
        self.بنائیں_اندراج()
        self.assertEqual(self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        مشین = self.بنائیں_اندراج()
        مشین['VMState'] = 'saved'
        لاگ_قدر = self.نفاذ_کریں_حکم.راستہ_2(self.نفاذ_کریں_حکم.پڑھیں()['serial_log'])
        لاگ_قدر.write_text('saved log')
        self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.assertFalse(any(حکم[0] == 'make' or حکم[1] == 'modifyvm' for حکم in self.상자.명령들))
        self.assertEqual([راستہ_2.read_text() for راستہ_2 in لاگ_قدر.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.بنائیں_اندراج()['VMState'] = 'paused'
        self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.assertTrue(any(حکم[1] == 'controlvm' and حکم[3] == 'resume' for حکم in self.상자.명령들))
        self.assertFalse(any(حکم[0] == 'make' for حکم in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.변경없음()

    def test_소유표식거부(self):
        self.بنائیں_اندراج()['owner'] = 'someone-else'
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.بنائیں_اندراج()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        مشین = self.بنائیں_اندراج()
        مشین['VMState'] = 'poweroff'
        مشین['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.변경없음()

    def test_전환중거부(self):
        self.بنائیں_اندراج()['VMState'] = 'saving'
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.변경없음()

    def test_등록해제거부(self):
        self.بنائیں_اندراج()
        self.상자.가상기계들.clear()
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        مشین = self.بنائیں_اندراج()
        مشین['VMState'] = 'poweroff'
        이전 = dict(مشین)
        self.상자.ناکامی_قدر = 'make'
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.assertEqual(مشین, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ناکامی_قدر = 'setextradata'
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()
        self.상자.명령들.clear()
        self.assertEqual(self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()['state'], 'running')
        self.assertFalse(any(حکم[1] == 'createvm' for حکم in self.상자.명령들))

    def test_보존ISO변조거부(self):
        مشین = self.بنائیں_اندراج()
        مشین['VMState'] = 'poweroff'
        Path(مشین['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.نفاذ_کریں_حکم()

    def test_상태미생성(self):
        self.assertEqual(self.نفاذ_کریں_حکم.دکھانا_حالت()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for راستہ_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.راستہ_2(راستہ_2)
        (self.روٹ_قدر / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ماڈیول_قدر.실행오류): self.نفاذ_کریں_حکم.راستہ_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        پیمائش = ماڈیول_قدر.وصف_قدر('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(پیمائش['VMState'], 'running')
        self.assertEqual(پیمائش['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
