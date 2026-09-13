package käyttäjän_tietosähkeiden_yhteyskäytäntö

import . "unsafe"
import . "konsoli"
import . "util"
import . "muistimanager"
import . "verkkojen_yhdyskäytäntö_4"

var udpKonsoli = TKonsoli{}

type TKäyttäjädatagramprotocolheaderbuffer struct {
	lähdeportin_numero	[2]byte
	kohdeportin_numero	[2]byte

	kesto		[2]byte
	checksum	[2]byte
}

var udpheaderKoko uint32 = 8

type TKäyttäjän_tietosähkeen_otsake struct {
	lähdeportin_numero	uint16
	kohdeportin_numero	uint16

	kesto		uint16
	checksum	uint16
}

func (itse *TKäyttäjän_tietosähkeen_otsake) Init(buffer_2 *TKäyttäjädatagramprotocolheaderbuffer) {
	itse.lähdeportin_numero = Taulukkotounsignedinteger16(buffer_2.lähdeportin_numero)
	itse.kohdeportin_numero = Taulukkotounsignedinteger16(buffer_2.kohdeportin_numero)

	itse.kesto = Taulukkotounsignedinteger16(buffer_2.kesto)
	itse.checksum = Taulukkotounsignedinteger16(buffer_2.checksum)
}
func (itse *TKäyttäjän_tietosähkeen_otsake) Asetabuffer(buffer_2 *TKäyttäjädatagramprotocolheaderbuffer) {

	buffer_2.lähdeportin_numero = Unsignedinteger16toTaulukko(itse.lähdeportin_numero)
	buffer_2.kohdeportin_numero = Unsignedinteger16toTaulukko(itse.kohdeportin_numero)

	buffer_2.kesto = Unsignedinteger16toTaulukko(itse.kesto)
	buffer_2.checksum = Unsignedinteger16toTaulukko(itse.checksum)

}

type IKäyttäjädatagramprotocolhandler interface {
	KahvaKäyttäjädatagramprotocolViesti(pistoke *TKäyttäjän_tietosähkeiden_päätepiste, data uintptr, koko uint16)
}

type TKäyttäjädatagramprotocolhandler struct {
}

func (itse *TKäyttäjädatagramprotocolhandler) Init(backend TVerkkojen_yhteyskäytännön_tarjoaja) {
}
func (itse *TKäyttäjädatagramprotocolhandler) KahvaKäyttäjädatagramprotocolViesti(pistoke *TKäyttäjän_tietosähkeiden_päätepiste, data uintptr, koko uint16) {
}

type IKäyttäjädatagramprotocolPistoke interface {
	KahvaKäyttäjädatagramprotocolViesti(data uintptr, koko uint16)
}
type TKäyttäjän_tietosähkeiden_päätepiste struct {
	etäPorttiNumero		uint16
	etäip			uint32
	paikallinenPorttiNumero	uint16
	paikallinenip		uint32

	listening	bool
}

var udpprovider TKäyttäjädatagramprotocolprovider
var udphandler IKäyttäjädatagramprotocolhandler

func (itse *TKäyttäjän_tietosähkeiden_päätepiste) Kokeile() {
}
func (itse *TKäyttäjän_tietosähkeiden_päätepiste) Init(pudpprovider TKäyttäjädatagramprotocolprovider, pudphandler IKäyttäjädatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	itse.listening = false
}
func (itse *TKäyttäjän_tietosähkeiden_päätepiste) KahvaKäyttäjädatagramprotocolViesti(data uintptr, koko uint16) {
	if udphandler != nil {
		udphandler.KahvaKäyttäjädatagramprotocolViesti(itse, data, koko)
	}
}
func (itse *TKäyttäjän_tietosähkeiden_päätepiste) Lähetä(pdata []byte, koko uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(koko); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Lähetä(itse, data, koko)
}
func (itse *TKäyttäjän_tietosähkeiden_päätepiste) Katkaiseyhteys() {
	udpprovider.Katkaiseyhteys(itse)
}

type TKäyttäjädatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TKäyttäjän_tietosähkeiden_päätepiste
var numerosockets int
var vapaanaPortti uint16

func (itse *TKäyttäjädatagramprotocolprovider) Init(pipprovider TVerkkojen_yhteyskäytännön_tarjoaja, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numerosockets = 0
	vapaanaPortti = 1024
}
func (itse *TKäyttäjädatagramprotocolprovider) Internetprotocolreceivewhen(lähdeipaddressVerkkobyteorder uint32, kohdeipaddressVerkkobyteorder uint32, internetprotocolpayload uintptr, koko uint32) bool {
	if koko < udpheaderKoko {
		return false
	}

	var buffer_2 *TKäyttäjädatagramprotocolheaderbuffer = (*TKäyttäjädatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKäyttäjän_tietosähkeen_otsake
	msg.Init(buffer_2)

	var pistoke *TKäyttäjän_tietosähkeiden_päätepiste = nil

	for i := 0; i < numerosockets && pistoke == nil; i++ {
		if sockets[i].paikallinenPorttiNumero == msg.kohdeportin_numero && sockets[i].paikallinenip == kohdeipaddressVerkkobyteorder && sockets[i].listening == true {
			pistoke = &sockets[i]
			pistoke.listening = false
			pistoke.etäPorttiNumero = msg.lähdeportin_numero
			pistoke.etäip = lähdeipaddressVerkkobyteorder
		} else if sockets[i].paikallinenPorttiNumero == msg.kohdeportin_numero && sockets[i].paikallinenip == kohdeipaddressVerkkobyteorder && sockets[i].etäPorttiNumero == msg.lähdeportin_numero && sockets[i].etäip == lähdeipaddressVerkkobyteorder {
			pistoke = &sockets[i]

		}
	}

	msg.Asetabuffer(buffer_2)
	if pistoke != nil {
		pistoke.KahvaKäyttäjädatagramprotocolViesti(internetprotocolpayload+uintptr(udpheaderKoko), uint16(koko-udpheaderKoko))
	}

	return false
}

func (itse *TKäyttäjädatagramprotocolprovider) Yhdistä(ip uint32, portti uint16) *TKäyttäjän_tietosähkeiden_päätepiste {
	var muistimanager = &TMuistimanager{}
	var pistoke = (*TKäyttäjän_tietosähkeiden_päätepiste)(muistimanager.Varaa_muistia(50))

	if pistoke != nil {

		pistoke.Init(*itse, nil)
		pistoke.etäPorttiNumero = portti
		pistoke.etäip = ip
		pistoke.paikallinenPorttiNumero = vapaanaPortti
		vapaanaPortti++
		pistoke.paikallinenip = uint32((*iphandler.Providerget()).Getipaddress())

		pistoke.etäPorttiNumero = Unsignedinteger16r(pistoke.etäPorttiNumero)
		pistoke.paikallinenPorttiNumero = Unsignedinteger16r(pistoke.paikallinenPorttiNumero)

		sockets[numerosockets] = *pistoke
		numerosockets++

	}
	return pistoke

}
func (itse *TKäyttäjädatagramprotocolprovider) Listen(portti uint16) *TKäyttäjän_tietosähkeiden_päätepiste {
	var pistoke = &TKäyttäjän_tietosähkeiden_päätepiste{}
	pistoke = nil
	if pistoke != nil {
		pistoke.Init(*itse, nil)
		pistoke.listening = true
		pistoke.paikallinenPorttiNumero = portti
		pistoke.paikallinenip = uint32((*iphandler.Providerget()).Getipaddress())

		pistoke.paikallinenPorttiNumero = Unsignedinteger16r(pistoke.paikallinenPorttiNumero)
	}
	return pistoke
}
func (itse *TKäyttäjädatagramprotocolprovider) Katkaiseyhteys(pistoke *TKäyttäjän_tietosähkeiden_päätepiste) {
	for i := 0; i < numerosockets && pistoke == nil; i++ {
		if sockets[i] == *pistoke {
			numerosockets--
			sockets[i] = sockets[numerosockets]
			break
		}
	}
}
func (itse *TKäyttäjädatagramprotocolprovider) Lähetä(pistoke *TKäyttäjän_tietosähkeiden_päätepiste, pdata uintptr, koko uint16) {
	var yhteensäKesto = uint32(koko) + udpheaderKoko

	var buffer_2 [4096]byte

	var msgbuffer = (*TKäyttäjädatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKäyttäjän_tietosähkeen_otsake{}

	msg.lähdeportin_numero = pistoke.paikallinenPorttiNumero
	msg.kohdeportin_numero = pistoke.etäPorttiNumero
	msg.kesto = Unsignedinteger16r(uint16(yhteensäKesto))

	msg.checksum = 0x0
	msg.Asetabuffer(msgbuffer)

	var datatavua [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(koko); i++ {
		buffer_2[int(udpheaderKoko)+i] = datatavua[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Lähetä(pistoke.etäip, 0x11, data, yhteensäKesto)

}
func (itse *TKäyttäjädatagramprotocolprovider) Bind(pistoke *TKäyttäjän_tietosähkeiden_päätepiste, handler *TKäyttäjädatagramprotocolhandler,) {
}
