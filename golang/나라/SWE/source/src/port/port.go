package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	läsAntal	uint16
	skrivAntal	uint16
}

func (själv *TPort8bit) Init(portnumber uint16) {
	själv.portnumber = portnumber
	själv.läsAntal = 65
	själv.skrivAntal = 65
}
func (själv *TPort8bit) Skriv(data uint8) {
	PortUtbyte(själv.portnumber, data)
}
func (själv *TPort8bit) Läs() uint8 {
	var rESULTAT = Portibyte(själv.portnumber)
	return rESULTAT
}
func PortSkrivbyte(portnumber uint16, data uint8) {
	PortUtbyte(portnumber, data)
}
func PortLäsbyte(portnumber uint16) uint8 {
	rESULTAT := Portibyte(portnumber)
	return rESULTAT
}

type TPort16bit struct {
	TPort
}

func (själv *TPort16bit) Init(portnumber uint16) {
	själv.TPort.portnumber = portnumber
}
func (själv *TPort16bit) Skriv(data uint16) {
	PortUtord(själv.TPort.portnumber, data)
}
func (själv *TPort16bit) Läs() uint16 {
	var rESULTAT = Portiord(själv.TPort.portnumber)
	return rESULTAT
}
func PortSkrivord(portnumber uint16, data uint16) {
	PortUtord(portnumber, data)
}
func PortLäsord(portnumber uint16) uint16 {
	var rESULTAT uint16 = Portiord(portnumber)
	return rESULTAT
}

type TPort32bit struct {
	TPort
}

func (själv *TPort32bit) Init(portnumber uint16) {
	själv.TPort.portnumber = portnumber
}
func (själv *TPort32bit) Skriv(data uint32) {
	PortUtdword(själv.TPort.portnumber, data)
}
func (själv *TPort32bit) Läs() {
	Portidword(själv.TPort.portnumber)
}
func PortSkrivdword(portnumber uint16, data uint32) {
	PortUtdword(portnumber, data)
}
func PortLäsdword(portnumber uint16) uint32 {
	var rESULTAT uint32 = Portidword(portnumber)
	return rESULTAT
}

var läsAntal uint16 = 65
var skrivAntal uint16 = 66

func PortUtbyte(portnumber uint16, data uint8)
func Portibyte(portnumber uint16) uint8

func PortUtord(portnumber uint16, data uint16)
func Portiord(portnumber uint16) uint16

func PortUtdword(portnumber uint16, data uint32)
func Portidword(portnumber uint16) uint32
