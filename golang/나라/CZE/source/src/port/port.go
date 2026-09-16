/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var umístění uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	čteníPočet	uint16
	zápisPočet	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.čteníPočet = 65
	self.zápisPočet = 65
}
func (self *TPort8bit) Zápis(data uint8) {
	PortVýstupbyte(self.portnumber, data)
}
func (self *TPort8bit) Čtení() uint8 {
	var vÝSLEDEK = PortVstupbyte(self.portnumber)
	return vÝSLEDEK
}
func PortZápisbyte(portnumber uint16, data uint8) {
	PortVýstupbyte(portnumber, data)
}
func PortČteníbyte(portnumber uint16) uint8 {
	vÝSLEDEK := PortVstupbyte(portnumber)
	return vÝSLEDEK
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Zápis(data uint16) {
	PortVýstupslovo(self.TPort.portnumber, data)
}
func (self *TPort16bit) Čtení() uint16 {
	var vÝSLEDEK = PortVstupslovo(self.TPort.portnumber)
	return vÝSLEDEK
}
func PortZápisslovo(portnumber uint16, data uint16) {
	PortVýstupslovo(portnumber, data)
}
func PortČteníslovo(portnumber uint16) uint16 {
	var vÝSLEDEK uint16 = PortVstupslovo(portnumber)
	return vÝSLEDEK
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Zápis(data uint32) {
	PortVýstupdword(self.TPort.portnumber, data)
}
func (self *TPort32bit) Čtení() {
	PortVstupdword(self.TPort.portnumber)
}
func PortZápisdword(portnumber uint16, data uint32) {
	PortVýstupdword(portnumber, data)
}
func PortČtenídword(portnumber uint16) uint32 {
	var vÝSLEDEK uint32 = PortVstupdword(portnumber)
	return vÝSLEDEK
}

var čteníPočet uint16 = 65
var zápisPočet uint16 = 66

func PortVýstupbyte(portnumber uint16, data uint8)
func PortVstupbyte(portnumber uint16) uint8

func PortVýstupslovo(portnumber uint16, data uint16)
func PortVstupslovo(portnumber uint16) uint16

func PortVýstupdword(portnumber uint16, data uint32)
func PortVstupdword(portnumber uint16) uint32
