package protokol_uživatelských_datagramů

import . "unsafe"
import . "konzole"
import . "util"
import . "paměťmanager"
import . "protokol_propojených_sítí_4"

var udpKonzole = TKonzole{}

type TUživateldatagramprotocolheaderbuffer struct {
	číslo_zdrojového_portu	[2]byte
	číslo_cílového_portu	[2]byte

	délka		[2]byte
	kontrolnísoučet	[2]byte
}

var udpheaderVelikost uint32 = 8

type THlavička_uživatelského_datagramu struct {
	číslo_zdrojového_portu	uint16
	číslo_cílového_portu	uint16

	délka		uint16
	kontrolnísoučet	uint16
}

func (self *THlavička_uživatelského_datagramu) Init(buffer_2 *TUživateldatagramprotocolheaderbuffer) {
	self.číslo_zdrojového_portu = Poledounsignedinteger16(buffer_2.číslo_zdrojového_portu)
	self.číslo_cílového_portu = Poledounsignedinteger16(buffer_2.číslo_cílového_portu)

	self.délka = Poledounsignedinteger16(buffer_2.délka)
	self.kontrolnísoučet = Poledounsignedinteger16(buffer_2.kontrolnísoučet)
}
func (self *THlavička_uživatelského_datagramu) Nastavitbuffer(buffer_2 *TUživateldatagramprotocolheaderbuffer) {

	buffer_2.číslo_zdrojového_portu = Unsignedinteger16doPole(self.číslo_zdrojového_portu)
	buffer_2.číslo_cílového_portu = Unsignedinteger16doPole(self.číslo_cílového_portu)

	buffer_2.délka = Unsignedinteger16doPole(self.délka)
	buffer_2.kontrolnísoučet = Unsignedinteger16doPole(self.kontrolnísoučet)

}

type IUživateldatagramprotocolhandler interface {
	ÚchytkaUživateldatagramprotocolZpráva(socket *TKoncový_bod_uživatelských_datagramů, data uintptr, velikost uint16)
}

type TUživateldatagramprotocolhandler struct {
}

func (self *TUživateldatagramprotocolhandler) Init(backend TPoskytovatel_protokolu_propojených_sítí) {
}
func (self *TUživateldatagramprotocolhandler) ÚchytkaUživateldatagramprotocolZpráva(socket *TKoncový_bod_uživatelských_datagramů, data uintptr, velikost uint16) {
}

type IUživateldatagramprotocolsocket interface {
	ÚchytkaUživateldatagramprotocolZpráva(data uintptr, velikost uint16)
}
type TKoncový_bod_uživatelských_datagramů struct {
	vzdálenýportČíslo	uint16
	vzdálenýip		uint32
	místníportČíslo		uint16
	místníip		uint32

	listening	bool
}

var udpprovider TUživateldatagramprotocolprovider
var udphandler IUživateldatagramprotocolhandler

func (self *TKoncový_bod_uživatelských_datagramů) Otestovat() {
}
func (self *TKoncový_bod_uživatelských_datagramů) Init(pudpprovider TUživateldatagramprotocolprovider, pudphandler IUživateldatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TKoncový_bod_uživatelských_datagramů) ÚchytkaUživateldatagramprotocolZpráva(data uintptr, velikost uint16) {
	if udphandler != nil {
		udphandler.ÚchytkaUživateldatagramprotocolZpráva(self, data, velikost)
	}
}
func (self *TKoncový_bod_uživatelských_datagramů) Poslat(pdata []byte, velikost uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(velikost); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Poslat(self, data, velikost)
}
func (self *TKoncový_bod_uživatelských_datagramů) Odpojit() {
	udpprovider.Odpojit(self)
}

type TUživateldatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TKoncový_bod_uživatelských_datagramů
var číslosockets int
var volnéport uint16

func (self *TUživateldatagramprotocolprovider) Init(pipprovider TPoskytovatel_protokolu_propojených_sítí, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	číslosockets = 0
	volnéport = 1024
}
func (self *TUživateldatagramprotocolprovider) Internetprotocolreceivewhen(zdrojipAdresaSíťbyteorder uint32, cílipAdresaSíťbyteorder uint32, internetprotocolpayload uintptr, velikost uint32) bool {
	if velikost < udpheaderVelikost {
		return false
	}

	var buffer_2 *TUživateldatagramprotocolheaderbuffer = (*TUživateldatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg THlavička_uživatelského_datagramu
	msg.Init(buffer_2)

	var socket *TKoncový_bod_uživatelských_datagramů = nil

	for i := 0; i < číslosockets && socket == nil; i++ {
		if sockets[i].místníportČíslo == msg.číslo_cílového_portu && sockets[i].místníip == cílipAdresaSíťbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.vzdálenýportČíslo = msg.číslo_zdrojového_portu
			socket.vzdálenýip = zdrojipAdresaSíťbyteorder
		} else if sockets[i].místníportČíslo == msg.číslo_cílového_portu && sockets[i].místníip == cílipAdresaSíťbyteorder && sockets[i].vzdálenýportČíslo == msg.číslo_zdrojového_portu && sockets[i].vzdálenýip == zdrojipAdresaSíťbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Nastavitbuffer(buffer_2)
	if socket != nil {
		socket.ÚchytkaUživateldatagramprotocolZpráva(internetprotocolpayload+uintptr(udpheaderVelikost), uint16(velikost-udpheaderVelikost))
	}

	return false
}

func (self *TUživateldatagramprotocolprovider) Spojení(ip uint32, port uint16) *TKoncový_bod_uživatelských_datagramů {
	var paměťmanager = &TPaměťmanager{}
	var socket = (*TKoncový_bod_uživatelských_datagramů)(paměťmanager.Přidělit_paměť(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.vzdálenýportČíslo = port
		socket.vzdálenýip = ip
		socket.místníportČíslo = volnéport
		volnéport++
		socket.místníip = uint32((*iphandler.Providerget()).GetipAdresa())

		socket.vzdálenýportČíslo = Unsignedinteger16r(socket.vzdálenýportČíslo)
		socket.místníportČíslo = Unsignedinteger16r(socket.místníportČíslo)

		sockets[číslosockets] = *socket
		číslosockets++

	}
	return socket

}
func (self *TUživateldatagramprotocolprovider) Listen(port uint16) *TKoncový_bod_uživatelských_datagramů {
	var socket = &TKoncový_bod_uživatelských_datagramů{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.místníportČíslo = port
		socket.místníip = uint32((*iphandler.Providerget()).GetipAdresa())

		socket.místníportČíslo = Unsignedinteger16r(socket.místníportČíslo)
	}
	return socket
}
func (self *TUživateldatagramprotocolprovider) Odpojit(socket *TKoncový_bod_uživatelských_datagramů) {
	for i := 0; i < číslosockets && socket == nil; i++ {
		if sockets[i] == *socket {
			číslosockets--
			sockets[i] = sockets[číslosockets]
			break
		}
	}
}
func (self *TUživateldatagramprotocolprovider) Poslat(socket *TKoncový_bod_uživatelských_datagramů, pdata uintptr, velikost uint16) {
	var celkemDélka = uint32(velikost) + udpheaderVelikost

	var buffer_2 [4096]byte

	var msgbuffer = (*TUživateldatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = THlavička_uživatelského_datagramu{}

	msg.číslo_zdrojového_portu = socket.místníportČíslo
	msg.číslo_cílového_portu = socket.vzdálenýportČíslo
	msg.délka = Unsignedinteger16r(uint16(celkemDélka))

	msg.kontrolnísoučet = 0x0
	msg.Nastavitbuffer(msgbuffer)

	var dataBytů [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(velikost); i++ {
		buffer_2[int(udpheaderVelikost)+i] = dataBytů[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Poslat(socket.vzdálenýip, 0x11, data, celkemDélka)

}
func (self *TUživateldatagramprotocolprovider) Svázat(socket *TKoncový_bod_uživatelských_datagramů, handler *TUživateldatagramprotocolhandler) {
}
