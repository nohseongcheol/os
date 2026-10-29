import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definição_VALOR = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
módulo_VALOR = importlib.util.module_from_spec(Definição_VALOR)
Definição_VALOR.loader.exec_module(módulo_VALOR)


class 가짜상자:
    def __init__(self, raiz_VALOR):
        self.raiz_VALOR = raiz_VALOR
        self.명령들 = []
        self.Máquinas_Virtuais = {}
        self.falha_VALOR = None

    def __call__(self, argumentos):
        argumentos = list(map(str, argumentos))
        self.명령들.append(argumentos)
        if self.falha_VALOR == argumentos[1] or (argumentos[0] == 'make' and self.falha_VALOR == 'make'):
            self.falha_VALOR = None
            raise módulo_VALOR.execução_erro('시험용 falha_VALOR')
        if argumentos[0] == 'make':
            caminho = self.raiz_VALOR / 'os/build/kernel.iso'
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Acção = argumentos[1]
        if Acção == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALOR['name'], ÍNDICE) for ÍNDICE, VALOR in self.Máquinas_Virtuais.items())
        if Acção == 'createvm':
            ÍNDICE, Nome = argumentos[argumentos.index('--uuid') + 1], argumentos[argumentos.index('--name') + 1]
            self.Máquinas_Virtuais[ÍNDICE] = {'UUID': ÍNDICE, 'name': Nome, 'VMState': 'poweroff',
                'CfgFile': str(self.raiz_VALOR / '.vbox/machines' / Nome / (Nome + '.vbox')), 'owner': None}
            return ''
        computador = self.Máquinas_Virtuais[argumentos[2]]
        if Acção == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nome), json.dumps(VALOR)) for Nome, VALOR in computador.items() if Nome != 'owner')
        if Acção == 'getextradata': return 'Value: ' + computador['owner'] if computador['owner'] else 'No value set!'
        if Acção == 'setextradata': computador['owner'] = argumentos[4]
        elif Acção == 'storagectl': computador['storagecontrollername0'] = 'JKOROS IDE'
        elif Acção == 'storageattach': computador['JKOROS IDE-0-0'] = argumentos[argumentos.index('--medium') + 1]
        elif Acção == 'startvm': computador['VMState'] = 'running'
        elif Acção == 'controlvm':
            assert argumentos[3] == 'resume'
            computador['VMState'] = 'running'
        elif Acção != 'modifyvm': raise AssertionError(argumentos)
        return ''


class execução_de_teste(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.raiz_VALOR = Path(self.임시.name)
        (self.raiz_VALOR / '.vbox').mkdir()
        self.상자 = 가짜상자(self.raiz_VALOR)
        self.Executar_comando = módulo_VALOR.app_Launcher(self.raiz_VALOR, 'jkoros operating system', comando=self.상자)

    def Criar_entrada(self):
        resultado = self.Executar_comando.Executar_comando()
        self.상자.명령들.clear()
        return self.상자.Máquinas_Virtuais[resultado['uuid']]

    def 변경없음(self):
        self.assertTrue(all(comando[0] == 'VBoxManage' and comando[1] in ('list', 'showvminfo', 'getextradata') for comando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        resultado = self.Executar_comando.Executar_comando()
        self.assertEqual(resultado['state'], 'running')
        self.assertTrue(Path(resultado['iso']).is_file())
        self.assertTrue(any('--nic1' in comando and 'none' in comando for comando in self.상자.명령들))
        self.assertFalse(any('hdd' in comando or 'discardstate' in comando or 'createmedium' in comando for comando in self.상자.명령들))

    def test_실행중유지(self):
        self.Criar_entrada()
        self.assertEqual(self.Executar_comando.Executar_comando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        computador = self.Criar_entrada()
        computador['VMState'] = 'saved'
        LOG_VALOR = self.Executar_comando.caminho(self.Executar_comando.Leitura()['serial_log'])
        LOG_VALOR.write_text('saved log')
        self.Executar_comando.Executar_comando()
        self.assertFalse(any(comando[0] == 'make' or comando[1] == 'modifyvm' for comando in self.상자.명령들))
        self.assertEqual([caminho.read_text() for caminho in LOG_VALOR.parent.glob('before-resume-*.log')], ['saved log'])

    def teste_Pausar_E_CV(self):
        self.Criar_entrada()['VMState'] = 'paused'
        self.Executar_comando.Executar_comando()
        self.assertTrue(any(comando[1] == 'controlvm' and comando[3] == 'resume' for comando in self.상자.명령들))
        self.assertFalse(any(comando[0] == 'make' for comando in self.상자.명령들))

    def teste_Outros_VM_nome_colisão(self):
        self.상자.Máquinas_Virtuais[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.변경없음()

    def test_소유표식거부(self):
        self.Criar_entrada()['owner'] = 'someone-else'
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Criar_entrada()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        computador = self.Criar_entrada()
        computador['VMState'] = 'poweroff'
        computador['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.변경없음()

    def test_전환중거부(self):
        self.Criar_entrada()['VMState'] = 'saving'
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.변경없음()

    def test_등록해제거부(self):
        self.Criar_entrada()
        self.상자.Máquinas_Virtuais.clear()
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        computador = self.Criar_entrada()
        computador['VMState'] = 'poweroff'
        Anterior_item = dict(computador)
        self.상자.falha_VALOR = 'make'
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.assertEqual(computador, Anterior_item)

    def test_중단된소유표식설정복구(self):
        self.상자.falha_VALOR = 'setextradata'
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()
        self.상자.명령들.clear()
        self.assertEqual(self.Executar_comando.Executar_comando()['state'], 'running')
        self.assertFalse(any(comando[1] == 'createvm' for comando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        computador = self.Criar_entrada()
        computador['VMState'] = 'poweroff'
        Path(computador['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.Executar_comando()

    def test_상태미생성(self):
        self.assertEqual(self.Executar_comando.mostrar_Estado()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for caminho in ('../outside', '/tmp/outside'):
            with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.caminho(caminho)
        (self.raiz_VALOR / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(módulo_VALOR.execução_erro): self.Executar_comando.caminho('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        resultado = módulo_VALOR.valor_do_atributo('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(resultado['VMState'], 'running')
        self.assertEqual(resultado['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
