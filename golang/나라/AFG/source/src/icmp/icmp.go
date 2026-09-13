package icmp

import . "unsafe"
import . "console"
import . "حافظهmanager"
import . "اترنتچارچوب"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type Tاینترنتمهارپیغامprotocolپیغامbuffer struct {
	Tنوع	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpاندازه int = 64

type Tاینترنتمهارپیغامprotocolپیغام struct {
	Tنوع	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (خود *Tاینترنتمهارپیغامprotocolپیغام) Init(buffer_2 Tاینترنتمهارپیغامprotocolپیغامbuffer) {
	خود.Tنوع = buffer_2.Tنوع
	خود.code = buffer_2.code

	خود.checksum = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.checksum))
	خود.data = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer_2.data))
}

func (خود *Tاینترنتمهارپیغامprotocolپیغام) Setbuffer(buffer_2 *Tاینترنتمهارپیغامprotocolپیغامbuffer) {
	buffer_2.Tنوع = خود.Tنوع
	buffer_2.code = خود.code

	buffer_2.checksum = Unsignedinteger16toآرایه(خود.checksum)
	buffer_2.data = Unsignedinteger32toآرایه(خود.data)
}

type Icmphandler struct {
	Tاینترنتprotocolhandler
}

var icmp *Tاینترنتمهارپیغامprotocol

func (خود *Icmphandler) Oاینترنتprotocolreceivewhen(مبدأipaddressشبکهbyteorder uint32, مقصدipaddressشبکهbyteorder uint32, datapointer uintptr, اندازه uint32) bool {
	return icmp.Oاینترنتprotocolreceivewhen(مبدأipaddressشبکهbyteorder, مقصدipaddressشبکهbyteorder, datapointer, اندازه)
}

var iphandler Iاینترنتprotocolhandler

type Tاینترنتمهارپیغامprotocol struct {
}

func (خود *Tاینترنتمهارپیغامprotocol) Init(backend Tاینترنتprotocolprovider, handler Iاینترنتprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = خود
}
func (خود *Tاینترنتمهارپیغامprotocol) Oاینترنتprotocolreceivewhen(مبدأipaddressشبکهbyteorder uint32, مقصدipaddressشبکهbyteorder uint32, datapointer uintptr, اندازه uint32) bool {
	if اندازه < uint32(icmpاندازه) {
		return false
	}

	var buffer_2 *Tاینترنتمهارپیغامprotocolپیغامbuffer = (*Tاینترنتمهارپیغامprotocolپیغامbuffer)(Pointer(datapointer))
	var msg Tاینترنتمهارپیغامprotocolپیغام = Tاینترنتمهارپیغامprotocolپیغام{}
	msg.Init(*buffer_2)

	icmpconsole.Mچاپ(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16چاپ(uint16(msg.Tنوع))
	icmpconsole.Mچاپ(([]byte)(":"))

	switch msg.Tنوع {
	case 0:
		icmpconsole.Mچاپ(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.Mچاپ(([]byte)("ping send "))
		msg.Tنوع = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpاندازه))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (خود *Tاینترنتمهارپیغامprotocol) Echorequestsend(ipشبکهbyteorder uint32) bool {
	var icmp Tاینترنتمهارپیغامprotocolپیغام = Tاینترنتمهارپیغامprotocolپیغام{}

	var حافظهmanager = &Tحافظهmanager{}
	var buffer_2 = (*Tاینترنتمهارپیغامprotocolپیغامbuffer)(حافظهmanager.Malloc(1024))

	icmp.Tنوع = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpاندازه))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipشبکهbyteorder, 0x01, datapointer, uint32(icmpاندازه))

	return false

}
