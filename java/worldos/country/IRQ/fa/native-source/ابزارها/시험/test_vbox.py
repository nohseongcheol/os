import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

تعریف_مقدار = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
مدول_مقدار = importlib.util.module_from_spec(تعریف_مقدار)
تعریف_مقدار.loader.exec_module(مدول_مقدار)


class 가짜상자:
    def __init__(self, جذر_مقدار):
        self.جذر_مقدار = جذر_مقدار
        self.명령들 = []
        self.가상기계들 = {}
        self.عدم_موفقیت_مقدار = None

    def __call__(self, نشانوندها):
        نشانوندها = list(map(str, نشانوندها))
        self.명령들.append(نشانوندها)
        if self.عدم_موفقیت_مقدار == نشانوندها[1] or (نشانوندها[0] == 'make' and self.عدم_موفقیت_مقدار == 'make'):
            self.عدم_موفقیت_مقدار = None
            raise مدول_مقدار.실행오류('시험용 عدم_موفقیت_مقدار')
        if نشانوندها[0] == 'make':
            مسیر = self.جذر_مقدار / 'os/build/kernel.iso'
            مسیر.parent.mkdir(parents=True, exist_ok=True)
            مسیر.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        کنش = نشانوندها[1]
        if کنش == 'list':
            return '\n'.join('"{}" {{{}}}'.format(مقدار['name'], فهرست) for فهرست, مقدار in self.가상기계들.items())
        if کنش == 'createvm':
            فهرست, نام = نشانوندها[نشانوندها.index('--uuid') + 1], نشانوندها[نشانوندها.index('--name') + 1]
            self.가상기계들[فهرست] = {'UUID': فهرست, 'name': نام, 'VMState': 'poweroff',
                'CfgFile': str(self.جذر_مقدار / '.vbox/machines' / نام / (نام + '.vbox')), 'owner': None}
            return ''
        دستگاه = self.가상기계들[نشانوندها[2]]
        if کنش == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(نام), json.dumps(مقدار)) for نام, مقدار in دستگاه.items() if نام != 'owner')
        if کنش == 'getextradata': return 'Value: ' + دستگاه['owner'] if دستگاه['owner'] else 'No value set!'
        if کنش == 'setextradata': دستگاه['owner'] = نشانوندها[4]
        elif کنش == 'storagectl': دستگاه['storagecontrollername0'] = 'JKOROS IDE'
        elif کنش == 'storageattach': دستگاه['JKOROS IDE-0-0'] = نشانوندها[نشانوندها.index('--medium') + 1]
        elif کنش == 'startvm': دستگاه['VMState'] = 'running'
        elif کنش == 'controlvm':
            assert نشانوندها[3] == 'resume'
            دستگاه['VMState'] = 'running'
        elif کنش != 'modifyvm': raise AssertionError(نشانوندها)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.جذر_مقدار = Path(self.임시.name)
        (self.جذر_مقدار / '.vbox').mkdir()
        self.상자 = 가짜상자(self.جذر_مقدار)
        self.اجرا_فرمان = مدول_مقدار.برنامه_راه_انداز(self.جذر_مقدار, 'jkoros operating system', فرمان=self.상자)

    def ایجاد_ورودی(self):
        سنجش = self.اجرا_فرمان.اجرا_فرمان()
        self.상자.명령들.clear()
        return self.상자.가상기계들[سنجش['uuid']]

    def 변경없음(self):
        self.assertTrue(all(فرمان[0] == 'VBoxManage' and فرمان[1] in ('list', 'showvminfo', 'getextradata') for فرمان in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        سنجش = self.اجرا_فرمان.اجرا_فرمان()
        self.assertEqual(سنجش['state'], 'running')
        self.assertTrue(Path(سنجش['iso']).is_file())
        self.assertTrue(any('--nic1' in فرمان and 'none' in فرمان for فرمان in self.상자.명령들))
        self.assertFalse(any('hdd' in فرمان or 'discardstate' in فرمان or 'createmedium' in فرمان for فرمان in self.상자.명령들))

    def test_실행중유지(self):
        self.ایجاد_ورودی()
        self.assertEqual(self.اجرا_فرمان.اجرا_فرمان()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        دستگاه = self.ایجاد_ورودی()
        دستگاه['VMState'] = 'saved'
        واقعه_نگار_مقدار = self.اجرا_فرمان.مسیر(self.اجرا_فرمان.خواندن()['serial_log'])
        واقعه_نگار_مقدار.write_text('saved log')
        self.اجرا_فرمان.اجرا_فرمان()
        self.assertFalse(any(فرمان[0] == 'make' or فرمان[1] == 'modifyvm' for فرمان in self.상자.명령들))
        self.assertEqual([مسیر.read_text() for مسیر in واقعه_نگار_مقدار.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ایجاد_ورودی()['VMState'] = 'paused'
        self.اجرا_فرمان.اجرا_فرمان()
        self.assertTrue(any(فرمان[1] == 'controlvm' and فرمان[3] == 'resume' for فرمان in self.상자.명령들))
        self.assertFalse(any(فرمان[0] == 'make' for فرمان in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.변경없음()

    def test_소유표식거부(self):
        self.ایجاد_ورودی()['owner'] = 'someone-else'
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ایجاد_ورودی()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        دستگاه = self.ایجاد_ورودی()
        دستگاه['VMState'] = 'poweroff'
        دستگاه['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.변경없음()

    def test_전환중거부(self):
        self.ایجاد_ورودی()['VMState'] = 'saving'
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.변경없음()

    def test_등록해제거부(self):
        self.ایجاد_ورودی()
        self.상자.가상기계들.clear()
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        دستگاه = self.ایجاد_ورودی()
        دستگاه['VMState'] = 'poweroff'
        이전 = dict(دستگاه)
        self.상자.عدم_موفقیت_مقدار = 'make'
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.assertEqual(دستگاه, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.عدم_موفقیت_مقدار = 'setextradata'
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()
        self.상자.명령들.clear()
        self.assertEqual(self.اجرا_فرمان.اجرا_فرمان()['state'], 'running')
        self.assertFalse(any(فرمان[1] == 'createvm' for فرمان in self.상자.명령들))

    def test_보존ISO변조거부(self):
        دستگاه = self.ایجاد_ورودی()
        دستگاه['VMState'] = 'poweroff'
        Path(دستگاه['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.اجرا_فرمان()

    def test_상태미생성(self):
        self.assertEqual(self.اجرا_فرمان.نمایش_وضعیت()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for مسیر in ('../outside', '/tmp/outside'):
            with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.مسیر(مسیر)
        (self.جذر_مقدار / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(مدول_مقدار.실행오류): self.اجرا_فرمان.مسیر('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        سنجش = مدول_مقدار.مشخصه_مقدار('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(سنجش['VMState'], 'running')
        self.assertEqual(سنجش['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
