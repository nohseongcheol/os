import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

تعریف_قدر = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(تعریف_قدر)
تعریف_قدر.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ناکامی_قدر = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ناکامی_قدر == 인수[1] or (인수[0] == 'make' and self.ناکامی_قدر == 'make'):
            self.ناکامی_قدر = None
            raise 모듈.실행오류('시험용 ناکامی_قدر')
        if 인수[0] == 'make':
            راہ = self.뿌리 / 'os/build/kernel.iso'
            راہ.parent.mkdir(parents=True, exist_ok=True)
            راہ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        کم = 인수[1]
        if کم == 'list':
            return '\n'.join('"{}" {{{}}}'.format(قدر['name'], اشاریہ) for اشاریہ, قدر in self.가상기계들.items())
        if کم == 'createvm':
            اشاریہ, ناں = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[اشاریہ] = {'UUID': اشاریہ, 'name': ناں, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / ناں / (ناں + '.vbox')), 'owner': None}
            return ''
        مشین = self.가상기계들[인수[2]]
        if کم == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ناں), json.dumps(قدر)) for ناں, قدر in مشین.items() if ناں != 'owner')
        if کم == 'getextradata': return 'Value: ' + مشین['owner'] if مشین['owner'] else 'No value set!'
        if کم == 'setextradata': مشین['owner'] = 인수[4]
        elif کم == 'storagectl': مشین['storagecontrollername0'] = 'JKOROS IDE'
        elif کم == 'storageattach': مشین['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif کم == 'startvm': مشین['VMState'] = 'running'
        elif کم == 'controlvm':
            assert 인수[3] == 'resume'
            مشین['VMState'] = 'running'
        elif کم != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.نفاذ_کرو_حکم = 모듈.ایپ_عملے_دا_رکن(self.뿌리, 'jkoros operating system', حکم=self.상자)

    def بنڑاؤ_داخلہ(self):
        결과 = self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(حکم[0] == 'VBoxManage' and حکم[1] in ('list', 'showvminfo', 'getextradata') for حکم in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in حکم and 'none' in حکم for حکم in self.상자.명령들))
        self.assertFalse(any('hdd' in حکم or 'discardstate' in حکم or 'createmedium' in حکم for حکم in self.상자.명령들))

    def test_실행중유지(self):
        self.بنڑاؤ_داخلہ()
        self.assertEqual(self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        مشین = self.بنڑاؤ_داخلہ()
        مشین['VMState'] = 'saved'
        لاگ_قدر = self.نفاذ_کرو_حکم.راہ(self.نفاذ_کرو_حکم.읽기()['serial_log'])
        لاگ_قدر.write_text('saved log')
        self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.assertFalse(any(حکم[0] == 'make' or حکم[1] == 'modifyvm' for حکم in self.상자.명령들))
        self.assertEqual([راہ.read_text() for راہ in لاگ_قدر.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.بنڑاؤ_داخلہ()['VMState'] = 'paused'
        self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.assertTrue(any(حکم[1] == 'controlvm' and حکم[3] == 'resume' for حکم in self.상자.명령들))
        self.assertFalse(any(حکم[0] == 'make' for حکم in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.변경없음()

    def test_소유표식거부(self):
        self.بنڑاؤ_داخلہ()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.بنڑاؤ_داخلہ()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        مشین = self.بنڑاؤ_داخلہ()
        مشین['VMState'] = 'poweroff'
        مشین['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.변경없음()

    def test_전환중거부(self):
        self.بنڑاؤ_داخلہ()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.변경없음()

    def test_등록해제거부(self):
        self.بنڑاؤ_داخلہ()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        مشین = self.بنڑاؤ_داخلہ()
        مشین['VMState'] = 'poweroff'
        이전 = dict(مشین)
        self.상자.ناکامی_قدر = 'make'
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.assertEqual(مشین, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ناکامی_قدر = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()
        self.상자.명령들.clear()
        self.assertEqual(self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()['state'], 'running')
        self.assertFalse(any(حکم[1] == 'createvm' for حکم in self.상자.명령들))

    def test_보존ISO변조거부(self):
        مشین = self.بنڑاؤ_داخلہ()
        مشین['VMState'] = 'poweroff'
        Path(مشین['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.نفاذ_کرو_حکم()

    def test_상태미생성(self):
        self.assertEqual(self.نفاذ_کرو_حکم.نمایش_کرو_حالت()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for راہ in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.راہ(راہ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.نفاذ_کرو_حکم.راہ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.وصف_قدر('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
