import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Sainmhíniú_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modúl_VALUE = importlib.util.module_from_spec(Sainmhíniú_VALUE)
Sainmhíniú_VALUE.loader.exec_module(modúl_VALUE)


class 가짜상자:
    def __init__(self, fréamh_VALUE):
        self.fréamh_VALUE = fréamh_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.teip_VALUE = None

    def __call__(self, Argóintí):
        Argóintí = list(map(str, Argóintí))
        self.명령들.append(Argóintí)
        if self.teip_VALUE == Argóintí[1] or (Argóintí[0] == 'make' and self.teip_VALUE == 'make'):
            self.teip_VALUE = None
            raise modúl_VALUE.실행오류('시험용 teip_VALUE')
        if Argóintí[0] == 'make':
            CONAIR = self.fréamh_VALUE / 'os/build/kernel.iso'
            CONAIR.parent.mkdir(parents=True, exist_ok=True)
            CONAIR.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Gníomh = Argóintí[1]
        if Gníomh == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Gníomh == 'createvm':
            INDEX, Ainm = Argóintí[Argóintí.index('--uuid') + 1], Argóintí[Argóintí.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Ainm, 'VMState': 'poweroff',
                'CfgFile': str(self.fréamh_VALUE / '.vbox/machines' / Ainm / (Ainm + '.vbox')), 'owner': None}
            return ''
        meaisín = self.가상기계들[Argóintí[2]]
        if Gníomh == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ainm), json.dumps(VALUE)) for Ainm, VALUE in meaisín.items() if Ainm != 'owner')
        if Gníomh == 'getextradata': return 'Value: ' + meaisín['owner'] if meaisín['owner'] else 'No value set!'
        if Gníomh == 'setextradata': meaisín['owner'] = Argóintí[4]
        elif Gníomh == 'storagectl': meaisín['storagecontrollername0'] = 'JKOROS IDE'
        elif Gníomh == 'storageattach': meaisín['JKOROS IDE-0-0'] = Argóintí[Argóintí.index('--medium') + 1]
        elif Gníomh == 'startvm': meaisín['VMState'] = 'running'
        elif Gníomh == 'controlvm':
            assert Argóintí[3] == 'resume'
            meaisín['VMState'] = 'running'
        elif Gníomh != 'modifyvm': raise AssertionError(Argóintí)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.fréamh_VALUE = Path(self.임시.name)
        (self.fréamh_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.fréamh_VALUE)
        self.Rith_ordú = modúl_VALUE.clár_tarraiceán_feidhmchlár(self.fréamh_VALUE, 'jkoros operating system', Ordú=self.상자)

    def Create_iontráil(self):
        tomhas = self.Rith_ordú.Rith_ordú()
        self.상자.명령들.clear()
        return self.상자.가상기계들[tomhas['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Ordú[0] == 'VBoxManage' and Ordú[1] in ('list', 'showvminfo', 'getextradata') for Ordú in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        tomhas = self.Rith_ordú.Rith_ordú()
        self.assertEqual(tomhas['state'], 'running')
        self.assertTrue(Path(tomhas['iso']).is_file())
        self.assertTrue(any('--nic1' in Ordú and 'none' in Ordú for Ordú in self.상자.명령들))
        self.assertFalse(any('hdd' in Ordú or 'discardstate' in Ordú or 'createmedium' in Ordú for Ordú in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_iontráil()
        self.assertEqual(self.Rith_ordú.Rith_ordú()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        meaisín = self.Create_iontráil()
        meaisín['VMState'] = 'saved'
        LOG_VALUE = self.Rith_ordú.CONAIR(self.Rith_ordú.Léigh()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Rith_ordú.Rith_ordú()
        self.assertFalse(any(Ordú[0] == 'make' or Ordú[1] == 'modifyvm' for Ordú in self.상자.명령들))
        self.assertEqual([CONAIR.read_text() for CONAIR in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_iontráil()['VMState'] = 'paused'
        self.Rith_ordú.Rith_ordú()
        self.assertTrue(any(Ordú[1] == 'controlvm' and Ordú[3] == 'resume' for Ordú in self.상자.명령들))
        self.assertFalse(any(Ordú[0] == 'make' for Ordú in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_iontráil()['owner'] = 'someone-else'
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_iontráil()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        meaisín = self.Create_iontráil()
        meaisín['VMState'] = 'poweroff'
        meaisín['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_iontráil()['VMState'] = 'saving'
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_iontráil()
        self.상자.가상기계들.clear()
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        meaisín = self.Create_iontráil()
        meaisín['VMState'] = 'poweroff'
        이전 = dict(meaisín)
        self.상자.teip_VALUE = 'make'
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.assertEqual(meaisín, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.teip_VALUE = 'setextradata'
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()
        self.상자.명령들.clear()
        self.assertEqual(self.Rith_ordú.Rith_ordú()['state'], 'running')
        self.assertFalse(any(Ordú[1] == 'createvm' for Ordú in self.상자.명령들))

    def test_보존ISO변조거부(self):
        meaisín = self.Create_iontráil()
        meaisín['VMState'] = 'poweroff'
        Path(meaisín['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.Rith_ordú()

    def test_상태미생성(self):
        self.assertEqual(self.Rith_ordú.seó_staid()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for CONAIR in ('../outside', '/tmp/outside'):
            with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.CONAIR(CONAIR)
        (self.fréamh_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modúl_VALUE.실행오류): self.Rith_ordú.CONAIR('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        tomhas = modúl_VALUE.tréith_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(tomhas['VMState'], 'running')
        self.assertEqual(tomhas['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
