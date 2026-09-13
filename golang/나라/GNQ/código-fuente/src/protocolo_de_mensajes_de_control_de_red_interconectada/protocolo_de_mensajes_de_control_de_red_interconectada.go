package protocolo_de_mensajes_de_control_de_red_interconectada

import . "unsafe"
import . "consola"
import . "memoriagestor"
import . "trama_de_la_red_de_medio_compartido"
import . "protocolo_de_red_interconectada_4"
import . "utilidad"

var icmpconsola = TConsola{}

type TInternetcontrolMensajeprotocolMensajebuffer struct {
	Tipo	byte
	code	byte

	sumadeverificación	[2]byte
	datos			[4]byte
}

var icmpTamaño int = 64

type TInternetcontrolMensajeprotocolMensaje struct {
	Tipo	uint8
	code	uint8

	sumadeverificación	uint16
	datos			uint32
}

func (propio *TInternetcontrolMensajeprotocolMensaje) Init(buffer_2 TInternetcontrolMensajeprotocolMensajebuffer) {
	propio.Tipo = buffer_2.Tipo
	propio.code = buffer_2.code

	propio.sumadeverificación = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.sumadeverificación))
	propio.datos = Unsignedinteger32r(Matriztounsignedinteger32(buffer_2.datos))
}

func (propio *TInternetcontrolMensajeprotocolMensaje) Establecerbuffer(buffer_2 *TInternetcontrolMensajeprotocolMensajebuffer) {
	buffer_2.Tipo = propio.Tipo
	buffer_2.code = propio.code

	buffer_2.sumadeverificación = Unsignedinteger16tomatriz(propio.sumadeverificación)
	buffer_2.datos = Unsignedinteger32tomatriz(propio.datos)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protocolo_de_mensajes_de_control_de_red_interconectada *TProtocolo_de_mensajes_de_control_de_red_interconectada

func (propio *Icmphandler) Internetprotocolreceivewhen(origenipDirecciónredoctetoorder uint32, destinoipDirecciónredoctetoorder uint32, datosPuntero uintptr, tamaño uint32) bool {
	return protocolo_de_mensajes_de_control_de_red_interconectada.Internetprotocolreceivewhen(origenipDirecciónredoctetoorder, destinoipDirecciónredoctetoorder, datosPuntero, tamaño)
}

var iphandler IInternetprotocolhandler

type TProtocolo_de_mensajes_de_control_de_red_interconectada struct {
}

func (propio *TProtocolo_de_mensajes_de_control_de_red_interconectada) Init(backend TProveedor_del_protocolo_de_red_interconectada, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protocolo_de_mensajes_de_control_de_red_interconectada = propio
}
func (propio *TProtocolo_de_mensajes_de_control_de_red_interconectada) Internetprotocolreceivewhen(origenipDirecciónredoctetoorder uint32, destinoipDirecciónredoctetoorder uint32, datosPuntero uintptr, tamaño uint32) bool {
	if tamaño < uint32(icmpTamaño) {
		return false
	}

	var buffer_2 *TInternetcontrolMensajeprotocolMensajebuffer = (*TInternetcontrolMensajeprotocolMensajebuffer)(Pointer(datosPuntero))
	var msg TInternetcontrolMensajeprotocolMensaje = TInternetcontrolMensajeprotocolMensaje{}
	msg.Init(*buffer_2)

	icmpconsola.MImprimir(([]byte)("icmp:OnInternet"))
	icmpconsola.MUnsignedinteger16Imprimir(uint16(msg.Tipo))
	icmpconsola.MImprimir(([]byte)(":"))

	switch msg.Tipo {
	case 0:
		icmpconsola.MImprimir(([]byte)("ping response from "))
		break

	case 8:
		icmpconsola.MImprimir(([]byte)("ping send "))
		msg.Tipo = 0

		msg.sumadeverificación = 0
		msg.Establecerbuffer(buffer_2)
		msg.sumadeverificación = iphandler.Providerget().Sumadeverificación((*([4096]uint16))(Pointer(datosPuntero)), uint32(icmpTamaño))

		msg.Establecerbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (propio *TProtocolo_de_mensajes_de_control_de_red_interconectada) EchorequestEnviar(ipredoctetoorder uint32) bool {
	var protocolo_de_mensajes_de_control_de_red_interconectada TInternetcontrolMensajeprotocolMensaje = TInternetcontrolMensajeprotocolMensaje{}

	var memoriagestor = &TMemoriagestor{}
	var buffer_2 = (*TInternetcontrolMensajeprotocolMensajebuffer)(memoriagestor.Asignar_memoria(1024))

	protocolo_de_mensajes_de_control_de_red_interconectada.Tipo = 8
	protocolo_de_mensajes_de_control_de_red_interconectada.code = 0
	protocolo_de_mensajes_de_control_de_red_interconectada.datos = 0x3713
	protocolo_de_mensajes_de_control_de_red_interconectada.sumadeverificación = 0
	protocolo_de_mensajes_de_control_de_red_interconectada.Establecerbuffer(buffer_2)
	protocolo_de_mensajes_de_control_de_red_interconectada.sumadeverificación = iphandler.Providerget().Sumadeverificación((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpTamaño))
	protocolo_de_mensajes_de_control_de_red_interconectada.Establecerbuffer(buffer_2)

	var datosPuntero uintptr = uintptr(Pointer(buffer_2))
	iphandler.Enviar(ipredoctetoorder, 0x01, datosPuntero, uint32(icmpTamaño))

	return false

}
