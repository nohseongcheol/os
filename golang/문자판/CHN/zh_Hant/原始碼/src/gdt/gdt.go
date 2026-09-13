package gdt

import . "unsafe"
import "reflect"
import . "控制台"

const (
	Seg核心code	uint32	= 0x08
	Seg核心資料		uint32	= 0x10
	Seg核心gs		uint32	= 0x18

	Seg使用者code	uint32	= 0x23
	Seg使用者資料		uint32	= 0x2B
	Seg使用者gs		uint32	= 0x33
	Seg工作狀態		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	限制低_2		uint16
	base低_2		uint16
	base高_2		uint8
	類型		uint8
	旗標限制高		uint8
	basevery高	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, 限制_2 uint32, 類型 uint8, 旗標_2 uint8) {

	self_2.base低_2 = uint16(base_2 & 0xFFFF)
	self_2.base高_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.basevery高 = uint8((base_2 >> 24) & 0xFF)

	self_2.限制低_2 = uint16(限制_2 & 0xFFFF)
	self_2.旗標限制高 = uint8((限制_2 >> 24) & 0x0F)
	self_2.旗標限制高 |= (旗標_2 & 0xF0)

	self_2.類型 = 類型

}

type TShareddescriptortable資料 struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var 資料_2 TShareddescriptortable資料

type TShareddescriptortable struct {
}

func (self_2 *TShareddescriptortable) Init() {

	var gdt項目 TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddress低) |
		uint32(gdtdescriptor.Gdtaddress高)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdt大小+1) / Sizeof(gdt項目))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(資料_2.segmentdescriptor[:], oldgdt)

	資料_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	資料_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	資料_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	目的地_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&目的地_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&資料_2)))

	大小_2 := (*uint16)(Pointer(&目的地_3[0]))
	(*大小_2) = (uint16)((Sizeof(資料_2)))

	gdtfunc(uintptr(Pointer(&目的地_3)))

	terminal := new(T控制台)
	terminal.M列印xy("gdt:", 1, 4)
	terminal.MUnsignedinteger32列印(uint32(uintptr(Pointer(&資料_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) S設定descriptor(idx int, base_2 uint32, 限制_2 uint32, 類型 uint8, 旗標_2 uint8) {
	資料_2.segmentdescriptor[idx].Init(base_2, 限制_2, 類型, 旗標_2)
}

const (
	Kcs索引	= 1
	Kds索引	= 2
	Kgs索引	= 3

	Kcsselector	= Kcs索引 * 8
	Kdsselector	= Kds索引 * 8
	Kgsselector	= Kgs索引 * 8

	Seggran位元組	= 0 << 7
	Seggran4k頁	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Seg系統	= 0 << 4
	Seg一般	= 1 << 4

	Segnoexec	= 0 << 3
	Seg執行		= 1 << 3

	Priv核心	= 0 << 5
	Priv使用者	= 3 << 5

	Segbig模式	= 1 << 6

	P目前	= 1 << 7

	Udesc32seg	= 1 << 0
	Udesc內容		= 3 << 1
	Udescrx僅用	= 1 << 3
	Udesc限制進頁	= 1 << 4
	Udescsegnot目前	= 1 << 5
	Udescusable	= 1 << 6

	Gdt項目	= 256
	Tls啟動	= 16
)

var (
	gdttable		= [Gdt項目]Gdt項目_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdt項目_2 struct {
	限制低	uint16
	base低	uint16
	basemid	uint8
	存取	uint8
	限制高和旗標	uint8
	base高	uint8
}

func (e *Gdt項目_2) Is目前() bool {
	return e.存取&P目前 != 0
}

func (e *Gdt項目_2) Fill(base uint32, 限制 uint32, 存取 uint8, 旗標 uint8) {
	e.限制高和旗標 = uint8((限制 >> 16) & 0x000F)
	e.限制高和旗標 |= 旗標
	e.存取 = 存取
	e.basemid = uint8(base >> 16)
	e.base高 = uint8(base >> 24)
	e.base低 = uint16(base & 0xFFFF)
	e.限制低 = uint16(限制 & 0x0000FFFF)
}

func (e *Gdt項目_2) C清除() {
	e.限制高和旗標 = 0
	e.存取 = 0
	e.basemid = 0
	e.base高 = 0
	e.base低 = 0
	e.限制低 = 0

}

type Gdtdescriptor struct {
	Gdt大小		uint16
	Gdtaddress低	uint16
	Gdtaddress高	uint16
}
type U使用者descriptor struct {
	E項目數字		uint32
	Baseaddress	uint32
	L限制		uint32
	F旗標		uint8
}

func S設定tlssegment(索引 uint32, descriptor *U使用者descriptor, table []Gdt項目_2) bool {
	if 索引 < Tls啟動 || 索引 > uint32(len(gdttable)) {
		return false
	}

	if descriptor.F旗標 == Udescrx僅用|Udescsegnot目前 {

		table[索引].C清除()
		return true
	}

	旗標 := uint8(Seggran位元組)
	if descriptor.F旗標&Udesc限制進頁 != 0 {
		旗標 = Seggran4k頁
	}
	存取 := uint8(Priv使用者 | Seg一般 | P目前)
	if descriptor.F旗標&Udescrx僅用 != 0 {
		存取 |= Seg執行
	} else {
		存取 |= Segw
	}
	if 存取&Seg一般 != 0 {
		旗標 |= Segbig模式
	}

	table[索引].Fill(descriptor.Baseaddress, descriptor.L限制, 存取, 旗標)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdt項目_2) {
	copy(gdttable[Tls啟動:], table[Tls啟動:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(資料_2.segmentdescriptor[Tls啟動:], table[Tls啟動:])
}
