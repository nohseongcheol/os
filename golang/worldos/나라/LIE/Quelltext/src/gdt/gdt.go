/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "konsole"

const (
	SegKerncode	uint32	= 0x08
	SegKernDaten	uint32	= 0x10
	SegKerngs	uint32	= 0x18

	SegBenutzercode		uint32	= 0x23
	SegBenutzerDaten	uint32	= 0x2B
	SegBenutzergs		uint32	= 0x33
	SegAufgabeStatus	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	beschränkungNiedrig_2		uint16
	baseNiedrig_2			uint16
	baseHoch_2			uint8
	typ				uint8
	optionenBeschränkungHoch	uint8
	baseveryHoch			uint8
}

func (selbst_2 *TSegmentdescriptor) Init(base_2 uint32, beschränkung_2 uint32, typ uint8, optionen_3 uint8) {

	selbst_2.baseNiedrig_2 = uint16(base_2 & 0xFFFF)
	selbst_2.baseHoch_2 = uint8((base_2 >> 16) & 0xFF)
	selbst_2.baseveryHoch = uint8((base_2 >> 24) & 0xFF)

	selbst_2.beschränkungNiedrig_2 = uint16(beschränkung_2 & 0xFFFF)
	selbst_2.optionenBeschränkungHoch = uint8((beschränkung_2 >> 24) & 0x0F)
	selbst_2.optionenBeschränkungHoch |= (optionen_3 & 0xF0)

	selbst_2.typ = typ

}

type TShareddescriptorTabelleDaten struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var daten_2 TShareddescriptorTabelleDaten

type TShareddescriptorTabelle struct {
}

func (selbst_2 *TShareddescriptorTabelle) Init() {

	var gdtEintrag TSegmentdescriptor

	gdtdescriptor = *getgdt()
	altgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressNiedrig) |
		uint32(gdtdescriptor.GdtaddressHoch)<<16)
	altgdtlen := int(uintptr(gdtdescriptor.GdtGröße+1) / Sizeof(gdtEintrag))
	altgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	altgdtlen,
		Cap:	altgdtlen,
		Data:	altgdtaddress,
	}))
	copy(daten_2.segmentdescriptor[:], altgdt)

	daten_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	daten_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	daten_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	ziel_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&ziel_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&daten_2)))

	größe_2 := (*uint16)(Pointer(&ziel_3[0]))
	(*größe_2) = (uint16)((Sizeof(daten_2)))

	gdtfunc(uintptr(Pointer(&ziel_3)))

	terminal := new(TKonsole)
	terminal.MDruckenxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Drucken(uint32(uintptr(Pointer(&daten_2.segmentdescriptor[3]))))

}
func (selbst_2 *TShareddescriptorTabelle) Setzendescriptor(idx int, base_2 uint32, beschränkung_2 uint32, typ uint8, optionen_3 uint8) {
	daten_2.segmentdescriptor[idx].Init(base_2, beschränkung_2, typ, optionen_3)
}

const (
	KcsInhalt	= 1
	KdsInhalt	= 2
	KgsInhalt	= 3

	Kcsselector	= KcsInhalt * 8
	Kdsselector	= KdsInhalt * 8
	Kgsselector	= KgsInhalt * 8

	SeggranByte	= 0 << 7
	Seggran4kSeite	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSystem	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	SegAusführen	= 1 << 3

	PrivKern	= 0 << 5
	PrivBenutzer	= 3 << 5

	SegGroßModus	= 1 << 6

	Vorhanden	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescInhalt			= 3 << 1
	Udescrxnur			= 1 << 3
	UdescBeschränkungEinpages	= 1 << 4
	UdescsegNichtVorhanden		= 1 << 5
	Udescusable			= 1 << 6

	GdtEintrag	= 256
	TlsStarten	= 16
)

var (
	gdtTabelle	= [GdtEintrag]GdtEintrag_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellelen	= 0
)

type GdtEintrag_2 struct {
	beschränkungNiedrig		uint16
	baseNiedrig			uint16
	basemid				uint8
	zugreifen			uint8
	beschränkungHochundOptionen	uint8
	baseHoch			uint8
}

func (e *GdtEintrag_2) IsVorhanden() bool {
	return e.zugreifen&Vorhanden != 0
}

func (e *GdtEintrag_2) Fill(base uint32, beschränkung uint32, zugreifen uint8, optionen uint8) {
	e.beschränkungHochundOptionen = uint8((beschränkung >> 16) & 0x000F)
	e.beschränkungHochundOptionen |= optionen
	e.zugreifen = zugreifen
	e.basemid = uint8(base >> 16)
	e.baseHoch = uint8(base >> 24)
	e.baseNiedrig = uint16(base & 0xFFFF)
	e.beschränkungNiedrig = uint16(beschränkung & 0x0000FFFF)
}

func (e *GdtEintrag_2) Leeren() {
	e.beschränkungHochundOptionen = 0
	e.zugreifen = 0
	e.basemid = 0
	e.baseHoch = 0
	e.baseNiedrig = 0
	e.beschränkungNiedrig = 0

}

type Gdtdescriptor struct {
	GdtGröße		uint16
	GdtaddressNiedrig	uint16
	GdtaddressHoch		uint16
}
type Benutzerdescriptor struct {
	EintragNummer	uint32
	Baseaddress	uint32
	Beschränkung	uint32
	Optionen	uint8
}

func Setzentlssegment(inhalt uint32, descriptor *Benutzerdescriptor, tabelle []GdtEintrag_2) bool {
	if inhalt < TlsStarten || inhalt > uint32(len(gdtTabelle)) {
		return false
	}

	if descriptor.Optionen == Udescrxnur|UdescsegNichtVorhanden {

		tabelle[inhalt].Leeren()
		return true
	}

	optionen := uint8(SeggranByte)
	if descriptor.Optionen&UdescBeschränkungEinpages != 0 {
		optionen = Seggran4kSeite
	}
	zugreifen := uint8(PrivBenutzer | Segnormal | Vorhanden)
	if descriptor.Optionen&Udescrxnur != 0 {
		zugreifen |= SegAusführen
	} else {
		zugreifen |= Segw
	}
	if zugreifen&Segnormal != 0 {
		optionen |= SegGroßModus
	}

	tabelle[inhalt].Fill(descriptor.Baseaddress, descriptor.Beschränkung, zugreifen, optionen)
	flushtlsTabelle(tabelle)

	return true
}

func flushtlsTabelle(tabelle []GdtEintrag_2) {
	copy(gdtTabelle[TlsStarten:], tabelle[TlsStarten:])
}
func FlushtlsTabelle(tabelle []TSegmentdescriptor) {
	copy(daten_2.segmentdescriptor[TlsStarten:], tabelle[TlsStarten:])
}
