package icmp

import . "unsafe"
import . "console"
import . "memorijamanager"
import . "ethernetframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetCtrlPORUKAprotocolPORUKAbuffer struct {
	Vrsta	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpVeličina int = 64

type TInternetCtrlPORUKAprotocolPORUKA struct {
	Vrsta	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (sam *TInternetCtrlPORUKAprotocolPORUKA) Init(buffer_2 TInternetCtrlPORUKAprotocolPORUKAbuffer) {
	sam.Vrsta = buffer_2.Vrsta
	sam.code = buffer_2.code

	sam.checksum = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.checksum))
	sam.data = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.data))
}

func (sam *TInternetCtrlPORUKAprotocolPORUKA) Postavibuffer(buffer_2 *TInternetCtrlPORUKAprotocolPORUKAbuffer) {
	buffer_2.Vrsta = sam.Vrsta
	buffer_2.code = sam.code

	buffer_2.checksum = Unsignedinteger16toNiz(sam.checksum)
	buffer_2.data = Unsignedinteger32toNiz(sam.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetCtrlPORUKAprotocol

func (sam *Icmphandler) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool {
	return icmp.Internetprotocolreceivewhen(izvoripaddressMrežabyteorder, odredišteipaddressMrežabyteorder, dataPokazivač, veličina)
}

var iphandler IInternetprotocolhandler

type TInternetCtrlPORUKAprotocol struct {
}

func (sam *TInternetCtrlPORUKAprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = sam
}
func (sam *TInternetCtrlPORUKAprotocol) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool {
	if veličina < uint32(icmpVeličina) {
		return false
	}

	var buffer_2 *TInternetCtrlPORUKAprotocolPORUKAbuffer = (*TInternetCtrlPORUKAprotocolPORUKAbuffer)(Pointer(dataPokazivač))
	var msg TInternetCtrlPORUKAprotocolPORUKA = TInternetCtrlPORUKAprotocolPORUKA{}
	msg.Init(*buffer_2)

	icmpconsole.MIspis(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Ispis(uint16(msg.Vrsta))
	icmpconsole.MIspis(([]byte)(":"))

	switch msg.Vrsta {
	case 0:
		icmpconsole.MIspis(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MIspis(([]byte)("ping send "))
		msg.Vrsta = 0

		msg.checksum = 0
		msg.Postavibuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPokazivač)), uint32(icmpVeličina))

		msg.Postavibuffer(buffer_2)

		return true
		break
	}
	return false
}

func (sam *TInternetCtrlPORUKAprotocol) EchorequestPošalji(ipMrežabyteorder uint32) bool {
	var icmp TInternetCtrlPORUKAprotocolPORUKA = TInternetCtrlPORUKAprotocolPORUKA{}

	var memorijamanager = &TMemorijamanager{}
	var buffer_2 = (*TInternetCtrlPORUKAprotocolPORUKAbuffer)(memorijamanager.Malloc(1024))

	icmp.Vrsta = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Postavibuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpVeličina))
	icmp.Postavibuffer(buffer_2)

	var dataPokazivač uintptr = uintptr(Pointer(buffer_2))
	iphandler.Pošalji(ipMrežabyteorder, 0x01, dataPokazivač, uint32(icmpVeličina))

	return false

}
