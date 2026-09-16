/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package prievadas

var pozicija uint16 = 1

type TPrievadas struct {
	portnumber uint16
}

type TPrievadas8bit struct {
	TPrievadas
	skaitymascount	uint16
	rašymascount	uint16
}

func (self *TPrievadas8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.skaitymascount = 65
	self.rašymascount = 65
}
func (self *TPrievadas8bit) Rašymas(data uint8) {
	PrievadasIšbyte(self.portnumber, data)
}
func (self *TPrievadas8bit) Skaitymas() uint8 {
	var rEZULTATAS = PrievadasĮbyte(self.portnumber)
	return rEZULTATAS
}
func PrievadasRašymasbyte(portnumber uint16, data uint8) {
	PrievadasIšbyte(portnumber, data)
}
func PrievadasSkaitymasbyte(portnumber uint16) uint8 {
	rEZULTATAS := PrievadasĮbyte(portnumber)
	return rEZULTATAS
}

type TPrievadas16bit struct {
	TPrievadas
}

func (self *TPrievadas16bit) Init(portnumber uint16) {
	self.TPrievadas.portnumber = portnumber
}
func (self *TPrievadas16bit) Rašymas(data uint16) {
	PrievadasIšžodis(self.TPrievadas.portnumber, data)
}
func (self *TPrievadas16bit) Skaitymas() uint16 {
	var rEZULTATAS = PrievadasĮžodis(self.TPrievadas.portnumber)
	return rEZULTATAS
}
func PrievadasRašymasžodis(portnumber uint16, data uint16) {
	PrievadasIšžodis(portnumber, data)
}
func PrievadasSkaitymasžodis(portnumber uint16) uint16 {
	var rEZULTATAS uint16 = PrievadasĮžodis(portnumber)
	return rEZULTATAS
}

type TPrievadas32bit struct {
	TPrievadas
}

func (self *TPrievadas32bit) Init(portnumber uint16) {
	self.TPrievadas.portnumber = portnumber
}
func (self *TPrievadas32bit) Rašymas(data uint32) {
	PrievadasIšdword(self.TPrievadas.portnumber, data)
}
func (self *TPrievadas32bit) Skaitymas() {
	PrievadasĮdword(self.TPrievadas.portnumber)
}
func PrievadasRašymasdword(portnumber uint16, data uint32) {
	PrievadasIšdword(portnumber, data)
}
func PrievadasSkaitymasdword(portnumber uint16) uint32 {
	var rEZULTATAS uint32 = PrievadasĮdword(portnumber)
	return rEZULTATAS
}

var skaitymascount uint16 = 65
var rašymascount uint16 = 66

func PrievadasIšbyte(portnumber uint16, data uint8)
func PrievadasĮbyte(portnumber uint16) uint8

func PrievadasIšžodis(portnumber uint16, data uint16)
func PrievadasĮžodis(portnumber uint16) uint16

func PrievadasIšdword(portnumber uint16, data uint32)
func PrievadasĮdword(portnumber uint16) uint32
