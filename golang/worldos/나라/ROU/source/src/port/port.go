/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var poziție uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	citirecount	uint16
	scrierecount	uint16
}

func (sine *TPort8bit) Init(portnumber uint16) {
	sine.portnumber = portnumber
	sine.citirecount = 65
	sine.scrierecount = 65
}
func (sine *TPort8bit) Scriere(data uint8) {
	PortIeșirebyte(sine.portnumber, data)
}
func (sine *TPort8bit) Citire() uint8 {
	var result = PortIntrarebyte(sine.portnumber)
	return result
}
func PortScrierebyte(portnumber uint16, data uint8) {
	PortIeșirebyte(portnumber, data)
}
func PortCitirebyte(portnumber uint16) uint8 {
	result := PortIntrarebyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (sine *TPort16bit) Init(portnumber uint16) {
	sine.TPort.portnumber = portnumber
}
func (sine *TPort16bit) Scriere(data uint16) {
	PortIeșirecuvânt(sine.TPort.portnumber, data)
}
func (sine *TPort16bit) Citire() uint16 {
	var result = PortIntrarecuvânt(sine.TPort.portnumber)
	return result
}
func PortScrierecuvânt(portnumber uint16, data uint16) {
	PortIeșirecuvânt(portnumber, data)
}
func PortCitirecuvânt(portnumber uint16) uint16 {
	var result uint16 = PortIntrarecuvânt(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (sine *TPort32bit) Init(portnumber uint16) {
	sine.TPort.portnumber = portnumber
}
func (sine *TPort32bit) Scriere(data uint32) {
	PortIeșiredword(sine.TPort.portnumber, data)
}
func (sine *TPort32bit) Citire() {
	PortIntraredword(sine.TPort.portnumber)
}
func PortScrieredword(portnumber uint16, data uint32) {
	PortIeșiredword(portnumber, data)
}
func PortCitiredword(portnumber uint16) uint32 {
	var result uint32 = PortIntraredword(portnumber)
	return result
}

var citirecount uint16 = 65
var scrierecount uint16 = 66

func PortIeșirebyte(portnumber uint16, data uint8)
func PortIntrarebyte(portnumber uint16) uint8

func PortIeșirecuvânt(portnumber uint16, data uint16)
func PortIntrarecuvânt(portnumber uint16) uint16

func PortIeșiredword(portnumber uint16, data uint32)
func PortIntraredword(portnumber uint16) uint32
