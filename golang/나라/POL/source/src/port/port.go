package port

var pozycja uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	odczytLiczba	uint16
	zapisLiczba	uint16
}

func (bieżący *TPort8bit) Init(portnumber uint16) {
	bieżący.portnumber = portnumber
	bieżący.odczytLiczba = 65
	bieżący.zapisLiczba = 65
}
func (bieżący *TPort8bit) Zapis(data uint8) {
	PortWychodzącybyte(bieżący.portnumber, data)
}
func (bieżący *TPort8bit) Odczyt() uint8 {
	var wYNIK = PortWchodzącybyte(bieżący.portnumber)
	return wYNIK
}
func PortZapisbyte(portnumber uint16, data uint8) {
	PortWychodzącybyte(portnumber, data)
}
func PortOdczytbyte(portnumber uint16) uint8 {
	wYNIK := PortWchodzącybyte(portnumber)
	return wYNIK
}

type TPort16bit struct {
	TPort
}

func (bieżący *TPort16bit) Init(portnumber uint16) {
	bieżący.TPort.portnumber = portnumber
}
func (bieżący *TPort16bit) Zapis(data uint16) {
	PortWychodzącysłowo(bieżący.TPort.portnumber, data)
}
func (bieżący *TPort16bit) Odczyt() uint16 {
	var wYNIK = PortWchodzącysłowo(bieżący.TPort.portnumber)
	return wYNIK
}
func PortZapissłowo(portnumber uint16, data uint16) {
	PortWychodzącysłowo(portnumber, data)
}
func PortOdczytsłowo(portnumber uint16) uint16 {
	var wYNIK uint16 = PortWchodzącysłowo(portnumber)
	return wYNIK
}

type TPort32bit struct {
	TPort
}

func (bieżący *TPort32bit) Init(portnumber uint16) {
	bieżący.TPort.portnumber = portnumber
}
func (bieżący *TPort32bit) Zapis(data uint32) {
	PortWychodzącydword(bieżący.TPort.portnumber, data)
}
func (bieżący *TPort32bit) Odczyt() {
	PortWchodzącydword(bieżący.TPort.portnumber)
}
func PortZapisdword(portnumber uint16, data uint32) {
	PortWychodzącydword(portnumber, data)
}
func PortOdczytdword(portnumber uint16) uint32 {
	var wYNIK uint32 = PortWchodzącydword(portnumber)
	return wYNIK
}

var odczytLiczba uint16 = 65
var zapisLiczba uint16 = 66

func PortWychodzącybyte(portnumber uint16, data uint8)
func PortWchodzącybyte(portnumber uint16) uint8

func PortWychodzącysłowo(portnumber uint16, data uint16)
func PortWchodzącysłowo(portnumber uint16) uint16

func PortWychodzącydword(portnumber uint16, data uint32)
func PortWchodzącydword(portnumber uint16) uint32
