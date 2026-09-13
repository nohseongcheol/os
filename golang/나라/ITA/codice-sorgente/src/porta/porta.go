package porta

var posizione uint16 = 1

type TPorta struct {
	portnumber uint16
}

type TPorta8bit struct {
	TPorta
	letturaConteggio	uint16
	scritturaConteggio	uint16
}

func (séstesso *TPorta8bit) Init(portnumber uint16) {
	séstesso.portnumber = portnumber
	séstesso.letturaConteggio = 65
	séstesso.scritturaConteggio = 65
}
func (séstesso *TPorta8bit) Scrittura(data uint8) {
	PortaUscitabyte(séstesso.portnumber, data)
}
func (séstesso *TPorta8bit) Lettura() uint8 {
	var rISULTATO = PortaIngressobyte(séstesso.portnumber)
	return rISULTATO
}
func PortaScritturabyte(portnumber uint16, data uint8) {
	PortaUscitabyte(portnumber, data)
}
func PortaLetturabyte(portnumber uint16) uint8 {
	rISULTATO := PortaIngressobyte(portnumber)
	return rISULTATO
}

type TPorta16bit struct {
	TPorta
}

func (séstesso *TPorta16bit) Init(portnumber uint16) {
	séstesso.TPorta.portnumber = portnumber
}
func (séstesso *TPorta16bit) Scrittura(data uint16) {
	PortaUscitaparola(séstesso.TPorta.portnumber, data)
}
func (séstesso *TPorta16bit) Lettura() uint16 {
	var rISULTATO = PortaIngressoparola(séstesso.TPorta.portnumber)
	return rISULTATO
}
func PortaScritturaparola(portnumber uint16, data uint16) {
	PortaUscitaparola(portnumber, data)
}
func PortaLetturaparola(portnumber uint16) uint16 {
	var rISULTATO uint16 = PortaIngressoparola(portnumber)
	return rISULTATO
}

type TPorta32bit struct {
	TPorta
}

func (séstesso *TPorta32bit) Init(portnumber uint16) {
	séstesso.TPorta.portnumber = portnumber
}
func (séstesso *TPorta32bit) Scrittura(data uint32) {
	PortaUscitadword(séstesso.TPorta.portnumber, data)
}
func (séstesso *TPorta32bit) Lettura() {
	PortaIngressodword(séstesso.TPorta.portnumber)
}
func PortaScritturadword(portnumber uint16, data uint32) {
	PortaUscitadword(portnumber, data)
}
func PortaLetturadword(portnumber uint16) uint32 {
	var rISULTATO uint32 = PortaIngressodword(portnumber)
	return rISULTATO
}

var letturaConteggio uint16 = 65
var scritturaConteggio uint16 = 66

func PortaUscitabyte(portnumber uint16, data uint8)
func PortaIngressobyte(portnumber uint16) uint8

func PortaUscitaparola(portnumber uint16, data uint16)
func PortaIngressoparola(portnumber uint16) uint16

func PortaUscitadword(portnumber uint16, data uint32)
func PortaIngressodword(portnumber uint16) uint32
