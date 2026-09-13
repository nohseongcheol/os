package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegNgườidùngcode	uint32	= 0x23
	SegNgườidùngdata	uint32	= 0x2B
	SegNgườidùnggs		uint32	= 0x33
	SegTácvụTrạngthái	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	giớihạnThấp_2	uint16
	baseThấp_2	uint16
	baseCao_2	uint8
	kiểu		uint8
	cờGiớihạnCao	uint8
	baseveryCao	uint8
}

func (mình_2 *TSegmentdescriptor) Init(base_2 uint32, giớihạn_2 uint32, kiểu uint8, cờ_2 uint8) {

	mình_2.baseThấp_2 = uint16(base_2 & 0xFFFF)
	mình_2.baseCao_2 = uint8((base_2 >> 16) & 0xFF)
	mình_2.baseveryCao = uint8((base_2 >> 24) & 0xFF)

	mình_2.giớihạnThấp_2 = uint16(giớihạn_2 & 0xFFFF)
	mình_2.cờGiớihạnCao = uint8((giớihạn_2 >> 24) & 0x0F)
	mình_2.cờGiớihạnCao |= (cờ_2 & 0xF0)

	mình_2.kiểu = kiểu

}

type TShareddescriptorBảngdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorBảngdata

type TShareddescriptorBảng struct {
}

func (mình_2 *TShareddescriptorBảng) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressThấp) |
		uint32(gdtdescriptor.GdtaddressCao)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtCỡ+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destination_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destination_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	cỡ_2 := (*uint16)(Pointer(&destination_3[0]))
	(*cỡ_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MInxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32In(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (mình_2 *TShareddescriptorBảng) Đặtdescriptor(idx int, base_2 uint32, giớihạn_2 uint32, kiểu uint8, cờ_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, giớihạn_2, kiểu, cờ_2)
}

const (
	KcsChỉmục	= 1
	KdsChỉmục	= 2
	KgsChỉmục	= 3

	Kcsselector	= KcsChỉmục * 8
	Kdsselector	= KdsChỉmục * 8
	Kgsselector	= KgsChỉmục * 8

	Seggranbyte	= 0 << 7
	Seggran4kTrang	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegHệthống	= 0 << 4
	SegBìnhthường	= 1 << 4

	Segnoexec	= 0 << 3
	SegChạy		= 1 << 3

	Privkernel	= 0 << 5
	PrivNgườidùng	= 3 << 5

	SegbigChếđộ	= 1 << 6

	Có	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescMụclục		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescGiớihạnVàoTrang	= 1 << 4
	UdescsegnotCó		= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsChạy		= 16
)

var (
	gdtBảng		= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtBảnglen	= 0
)

type Gdtentry_2 struct {
	giớihạnThấp	uint16
	baseThấp	uint16
	basemid		uint8
	truycập		uint8
	giớihạnCaovàCờ	uint8
	baseCao		uint8
}

func (e *Gdtentry_2) IsCó() bool {
	return e.truycập&Có != 0
}

func (e *Gdtentry_2) Fill(base uint32, giớihạn uint32, truycập uint8, cờ uint8) {
	e.giớihạnCaovàCờ = uint8((giớihạn >> 16) & 0x000F)
	e.giớihạnCaovàCờ |= cờ
	e.truycập = truycập
	e.basemid = uint8(base >> 16)
	e.baseCao = uint8(base >> 24)
	e.baseThấp = uint16(base & 0xFFFF)
	e.giớihạnThấp = uint16(giớihạn & 0x0000FFFF)
}

func (e *Gdtentry_2) Xoá() {
	e.giớihạnCaovàCờ = 0
	e.truycập = 0
	e.basemid = 0
	e.baseCao = 0
	e.baseThấp = 0
	e.giớihạnThấp = 0

}

type Gdtdescriptor struct {
	GdtCỡ		uint16
	GdtaddressThấp	uint16
	GdtaddressCao	uint16
}
type Ngườidùngdescriptor struct {
	EntrySỐ		uint32
	Baseaddress	uint32
	Giớihạn		uint32
	Cờ		uint8
}

func Đặttlssegment(chỉmục uint32, descriptor *Ngườidùngdescriptor, bảng []Gdtentry_2) bool {
	if chỉmục < TlsChạy || chỉmục > uint32(len(gdtBảng)) {
		return false
	}

	if descriptor.Cờ == Udescrxonly|UdescsegnotCó {

		bảng[chỉmục].Xoá()
		return true
	}

	cờ := uint8(Seggranbyte)
	if descriptor.Cờ&UdescGiớihạnVàoTrang != 0 {
		cờ = Seggran4kTrang
	}
	truycập := uint8(PrivNgườidùng | SegBìnhthường | Có)
	if descriptor.Cờ&Udescrxonly != 0 {
		truycập |= SegChạy
	} else {
		truycập |= Segw
	}
	if truycập&SegBìnhthường != 0 {
		cờ |= SegbigChếđộ
	}

	bảng[chỉmục].Fill(descriptor.Baseaddress, descriptor.Giớihạn, truycập, cờ)
	flushtlsBảng(bảng)

	return true
}

func flushtlsBảng(bảng []Gdtentry_2) {
	copy(gdtBảng[TlsChạy:], bảng[TlsChạy:])
}
func FlushtlsBảng(bảng []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsChạy:], bảng[TlsChạy:])
}
