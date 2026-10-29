import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

הגדרה_ערך = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
מודול_ערך = importlib.util.module_from_spec(הגדרה_ערך)
הגדרה_ערך.loader.exec_module(מודול_ערך)


class 가짜상자:
    def __init__(self, בסיס_ערך):
        self.בסיס_ערך = בסיס_ערך
        self.명령들 = []
        self.가상기계들 = {}
        self.כשל_ערך = None

    def __call__(self, ארגומנטים):
        ארגומנטים = list(map(str, ארגומנטים))
        self.명령들.append(ארגומנטים)
        if self.כשל_ערך == ארגומנטים[1] or (ארגומנטים[0] == 'make' and self.כשל_ערך == 'make'):
            self.כשל_ערך = None
            raise מודול_ערך.실행오류('시험용 כשל_ערך')
        if ארגומנטים[0] == 'make':
            נתיב = self.בסיס_ערך / 'os/build/kernel.iso'
            נתיב.parent.mkdir(parents=True, exist_ok=True)
            נתיב.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        פעולה = ארגומנטים[1]
        if פעולה == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ערך['name'], מדד) for מדד, ערך in self.가상기계들.items())
        if פעולה == 'createvm':
            מדד, שם = ארגומנטים[ארגומנטים.index('--uuid') + 1], ארגומנטים[ארגומנטים.index('--name') + 1]
            self.가상기계들[מדד] = {'UUID': מדד, 'name': שם, 'VMState': 'poweroff',
                'CfgFile': str(self.בסיס_ערך / '.vbox/machines' / שם / (שם + '.vbox')), 'owner': None}
            return ''
        מחשב = self.가상기계들[ארגומנטים[2]]
        if פעולה == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(שם), json.dumps(ערך)) for שם, ערך in מחשב.items() if שם != 'owner')
        if פעולה == 'getextradata': return 'Value: ' + מחשב['owner'] if מחשב['owner'] else 'No value set!'
        if פעולה == 'setextradata': מחשב['owner'] = ארגומנטים[4]
        elif פעולה == 'storagectl': מחשב['storagecontrollername0'] = 'JKOROS IDE'
        elif פעולה == 'storageattach': מחשב['JKOROS IDE-0-0'] = ארגומנטים[ארגומנטים.index('--medium') + 1]
        elif פעולה == 'startvm': מחשב['VMState'] = 'running'
        elif פעולה == 'controlvm':
            assert ארגומנטים[3] == 'resume'
            מחשב['VMState'] = 'running'
        elif פעולה != 'modifyvm': raise AssertionError(ארגומנטים)
        return ''


class בדיקות_שהופעלו(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.בסיס_ערך = Path(self.임시.name)
        (self.בסיס_ערך / '.vbox').mkdir()
        self.상자 = 가짜상자(self.בסיס_ערך)
        self.לבצע_פקודה = מודול_ערך.תוכנית_מפעיל(self.בסיס_ערך, 'jkoros operating system', פקודה=self.상자)

    def ליצור_ערך(self):
        תוצאה = self.לבצע_פקודה.לבצע_פקודה()
        self.상자.명령들.clear()
        return self.상자.가상기계들[תוצאה['uuid']]

    def 변경없음(self):
        self.assertTrue(all(פקודה[0] == 'VBoxManage' and פקודה[1] in ('list', 'showvminfo', 'getextradata') for פקודה in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        תוצאה = self.לבצע_פקודה.לבצע_פקודה()
        self.assertEqual(תוצאה['state'], 'running')
        self.assertTrue(Path(תוצאה['iso']).is_file())
        self.assertTrue(any('--nic1' in פקודה and 'none' in פקודה for פקודה in self.상자.명령들))
        self.assertFalse(any('hdd' in פקודה or 'discardstate' in פקודה or 'createmedium' in פקודה for פקודה in self.상자.명령들))

    def test_실행중유지(self):
        self.ליצור_ערך()
        self.assertEqual(self.לבצע_פקודה.לבצע_פקודה()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        מחשב = self.ליצור_ערך()
        מחשב['VMState'] = 'saved'
        לרשום_ערך = self.לבצע_פקודה.נתיב(self.לבצע_פקודה.קרא()['serial_log'])
        לרשום_ערך.write_text('saved log')
        self.לבצע_פקודה.לבצע_פקודה()
        self.assertFalse(any(פקודה[0] == 'make' or פקודה[1] == 'modifyvm' for פקודה in self.상자.명령들))
        self.assertEqual([נתיב.read_text() for נתיב in לרשום_ערך.parent.glob('before-resume-*.log')], ['saved log'])

    def נסה_השהה_פעולת_גם_חדש_פעולה(self):
        self.ליצור_ערך()['VMState'] = 'paused'
        self.לבצע_פקודה.לבצע_פקודה()
        self.assertTrue(any(פקודה[1] == 'controlvm' and פקודה[3] == 'resume' for פקודה in self.상자.명령들))
        self.assertFalse(any(פקודה[0] == 'make' for פקודה in self.상자.명령들))

    def נסה_אחר_מחשב_וירטואלי_שם_התנגשות(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.변경없음()

    def test_소유표식거부(self):
        self.ליצור_ערך()['owner'] = 'someone-else'
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ליצור_ערך()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        מחשב = self.ליצור_ערך()
        מחשב['VMState'] = 'poweroff'
        מחשב['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.변경없음()

    def test_전환중거부(self):
        self.ליצור_ערך()['VMState'] = 'saving'
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.변경없음()

    def test_등록해제거부(self):
        self.ליצור_ערך()
        self.상자.가상기계들.clear()
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        מחשב = self.ליצור_ערך()
        מחשב['VMState'] = 'poweroff'
        이전 = dict(מחשב)
        self.상자.כשל_ערך = 'make'
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.assertEqual(מחשב, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.כשל_ערך = 'setextradata'
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()
        self.상자.명령들.clear()
        self.assertEqual(self.לבצע_פקודה.לבצע_פקודה()['state'], 'running')
        self.assertFalse(any(פקודה[1] == 'createvm' for פקודה in self.상자.명령들))

    def test_보존ISO변조거부(self):
        מחשב = self.ליצור_ערך()
        מחשב['VMState'] = 'poweroff'
        Path(מחשב['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.לבצע_פקודה()

    def test_상태미생성(self):
        self.assertEqual(self.לבצע_פקודה.הופעה_מצב()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for נתיב in ('../outside', '/tmp/outside'):
            with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.נתיב(נתיב)
        (self.בסיס_ערך / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(מודול_ערך.실행오류): self.לבצע_פקודה.נתיב('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        תוצאה = מודול_ערך.ערך_תכונה('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(תוצאה['VMState'], 'running')
        self.assertEqual(תוצאה['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
