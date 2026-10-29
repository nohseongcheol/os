/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package giao_thức_gói_tin_người_dùng

import . "unsafe"
import . "console"
import . "util"
import . "bộnhớmanager"
import . "giao_thức_mạng_liên_kết_4"

var udpconsole = TConsole{}

type TNgườidùngdatagramprotocolheaderbuffer struct {
	số_cổng_nguồn		[2]byte
	số_cổng_đích	[2]byte

	độdài		[2]byte
	checksum	[2]byte
}

var udpheaderCỡ uint32 = 8

type TĐầu_gói_tin_người_dùng struct {
	số_cổng_nguồn		uint16
	số_cổng_đích	uint16

	độdài		uint16
	checksum	uint16
}

func (mình *TĐầu_gói_tin_người_dùng) Init(buffer_2 *TNgườidùngdatagramprotocolheaderbuffer) {
	mình.số_cổng_nguồn = Mảngtounsignedinteger16(buffer_2.số_cổng_nguồn)
	mình.số_cổng_đích = Mảngtounsignedinteger16(buffer_2.số_cổng_đích)

	mình.độdài = Mảngtounsignedinteger16(buffer_2.độdài)
	mình.checksum = Mảngtounsignedinteger16(buffer_2.checksum)
}
func (mình *TĐầu_gói_tin_người_dùng) Đặtbuffer(buffer_2 *TNgườidùngdatagramprotocolheaderbuffer) {

	buffer_2.số_cổng_nguồn = Unsignedinteger16toMảng(mình.số_cổng_nguồn)
	buffer_2.số_cổng_đích = Unsignedinteger16toMảng(mình.số_cổng_đích)

	buffer_2.độdài = Unsignedinteger16toMảng(mình.độdài)
	buffer_2.checksum = Unsignedinteger16toMảng(mình.checksum)

}

type INgườidùngdatagramprotocolhandler interface {
	HandleNgườidùngdatagramprotocolthôngbáo(socket *TĐiểm_cuối_gói_tin_người_dùng, data uintptr, cỡ uint16)
}

type TNgườidùngdatagramprotocolhandler struct {
}

func (mình *TNgườidùngdatagramprotocolhandler) Init(backend TBộ_cung_cấp_giao_thức_mạng_liên_kết) {
}
func (mình *TNgườidùngdatagramprotocolhandler) HandleNgườidùngdatagramprotocolthôngbáo(socket *TĐiểm_cuối_gói_tin_người_dùng, data uintptr, cỡ uint16) {
}

type INgườidùngdatagramprotocolsocket interface {
	HandleNgườidùngdatagramprotocolthôngbáo(data uintptr, cỡ uint16)
}
type TĐiểm_cuối_gói_tin_người_dùng struct {
	từxaCổngSỐ	uint16
	từxaip		uint32
	cụcbộCổngSỐ	uint16
	cụcbộip		uint32

	listening	bool
}

var udpprovider TNgườidùngdatagramprotocolprovider
var udphandler INgườidùngdatagramprotocolhandler

func (mình *TĐiểm_cuối_gói_tin_người_dùng) Thử() {
}
func (mình *TĐiểm_cuối_gói_tin_người_dùng) Init(pudpprovider TNgườidùngdatagramprotocolprovider, pudphandler INgườidùngdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	mình.listening = false
}
func (mình *TĐiểm_cuối_gói_tin_người_dùng) HandleNgườidùngdatagramprotocolthôngbáo(data uintptr, cỡ uint16) {
	if udphandler != nil {
		udphandler.HandleNgườidùngdatagramprotocolthôngbáo(mình, data, cỡ)
	}
}
func (mình *TĐiểm_cuối_gói_tin_người_dùng) Gởi(pdata []byte, cỡ uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(cỡ); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Gởi(mình, data, cỡ)
}
func (mình *TĐiểm_cuối_gói_tin_người_dùng) Ngắtkếtnối() {
	udpprovider.Ngắtkếtnối(mình)
}

type TNgườidùngdatagramprotocolprovider struct {
}

var iphandler IMạngprotocolhandler
var sockets [65535]TĐiểm_cuối_gói_tin_người_dùng
var sỐsockets int
var rảnhCổng uint16

func (mình *TNgườidùngdatagramprotocolprovider) Init(pipprovider TBộ_cung_cấp_giao_thức_mạng_liên_kết, piphandler IMạngprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	sỐsockets = 0
	rảnhCổng = 1024
}
func (mình *TNgườidùngdatagramprotocolprovider) Mạngprotocolreceivewhen(mãnguồnipaddressMạngbyteorder uint32, destinationipaddressMạngbyteorder uint32, mạngprotocolpayload uintptr, cỡ uint32) bool {
	if cỡ < udpheaderCỡ {
		return false
	}

	var buffer_2 *TNgườidùngdatagramprotocolheaderbuffer = (*TNgườidùngdatagramprotocolheaderbuffer)(Pointer(mạngprotocolpayload))
	var msg TĐầu_gói_tin_người_dùng
	msg.Init(buffer_2)

	var socket *TĐiểm_cuối_gói_tin_người_dùng = nil

	for i := 0; i < sỐsockets && socket == nil; i++ {
		if sockets[i].cụcbộCổngSỐ == msg.số_cổng_đích && sockets[i].cụcbộip == destinationipaddressMạngbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.từxaCổngSỐ = msg.số_cổng_nguồn
			socket.từxaip = mãnguồnipaddressMạngbyteorder
		} else if sockets[i].cụcbộCổngSỐ == msg.số_cổng_đích && sockets[i].cụcbộip == destinationipaddressMạngbyteorder && sockets[i].từxaCổngSỐ == msg.số_cổng_nguồn && sockets[i].từxaip == mãnguồnipaddressMạngbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Đặtbuffer(buffer_2)
	if socket != nil {
		socket.HandleNgườidùngdatagramprotocolthôngbáo(mạngprotocolpayload+uintptr(udpheaderCỡ), uint16(cỡ-udpheaderCỡ))
	}

	return false
}

func (mình *TNgườidùngdatagramprotocolprovider) Kếtnối(ip uint32, cổng uint16) *TĐiểm_cuối_gói_tin_người_dùng {
	var bộnhớmanager = &TBộnhớmanager{}
	var socket = (*TĐiểm_cuối_gói_tin_người_dùng)(bộnhớmanager.Cấp_phát_bộ_nhớ(50))

	if socket != nil {

		socket.Init(*mình, nil)
		socket.từxaCổngSỐ = cổng
		socket.từxaip = ip
		socket.cụcbộCổngSỐ = rảnhCổng
		rảnhCổng++
		socket.cụcbộip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.từxaCổngSỐ = Unsignedinteger16r(socket.từxaCổngSỐ)
		socket.cụcbộCổngSỐ = Unsignedinteger16r(socket.cụcbộCổngSỐ)

		sockets[sỐsockets] = *socket
		sỐsockets++

	}
	return socket

}
func (mình *TNgườidùngdatagramprotocolprovider) Listen(cổng uint16) *TĐiểm_cuối_gói_tin_người_dùng {
	var socket = &TĐiểm_cuối_gói_tin_người_dùng{}
	socket = nil
	if socket != nil {
		socket.Init(*mình, nil)
		socket.listening = true
		socket.cụcbộCổngSỐ = cổng
		socket.cụcbộip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.cụcbộCổngSỐ = Unsignedinteger16r(socket.cụcbộCổngSỐ)
	}
	return socket
}
func (mình *TNgườidùngdatagramprotocolprovider) Ngắtkếtnối(socket *TĐiểm_cuối_gói_tin_người_dùng) {
	for i := 0; i < sỐsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			sỐsockets--
			sockets[i] = sockets[sỐsockets]
			break
		}
	}
}
func (mình *TNgườidùngdatagramprotocolprovider) Gởi(socket *TĐiểm_cuối_gói_tin_người_dùng, pdata uintptr, cỡ uint16) {
	var tổngĐộdài = uint32(cỡ) + udpheaderCỡ

	var buffer_2 [4096]byte

	var msgbuffer = (*TNgườidùngdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TĐầu_gói_tin_người_dùng{}

	msg.số_cổng_nguồn = socket.cụcbộCổngSỐ
	msg.số_cổng_đích = socket.từxaCổngSỐ
	msg.độdài = Unsignedinteger16r(uint16(tổngĐộdài))

	msg.checksum = 0x0
	msg.Đặtbuffer(msgbuffer)

	var dataByte [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(cỡ); i++ {
		buffer_2[int(udpheaderCỡ)+i] = dataByte[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Gởi(socket.từxaip, 0x11, data, tổngĐộdài)

}
func (mình *TNgườidùngdatagramprotocolprovider) Bind(socket *TĐiểm_cuối_gói_tin_người_dùng, handler *TNgườidùngdatagramprotocolhandler,) {
}
