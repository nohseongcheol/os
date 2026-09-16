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
	balacount	uint16
	ngolacount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.balacount = 65
	self.ngolacount = 65
}
func (self *TPort8bit) Ngola(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Bala() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portngolabyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portbalabyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Ngola(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Bala() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portngolaword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portbalaword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Ngola(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Bala() {
	Portindword(self.TPort.portnumber)
}
func Portngoladword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portbaladword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var balacount uint16 = 65
var ngolacount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
