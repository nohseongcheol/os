import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definición_VALOR = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
módulo_VALOR = importlib.util.module_from_spec(Definición_VALOR)
Definición_VALOR.loader.exec_module(módulo_VALOR)


class 가짜상자:
    def __init__(self, raíz_VALOR):
        self.raíz_VALOR = raíz_VALOR
        self.명령들 = []
        self.가상기계들 = {}
        self.erro_VALOR = None

    def __call__(self, Argumentos):
        Argumentos = list(map(str, Argumentos))
        self.명령들.append(Argumentos)
        if self.erro_VALOR == Argumentos[1] or (Argumentos[0] == 'make' and self.erro_VALOR == 'make'):
            self.erro_VALOR = None
            raise módulo_VALOR.실행오류('시험용 erro_VALOR')
        if Argumentos[0] == 'make':
            CAMIÑO = self.raíz_VALOR / 'os/build/kernel.iso'
            CAMIÑO.parent.mkdir(parents=True, exist_ok=True)
            CAMIÑO.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Acción = Argumentos[1]
        if Acción == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALOR['name'], ÍNDICE) for ÍNDICE, VALOR in self.가상기계들.items())
        if Acción == 'createvm':
            ÍNDICE, Nome = Argumentos[Argumentos.index('--uuid') + 1], Argumentos[Argumentos.index('--name') + 1]
            self.가상기계들[ÍNDICE] = {'UUID': ÍNDICE, 'name': Nome, 'VMState': 'poweroff',
                'CfgFile': str(self.raíz_VALOR / '.vbox/machines' / Nome / (Nome + '.vbox')), 'owner': None}
            return ''
        máquina = self.가상기계들[Argumentos[2]]
        if Acción == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nome), json.dumps(VALOR)) for Nome, VALOR in máquina.items() if Nome != 'owner')
        if Acción == 'getextradata': return 'Value: ' + máquina['owner'] if máquina['owner'] else 'No value set!'
        if Acción == 'setextradata': máquina['owner'] = Argumentos[4]
        elif Acción == 'storagectl': máquina['storagecontrollername0'] = 'JKOROS IDE'
        elif Acción == 'storageattach': máquina['JKOROS IDE-0-0'] = Argumentos[Argumentos.index('--medium') + 1]
        elif Acción == 'startvm': máquina['VMState'] = 'running'
        elif Acción == 'controlvm':
            assert Argumentos[3] == 'resume'
            máquina['VMState'] = 'running'
        elif Acción != 'modifyvm': raise AssertionError(Argumentos)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.raíz_VALOR = Path(self.임시.name)
        (self.raíz_VALOR / '.vbox').mkdir()
        self.상자 = 가짜상자(self.raíz_VALOR)
        self.executar_comando = módulo_VALOR.apl_iniciador(self.raíz_VALOR, 'jkoros operating system', Orde=self.상자)

    def crear_introdución(self):
        RESULTANTE = self.executar_comando.executar_comando()
        self.상자.명령들.clear()
        return self.상자.가상기계들[RESULTANTE['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Orde[0] == 'VBoxManage' and Orde[1] in ('list', 'showvminfo', 'getextradata') for Orde in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        RESULTANTE = self.executar_comando.executar_comando()
        self.assertEqual(RESULTANTE['state'], 'running')
        self.assertTrue(Path(RESULTANTE['iso']).is_file())
        self.assertTrue(any('--nic1' in Orde and 'none' in Orde for Orde in self.상자.명령들))
        self.assertFalse(any('hdd' in Orde or 'discardstate' in Orde or 'createmedium' in Orde for Orde in self.상자.명령들))

    def test_실행중유지(self):
        self.crear_introdución()
        self.assertEqual(self.executar_comando.executar_comando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        máquina = self.crear_introdución()
        máquina['VMState'] = 'saved'
        LOG_VALOR = self.executar_comando.CAMIÑO(self.executar_comando.Lectura()['serial_log'])
        LOG_VALOR.write_text('saved log')
        self.executar_comando.executar_comando()
        self.assertFalse(any(Orde[0] == 'make' or Orde[1] == 'modifyvm' for Orde in self.상자.명령들))
        self.assertEqual([CAMIÑO.read_text() for CAMIÑO in LOG_VALOR.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.crear_introdución()['VMState'] = 'paused'
        self.executar_comando.executar_comando()
        self.assertTrue(any(Orde[1] == 'controlvm' and Orde[3] == 'resume' for Orde in self.상자.명령들))
        self.assertFalse(any(Orde[0] == 'make' for Orde in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.변경없음()

    def test_소유표식거부(self):
        self.crear_introdución()['owner'] = 'someone-else'
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.crear_introdución()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        máquina = self.crear_introdución()
        máquina['VMState'] = 'poweroff'
        máquina['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.변경없음()

    def test_전환중거부(self):
        self.crear_introdución()['VMState'] = 'saving'
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.변경없음()

    def test_등록해제거부(self):
        self.crear_introdución()
        self.상자.가상기계들.clear()
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        máquina = self.crear_introdución()
        máquina['VMState'] = 'poweroff'
        이전 = dict(máquina)
        self.상자.erro_VALOR = 'make'
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.assertEqual(máquina, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.erro_VALOR = 'setextradata'
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()
        self.상자.명령들.clear()
        self.assertEqual(self.executar_comando.executar_comando()['state'], 'running')
        self.assertFalse(any(Orde[1] == 'createvm' for Orde in self.상자.명령들))

    def test_보존ISO변조거부(self):
        máquina = self.crear_introdución()
        máquina['VMState'] = 'poweroff'
        Path(máquina['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.executar_comando()

    def test_상태미생성(self):
        self.assertEqual(self.executar_comando.mostrar_Estado()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for CAMIÑO in ('../outside', '/tmp/outside'):
            with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.CAMIÑO(CAMIÑO)
        (self.raíz_VALOR / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(módulo_VALOR.실행오류): self.executar_comando.CAMIÑO('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        RESULTANTE = módulo_VALOR.atributo_VALOR('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(RESULTANTE['VMState'], 'running')
        self.assertEqual(RESULTANTE['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
