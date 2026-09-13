package amdam79c973

import . "unsafe"
import . "katkestus"
import . "console"
import . "port"
import . "pci"

var võrkKaardimängudconsole TConsole = TConsole{}

type TInitializationKast struct {
	rEŽIIM		uint16
	arvSaadabuffer	uint8
	arvrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferKirjeldusaddress	uintptr
	saadabufferKirjeldusaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	lipud		uint32
	lipud2		uint32
	saadaval	uint32
}

type IRawdatahandler interface {
	Seesrawdatareceive(dataKursor uintptr, suurus int) bool
	Saada(dataKursor uintptr, suurus uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (ise *TRawdatahandler) Määrabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (ise *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (ise *TRawdatahandler) Seesrawdatareceive(dataKursor uintptr, suurus int) bool {
	võrkKaardimängudconsole.MPrindixy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (ise *TRawdatahandler) Saada(dataKursor uintptr, suurus uint32) {
	võrkKaardimängudconsole.MPrindixy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Saada(dataKursor, suurus)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var lähtestaport uint16
var busJuhtregisterdataport uint16

var initKast TInitializationKast

var saadabufferKirjeldus [8]TBufferdescriptor
var saadabufferKirjeldusMälu [2048 + 15]byte
var saadabuffer [2*1024 + 15][8]uint8
var käesolevSaadabuffer uint8

var recvbufferKirjeldus [8]TBufferdescriptor
var recvbufferKirjeldusMälu [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var käesolevrecvbuffer uint8
var funcVäärtus func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TKatkestushandler
	seadedescriptor	TPeripheralcomponentinterconnectSeadedescriptor
	katkestus	*TKatkestusmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (ise *Tamdam79c973) Initdriver(katkestus *TKatkestusmanager, seadedescriptor TPeripheralcomponentinterconnectSeadedescriptor, handler IRawdatahandler) {

	ise.seadedescriptor = seadedescriptor

	funcVäärtus = (*Tamdam79c973).HandleKatkestus
	var address uintptr
	address = uintptr(Pointer(&funcVäärtus))

	ise.Init(uint8(0x20+seadedescriptor.Katkestus), uintptr(Pointer(katkestus)), address)

	Macaddress0port = uint16(seadedescriptor.Portbase)
	Macaddress2port = uint16(seadedescriptor.Portbase) + 0x02
	Macaddress4port = uint16(seadedescriptor.Portbase) + 0x04
	registerdataport = uint16(seadedescriptor.Portbase) + 0x10
	registeraddressport = uint16(seadedescriptor.Portbase) + 0x12
	lähtestaport = uint16(seadedescriptor.Portbase) + 0x14
	busJuhtregisterdataport = uint16(seadedescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	käesolevSaadabuffer = 0
	käesolevrecvbuffer = 0

	var Mac0 uint64 = uint64(PortLugeminesõna(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortLugeminesõna(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortLugeminesõna(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortLugeminesõna(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortLugeminesõna(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortLugeminesõna(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MPrindixy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalPrindi(uint8(seadedescriptor.Katkestus))
	console_2.MPrindi(([]byte)("]"))
	console_2.MPrindi(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Prindi(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Prindi(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MPrindi(([]byte)("]"))

	PortKirjutaminesõna(registeraddressport, 20)
	PortKirjutaminesõna(busJuhtregisterdataport, 0x102)

	PortKirjutaminesõna(registeraddressport, 0)
	PortKirjutaminesõna(registerdataport, 0x04)

	initKast.rEŽIIM = 0x0000
	initKast.arvSaadabuffer = 3
	initKast.arvrecvbuffer = 3

	initKast.physicaladdress = Mac

	initKast.logicaladdress = 0

	saadabufferKirjeldus = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&saadabufferKirjeldusMälu)) + 15) & ^(uintptr)(0xF)))
	initKast.saadabufferKirjeldusaddress = uintptr(Pointer(&saadabufferKirjeldus))
	recvbufferKirjeldus = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferKirjeldusMälu)) + 15) & ^(uintptr)(0xF)))
	initKast.recvbufferKirjeldusaddress = uintptr(Pointer(&recvbufferKirjeldus))

	for i := 0; i < 8; i++ {
		saadabufferKirjeldus[i].address_2 = uint32((uintptr(Pointer(&saadabuffer[i])) + 15) & ^(uintptr(0xF)))
		saadabufferKirjeldus[i].lipud = 0x7FF | 0xF000
		saadabufferKirjeldus[i].lipud2 = 0
		saadabufferKirjeldus[i].saadaval = 0

		recvbufferKirjeldus[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferKirjeldus[i].lipud = 0xF7FF | 0x80000000

	}

	PortKirjutaminesõna(registeraddressport, 1)
	PortKirjutaminesõna(registerdataport, uint16(uintptr(Pointer(&initKast))&0xFFFF))

	PortKirjutaminesõna(registeraddressport, 2)
	PortKirjutaminesõna(registerdataport, uint16((uintptr(Pointer(&initKast))>>16)&0xFFFF))

}
func (ise *Tamdam79c973) Lülitasisse() {
	PortKirjutaminesõna(registeraddressport, 0)
	PortKirjutaminesõna(registerdataport, 0x41)

	PortKirjutaminesõna(registeraddressport, 4)
	temporary := PortLugeminesõna(registerdataport)
	PortKirjutaminesõna(registeraddressport, 4)
	PortKirjutaminesõna(registerdataport, temporary|0xC00)

	PortKirjutaminesõna(registeraddressport, 0)
	PortKirjutaminesõna(registerdataport, 0x42)

}
func (ise *Tamdam79c973) Lähtesta() int {
	PortLugeminesõna(lähtestaport)
	PortKirjutaminesõna(lähtestaport, 0)
	return 10
}

var count uint16 = 0

func (ise *Tamdam79c973) HandleKatkestus(esp uint32) uint32 {

	PortKirjutaminesõna(registeraddressport, 0)
	temporary := uint32(PortLugeminesõna(registerdataport))
	console_2.MPrindi(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Prindi(esp)
	console_2.MPrindi(([]byte)(":"))
	console_2.MUnsignedinteger32Prindi(temporary)
	console_2.MPrindi(([]byte)(":"))
	console_2.MUnsignedinteger16Prindi(count)
	count++
	console_2.MPrindi(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MPrindi(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MPrindi(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MPrindi(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MPrindi(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MPrindi(([]byte)("am79c973 data received"))
		ise.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MPrindi(([]byte)("am79c973 data sent"))
	}

	PortKirjutaminesõna(registeraddressport, 0)
	PortKirjutaminesõna(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MPrindi(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (ise *Tamdam79c973) Saada(dataKursor uintptr, suurus uint32) {
	var saadadescriptor uint16 = uint16(käesolevSaadabuffer)
	käesolevSaadabuffer = 0

	if suurus > 1518 {
		suurus = 1518
	}

	var aLLIKAS_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursor))
	var sihtfail_2 uint32 = saadabufferKirjeldus[saadadescriptor].address_2 + suurus - 1

	for i := 0; i < int(suurus); i++ {

		*(*byte)(Pointer(uintptr(sihtfail_2))) = aLLIKAS_2[int(suurus)-i-1]

		sihtfail_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKursor))
	console_2.MPrindixy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalPrindi(data[i])
		console_2.MPrindi(([]byte)(":"))
	}
	console_2.MPrindi(([]byte)("\n"))

	saadabufferKirjeldus[saadadescriptor].saadaval = 0
	saadabufferKirjeldus[saadadescriptor].lipud2 = 0
	saadabufferKirjeldus[saadadescriptor].lipud = 0x8300F000 | uint32((-suurus)&0xFFF)

	PortKirjutaminesõna(registeraddressport, 0)
	PortKirjutaminesõna(registerdataport, 0x48)

}
func (ise *Tamdam79c973) Receive() {
	console_2.MPrindi(([]byte)(":"))
	console_2.MUnsignedinteger32Prindi(uint32(uintptr(Pointer(&saadabuffer))))
	console_2.MPrindi(([]byte)(":"))
	console_2.MHexadecimalPrindi(saadabuffer[0][0])
	console_2.MHexadecimalPrindi(saadabuffer[0][1])
	console_2.MPrindi(([]byte)(":"))
	käesolevrecvbuffer = 0

	for ; (recvbufferKirjeldus[käesolevrecvbuffer].lipud & 0x80000000) == 0; käesolevrecvbuffer = (käesolevrecvbuffer + 1) % 8 {

		if !(recvbufferKirjeldus[käesolevrecvbuffer].lipud&0x40000000 != 0) && ((recvbufferKirjeldus[käesolevrecvbuffer].lipud & 0x03000000) == 0x03000000) {
			var suurus uint32 = recvbufferKirjeldus[käesolevrecvbuffer].lipud & 0xFFF
			if suurus > 64 {
				suurus -= 4
			}

			console_2.MPrindi([]byte(" size : ["))
			console_2.MUnsignedinteger32Prindi(suurus)
			console_2.MPrindi([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferKirjeldus[käesolevrecvbuffer].address_2)))
			var kursor uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Seesrawdatareceive(kursor, int(suurus)) {

					console_2.MPrindixy(([]byte)("self.Send"), 0, 22)

					ise.Saada(kursor, suurus)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalPrindi(buffer_2[i])
				console_2.MPrindi([]byte(":"))
			}

		}
		recvbufferKirjeldus[käesolevrecvbuffer].lipud2 = 0
		recvbufferKirjeldus[käesolevrecvbuffer].lipud = 0x8000F7FF
	}
}
func (ise *Tamdam79c973) Määrahandler(handler *TRawdatahandler) {
	ise.handler = handler
}
func (ise *Tamdam79c973) Getmacaddress() uint64 {

	return initKast.physicaladdress
}
func (ise *Tamdam79c973) Määraipaddress(ip uint64) {
	initKast.logicaladdress = ip
}
func (ise *Tamdam79c973) Getipaddress() uint64 {
	return initKast.logicaladdress
}
