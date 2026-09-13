package giao_thức_thông_điệp_điều_khiển_mạng_liên_kết

import . "unsafe"
import . "console"
import . "bộnhớmanager"
import . "khung_mạng_dùng_chung_môi_trường_truyền"
import . "giao_thức_mạng_liên_kết_4"
import . "util"

var icmpconsole = TConsole{}

type TMạngĐiềukhiểnthôngbáoprotocolthôngbáobuffer struct {
	Kiểu	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpCỡ int = 64

type TMạngĐiềukhiểnthôngbáoprotocolthôngbáo struct {
	Kiểu	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (mình *TMạngĐiềukhiểnthôngbáoprotocolthôngbáo) Init(buffer_2 TMạngĐiềukhiểnthôngbáoprotocolthôngbáobuffer) {
	mình.Kiểu = buffer_2.Kiểu
	mình.code = buffer_2.code

	mình.checksum = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.checksum))
	mình.data = Unsignedinteger32r(Mảngtounsignedinteger32(buffer_2.data))
}

func (mình *TMạngĐiềukhiểnthôngbáoprotocolthôngbáo) Đặtbuffer(buffer_2 *TMạngĐiềukhiểnthôngbáoprotocolthôngbáobuffer) {
	buffer_2.Kiểu = mình.Kiểu
	buffer_2.code = mình.code

	buffer_2.checksum = Unsignedinteger16toMảng(mình.checksum)
	buffer_2.data = Unsignedinteger32toMảng(mình.data)
}

type Icmphandler struct {
	TMạngprotocolhandler
}

var giao_thức_thông_điệp_điều_khiển_mạng_liên_kết *TGiao_thức_thông_điệp_điều_khiển_mạng_liên_kết

func (mình *Icmphandler) Mạngprotocolreceivewhen(mãnguồnipaddressMạngbyteorder uint32, destinationipaddressMạngbyteorder uint32, dataContrỏ uintptr, cỡ uint32) bool {
	return giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.Mạngprotocolreceivewhen(mãnguồnipaddressMạngbyteorder, destinationipaddressMạngbyteorder, dataContrỏ, cỡ)
}

var iphandler IMạngprotocolhandler

type TGiao_thức_thông_điệp_điều_khiển_mạng_liên_kết struct {
}

func (mình *TGiao_thức_thông_điệp_điều_khiển_mạng_liên_kết) Init(backend TBộ_cung_cấp_giao_thức_mạng_liên_kết, handler IMạngprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết = mình
}
func (mình *TGiao_thức_thông_điệp_điều_khiển_mạng_liên_kết) Mạngprotocolreceivewhen(mãnguồnipaddressMạngbyteorder uint32, destinationipaddressMạngbyteorder uint32, dataContrỏ uintptr, cỡ uint32) bool {
	if cỡ < uint32(icmpCỡ) {
		return false
	}

	var buffer_2 *TMạngĐiềukhiểnthôngbáoprotocolthôngbáobuffer = (*TMạngĐiềukhiểnthôngbáoprotocolthôngbáobuffer)(Pointer(dataContrỏ))
	var msg TMạngĐiềukhiểnthôngbáoprotocolthôngbáo = TMạngĐiềukhiểnthôngbáoprotocolthôngbáo{}
	msg.Init(*buffer_2)

	icmpconsole.MIn(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16In(uint16(msg.Kiểu))
	icmpconsole.MIn(([]byte)(":"))

	switch msg.Kiểu {
	case 0:
		icmpconsole.MIn(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MIn(([]byte)("ping send "))
		msg.Kiểu = 0

		msg.checksum = 0
		msg.Đặtbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataContrỏ)), uint32(icmpCỡ))

		msg.Đặtbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (mình *TGiao_thức_thông_điệp_điều_khiển_mạng_liên_kết) EchorequestGởi(ipMạngbyteorder uint32) bool {
	var giao_thức_thông_điệp_điều_khiển_mạng_liên_kết TMạngĐiềukhiểnthôngbáoprotocolthôngbáo = TMạngĐiềukhiểnthôngbáoprotocolthôngbáo{}

	var bộnhớmanager = &TBộnhớmanager{}
	var buffer_2 = (*TMạngĐiềukhiểnthôngbáoprotocolthôngbáobuffer)(bộnhớmanager.Cấp_phát_bộ_nhớ(1024))

	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.Kiểu = 8
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.code = 0
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.data = 0x3713
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.checksum = 0
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.Đặtbuffer(buffer_2)
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpCỡ))
	giao_thức_thông_điệp_điều_khiển_mạng_liên_kết.Đặtbuffer(buffer_2)

	var dataContrỏ uintptr = uintptr(Pointer(buffer_2))
	iphandler.Gởi(ipMạngbyteorder, 0x01, dataContrỏ, uint32(icmpCỡ))

	return false

}
