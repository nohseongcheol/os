import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Diffiniad_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modiwl_VALUE = importlib.util.module_from_spec(Diffiniad_VALUE)
Diffiniad_VALUE.loader.exec_module(modiwl_VALUE)


class 가짜상자:
    def __init__(self, gwraidd_VALUE):
        self.gwraidd_VALUE = gwraidd_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.methiant_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.methiant_VALUE == 인수[1] or (인수[0] == 'make' and self.methiant_VALUE == 'make'):
            self.methiant_VALUE = None
            raise modiwl_VALUE.실행오류('시험용 methiant_VALUE')
        if 인수[0] == 'make':
            LLWYBR = self.gwraidd_VALUE / 'os/build/kernel.iso'
            LLWYBR.parent.mkdir(parents=True, exist_ok=True)
            LLWYBR.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Gweithrediad = 인수[1]
        if Gweithrediad == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Gweithrediad == 'createvm':
            INDEX, Enw = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Enw, 'VMState': 'poweroff',
                'CfgFile': str(self.gwraidd_VALUE / '.vbox/machines' / Enw / (Enw + '.vbox')), 'owner': None}
            return ''
        peiriant = self.가상기계들[인수[2]]
        if Gweithrediad == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Enw), json.dumps(VALUE)) for Enw, VALUE in peiriant.items() if Enw != 'owner')
        if Gweithrediad == 'getextradata': return 'Value: ' + peiriant['owner'] if peiriant['owner'] else 'No value set!'
        if Gweithrediad == 'setextradata': peiriant['owner'] = 인수[4]
        elif Gweithrediad == 'storagectl': peiriant['storagecontrollername0'] = 'JKOROS IDE'
        elif Gweithrediad == 'storageattach': peiriant['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Gweithrediad == 'startvm': peiriant['VMState'] = 'running'
        elif Gweithrediad == 'controlvm':
            assert 인수[3] == 'resume'
            peiriant['VMState'] = 'running'
        elif Gweithrediad != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.gwraidd_VALUE = Path(self.임시.name)
        (self.gwraidd_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.gwraidd_VALUE)
        self.Gweithredu_gorchymyn = modiwl_VALUE.Rhaglen_lansiwr(self.gwraidd_VALUE, 'jkoros operating system', Gorchymyn=self.상자)

    def Creu_cofnod(self):
        mesur = self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.상자.명령들.clear()
        return self.상자.가상기계들[mesur['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Gorchymyn[0] == 'VBoxManage' and Gorchymyn[1] in ('list', 'showvminfo', 'getextradata') for Gorchymyn in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        mesur = self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.assertEqual(mesur['state'], 'running')
        self.assertTrue(Path(mesur['iso']).is_file())
        self.assertTrue(any('--nic1' in Gorchymyn and 'none' in Gorchymyn for Gorchymyn in self.상자.명령들))
        self.assertFalse(any('hdd' in Gorchymyn or 'discardstate' in Gorchymyn or 'createmedium' in Gorchymyn for Gorchymyn in self.상자.명령들))

    def test_실행중유지(self):
        self.Creu_cofnod()
        self.assertEqual(self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        peiriant = self.Creu_cofnod()
        peiriant['VMState'] = 'saved'
        LOG_VALUE = self.Gweithredu_gorchymyn.LLWYBR(self.Gweithredu_gorchymyn.Darllen()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.assertFalse(any(Gorchymyn[0] == 'make' or Gorchymyn[1] == 'modifyvm' for Gorchymyn in self.상자.명령들))
        self.assertEqual([LLWYBR.read_text() for LLWYBR in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Creu_cofnod()['VMState'] = 'paused'
        self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.assertTrue(any(Gorchymyn[1] == 'controlvm' and Gorchymyn[3] == 'resume' for Gorchymyn in self.상자.명령들))
        self.assertFalse(any(Gorchymyn[0] == 'make' for Gorchymyn in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.변경없음()

    def test_소유표식거부(self):
        self.Creu_cofnod()['owner'] = 'someone-else'
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Creu_cofnod()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        peiriant = self.Creu_cofnod()
        peiriant['VMState'] = 'poweroff'
        peiriant['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.변경없음()

    def test_전환중거부(self):
        self.Creu_cofnod()['VMState'] = 'saving'
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.변경없음()

    def test_등록해제거부(self):
        self.Creu_cofnod()
        self.상자.가상기계들.clear()
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        peiriant = self.Creu_cofnod()
        peiriant['VMState'] = 'poweroff'
        이전 = dict(peiriant)
        self.상자.methiant_VALUE = 'make'
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.assertEqual(peiriant, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.methiant_VALUE = 'setextradata'
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()
        self.상자.명령들.clear()
        self.assertEqual(self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()['state'], 'running')
        self.assertFalse(any(Gorchymyn[1] == 'createvm' for Gorchymyn in self.상자.명령들))

    def test_보존ISO변조거부(self):
        peiriant = self.Creu_cofnod()
        peiriant['VMState'] = 'poweroff'
        Path(peiriant['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.Gweithredu_gorchymyn()

    def test_상태미생성(self):
        self.assertEqual(self.Gweithredu_gorchymyn.sioe_cyflwr()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for LLWYBR in ('../outside', '/tmp/outside'):
            with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.LLWYBR(LLWYBR)
        (self.gwraidd_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modiwl_VALUE.실행오류): self.Gweithredu_gorchymyn.LLWYBR('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        mesur = modiwl_VALUE.priodoledd_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(mesur['VMState'], 'running')
        self.assertEqual(mesur['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
