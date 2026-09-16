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
	ancount		uint16
	khiancount	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.ancount = 65
	self.khiancount = 65
}
func (self *TPort8bit) Khian(data uint8) {
	Portออกbyte(self.portnumber, data)
}
func (self *TPort8bit) An() uint8 {
	var result = Portขยายbyte(self.portnumber)
	return result
}
func Portkhianbyte(portnumber uint16, data uint8) {
	Portออกbyte(portnumber, data)
}
func Portanbyte(portnumber uint16) uint8 {
	result := Portขยายbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Khian(data uint16) {
	Portออกคำ(self.TPort.portnumber, data)
}
func (self *TPort16bit) An() uint16 {
	var result = Portขยายคำ(self.TPort.portnumber)
	return result
}
func Portkhianคำ(portnumber uint16, data uint16) {
	Portออกคำ(portnumber, data)
}
func Portanคำ(portnumber uint16) uint16 {
	var result uint16 = Portขยายคำ(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Khian(data uint32) {
	Portออกdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) An() {
	Portขยายdword(self.TPort.portnumber)
}
func Portkhiandword(portnumber uint16, data uint32) {
	Portออกdword(portnumber, data)
}
func Portandword(portnumber uint16) uint32 {
	var result uint32 = Portขยายdword(portnumber)
	return result
}

var ancount uint16 = 65
var khiancount uint16 = 66

func Portออกbyte(portnumber uint16, data uint8)
func Portขยายbyte(portnumber uint16) uint8

func Portออกคำ(portnumber uint16, data uint16)
func Portขยายคำ(portnumber uint16) uint16

func Portออกdword(portnumber uint16, data uint32)
func Portขยายdword(portnumber uint16) uint32
