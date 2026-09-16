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
	aqracount	uint16
	iktebcount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.aqracount = 65
	self.iktebcount = 65
}
func (self *TPort8bit) Ikteb(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Aqra() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portiktebbyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portaqrabyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Ikteb(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Aqra() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portiktebword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portaqraword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Ikteb(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Aqra() {
	Portindword(self.TPort.portnumber)
}
func Portiktebdword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portaqradword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var aqracount uint16 = 65
var iktebcount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
