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
	faitaucount	uint16
	tusitusicount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.faitaucount = 65
	self.tusitusicount = 65
}
func (self *TPort8bit) Tusitusi(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Faitau() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Porttusitusibyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portfaitaubyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Tusitusi(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Faitau() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Porttusitusiword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portfaitauword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Tusitusi(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Faitau() {
	Portindword(self.TPort.portnumber)
}
func Porttusitusidword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portfaitaudword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var faitaucount uint16 = 65
var tusitusicount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
