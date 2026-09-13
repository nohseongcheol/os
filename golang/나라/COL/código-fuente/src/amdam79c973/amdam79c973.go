package amdam79c973

import . "unsafe"
import . "interrupción"
import . "consola"
import . "puerto"
import . "pci"

var redCartasconsola TConsola = TConsola{}

type TInitializationBloque struct {
	modo			uint16
	númeroEnviarbuffer	uint8
	númerorecvbuffer	uint8

	físicoDirección	uint64

	lógicoDirección				uint64
	recvbufferDescripciónDirección		uintptr
	enviarbufferDescripciónDirección	uintptr
}
type TBufferdescriptor struct {
	dirección_2	uint32
	banderas	uint32
	banderas2	uint32
	disponible	uint32
}

type IRawdatoshandler interface {
	Alrawdatosreceive(datosPuntero uintptr, tamaño int) bool
	Enviar(datosPuntero uintptr, tamaño uint32)
}

var rawdatosbackend Tamdam79c973

type TRawdatoshandler struct {
}

func (propio *TRawdatoshandler) Establecerbackend(backend Tamdam79c973) {

	rawdatosbackend = backend
}
func (propio *TRawdatoshandler) Getbackend() Tamdam79c973 {
	return rawdatosbackend
}
func (propio *TRawdatoshandler) Alrawdatosreceive(datosPuntero uintptr, tamaño int) bool {
	redCartasconsola.MImprimirxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (propio *TRawdatoshandler) Enviar(datosPuntero uintptr, tamaño uint32) {
	redCartasconsola.MImprimirxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatosbackend.Enviar(datosPuntero, tamaño)
}

var MacDirección0puerto uint16
var MacDirección2puerto uint16
var MacDirección4puerto uint16
var registrodatospuerto uint16
var registroDirecciónpuerto uint16
var reiniciarpuerto uint16
var buscontrolregistrodatospuerto uint16

var initBloque TInitializationBloque

var enviarbufferDescripción [8]TBufferdescriptor
var enviarbufferDescripciónmemoria [2048 + 15]byte
var enviarbuffer [2*1024 + 15][8]uint8
var actualEnviarbuffer uint8

var recvbufferDescripción [8]TBufferdescriptor
var recvbufferDescripciónmemoria [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var actualrecvbuffer uint8
var funcValor func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupciónhandler
	dispositivodescriptor	TPeripheralcomponentinterconnectDispositivodescriptor
	interrupción		*TInterrupcióngestor
	handler			*TRawdatoshandler
}

var consola_2 TConsola = TConsola{}
var irawdatoshandler IRawdatoshandler

func (propio *Tamdam79c973) Initcontrolador(interrupción *TInterrupcióngestor, dispositivodescriptor TPeripheralcomponentinterconnectDispositivodescriptor, handler IRawdatoshandler) {

	propio.dispositivodescriptor = dispositivodescriptor

	funcValor = (*Tamdam79c973).Manijainterrupción
	var dirección uintptr
	dirección = uintptr(Pointer(&funcValor))

	propio.Init(uint8(0x20+dispositivodescriptor.Interrupción), uintptr(Pointer(interrupción)), dirección)

	MacDirección0puerto = uint16(dispositivodescriptor.Puertobase)
	MacDirección2puerto = uint16(dispositivodescriptor.Puertobase) + 0x02
	MacDirección4puerto = uint16(dispositivodescriptor.Puertobase) + 0x04
	registrodatospuerto = uint16(dispositivodescriptor.Puertobase) + 0x10
	registroDirecciónpuerto = uint16(dispositivodescriptor.Puertobase) + 0x12
	reiniciarpuerto = uint16(dispositivodescriptor.Puertobase) + 0x14
	buscontrolregistrodatospuerto = uint16(dispositivodescriptor.Puertobase) + 0x16

	irawdatoshandler = &TRawdatoshandler{}
	if handler != nil {
		irawdatoshandler = handler
	}

	actualEnviarbuffer = 0
	actualrecvbuffer = 0

	var Mac0 uint64 = uint64(Puertoleerpalabra(MacDirección0puerto) % 256)
	var Mac1 uint64 = uint64(Puertoleerpalabra(MacDirección0puerto) / 256)
	var Mac2 uint64 = uint64(Puertoleerpalabra(MacDirección2puerto) % 256)
	var Mac3 uint64 = uint64(Puertoleerpalabra(MacDirección2puerto) / 256)
	var Mac4 uint64 = uint64(Puertoleerpalabra(MacDirección4puerto) % 256)
	var Mac5 uint64 = uint64(Puertoleerpalabra(MacDirección4puerto) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macDirección uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	consola_2.MImprimirxy(([]byte)("[interrupt num : "), 0, 13)
	consola_2.MHexadecimalImprimir(uint8(dispositivodescriptor.Interrupción))
	consola_2.MImprimir(([]byte)("]"))
	consola_2.MImprimir(([]byte)("[mac address : "))
	consola_2.MUnsignedinteger16Imprimir(uint16(macDirección >> 32))
	consola_2.MUnsignedinteger32Imprimir(uint32(macDirección & 0x00000000FFFFFFFF))
	consola_2.MImprimir(([]byte)("]"))

	Puertoescribirpalabra(registroDirecciónpuerto, 20)
	Puertoescribirpalabra(buscontrolregistrodatospuerto, 0x102)

	Puertoescribirpalabra(registroDirecciónpuerto, 0)
	Puertoescribirpalabra(registrodatospuerto, 0x04)

	initBloque.modo = 0x0000
	initBloque.númeroEnviarbuffer = 3
	initBloque.númerorecvbuffer = 3

	initBloque.físicoDirección = Mac

	initBloque.lógicoDirección = 0

	enviarbufferDescripción = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&enviarbufferDescripciónmemoria)) + 15) & ^(uintptr)(0xF)))
	initBloque.enviarbufferDescripciónDirección = uintptr(Pointer(&enviarbufferDescripción))
	recvbufferDescripción = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferDescripciónmemoria)) + 15) & ^(uintptr)(0xF)))
	initBloque.recvbufferDescripciónDirección = uintptr(Pointer(&recvbufferDescripción))

	for i := 0; i < 8; i++ {
		enviarbufferDescripción[i].dirección_2 = uint32((uintptr(Pointer(&enviarbuffer[i])) + 15) & ^(uintptr(0xF)))
		enviarbufferDescripción[i].banderas = 0x7FF | 0xF000
		enviarbufferDescripción[i].banderas2 = 0
		enviarbufferDescripción[i].disponible = 0

		recvbufferDescripción[i].dirección_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferDescripción[i].banderas = 0xF7FF | 0x80000000

	}

	Puertoescribirpalabra(registroDirecciónpuerto, 1)
	Puertoescribirpalabra(registrodatospuerto, uint16(uintptr(Pointer(&initBloque))&0xFFFF))

	Puertoescribirpalabra(registroDirecciónpuerto, 2)
	Puertoescribirpalabra(registrodatospuerto, uint16((uintptr(Pointer(&initBloque))>>16)&0xFFFF))

}
func (propio *Tamdam79c973) Activar() {
	Puertoescribirpalabra(registroDirecciónpuerto, 0)
	Puertoescribirpalabra(registrodatospuerto, 0x41)

	Puertoescribirpalabra(registroDirecciónpuerto, 4)
	temporary := Puertoleerpalabra(registrodatospuerto)
	Puertoescribirpalabra(registroDirecciónpuerto, 4)
	Puertoescribirpalabra(registrodatospuerto, temporary|0xC00)

	Puertoescribirpalabra(registroDirecciónpuerto, 0)
	Puertoescribirpalabra(registrodatospuerto, 0x42)

}
func (propio *Tamdam79c973) Reiniciar() int {
	Puertoleerpalabra(reiniciarpuerto)
	Puertoescribirpalabra(reiniciarpuerto, 0)
	return 10
}

var recuento uint16 = 0

func (propio *Tamdam79c973) Manijainterrupción(esp uint32) uint32 {

	Puertoescribirpalabra(registroDirecciónpuerto, 0)
	temporary := uint32(Puertoleerpalabra(registrodatospuerto))
	consola_2.MImprimir(([]byte)("interrupt("))
	consola_2.MUnsignedinteger32Imprimir(esp)
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimir(temporary)
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MUnsignedinteger16Imprimir(recuento)
	recuento++
	consola_2.MImprimir(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		consola_2.MImprimir(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		consola_2.MImprimir(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		consola_2.MImprimir(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		consola_2.MImprimir(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		consola_2.MImprimir(([]byte)("am79c973 data received"))
		propio.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		consola_2.MImprimir(([]byte)("am79c973 data sent"))
	}

	Puertoescribirpalabra(registroDirecciónpuerto, 0)
	Puertoescribirpalabra(registrodatospuerto, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		consola_2.MImprimir(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (propio *Tamdam79c973) Enviar(datosPuntero uintptr, tamaño uint32) {
	var enviardescriptor uint16 = uint16(actualEnviarbuffer)
	actualEnviarbuffer = 0

	if tamaño > 1518 {
		tamaño = 1518
	}

	var origen_2 [4096]byte = *(*([4096]byte))(Pointer(datosPuntero))
	var destino_2 uint32 = enviarbufferDescripción[enviardescriptor].dirección_2 + tamaño - 1

	for i := 0; i < int(tamaño); i++ {

		*(*byte)(Pointer(uintptr(destino_2))) = origen_2[int(tamaño)-i-1]

		destino_2--
	}

	var datos [4096]byte = *(*([4096]byte))(Pointer(datosPuntero))
	consola_2.MImprimirxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		consola_2.MHexadecimalImprimir(datos[i])
		consola_2.MImprimir(([]byte)(":"))
	}
	consola_2.MImprimir(([]byte)("\n"))

	enviarbufferDescripción[enviardescriptor].disponible = 0
	enviarbufferDescripción[enviardescriptor].banderas2 = 0
	enviarbufferDescripción[enviardescriptor].banderas = 0x8300F000 | uint32((-tamaño)&0xFFF)

	Puertoescribirpalabra(registroDirecciónpuerto, 0)
	Puertoescribirpalabra(registrodatospuerto, 0x48)

}
func (propio *Tamdam79c973) Receive() {
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(&enviarbuffer))))
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MHexadecimalImprimir(enviarbuffer[0][0])
	consola_2.MHexadecimalImprimir(enviarbuffer[0][1])
	consola_2.MImprimir(([]byte)(":"))
	actualrecvbuffer = 0

	for ; (recvbufferDescripción[actualrecvbuffer].banderas & 0x80000000) == 0; actualrecvbuffer = (actualrecvbuffer + 1) % 8 {

		if !(recvbufferDescripción[actualrecvbuffer].banderas&0x40000000 != 0) && ((recvbufferDescripción[actualrecvbuffer].banderas & 0x03000000) == 0x03000000) {
			var tamaño uint32 = recvbufferDescripción[actualrecvbuffer].banderas & 0xFFF
			if tamaño > 64 {
				tamaño -= 4
			}

			consola_2.MImprimir([]byte(" size : ["))
			consola_2.MUnsignedinteger32Imprimir(tamaño)
			consola_2.MImprimir([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferDescripción[actualrecvbuffer].dirección_2)))
			var referencia_de_memoria uintptr = uintptr(Pointer(&buffer_2))
			if irawdatoshandler != nil {
				if irawdatoshandler.Alrawdatosreceive(referencia_de_memoria, int(tamaño)) {

					consola_2.MImprimirxy(([]byte)("self.Send"), 0, 22)

					propio.Enviar(referencia_de_memoria, tamaño)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				consola_2.MHexadecimalImprimir(buffer_2[i])
				consola_2.MImprimir([]byte(":"))
			}

		}
		recvbufferDescripción[actualrecvbuffer].banderas2 = 0
		recvbufferDescripción[actualrecvbuffer].banderas = 0x8000F7FF
	}
}
func (propio *Tamdam79c973) Establecerhandler(handler *TRawdatoshandler) {
	propio.handler = handler
}
func (propio *Tamdam79c973) GetmacDirección() uint64 {

	return initBloque.físicoDirección
}
func (propio *Tamdam79c973) EstableceripDirección(ip uint64) {
	initBloque.lógicoDirección = ip
}
func (propio *Tamdam79c973) GetipDirección() uint64 {
	return initBloque.lógicoDirección
}
