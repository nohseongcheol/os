package rahmen_des_gemeinsamen_Übertragungsnetzes

import . "konsole"

import . "amdam79c973"
import . "unsafe"
import . "hilfswerkzeug"

var ethernetKonsole TKonsole = TKonsole{}

type TEthernetRahmenKopfbuffer struct {
	zielmacbe	[6]byte
	quellemacbe	[6]byte
	ethernetTypbe	[2]byte
}

var rahmenKopfGröße int = 14

type TRahmenkopf_des_gemeinsamen_Übertragungsnetzes struct {
	zielmacbe	uint64
	quellemacbe	uint64
	ethernetTypbe	uint16
}

func (selbst *TRahmenkopf_des_gemeinsamen_Übertragungsnetzes) Init(buffer_2 TEthernetRahmenKopfbuffer) {
	selbst.zielmacbe = (Feldtounsignedinteger48(buffer_2.zielmacbe))
	selbst.quellemacbe = (Feldtounsignedinteger48(buffer_2.quellemacbe))
	selbst.ethernetTypbe = (Feldtounsignedinteger16(buffer_2.ethernetTypbe))

}
func (selbst *TRahmenkopf_des_gemeinsamen_Übertragungsnetzes) Setzenbuffer(buffer_2 *TEthernetRahmenKopfbuffer) {
	buffer_2.zielmacbe = Unsignedinteger48toFeld(Unsignedinteger48r(selbst.zielmacbe))
	buffer_2.quellemacbe = Unsignedinteger48toFeld(Unsignedinteger48r(selbst.quellemacbe))
	buffer_2.ethernetTypbe = Unsignedinteger16toFeld(Unsignedinteger16r(selbst.ethernetTypbe))
}

type IEthernetRahmenhandler interface {
	Init(backend TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes)
	Setzenhandler(handler IEthernetRahmenhandler, ethernetTyp uint16)
	EthernetRahmenreceivewhen(datenZeiger uintptr, größe int) bool
	Senden(zielmacbe uint64, datenZeiger uintptr, größe uint32)
	RahmenSenden(zielmacbe uint64, ethernetTypbe uint16, datenZeiger uintptr, größe uint32)
	Providerget() TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRahmenhandler struct {
}

var rahmen TRahmenkopf_des_gemeinsamen_Übertragungsnetzes
var Backend TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes
var handler_2 [65535]IEthernetRahmenhandler
var efhandler *TEthernetRahmenhandler = nil

func (selbst *TEthernetRahmenhandler) Init(backend TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) {
	Backend = backend
}

func (selbst *TEthernetRahmenhandler) Setzenhandler(handler IEthernetRahmenhandler, pEthernetTyp uint16) {
	handler_2[pEthernetTyp] = handler
}
func (selbst *TEthernetRahmenhandler) Setzenbackend(backend TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) {
	Backend = backend
}
func (selbst *TEthernetRahmenhandler) Getbackend() TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes {
	return Backend
}
func (selbst *TEthernetRahmenhandler) EthernetRahmenreceivewhen(datenZeiger uintptr, größe int) bool {
	ethernetKonsole.MDrucken(([]byte)("OnEtherFrameReceived"))
	return false
}
func (selbst *TEthernetRahmenhandler) Senden(zielmacbe uint64, datenZeiger uintptr, größe uint32) {
	Backend.RahmenSenden(zielmacbe, rahmen.ethernetTypbe, datenZeiger, größe)
}
func (selbst *TEthernetRahmenhandler) RahmenSenden(zielmacbe uint64, ethernetTypbe uint16, datenZeiger uintptr, größe uint32) {
	Backend.RahmenSenden(zielmacbe, ethernetTypbe, datenZeiger, größe)
}
func (selbst *TEthernetRahmenhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (selbst *TEthernetRahmenhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (selbst *TEthernetRahmenhandler) Providerget() TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes {
	return Backend
}

type TEthernetRahmenrawDatenhandler struct {
	TRawDatenhandler
}

var provider TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes

func (selbst *TEthernetRahmenrawDatenhandler) Init(pprovider TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (selbst *TEthernetRahmenrawDatenhandler) BeirawDatenreceive(datenZeiger uintptr, größe int) bool {
	return provider.BeirawDatenreceive(datenZeiger, größe)
}
func (selbst *TEthernetRahmenrawDatenhandler) Senden(datenZeiger uintptr, größe uint32) {
	provider.Senden(datenZeiger, größe)
}
func (selbst *TEthernetRahmenrawDatenhandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (selbst *TEthernetRahmenrawDatenhandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (selbst *TEthernetRahmenrawDatenhandler) Providerget() TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes {
	return provider
}

type TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes struct {
	netzwerkKartenspiele	Tamdam79c973
	handler_2		[65565]IEthernetRahmenhandler
}

func (selbst *TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) Init(backend Tamdam79c973) {

	selbst.netzwerkKartenspiele = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		selbst.handler_2[i] = nil
	}
}

var anzahl uint16 = 0

func (selbst *TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) BeirawDatenreceive(datenZeiger uintptr, größe int) bool {

	var buffer_2 *TEthernetRahmenKopfbuffer = (*TEthernetRahmenKopfbuffer)(Pointer(datenZeiger))
	var rahmen TRahmenkopf_des_gemeinsamen_Übertragungsnetzes = TRahmenkopf_des_gemeinsamen_Übertragungsnetzes{}
	rahmen.Init(*buffer_2)
	var reply bool = false

	if rahmen.zielmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(rahmen.zielmacbe) == selbst.Getmacaddress() {
		if handler_2[rahmen.ethernetTypbe] != nil {
			ethernetKonsole.MDrucken(([]byte)("provider\n"))

			var adressverweis uintptr = uintptr(Pointer(datenZeiger)) + uintptr(rahmenKopfGröße)
			reply = handler_2[rahmen.ethernetTypbe].EthernetRahmenreceivewhen(adressverweis, größe-rahmenKopfGröße)

		}
	}

	if reply {
		rahmen.zielmacbe = rahmen.quellemacbe
		rahmen.quellemacbe = Unsignedinteger48r(selbst.Getmacaddress())
		rahmen.Setzenbuffer(buffer_2)

	}

	ethernetKonsole.MDruckenxy(([]byte)("spro["), 0, 1)
	ethernetKonsole.MUnsignedinteger64Drucken(rahmen.quellemacbe)
	ethernetKonsole.MDrucken(([]byte)(":"))
	ethernetKonsole.MUnsignedinteger64Drucken(rahmen.zielmacbe)
	ethernetKonsole.MDrucken(([]byte)(":]["))
	ethernetKonsole.MUnsignedinteger64Drucken(selbst.Getmacaddress())
	ethernetKonsole.MDrucken(([]byte)(":"))
	ethernetKonsole.MUnsignedinteger16Drucken(rahmen.ethernetTypbe)
	ethernetKonsole.MDrucken(([]byte)("]"))

	return reply

}
func (selbst *TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) Senden(datenZeiger uintptr, größe uint32) {
	selbst.netzwerkKartenspiele.Senden(datenZeiger, größe)
}
func (selbst *TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) RahmenSenden(zielmacbe uint64, ethernetTypbe uint16, datenZeiger uintptr, größe uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRahmenKopfbuffer = (*TEthernetRahmenKopfbuffer)(Pointer(&buffer2_2))

	var rahmen TRahmenkopf_des_gemeinsamen_Übertragungsnetzes = TRahmenkopf_des_gemeinsamen_Übertragungsnetzes{}
	rahmen.Init(*buffer_2)

	rahmen.zielmacbe = Unsignedinteger48r(zielmacbe)
	rahmen.quellemacbe = Unsignedinteger48r(selbst.netzwerkKartenspiele.Getmacaddress())
	rahmen.ethernetTypbe = Unsignedinteger16r(ethernetTypbe)

	rahmen.Setzenbuffer(buffer_2)
	var quelle_2 [4096]byte = *(*([4096]byte))(Pointer(datenZeiger))

	var i uint32 = 0
	for i = 0; i < größe; i++ {
		buffer2_2[uint32(rahmenKopfGröße)+i] = quelle_2[i]

	}

	var adressverweis uintptr = uintptr(Pointer(&buffer2_2))

	selbst.netzwerkKartenspiele.Senden(adressverweis, größe+uint32(rahmenKopfGröße))

}
func (selbst *TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) Getmacaddress() uint64 {
	return selbst.netzwerkKartenspiele.Getmacaddress()
}
func (selbst *TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes) Getipaddress() uint64 {
	return selbst.netzwerkKartenspiele.Getipaddress()
}
