import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

تعريف_قيمة = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
وحدة_نمطية_قيمة = importlib.util.module_from_spec(تعريف_قيمة)
تعريف_قيمة.loader.exec_module(وحدة_نمطية_قيمة)


class 가짜상자:
    def __init__(self, جذر_قيمة):
        self.جذر_قيمة = جذر_قيمة
        self.명령들 = []
        self.가상기계들 = {}
        self.فشل_قيمة = None

    def __call__(self, وسائط):
        وسائط = list(map(str, وسائط))
        self.명령들.append(وسائط)
        if self.فشل_قيمة == وسائط[1] or (وسائط[0] == 'make' and self.فشل_قيمة == 'make'):
            self.فشل_قيمة = None
            raise وحدة_نمطية_قيمة.실행오류('시험용 فشل_قيمة')
        if وسائط[0] == 'make':
            مسار = self.جذر_قيمة / 'os/build/kernel.iso'
            مسار.parent.mkdir(parents=True, exist_ok=True)
            مسار.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        إجراء = وسائط[1]
        if إجراء == 'list':
            return '\n'.join('"{}" {{{}}}'.format(قيمة['name'], فهرس) for فهرس, قيمة in self.가상기계들.items())
        if إجراء == 'createvm':
            فهرس, اسم = وسائط[وسائط.index('--uuid') + 1], وسائط[وسائط.index('--name') + 1]
            self.가상기계들[فهرس] = {'UUID': فهرس, 'name': اسم, 'VMState': 'poweroff',
                'CfgFile': str(self.جذر_قيمة / '.vbox/machines' / اسم / (اسم + '.vbox')), 'owner': None}
            return ''
        جهاز = self.가상기계들[وسائط[2]]
        if إجراء == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(اسم), json.dumps(قيمة)) for اسم, قيمة in جهاز.items() if اسم != 'owner')
        if إجراء == 'getextradata': return 'Value: ' + جهاز['owner'] if جهاز['owner'] else 'No value set!'
        if إجراء == 'setextradata': جهاز['owner'] = وسائط[4]
        elif إجراء == 'storagectl': جهاز['storagecontrollername0'] = 'JKOROS IDE'
        elif إجراء == 'storageattach': جهاز['JKOROS IDE-0-0'] = وسائط[وسائط.index('--medium') + 1]
        elif إجراء == 'startvm': جهاز['VMState'] = 'running'
        elif إجراء == 'controlvm':
            assert وسائط[3] == 'resume'
            جهاز['VMState'] = 'running'
        elif إجراء != 'modifyvm': raise AssertionError(وسائط)
        return ''


class مجموعة_الاختبارات(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.جذر_قيمة = Path(self.임시.name)
        (self.جذر_قيمة / '.vbox').mkdir()
        self.상자 = 가짜상자(self.جذر_قيمة)
        self.ينفذ_أمر = وحدة_نمطية_قيمة.تطبيق_مشغّل(self.جذر_قيمة, 'jkoros operating system', أمر=self.상자)

    def فتح_إدخال(self):
        نتيجة = self.ينفذ_أمر.ينفذ_أمر()
        self.상자.명령들.clear()
        return self.상자.가상기계들[نتيجة['uuid']]

    def 변경없음(self):
        self.assertTrue(all(أمر[0] == 'VBoxManage' and أمر[1] in ('list', 'showvminfo', 'getextradata') for أمر in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        نتيجة = self.ينفذ_أمر.ينفذ_أمر()
        self.assertEqual(نتيجة['state'], 'running')
        self.assertTrue(Path(نتيجة['iso']).is_file())
        self.assertTrue(any('--nic1' in أمر and 'none' in أمر for أمر in self.상자.명령들))
        self.assertFalse(any('hdd' in أمر or 'discardstate' in أمر or 'createmedium' in أمر for أمر in self.상자.명령들))

    def test_실행중유지(self):
        self.فتح_إدخال()
        self.assertEqual(self.ينفذ_أمر.ينفذ_أمر()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        جهاز = self.فتح_إدخال()
        جهاز['VMState'] = 'saved'
        سجل_قيمة = self.ينفذ_أمر.مسار(self.ينفذ_أمر.قراءة()['serial_log'])
        سجل_قيمة.write_text('saved log')
        self.ينفذ_أمر.ينفذ_أمر()
        self.assertFalse(any(أمر[0] == 'make' or أمر[1] == 'modifyvm' for أمر in self.상자.명령들))
        self.assertEqual([مسار.read_text() for مسار in سجل_قيمة.parent.glob('before-resume-*.log')], ['saved log'])

    def يختبر_إيقاف_مؤقت_و_استئناف(self):
        self.فتح_إدخال()['VMState'] = 'paused'
        self.ينفذ_أمر.ينفذ_أمر()
        self.assertTrue(any(أمر[1] == 'controlvm' and أمر[3] == 'resume' for أمر in self.상자.명령들))
        self.assertFalse(any(أمر[0] == 'make' for أمر in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.변경없음()

    def test_소유표식거부(self):
        self.فتح_إدخال()['owner'] = 'someone-else'
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.فتح_إدخال()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        جهاز = self.فتح_إدخال()
        جهاز['VMState'] = 'poweroff'
        جهاز['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.변경없음()

    def test_전환중거부(self):
        self.فتح_إدخال()['VMState'] = 'saving'
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.변경없음()

    def test_등록해제거부(self):
        self.فتح_إدخال()
        self.상자.가상기계들.clear()
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        جهاز = self.فتح_إدخال()
        جهاز['VMState'] = 'poweroff'
        이전 = dict(جهاز)
        self.상자.فشل_قيمة = 'make'
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.assertEqual(جهاز, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.فشل_قيمة = 'setextradata'
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()
        self.상자.명령들.clear()
        self.assertEqual(self.ينفذ_أمر.ينفذ_أمر()['state'], 'running')
        self.assertFalse(any(أمر[1] == 'createvm' for أمر in self.상자.명령들))

    def test_보존ISO변조거부(self):
        جهاز = self.فتح_إدخال()
        جهاز['VMState'] = 'poweroff'
        Path(جهاز['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.ينفذ_أمر()

    def test_상태미생성(self):
        self.assertEqual(self.ينفذ_أمر.عرض_حالة()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for مسار in ('../outside', '/tmp/outside'):
            with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.مسار(مسار)
        (self.جذر_قيمة / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(وحدة_نمطية_قيمة.실행오류): self.ينفذ_أمر.مسار('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        نتيجة = وحدة_نمطية_قيمة.قيمة_السمة('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(نتيجة['VMState'], 'running')
        self.assertEqual(نتيجة['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
