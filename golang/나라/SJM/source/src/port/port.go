package port

var posisjon uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	lesAntall	uint16
	skrivAntall	uint16
}

func (selv *TPort8bit) Init(portnumber uint16) {
	selv.portnumber = portnumber
	selv.lesAntall = 65
	selv.skrivAntall = 65
}
func (selv *TPort8bit) Skriv(data uint8) {
	PortUtbyte(selv.portnumber, data)
}
func (selv *TPort8bit) Les() uint8 {
	var result = PortInnbyte(selv.portnumber)
	return result
}
func PortSkrivbyte(portnumber uint16, data uint8) {
	PortUtbyte(portnumber, data)
}
func PortLesbyte(portnumber uint16) uint8 {
	result := PortInnbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (selv *TPort16bit) Init(portnumber uint16) {
	selv.TPort.portnumber = portnumber
}
func (selv *TPort16bit) Skriv(data uint16) {
	PortUtord(selv.TPort.portnumber, data)
}
func (selv *TPort16bit) Les() uint16 {
	var result = PortInnord(selv.TPort.portnumber)
	return result
}
func PortSkrivord(portnumber uint16, data uint16) {
	PortUtord(portnumber, data)
}
func PortLesord(portnumber uint16) uint16 {
	var result uint16 = PortInnord(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (selv *TPort32bit) Init(portnumber uint16) {
	selv.TPort.portnumber = portnumber
}
func (selv *TPort32bit) Skriv(data uint32) {
	PortUtdword(selv.TPort.portnumber, data)
}
func (selv *TPort32bit) Les() {
	PortInndword(selv.TPort.portnumber)
}
func PortSkrivdword(portnumber uint16, data uint32) {
	PortUtdword(portnumber, data)
}
func PortLesdword(portnumber uint16) uint32 {
	var result uint32 = PortInndword(portnumber)
	return result
}

var lesAntall uint16 = 65
var skrivAntall uint16 = 66

func PortUtbyte(portnumber uint16, data uint8)
func PortInnbyte(portnumber uint16) uint8

func PortUtord(portnumber uint16, data uint16)
func PortInnord(portnumber uint16) uint16

func PortUtdword(portnumber uint16, data uint32)
func PortInndword(portnumber uint16) uint32
