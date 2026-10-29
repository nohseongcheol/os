#!/usr/bin/env python3
"""jkoros 전용 VirtualBox LanzadorPrograma. 기존 VM/디스크/valorAlmacenar 상태는 삭제하지 않는다."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid


class errorEjecución(RuntimeError):
    pass


def ejecutarComandoIntérpreteComandos(argumentos):
    entorno = dict(os.environ, LC_ALL='C')
    resultado = subprocess.run([str(valor) for valor in argumentos], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=entorno, timeout=180)
    valorContenidoValor = resultado.stdout.decode('utf-8', 'replace')
    if resultado.returncode:
        raise errorEjecución('comando valorFallo: ' + ' '.join(str(valor) for valor in argumentos) + '\n' + valorContenidoValor[-10000:])
    return valorContenidoValor


def valorAtributo(valorContenidoValor):
    resultado = {}
    for línea in valorContenidoValor.splitlines():
        if '=' not in línea:
            continue
        nombre, valor = línea.split('=', 1)
        if nombre.startswith('"'):
            nombre = json.loads(nombre)
        if valor.startswith('"'):
            try:
                leerValor, terminación = json.JSONDecoder().raw_decode(valor)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if terminación == len(valor): valor = leerValor
            except ValueError:
                raise errorEjecución('VirtualBox valorAtributo valorFormato error: ' + línea)
        resultado[nombre] = valor
    return resultado


def entradasRegistradoElemento(valorContenidoValor):
    resultado = {}
    for línea in valorContenidoValor.splitlines():
        esIgual = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', línea)
        if esIgual: resultado[esIgual.group(2).lower()] = esIgual.group(1)
    return resultado


def sumaComprobación(ruta):
    valor = hashlib.sha256()
    with ruta.open('rb') as Archivo:
        for Datos in iter(lambda: Archivo.read(1024 * 1024), b''): valor.update(Datos)
    return valor.hexdigest()


class LanzadorPrograma:
    def __init__(self, valorRaíz, nombre, modoMétodo='gui', comando=ejecutarComandoIntérpreteComandos):
        self.valorRaíz = Path(valorRaíz).resolve()
        self.nombre, self.modoMétodo, self.comando = nombre, modoMétodo, comando
        self.preservarValor = self.valorRaíz / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', nombre) or nombre in ('.', '..'):
            raise errorEjecución('VM 이름은 Caracteres·valorDígito·공백·밑줄·괄호·마침표·하이픈만 사용할 númeroValor 있습니다.')
        if modoMétodo not in ('gui', 'headless'): raise errorEjecución('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ruta(self, valorParRed):
        if Path(valorParRed).is_absolute() or '..' in Path(valorParRed).parts:
            raise errorEjecución('잘못된 관리 ruta: ' + str(valorParRed))
        resultado = self.preservarValor
        for valorSubparte in ['.vbox'] + list(Path(valorParRed).parts):
            if valorSubparte == '.vbox': resultado = self.preservarValor
            else: resultado = resultado / valorSubparte
            if resultado.is_symlink(): raise errorEjecución('conectar 경로는 사용하지 않습니다: ' + str(resultado))
        return resultado

    def leer(self):
        ruta = self.ruta('state.json')
        if not ruta.exists(): return None
        valorEstadoValor = json.loads(ruta.read_text(encoding='utf-8'))
        if valorEstadoValor.get('version') != 1 or valorEstadoValor.get('name') != self.nombre:
            raise errorEjecución('관리 상태의 VM nombre/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for nombre in ('uuid', 'owner'):
            if str(uuid.UUID(valorEstadoValor[nombre])) != valorEstadoValor[nombre]: raise errorEjecución('잘못된 VM valorIdentificador')
        return valorEstadoValor

    def valorAlmacenar(self, valorEstadoValor):
        valorDestino = self.ruta('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.preservarValor), delete=False) as Archivo:
            json.dump(valorEstadoValor, Archivo, ensure_ascii=False, indent=2)
            Archivo.write('\n')
            valorTemporal = Archivo.name
        os.replace(valorTemporal, str(valorDestino))

    def informaciónSistema(self, valorEstadoValor, valorRegistradoElemento, recuperarEstadoValor=False):
        if valorEstadoValor['uuid'] not in valorRegistradoElemento:
            raise errorEjecución('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        informaciónSistema = valorAtributo(self.comando(['VBoxManage', 'showvminfo', valorEstadoValor['uuid'], '--machinereadable']))
        posición = Path(informaciónSistema.get('CfgFile', '')).resolve()
        if self.ruta('machines').resolve() not in posición.parents or informaciónSistema.get('UUID') != valorEstadoValor['uuid']:
            raise errorEjecución('이 프로젝트의 VM ajustes ruta/UUID와 일치하지 않아 변경하지 않습니다.')
        valorMarcador = self.comando(['VBoxManage', 'getextradata', valorEstadoValor['uuid'], 'JKOROS/Owner']).strip()
        if valorMarcador != 'Value: ' + valorEstadoValor['owner']:
            if recuperarEstadoValor and valorEstadoValor.get('pending') and valorMarcador == 'No value set!':
                self.comando(['VBoxManage', 'setextradata', valorEstadoValor['uuid'], 'JKOROS/Owner', valorEstadoValor['owner']])
            else:
                raise errorEjecución('VM valorPropietario 표식이 일치하지 않아 변경하지 않습니다.')
        return informaciónSistema

    def comprobarMedios(self, valorEstadoValor, informaciónSistema):
        listaControladores = [valor for nombre, valor in informaciónSistema.items() if re.fullmatch(r'storagecontrollername\d+', nombre)]
        permitirValor = [str(self.ruta(valor)) for valor in valorEstadoValor.get('media', [])]
        for nombre, valor in informaciónSistema.items():
            if any(re.fullmatch(re.escape(Controlador) + r'-\d+-\d+', nombre) for Controlador in listaControladores):
                if valor not in ('none', 'emptydrive') and valor not in permitirValor:
                    raise errorEjecución('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + valor)

    def mostrarEstadoValor(self):
        valorEstadoValor = self.leer()
        if valorEstadoValor is None: return {'name': self.nombre, 'state': 'not-created'}
        informaciónSistema = self.informaciónSistema(valorEstadoValor, entradasRegistradoElemento(self.comando(['VBoxManage', 'list', 'vms'])))
        return {'name': informaciónSistema.get('name', valorEstadoValor['name']), 'uuid': valorEstadoValor['uuid'], 'state': informaciónSistema.get('VMState'),
                'iso': str(self.ruta(valorEstadoValor['iso'])) if valorEstadoValor.get('iso') else None,
                'serial_log': str(self.ruta(valorEstadoValor['serial_log'])) if valorEstadoValor.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ejecutarComando(self):
        valorEstadoValor = self.leer()
        valorRegistradoElemento = entradasRegistradoElemento(self.comando(['VBoxManage', 'list', 'vms']))
        informaciónSistema = None
        if valorEstadoValor is not None and valorEstadoValor['uuid'] in valorRegistradoElemento:
            informaciónSistema = self.informaciónSistema(valorEstadoValor, valorRegistradoElemento, recuperarEstadoValor=True)
            elementoListaActual = informaciónSistema.get('VMState')
            if elementoListaActual == 'running':
                print('이미 ejecutarComando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.mostrarEstadoValor()
            self.comprobarMedios(valorEstadoValor, informaciónSistema)
            if elementoListaActual in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 valorAlmacenar 상태를 버리지 않습니다.'.format(elementoListaActual))
                if elementoListaActual == 'paused':
                    self.comando(['VBoxManage', 'controlvm', valorEstadoValor['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 valorReintentar abrir 전에 기존 기록도 보관한다.
                    if valorEstadoValor.get('serial_log'):
                        original = self.ruta(valorEstadoValor['serial_log'])
                        if original.is_file():
                            shutil.copyfile(str(original), str(self.ruta('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.comando(['VBoxManage', 'startvm', valorEstadoValor['uuid'], '--type', self.modoMétodo])
                return self.mostrarEstadoValor()
            if elementoListaActual not in ('poweroff', 'aborted'):
                raise errorEjecución('VM이 modoConmutar 중입니다 ({}). 작업이 끝난 valorLadoPosterior valorReintentar 실행하세요.'.format(elementoListaActual))
        elif valorEstadoValor is not None and not valorEstadoValor.get('pending'):
            raise errorEjecución('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 valorReintentar 등록하세요.')
        elif self.nombre in valorRegistradoElemento.values():
            raise errorEjecución('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # valorAlmacenar/ejecutarComando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.comando(['make', '-C', str(self.valorRaíz / 'os'), 'iso']), end='')
        original = self.valorRaíz / 'os/build/kernel.iso'
        if not original.is_file() or original.stat().st_size == 0: raise errorEjecución('Arranque ISO가 생성되지 않았습니다.')
        valorMedios = 'media/kernel-' + sumaComprobación(original) + '.iso'
        valorDestino = self.ruta(valorMedios)
        valorDestino.parent.mkdir(exist_ok=True)
        if valorDestino.exists():
            if sumaComprobación(valorDestino) != sumaComprobación(original): raise errorEjecución('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(valorDestino))
        else:
            with tempfile.NamedTemporaryFile(dir=str(valorDestino.parent)) as Archivo:
                shutil.copyfile(str(original), Archivo.name)
                os.link(Archivo.name, str(valorDestino))

        if valorEstadoValor is None:
            valorEstadoValor = {'version': 1, 'name': self.nombre, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.valorAlmacenar(valorEstadoValor)
        if informaciónSistema is None:
            self.comando(['VBoxManage', 'createvm', '--name', valorEstadoValor['name'], '--uuid', valorEstadoValor['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ruta('machines')), '--register'])
            self.comando(['VBoxManage', 'setextradata', valorEstadoValor['uuid'], 'JKOROS/Owner', valorEstadoValor['owner']])
        # construirSistema 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        informaciónSistema = self.informaciónSistema(valorEstadoValor, entradasRegistradoElemento(self.comando(['VBoxManage', 'list', 'vms'])))
        if informaciónSistema.get('VMState') not in ('poweroff', 'aborted'):
            raise errorEjecución('construirSistema 중 VM 상태가 바뀌었습니다. valorReintentar make vbox를 실행하세요.')
        self.comprobarMedios(valorEstadoValor, informaciónSistema)
        valorEstadoValor['iso'] = valorMedios
        if valorMedios not in valorEstadoValor['media']: valorEstadoValor['media'].append(valorMedios)
        valorEstadoValor['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        valorDiario = self.ruta(valorEstadoValor['serial_log'])
        valorDiario.parent.mkdir(exist_ok=True)
        self.valorAlmacenar(valorEstadoValor)
        self.comando(['VBoxManage', 'modifyvm', valorEstadoValor['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(valorDiario)])
        listaControladores = [valor for nombre, valor in informaciónSistema.items() if re.fullmatch(r'storagecontrollername\d+', nombre)]
        if 'JKOROS IDE' not in listaControladores:
            self.comando(['VBoxManage', 'storagectl', valorEstadoValor['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.comando(['VBoxManage', 'storageattach', valorEstadoValor['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(valorDestino)])
        valorEstadoValor['pending'] = False
        self.valorAlmacenar(valorEstadoValor)
        self.comando(['VBoxManage', 'startvm', valorEstadoValor['uuid'], '--type', self.modoMétodo])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.mostrarEstadoValor()


def ponerEnMarcha():
    analizarValor = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ejecutarComando 및 valorEstadoValor valorConsultar')
    analizarValor.add_argument('action', choices=['run', 'status'])
    argumentoParámetro = analizarValor.parse_args()
    ejecutarComando = LanzadorPrograma(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if argumentoParámetro.action == 'status':
        print(json.dumps(ejecutarComando.mostrarEstadoValor(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise errorEjecución('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise errorEjecución('/dev/vboxdrv에 접근할 númeroValor 없습니다. Anfitrión 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/valorPermiso 변경은 하지 않습니다.')
    os.umask(0o077)
    ejecutarComando.ruta('lock').parent.mkdir(parents=True, exist_ok=True)
    with ejecutarComando.ruta('lock').open('a') as valorCerrojo:
        try: fcntl.flock(valorCerrojo, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise errorEjecución('다른 jkoros VirtualBox ejecutarComando 작업이 진행 중입니다.')
        print(json.dumps(ejecutarComando.ejecutarComando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ponerEnMarcha()
    except (errorEjecución, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print('VBOX error: ' + str(error), file=sys.stderr)
        sys.exit(1)
