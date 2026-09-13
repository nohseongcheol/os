package amdam79c973

import . "unsafe"
import . "中斷"
import . "控制台"
import . "連接埠"
import . "pci"

var 網路紙牌控制台 T控制台 = T控制台{}

type TInitialization區塊 struct {
	模式		uint16
	數字送出buffer	uint8
	數字recvbuffer	uint8

	物理address	uint64

	邏輯address		uint64
	recvbuffer描述address	uintptr
	送出buffer描述address	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	旗標		uint32
	旗標2		uint32
	可用空間		uint32
}

type IRaw資料handler interface {
	O時raw資料receive(資料指標 uintptr, 大小 int) bool
	S送出(資料指標 uintptr, 大小 uint32)
}

var raw資料backend Tamdam79c973

type TRaw資料handler struct {
}

func (self *TRaw資料handler) S設定backend(backend Tamdam79c973) {

	raw資料backend = backend
}
func (self *TRaw資料handler) Getbackend() Tamdam79c973 {
	return raw資料backend
}
func (self *TRaw資料handler) O時raw資料receive(資料指標 uintptr, 大小 int) bool {
	網路紙牌控制台.M列印xy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRaw資料handler) S送出(資料指標 uintptr, 大小 uint32) {
	網路紙牌控制台.M列印xy(([]byte)("TRawDataSend"), 10, 10)
	raw資料backend.S送出(資料指標, 大小)
}

var Macaddress0連接埠 uint16
var Macaddress2連接埠 uint16
var Macaddress4連接埠 uint16
var 暫存器資料連接埠 uint16
var 暫存器address連接埠 uint16
var 重設連接埠 uint16
var bus控制暫存器資料連接埠 uint16

var init區塊 TInitialization區塊

var 送出buffer描述 [8]TBufferdescriptor
var 送出buffer描述記憶體 [2048 + 15]byte
var 送出buffer [2*1024 + 15][8]uint8
var 目前送出buffer uint8

var recvbuffer描述 [8]TBufferdescriptor
var recvbuffer描述記憶體 [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var 目前recvbuffer uint8
var func數值 func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	T中斷handler
	裝置descriptor	TPeripheralcomponentinterconnect裝置descriptor
	中斷		*T中斷管理器
	handler		*TRaw資料handler
}

var 控制台_2 T控制台 = T控制台{}
var iraw資料handler IRaw資料handler

func (self *Tamdam79c973) Init驅動程式(中斷 *T中斷管理器, 裝置descriptor TPeripheralcomponentinterconnect裝置descriptor, handler IRaw資料handler) {

	self.裝置descriptor = 裝置descriptor

	func數值 = (*Tamdam79c973).H控制把中斷
	var address uintptr
	address = uintptr(Pointer(&func數值))

	self.Init(uint8(0x20+裝置descriptor.I中斷), uintptr(Pointer(中斷)), address)

	Macaddress0連接埠 = uint16(裝置descriptor.P連接埠base)
	Macaddress2連接埠 = uint16(裝置descriptor.P連接埠base) + 0x02
	Macaddress4連接埠 = uint16(裝置descriptor.P連接埠base) + 0x04
	暫存器資料連接埠 = uint16(裝置descriptor.P連接埠base) + 0x10
	暫存器address連接埠 = uint16(裝置descriptor.P連接埠base) + 0x12
	重設連接埠 = uint16(裝置descriptor.P連接埠base) + 0x14
	bus控制暫存器資料連接埠 = uint16(裝置descriptor.P連接埠base) + 0x16

	iraw資料handler = &TRaw資料handler{}
	if handler != nil {
		iraw資料handler = handler
	}

	目前送出buffer = 0
	目前recvbuffer = 0

	var Mac0 uint64 = uint64(P連接埠讀取字(Macaddress0連接埠) % 256)
	var Mac1 uint64 = uint64(P連接埠讀取字(Macaddress0連接埠) / 256)
	var Mac2 uint64 = uint64(P連接埠讀取字(Macaddress2連接埠) % 256)
	var Mac3 uint64 = uint64(P連接埠讀取字(Macaddress2連接埠) / 256)
	var Mac4 uint64 = uint64(P連接埠讀取字(Macaddress4連接埠) % 256)
	var Mac5 uint64 = uint64(P連接埠讀取字(Macaddress4連接埠) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	控制台_2.M列印xy(([]byte)("[interrupt num : "), 0, 13)
	控制台_2.MHexadecimal列印(uint8(裝置descriptor.I中斷))
	控制台_2.M列印(([]byte)("]"))
	控制台_2.M列印(([]byte)("[mac address : "))
	控制台_2.MUnsignedinteger16列印(uint16(macaddress >> 32))
	控制台_2.MUnsignedinteger32列印(uint32(macaddress & 0x00000000FFFFFFFF))
	控制台_2.M列印(([]byte)("]"))

	P連接埠寫入字(暫存器address連接埠, 20)
	P連接埠寫入字(bus控制暫存器資料連接埠, 0x102)

	P連接埠寫入字(暫存器address連接埠, 0)
	P連接埠寫入字(暫存器資料連接埠, 0x04)

	init區塊.模式 = 0x0000
	init區塊.數字送出buffer = 3
	init區塊.數字recvbuffer = 3

	init區塊.物理address = Mac

	init區塊.邏輯address = 0

	送出buffer描述 = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&送出buffer描述記憶體)) + 15) & ^(uintptr)(0xF)))
	init區塊.送出buffer描述address = uintptr(Pointer(&送出buffer描述))
	recvbuffer描述 = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbuffer描述記憶體)) + 15) & ^(uintptr)(0xF)))
	init區塊.recvbuffer描述address = uintptr(Pointer(&recvbuffer描述))

	for i := 0; i < 8; i++ {
		送出buffer描述[i].address_2 = uint32((uintptr(Pointer(&送出buffer[i])) + 15) & ^(uintptr(0xF)))
		送出buffer描述[i].旗標 = 0x7FF | 0xF000
		送出buffer描述[i].旗標2 = 0
		送出buffer描述[i].可用空間 = 0

		recvbuffer描述[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbuffer描述[i].旗標 = 0xF7FF | 0x80000000

	}

	P連接埠寫入字(暫存器address連接埠, 1)
	P連接埠寫入字(暫存器資料連接埠, uint16(uintptr(Pointer(&init區塊))&0xFFFF))

	P連接埠寫入字(暫存器address連接埠, 2)
	P連接埠寫入字(暫存器資料連接埠, uint16((uintptr(Pointer(&init區塊))>>16)&0xFFFF))

}
func (self *Tamdam79c973) A使用() {
	P連接埠寫入字(暫存器address連接埠, 0)
	P連接埠寫入字(暫存器資料連接埠, 0x41)

	P連接埠寫入字(暫存器address連接埠, 4)
	temporary := P連接埠讀取字(暫存器資料連接埠)
	P連接埠寫入字(暫存器address連接埠, 4)
	P連接埠寫入字(暫存器資料連接埠, temporary|0xC00)

	P連接埠寫入字(暫存器address連接埠, 0)
	P連接埠寫入字(暫存器資料連接埠, 0x42)

}
func (self *Tamdam79c973) R重設() int {
	P連接埠讀取字(重設連接埠)
	P連接埠寫入字(重設連接埠, 0)
	return 10
}

var 計數 uint16 = 0

func (self *Tamdam79c973) H控制把中斷(esp uint32) uint32 {

	P連接埠寫入字(暫存器address連接埠, 0)
	temporary := uint32(P連接埠讀取字(暫存器資料連接埠))
	控制台_2.M列印(([]byte)("interrupt("))
	控制台_2.MUnsignedinteger32列印(esp)
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MUnsignedinteger32列印(temporary)
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MUnsignedinteger16列印(計數)
	計數++
	控制台_2.M列印(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		控制台_2.M列印(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		控制台_2.M列印(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		控制台_2.M列印(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		控制台_2.M列印(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		控制台_2.M列印(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		控制台_2.M列印(([]byte)("am79c973 data sent"))
	}

	P連接埠寫入字(暫存器address連接埠, 0)
	P連接埠寫入字(暫存器資料連接埠, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		控制台_2.M列印(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) S送出(資料指標 uintptr, 大小 uint32) {
	var 送出descriptor uint16 = uint16(目前送出buffer)
	目前送出buffer = 0

	if 大小 > 1518 {
		大小 = 1518
	}

	var 來源_2 [4096]byte = *(*([4096]byte))(Pointer(資料指標))
	var 目的地_2 uint32 = 送出buffer描述[送出descriptor].address_2 + 大小 - 1

	for i := 0; i < int(大小); i++ {

		*(*byte)(Pointer(uintptr(目的地_2))) = 來源_2[int(大小)-i-1]

		目的地_2--
	}

	var 資料 [4096]byte = *(*([4096]byte))(Pointer(資料指標))
	控制台_2.M列印xy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		控制台_2.MHexadecimal列印(資料[i])
		控制台_2.M列印(([]byte)(":"))
	}
	控制台_2.M列印(([]byte)("\n"))

	送出buffer描述[送出descriptor].可用空間 = 0
	送出buffer描述[送出descriptor].旗標2 = 0
	送出buffer描述[送出descriptor].旗標 = 0x8300F000 | uint32((-大小)&0xFFF)

	P連接埠寫入字(暫存器address連接埠, 0)
	P連接埠寫入字(暫存器資料連接埠, 0x48)

}
func (self *Tamdam79c973) Receive() {
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MUnsignedinteger32列印(uint32(uintptr(Pointer(&送出buffer))))
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MHexadecimal列印(送出buffer[0][0])
	控制台_2.MHexadecimal列印(送出buffer[0][1])
	控制台_2.M列印(([]byte)(":"))
	目前recvbuffer = 0

	for ; (recvbuffer描述[目前recvbuffer].旗標 & 0x80000000) == 0; 目前recvbuffer = (目前recvbuffer + 1) % 8 {

		if !(recvbuffer描述[目前recvbuffer].旗標&0x40000000 != 0) && ((recvbuffer描述[目前recvbuffer].旗標 & 0x03000000) == 0x03000000) {
			var 大小 uint32 = recvbuffer描述[目前recvbuffer].旗標 & 0xFFF
			if 大小 > 64 {
				大小 -= 4
			}

			控制台_2.M列印([]byte(" size : ["))
			控制台_2.MUnsignedinteger32列印(大小)
			控制台_2.M列印([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbuffer描述[目前recvbuffer].address_2)))
			var 位址參照 uintptr = uintptr(Pointer(&buffer_2))
			if iraw資料handler != nil {
				if iraw資料handler.O時raw資料receive(位址參照, int(大小)) {

					控制台_2.M列印xy(([]byte)("self.Send"), 0, 22)

					self.S送出(位址參照, 大小)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				控制台_2.MHexadecimal列印(buffer_2[i])
				控制台_2.M列印([]byte(":"))
			}

		}
		recvbuffer描述[目前recvbuffer].旗標2 = 0
		recvbuffer描述[目前recvbuffer].旗標 = 0x8000F7FF
	}
}
func (self *Tamdam79c973) S設定handler(handler *TRaw資料handler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return init區塊.物理address
}
func (self *Tamdam79c973) S設定ipaddress(ip uint64) {
	init區塊.邏輯address = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return init區塊.邏輯address
}
