package port

var placering uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	læseAntal	uint16
	skriveAntal	uint16
}

func (selv *TPort8bit) Init(portnumber uint16) {
	selv.portnumber = portnumber
	selv.læseAntal = 65
	selv.skriveAntal = 65
}
func (selv *TPort8bit) Skrive(data uint8) {
	PortUdbyte(selv.portnumber, data)
}
func (selv *TPort8bit) Læse() uint8 {
	var result = PortIndbyte(selv.portnumber)
	return result
}
func PortSkrivebyte(portnumber uint16, data uint8) {
	PortUdbyte(portnumber, data)
}
func PortLæsebyte(portnumber uint16) uint8 {
	result := PortIndbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (selv *TPort16bit) Init(portnumber uint16) {
	selv.TPort.portnumber = portnumber
}
func (selv *TPort16bit) Skrive(data uint16) {
	PortUdord(selv.TPort.portnumber, data)
}
func (selv *TPort16bit) Læse() uint16 {
	var result = PortIndord(selv.TPort.portnumber)
	return result
}
func PortSkriveord(portnumber uint16, data uint16) {
	PortUdord(portnumber, data)
}
func PortLæseord(portnumber uint16) uint16 {
	var result uint16 = PortIndord(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (selv *TPort32bit) Init(portnumber uint16) {
	selv.TPort.portnumber = portnumber
}
func (selv *TPort32bit) Skrive(data uint32) {
	PortUddword(selv.TPort.portnumber, data)
}
func (selv *TPort32bit) Læse() {
	PortInddword(selv.TPort.portnumber)
}
func PortSkrivedword(portnumber uint16, data uint32) {
	PortUddword(portnumber, data)
}
func PortLæsedword(portnumber uint16) uint32 {
	var result uint32 = PortInddword(portnumber)
	return result
}

var læseAntal uint16 = 65
var skriveAntal uint16 = 66

func PortUdbyte(portnumber uint16, data uint8)
func PortIndbyte(portnumber uint16) uint8

func PortUdord(portnumber uint16, data uint16)
func PortIndord(portnumber uint16) uint16

func PortUddword(portnumber uint16, data uint32)
func PortInddword(portnumber uint16) uint32
