import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

정의 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(정의)
정의.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ == 인수[1] or (인수[0] == 'make' and self.ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ == 'make'):
            self.ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ = None
            raise 모듈.실행오류('시험용 ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ')
        if 인수[0] == 'make':
            ᎠᏍᏓᏩᏛᏍᏗ = self.뿌리 / 'os/build/kernel.iso'
            ᎠᏍᏓᏩᏛᏍᏗ.parent.mkdir(parents=True, exist_ok=True)
            ᎠᏍᏓᏩᏛᏍᏗ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ᎠᏛᏁᎵᏓ = 인수[1]
        if ᎠᏛᏁᎵᏓ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ᏧᎬᏩᎶᏗᏯ['name'], ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) for ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᏧᎬᏩᎶᏗᏯ in self.가상기계들.items())
        if ᎠᏛᏁᎵᏓ == 'createvm':
            ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᏚᏙᎥᎢ = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = {'UUID': ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, 'name': ᏚᏙᎥᎢ, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / ᏚᏙᎥᎢ / (ᏚᏙᎥᎢ + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[인수[2]]
        if ᎠᏛᏁᎵᏓ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ᏚᏙᎥᎢ), json.dumps(ᏧᎬᏩᎶᏗᏯ)) for ᏚᏙᎥᎢ, ᏧᎬᏩᎶᏗᏯ in 기계.items() if ᏚᏙᎥᎢ != 'owner')
        if ᎠᏛᏁᎵᏓ == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if ᎠᏛᏁᎵᏓ == 'setextradata': 기계['owner'] = 인수[4]
        elif ᎠᏛᏁᎵᏓ == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif ᎠᏛᏁᎵᏓ == 'storageattach': 기계['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ᎠᏛᏁᎵᏓ == 'startvm': 기계['VMState'] = 'running'
        elif ᎠᏛᏁᎵᏓ == 'controlvm':
            assert 인수[3] == 'resume'
            기계['VMState'] = 'running'
        elif ᎠᏛᏁᎵᏓ != 'modifyvm': raise AssertionError(인수)
        return ''


class ᎠᏓᎪᎵᏰᏍᎩ_ᎠᎢᏎᏍᏗ(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ = 모듈.실행기(self.뿌리, 'jkoros operating system', ᎤᏁᏤᎸᎩ=self.상자)

    def 만들기(self):
        결과 = self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ᎤᏁᏤᎸᎩ[0] == 'VBoxManage' and ᎤᏁᏤᎸᎩ[1] in ('list', 'showvminfo', 'getextradata') for ᎤᏁᏤᎸᎩ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in ᎤᏁᏤᎸᎩ and 'none' in ᎤᏁᏤᎸᎩ for ᎤᏁᏤᎸᎩ in self.상자.명령들))
        self.assertFalse(any('hdd' in ᎤᏁᏤᎸᎩ or 'discardstate' in ᎤᏁᏤᎸᎩ or 'createmedium' in ᎤᏁᏤᎸᎩ for ᎤᏁᏤᎸᎩ in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᏧᎬᏩᎶᏗᏯ = self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᏍᏓᏩᏛᏍᏗ(self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.읽기()['serial_log'])
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᏧᎬᏩᎶᏗᏯ.write_text('saved log')
        self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.assertFalse(any(ᎤᏁᏤᎸᎩ[0] == 'make' or ᎤᏁᏤᎸᎩ[1] == 'modifyvm' for ᎤᏁᏤᎸᎩ in self.상자.명령들))
        self.assertEqual([ᎠᏍᏓᏩᏛᏍᏗ.read_text() for ᎠᏍᏓᏩᏛᏍᏗ in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᏧᎬᏩᎶᏗᏯ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.assertTrue(any(ᎤᏁᏤᎸᎩ[1] == 'controlvm' and ᎤᏁᏤᎸᎩ[3] == 'resume' for ᎤᏁᏤᎸᎩ in self.상자.명령들))
        self.assertFalse(any(ᎤᏁᏤᎸᎩ[0] == 'make' for ᎤᏁᏤᎸᎩ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.변경없음()

    def test_소유표식거부(self):
        self.만들기()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.만들기()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        기계['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.변경없음()

    def test_전환중거부(self):
        self.만들기()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.변경없음()

    def test_등록해제거부(self):
        self.만들기()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        이전 = dict(기계)
        self.상자.ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ = 'make'
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.assertEqual(기계, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
        self.상자.명령들.clear()
        self.assertEqual(self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()['state'], 'running')
        self.assertFalse(any(ᎤᏁᏤᎸᎩ[1] == 'createvm' for ᎤᏁᏤᎸᎩ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()

    def test_상태미생성(self):
        self.assertEqual(self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᏍᎩᎪᏩᏛᏓ_ᏄᏍᏗᏓᏅ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ᎠᏍᏓᏩᏛᏍᏗ in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᏍᏓᏩᏛᏍᏗ(ᎠᏍᏓᏩᏛᏍᏗ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᏍᏓᏩᏛᏍᏗ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
