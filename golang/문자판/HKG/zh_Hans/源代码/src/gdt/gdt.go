package gdt

import . "unsafe"
import "reflect"
import . "控制台"

const (
	Seg内核code	uint32	= 0x08
	Seg内核数据		uint32	= 0x10
	Seg内核gs		uint32	= 0x18

	Seg用户code	uint32	= 0x23
	Seg用户数据	uint32	= 0x2B
	Seg用户gs	uint32	= 0x33
	Seg任务状态		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	限定低_2		uint16
	base低_2		uint16
	base高_2		uint8
	类型		uint8
	标志限定高		uint8
	basevery高	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, 限定_2 uint32, 类型 uint8, 标志_2 uint8) {

	self_2.base低_2 = uint16(base_2 & 0xFFFF)
	self_2.base高_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.basevery高 = uint8((base_2 >> 24) & 0xFF)

	self_2.限定低_2 = uint16(限定_2 & 0xFFFF)
	self_2.标志限定高 = uint8((限定_2 >> 24) & 0x0F)
	self_2.标志限定高 |= (标志_2 & 0xF0)

	self_2.类型 = 类型

}

type TShareddescriptor表格数据 struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var 数据_2 TShareddescriptor表格数据

type TShareddescriptor表格 struct {
}

func (self_2 *TShareddescriptor表格) Init() {

	var gdt条目 TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddress低) |
		uint32(gdtdescriptor.Gdtaddress高)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdt大小+1) / Sizeof(gdt条目))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(数据_2.segmentdescriptor[:], oldgdt)

	数据_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	数据_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	数据_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	目的_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&目的_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&数据_2)))

	大小_2 := (*uint16)(Pointer(&目的_3[0]))
	(*大小_2) = (uint16)((Sizeof(数据_2)))

	gdtfunc(uintptr(Pointer(&目的_3)))

	terminal := new(T控制台)
	terminal.M打印xy("gdt:", 1, 4)
	terminal.MUnsignedinteger32打印(uint32(uintptr(Pointer(&数据_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptor表格) S集合descriptor(idx int, base_2 uint32, 限定_2 uint32, 类型 uint8, 标志_2 uint8) {
	数据_2.segmentdescriptor[idx].Init(base_2, 限定_2, 类型, 标志_2)
}

const (
	Kcs索引	= 1
	Kds索引	= 2
	Kgs索引	= 3

	Kcsselector	= Kcs索引 * 8
	Kdsselector	= Kds索引 * 8
	Kgsselector	= Kgs索引 * 8

	Seggran字节	= 0 << 7
	Seggran4k页	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Seg系统	= 0 << 4
	Seg正常	= 1 << 4

	Segnoexec	= 0 << 3
	Seg执行		= 1 << 3

	Priv内核	= 0 << 5
	Priv用户	= 3 << 5

	Segbig模式	= 1 << 6

	P当前电池	= 1 << 7

	Udesc32seg	= 1 << 0
	Udesc目录		= 3 << 1
	Udescrx仅用	= 1 << 3
	Udesc限定进pages	= 1 << 4
	Udescsegnot当前电池	= 1 << 5
	Udescusable	= 1 << 6

	Gdt条目	= 256
	Tls开始	= 16
)

var (
	gdt表格	= [Gdt条目]Gdt条目_2{}
	gdtdescriptor	Gdtdescriptor
	gdt表格len	= 0
)

type Gdt条目_2 struct {
	限定低	uint16
	base低	uint16
	basemid	uint8
	访问	uint8
	限定高与标志	uint8
	base高	uint8
}

func (e *Gdt条目_2) Is当前电池() bool {
	return e.访问&P当前电池 != 0
}

func (e *Gdt条目_2) Fill(base uint32, 限定 uint32, 访问 uint8, 标志 uint8) {
	e.限定高与标志 = uint8((限定 >> 16) & 0x000F)
	e.限定高与标志 |= 标志
	e.访问 = 访问
	e.basemid = uint8(base >> 16)
	e.base高 = uint8(base >> 24)
	e.base低 = uint16(base & 0xFFFF)
	e.限定低 = uint16(限定 & 0x0000FFFF)
}

func (e *Gdt条目_2) C清除() {
	e.限定高与标志 = 0
	e.访问 = 0
	e.basemid = 0
	e.base高 = 0
	e.base低 = 0
	e.限定低 = 0

}

type Gdtdescriptor struct {
	Gdt大小		uint16
	Gdtaddress低	uint16
	Gdtaddress高	uint16
}
type U用户descriptor struct {
	E条目数字		uint32
	Baseaddress	uint32
	L限定		uint32
	F标志		uint8
}

func S集合tlssegment(索引 uint32, descriptor *U用户descriptor, 表格 []Gdt条目_2) bool {
	if 索引 < Tls开始 || 索引 > uint32(len(gdt表格)) {
		return false
	}

	if descriptor.F标志 == Udescrx仅用|Udescsegnot当前电池 {

		表格[索引].C清除()
		return true
	}

	标志 := uint8(Seggran字节)
	if descriptor.F标志&Udesc限定进pages != 0 {
		标志 = Seggran4k页
	}
	访问 := uint8(Priv用户 | Seg正常 | P当前电池)
	if descriptor.F标志&Udescrx仅用 != 0 {
		访问 |= Seg执行
	} else {
		访问 |= Segw
	}
	if 访问&Seg正常 != 0 {
		标志 |= Segbig模式
	}

	表格[索引].Fill(descriptor.Baseaddress, descriptor.L限定, 访问, 标志)
	flushtls表格(表格)

	return true
}

func flushtls表格(表格 []Gdt条目_2) {
	copy(gdt表格[Tls开始:], 表格[Tls开始:])
}
func Flushtls表格(表格 []TSegmentdescriptor) {
	copy(数据_2.segmentdescriptor[Tls开始:], 表格[Tls开始:])
}
