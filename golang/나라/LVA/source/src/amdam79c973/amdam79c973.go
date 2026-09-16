/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "pārtraukums"
import . "console"
import . "ports"
import . "pci"

var tīklscardconsole TConsole = TConsole{}

type TInitializationBloks struct {
	režīms			uint16
	skaitlisSūtītbuffer	uint8
	skaitlisrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferAprakstsaddress	uintptr
	sūtītbufferAprakstsaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	karogi		uint32
	karogi2		uint32
	pieejams	uint32
}

type IRawdatahandler interface {
	Ieslēgtsrawdatareceive(dataKursors uintptr, izmērs int) bool
	Sūtīt(dataKursors uintptr, izmērs uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (pats *TRawdatahandler) Kopabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (pats *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (pats *TRawdatahandler) Ieslēgtsrawdatareceive(dataKursors uintptr, izmērs int) bool {
	tīklscardconsole.MDrukātxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (pats *TRawdatahandler) Sūtīt(dataKursors uintptr, izmērs uint32) {
	tīklscardconsole.MDrukātxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Sūtīt(dataKursors, izmērs)
}

var Macaddress0Ports uint16
var Macaddress2Ports uint16
var Macaddress4Ports uint16
var registerdataPorts uint16
var registeraddressPorts uint16
var pārstatītPorts uint16
var busCtrlregisterdataPorts uint16

var initBloks TInitializationBloks

var sūtītbufferApraksts [8]TBufferdescriptor
var sūtītbufferAprakstsAtmiņa [2048 + 15]byte
var sūtītbuffer [2*1024 + 15][8]uint8
var pašreizējaisSūtītbuffer uint8

var recvbufferApraksts [8]TBufferdescriptor
var recvbufferAprakstsAtmiņa [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var pašreizējaisrecvbuffer uint8
var funcVērtība func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPārtraukumshandler
	ierīcedescriptor	TPeripheralcomponentinterconnectIerīcedescriptor
	pārtraukums		*TPārtraukumsmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (pats *Tamdam79c973) Initdriver(pārtraukums *TPārtraukumsmanager, ierīcedescriptor TPeripheralcomponentinterconnectIerīcedescriptor, handler IRawdatahandler) {

	pats.ierīcedescriptor = ierīcedescriptor

	funcVērtība = (*Tamdam79c973).HandlePārtraukums
	var address uintptr
	address = uintptr(Pointer(&funcVērtība))

	pats.Init(uint8(0x20+ierīcedescriptor.Pārtraukums), uintptr(Pointer(pārtraukums)), address)

	Macaddress0Ports = uint16(ierīcedescriptor.Portsbase)
	Macaddress2Ports = uint16(ierīcedescriptor.Portsbase) + 0x02
	Macaddress4Ports = uint16(ierīcedescriptor.Portsbase) + 0x04
	registerdataPorts = uint16(ierīcedescriptor.Portsbase) + 0x10
	registeraddressPorts = uint16(ierīcedescriptor.Portsbase) + 0x12
	pārstatītPorts = uint16(ierīcedescriptor.Portsbase) + 0x14
	busCtrlregisterdataPorts = uint16(ierīcedescriptor.Portsbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	pašreizējaisSūtītbuffer = 0
	pašreizējaisrecvbuffer = 0

	var Mac0 uint64 = uint64(PortsLasītvārds(Macaddress0Ports) % 256)
	var Mac1 uint64 = uint64(PortsLasītvārds(Macaddress0Ports) / 256)
	var Mac2 uint64 = uint64(PortsLasītvārds(Macaddress2Ports) % 256)
	var Mac3 uint64 = uint64(PortsLasītvārds(Macaddress2Ports) / 256)
	var Mac4 uint64 = uint64(PortsLasītvārds(Macaddress4Ports) % 256)
	var Mac5 uint64 = uint64(PortsLasītvārds(Macaddress4Ports) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MDrukātxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalDrukāt(uint8(ierīcedescriptor.Pārtraukums))
	console_2.MDrukāt(([]byte)("]"))
	console_2.MDrukāt(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Drukāt(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Drukāt(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MDrukāt(([]byte)("]"))

	PortsRakstītvārds(registeraddressPorts, 20)
	PortsRakstītvārds(busCtrlregisterdataPorts, 0x102)

	PortsRakstītvārds(registeraddressPorts, 0)
	PortsRakstītvārds(registerdataPorts, 0x04)

	initBloks.režīms = 0x0000
	initBloks.skaitlisSūtītbuffer = 3
	initBloks.skaitlisrecvbuffer = 3

	initBloks.physicaladdress = Mac

	initBloks.logicaladdress = 0

	sūtītbufferApraksts = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sūtītbufferAprakstsAtmiņa)) + 15) & ^(uintptr)(0xF)))
	initBloks.sūtītbufferAprakstsaddress = uintptr(Pointer(&sūtītbufferApraksts))
	recvbufferApraksts = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferAprakstsAtmiņa)) + 15) & ^(uintptr)(0xF)))
	initBloks.recvbufferAprakstsaddress = uintptr(Pointer(&recvbufferApraksts))

	for i := 0; i < 8; i++ {
		sūtītbufferApraksts[i].address_2 = uint32((uintptr(Pointer(&sūtītbuffer[i])) + 15) & ^(uintptr(0xF)))
		sūtītbufferApraksts[i].karogi = 0x7FF | 0xF000
		sūtītbufferApraksts[i].karogi2 = 0
		sūtītbufferApraksts[i].pieejams = 0

		recvbufferApraksts[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferApraksts[i].karogi = 0xF7FF | 0x80000000

	}

	PortsRakstītvārds(registeraddressPorts, 1)
	PortsRakstītvārds(registerdataPorts, uint16(uintptr(Pointer(&initBloks))&0xFFFF))

	PortsRakstītvārds(registeraddressPorts, 2)
	PortsRakstītvārds(registerdataPorts, uint16((uintptr(Pointer(&initBloks))>>16)&0xFFFF))

}
func (pats *Tamdam79c973) Aktivizēt() {
	PortsRakstītvārds(registeraddressPorts, 0)
	PortsRakstītvārds(registerdataPorts, 0x41)

	PortsRakstītvārds(registeraddressPorts, 4)
	temporary := PortsLasītvārds(registerdataPorts)
	PortsRakstītvārds(registeraddressPorts, 4)
	PortsRakstītvārds(registerdataPorts, temporary|0xC00)

	PortsRakstītvārds(registeraddressPorts, 0)
	PortsRakstītvārds(registerdataPorts, 0x42)

}
func (pats *Tamdam79c973) Pārstatīt() int {
	PortsLasītvārds(pārstatītPorts)
	PortsRakstītvārds(pārstatītPorts, 0)
	return 10
}

var count uint16 = 0

func (pats *Tamdam79c973) HandlePārtraukums(esp uint32) uint32 {

	PortsRakstītvārds(registeraddressPorts, 0)
	temporary := uint32(PortsLasītvārds(registerdataPorts))
	console_2.MDrukāt(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Drukāt(esp)
	console_2.MDrukāt(([]byte)(":"))
	console_2.MUnsignedinteger32Drukāt(temporary)
	console_2.MDrukāt(([]byte)(":"))
	console_2.MUnsignedinteger16Drukāt(count)
	count++
	console_2.MDrukāt(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MDrukāt(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MDrukāt(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MDrukāt(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MDrukāt(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MDrukāt(([]byte)("am79c973 data received"))
		pats.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MDrukāt(([]byte)("am79c973 data sent"))
	}

	PortsRakstītvārds(registeraddressPorts, 0)
	PortsRakstītvārds(registerdataPorts, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MDrukāt(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (pats *Tamdam79c973) Sūtīt(dataKursors uintptr, izmērs uint32) {
	var sūtītdescriptor uint16 = uint16(pašreizējaisSūtītbuffer)
	pašreizējaisSūtītbuffer = 0

	if izmērs > 1518 {
		izmērs = 1518
	}

	var avots_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursors))
	var mērķis_2 uint32 = sūtītbufferApraksts[sūtītdescriptor].address_2 + izmērs - 1

	for i := 0; i < int(izmērs); i++ {

		*(*byte)(Pointer(uintptr(mērķis_2))) = avots_2[int(izmērs)-i-1]

		mērķis_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKursors))
	console_2.MDrukātxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalDrukāt(data[i])
		console_2.MDrukāt(([]byte)(":"))
	}
	console_2.MDrukāt(([]byte)("\n"))

	sūtītbufferApraksts[sūtītdescriptor].pieejams = 0
	sūtītbufferApraksts[sūtītdescriptor].karogi2 = 0
	sūtītbufferApraksts[sūtītdescriptor].karogi = 0x8300F000 | uint32((-izmērs)&0xFFF)

	PortsRakstītvārds(registeraddressPorts, 0)
	PortsRakstītvārds(registerdataPorts, 0x48)

}
func (pats *Tamdam79c973) Receive() {
	console_2.MDrukāt(([]byte)(":"))
	console_2.MUnsignedinteger32Drukāt(uint32(uintptr(Pointer(&sūtītbuffer))))
	console_2.MDrukāt(([]byte)(":"))
	console_2.MHexadecimalDrukāt(sūtītbuffer[0][0])
	console_2.MHexadecimalDrukāt(sūtītbuffer[0][1])
	console_2.MDrukāt(([]byte)(":"))
	pašreizējaisrecvbuffer = 0

	for ; (recvbufferApraksts[pašreizējaisrecvbuffer].karogi & 0x80000000) == 0; pašreizējaisrecvbuffer = (pašreizējaisrecvbuffer + 1) % 8 {

		if !(recvbufferApraksts[pašreizējaisrecvbuffer].karogi&0x40000000 != 0) && ((recvbufferApraksts[pašreizējaisrecvbuffer].karogi & 0x03000000) == 0x03000000) {
			var izmērs uint32 = recvbufferApraksts[pašreizējaisrecvbuffer].karogi & 0xFFF
			if izmērs > 64 {
				izmērs -= 4
			}

			console_2.MDrukāt([]byte(" size : ["))
			console_2.MUnsignedinteger32Drukāt(izmērs)
			console_2.MDrukāt([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferApraksts[pašreizējaisrecvbuffer].address_2)))
			var kursors uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Ieslēgtsrawdatareceive(kursors, int(izmērs)) {

					console_2.MDrukātxy(([]byte)("self.Send"), 0, 22)

					pats.Sūtīt(kursors, izmērs)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalDrukāt(buffer_2[i])
				console_2.MDrukāt([]byte(":"))
			}

		}
		recvbufferApraksts[pašreizējaisrecvbuffer].karogi2 = 0
		recvbufferApraksts[pašreizējaisrecvbuffer].karogi = 0x8000F7FF
	}
}
func (pats *Tamdam79c973) Kopahandler(handler *TRawdatahandler) {
	pats.handler = handler
}
func (pats *Tamdam79c973) Getmacaddress() uint64 {

	return initBloks.physicaladdress
}
func (pats *Tamdam79c973) Kopaipaddress(ip uint64) {
	initBloks.logicaladdress = ip
}
func (pats *Tamdam79c973) Getipaddress() uint64 {
	return initBloks.logicaladdress
}
