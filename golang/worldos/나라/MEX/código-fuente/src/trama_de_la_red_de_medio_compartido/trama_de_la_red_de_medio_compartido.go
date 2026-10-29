/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package trama_de_la_red_de_medio_compartido

import . "consola"

import . "amdam79c973"
import . "unsafe"
import . "utilidad"

var ethernetconsola TConsola = TConsola{}

type TEthernettramaencabezadobuffer struct {
	destinomacbe	[6]byte
	origenmacbe	[6]byte
	ethernettipobe	[2]byte
}

var tramaencabezadoTamaño int = 14

type TCabecera_de_trama_de_red_de_medio_compartido struct {
	destinomacbe	uint64
	origenmacbe	uint64
	ethernettipobe	uint16
}

func (propio *TCabecera_de_trama_de_red_de_medio_compartido) Init(buffer_2 TEthernettramaencabezadobuffer) {
	propio.destinomacbe = (Matriztounsignedinteger48(buffer_2.destinomacbe))
	propio.origenmacbe = (Matriztounsignedinteger48(buffer_2.origenmacbe))
	propio.ethernettipobe = (Matriztounsignedinteger16(buffer_2.ethernettipobe))

}
func (propio *TCabecera_de_trama_de_red_de_medio_compartido) Establecerbuffer(buffer_2 *TEthernettramaencabezadobuffer) {
	buffer_2.destinomacbe = Unsignedinteger48tomatriz(Unsignedinteger48r(propio.destinomacbe))
	buffer_2.origenmacbe = Unsignedinteger48tomatriz(Unsignedinteger48r(propio.origenmacbe))
	buffer_2.ethernettipobe = Unsignedinteger16tomatriz(Unsignedinteger16r(propio.ethernettipobe))
}

type IEthernettramahandler interface {
	Init(backend TProveedor_de_tramas_de_red_de_medio_compartido)
	Establecerhandler(handler IEthernettramahandler, ethernettipo uint16)
	Ethernettramareceivewhen(datosPuntero uintptr, tamaño int) bool
	Enviar(destinomacbe uint64, datosPuntero uintptr, tamaño uint32)
	TramaEnviar(destinomacbe uint64, ethernettipobe uint16, datosPuntero uintptr, tamaño uint32)
	Providerget() TProveedor_de_tramas_de_red_de_medio_compartido
	GetmacDirección() uint64
	GetipDirección() uint64
}

type TEthernettramahandler struct {
}

var trama TCabecera_de_trama_de_red_de_medio_compartido
var Backend TProveedor_de_tramas_de_red_de_medio_compartido
var handler_2 [65535]IEthernettramahandler
var efhandler *TEthernettramahandler = nil

func (propio *TEthernettramahandler) Init(backend TProveedor_de_tramas_de_red_de_medio_compartido) {
	Backend = backend
}

func (propio *TEthernettramahandler) Establecerhandler(handler IEthernettramahandler, pethernettipo uint16) {
	handler_2[pethernettipo] = handler
}
func (propio *TEthernettramahandler) Establecerbackend(backend TProveedor_de_tramas_de_red_de_medio_compartido) {
	Backend = backend
}
func (propio *TEthernettramahandler) Getbackend() TProveedor_de_tramas_de_red_de_medio_compartido {
	return Backend
}
func (propio *TEthernettramahandler) Ethernettramareceivewhen(datosPuntero uintptr, tamaño int) bool {
	ethernetconsola.MImprimir(([]byte)("OnEtherFrameReceived"))
	return false
}
func (propio *TEthernettramahandler) Enviar(destinomacbe uint64, datosPuntero uintptr, tamaño uint32) {
	Backend.TramaEnviar(destinomacbe, trama.ethernettipobe, datosPuntero, tamaño)
}
func (propio *TEthernettramahandler) TramaEnviar(destinomacbe uint64, ethernettipobe uint16, datosPuntero uintptr, tamaño uint32) {
	Backend.TramaEnviar(destinomacbe, ethernettipobe, datosPuntero, tamaño)
}
func (propio *TEthernettramahandler) GetmacDirección() uint64 {
	return Backend.GetmacDirección()
}
func (propio *TEthernettramahandler) GetipDirección() uint64 {
	return Backend.GetipDirección()
}
func (propio *TEthernettramahandler) Providerget() TProveedor_de_tramas_de_red_de_medio_compartido {
	return Backend
}

type TEthernettramarawdatoshandler struct {
	TRawdatoshandler
}

var provider TProveedor_de_tramas_de_red_de_medio_compartido

func (propio *TEthernettramarawdatoshandler) Init(pprovider TProveedor_de_tramas_de_red_de_medio_compartido, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (propio *TEthernettramarawdatoshandler) Alrawdatosreceive(datosPuntero uintptr, tamaño int) bool {
	return provider.Alrawdatosreceive(datosPuntero, tamaño)
}
func (propio *TEthernettramarawdatoshandler) Enviar(datosPuntero uintptr, tamaño uint32) {
	provider.Enviar(datosPuntero, tamaño)
}
func (propio *TEthernettramarawdatoshandler) GetmacDirección() uint64 {
	return provider.GetmacDirección()
}
func (propio *TEthernettramarawdatoshandler) GetipDirección() uint64 {
	return provider.GetipDirección()
}
func (propio *TEthernettramarawdatoshandler) Providerget() TProveedor_de_tramas_de_red_de_medio_compartido {
	return provider
}

type TProveedor_de_tramas_de_red_de_medio_compartido struct {
	redCartas	Tamdam79c973
	handler_2	[65565]IEthernettramahandler
}

func (propio *TProveedor_de_tramas_de_red_de_medio_compartido) Init(backend Tamdam79c973) {

	propio.redCartas = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		propio.handler_2[i] = nil
	}
}

var recuento uint16 = 0

func (propio *TProveedor_de_tramas_de_red_de_medio_compartido) Alrawdatosreceive(datosPuntero uintptr, tamaño int) bool {

	var buffer_2 *TEthernettramaencabezadobuffer = (*TEthernettramaencabezadobuffer)(Pointer(datosPuntero))
	var trama TCabecera_de_trama_de_red_de_medio_compartido = TCabecera_de_trama_de_red_de_medio_compartido{}
	trama.Init(*buffer_2)
	var reply bool = false

	if trama.destinomacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(trama.destinomacbe) == propio.GetmacDirección() {
		if handler_2[trama.ethernettipobe] != nil {
			ethernetconsola.MImprimir(([]byte)("provider\n"))

			var referencia_de_memoria uintptr = uintptr(Pointer(datosPuntero)) + uintptr(tramaencabezadoTamaño)
			reply = handler_2[trama.ethernettipobe].Ethernettramareceivewhen(referencia_de_memoria, tamaño-tramaencabezadoTamaño)

		}
	}

	if reply {
		trama.destinomacbe = trama.origenmacbe
		trama.origenmacbe = Unsignedinteger48r(propio.GetmacDirección())
		trama.Establecerbuffer(buffer_2)

	}

	ethernetconsola.MImprimirxy(([]byte)("spro["), 0, 1)
	ethernetconsola.MUnsignedinteger64Imprimir(trama.origenmacbe)
	ethernetconsola.MImprimir(([]byte)(":"))
	ethernetconsola.MUnsignedinteger64Imprimir(trama.destinomacbe)
	ethernetconsola.MImprimir(([]byte)(":]["))
	ethernetconsola.MUnsignedinteger64Imprimir(propio.GetmacDirección())
	ethernetconsola.MImprimir(([]byte)(":"))
	ethernetconsola.MUnsignedinteger16Imprimir(trama.ethernettipobe)
	ethernetconsola.MImprimir(([]byte)("]"))

	return reply

}
func (propio *TProveedor_de_tramas_de_red_de_medio_compartido) Enviar(datosPuntero uintptr, tamaño uint32) {
	propio.redCartas.Enviar(datosPuntero, tamaño)
}
func (propio *TProveedor_de_tramas_de_red_de_medio_compartido) TramaEnviar(destinomacbe uint64, ethernettipobe uint16, datosPuntero uintptr, tamaño uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernettramaencabezadobuffer = (*TEthernettramaencabezadobuffer)(Pointer(&buffer2_2))

	var trama TCabecera_de_trama_de_red_de_medio_compartido = TCabecera_de_trama_de_red_de_medio_compartido{}
	trama.Init(*buffer_2)

	trama.destinomacbe = Unsignedinteger48r(destinomacbe)
	trama.origenmacbe = Unsignedinteger48r(propio.redCartas.GetmacDirección())
	trama.ethernettipobe = Unsignedinteger16r(ethernettipobe)

	trama.Establecerbuffer(buffer_2)
	var origen_2 [4096]byte = *(*([4096]byte))(Pointer(datosPuntero))

	var i uint32 = 0
	for i = 0; i < tamaño; i++ {
		buffer2_2[uint32(tramaencabezadoTamaño)+i] = origen_2[i]

	}

	var referencia_de_memoria uintptr = uintptr(Pointer(&buffer2_2))

	propio.redCartas.Enviar(referencia_de_memoria, tamaño+uint32(tramaencabezadoTamaño))

}
func (propio *TProveedor_de_tramas_de_red_de_medio_compartido) GetmacDirección() uint64 {
	return propio.redCartas.GetmacDirección()
}
func (propio *TProveedor_de_tramas_de_red_de_medio_compartido) GetipDirección() uint64 {
	return propio.redCartas.GetipDirección()
}
