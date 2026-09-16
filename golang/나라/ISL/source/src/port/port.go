/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var staða uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	lesturcount	uint16
	skriftcount	uint16
}

func (sjálft *TPort8bit) Init(portnumber uint16) {
	sjálft.portnumber = portnumber
	sjálft.lesturcount = 65
	sjálft.skriftcount = 65
}
func (sjálft *TPort8bit) Skrift(data uint8) {
	PortÚtbyte(sjálft.portnumber, data)
}
func (sjálft *TPort8bit) Lestur() uint8 {
	var nIÐURSTAÐA = PortInnbyte(sjálft.portnumber)
	return nIÐURSTAÐA
}
func PortSkriftbyte(portnumber uint16, data uint8) {
	PortÚtbyte(portnumber, data)
}
func PortLesturbyte(portnumber uint16) uint8 {
	nIÐURSTAÐA := PortInnbyte(portnumber)
	return nIÐURSTAÐA
}

type TPort16bit struct {
	TPort
}

func (sjálft *TPort16bit) Init(portnumber uint16) {
	sjálft.TPort.portnumber = portnumber
}
func (sjálft *TPort16bit) Skrift(data uint16) {
	PortÚtorð(sjálft.TPort.portnumber, data)
}
func (sjálft *TPort16bit) Lestur() uint16 {
	var nIÐURSTAÐA = PortInnorð(sjálft.TPort.portnumber)
	return nIÐURSTAÐA
}
func PortSkriftorð(portnumber uint16, data uint16) {
	PortÚtorð(portnumber, data)
}
func PortLesturorð(portnumber uint16) uint16 {
	var nIÐURSTAÐA uint16 = PortInnorð(portnumber)
	return nIÐURSTAÐA
}

type TPort32bit struct {
	TPort
}

func (sjálft *TPort32bit) Init(portnumber uint16) {
	sjálft.TPort.portnumber = portnumber
}
func (sjálft *TPort32bit) Skrift(data uint32) {
	PortÚtdword(sjálft.TPort.portnumber, data)
}
func (sjálft *TPort32bit) Lestur() {
	PortInndword(sjálft.TPort.portnumber)
}
func PortSkriftdword(portnumber uint16, data uint32) {
	PortÚtdword(portnumber, data)
}
func PortLesturdword(portnumber uint16) uint32 {
	var nIÐURSTAÐA uint32 = PortInndword(portnumber)
	return nIÐURSTAÐA
}

var lesturcount uint16 = 65
var skriftcount uint16 = 66

func PortÚtbyte(portnumber uint16, data uint8)
func PortInnbyte(portnumber uint16) uint8

func PortÚtorð(portnumber uint16, data uint16)
func PortInnorð(portnumber uint16) uint16

func PortÚtdword(portnumber uint16, data uint32)
func PortInndword(portnumber uint16) uint32
