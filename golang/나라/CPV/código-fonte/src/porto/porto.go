package porto

var posição uint16 = 1

type TPorto struct {
	portnumber uint16
}

type TPorto8bit struct {
	TPorto
	lerContar	uint16
	escreverContar	uint16
}

func (próprio *TPorto8bit) Init(portnumber uint16) {
	próprio.portnumber = portnumber
	próprio.lerContar = 65
	próprio.escreverContar = 65
}
func (próprio *TPorto8bit) Escrever(dados uint8) {
	PortoSaídaocteto(próprio.portnumber, dados)
}
func (próprio *TPorto8bit) Ler() uint8 {
	var destino_3 = PortoEntradaocteto(próprio.portnumber)
	return destino_3
}
func Portoescreverocteto(portnumber uint16, dados uint8) {
	PortoSaídaocteto(portnumber, dados)
}
func Portolerocteto(portnumber uint16) uint8 {
	destino_3 := PortoEntradaocteto(portnumber)
	return destino_3
}

type TPorto16bit struct {
	TPorto
}

func (próprio *TPorto16bit) Init(portnumber uint16) {
	próprio.TPorto.portnumber = portnumber
}
func (próprio *TPorto16bit) Escrever(dados uint16) {
	PortoSaídapalavra(próprio.TPorto.portnumber, dados)
}
func (próprio *TPorto16bit) Ler() uint16 {
	var destino_3 = PortoEntradapalavra(próprio.TPorto.portnumber)
	return destino_3
}
func Portoescreverpalavra(portnumber uint16, dados uint16) {
	PortoSaídapalavra(portnumber, dados)
}
func Portolerpalavra(portnumber uint16) uint16 {
	var destino_3 uint16 = PortoEntradapalavra(portnumber)
	return destino_3
}

type TPorto32bit struct {
	TPorto
}

func (próprio *TPorto32bit) Init(portnumber uint16) {
	próprio.TPorto.portnumber = portnumber
}
func (próprio *TPorto32bit) Escrever(dados uint32) {
	PortoSaídadword(próprio.TPorto.portnumber, dados)
}
func (próprio *TPorto32bit) Ler() {
	PortoEntradadword(próprio.TPorto.portnumber)
}
func Portoescreverdword(portnumber uint16, dados uint32) {
	PortoSaídadword(portnumber, dados)
}
func Portolerdword(portnumber uint16) uint32 {
	var destino_3 uint32 = PortoEntradadword(portnumber)
	return destino_3
}

var lerContar uint16 = 65
var escreverContar uint16 = 66

func PortoSaídaocteto(portnumber uint16, dados uint8)
func PortoEntradaocteto(portnumber uint16) uint8

func PortoSaídapalavra(portnumber uint16, dados uint16)
func PortoEntradapalavra(portnumber uint16) uint16

func PortoSaídadword(portnumber uint16, dados uint32)
func PortoEntradadword(portnumber uint16) uint32
