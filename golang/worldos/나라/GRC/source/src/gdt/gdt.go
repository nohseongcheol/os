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

	SegΧρήστηςcode		uint32	= 0x23
	SegΧρήστηςdata		uint32	= 0x2B
	SegΧρήστηςgs		uint32	= 0x33
	SegΔιεργασίαΚατάσταση	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	όριοΧαμηλή_2		uint16
	baseΧαμηλή_2		uint16
	baseΥψηλή_2		uint8
	τύπος			uint8
	διακόπτεςΌριοΥψηλή	uint8
	baseveryΥψηλή		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, όριο_2 uint32, τύπος uint8, διακόπτες_2 uint8) {

	self_2.baseΧαμηλή_2 = uint16(base_2 & 0xFFFF)
	self_2.baseΥψηλή_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryΥψηλή = uint8((base_2 >> 24) & 0xFF)

	self_2.όριοΧαμηλή_2 = uint16(όριο_2 & 0xFFFF)
	self_2.διακόπτεςΌριοΥψηλή = uint8((όριο_2 >> 24) & 0x0F)
	self_2.διακόπτεςΌριοΥψηλή |= (διακόπτες_2 & 0xF0)

	self_2.τύπος = τύπος

}

type TShareddescriptorΠίνακαςdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorΠίνακαςdata

type TShareddescriptorΠίνακας struct {
}

func (self_2 *TShareddescriptorΠίνακας) Init() {

	var gdtκαταχώρηση TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressΧαμηλή) |
		uint32(gdtdescriptor.GdtaddressΥψηλή)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtΜέγεθος+1) / Sizeof(gdtκαταχώρηση))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	προορισμός_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&προορισμός_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	μέγεθος_2 := (*uint16)(Pointer(&προορισμός_3[0]))
	(*μέγεθος_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&προορισμός_3)))

	terminal := new(TConsole)
	terminal.MΕκτύπωσηxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Εκτύπωση(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorΠίνακας) Σύνολοdescriptor(idx int, base_2 uint32, όριο_2 uint32, τύπος uint8, διακόπτες_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, όριο_2, τύπος, διακόπτες_2)
}

const (
	KcsΚατάλογος	= 1
	KdsΚατάλογος	= 2
	KgsΚατάλογος	= 3

	Kcsselector	= KcsΚατάλογος * 8
	Kdsselector	= KdsΚατάλογος * 8
	Kgsselector	= KgsΚατάλογος * 8

	Seggranbyte	= 0 << 7
	Seggran4kΣελίδα	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegΣύστημα	= 0 << 4
	SegΚανονικό	= 1 << 4

	Segnoexec	= 0 << 3
	SegΕκτέλεση	= 1 << 3

	Privkernel	= 0 << 5
	PrivΧρήστης	= 3 << 5

	SegbigΚΑΤΑΣΤΑΣΗ	= 1 << 6

	Παρούσα	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescΠεριεχόμενα	= 3 << 1
	Udescrxonly		= 1 << 3
	UdescΌριοσεpages	= 1 << 4
	UdescsegnotΠαρούσα	= 1 << 5
	Udescusable		= 1 << 6

	Gdtκαταχώρηση	= 256
	TlsΈναρξη	= 16
)

var (
	gdtΠίνακας	= [Gdtκαταχώρηση]Gdtκαταχώρηση_2{}
	gdtdescriptor	Gdtdescriptor
	gdtΠίνακαςlen	= 0
)

type Gdtκαταχώρηση_2 struct {
	όριοΧαμηλή		uint16
	baseΧαμηλή		uint16
	basemid			uint8
	προσπέλαση		uint8
	όριοΥψηλήΚΑΙΔιακόπτες	uint8
	baseΥψηλή		uint8
}

func (e *Gdtκαταχώρηση_2) IsΠαρούσα() bool {
	return e.προσπέλαση&Παρούσα != 0
}

func (e *Gdtκαταχώρηση_2) Fill(base uint32, όριο uint32, προσπέλαση uint8, διακόπτες uint8) {
	e.όριοΥψηλήΚΑΙΔιακόπτες = uint8((όριο >> 16) & 0x000F)
	e.όριοΥψηλήΚΑΙΔιακόπτες |= διακόπτες
	e.προσπέλαση = προσπέλαση
	e.basemid = uint8(base >> 16)
	e.baseΥψηλή = uint8(base >> 24)
	e.baseΧαμηλή = uint16(base & 0xFFFF)
	e.όριοΧαμηλή = uint16(όριο & 0x0000FFFF)
}

func (e *Gdtκαταχώρηση_2) Καθαρισμός() {
	e.όριοΥψηλήΚΑΙΔιακόπτες = 0
	e.προσπέλαση = 0
	e.basemid = 0
	e.baseΥψηλή = 0
	e.baseΧαμηλή = 0
	e.όριοΧαμηλή = 0

}

type Gdtdescriptor struct {
	GdtΜέγεθος		uint16
	GdtaddressΧαμηλή	uint16
	GdtaddressΥψηλή		uint16
}
type Χρήστηςdescriptor struct {
	ΚαταχώρησηΑριθμός	uint32
	Baseaddress		uint32
	Όριο			uint32
	Διακόπτες		uint8
}

func Σύνολοtlssegment(κατάλογος uint32, descriptor *Χρήστηςdescriptor, πίνακας []Gdtκαταχώρηση_2) bool {
	if κατάλογος < TlsΈναρξη || κατάλογος > uint32(len(gdtΠίνακας)) {
		return false
	}

	if descriptor.Διακόπτες == Udescrxonly|UdescsegnotΠαρούσα {

		πίνακας[κατάλογος].Καθαρισμός()
		return true
	}

	διακόπτες := uint8(Seggranbyte)
	if descriptor.Διακόπτες&UdescΌριοσεpages != 0 {
		διακόπτες = Seggran4kΣελίδα
	}
	προσπέλαση := uint8(PrivΧρήστης | SegΚανονικό | Παρούσα)
	if descriptor.Διακόπτες&Udescrxonly != 0 {
		προσπέλαση |= SegΕκτέλεση
	} else {
		προσπέλαση |= Segw
	}
	if προσπέλαση&SegΚανονικό != 0 {
		διακόπτες |= SegbigΚΑΤΑΣΤΑΣΗ
	}

	πίνακας[κατάλογος].Fill(descriptor.Baseaddress, descriptor.Όριο, προσπέλαση, διακόπτες)
	flushtlsΠίνακας(πίνακας)

	return true
}

func flushtlsΠίνακας(πίνακας []Gdtκαταχώρηση_2) {
	copy(gdtΠίνακας[TlsΈναρξη:], πίνακας[TlsΈναρξη:])
}
func FlushtlsΠίνακας(πίνακας []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsΈναρξη:], πίνακας[TlsΈναρξη:])
}
