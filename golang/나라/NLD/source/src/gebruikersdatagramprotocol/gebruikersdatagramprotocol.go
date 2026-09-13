package gebruikersdatagramprotocol

import . "unsafe"
import . "console"
import . "util"
import . "geheugenmanager"
import . "protocol_voor_verbonden_netwerken_4"

var udpconsole = TConsole{}

type TGebruikerdatagramprotocolheaderbuffer struct {
	bronpoortnummer		[2]byte
	doelpoortnummer	[2]byte

	lengte		[2]byte
	checksum	[2]byte
}

var udpheaderGrootte uint32 = 8

type TGebruikersdatagramkop struct {
	bronpoortnummer		uint16
	doelpoortnummer	uint16

	lengte		uint16
	checksum	uint16
}

func (zelf *TGebruikersdatagramkop) Init(buffer_2 *TGebruikerdatagramprotocolheaderbuffer) {
	zelf.bronpoortnummer = Reeksnaarunsignedinteger16(buffer_2.bronpoortnummer)
	zelf.doelpoortnummer = Reeksnaarunsignedinteger16(buffer_2.doelpoortnummer)

	zelf.lengte = Reeksnaarunsignedinteger16(buffer_2.lengte)
	zelf.checksum = Reeksnaarunsignedinteger16(buffer_2.checksum)
}
func (zelf *TGebruikersdatagramkop) Instellenbuffer(buffer_2 *TGebruikerdatagramprotocolheaderbuffer) {

	buffer_2.bronpoortnummer = Unsignedinteger16naarReeks(zelf.bronpoortnummer)
	buffer_2.doelpoortnummer = Unsignedinteger16naarReeks(zelf.doelpoortnummer)

	buffer_2.lengte = Unsignedinteger16naarReeks(zelf.lengte)
	buffer_2.checksum = Unsignedinteger16naarReeks(zelf.checksum)

}

type IGebruikerdatagramprotocolhandler interface {
	HandgreepGebruikerdatagramprotocolBericht(contactpunt *TGebruikersdatagrameindpunt, data uintptr, grootte uint16)
}

type TGebruikerdatagramprotocolhandler struct {
}

func (zelf *TGebruikerdatagramprotocolhandler) Init(backend TProtocolleverancier_voor_verbonden_netwerken) {
}
func (zelf *TGebruikerdatagramprotocolhandler) HandgreepGebruikerdatagramprotocolBericht(contactpunt *TGebruikersdatagrameindpunt, data uintptr, grootte uint16) {
}

type IGebruikerdatagramprotocolContactpunt interface {
	HandgreepGebruikerdatagramprotocolBericht(data uintptr, grootte uint16)
}
type TGebruikersdatagrameindpunt struct {
	opafstandPoortGetal	uint16
	opafstandip		uint32
	lokaalPoortGetal	uint16
	lokaalip		uint32

	listening	bool
}

var udpprovider TGebruikerdatagramprotocolprovider
var udphandler IGebruikerdatagramprotocolhandler

func (zelf *TGebruikersdatagrameindpunt) Proef() {
}
func (zelf *TGebruikersdatagrameindpunt) Init(pudpprovider TGebruikerdatagramprotocolprovider, pudphandler IGebruikerdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	zelf.listening = false
}
func (zelf *TGebruikersdatagrameindpunt) HandgreepGebruikerdatagramprotocolBericht(data uintptr, grootte uint16) {
	if udphandler != nil {
		udphandler.HandgreepGebruikerdatagramprotocolBericht(zelf, data, grootte)
	}
}
func (zelf *TGebruikersdatagrameindpunt) Verzenden(pdata []byte, grootte uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(grootte); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Verzenden(zelf, data, grootte)
}
func (zelf *TGebruikersdatagrameindpunt) Verbindingverbreken() {
	udpprovider.Verbindingverbreken(zelf)
}

type TGebruikerdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TGebruikersdatagrameindpunt
var getalsockets int
var vrijPoort uint16

func (zelf *TGebruikerdatagramprotocolprovider) Init(pipprovider TProtocolleverancier_voor_verbonden_netwerken, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	getalsockets = 0
	vrijPoort = 1024
}
func (zelf *TGebruikerdatagramprotocolprovider) Internetprotocolreceivewhen(bronipaddressNetwerkbyteorder uint32, bestemmingipaddressNetwerkbyteorder uint32, internetprotocolpayload uintptr, grootte uint32) bool {
	if grootte < udpheaderGrootte {
		return false
	}

	var buffer_2 *TGebruikerdatagramprotocolheaderbuffer = (*TGebruikerdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TGebruikersdatagramkop
	msg.Init(buffer_2)

	var contactpunt *TGebruikersdatagrameindpunt = nil

	for i := 0; i < getalsockets && contactpunt == nil; i++ {
		if sockets[i].lokaalPoortGetal == msg.doelpoortnummer && sockets[i].lokaalip == bestemmingipaddressNetwerkbyteorder && sockets[i].listening == true {
			contactpunt = &sockets[i]
			contactpunt.listening = false
			contactpunt.opafstandPoortGetal = msg.bronpoortnummer
			contactpunt.opafstandip = bronipaddressNetwerkbyteorder
		} else if sockets[i].lokaalPoortGetal == msg.doelpoortnummer && sockets[i].lokaalip == bestemmingipaddressNetwerkbyteorder && sockets[i].opafstandPoortGetal == msg.bronpoortnummer && sockets[i].opafstandip == bronipaddressNetwerkbyteorder {
			contactpunt = &sockets[i]

		}
	}

	msg.Instellenbuffer(buffer_2)
	if contactpunt != nil {
		contactpunt.HandgreepGebruikerdatagramprotocolBericht(internetprotocolpayload+uintptr(udpheaderGrootte), uint16(grootte-udpheaderGrootte))
	}

	return false
}

func (zelf *TGebruikerdatagramprotocolprovider) Verbinden(ip uint32, poort uint16) *TGebruikersdatagrameindpunt {
	var geheugenmanager = &TGeheugenmanager{}
	var contactpunt = (*TGebruikersdatagrameindpunt)(geheugenmanager.Geheugen_toewijzen(50))

	if contactpunt != nil {

		contactpunt.Init(*zelf, nil)
		contactpunt.opafstandPoortGetal = poort
		contactpunt.opafstandip = ip
		contactpunt.lokaalPoortGetal = vrijPoort
		vrijPoort++
		contactpunt.lokaalip = uint32((*iphandler.Providerget()).Getipaddress())

		contactpunt.opafstandPoortGetal = Unsignedinteger16r(contactpunt.opafstandPoortGetal)
		contactpunt.lokaalPoortGetal = Unsignedinteger16r(contactpunt.lokaalPoortGetal)

		sockets[getalsockets] = *contactpunt
		getalsockets++

	}
	return contactpunt

}
func (zelf *TGebruikerdatagramprotocolprovider) Listen(poort uint16) *TGebruikersdatagrameindpunt {
	var contactpunt = &TGebruikersdatagrameindpunt{}
	contactpunt = nil
	if contactpunt != nil {
		contactpunt.Init(*zelf, nil)
		contactpunt.listening = true
		contactpunt.lokaalPoortGetal = poort
		contactpunt.lokaalip = uint32((*iphandler.Providerget()).Getipaddress())

		contactpunt.lokaalPoortGetal = Unsignedinteger16r(contactpunt.lokaalPoortGetal)
	}
	return contactpunt
}
func (zelf *TGebruikerdatagramprotocolprovider) Verbindingverbreken(contactpunt *TGebruikersdatagrameindpunt) {
	for i := 0; i < getalsockets && contactpunt == nil; i++ {
		if sockets[i] == *contactpunt {
			getalsockets--
			sockets[i] = sockets[getalsockets]
			break
		}
	}
}
func (zelf *TGebruikerdatagramprotocolprovider) Verzenden(contactpunt *TGebruikersdatagrameindpunt, pdata uintptr, grootte uint16) {
	var totaalLengte = uint32(grootte) + udpheaderGrootte

	var buffer_2 [4096]byte

	var msgbuffer = (*TGebruikerdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TGebruikersdatagramkop{}

	msg.bronpoortnummer = contactpunt.lokaalPoortGetal
	msg.doelpoortnummer = contactpunt.opafstandPoortGetal
	msg.lengte = Unsignedinteger16r(uint16(totaalLengte))

	msg.checksum = 0x0
	msg.Instellenbuffer(msgbuffer)

	var databytes [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(grootte); i++ {
		buffer_2[int(udpheaderGrootte)+i] = databytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Verzenden(contactpunt.opafstandip, 0x11, data, totaalLengte)

}
func (zelf *TGebruikerdatagramprotocolprovider) Bind(contactpunt *TGebruikersdatagrameindpunt, handler *TGebruikerdatagramprotocolhandler) {
}
