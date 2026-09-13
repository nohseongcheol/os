package порт

var положај uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	читањеcount	uint16
	upiscount	uint16
}

func (isti *TПорт8bit) Init(portnumber uint16) {
	isti.portnumber = portnumber
	isti.читањеcount = 65
	isti.upiscount = 65
}
func (isti *TПорт8bit) Upis(data uint8) {
	ПортPoslatobyte(isti.portnumber, data)
}
func (isti *TПорт8bit) Читање() uint8 {
	var иСХОД = ПортПримљеноbyte(isti.portnumber)
	return иСХОД
}
func Портupisbyte(portnumber uint16, data uint8) {
	ПортPoslatobyte(portnumber, data)
}
func Портчитањеbyte(portnumber uint16) uint8 {
	иСХОД := ПортПримљеноbyte(portnumber)
	return иСХОД
}

type TПорт16bit struct {
	TПорт
}

func (isti *TПорт16bit) Init(portnumber uint16) {
	isti.TПорт.portnumber = portnumber
}
func (isti *TПорт16bit) Upis(data uint16) {
	ПортPoslatoreč(isti.TПорт.portnumber, data)
}
func (isti *TПорт16bit) Читање() uint16 {
	var иСХОД = ПортПримљеноreč(isti.TПорт.portnumber)
	return иСХОД
}
func Портupisreč(portnumber uint16, data uint16) {
	ПортPoslatoreč(portnumber, data)
}
func Портчитањеreč(portnumber uint16) uint16 {
	var иСХОД uint16 = ПортПримљеноreč(portnumber)
	return иСХОД
}

type TПорт32bit struct {
	TПорт
}

func (isti *TПорт32bit) Init(portnumber uint16) {
	isti.TПорт.portnumber = portnumber
}
func (isti *TПорт32bit) Upis(data uint32) {
	ПортPoslatodword(isti.TПорт.portnumber, data)
}
func (isti *TПорт32bit) Читање() {
	ПортПримљеноdword(isti.TПорт.portnumber)
}
func Портupisdword(portnumber uint16, data uint32) {
	ПортPoslatodword(portnumber, data)
}
func Портчитањеdword(portnumber uint16) uint32 {
	var иСХОД uint32 = ПортПримљеноdword(portnumber)
	return иСХОД
}

var читањеcount uint16 = 65
var upiscount uint16 = 66

func ПортPoslatobyte(portnumber uint16, data uint8)
func ПортПримљеноbyte(portnumber uint16) uint8

func ПортPoslatoreč(portnumber uint16, data uint16)
func ПортПримљеноreč(portnumber uint16) uint16

func ПортPoslatodword(portnumber uint16, data uint32)
func ПортПримљеноdword(portnumber uint16) uint32
