/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocolo_de_red_interconectada_4

import . "unsafe"
import . "utilidad"
import . "consola"
import . "trama_de_la_red_de_medio_compartido"
import . "arp"

var ipconsola TConsola = TConsola{}

type TInternetprotocolv4Mensajebuffer struct {
	lenver		byte
	tos		byte
	totalDuración	[2]byte

	ident			[2]byte
	banderasyDesplazamiento	[2]byte

	horatolive		byte
	protocol		byte
	sumadeverificación	[2]byte

	origenipDirección	[4]byte
	destinoipDirección	[4]byte
}

var ipTamaño uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Mensaje struct {
	encabezadoDuración	uint8
	versión			uint8
	tos			uint8
	totalDuración		uint16

	ident			uint16
	banderasyDesplazamiento	uint16

	horatolive		uint8
	protocol		uint8
	sumadeverificación	uint16

	origenipDirección	uint32
	destinoipDirección	uint32
}

func (propio *TInternetprotocolv4Mensaje) Init(buffer_2 TInternetprotocolv4Mensajebuffer) {

	propio.versión = ((buffer_2.lenver & 0xF0) >> 4)
	propio.encabezadoDuración = buffer_2.lenver & 0x0F
	propio.tos = buffer_2.tos
	propio.totalDuración = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.totalDuración))

	propio.ident = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.ident))
	propio.banderasyDesplazamiento = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.banderasyDesplazamiento))

	propio.horatolive = buffer_2.horatolive
	propio.protocol = buffer_2.protocol
	propio.sumadeverificación = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.sumadeverificación))

	propio.origenipDirección = Unsignedinteger32r(Matriztounsignedinteger32(buffer_2.origenipDirección))
	propio.destinoipDirección = Unsignedinteger32r(Matriztounsignedinteger32(buffer_2.destinoipDirección))

}
func (propio *TInternetprotocolv4Mensaje) Establecerbuffer(buffer_2 *TInternetprotocolv4Mensajebuffer) {

	buffer_2.lenver = byte(((propio.versión & 0x0F) << 4) | (propio.encabezadoDuración & 0x0F))
	buffer_2.tos = propio.tos
	buffer_2.totalDuración = Unsignedinteger16tomatriz(propio.totalDuración)

	buffer_2.ident = Unsignedinteger16tomatriz(propio.ident)
	buffer_2.banderasyDesplazamiento = Unsignedinteger16tomatriz(propio.banderasyDesplazamiento)

	buffer_2.horatolive = propio.horatolive
	buffer_2.protocol = propio.protocol
	buffer_2.sumadeverificación = Unsignedinteger16tomatriz(propio.sumadeverificación)

	buffer_2.origenipDirección = Unsignedinteger32tomatriz(propio.origenipDirección)
	buffer_2.destinoipDirección = Unsignedinteger32tomatriz(propio.destinoipDirección)

}

type IInternetprotocolhandler interface {
	Init(backend TProveedor_del_protocolo_de_red_interconectada, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(origenipDirecciónredoctetoorder uint32, destinoipDirecciónredoctetoorder uint32, datosPuntero uintptr, tamaño uint32) bool
	Enviar(destinoipDirecciónredoctetoorder uint32, pprotocol uint8, datosPuntero uintptr, tamaño uint32)
	Providerget() *TProveedor_del_protocolo_de_red_interconectada
}

type TInternetprotocolhandler struct {
}

var ipethernettramahandler Ipethernettramahandler = Ipethernettramahandler{}
var protocol uint8

func (propio *TInternetprotocolhandler) Init(backend TProveedor_del_protocolo_de_red_interconectada, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (propio *TInternetprotocolhandler) Internetprotocolreceivewhen(origenipDirecciónredoctetoorder uint32, destinoipDirecciónredoctetoorder uint32, datosPuntero uintptr, tamaño uint32) bool {
	ipconsola.MImprimir(([]byte)("ipHandler:OnInternet"))
	return false
}
func (propio *TInternetprotocolhandler) Enviar(destinoipDirecciónredoctetoorder uint32, pprotocol uint8, datosPuntero uintptr, tamaño uint32) {

	proveedor_del_protocolo_de_red_interconectada.Enviar(destinoipDirecciónredoctetoorder, pprotocol, datosPuntero, tamaño)
}
func (propio *TInternetprotocolhandler) Providerget() *TProveedor_del_protocolo_de_red_interconectada {
	return &proveedor_del_protocolo_de_red_interconectada
}

type Ipethernettramahandler struct {
	TEthernettramahandler
}

var proveedor_del_protocolo_de_red_interconectada TProveedor_del_protocolo_de_red_interconectada

func (propio *Ipethernettramahandler) Ethernettramareceivewhen(datosPuntero uintptr, tamaño int) bool {
	ipconsola.MImprimir(([]byte)("iphandler:onEtherfameRecv\n"))
	return proveedor_del_protocolo_de_red_interconectada.Ethernettramareceivewhen(datosPuntero, uint32(tamaño))

}

func (propio *Ipethernettramahandler) Enviar(destinoipDirecciónredoctetoorder uint64, datosPuntero uintptr, tamaño uint32) {
	ipconsola.MImprimir(([]byte)("ipefhandler:send\n"))
	var ethernettipobe = Unsignedinteger16r(0x0800)
	propio.TEthernettramahandler.TramaEnviar(destinoipDirecciónredoctetoorder, ethernettipobe, datosPuntero, tamaño)

}

var handler_2 [255]IInternetprotocolhandler

type TProveedor_del_protocolo_de_red_interconectada struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMáscara	uint32
}

var efhandler IEthernettramahandler

func (propio *TProveedor_del_protocolo_de_red_interconectada) Init(pefprovider TProveedor_de_tramas_de_red_de_medio_compartido, pefhandler IEthernettramahandler, arp Arpprovider, gatewayip uint32, subnetMáscara uint32) {

	efhandler = pefhandler
	efhandler.Establecerhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	propio.arpprovider = arp
	propio.Gatewayip = gatewayip
	propio.SubnetMáscara = subnetMáscara
	proveedor_del_protocolo_de_red_interconectada = *propio
}
func (propio *TProveedor_del_protocolo_de_red_interconectada) Ethernettramareceivewhen(ethernettramapayload uintptr, tamaño uint32) bool {
	if tamaño < uint32(ipTamaño) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Mensajebuffer = (*TInternetprotocolv4Mensajebuffer)(Pointer(ethernettramapayload))
	var internetprotocolMensaje TInternetprotocolv4Mensaje
	internetprotocolMensaje.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMensaje.destinoipDirección == uint32(efhandler.GetipDirección()) {

		var duración uint32 = uint32(internetprotocolMensaje.totalDuración)
		if duración > tamaño {
			duración = tamaño
		}
		if handler_2[internetprotocolMensaje.protocol] != nil {
			reply = handler_2[internetprotocolMensaje.protocol].Internetprotocolreceivewhen(internetprotocolMensaje.origenipDirección, internetprotocolMensaje.destinoipDirección, ethernettramapayload+uintptr(4*internetprotocolMensaje.encabezadoDuración), uint32(duración-uint32(4*internetprotocolMensaje.encabezadoDuración)))

		}
	}

	if reply {

		var temporary = internetprotocolMensaje.destinoipDirección
		internetprotocolMensaje.destinoipDirección = internetprotocolMensaje.origenipDirección
		internetprotocolMensaje.origenipDirección = temporary

		internetprotocolMensaje.horatolive = 0x40
		internetprotocolMensaje.sumadeverificación = 0

		internetprotocolMensaje.Establecerbuffer(buffer_2)
		internetprotocolMensaje.sumadeverificación = propio.Sumadeverificación((*([4096]uint16))(Pointer(ethernettramapayload)), uint32(4*internetprotocolMensaje.encabezadoDuración))

		internetprotocolMensaje.Establecerbuffer(buffer_2)

	}

	ipconsola.MImprimir(([]byte)("ipmessage"))
	ipconsola.MUnsignedinteger32Imprimir(internetprotocolMensaje.origenipDirección)
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MUnsignedinteger32Imprimir(internetprotocolMensaje.destinoipDirección)
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MUnsignedinteger16Imprimir(uint16(internetprotocolMensaje.encabezadoDuración))
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MUnsignedinteger16Imprimir(uint16(internetprotocolMensaje.versión))
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MUnsignedinteger16Imprimir(internetprotocolMensaje.totalDuración)
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MUnsignedinteger32Imprimir(uint32(efhandler.GetipDirección()))
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MImprimir(([]byte)("\n"))

	return reply

}
func (propio *TProveedor_del_protocolo_de_red_interconectada) Enviar(destinoipDirecciónredoctetoorder uint32, protocol uint8, datosPuntero uintptr, tamaño uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Mensajebuffer = (*TInternetprotocolv4Mensajebuffer)(Pointer(&buffer1_2))
	var mensaje TInternetprotocolv4Mensaje = TInternetprotocolv4Mensaje{}
	mensaje.versión = 4
	mensaje.encabezadoDuración = ipTamaño / 4
	mensaje.tos = 0
	mensaje.totalDuración = Unsignedinteger16r(uint16(tamaño + uint32(ipTamaño)))

	mensaje.ident = 0x0100
	mensaje.banderasyDesplazamiento = 0x0040
	mensaje.horatolive = 0x40
	mensaje.protocol = protocol

	mensaje.destinoipDirección = destinoipDirecciónredoctetoorder

	mensaje.origenipDirección = uint32(efhandler.GetipDirección())

	mensaje.sumadeverificación = 0

	mensaje.Establecerbuffer(buffer_2)
	mensaje.sumadeverificación = propio.Sumadeverificación((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipTamaño))
	mensaje.Establecerbuffer(buffer_2)

	var datosbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datosPuntero))

	for i := 0; i < int(tamaño); i++ {

		buffer1_2[i+int(ipTamaño)] = datosbuffer_2[i]
	}

	ipconsola.MImprimirxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(tamaño)+int(ipTamaño); i++ {
		ipconsola.MHexadecimalImprimir(buffer1_2[i])
	}
	ipconsola.MImprimir(([]byte)(":"))
	ipconsola.MImprimir(([]byte)("]\n"))

	var siguientehopipDirecciónredoctetoorder uint32 = destinoipDirecciónredoctetoorder
	if (destinoipDirecciónredoctetoorder & propio.SubnetMáscara) != (mensaje.origenipDirección & propio.SubnetMáscara) {
		siguientehopipDirecciónredoctetoorder = propio.Gatewayip
	}

	var enviardatosPuntero = uintptr(Pointer(&buffer1_2))
	ipconsola.MUnsignedinteger32Imprimir(siguientehopipDirecciónredoctetoorder)

	var ethernettipobe = Unsignedinteger16r(0x0800)
	efhandler.TramaEnviar(propio.arpprovider.Resolver(siguientehopipDirecciónredoctetoorder), ethernettipobe, enviardatosPuntero, uint32(ipTamaño)+uint32(tamaño))

}
func (propio *TProveedor_del_protocolo_de_red_interconectada) Sumadeverificación(pdatos *[4096]uint16, duraciónEntradabytes uint32) uint16 {
	var datos [4096]uint16 = *pdatos
	var temporary uint32 = 0
	var datosbytes [4096]byte = *(*([4096]byte))(Pointer(&datos))
	if (duraciónEntradabytes % 2) != 0 {
		temporary += uint32(uint16(datosbytes[duraciónEntradabytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (propio *TProveedor_del_protocolo_de_red_interconectada) GetipDirección() uint64 {
	return efhandler.GetipDirección()
}
