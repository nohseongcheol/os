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
	gusomacount	uint16
	kwandikacount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.gusomacount = 65
	self.kwandikacount = 65
}
func (self *TPort8bit) Kwandika(data uint8) {
	Portoutbyte(self.portnumber, data)
}
func (self *TPort8bit) Gusoma() uint8 {
	var result = Portinbyte(self.portnumber)
	return result
}
func Portkwandikabyte(portnumber uint16, data uint8) {
	Portoutbyte(portnumber, data)
}
func Portgusomabyte(portnumber uint16) uint8 {
	result := Portinbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Kwandika(data uint16) {
	Portoutword(self.TPort.portnumber, data)
}
func (self *TPort16bit) Gusoma() uint16 {
	var result = Portinword(self.TPort.portnumber)
	return result
}
func Portkwandikaword(portnumber uint16, data uint16) {
	Portoutword(portnumber, data)
}
func Portgusomaword(portnumber uint16) uint16 {
	var result uint16 = Portinword(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Kwandika(data uint32) {
	Portoutdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Gusoma() {
	Portindword(self.TPort.portnumber)
}
func Portkwandikadword(portnumber uint16, data uint32) {
	Portoutdword(portnumber, data)
}
func Portgusomadword(portnumber uint16) uint32 {
	var result uint32 = Portindword(portnumber)
	return result
}

var gusomacount uint16 = 65
var kwandikacount uint16 = 66

func Portoutbyte(portnumber uint16, data uint8)
func Portinbyte(portnumber uint16) uint8

func Portoutword(portnumber uint16, data uint16)
func Portinword(portnumber uint16) uint16

func Portoutdword(portnumber uint16, data uint32)
func Portindword(portnumber uint16) uint32
