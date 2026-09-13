package protocolo_de_datagramas_de_usuario

import . "unsafe"
import . "consola"
import . "utilidad"
import . "memoriagestor"
import . "protocolo_de_red_interconectada_4"

var udpconsola = TConsola{}

type TUsuariodatagramprotocolencabezadobuffer struct {
	número_del_puerto_de_origen	[2]byte
	número_del_puerto_de_destino	[2]byte

	duración		[2]byte
	sumadeverificación	[2]byte
}

var udpencabezadoTamaño uint32 = 8

type TCabecera_de_datagramas_de_usuario struct {
	número_del_puerto_de_origen	uint16
	número_del_puerto_de_destino	uint16

	duración		uint16
	sumadeverificación	uint16
}

func (propio *TCabecera_de_datagramas_de_usuario) Init(buffer_2 *TUsuariodatagramprotocolencabezadobuffer) {
	propio.número_del_puerto_de_origen = Matriztounsignedinteger16(buffer_2.número_del_puerto_de_origen)
	propio.número_del_puerto_de_destino = Matriztounsignedinteger16(buffer_2.número_del_puerto_de_destino)

	propio.duración = Matriztounsignedinteger16(buffer_2.duración)
	propio.sumadeverificación = Matriztounsignedinteger16(buffer_2.sumadeverificación)
}
func (propio *TCabecera_de_datagramas_de_usuario) Establecerbuffer(buffer_2 *TUsuariodatagramprotocolencabezadobuffer) {

	buffer_2.número_del_puerto_de_origen = Unsignedinteger16tomatriz(propio.número_del_puerto_de_origen)
	buffer_2.número_del_puerto_de_destino = Unsignedinteger16tomatriz(propio.número_del_puerto_de_destino)

	buffer_2.duración = Unsignedinteger16tomatriz(propio.duración)
	buffer_2.sumadeverificación = Unsignedinteger16tomatriz(propio.sumadeverificación)

}

type IUsuariodatagramprotocolhandler interface {
	ManijausuariodatagramprotocolMensaje(conectorRed *TExtremo_de_comunicación_de_datagramas_de_usuario, datos uintptr, tamaño uint16)
}

type TUsuariodatagramprotocolhandler struct {
}

func (propio *TUsuariodatagramprotocolhandler) Init(backend TProveedor_del_protocolo_de_red_interconectada) {
}
func (propio *TUsuariodatagramprotocolhandler) ManijausuariodatagramprotocolMensaje(conectorRed *TExtremo_de_comunicación_de_datagramas_de_usuario, datos uintptr, tamaño uint16) {
}

type IUsuariodatagramprotocolconectorRed interface {
	ManijausuariodatagramprotocolMensaje(datos uintptr, tamaño uint16)
}
type TExtremo_de_comunicación_de_datagramas_de_usuario struct {
	remotopuertoNúmero	uint16
	remotoip		uint32
	localpuertoNúmero	uint16
	localip			uint32

	listening	bool
}

var udpprovider TUsuariodatagramprotocolprovider
var udphandler IUsuariodatagramprotocolhandler

func (propio *TExtremo_de_comunicación_de_datagramas_de_usuario) Probar() {
}
func (propio *TExtremo_de_comunicación_de_datagramas_de_usuario) Init(pudpprovider TUsuariodatagramprotocolprovider, pudphandler IUsuariodatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	propio.listening = false
}
func (propio *TExtremo_de_comunicación_de_datagramas_de_usuario) ManijausuariodatagramprotocolMensaje(datos uintptr, tamaño uint16) {
	if udphandler != nil {
		udphandler.ManijausuariodatagramprotocolMensaje(propio, datos, tamaño)
	}
}
func (propio *TExtremo_de_comunicación_de_datagramas_de_usuario) Enviar(pdatos []byte, tamaño uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(tamaño); i++ {
		buffer_2[i] = pdatos[i]
	}
	var datos = uintptr(Pointer(&buffer_2))
	udpprovider.Enviar(propio, datos, tamaño)
}
func (propio *TExtremo_de_comunicación_de_datagramas_de_usuario) Desconectar() {
	udpprovider.Desconectar(propio)
}

type TUsuariodatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TExtremo_de_comunicación_de_datagramas_de_usuario
var númerosockets int
var librepuerto uint16

func (propio *TUsuariodatagramprotocolprovider) Init(pipprovider TProveedor_del_protocolo_de_red_interconectada, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	númerosockets = 0
	librepuerto = 1024
}
func (propio *TUsuariodatagramprotocolprovider) Internetprotocolreceivewhen(origenipDirecciónredoctetoorder uint32, destinoipDirecciónredoctetoorder uint32, internetprotocolpayload uintptr, tamaño uint32) bool {
	if tamaño < udpencabezadoTamaño {
		return false
	}

	var buffer_2 *TUsuariodatagramprotocolencabezadobuffer = (*TUsuariodatagramprotocolencabezadobuffer)(Pointer(internetprotocolpayload))
	var msg TCabecera_de_datagramas_de_usuario
	msg.Init(buffer_2)

	var conectorRed *TExtremo_de_comunicación_de_datagramas_de_usuario = nil

	for i := 0; i < númerosockets && conectorRed == nil; i++ {
		if sockets[i].localpuertoNúmero == msg.número_del_puerto_de_destino && sockets[i].localip == destinoipDirecciónredoctetoorder && sockets[i].listening == true {
			conectorRed = &sockets[i]
			conectorRed.listening = false
			conectorRed.remotopuertoNúmero = msg.número_del_puerto_de_origen
			conectorRed.remotoip = origenipDirecciónredoctetoorder
		} else if sockets[i].localpuertoNúmero == msg.número_del_puerto_de_destino && sockets[i].localip == destinoipDirecciónredoctetoorder && sockets[i].remotopuertoNúmero == msg.número_del_puerto_de_origen && sockets[i].remotoip == origenipDirecciónredoctetoorder {
			conectorRed = &sockets[i]

		}
	}

	msg.Establecerbuffer(buffer_2)
	if conectorRed != nil {
		conectorRed.ManijausuariodatagramprotocolMensaje(internetprotocolpayload+uintptr(udpencabezadoTamaño), uint16(tamaño-udpencabezadoTamaño))
	}

	return false
}

func (propio *TUsuariodatagramprotocolprovider) Conectar(ip uint32, puerto uint16) *TExtremo_de_comunicación_de_datagramas_de_usuario {
	var memoriagestor = &TMemoriagestor{}
	var conectorRed = (*TExtremo_de_comunicación_de_datagramas_de_usuario)(memoriagestor.Asignar_memoria(50))

	if conectorRed != nil {

		conectorRed.Init(*propio, nil)
		conectorRed.remotopuertoNúmero = puerto
		conectorRed.remotoip = ip
		conectorRed.localpuertoNúmero = librepuerto
		librepuerto++
		conectorRed.localip = uint32((*iphandler.Providerget()).GetipDirección())

		conectorRed.remotopuertoNúmero = Unsignedinteger16r(conectorRed.remotopuertoNúmero)
		conectorRed.localpuertoNúmero = Unsignedinteger16r(conectorRed.localpuertoNúmero)

		sockets[númerosockets] = *conectorRed
		númerosockets++

	}
	return conectorRed

}
func (propio *TUsuariodatagramprotocolprovider) Listen(puerto uint16) *TExtremo_de_comunicación_de_datagramas_de_usuario {
	var conectorRed = &TExtremo_de_comunicación_de_datagramas_de_usuario{}
	conectorRed = nil
	if conectorRed != nil {
		conectorRed.Init(*propio, nil)
		conectorRed.listening = true
		conectorRed.localpuertoNúmero = puerto
		conectorRed.localip = uint32((*iphandler.Providerget()).GetipDirección())

		conectorRed.localpuertoNúmero = Unsignedinteger16r(conectorRed.localpuertoNúmero)
	}
	return conectorRed
}
func (propio *TUsuariodatagramprotocolprovider) Desconectar(conectorRed *TExtremo_de_comunicación_de_datagramas_de_usuario) {
	for i := 0; i < númerosockets && conectorRed == nil; i++ {
		if sockets[i] == *conectorRed {
			númerosockets--
			sockets[i] = sockets[númerosockets]
			break
		}
	}
}
func (propio *TUsuariodatagramprotocolprovider) Enviar(conectorRed *TExtremo_de_comunicación_de_datagramas_de_usuario, pdatos uintptr, tamaño uint16) {
	var totalDuración = uint32(tamaño) + udpencabezadoTamaño

	var buffer_2 [4096]byte

	var msgbuffer = (*TUsuariodatagramprotocolencabezadobuffer)(Pointer(&buffer_2))

	var msg = TCabecera_de_datagramas_de_usuario{}

	msg.número_del_puerto_de_origen = conectorRed.localpuertoNúmero
	msg.número_del_puerto_de_destino = conectorRed.remotopuertoNúmero
	msg.duración = Unsignedinteger16r(uint16(totalDuración))

	msg.sumadeverificación = 0x0
	msg.Establecerbuffer(msgbuffer)

	var datosbytes [4096]byte = *(*[4096]byte)(Pointer(pdatos))
	for i := 0; i < int(tamaño); i++ {
		buffer_2[int(udpencabezadoTamaño)+i] = datosbytes[i]
	}

	var datos uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Enviar(conectorRed.remotoip, 0x11, datos, totalDuración)

}
func (propio *TUsuariodatagramprotocolprovider) Víncula(conectorRed *TExtremo_de_comunicación_de_datagramas_de_usuario, handler *TUsuariodatagramprotocolhandler) {
}
