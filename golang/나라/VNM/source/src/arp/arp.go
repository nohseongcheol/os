/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "khung_mạng_dùng_chung_môi_trường_truyền"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpthôngbáobuffer struct {
	phầncứngKiểu		[2]byte
	protocol		[2]byte
	phầncứngaddressCỡ	byte
	protocoladdressCỡ	byte
	lệnh			[2]byte

	mãnguồnmacaddress	[6]byte
	mãnguồnipaddress	[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgCỡ uint32 = (64+92+64)/8 + 2

type Arpthôngbáo struct {
	phầncứngKiểu		uint16
	protocol		uint16
	phầncứngaddressCỡ	uint8
	protocoladdressCỡ	uint8
	lệnh			uint16

	mãnguồnmacaddress	uint64
	mãnguồnipaddress	uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (mình *Arpthôngbáo) Init(buffer_2 *Arpthôngbáobuffer) {

	mình.phầncứngKiểu = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.phầncứngKiểu))
	mình.protocol = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.protocol))
	mình.phầncứngaddressCỡ = byte(buffer_2.phầncứngaddressCỡ)
	mình.protocoladdressCỡ = byte(buffer_2.protocoladdressCỡ)
	mình.lệnh = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.lệnh))

	mình.mãnguồnmacaddress = Unsignedinteger48r(Mảngtounsignedinteger48(buffer_2.mãnguồnmacaddress))
	mình.mãnguồnipaddress = Unsignedinteger32r(Mảngtounsignedinteger32(buffer_2.mãnguồnipaddress))
	mình.destinationmacaddress = Unsignedinteger48r(Mảngtounsignedinteger48(buffer_2.destinationmacaddress))
	mình.destinationipaddress = Unsignedinteger32r(Mảngtounsignedinteger32(buffer_2.destinationipaddress))
}
func (mình *Arpthôngbáo) Đặtbuffer(buffer_2 *Arpthôngbáobuffer) {
	buffer_2.phầncứngKiểu = Unsignedinteger16toMảng(mình.phầncứngKiểu)
	buffer_2.protocol = Unsignedinteger16toMảng(mình.protocol)
	buffer_2.phầncứngaddressCỡ = uint8(mình.phầncứngaddressCỡ)
	buffer_2.protocoladdressCỡ = uint8(mình.protocoladdressCỡ)

	buffer_2.lệnh = Unsignedinteger16toMảng(mình.lệnh)
	buffer_2.mãnguồnmacaddress = Unsignedinteger48toMảng(mình.mãnguồnmacaddress)
	buffer_2.mãnguồnipaddress = Unsignedinteger32toMảng(mình.mãnguồnipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toMảng(mình.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toMảng(mình.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var bộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền

func (mình *Arpethernetframehandler) Ethernetframereceivewhen(dataContrỏ uintptr, cỡ int) bool {
	arpconsole.MInxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(dataContrỏ, uint32(cỡ))

}
func (mình *Arpethernetframehandler) Gởi(destinationmacbe uint64, dataContrỏ uintptr, cỡ uint32) {
	arpconsole.MInxy([]byte("arp send:"), 0, 24)
	var ethernetKiểube = Unsignedinteger16r(0x0806)
	mình.TEthernetframehandler.FrameGởi(destinationmacbe, ethernetKiểube, dataContrỏ, cỡ)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	sỐcacheentry	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (mình *Arpprovider) Init(backend TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Đặthandler(userhandler, 0x0806)
	mình.sỐcacheentry = 0
	arpprovider = *mình

}

func (mình *Arpprovider) Ethernetframereceivewhen(dataContrỏ uintptr, cỡ uint32) bool {

	if cỡ < arpmesgCỡ {
		return false
	}
	var arpbuffer *Arpthôngbáobuffer = (*Arpthôngbáobuffer)(Pointer(dataContrỏ))
	var arp Arpthôngbáo = Arpthôngbáo{}
	arp.Init(arpbuffer)

	if arp.phầncứngKiểu == 0x0100 {

		if arp.protocol == 0x0008 && arp.phầncứngaddressCỡ == 6 && arp.protocoladdressCỡ == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MIn([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16In(arp.protocol)
			arpconsole.MIn([]byte(":"))
			arpconsole.MUnsignedinteger64In(uint64(arp.destinationmacaddress))
			arpconsole.MIn([]byte(":"))
			arpconsole.MUnsignedinteger16In(arp.lệnh)
			arpconsole.MIn([]byte(":"))
			arpconsole.MUnsignedinteger64In(handler.Getmacaddress())

			switch arp.lệnh {
			case 0x0100:

				if mình.Getmacfromcache(arp.mãnguồnipaddress) == 0xFFFFFFFFFFFF {
					if mình.sỐcacheentry < 128 {
						mình.Ipcache[mình.sỐcacheentry] = arp.mãnguồnipaddress
						mình.Maccache[mình.sỐcacheentry] = arp.mãnguồnmacaddress
						mình.sỐcacheentry++
					}
				}
				arp.lệnh = 0x0200
				arp.destinationipaddress = arp.mãnguồnipaddress
				arp.destinationmacaddress = arp.mãnguồnmacaddress
				arp.mãnguồnipaddress = uint32(handler.Getipaddress())
				arp.mãnguồnmacaddress = handler.Getmacaddress()
				arp.Đặtbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MIn(([]byte)("self.numCacheEntries"))

				if mình.sỐcacheentry < 128 {
					mình.Ipcache[mình.sỐcacheentry] = arp.mãnguồnipaddress
					mình.Maccache[mình.sỐcacheentry] = arp.mãnguồnmacaddress
					mình.sỐcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (mình *Arpprovider) Broadcastmacaddress(IpMạngbyteorder uint32) {

	var arp Arpthôngbáo = Arpthôngbáo{}
	arp.phầncứngKiểu = 0x0100
	arp.protocol = 0x0008
	arp.phầncứngaddressCỡ = 6
	arp.protocoladdressCỡ = 4
	arp.lệnh = 0x0200

	arp.mãnguồnipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = mình.Resolve(IpMạngbyteorder)
	arp.destinationipaddress = IpMạngbyteorder
	arpconsole.MInxy([]byte("broad mac"), 0, 15)

	arp.mãnguồnmacaddress = handler.Getmacaddress()

	var arpbuffer Arpthôngbáobuffer = Arpthôngbáobuffer{}
	arp.Đặtbuffer(&arpbuffer)

	var tham_chiếu_địa_chỉ uintptr = uintptr(Pointer(&arpbuffer))
	handler.Gởi(arp.destinationmacaddress, tham_chiếu_địa_chỉ, arpmesgCỡ)
}
func (mình *Arpprovider) Requestmacaddress(IpMạngbyteorder uint32) {

	var arp Arpthôngbáo = Arpthôngbáo{}
	arp.phầncứngKiểu = 0x0100

	arp.protocol = 0x0008
	arp.phầncứngaddressCỡ = 6
	arp.protocoladdressCỡ = 4
	arp.lệnh = 0x0100

	arp.mãnguồnmacaddress = handler.Getmacaddress()
	arp.mãnguồnipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpMạngbyteorder

	var arpbuffer Arpthôngbáobuffer = Arpthôngbáobuffer{}
	arp.Đặtbuffer(&arpbuffer)

	var tham_chiếu_địa_chỉ uintptr = uintptr(Pointer(&arpbuffer))
	handler.Gởi(arp.destinationmacaddress, tham_chiếu_địa_chỉ, arpmesgCỡ)
}
func (mình *Arpprovider) ThửIn(data *[]byte, cỡ uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MInxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalIn(buffer_2[i])
		arpconsole.MIn([]byte(":"))
	}
	arpconsole.MIn([]byte("]"))
}

func (mình *Arpprovider) Getmacfromcache(IpMạngbyteorder uint32) uint64 {
	for i := 0; i < mình.sỐcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MIn(([]byte)("["))
		arpconsole.MUnsignedinteger32In(mình.Ipcache[i])
		arpconsole.MIn(([]byte)(":"))
		arpconsole.MUnsignedinteger32In(IpMạngbyteorder)
		arpconsole.MIn(([]byte)(":"))
		arpconsole.MIn(([]byte)(":"))
		arpconsole.MUnsignedinteger64In(mình.Maccache[i])
		arpconsole.MIn(([]byte)("]\n"))

		if mình.Ipcache[i] == IpMạngbyteorder {
			arpconsole.MIn([]byte("getmacfromcache"))
			return mình.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (mình *Arpprovider) Resolve(IpMạngbyteorder uint32) uint64 {
	var result uint64 = mình.Getmacfromcache(IpMạngbyteorder)
	if result == 0xFFFFFFFFFFFF {
		mình.Requestmacaddress(IpMạngbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = mình.Getmacfromcache(IpMạngbyteorder)

	}

	return result
}
