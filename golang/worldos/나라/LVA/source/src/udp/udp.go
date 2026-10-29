/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "atmiņamanager"
import . "ipv4"

var udpconsole = TConsole{}

type TLietotājsdatagramprotocolheaderbuffer struct {
	avotsPortsSkaitlis	[2]byte
	mērķisPortsSkaitlis	[2]byte

	garums		[2]byte
	checksum	[2]byte
}

var udpheaderIzmērs uint32 = 8

type TLietotājsdatagramprotocolheader struct {
	avotsPortsSkaitlis	uint16
	mērķisPortsSkaitlis	uint16

	garums		uint16
	checksum	uint16
}

func (pats *TLietotājsdatagramprotocolheader) Init(buffer_2 *TLietotājsdatagramprotocolheaderbuffer) {
	pats.avotsPortsSkaitlis = Masīvstounsignedinteger16(buffer_2.avotsPortsSkaitlis)
	pats.mērķisPortsSkaitlis = Masīvstounsignedinteger16(buffer_2.mērķisPortsSkaitlis)

	pats.garums = Masīvstounsignedinteger16(buffer_2.garums)
	pats.checksum = Masīvstounsignedinteger16(buffer_2.checksum)
}
func (pats *TLietotājsdatagramprotocolheader) Kopabuffer(buffer_2 *TLietotājsdatagramprotocolheaderbuffer) {

	buffer_2.avotsPortsSkaitlis = Unsignedinteger16toMasīvs(pats.avotsPortsSkaitlis)
	buffer_2.mērķisPortsSkaitlis = Unsignedinteger16toMasīvs(pats.mērķisPortsSkaitlis)

	buffer_2.garums = Unsignedinteger16toMasīvs(pats.garums)
	buffer_2.checksum = Unsignedinteger16toMasīvs(pats.checksum)

}

type ILietotājsdatagramprotocolhandler interface {
	HandleLietotājsdatagramprotocolZiņojums(ligzda *TLietotājsdatagramprotocolLigzda, data uintptr, izmērs uint16)
}

type TLietotājsdatagramprotocolhandler struct {
}

func (pats *TLietotājsdatagramprotocolhandler) Init(backend TInternetsprotocolprovider) {
}
func (pats *TLietotājsdatagramprotocolhandler) HandleLietotājsdatagramprotocolZiņojums(ligzda *TLietotājsdatagramprotocolLigzda, data uintptr, izmērs uint16) {
}

type ILietotājsdatagramprotocolLigzda interface {
	HandleLietotājsdatagramprotocolZiņojums(data uintptr, izmērs uint16)
}
type TLietotājsdatagramprotocolLigzda struct {
	remotePortsSkaitlis	uint16
	remoteip		uint32
	vietējaisPortsSkaitlis	uint16
	vietējaisip		uint32

	listening	bool
}

var udpprovider TLietotājsdatagramprotocolprovider
var udphandler ILietotājsdatagramprotocolhandler

func (pats *TLietotājsdatagramprotocolLigzda) Pārbaudīt() {
}
func (pats *TLietotājsdatagramprotocolLigzda) Init(pudpprovider TLietotājsdatagramprotocolprovider, pudphandler ILietotājsdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	pats.listening = false
}
func (pats *TLietotājsdatagramprotocolLigzda) HandleLietotājsdatagramprotocolZiņojums(data uintptr, izmērs uint16) {
	if udphandler != nil {
		udphandler.HandleLietotājsdatagramprotocolZiņojums(pats, data, izmērs)
	}
}
func (pats *TLietotājsdatagramprotocolLigzda) Sūtīt(pdata []byte, izmērs uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(izmērs); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Sūtīt(pats, data, izmērs)
}
func (pats *TLietotājsdatagramprotocolLigzda) Atvienoties() {
	udpprovider.Atvienoties(pats)
}

type TLietotājsdatagramprotocolprovider struct {
}

var iphandler IInternetsprotocolhandler
var sockets [65535]TLietotājsdatagramprotocolLigzda
var skaitlissockets int
var brīvsPorts uint16

func (pats *TLietotājsdatagramprotocolprovider) Init(pipprovider TInternetsprotocolprovider, piphandler IInternetsprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	skaitlissockets = 0
	brīvsPorts = 1024
}
func (pats *TLietotājsdatagramprotocolprovider) Internetsprotocolreceivewhen(avotsipaddressTīklsbyteorder uint32, mērķisipaddressTīklsbyteorder uint32, internetsprotocolpayload uintptr, izmērs uint32) bool {
	if izmērs < udpheaderIzmērs {
		return false
	}

	var buffer_2 *TLietotājsdatagramprotocolheaderbuffer = (*TLietotājsdatagramprotocolheaderbuffer)(Pointer(internetsprotocolpayload))
	var msg TLietotājsdatagramprotocolheader
	msg.Init(buffer_2)

	var ligzda *TLietotājsdatagramprotocolLigzda = nil

	for i := 0; i < skaitlissockets && ligzda == nil; i++ {
		if sockets[i].vietējaisPortsSkaitlis == msg.mērķisPortsSkaitlis && sockets[i].vietējaisip == mērķisipaddressTīklsbyteorder && sockets[i].listening == true {
			ligzda = &sockets[i]
			ligzda.listening = false
			ligzda.remotePortsSkaitlis = msg.avotsPortsSkaitlis
			ligzda.remoteip = avotsipaddressTīklsbyteorder
		} else if sockets[i].vietējaisPortsSkaitlis == msg.mērķisPortsSkaitlis && sockets[i].vietējaisip == mērķisipaddressTīklsbyteorder && sockets[i].remotePortsSkaitlis == msg.avotsPortsSkaitlis && sockets[i].remoteip == avotsipaddressTīklsbyteorder {
			ligzda = &sockets[i]

		}
	}

	msg.Kopabuffer(buffer_2)
	if ligzda != nil {
		ligzda.HandleLietotājsdatagramprotocolZiņojums(internetsprotocolpayload+uintptr(udpheaderIzmērs), uint16(izmērs-udpheaderIzmērs))
	}

	return false
}

func (pats *TLietotājsdatagramprotocolprovider) Savienoties(ip uint32, ports uint16) *TLietotājsdatagramprotocolLigzda {
	var atmiņamanager = &TAtmiņamanager{}
	var ligzda = (*TLietotājsdatagramprotocolLigzda)(atmiņamanager.Malloc(50))

	if ligzda != nil {

		ligzda.Init(*pats, nil)
		ligzda.remotePortsSkaitlis = ports
		ligzda.remoteip = ip
		ligzda.vietējaisPortsSkaitlis = brīvsPorts
		brīvsPorts++
		ligzda.vietējaisip = uint32((*iphandler.Providerget()).Getipaddress())

		ligzda.remotePortsSkaitlis = Unsignedinteger16r(ligzda.remotePortsSkaitlis)
		ligzda.vietējaisPortsSkaitlis = Unsignedinteger16r(ligzda.vietējaisPortsSkaitlis)

		sockets[skaitlissockets] = *ligzda
		skaitlissockets++

	}
	return ligzda

}
func (pats *TLietotājsdatagramprotocolprovider) Listen(ports uint16) *TLietotājsdatagramprotocolLigzda {
	var ligzda = &TLietotājsdatagramprotocolLigzda{}
	ligzda = nil
	if ligzda != nil {
		ligzda.Init(*pats, nil)
		ligzda.listening = true
		ligzda.vietējaisPortsSkaitlis = ports
		ligzda.vietējaisip = uint32((*iphandler.Providerget()).Getipaddress())

		ligzda.vietējaisPortsSkaitlis = Unsignedinteger16r(ligzda.vietējaisPortsSkaitlis)
	}
	return ligzda
}
func (pats *TLietotājsdatagramprotocolprovider) Atvienoties(ligzda *TLietotājsdatagramprotocolLigzda) {
	for i := 0; i < skaitlissockets && ligzda == nil; i++ {
		if sockets[i] == *ligzda {
			skaitlissockets--
			sockets[i] = sockets[skaitlissockets]
			break
		}
	}
}
func (pats *TLietotājsdatagramprotocolprovider) Sūtīt(ligzda *TLietotājsdatagramprotocolLigzda, pdata uintptr, izmērs uint16) {
	var kopāGarums = uint32(izmērs) + udpheaderIzmērs

	var buffer_2 [4096]byte

	var msgbuffer = (*TLietotājsdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TLietotājsdatagramprotocolheader{}

	msg.avotsPortsSkaitlis = ligzda.vietējaisPortsSkaitlis
	msg.mērķisPortsSkaitlis = ligzda.remotePortsSkaitlis
	msg.garums = Unsignedinteger16r(uint16(kopāGarums))

	msg.checksum = 0x0
	msg.Kopabuffer(msgbuffer)

	var dataBaiti [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(izmērs); i++ {
		buffer_2[int(udpheaderIzmērs)+i] = dataBaiti[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Sūtīt(ligzda.remoteip, 0x11, data, kopāGarums)

}
func (pats *TLietotājsdatagramprotocolprovider) Bind(ligzda *TLietotājsdatagramprotocolLigzda, handler *TLietotājsdatagramprotocolhandler) {
}
