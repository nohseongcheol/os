package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegUtentecode		uint32	= 0x23
	SegUtentedata		uint32	= 0x2B
	SegUtentegs		uint32	= 0x33
	SegProcessoStato	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limiteBasso_2	uint16
	baseBasso_2	uint16
	baseAlto_2	uint8
	tipo_2		uint8
	flagLimiteAlto	uint8
	baseveryAlto	uint8
}

func (séstesso_2 *TSegmentdescriptor) Init(base_2 uint32, limite_2 uint32, tipo_2 uint8, flag_2 uint8) {

	séstesso_2.baseBasso_2 = uint16(base_2 & 0xFFFF)
	séstesso_2.baseAlto_2 = uint8((base_2 >> 16) & 0xFF)
	séstesso_2.baseveryAlto = uint8((base_2 >> 24) & 0xFF)

	séstesso_2.limiteBasso_2 = uint16(limite_2 & 0xFFFF)
	séstesso_2.flagLimiteAlto = uint8((limite_2 >> 24) & 0x0F)
	séstesso_2.flagLimiteAlto |= (flag_2 & 0xF0)

	séstesso_2.tipo_2 = tipo_2

}

type TShareddescriptorTabelladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabelladata

type TShareddescriptorTabella struct {
}

func (séstesso_2 *TShareddescriptorTabella) Init() {

	var gdtvoce TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressBasso) |
		uint32(gdtdescriptor.GdtaddressAlto)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtDimensione+1) / Sizeof(gdtvoce))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destinazione_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destinazione_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	dimensione_2 := (*uint16)(Pointer(&destinazione_3[0]))
	(*dimensione_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destinazione_3)))

	terminal := new(TConsole)
	terminal.MStampaxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Stampa(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (séstesso_2 *TShareddescriptorTabella) Impostadescriptor(idx int, base_2 uint32, limite_2 uint32, tipo_2 uint8, flag_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limite_2, tipo_2, flag_2)
}

const (
	KcsIndice	= 1
	KdsIndice	= 2
	KgsIndice	= 3

	Kcsselector	= KcsIndice * 8
	Kdsselector	= KdsIndice * 8
	Kgsselector	= KgsIndice * 8

	Seggranbyte	= 0 << 7
	Seggran4kPAGINA	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistema	= 0 << 4
	SegNormale	= 1 << 4

	Segnoexec	= 0 << 3
	SegEsecuzione	= 1 << 3

	Privkernel	= 0 << 5
	PrivUtente	= 3 << 5

	SegbigMODO	= 1 << 6

	Presente	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSommario			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescLimiteIngressoPagine	= 1 << 4
	UdescsegnotPresente		= 1 << 5
	Udescusable			= 1 << 6

	Gdtvoce		= 256
	TlsAvvia	= 16
)

var (
	gdtTabella	= [Gdtvoce]Gdtvoce_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellalen	= 0
)

type Gdtvoce_2 struct {
	limiteBasso	uint16
	baseBasso	uint16
	basemid		uint8
	accesso		uint8
	limiteAltoeFlag	uint8
	baseAlto	uint8
}

func (e *Gdtvoce_2) IsPresente() bool {
	return e.accesso&Presente != 0
}

func (e *Gdtvoce_2) Fill(base uint32, limite uint32, accesso uint8, flag uint8) {
	e.limiteAltoeFlag = uint8((limite >> 16) & 0x000F)
	e.limiteAltoeFlag |= flag
	e.accesso = accesso
	e.basemid = uint8(base >> 16)
	e.baseAlto = uint8(base >> 24)
	e.baseBasso = uint16(base & 0xFFFF)
	e.limiteBasso = uint16(limite & 0x0000FFFF)
}

func (e *Gdtvoce_2) Pulisci() {
	e.limiteAltoeFlag = 0
	e.accesso = 0
	e.basemid = 0
	e.baseAlto = 0
	e.baseBasso = 0
	e.limiteBasso = 0

}

type Gdtdescriptor struct {
	GdtDimensione	uint16
	GdtaddressBasso	uint16
	GdtaddressAlto	uint16
}
type Utentedescriptor struct {
	VoceNumero	uint32
	Baseaddress	uint32
	Limite		uint32
	Flag		uint8
}

func Impostatlssegment(indice uint32, descriptor *Utentedescriptor, tabella []Gdtvoce_2) bool {
	if indice < TlsAvvia || indice > uint32(len(gdtTabella)) {
		return false
	}

	if descriptor.Flag == Udescrxonly|UdescsegnotPresente {

		tabella[indice].Pulisci()
		return true
	}

	flag := uint8(Seggranbyte)
	if descriptor.Flag&UdescLimiteIngressoPagine != 0 {
		flag = Seggran4kPAGINA
	}
	accesso := uint8(PrivUtente | SegNormale | Presente)
	if descriptor.Flag&Udescrxonly != 0 {
		accesso |= SegEsecuzione
	} else {
		accesso |= Segw
	}
	if accesso&SegNormale != 0 {
		flag |= SegbigMODO
	}

	tabella[indice].Fill(descriptor.Baseaddress, descriptor.Limite, accesso, flag)
	flushtlsTabella(tabella)

	return true
}

func flushtlsTabella(tabella []Gdtvoce_2) {
	copy(gdtTabella[TlsAvvia:], tabella[TlsAvvia:])
}
func FlushtlsTabella(tabella []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsAvvia:], tabella[TlsAvvia:])
}
