"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

direcciónMáquina = bytes.fromhex('525400123456')
direcciónEquipoFísicoPasarela = bytes.fromhex('52550a000202')
valorDirecciónInternet = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class puenteRed:
    def __init__(valorPropio, númeroPuertoTransferenciaArchivo=2121, reglasReenvíoEnCurso=(), capturarDatos=False, direcciónInvitado=None, direcciónAnfitrión='127.0.0.1'):
        if not 1024 <= númeroPuertoTransferenciaArchivo <= 65535 or 50000 <= númeroPuertoTransferenciaArchivo <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        valorPropio.númeroPuertoTransferenciaArchivo = númeroPuertoTransferenciaArchivo
        valorPropio.ip_config = read_config(Path(__file__).resolve().parents[1])
        direcciónInvitado = direcciónInvitado or valorPropio.ip_config['IP']
        qemu_network(valorPropio.ip_config, direcciónInvitado)
        dirección=ipaddress.IPv4Address(direcciónInvitado)
        valorPropio.direcciónInvitado=str(dirección); valorPropio.direcciónActual=dirección.packed
        dirección=ipaddress.IPv4Address(direcciónAnfitrión)
        if dirección.is_multicast or str(dirección)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        valorPropio.direcciónAnfitrión=str(dirección)
        valorPropio.capturarDatos = capturarDatos; valorPropio.diarioTraza = []
        valorPropio.reglasReenvíoEnCurso = []
        ocupado = {('tcp', númeroPuertoTransferenciaArchivo)} | {('tcp', posiciónDatos) for posiciónDatos in range(50000,50008)}
        for valorRegla in reglasReenvíoEnCurso:
            componenteRuta = valorRegla.split(':')
            if len(componenteRuta) != 3 or componenteRuta[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            ABIRed, Anfitrión, invitado = componenteRuta[0], int(componenteRuta[1]), int(componenteRuta[2])
            if not 1024 <= Anfitrión <= 65535 or not 1 <= invitado <= 65535 or (ABIRed, Anfitrión) in ocupado:
                raise ValueError('invalid or duplicate forward: ' + valorRegla)
            ocupado.add((ABIRed, Anfitrión)); valorPropio.reglasReenvíoEnCurso.append((ABIRed, Anfitrión, invitado))
        valorPropio.recibirPuertos = []
        for _ in range(2):
            valorServidor = socket.socket()
            valorServidor.bind(('127.0.0.1', 0)); valorServidor.listen(1); valorServidor.setblocking(False)
            valorPropio.recibirPuertos.append(valorServidor)
        valorPropio.clientes = [None, None]
        valorPropio.esPendiente = [bytearray(), bytearray()]
        valorPropio.ethernet = bytearray(); valorPropio.datagramaSerie = bytearray(); valorPropio.escapado = valorPropio.esInválido = False
        valorPropio.eventoPausar = threading.Event(); valorPropio.error = None
        valorPropio.invitadoHaciaMarcos = valorPropio.invitadoDesdeMarcos = 0
        valorPropio.tareaFondo = threading.Thread(target=valorPropio.valorCiclo, daemon=True)
        valorPropio.tareaFondo.start()

    def argumentoReenviado(valorPropio):
        númeroPuertoSerie, puertoEthernet = [datosCadena.getsockname()[1] for datosCadena in valorPropio.recibirPuertos]
        reglaReenvíoEnCurso = 'user,id=wan,' + qemu_network(valorPropio.ip_config, valorPropio.direcciónInvitado) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(valorPropio.númeroPuertoTransferenciaArchivo, valorPropio.direcciónInvitado)
        for númeroPuerto in range(50000, 50008):
            reglaReenvíoEnCurso += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(númeroPuerto, valorPropio.direcciónInvitado)
        for ABIRed, Anfitrión, invitado in valorPropio.reglasReenvíoEnCurso:
            reglaReenvíoEnCurso += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(ABIRed, Anfitrión, valorPropio.direcciónInvitado, invitado)
        reglaReenvíoEnCurso=reglaReenvíoEnCurso.replace('127.0.0.1:',valorPropio.direcciónAnfitrión+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(númeroPuertoSerie),
                '-serial', 'chardev:slip', '-netdev', reglaReenvíoEnCurso,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(puertoEthernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def marcoEjecución(valorPropio, datosPaqueteDatos):
        valorPropio.esPendiente[1] += struct.pack('!I', len(datosPaqueteDatos)) + datosPaqueteDatos

    def paqueteDatosTraza(valorPropio, direcciónSentido, datosPaqueteDatos):
        if not valorPropio.capturarDatos or len(datosPaqueteDatos)<20: return
        valorDesfase=(datosPaqueteDatos[0]&15)*4
        valorEntradaElemento={'time':time.monotonic(),'direction':direcciónSentido,'bytes':len(datosPaqueteDatos),'protocol':datosPaqueteDatos[9]}
        if datosPaqueteDatos[9]==6 and len(datosPaqueteDatos)>=valorDesfase+20:
            datosOriginal,direcciónDatosDestino,númeroOrden,númeroConfirmación,bitsConfiguración,ventana=struct.unpack_from('!HHIIHH',datosPaqueteDatos,valorDesfase)
            valorEntradaElemento.update(source=datosOriginal,destination=direcciónDatosDestino,seq=númeroOrden,ack=númeroConfirmación,flags=bitsConfiguración&255,window=ventana,
                        payload=len(datosPaqueteDatos)-valorDesfase-((datosPaqueteDatos[valorDesfase+12]>>4)*4))
        valorPropio.diarioTraza.append(valorEntradaElemento)
        if len(valorPropio.diarioTraza)>2048: del valorPropio.diarioTraza[:1024]

    def entradaSLIP(valorPropio, Datos):
        for códigoCarácter in Datos:
            if códigoCarácter == 192:
                if valorPropio.datagramaSerie and not valorPropio.esInválido and not valorPropio.escapado:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(valorPropio.datagramaSerie)>=20 and valorPropio.datagramaSerie[0]>>4==4:
                        dirección=bytes(valorPropio.datagramaSerie[12:16])
                        try:
                            qemu_network(valorPropio.ip_config, str(ipaddress.IPv4Address(dirección)))
                            valorPropio.direcciónActual=dirección
                        except ValueError:
                            pass
                    valorPropio.paqueteDatosTraza('from_guest',valorPropio.datagramaSerie)
                    valorPropio.marcoEjecución(direcciónEquipoFísicoPasarela + direcciónMáquina + b'\x08\x00' + valorPropio.datagramaSerie)
                    valorPropio.invitadoDesdeMarcos += 1
                valorPropio.datagramaSerie.clear(); valorPropio.escapado = valorPropio.esInválido = False
            elif códigoCarácter == 219 and not valorPropio.escapado:
                valorPropio.escapado = True
            else:
                if valorPropio.escapado:
                    if códigoCarácter not in (220, 221): valorPropio.esInválido = True
                    códigoCarácter = 192 if códigoCarácter == 220 else 219
                    valorPropio.escapado = False
                if len(valorPropio.datagramaSerie) < 1600: valorPropio.datagramaSerie.append(códigoCarácter)
                else: valorPropio.esInválido = True

    def entradaEthernet(valorPropio, Datos):
        valorPropio.ethernet += Datos
        while len(valorPropio.ethernet) >= 4:
            númeroElementosElementoLista = struct.unpack_from('!I', valorPropio.ethernet)[0]
            if númeroElementosElementoLista > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(valorPropio.ethernet) < númeroElementosElementoLista + 4: return
            marcoEjecución = bytes(valorPropio.ethernet[4:4+númeroElementosElementoLista]); del valorPropio.ethernet[:4+númeroElementosElementoLista]
            if len(marcoEjecución) < 14: continue
            if marcoEjecución[12:14] == b'\x08\x06' and len(marcoEjecución) >= 42:
                paqueteDatosResoluciónDirección = marcoEjecución[14:42]
                if paqueteDatosResoluciónDirección[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and paqueteDatosResoluciónDirección[24:28] == valorPropio.direcciónActual:
                    respuestaRetorno = paqueteDatosResoluciónDirección[:6] + b'\x00\x02' + direcciónMáquina + valorPropio.direcciónActual + paqueteDatosResoluciónDirección[8:18]
                    valorPropio.marcoEjecución(marcoEjecución[6:12] + direcciónMáquina + b'\x08\x06' + respuestaRetorno)
            elif marcoEjecución[12:14] == b'\x08\x00':
                datosPaqueteDatos = marcoEjecución[14:]
                valorPropio.paqueteDatosTraza('to_guest',datosPaqueteDatos)
                valorPropio.esPendiente[0] += b'\xc0' + datosPaqueteDatos.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                valorPropio.invitadoHaciaMarcos += 1

    def valorCiclo(valorPropio):
        try:
            while not valorPropio.eventoPausar.is_set():
                lectores = [datosCadena for índiceOrdinal, datosCadena in enumerate(valorPropio.recibirPuertos) if valorPropio.clientes[índiceOrdinal] is None]
                lectores += [datosCadena for datosCadena in valorPropio.clientes if datosCadena is not None]
                escritores = [datosCadena for índiceOrdinal, datosCadena in enumerate(valorPropio.clientes) if datosCadena is not None and valorPropio.esPendiente[índiceOrdinal]]
                puedeLeer, escribible, _ = select.select(lectores, escritores, [], .05)
                for datosCadena in puedeLeer:
                    if datosCadena in valorPropio.recibirPuertos:
                        índiceOrdinal = valorPropio.recibirPuertos.index(datosCadena); valorPropio.clientes[índiceOrdinal], _ = datosCadena.accept(); valorPropio.clientes[índiceOrdinal].setblocking(False)
                    else:
                        índiceOrdinal = valorPropio.clientes.index(datosCadena); Datos = datosCadena.recv(16384)
                        if not Datos: return
                        (valorPropio.entradaSLIP if índiceOrdinal == 0 else valorPropio.entradaEthernet)(Datos)
                for datosCadena in escribible:
                    índiceOrdinal = valorPropio.clientes.index(datosCadena)
                    try: númeroElementosElementoLista = datosCadena.send(valorPropio.esPendiente[índiceOrdinal])
                    except BlockingIOError: continue
                    del valorPropio.esPendiente[índiceOrdinal][:númeroElementosElementoLista]
                if any(len(valorSegundo) > 1024 * 1024 for valorSegundo in valorPropio.esPendiente):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as entradaElementoAuxiliar:
            if not valorPropio.eventoPausar.is_set(): valorPropio.error = str(entradaElementoAuxiliar)

    def cerrar(valorPropio):
        valorPropio.eventoPausar.set(); valorPropio.tareaFondo.join(timeout=2)
        for datosCadena in valorPropio.recibirPuertos + valorPropio.clientes:
            if datosCadena is not None: datosCadena.close()

    def __enter__(valorPropio): return valorPropio
    def __exit__(valorPropio, *arregloArgumento): valorPropio.cerrar()
