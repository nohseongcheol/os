package arp

import . "unsafe"
import . "console"
import . "اترنتچارچوب"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpپیغامbuffer struct {
	سختافزارنوع		[2]byte
	protocol		[2]byte
	سختافزارaddressاندازه	byte
	protocoladdressاندازه	byte
	فرمان			[2]byte

	مبدأmacaddress	[6]byte
	مبدأipaddress	[4]byte
	مقصدmacaddress	[6]byte
	مقصدipaddress	[4]byte
}

var arpmesgاندازه uint32 = (64+92+64)/8 + 2

type Arpپیغام struct {
	سختافزارنوع		uint16
	protocol		uint16
	سختافزارaddressاندازه	uint8
	protocoladdressاندازه	uint8
	فرمان			uint16

	مبدأmacaddress	uint64
	مبدأipaddress	uint32
	مقصدmacaddress	uint64
	مقصدipaddress	uint32
}

func (خود *Arpپیغام) Init(buffer_2 *Arpپیغامbuffer) {

	خود.سختافزارنوع = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.سختافزارنوع))
	خود.protocol = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.protocol))
	خود.سختافزارaddressاندازه = byte(buffer_2.سختافزارaddressاندازه)
	خود.protocoladdressاندازه = byte(buffer_2.protocoladdressاندازه)
	خود.فرمان = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.فرمان))

	خود.مبدأmacaddress = Unsignedinteger48r(Aآرایهtounsignedinteger48(buffer_2.مبدأmacaddress))
	خود.مبدأipaddress = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer_2.مبدأipaddress))
	خود.مقصدmacaddress = Unsignedinteger48r(Aآرایهtounsignedinteger48(buffer_2.مقصدmacaddress))
	خود.مقصدipaddress = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer_2.مقصدipaddress))
}
func (خود *Arpپیغام) Setbuffer(buffer_2 *Arpپیغامbuffer) {
	buffer_2.سختافزارنوع = Unsignedinteger16toآرایه(خود.سختافزارنوع)
	buffer_2.protocol = Unsignedinteger16toآرایه(خود.protocol)
	buffer_2.سختافزارaddressاندازه = uint8(خود.سختافزارaddressاندازه)
	buffer_2.protocoladdressاندازه = uint8(خود.protocoladdressاندازه)

	buffer_2.فرمان = Unsignedinteger16toآرایه(خود.فرمان)
	buffer_2.مبدأmacaddress = Unsignedinteger48toآرایه(خود.مبدأmacaddress)
	buffer_2.مبدأipaddress = Unsignedinteger32toآرایه(خود.مبدأipaddress)
	buffer_2.مقصدmacaddress = Unsignedinteger48toآرایه(خود.مقصدmacaddress)
	buffer_2.مقصدipaddress = Unsignedinteger32toآرایه(خود.مقصدipaddress)
}

type Arpاترنتچارچوبhandler struct {
	Tاترنتچارچوبhandler
}

var arpprovider Arpprovider
var اترنتچارچوبprovider Tاترنتچارچوبprovider

func (خود *Arpاترنتچارچوبhandler) Oاترنتچارچوبreceivewhen(datapointer uintptr, اندازه int) bool {
	arpconsole.Mچاپxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oاترنتچارچوبreceivewhen(datapointer, uint32(اندازه))

}
func (خود *Arpاترنتچارچوبhandler) Send(مقصدmacbe uint64, datapointer uintptr, اندازه uint32) {
	arpconsole.Mچاپxy([]byte("arp send:"), 0, 24)
	var اترنتنوعbe = Unsignedinteger16r(0x0806)
	خود.Tاترنتچارچوبhandler.Sچارچوبsend(مقصدmacbe, اترنتنوعbe, datapointer, اندازه)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	Iاترنتچارچوبhandler
}

var handler Iاترنتچارچوبhandler

func (خود *Arpprovider) Init(backend Tاترنتچارچوبprovider, userhandler Iاترنتچارچوبhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	خود.numbercacheentry = 0
	arpprovider = *خود

}

func (خود *Arpprovider) Oاترنتچارچوبreceivewhen(datapointer uintptr, اندازه uint32) bool {

	if اندازه < arpmesgاندازه {
		return false
	}
	var arpbuffer *Arpپیغامbuffer = (*Arpپیغامbuffer)(Pointer(datapointer))
	var arp Arpپیغام = Arpپیغام{}
	arp.Init(arpbuffer)

	if arp.سختافزارنوع == 0x0100 {

		if arp.protocol == 0x0008 && arp.سختافزارaddressاندازه == 6 && arp.protocoladdressاندازه == 4 && uint64(arp.مقصدipaddress) == handler.Getipaddress() {

			arpconsole.Mچاپ([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16چاپ(arp.protocol)
			arpconsole.Mچاپ([]byte(":"))
			arpconsole.MUnsignedinteger64چاپ(uint64(arp.مقصدmacaddress))
			arpconsole.Mچاپ([]byte(":"))
			arpconsole.MUnsignedinteger16چاپ(arp.فرمان)
			arpconsole.Mچاپ([]byte(":"))
			arpconsole.MUnsignedinteger64چاپ(handler.Getmacaddress())

			switch arp.فرمان {
			case 0x0100:

				if خود.Getmacfromcache(arp.مبدأipaddress) == 0xFFFFFFFFFFFF {
					if خود.numbercacheentry < 128 {
						خود.Ipcache[خود.numbercacheentry] = arp.مبدأipaddress
						خود.Maccache[خود.numbercacheentry] = arp.مبدأmacaddress
						خود.numbercacheentry++
					}
				}
				arp.فرمان = 0x0200
				arp.مقصدipaddress = arp.مبدأipaddress
				arp.مقصدmacaddress = arp.مبدأmacaddress
				arp.مبدأipaddress = uint32(handler.Getipaddress())
				arp.مبدأmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.Mچاپ(([]byte)("self.numCacheEntries"))

				if خود.numbercacheentry < 128 {
					خود.Ipcache[خود.numbercacheentry] = arp.مبدأipaddress
					خود.Maccache[خود.numbercacheentry] = arp.مبدأmacaddress
					خود.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (خود *Arpprovider) Broadcastmacaddress(Ipشبکهbyteorder uint32) {

	var arp Arpپیغام = Arpپیغام{}
	arp.سختافزارنوع = 0x0100
	arp.protocol = 0x0008
	arp.سختافزارaddressاندازه = 6
	arp.protocoladdressاندازه = 4
	arp.فرمان = 0x0200

	arp.مبدأipaddress = uint32(handler.Getipaddress())

	arp.مقصدmacaddress = خود.Resolve(Ipشبکهbyteorder)
	arp.مقصدipaddress = Ipشبکهbyteorder
	arpconsole.Mچاپxy([]byte("broad mac"), 0, 15)

	arp.مبدأmacaddress = handler.Getmacaddress()

	var arpbuffer Arpپیغامbuffer = Arpپیغامbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.مقصدmacaddress, pointer, arpmesgاندازه)
}
func (خود *Arpprovider) Requestmacaddress(Ipشبکهbyteorder uint32) {

	var arp Arpپیغام = Arpپیغام{}
	arp.سختافزارنوع = 0x0100

	arp.protocol = 0x0008
	arp.سختافزارaddressاندازه = 6
	arp.protocoladdressاندازه = 4
	arp.فرمان = 0x0100

	arp.مبدأmacaddress = handler.Getmacaddress()
	arp.مبدأipaddress = uint32(handler.Getipaddress())

	arp.مقصدmacaddress = 0xFFFFFFFFFFFF
	arp.مقصدipaddress = Ipشبکهbyteorder

	var arpbuffer Arpپیغامbuffer = Arpپیغامbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.مقصدmacaddress, pointer, arpmesgاندازه)
}
func (خود *Arpprovider) Testچاپ(data *[]byte, اندازه uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.Mچاپxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalچاپ(buffer_2[i])
		arpconsole.Mچاپ([]byte(":"))
	}
	arpconsole.Mچاپ([]byte("]"))
}

func (خود *Arpprovider) Getmacfromcache(Ipشبکهbyteorder uint32) uint64 {
	for i := 0; i < خود.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.Mچاپ(([]byte)("["))
		arpconsole.MUnsignedinteger32چاپ(خود.Ipcache[i])
		arpconsole.Mچاپ(([]byte)(":"))
		arpconsole.MUnsignedinteger32چاپ(Ipشبکهbyteorder)
		arpconsole.Mچاپ(([]byte)(":"))
		arpconsole.Mچاپ(([]byte)(":"))
		arpconsole.MUnsignedinteger64چاپ(خود.Maccache[i])
		arpconsole.Mچاپ(([]byte)("]\n"))

		if خود.Ipcache[i] == Ipشبکهbyteorder {
			arpconsole.Mچاپ([]byte("getmacfromcache"))
			return خود.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (خود *Arpprovider) Resolve(Ipشبکهbyteorder uint32) uint64 {
	var result uint64 = خود.Getmacfromcache(Ipشبکهbyteorder)
	if result == 0xFFFFFFFFFFFF {
		خود.Requestmacaddress(Ipشبکهbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = خود.Getmacfromcache(Ipشبکهbyteorder)

	}

	return result
}
