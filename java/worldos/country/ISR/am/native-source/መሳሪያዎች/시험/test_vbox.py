import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

ፍቺ_እሴት = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ሞጁል_እሴት = importlib.util.module_from_spec(ፍቺ_እሴት)
ፍቺ_እሴት.loader.exec_module(ሞጁል_እሴት)


class 가짜상자:
    def __init__(self, ስር_እሴት):
        self.ስር_እሴት = ስር_እሴት
        self.명령들 = []
        self.가상기계들 = {}
        self.ተስኖት_እሴት = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ተስኖት_እሴት == 인수[1] or (인수[0] == 'make' and self.ተስኖት_እሴት == 'make'):
            self.ተስኖት_እሴት = None
            raise ሞጁል_እሴት.실행오류('시험용 ተስኖት_እሴት')
        if 인수[0] == 'make':
            መተላለፊያ = self.ስር_እሴት / 'os/build/kernel.iso'
            መተላለፊያ.parent.mkdir(parents=True, exist_ok=True)
            መተላለፊያ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ተግባር = 인수[1]
        if ተግባር == 'list':
            return '\n'.join('"{}" {{{}}}'.format(እሴት['name'], መረጃ_ጠቆመ) for መረጃ_ጠቆመ, እሴት in self.가상기계들.items())
        if ተግባር == 'createvm':
            መረጃ_ጠቆመ, ስም = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[መረጃ_ጠቆመ] = {'UUID': መረጃ_ጠቆመ, 'name': ስም, 'VMState': 'poweroff',
                'CfgFile': str(self.ስር_እሴት / '.vbox/machines' / ስም / (ስም + '.vbox')), 'owner': None}
            return ''
        ማሽን = self.가상기계들[인수[2]]
        if ተግባር == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ስም), json.dumps(እሴት)) for ስም, እሴት in ማሽን.items() if ስም != 'owner')
        if ተግባር == 'getextradata': return 'Value: ' + ማሽን['owner'] if ማሽን['owner'] else 'No value set!'
        if ተግባር == 'setextradata': ማሽን['owner'] = 인수[4]
        elif ተግባር == 'storagectl': ማሽን['storagecontrollername0'] = 'JKOROS IDE'
        elif ተግባር == 'storageattach': ማሽን['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ተግባር == 'startvm': ማሽን['VMState'] = 'running'
        elif ተግባር == 'controlvm':
            assert 인수[3] == 'resume'
            ማሽን['VMState'] = 'running'
        elif ተግባር != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ስር_እሴት = Path(self.임시.name)
        (self.ስር_እሴት / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ስር_እሴት)
        self.ፈጽም_ትእዛዝ = ሞጁል_እሴት.ፕሮግራም_የመተግበሪያ_መሳቢያ(self.ስር_እሴት, 'jkoros operating system', ትእዛዝ=self.상자)

    def ፍጠር_ምዝግብ(self):
        ልኬት = self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ልኬት['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ትእዛዝ[0] == 'VBoxManage' and ትእዛዝ[1] in ('list', 'showvminfo', 'getextradata') for ትእዛዝ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ልኬት = self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.assertEqual(ልኬት['state'], 'running')
        self.assertTrue(Path(ልኬት['iso']).is_file())
        self.assertTrue(any('--nic1' in ትእዛዝ and 'none' in ትእዛዝ for ትእዛዝ in self.상자.명령들))
        self.assertFalse(any('hdd' in ትእዛዝ or 'discardstate' in ትእዛዝ or 'createmedium' in ትእዛዝ for ትእዛዝ in self.상자.명령들))

    def test_실행중유지(self):
        self.ፍጠር_ምዝግብ()
        self.assertEqual(self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ማሽን = self.ፍጠር_ምዝግብ()
        ማሽን['VMState'] = 'saved'
        መዝግብ_እሴት_e0918eb0 = self.ፈጽም_ትእዛዝ.መተላለፊያ(self.ፈጽም_ትእዛዝ.ማንበቢያ()['serial_log'])
        መዝግብ_እሴት_e0918eb0.write_text('saved log')
        self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.assertFalse(any(ትእዛዝ[0] == 'make' or ትእዛዝ[1] == 'modifyvm' for ትእዛዝ in self.상자.명령들))
        self.assertEqual([መተላለፊያ.read_text() for መተላለፊያ in መዝግብ_እሴት_e0918eb0.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ፍጠር_ምዝግብ()['VMState'] = 'paused'
        self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.assertTrue(any(ትእዛዝ[1] == 'controlvm' and ትእዛዝ[3] == 'resume' for ትእዛዝ in self.상자.명령들))
        self.assertFalse(any(ትእዛዝ[0] == 'make' for ትእዛዝ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ፍጠር_ምዝግብ()['owner'] = 'someone-else'
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ፍጠር_ምዝግብ()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ማሽን = self.ፍጠር_ምዝግብ()
        ማሽን['VMState'] = 'poweroff'
        ማሽን['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.변경없음()

    def test_전환중거부(self):
        self.ፍጠር_ምዝግብ()['VMState'] = 'saving'
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ፍጠር_ምዝግብ()
        self.상자.가상기계들.clear()
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ማሽን = self.ፍጠር_ምዝግብ()
        ማሽን['VMState'] = 'poweroff'
        이전 = dict(ማሽን)
        self.상자.ተስኖት_እሴት = 'make'
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.assertEqual(ማሽን, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ተስኖት_እሴት = 'setextradata'
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()
        self.상자.명령들.clear()
        self.assertEqual(self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()['state'], 'running')
        self.assertFalse(any(ትእዛዝ[1] == 'createvm' for ትእዛዝ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ማሽን = self.ፍጠር_ምዝግብ()
        ማሽን['VMState'] = 'poweroff'
        Path(ማሽን['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ()

    def test_상태미생성(self):
        self.assertEqual(self.ፈጽም_ትእዛዝ.አሳይ_ዞን()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for መተላለፊያ in ('../outside', '/tmp/outside'):
            with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.መተላለፊያ(መተላለፊያ)
        (self.ስር_እሴት / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ሞጁል_እሴት.실행오류): self.ፈጽም_ትእዛዝ.መተላለፊያ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ልኬት = ሞጁል_እሴት.ዓይነታ_እሴት('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ልኬት['VMState'], 'running')
        self.assertEqual(ልኬት['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
