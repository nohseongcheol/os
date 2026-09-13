package icmp

import . "unsafe"
import . "console"
import . "minnimanager"
import . "ethernetRammi"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetiðStýringSKILABOÐprotocolSKILABOÐbuffer struct {
	Tegund	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpStærð int = 64

type TInternetiðStýringSKILABOÐprotocolSKILABOÐ struct {
	Tegund	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (sjálft *TInternetiðStýringSKILABOÐprotocolSKILABOÐ) Init(buffer_2 TInternetiðStýringSKILABOÐprotocolSKILABOÐbuffer) {
	sjálft.Tegund = buffer_2.Tegund
	sjálft.code = buffer_2.code

	sjálft.checksum = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.checksum))
	sjálft.data = Unsignedinteger32r(Fylkitounsignedinteger32(buffer_2.data))
}

func (sjálft *TInternetiðStýringSKILABOÐprotocolSKILABOÐ) Setjabuffer(buffer_2 *TInternetiðStýringSKILABOÐprotocolSKILABOÐbuffer) {
	buffer_2.Tegund = sjálft.Tegund
	buffer_2.code = sjálft.code

	buffer_2.checksum = Unsignedinteger16toFylki(sjálft.checksum)
	buffer_2.data = Unsignedinteger32toFylki(sjálft.data)
}

type Icmphandler struct {
	TInternetiðprotocolhandler
}

var icmp *TInternetiðStýringSKILABOÐprotocol

func (sjálft *Icmphandler) Internetiðprotocolreceivewhen(uppruniipaddressNetkerfibyteorder uint32, áfangastaðuripaddressNetkerfibyteorder uint32, dataBendill uintptr, stærð uint32) bool {
	return icmp.Internetiðprotocolreceivewhen(uppruniipaddressNetkerfibyteorder, áfangastaðuripaddressNetkerfibyteorder, dataBendill, stærð)
}

var iphandler IInternetiðprotocolhandler

type TInternetiðStýringSKILABOÐprotocol struct {
}

func (sjálft *TInternetiðStýringSKILABOÐprotocol) Init(backend TInternetiðprotocolprovider, handler IInternetiðprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = sjálft
}
func (sjálft *TInternetiðStýringSKILABOÐprotocol) Internetiðprotocolreceivewhen(uppruniipaddressNetkerfibyteorder uint32, áfangastaðuripaddressNetkerfibyteorder uint32, dataBendill uintptr, stærð uint32) bool {
	if stærð < uint32(icmpStærð) {
		return false
	}

	var buffer_2 *TInternetiðStýringSKILABOÐprotocolSKILABOÐbuffer = (*TInternetiðStýringSKILABOÐprotocolSKILABOÐbuffer)(Pointer(dataBendill))
	var msg TInternetiðStýringSKILABOÐprotocolSKILABOÐ = TInternetiðStýringSKILABOÐprotocolSKILABOÐ{}
	msg.Init(*buffer_2)

	icmpconsole.MPrenta(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Prenta(uint16(msg.Tegund))
	icmpconsole.MPrenta(([]byte)(":"))

	switch msg.Tegund {
	case 0:
		icmpconsole.MPrenta(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MPrenta(([]byte)("ping send "))
		msg.Tegund = 0

		msg.checksum = 0
		msg.Setjabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataBendill)), uint32(icmpStærð))

		msg.Setjabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (sjálft *TInternetiðStýringSKILABOÐprotocol) EchorequestSenda(ipNetkerfibyteorder uint32) bool {
	var icmp TInternetiðStýringSKILABOÐprotocolSKILABOÐ = TInternetiðStýringSKILABOÐprotocolSKILABOÐ{}

	var minnimanager = &TMinnimanager{}
	var buffer_2 = (*TInternetiðStýringSKILABOÐprotocolSKILABOÐbuffer)(minnimanager.Malloc(1024))

	icmp.Tegund = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setjabuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpStærð))
	icmp.Setjabuffer(buffer_2)

	var dataBendill uintptr = uintptr(Pointer(buffer_2))
	iphandler.Senda(ipNetkerfibyteorder, 0x01, dataBendill, uint32(icmpStærð))

	return false

}
