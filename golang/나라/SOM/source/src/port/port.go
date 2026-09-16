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
	akhricount	uint16
	qorcount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.akhricount = 65
	self.qorcount = 65
}
func (self *TPort8bit) Qor(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Akhri() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portqorbyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portakhribyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Qor(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Akhri() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portqorword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portakhriword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Qor(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Akhri() {
	Portindword(self.TPort.portnumber)
}
func Portqordword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portakhridword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var akhricount uint16 = 65
var qorcount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
