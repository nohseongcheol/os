/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var position uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	atuarneqcount	uint16
	allanneqcount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.atuarneqcount = 65
	self.allanneqcount = 65
}
func (self *TPort8bit) Allanneq(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Atuarneq() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portallanneqbyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portatuarneqbyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Allanneq(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Atuarneq() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portallanneqword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portatuarneqword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Allanneq(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Atuarneq() {
	Portindword(self.TPort.portnumber)
}
func Portallanneqdword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portatuarneqdword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var atuarneqcount uint16 = 65
var allanneqcount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
