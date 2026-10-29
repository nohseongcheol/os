import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

నిర్వచనం_మూల్యం = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
మాడ్యూల్_మూల్యం = importlib.util.module_from_spec(నిర్వచనం_మూల్యం)
నిర్వచనం_మూల్యం.loader.exec_module(మాడ్యూల్_మూల్యం)


class 가짜상자:
    def __init__(self, మూలం_మూల్యం):
        self.మూలం_మూల్యం = మూలం_మూల్యం
        self.명령들 = []
        self.가상기계들 = {}
        self.వైఫల్యం_మూల్యం = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.వైఫల్యం_మూల్యం == 인수[1] or (인수[0] == 'make' and self.వైఫల్యం_మూల్యం == 'make'):
            self.వైఫల్యం_మూల్యం = None
            raise మాడ్యూల్_మూల్యం.실행오류('시험용 వైఫల్యం_మూల్యం')
        if 인수[0] == 'make':
            పాత్ = self.మూలం_మూల్యం / 'os/build/kernel.iso'
            పాత్.parent.mkdir(parents=True, exist_ok=True)
            పాత్.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        చర్య = 인수[1]
        if చర్య == 'list':
            return '\n'.join('"{}" {{{}}}'.format(మూల్యం['name'], సూచీ) for సూచీ, మూల్యం in self.가상기계들.items())
        if చర్య == 'createvm':
            సూచీ, పేరు = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[సూచీ] = {'UUID': సూచీ, 'name': పేరు, 'VMState': 'poweroff',
                'CfgFile': str(self.మూలం_మూల్యం / '.vbox/machines' / పేరు / (పేరు + '.vbox')), 'owner': None}
            return ''
        యంత్రం = self.가상기계들[인수[2]]
        if చర్య == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(పేరు), json.dumps(మూల్యం)) for పేరు, మూల్యం in యంత్రం.items() if పేరు != 'owner')
        if చర్య == 'getextradata': return 'Value: ' + యంత్రం['owner'] if యంత్రం['owner'] else 'No value set!'
        if చర్య == 'setextradata': యంత్రం['owner'] = 인수[4]
        elif చర్య == 'storagectl': యంత్రం['storagecontrollername0'] = 'JKOROS IDE'
        elif చర్య == 'storageattach': యంత్రం['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif చర్య == 'startvm': యంత్రం['VMState'] = 'running'
        elif చర్య == 'controlvm':
            assert 인수[3] == 'resume'
            యంత్రం['VMState'] = 'running'
        elif చర్య != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.మూలం_మూల్యం = Path(self.임시.name)
        (self.మూలం_మూల్యం / '.vbox').mkdir()
        self.상자 = 가짜상자(self.మూలం_మూల్యం)
        self.అమలు_చేయి_ఆదేశం = మాడ్యూల్_మూల్యం.అనువర్తనం_లాంచర్(self.మూలం_మూల్యం, 'jkoros operating system', ఆదేశము=self.상자)

    def క్రియేట్_ప్రవేశం(self):
        ప్రమాణం = self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ప్రమాణం['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ఆదేశము[0] == 'VBoxManage' and ఆదేశము[1] in ('list', 'showvminfo', 'getextradata') for ఆదేశము in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ప్రమాణం = self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.assertEqual(ప్రమాణం['state'], 'running')
        self.assertTrue(Path(ప్రమాణం['iso']).is_file())
        self.assertTrue(any('--nic1' in ఆదేశము and 'none' in ఆదేశము for ఆదేశము in self.상자.명령들))
        self.assertFalse(any('hdd' in ఆదేశము or 'discardstate' in ఆదేశము or 'createmedium' in ఆదేశము for ఆదేశము in self.상자.명령들))

    def test_실행중유지(self):
        self.క్రియేట్_ప్రవేశం()
        self.assertEqual(self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        యంత్రం = self.క్రియేట్_ప్రవేశం()
        యంత్రం['VMState'] = 'saved'
        లాగ్_మూల్యం = self.అమలు_చేయి_ఆదేశం.పాత్(self.అమలు_చేయి_ఆదేశం.చదువు()['serial_log'])
        లాగ్_మూల్యం.write_text('saved log')
        self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.assertFalse(any(ఆదేశము[0] == 'make' or ఆదేశము[1] == 'modifyvm' for ఆదేశము in self.상자.명령들))
        self.assertEqual([పాత్.read_text() for పాత్ in లాగ్_మూల్యం.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.క్రియేట్_ప్రవేశం()['VMState'] = 'paused'
        self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.assertTrue(any(ఆదేశము[1] == 'controlvm' and ఆదేశము[3] == 'resume' for ఆదేశము in self.상자.명령들))
        self.assertFalse(any(ఆదేశము[0] == 'make' for ఆదేశము in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.변경없음()

    def test_소유표식거부(self):
        self.క్రియేట్_ప్రవేశం()['owner'] = 'someone-else'
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.క్రియేట్_ప్రవేశం()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        యంత్రం = self.క్రియేట్_ప్రవేశం()
        యంత్రం['VMState'] = 'poweroff'
        యంత్రం['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.변경없음()

    def test_전환중거부(self):
        self.క్రియేట్_ప్రవేశం()['VMState'] = 'saving'
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.변경없음()

    def test_등록해제거부(self):
        self.క్రియేట్_ప్రవేశం()
        self.상자.가상기계들.clear()
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        యంత్రం = self.క్రియేట్_ప్రవేశం()
        యంత్రం['VMState'] = 'poweroff'
        이전 = dict(యంత్రం)
        self.상자.వైఫల్యం_మూల్యం = 'make'
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.assertEqual(యంత్రం, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.వైఫల్యం_మూల్యం = 'setextradata'
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()
        self.상자.명령들.clear()
        self.assertEqual(self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()['state'], 'running')
        self.assertFalse(any(ఆదేశము[1] == 'createvm' for ఆదేశము in self.상자.명령들))

    def test_보존ISO변조거부(self):
        యంత్రం = self.క్రియేట్_ప్రవేశం()
        యంత్రం['VMState'] = 'poweroff'
        Path(యంత్రం['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం()

    def test_상태미생성(self):
        self.assertEqual(self.అమలు_చేయి_ఆదేశం.చూపించు_స్థితి()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for పాత్ in ('../outside', '/tmp/outside'):
            with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.పాత్(పాత్)
        (self.మూలం_మూల్యం / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(మాడ్యూల్_మూల్యం.실행오류): self.అమలు_చేయి_ఆదేశం.పాత్('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ప్రమాణం = మాడ్యూల్_మూల్యం.లక్షణం_మూల్యం('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ప్రమాణం['VMState'], 'running')
        self.assertEqual(ప్రమాణం['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
