import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

deifinisean_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
mòideal_VALUE = importlib.util.module_from_spec(deifinisean_VALUE)
deifinisean_VALUE.loader.exec_module(mòideal_VALUE)


class 가짜상자:
    def __init__(self, freumh_VALUE):
        self.freumh_VALUE = freumh_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.fàilligeadh_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.fàilligeadh_VALUE == 인수[1] or (인수[0] == 'make' and self.fàilligeadh_VALUE == 'make'):
            self.fàilligeadh_VALUE = None
            raise mòideal_VALUE.실행오류('시험용 fàilligeadh_VALUE')
        if 인수[0] == 'make':
            Slighe = self.freumh_VALUE / 'os/build/kernel.iso'
            Slighe.parent.mkdir(parents=True, exist_ok=True)
            Slighe.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Gnìomh = 인수[1]
        if Gnìomh == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Gnìomh == 'createvm':
            INDEX, Ainm = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Ainm, 'VMState': 'poweroff',
                'CfgFile': str(self.freumh_VALUE / '.vbox/machines' / Ainm / (Ainm + '.vbox')), 'owner': None}
            return ''
        inneal = self.가상기계들[인수[2]]
        if Gnìomh == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ainm), json.dumps(VALUE)) for Ainm, VALUE in inneal.items() if Ainm != 'owner')
        if Gnìomh == 'getextradata': return 'Value: ' + inneal['owner'] if inneal['owner'] else 'No value set!'
        if Gnìomh == 'setextradata': inneal['owner'] = 인수[4]
        elif Gnìomh == 'storagectl': inneal['storagecontrollername0'] = 'JKOROS IDE'
        elif Gnìomh == 'storageattach': inneal['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Gnìomh == 'startvm': inneal['VMState'] = 'running'
        elif Gnìomh == 'controlvm':
            assert 인수[3] == 'resume'
            inneal['VMState'] = 'running'
        elif Gnìomh != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.freumh_VALUE = Path(self.임시.name)
        (self.freumh_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.freumh_VALUE)
        self.gnìomhaich_àithne = mòideal_VALUE.ap_drathair_nan_aplacaid(self.freumh_VALUE, 'jkoros operating system', àithne=self.상자)

    def Create_cur_a_steach(self):
        tomhas = self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.상자.명령들.clear()
        return self.상자.가상기계들[tomhas['uuid']]

    def 변경없음(self):
        self.assertTrue(all(àithne[0] == 'VBoxManage' and àithne[1] in ('list', 'showvminfo', 'getextradata') for àithne in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        tomhas = self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.assertEqual(tomhas['state'], 'running')
        self.assertTrue(Path(tomhas['iso']).is_file())
        self.assertTrue(any('--nic1' in àithne and 'none' in àithne for àithne in self.상자.명령들))
        self.assertFalse(any('hdd' in àithne or 'discardstate' in àithne or 'createmedium' in àithne for àithne in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_cur_a_steach()
        self.assertEqual(self.gnìomhaich_àithne.gnìomhaich_àithne()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        inneal = self.Create_cur_a_steach()
        inneal['VMState'] = 'saved'
        LOG_VALUE = self.gnìomhaich_àithne.Slighe(self.gnìomhaich_àithne.읽기()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.assertFalse(any(àithne[0] == 'make' or àithne[1] == 'modifyvm' for àithne in self.상자.명령들))
        self.assertEqual([Slighe.read_text() for Slighe in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_cur_a_steach()['VMState'] = 'paused'
        self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.assertTrue(any(àithne[1] == 'controlvm' and àithne[3] == 'resume' for àithne in self.상자.명령들))
        self.assertFalse(any(àithne[0] == 'make' for àithne in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_cur_a_steach()['owner'] = 'someone-else'
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_cur_a_steach()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        inneal = self.Create_cur_a_steach()
        inneal['VMState'] = 'poweroff'
        inneal['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_cur_a_steach()['VMState'] = 'saving'
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_cur_a_steach()
        self.상자.가상기계들.clear()
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        inneal = self.Create_cur_a_steach()
        inneal['VMState'] = 'poweroff'
        이전 = dict(inneal)
        self.상자.fàilligeadh_VALUE = 'make'
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.assertEqual(inneal, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.fàilligeadh_VALUE = 'setextradata'
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()
        self.상자.명령들.clear()
        self.assertEqual(self.gnìomhaich_àithne.gnìomhaich_àithne()['state'], 'running')
        self.assertFalse(any(àithne[1] == 'createvm' for àithne in self.상자.명령들))

    def test_보존ISO변조거부(self):
        inneal = self.Create_cur_a_steach()
        inneal['VMState'] = 'poweroff'
        Path(inneal['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.gnìomhaich_àithne()

    def test_상태미생성(self):
        self.assertEqual(self.gnìomhaich_àithne.show_cor()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Slighe in ('../outside', '/tmp/outside'):
            with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.Slighe(Slighe)
        (self.freumh_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(mòideal_VALUE.실행오류): self.gnìomhaich_àithne.Slighe('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        tomhas = mòideal_VALUE.buadh_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(tomhas['VMState'], 'running')
        self.assertEqual(tomhas['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
