package icmp

import . "unsafe"
import . "konzola"
import . "memorijamanager"
import . "žičanavezaOkvir"
import . "ipv4"
import . "util"

var icmpKonzola = TKonzola{}

type TInternetKontrolporukaprotocolporukabuffer struct {
	Vrsta	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpVeličina int = 64

type TInternetKontrolporukaprotocolporuka struct {
	Vrsta	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (isti *TInternetKontrolporukaprotocolporuka) Init(buffer_2 TInternetKontrolporukaprotocolporukabuffer) {
	isti.Vrsta = buffer_2.Vrsta
	isti.code = buffer_2.code

	isti.checksum = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.checksum))
	isti.data = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.data))
}

func (isti *TInternetKontrolporukaprotocolporuka) Skupbuffer(buffer_2 *TInternetKontrolporukaprotocolporukabuffer) {
	buffer_2.Vrsta = isti.Vrsta
	buffer_2.code = isti.code

	buffer_2.checksum = Unsignedinteger16toNiz(isti.checksum)
	buffer_2.data = Unsignedinteger32toNiz(isti.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetKontrolporukaprotocol

func (isti *Icmphandler) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool {
	return icmp.Internetprotocolreceivewhen(izvoripaddressMrežabyteorder, odredišteipaddressMrežabyteorder, dataPokazivač, veličina)
}

var iphandler IInternetprotocolhandler

type TInternetKontrolporukaprotocol struct {
}

func (isti *TInternetKontrolporukaprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = isti
}
func (isti *TInternetKontrolporukaprotocol) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool {
	if veličina < uint32(icmpVeličina) {
		return false
	}

	var buffer_2 *TInternetKontrolporukaprotocolporukabuffer = (*TInternetKontrolporukaprotocolporukabuffer)(Pointer(dataPokazivač))
	var msg TInternetKontrolporukaprotocolporuka = TInternetKontrolporukaprotocolporuka{}
	msg.Init(*buffer_2)

	icmpKonzola.MŠtampaj(([]byte)("icmp:OnInternet"))
	icmpKonzola.MUnsignedinteger16Štampaj(uint16(msg.Vrsta))
	icmpKonzola.MŠtampaj(([]byte)(":"))

	switch msg.Vrsta {
	case 0:
		icmpKonzola.MŠtampaj(([]byte)("ping response from "))
		break

	case 8:
		icmpKonzola.MŠtampaj(([]byte)("ping send "))
		msg.Vrsta = 0

		msg.checksum = 0
		msg.Skupbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPokazivač)), uint32(icmpVeličina))

		msg.Skupbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (isti *TInternetKontrolporukaprotocol) EchorequestPošalji(ipMrežabyteorder uint32) bool {
	var icmp TInternetKontrolporukaprotocolporuka = TInternetKontrolporukaprotocolporuka{}

	var memorijamanager = &TMemorijamanager{}
	var buffer_2 = (*TInternetKontrolporukaprotocolporukabuffer)(memorijamanager.Malloc(1024))

	icmp.Vrsta = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Skupbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpVeličina))
	icmp.Skupbuffer(buffer_2)

	var dataPokazivač uintptr = uintptr(Pointer(buffer_2))
	iphandler.Pošalji(ipMrežabyteorder, 0x01, dataPokazivač, uint32(icmpVeličina))

	return false

}
