package amdam79c973

import . "unsafe"
import . "interrupció"
import . "consola"
import . "port"
import . "pci"

var xarxaCartesConsola TConsola = TConsola{}

type TInitializationBloc struct {
	mode			uint16
	nombreEnviabuffer	uint8
	nombrerecvbuffer	uint8

	physicalAdreça	uint64

	logicalAdreça			uint64
	recvbufferDescripcióAdreça	uintptr
	enviabufferDescripcióAdreça	uintptr
}
type TBufferdescriptor struct {
	adreça_2	uint32
	senyaladors	uint32
	senyaladors2	uint32
	disponible	uint32
}

type IRawdatahandler interface {
	Engegatrawdatareceive(dataPunter uintptr, mida int) bool
	Envia(dataPunter uintptr, mida uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (unmateix *TRawdatahandler) Estableixbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (unmateix *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (unmateix *TRawdatahandler) Engegatrawdatareceive(dataPunter uintptr, mida int) bool {
	xarxaCartesConsola.MImprimeixxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (unmateix *TRawdatahandler) Envia(dataPunter uintptr, mida uint32) {
	xarxaCartesConsola.MImprimeixxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Envia(dataPunter, mida)
}

var MacAdreça0port uint16
var MacAdreça2port uint16
var MacAdreça4port uint16
var registerdataport uint16
var registerAdreçaport uint16
var restableixport uint16
var buscontrolregisterdataport uint16

var initBloc TInitializationBloc

var enviabufferDescripció [8]TBufferdescriptor
var enviabufferDescripcióMemòria [2048 + 15]byte
var enviabuffer [2*1024 + 15][8]uint8
var actualEnviabuffer uint8

var recvbufferDescripció [8]TBufferdescriptor
var recvbufferDescripcióMemòria [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var actualrecvbuffer uint8
var funcValor func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupcióhandler
	dispositiudescriptor	TPeripheralcomponentinterconnectDispositiudescriptor
	interrupció		*TInterrupciómanager
	handler			*TRawdatahandler
}

var consola_2 TConsola = TConsola{}
var irawdatahandler IRawdatahandler

func (unmateix *Tamdam79c973) Initdriver(interrupció *TInterrupciómanager, dispositiudescriptor TPeripheralcomponentinterconnectDispositiudescriptor, handler IRawdatahandler) {

	unmateix.dispositiudescriptor = dispositiudescriptor

	funcValor = (*Tamdam79c973).GestorInterrupció
	var adreça uintptr
	adreça = uintptr(Pointer(&funcValor))

	unmateix.Init(uint8(0x20+dispositiudescriptor.Interrupció), uintptr(Pointer(interrupció)), adreça)

	MacAdreça0port = uint16(dispositiudescriptor.Portbase)
	MacAdreça2port = uint16(dispositiudescriptor.Portbase) + 0x02
	MacAdreça4port = uint16(dispositiudescriptor.Portbase) + 0x04
	registerdataport = uint16(dispositiudescriptor.Portbase) + 0x10
	registerAdreçaport = uint16(dispositiudescriptor.Portbase) + 0x12
	restableixport = uint16(dispositiudescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(dispositiudescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	actualEnviabuffer = 0
	actualrecvbuffer = 0

	var Mac0 uint64 = uint64(PortLecturaparaula(MacAdreça0port) % 256)
	var Mac1 uint64 = uint64(PortLecturaparaula(MacAdreça0port) / 256)
	var Mac2 uint64 = uint64(PortLecturaparaula(MacAdreça2port) % 256)
	var Mac3 uint64 = uint64(PortLecturaparaula(MacAdreça2port) / 256)
	var Mac4 uint64 = uint64(PortLecturaparaula(MacAdreça4port) % 256)
	var Mac5 uint64 = uint64(PortLecturaparaula(MacAdreça4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macAdreça uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	consola_2.MImprimeixxy(([]byte)("[interrupt num : "), 0, 13)
	consola_2.MHexadecimalImprimeix(uint8(dispositiudescriptor.Interrupció))
	consola_2.MImprimeix(([]byte)("]"))
	consola_2.MImprimeix(([]byte)("[mac address : "))
	consola_2.MUnsignedinteger16Imprimeix(uint16(macAdreça >> 32))
	consola_2.MUnsignedinteger32Imprimeix(uint32(macAdreça & 0x00000000FFFFFFFF))
	consola_2.MImprimeix(([]byte)("]"))

	PortEscripturaparaula(registerAdreçaport, 20)
	PortEscripturaparaula(buscontrolregisterdataport, 0x102)

	PortEscripturaparaula(registerAdreçaport, 0)
	PortEscripturaparaula(registerdataport, 0x04)

	initBloc.mode = 0x0000
	initBloc.nombreEnviabuffer = 3
	initBloc.nombrerecvbuffer = 3

	initBloc.physicalAdreça = Mac

	initBloc.logicalAdreça = 0

	enviabufferDescripció = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&enviabufferDescripcióMemòria)) + 15) & ^(uintptr)(0xF)))
	initBloc.enviabufferDescripcióAdreça = uintptr(Pointer(&enviabufferDescripció))
	recvbufferDescripció = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferDescripcióMemòria)) + 15) & ^(uintptr)(0xF)))
	initBloc.recvbufferDescripcióAdreça = uintptr(Pointer(&recvbufferDescripció))

	for i := 0; i < 8; i++ {
		enviabufferDescripció[i].adreça_2 = uint32((uintptr(Pointer(&enviabuffer[i])) + 15) & ^(uintptr(0xF)))
		enviabufferDescripció[i].senyaladors = 0x7FF | 0xF000
		enviabufferDescripció[i].senyaladors2 = 0
		enviabufferDescripció[i].disponible = 0

		recvbufferDescripció[i].adreça_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferDescripció[i].senyaladors = 0xF7FF | 0x80000000

	}

	PortEscripturaparaula(registerAdreçaport, 1)
	PortEscripturaparaula(registerdataport, uint16(uintptr(Pointer(&initBloc))&0xFFFF))

	PortEscripturaparaula(registerAdreçaport, 2)
	PortEscripturaparaula(registerdataport, uint16((uintptr(Pointer(&initBloc))>>16)&0xFFFF))

}
func (unmateix *Tamdam79c973) Activa() {
	PortEscripturaparaula(registerAdreçaport, 0)
	PortEscripturaparaula(registerdataport, 0x41)

	PortEscripturaparaula(registerAdreçaport, 4)
	temporary := PortLecturaparaula(registerdataport)
	PortEscripturaparaula(registerAdreçaport, 4)
	PortEscripturaparaula(registerdataport, temporary|0xC00)

	PortEscripturaparaula(registerAdreçaport, 0)
	PortEscripturaparaula(registerdataport, 0x42)

}
func (unmateix *Tamdam79c973) Restableix() int {
	PortLecturaparaula(restableixport)
	PortEscripturaparaula(restableixport, 0)
	return 10
}

var recompte uint16 = 0

func (unmateix *Tamdam79c973) GestorInterrupció(esp uint32) uint32 {

	PortEscripturaparaula(registerAdreçaport, 0)
	temporary := uint32(PortLecturaparaula(registerdataport))
	consola_2.MImprimeix(([]byte)("interrupt("))
	consola_2.MUnsignedinteger32Imprimeix(esp)
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimeix(temporary)
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MUnsignedinteger16Imprimeix(recompte)
	recompte++
	consola_2.MImprimeix(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		consola_2.MImprimeix(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		consola_2.MImprimeix(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		consola_2.MImprimeix(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		consola_2.MImprimeix(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		consola_2.MImprimeix(([]byte)("am79c973 data received"))
		unmateix.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		consola_2.MImprimeix(([]byte)("am79c973 data sent"))
	}

	PortEscripturaparaula(registerAdreçaport, 0)
	PortEscripturaparaula(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		consola_2.MImprimeix(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (unmateix *Tamdam79c973) Envia(dataPunter uintptr, mida uint32) {
	var enviadescriptor uint16 = uint16(actualEnviabuffer)
	actualEnviabuffer = 0

	if mida > 1518 {
		mida = 1518
	}

	var origen_2 [4096]byte = *(*([4096]byte))(Pointer(dataPunter))
	var destinació_2 uint32 = enviabufferDescripció[enviadescriptor].adreça_2 + mida - 1

	for i := 0; i < int(mida); i++ {

		*(*byte)(Pointer(uintptr(destinació_2))) = origen_2[int(mida)-i-1]

		destinació_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPunter))
	consola_2.MImprimeixxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		consola_2.MHexadecimalImprimeix(data[i])
		consola_2.MImprimeix(([]byte)(":"))
	}
	consola_2.MImprimeix(([]byte)("\n"))

	enviabufferDescripció[enviadescriptor].disponible = 0
	enviabufferDescripció[enviadescriptor].senyaladors2 = 0
	enviabufferDescripció[enviadescriptor].senyaladors = 0x8300F000 | uint32((-mida)&0xFFF)

	PortEscripturaparaula(registerAdreçaport, 0)
	PortEscripturaparaula(registerdataport, 0x48)

}
func (unmateix *Tamdam79c973) Receive() {
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimeix(uint32(uintptr(Pointer(&enviabuffer))))
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MHexadecimalImprimeix(enviabuffer[0][0])
	consola_2.MHexadecimalImprimeix(enviabuffer[0][1])
	consola_2.MImprimeix(([]byte)(":"))
	actualrecvbuffer = 0

	for ; (recvbufferDescripció[actualrecvbuffer].senyaladors & 0x80000000) == 0; actualrecvbuffer = (actualrecvbuffer + 1) % 8 {

		if !(recvbufferDescripció[actualrecvbuffer].senyaladors&0x40000000 != 0) && ((recvbufferDescripció[actualrecvbuffer].senyaladors & 0x03000000) == 0x03000000) {
			var mida uint32 = recvbufferDescripció[actualrecvbuffer].senyaladors & 0xFFF
			if mida > 64 {
				mida -= 4
			}

			consola_2.MImprimeix([]byte(" size : ["))
			consola_2.MUnsignedinteger32Imprimeix(mida)
			consola_2.MImprimeix([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferDescripció[actualrecvbuffer].adreça_2)))
			var punter uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Engegatrawdatareceive(punter, int(mida)) {

					consola_2.MImprimeixxy(([]byte)("self.Send"), 0, 22)

					unmateix.Envia(punter, mida)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				consola_2.MHexadecimalImprimeix(buffer_2[i])
				consola_2.MImprimeix([]byte(":"))
			}

		}
		recvbufferDescripció[actualrecvbuffer].senyaladors2 = 0
		recvbufferDescripció[actualrecvbuffer].senyaladors = 0x8000F7FF
	}
}
func (unmateix *Tamdam79c973) Estableixhandler(handler *TRawdatahandler) {
	unmateix.handler = handler
}
func (unmateix *Tamdam79c973) GetmacAdreça() uint64 {

	return initBloc.physicalAdreça
}
func (unmateix *Tamdam79c973) EstableixipAdreça(ip uint64) {
	initBloc.logicalAdreça = ip
}
func (unmateix *Tamdam79c973) GetipAdreça() uint64 {
	return initBloc.logicalAdreça
}
