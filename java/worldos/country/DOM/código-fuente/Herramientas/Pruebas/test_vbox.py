import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

valorDefinición = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
valorMódulo = importlib.util.module_from_spec(valorDefinición)
valorDefinición.loader.exec_module(valorMódulo)


class CajaSimulado:
    def __init__(self, valorRaíz):
        self.valorRaíz = valorRaíz
        self.listaComandos = []
        self.máquinasVirtual = {}
        self.valorFallo = None

    def __call__(self, argumentos):
        argumentos = list(map(str, argumentos))
        self.listaComandos.append(argumentos)
        if self.valorFallo == argumentos[1] or (argumentos[0] == 'make' and self.valorFallo == 'make'):
            self.valorFallo = None
            raise valorMódulo.errorEjecución('시험용 valorFallo')
        if argumentos[0] == 'make':
            ruta = self.valorRaíz / 'os/build/kernel.iso'
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        acción = argumentos[1]
        if acción == 'list':
            return '\n'.join('"{}" {{{}}}'.format(valor['name'], número) for número, valor in self.máquinasVirtual.items())
        if acción == 'createvm':
            número, nombre = argumentos[argumentos.index('--uuid') + 1], argumentos[argumentos.index('--name') + 1]
            self.máquinasVirtual[número] = {'UUID': número, 'name': nombre, 'VMState': 'poweroff',
                'CfgFile': str(self.valorRaíz / '.vbox/machines' / nombre / (nombre + '.vbox')), 'owner': None}
            return ''
        máquina = self.máquinasVirtual[argumentos[2]]
        if acción == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(nombre), json.dumps(valor)) for nombre, valor in máquina.items() if nombre != 'owner')
        if acción == 'getextradata': return 'Value: ' + máquina['owner'] if máquina['owner'] else 'No value set!'
        if acción == 'setextradata': máquina['owner'] = argumentos[4]
        elif acción == 'storagectl': máquina['storagecontrollername0'] = 'JKOROS IDE'
        elif acción == 'storageattach': máquina['JKOROS IDE-0-0'] = argumentos[argumentos.index('--medium') + 1]
        elif acción == 'startvm': máquina['VMState'] = 'running'
        elif acción == 'controlvm':
            assert argumentos[3] == 'resume'
            máquina['VMState'] = 'running'
        elif acción != 'modifyvm': raise AssertionError(argumentos)
        return ''


class pruebaPonerEnMarcha(unittest.TestCase):
    def setUp(self):
        self.valorTemporal = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.valorTemporal.cleanup)
        self.valorRaíz = Path(self.valorTemporal.name)
        (self.valorRaíz / '.vbox').mkdir()
        self.valorCaja = CajaSimulado(self.valorRaíz)
        self.ejecutarComando = valorMódulo.LanzadorPrograma(self.valorRaíz, 'jkoros operating system', comando=self.valorCaja)

    def crearEntradaElemento(self):
        resultado = self.ejecutarComando.ejecutarComando()
        self.valorCaja.listaComandos.clear()
        return self.valorCaja.máquinasVirtual[resultado['uuid']]

    def esSinCambiar(self):
        self.assertTrue(all(comando[0] == 'VBoxManage' and comando[1] in ('list', 'showvminfo', 'getextradata') for comando in self.valorCaja.listaComandos))

    def pruebaArranqueÓpticoYCreaciónInicialValor(self):
        resultado = self.ejecutarComando.ejecutarComando()
        self.assertEqual(resultado['state'], 'running')
        self.assertTrue(Path(resultado['iso']).is_file())
        self.assertTrue(any('--nic1' in comando and 'none' in comando for comando in self.valorCaja.listaComandos))
        self.assertFalse(any('hdd' in comando or 'discardstate' in comando or 'createmedium' in comando for comando in self.valorCaja.listaComandos))

    def pruebaPreservadoMáquinaVirtualEnEjecución(self):
        self.crearEntradaElemento()
        self.assertEqual(self.ejecutarComando.ejecutarComando()['state'], 'running')
        self.esSinCambiar()

    def pruebaPreservaciónDiarioYReanudarEstadoValorGuardado(self):
        máquina = self.crearEntradaElemento()
        máquina['VMState'] = 'saved'
        valorDiario = self.ejecutarComando.ruta(self.ejecutarComando.leer()['serial_log'])
        valorDiario.write_text('saved log')
        self.ejecutarComando.ejecutarComando()
        self.assertFalse(any(comando[0] == 'make' or comando[1] == 'modifyvm' for comando in self.valorCaja.listaComandos))
        self.assertEqual([ruta.read_text() for ruta in valorDiario.parent.glob('before-resume-*.log')], ['saved log'])

    def pruebaReanudarYPausar(self):
        self.crearEntradaElemento()['VMState'] = 'paused'
        self.ejecutarComando.ejecutarComando()
        self.assertTrue(any(comando[1] == 'controlvm' and comando[3] == 'resume' for comando in self.valorCaja.listaComandos))
        self.assertFalse(any(comando[0] == 'make' for comando in self.valorCaja.listaComandos))

    def pruebaColisiónNombreMáquinaVirtualOtro(self):
        self.valorCaja.máquinasVirtual[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.esSinCambiar()

    def pruebaRechazadoMarcadorPropiedad(self):
        self.crearEntradaElemento()['owner'] = 'someone-else'
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.esSinCambiar()

    def pruebaRechazadoRutaAjustesOtro(self):
        self.crearEntradaElemento()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.esSinCambiar()

    def pruebaPreservadoDiscoUsuarioAdicional(self):
        máquina = self.crearEntradaElemento()
        máquina['VMState'] = 'poweroff'
        máquina['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.esSinCambiar()

    def pruebaRechazadoTransición(self):
        self.crearEntradaElemento()['VMState'] = 'saving'
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.esSinCambiar()

    def pruebaRechazadoDesregistrar(self):
        self.crearEntradaElemento()
        self.valorCaja.máquinasVirtual.clear()
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.esSinCambiar()

    def pruebaFalloConstruirActivadoPreservadoMáquinaVirtual(self):
        máquina = self.crearEntradaElemento()
        máquina['VMState'] = 'poweroff'
        elementoListaElementoPrevio = dict(máquina)
        self.valorCaja.valorFallo = 'make'
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.assertEqual(máquina, elementoListaElementoPrevio)

    def pruebaRecuperaciónMarcadorPropiedadInterrumpido(self):
        self.valorCaja.valorFallo = 'setextradata'
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()
        self.valorCaja.listaComandos.clear()
        self.assertEqual(self.ejecutarComando.ejecutarComando()['state'], 'running')
        self.assertFalse(any(comando[1] == 'createvm' for comando in self.valorCaja.listaComandos))

    def pruebaRechazadoAlteraciónISOPreservado(self):
        máquina = self.crearEntradaElemento()
        máquina['VMState'] = 'poweroff'
        Path(máquina['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ejecutarComando()

    def pruebaCreadoEstadoValorNinguno(self):
        self.assertEqual(self.ejecutarComando.mostrarEstadoValor()['state'], 'not-created')
        self.assertFalse(self.valorCaja.listaComandos)

    def pruebaRechazadoEscaparRuta(self):
        for ruta in ('../outside', '/tmp/outside'):
            with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ruta(ruta)
        (self.valorRaíz / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(valorMódulo.errorEjecución): self.ejecutarComando.ruta('media/kernel.iso')

    def pruebaPropiedadesCompuestoObjeto52VirtualBox(self):
        resultado = valorMódulo.valorAtributo('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(resultado['VMState'], 'running')
        self.assertEqual(resultado['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
