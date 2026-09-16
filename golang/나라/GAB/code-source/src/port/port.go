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
	lireNombre	uint16
	écrireNombre	uint16
}

func (self *TPort8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.lireNombre = 65
	self.écrireNombre = 65
}
func (self *TPort8bit) Écrire(données uint8) {
	PortSortanteoctet(self.portnumber, données)
}
func (self *TPort8bit) Lire() uint8 {
	var rÉSULTAT = PortEntranteoctet(self.portnumber)
	return rÉSULTAT
}
func Portécrireoctet(portnumber uint16, données uint8) {
	PortSortanteoctet(portnumber, données)
}
func Portlireoctet(portnumber uint16) uint8 {
	rÉSULTAT := PortEntranteoctet(portnumber)
	return rÉSULTAT
}

type TPort16bit struct {
	TPort
}

func (self *TPort16bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort16bit) Écrire(données uint16) {
	PortSortantemot(self.TPort.portnumber, données)
}
func (self *TPort16bit) Lire() uint16 {
	var rÉSULTAT = PortEntrantemot(self.TPort.portnumber)
	return rÉSULTAT
}
func Portécriremot(portnumber uint16, données uint16) {
	PortSortantemot(portnumber, données)
}
func Portliremot(portnumber uint16) uint16 {
	var rÉSULTAT uint16 = PortEntrantemot(portnumber)
	return rÉSULTAT
}

type TPort32bit struct {
	TPort
}

func (self *TPort32bit) Init(portnumber uint16) {
	self.TPort.portnumber = portnumber
}
func (self *TPort32bit) Écrire(données uint32) {
	PortSortantedword(self.TPort.portnumber, données)
}
func (self *TPort32bit) Lire() {
	PortEntrantedword(self.TPort.portnumber)
}
func Portécriredword(portnumber uint16, données uint32) {
	PortSortantedword(portnumber, données)
}
func Portliredword(portnumber uint16) uint32 {
	var rÉSULTAT uint32 = PortEntrantedword(portnumber)
	return rÉSULTAT
}

var lireNombre uint16 = 65
var écrireNombre uint16 = 66

func PortSortanteoctet(portnumber uint16, données uint8)
func PortEntranteoctet(portnumber uint16) uint8

func PortSortantemot(portnumber uint16, données uint16)
func PortEntrantemot(portnumber uint16) uint16

func PortSortantedword(portnumber uint16, données uint32)
func PortEntrantedword(portnumber uint16) uint32
