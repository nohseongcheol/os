/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegLietotājscode	uint32	= 0x23
	SegLietotājsdata	uint32	= 0x2B
	SegLietotājsgs		uint32	= 0x33
	SegtaskStāvoklis	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ierobežotKlusi_2	uint16
	baseKlusi_2		uint16
	baseAugsta_2		uint8
	tips			uint8
	karogiIerobežotAugsta	uint8
	baseveryAugsta		uint8
}

func (pats_2 *TSegmentdescriptor) Init(base_2 uint32, ierobežot_2 uint32, tips uint8, karogi_2 uint8) {

	pats_2.baseKlusi_2 = uint16(base_2 & 0xFFFF)
	pats_2.baseAugsta_2 = uint8((base_2 >> 16) & 0xFF)
	pats_2.baseveryAugsta = uint8((base_2 >> 24) & 0xFF)

	pats_2.ierobežotKlusi_2 = uint16(ierobežot_2 & 0xFFFF)
	pats_2.karogiIerobežotAugsta = uint8((ierobežot_2 >> 24) & 0x0F)
	pats_2.karogiIerobežotAugsta |= (karogi_2 & 0xF0)

	pats_2.tips = tips

}

type TShareddescriptorTabuladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabuladata

type TShareddescriptorTabula struct {
}

func (pats_2 *TShareddescriptorTabula) Init() {

	var gdtieraksts TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressKlusi) |
		uint32(gdtdescriptor.GdtaddressAugsta)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtIzmērs+1) / Sizeof(gdtieraksts))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	mērķis_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&mērķis_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	izmērs_2 := (*uint16)(Pointer(&mērķis_3[0]))
	(*izmērs_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&mērķis_3)))

	terminal := new(TConsole)
	terminal.MDrukātxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Drukāt(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (pats_2 *TShareddescriptorTabula) Kopadescriptor(idx int, base_2 uint32, ierobežot_2 uint32, tips uint8, karogi_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ierobežot_2, tips, karogi_2)
}

const (
	KcsSaturs	= 1
	KdsSaturs	= 2
	KgsSaturs	= 3

	Kcsselector	= KcsSaturs * 8
	Kdsselector	= KdsSaturs * 8
	Kgsselector	= KgsSaturs * 8

	Seggranbyte	= 0 << 7
	Seggran4kLapa	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistēma	= 0 << 4
	SegParasts	= 1 << 4

	Segnoexec	= 0 << 3
	SegIzpildīt	= 1 << 3

	Privkernel	= 0 << 5
	PrivLietotājs	= 3 << 5

	SegbigRežīms	= 1 << 6

	Klātesošs	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSaturs			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescIerobežotIenākošāpages	= 1 << 4
	UdescsegnotKlātesošs		= 1 << 5
	Udescusable			= 1 << 6

	Gdtieraksts	= 256
	TlsStartēt	= 16
)

var (
	gdtTabula	= [Gdtieraksts]Gdtieraksts_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabulalen	= 0
)

type Gdtieraksts_2 struct {
	ierobežotKlusi			uint16
	baseKlusi			uint16
	basemid				uint8
	piekļūt				uint8
	ierobežotAugstaandKarogi	uint8
	baseAugsta			uint8
}

func (e *Gdtieraksts_2) IsKlātesošs() bool {
	return e.piekļūt&Klātesošs != 0
}

func (e *Gdtieraksts_2) Fill(base uint32, ierobežot uint32, piekļūt uint8, karogi uint8) {
	e.ierobežotAugstaandKarogi = uint8((ierobežot >> 16) & 0x000F)
	e.ierobežotAugstaandKarogi |= karogi
	e.piekļūt = piekļūt
	e.basemid = uint8(base >> 16)
	e.baseAugsta = uint8(base >> 24)
	e.baseKlusi = uint16(base & 0xFFFF)
	e.ierobežotKlusi = uint16(ierobežot & 0x0000FFFF)
}

func (e *Gdtieraksts_2) Notīrīt() {
	e.ierobežotAugstaandKarogi = 0
	e.piekļūt = 0
	e.basemid = 0
	e.baseAugsta = 0
	e.baseKlusi = 0
	e.ierobežotKlusi = 0

}

type Gdtdescriptor struct {
	GdtIzmērs		uint16
	GdtaddressKlusi		uint16
	GdtaddressAugsta	uint16
}
type Lietotājsdescriptor struct {
	IerakstsSkaitlis	uint32
	Baseaddress		uint32
	Ierobežot		uint32
	Karogi			uint8
}

func Kopatlssegment(saturs uint32, descriptor *Lietotājsdescriptor, tabula []Gdtieraksts_2) bool {
	if saturs < TlsStartēt || saturs > uint32(len(gdtTabula)) {
		return false
	}

	if descriptor.Karogi == Udescrxonly|UdescsegnotKlātesošs {

		tabula[saturs].Notīrīt()
		return true
	}

	karogi := uint8(Seggranbyte)
	if descriptor.Karogi&UdescIerobežotIenākošāpages != 0 {
		karogi = Seggran4kLapa
	}
	piekļūt := uint8(PrivLietotājs | SegParasts | Klātesošs)
	if descriptor.Karogi&Udescrxonly != 0 {
		piekļūt |= SegIzpildīt
	} else {
		piekļūt |= Segw
	}
	if piekļūt&SegParasts != 0 {
		karogi |= SegbigRežīms
	}

	tabula[saturs].Fill(descriptor.Baseaddress, descriptor.Ierobežot, piekļūt, karogi)
	flushtlsTabula(tabula)

	return true
}

func flushtlsTabula(tabula []Gdtieraksts_2) {
	copy(gdtTabula[TlsStartēt:], tabula[TlsStartēt:])
}
func FlushtlsTabula(tabula []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsStartēt:], tabula[TlsStartēt:])
}
