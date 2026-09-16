/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var pozicija uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	čitajcount	uint16
	zapišicount	uint16
}

func (sam *TPort8bit) Init(portnumber uint16) {
	sam.portnumber = portnumber
	sam.čitajcount = 65
	sam.zapišicount = 65
}
func (sam *TPort8bit) Zapiši(data uint8) {
	PortSmanjibyte(sam.portnumber, data)
}
func (sam *TPort8bit) Čitaj() uint8 {
	var rEZULTAT = PortPovećajbyte(sam.portnumber)
	return rEZULTAT
}
func PortZapišibyte(portnumber uint16, data uint8) {
	PortSmanjibyte(portnumber, data)
}
func PortČitajbyte(portnumber uint16) uint8 {
	rEZULTAT := PortPovećajbyte(portnumber)
	return rEZULTAT
}

type TPort16bit struct {
	TPort
}

func (sam *TPort16bit) Init(portnumber uint16) {
	sam.TPort.portnumber = portnumber
}
func (sam *TPort16bit) Zapiši(data uint16) {
	PortSmanjiriječ(sam.TPort.portnumber, data)
}
func (sam *TPort16bit) Čitaj() uint16 {
	var rEZULTAT = PortPovećajriječ(sam.TPort.portnumber)
	return rEZULTAT
}
func PortZapiširiječ(portnumber uint16, data uint16) {
	PortSmanjiriječ(portnumber, data)
}
func PortČitajriječ(portnumber uint16) uint16 {
	var rEZULTAT uint16 = PortPovećajriječ(portnumber)
	return rEZULTAT
}

type TPort32bit struct {
	TPort
}

func (sam *TPort32bit) Init(portnumber uint16) {
	sam.TPort.portnumber = portnumber
}
func (sam *TPort32bit) Zapiši(data uint32) {
	PortSmanjidword(sam.TPort.portnumber, data)
}
func (sam *TPort32bit) Čitaj() {
	PortPovećajdword(sam.TPort.portnumber)
}
func PortZapišidword(portnumber uint16, data uint32) {
	PortSmanjidword(portnumber, data)
}
func PortČitajdword(portnumber uint16) uint32 {
	var rEZULTAT uint32 = PortPovećajdword(portnumber)
	return rEZULTAT
}

var čitajcount uint16 = 65
var zapišicount uint16 = 66

func PortSmanjibyte(portnumber uint16, data uint8)
func PortPovećajbyte(portnumber uint16) uint8

func PortSmanjiriječ(portnumber uint16, data uint16)
func PortPovećajriječ(portnumber uint16) uint16

func PortSmanjidword(portnumber uint16, data uint32)
func PortPovećajdword(portnumber uint16) uint32
