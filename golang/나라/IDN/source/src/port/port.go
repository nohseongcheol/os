/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var posisi uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	bacacount	uint16
	tuliscount	uint16
}

func (dirisendiri *TPort8bit) Init(portnumber uint16) {
	dirisendiri.portnumber = portnumber
	dirisendiri.bacacount = 65
	dirisendiri.tuliscount = 65
}
func (dirisendiri *TPort8bit) Tulis(data uint8) {
	PortKeluarbyte(dirisendiri.portnumber, data)
}
func (dirisendiri *TPort8bit) Baca() uint8 {
	var hASIL = PortMasukbyte(dirisendiri.portnumber)
	return hASIL
}
func PortTulisbyte(portnumber uint16, data uint8) {
	PortKeluarbyte(portnumber, data)
}
func PortBacabyte(portnumber uint16) uint8 {
	hASIL := PortMasukbyte(portnumber)
	return hASIL
}

type TPort16bit struct {
	TPort
}

func (dirisendiri *TPort16bit) Init(portnumber uint16) {
	dirisendiri.TPort.portnumber = portnumber
}
func (dirisendiri *TPort16bit) Tulis(data uint16) {
	PortKeluarkata(dirisendiri.TPort.portnumber, data)
}
func (dirisendiri *TPort16bit) Baca() uint16 {
	var hASIL = PortMasukkata(dirisendiri.TPort.portnumber)
	return hASIL
}
func PortTuliskata(portnumber uint16, data uint16) {
	PortKeluarkata(portnumber, data)
}
func PortBacakata(portnumber uint16) uint16 {
	var hASIL uint16 = PortMasukkata(portnumber)
	return hASIL
}

type TPort32bit struct {
	TPort
}

func (dirisendiri *TPort32bit) Init(portnumber uint16) {
	dirisendiri.TPort.portnumber = portnumber
}
func (dirisendiri *TPort32bit) Tulis(data uint32) {
	PortKeluardword(dirisendiri.TPort.portnumber, data)
}
func (dirisendiri *TPort32bit) Baca() {
	PortMasukdword(dirisendiri.TPort.portnumber)
}
func PortTulisdword(portnumber uint16, data uint32) {
	PortKeluardword(portnumber, data)
}
func PortBacadword(portnumber uint16) uint32 {
	var hASIL uint32 = PortMasukdword(portnumber)
	return hASIL
}

var bacacount uint16 = 65
var tuliscount uint16 = 66

func PortKeluarbyte(portnumber uint16, data uint8)
func PortMasukbyte(portnumber uint16) uint8

func PortKeluarkata(portnumber uint16, data uint16)
func PortMasukkata(portnumber uint16) uint16

func PortKeluardword(portnumber uint16, data uint32)
func PortMasukdword(portnumber uint16) uint32
