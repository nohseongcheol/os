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
	logcount	uint16
	bricount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.logcount = 65
	self.bricount = 65
}
func (self *TPort8bit) Bri(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Log() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portbribyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portlogbyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Bri(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Log() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portbriword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portlogword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Bri(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Log() {
	Portindword(self.TPort.portnumber)
}
func Portbridword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portlogdword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var logcount uint16 = 65
var bricount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
