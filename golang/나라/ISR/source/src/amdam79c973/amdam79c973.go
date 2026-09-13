package amdam79c973

import . "unsafe"
import . "פסק"
import . "console"
import . "שער"
import . "pci"

var רשתקלפיםconsole TConsole = TConsole{}

type TInitializationבלוק struct {
	מצב		uint16
	מספרשלחbuffer	uint8
	מספרrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferתיאורaddress	uintptr
	שלחbufferתיאורaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	דגלים		uint32
	דגלים2		uint32
	פנוי		uint32
}

type IRawdatahandler interface {
	Oפעילrawdatareceive(dataסמן uintptr, גודל int) bool
	Sשלח(dataסמן uintptr, גודל uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Sקבעbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Oפעילrawdatareceive(dataסמן uintptr, גודל int) bool {
	רשתקלפיםconsole.Mהדפסהxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Sשלח(dataסמן uintptr, גודל uint32) {
	רשתקלפיםconsole.Mהדפסהxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Sשלח(dataסמן, גודל)
}

var Macaddress0שער uint16
var Macaddress2שער uint16
var Macaddress4שער uint16
var registerdataשער uint16
var registeraddressשער uint16
var אפסשער uint16
var busבקרהregisterdataשער uint16

var initבלוק TInitializationבלוק

var שלחbufferתיאור [8]TBufferdescriptor
var שלחbufferתיאורזיכרון [2048 + 15]byte
var שלחbuffer [2*1024 + 15][8]uint8
var נוכחישלחbuffer uint8

var recvbufferתיאור [8]TBufferdescriptor
var recvbufferתיאורזיכרון [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var נוכחיrecvbuffer uint8
var funcערך func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	Tפסקhandler
	התקןdescriptor	TPeripheralcomponentinterconnectהתקןdescriptor
	פסק		*Tפסקmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(פסק *Tפסקmanager, התקןdescriptor TPeripheralcomponentinterconnectהתקןdescriptor, handler IRawdatahandler) {

	self.התקןdescriptor = התקןdescriptor

	funcערך = (*Tamdam79c973).Hידיתפסק
	var address uintptr
	address = uintptr(Pointer(&funcערך))

	self.Init(uint8(0x20+התקןdescriptor.Iפסק), uintptr(Pointer(פסק)), address)

	Macaddress0שער = uint16(התקןdescriptor.Pשערbase)
	Macaddress2שער = uint16(התקןdescriptor.Pשערbase) + 0x02
	Macaddress4שער = uint16(התקןdescriptor.Pשערbase) + 0x04
	registerdataשער = uint16(התקןdescriptor.Pשערbase) + 0x10
	registeraddressשער = uint16(התקןdescriptor.Pשערbase) + 0x12
	אפסשער = uint16(התקןdescriptor.Pשערbase) + 0x14
	busבקרהregisterdataשער = uint16(התקןdescriptor.Pשערbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	נוכחישלחbuffer = 0
	נוכחיrecvbuffer = 0

	var Mac0 uint64 = uint64(Pשערקריאהמילים(Macaddress0שער) % 256)
	var Mac1 uint64 = uint64(Pשערקריאהמילים(Macaddress0שער) / 256)
	var Mac2 uint64 = uint64(Pשערקריאהמילים(Macaddress2שער) % 256)
	var Mac3 uint64 = uint64(Pשערקריאהמילים(Macaddress2שער) / 256)
	var Mac4 uint64 = uint64(Pשערקריאהמילים(Macaddress4שער) % 256)
	var Mac5 uint64 = uint64(Pשערקריאהמילים(Macaddress4שער) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.Mהדפסהxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalהדפסה(uint8(התקןdescriptor.Iפסק))
	console_2.Mהדפסה(([]byte)("]"))
	console_2.Mהדפסה(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16הדפסה(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32הדפסה(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.Mהדפסה(([]byte)("]"))

	Pשערכתיבהמילים(registeraddressשער, 20)
	Pשערכתיבהמילים(busבקרהregisterdataשער, 0x102)

	Pשערכתיבהמילים(registeraddressשער, 0)
	Pשערכתיבהמילים(registerdataשער, 0x04)

	initבלוק.מצב = 0x0000
	initבלוק.מספרשלחbuffer = 3
	initבלוק.מספרrecvbuffer = 3

	initבלוק.physicaladdress = Mac

	initבלוק.logicaladdress = 0

	שלחbufferתיאור = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&שלחbufferתיאורזיכרון)) + 15) & ^(uintptr)(0xF)))
	initבלוק.שלחbufferתיאורaddress = uintptr(Pointer(&שלחbufferתיאור))
	recvbufferתיאור = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferתיאורזיכרון)) + 15) & ^(uintptr)(0xF)))
	initבלוק.recvbufferתיאורaddress = uintptr(Pointer(&recvbufferתיאור))

	for i := 0; i < 8; i++ {
		שלחbufferתיאור[i].address_2 = uint32((uintptr(Pointer(&שלחbuffer[i])) + 15) & ^(uintptr(0xF)))
		שלחbufferתיאור[i].דגלים = 0x7FF | 0xF000
		שלחbufferתיאור[i].דגלים2 = 0
		שלחbufferתיאור[i].פנוי = 0

		recvbufferתיאור[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferתיאור[i].דגלים = 0xF7FF | 0x80000000

	}

	Pשערכתיבהמילים(registeraddressשער, 1)
	Pשערכתיבהמילים(registerdataשער, uint16(uintptr(Pointer(&initבלוק))&0xFFFF))

	Pשערכתיבהמילים(registeraddressשער, 2)
	Pשערכתיבהמילים(registerdataשער, uint16((uintptr(Pointer(&initבלוק))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aהפעל() {
	Pשערכתיבהמילים(registeraddressשער, 0)
	Pשערכתיבהמילים(registerdataשער, 0x41)

	Pשערכתיבהמילים(registeraddressשער, 4)
	temporary := Pשערקריאהמילים(registerdataשער)
	Pשערכתיבהמילים(registeraddressשער, 4)
	Pשערכתיבהמילים(registerdataשער, temporary|0xC00)

	Pשערכתיבהמילים(registeraddressשער, 0)
	Pשערכתיבהמילים(registerdataשער, 0x42)

}
func (self *Tamdam79c973) Rאפס() int {
	Pשערקריאהמילים(אפסשער)
	Pשערכתיבהמילים(אפסשער, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Hידיתפסק(esp uint32) uint32 {

	Pשערכתיבהמילים(registeraddressשער, 0)
	temporary := uint32(Pשערקריאהמילים(registerdataשער))
	console_2.Mהדפסה(([]byte)("interrupt("))
	console_2.MUnsignedinteger32הדפסה(esp)
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MUnsignedinteger32הדפסה(temporary)
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MUnsignedinteger16הדפסה(count)
	count++
	console_2.Mהדפסה(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.Mהדפסה(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.Mהדפסה(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.Mהדפסה(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.Mהדפסה(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.Mהדפסה(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.Mהדפסה(([]byte)("am79c973 data sent"))
	}

	Pשערכתיבהמילים(registeraddressשער, 0)
	Pשערכתיבהמילים(registerdataשער, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.Mהדפסה(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Sשלח(dataסמן uintptr, גודל uint32) {
	var שלחdescriptor uint16 = uint16(נוכחישלחbuffer)
	נוכחישלחbuffer = 0

	if גודל > 1518 {
		גודל = 1518
	}

	var מקור_2 [4096]byte = *(*([4096]byte))(Pointer(dataסמן))
	var יעד_2 uint32 = שלחbufferתיאור[שלחdescriptor].address_2 + גודל - 1

	for i := 0; i < int(גודל); i++ {

		*(*byte)(Pointer(uintptr(יעד_2))) = מקור_2[int(גודל)-i-1]

		יעד_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataסמן))
	console_2.Mהדפסהxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalהדפסה(data[i])
		console_2.Mהדפסה(([]byte)(":"))
	}
	console_2.Mהדפסה(([]byte)("\n"))

	שלחbufferתיאור[שלחdescriptor].פנוי = 0
	שלחbufferתיאור[שלחdescriptor].דגלים2 = 0
	שלחbufferתיאור[שלחdescriptor].דגלים = 0x8300F000 | uint32((-גודל)&0xFFF)

	Pשערכתיבהמילים(registeraddressשער, 0)
	Pשערכתיבהמילים(registerdataשער, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MUnsignedinteger32הדפסה(uint32(uintptr(Pointer(&שלחbuffer))))
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MHexadecimalהדפסה(שלחbuffer[0][0])
	console_2.MHexadecimalהדפסה(שלחbuffer[0][1])
	console_2.Mהדפסה(([]byte)(":"))
	נוכחיrecvbuffer = 0

	for ; (recvbufferתיאור[נוכחיrecvbuffer].דגלים & 0x80000000) == 0; נוכחיrecvbuffer = (נוכחיrecvbuffer + 1) % 8 {

		if !(recvbufferתיאור[נוכחיrecvbuffer].דגלים&0x40000000 != 0) && ((recvbufferתיאור[נוכחיrecvbuffer].דגלים & 0x03000000) == 0x03000000) {
			var גודל uint32 = recvbufferתיאור[נוכחיrecvbuffer].דגלים & 0xFFF
			if גודל > 64 {
				גודל -= 4
			}

			console_2.Mהדפסה([]byte(" size : ["))
			console_2.MUnsignedinteger32הדפסה(גודל)
			console_2.Mהדפסה([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferתיאור[נוכחיrecvbuffer].address_2)))
			var סמן uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Oפעילrawdatareceive(סמן, int(גודל)) {

					console_2.Mהדפסהxy(([]byte)("self.Send"), 0, 22)

					self.Sשלח(סמן, גודל)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalהדפסה(buffer_2[i])
				console_2.Mהדפסה([]byte(":"))
			}

		}
		recvbufferתיאור[נוכחיrecvbuffer].דגלים2 = 0
		recvbufferתיאור[נוכחיrecvbuffer].דגלים = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sקבעhandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initבלוק.physicaladdress
}
func (self *Tamdam79c973) Sקבעipaddress(ip uint64) {
	initבלוק.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initבלוק.logicaladdress
}
