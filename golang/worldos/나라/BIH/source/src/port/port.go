/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var položaj uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	čitajcount	uint16
	pišicount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.čitajcount = 65
	self.pišicount = 65
}
func (self *TPort8bit) Piši(data uint8) {
	PortPoslatobyte(self.portnumber, data)
}
func (self *TPort8bit) Čitaj() uint8 {
	var result = PortPrimljenobyte(self.portnumber)
	return result
}
func PortPišibyte(portnumber uint16, data uint8) {
	PortPoslatobyte(portnumber, data)
}
func PortČitajbyte(portnumber uint16) uint8 {
	result := PortPrimljenobyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Piši(data uint16) {
	PortPoslatoword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Čitaj() uint16 {
	var result = PortPrimljenoword(self.TPort.portnumber)
	return result
}
func PortPišiword(portnumber uint16, data uint16) {
	PortPoslatoword(portnumber, data)
}
func PortČitajword(portnumber uint16) uint16 {
	var result uint16 = PortPrimljenoword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Piši(data uint32) {
	PortPoslatodword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Čitaj() {
	PortPrimljenodword(self.TPort.portnumber)
}
func PortPišidword(portnumber uint16, data uint32) {
	PortPoslatodword(portnumber, data)
}
func PortČitajdword(portnumber uint16) uint32 {
	var result uint32 = PortPrimljenodword(portnumber)
	return result
}

var čitajcount uint16 = 65
var pišicount uint16 = 66

func PortPoslatobyte(portnumber uint16, data uint8)
func PortPrimljenobyte(portnumber uint16) uint8

func PortPoslatoword(portnumber uint16, data uint16)
func PortPrimljenoword(portnumber uint16) uint16

func PortPoslatodword(portnumber uint16, data uint32)
func PortPrimljenodword(portnumber uint16) uint32
