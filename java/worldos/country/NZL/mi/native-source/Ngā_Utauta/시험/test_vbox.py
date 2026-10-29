import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Whakamāramatanga_uara = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
kōwae_uara = importlib.util.module_from_spec(Whakamāramatanga_uara)
Whakamāramatanga_uara.loader.exec_module(kōwae_uara)


class 가짜상자:
    def __init__(self, pūtake_uara):
        self.pūtake_uara = pūtake_uara
        self.명령들 = []
        self.가상기계들 = {}
        self.rahunga_uara = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.rahunga_uara == 인수[1] or (인수[0] == 'make' and self.rahunga_uara == 'make'):
            self.rahunga_uara = None
            raise kōwae_uara.실행오류('시험용 rahunga_uara')
        if 인수[0] == 'make':
            ara = self.pūtake_uara / 'os/build/kernel.iso'
            ara.parent.mkdir(parents=True, exist_ok=True)
            ara.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        hohenga = 인수[1]
        if hohenga == 'list':
            return '\n'.join('"{}" {{{}}}'.format(uara['name'], INDEX) for INDEX, uara in self.가상기계들.items())
        if hohenga == 'createvm':
            INDEX, Ingoa = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Ingoa, 'VMState': 'poweroff',
                'CfgFile': str(self.pūtake_uara / '.vbox/machines' / Ingoa / (Ingoa + '.vbox')), 'owner': None}
            return ''
        mīhini = self.가상기계들[인수[2]]
        if hohenga == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ingoa), json.dumps(uara)) for Ingoa, uara in mīhini.items() if Ingoa != 'owner')
        if hohenga == 'getextradata': return 'Value: ' + mīhini['owner'] if mīhini['owner'] else 'No value set!'
        if hohenga == 'setextradata': mīhini['owner'] = 인수[4]
        elif hohenga == 'storagectl': mīhini['storagecontrollername0'] = 'JKOROS IDE'
        elif hohenga == 'storageattach': mīhini['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif hohenga == 'startvm': mīhini['VMState'] = 'running'
        elif hohenga == 'controlvm':
            assert 인수[3] == 'resume'
            mīhini['VMState'] = 'running'
        elif hohenga != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.pūtake_uara = Path(self.임시.name)
        (self.pūtake_uara / '.vbox').mkdir()
        self.상자 = 가짜상자(self.pūtake_uara)
        self.kawe_tono = kōwae_uara.kaupapa_pūwhiri_taupānga(self.pūtake_uara, 'jkoros operating system', tono=self.상자)

    def Waihanga_tāurunga(self):
        mēhua = self.kawe_tono.kawe_tono()
        self.상자.명령들.clear()
        return self.상자.가상기계들[mēhua['uuid']]

    def 변경없음(self):
        self.assertTrue(all(tono[0] == 'VBoxManage' and tono[1] in ('list', 'showvminfo', 'getextradata') for tono in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        mēhua = self.kawe_tono.kawe_tono()
        self.assertEqual(mēhua['state'], 'running')
        self.assertTrue(Path(mēhua['iso']).is_file())
        self.assertTrue(any('--nic1' in tono and 'none' in tono for tono in self.상자.명령들))
        self.assertFalse(any('hdd' in tono or 'discardstate' in tono or 'createmedium' in tono for tono in self.상자.명령들))

    def test_실행중유지(self):
        self.Waihanga_tāurunga()
        self.assertEqual(self.kawe_tono.kawe_tono()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mīhini = self.Waihanga_tāurunga()
        mīhini['VMState'] = 'saved'
        LOG_uara = self.kawe_tono.ara(self.kawe_tono.Pānuitia()['serial_log'])
        LOG_uara.write_text('saved log')
        self.kawe_tono.kawe_tono()
        self.assertFalse(any(tono[0] == 'make' or tono[1] == 'modifyvm' for tono in self.상자.명령들))
        self.assertEqual([ara.read_text() for ara in LOG_uara.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Waihanga_tāurunga()['VMState'] = 'paused'
        self.kawe_tono.kawe_tono()
        self.assertTrue(any(tono[1] == 'controlvm' and tono[3] == 'resume' for tono in self.상자.명령들))
        self.assertFalse(any(tono[0] == 'make' for tono in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.변경없음()

    def test_소유표식거부(self):
        self.Waihanga_tāurunga()['owner'] = 'someone-else'
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Waihanga_tāurunga()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mīhini = self.Waihanga_tāurunga()
        mīhini['VMState'] = 'poweroff'
        mīhini['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.변경없음()

    def test_전환중거부(self):
        self.Waihanga_tāurunga()['VMState'] = 'saving'
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.변경없음()

    def test_등록해제거부(self):
        self.Waihanga_tāurunga()
        self.상자.가상기계들.clear()
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mīhini = self.Waihanga_tāurunga()
        mīhini['VMState'] = 'poweroff'
        이전 = dict(mīhini)
        self.상자.rahunga_uara = 'make'
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.assertEqual(mīhini, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.rahunga_uara = 'setextradata'
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()
        self.상자.명령들.clear()
        self.assertEqual(self.kawe_tono.kawe_tono()['state'], 'running')
        self.assertFalse(any(tono[1] == 'createvm' for tono in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mīhini = self.Waihanga_tāurunga()
        mīhini['VMState'] = 'poweroff'
        Path(mīhini['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.kawe_tono()

    def test_상태미생성(self):
        self.assertEqual(self.kawe_tono.whakaatu_tūnga()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ara in ('../outside', '/tmp/outside'):
            with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.ara(ara)
        (self.pūtake_uara / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(kōwae_uara.실행오류): self.kawe_tono.ara('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        mēhua = kōwae_uara.huanga_uara('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(mēhua['VMState'], 'running')
        self.assertEqual(mēhua['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
