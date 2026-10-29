/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var kedudukan uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	bacacount	uint16
	tuliscount	uint16
}

func (diri *TPort8bit) Init(portnumber uint16) {
	diri.portnumber = portnumber
	diri.bacacount = 65
	diri.tuliscount = 65
}
func (diri *TPort8bit) Tulis(data uint8) {
	PortKeluarbyte(diri.portnumber, data)
}
func (diri *TPort8bit) Baca() uint8 {
	var result = PortMasukbyte(diri.portnumber)
	return result
}
func PortTulisbyte(portnumber uint16, data uint8) {
	PortKeluarbyte(portnumber, data)
}
func PortBacabyte(portnumber uint16) uint8 {
	result := PortMasukbyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (diri *TPort16bit) Init(portnumber uint16) {
	diri.TPort.portnumber = portnumber
}
func (diri *TPort16bit) Tulis(data uint16) {
	PortKeluarperkataan(diri.TPort.portnumber, data)
}
func (diri *TPort16bit) Baca() uint16 {
	var result = PortMasukperkataan(diri.TPort.portnumber)
	return result
}
func PortTulisperkataan(portnumber uint16, data uint16) {
	PortKeluarperkataan(portnumber, data)
}
func PortBacaperkataan(portnumber uint16) uint16 {
	var result uint16 = PortMasukperkataan(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (diri *TPort32bit) Init(portnumber uint16) {
	diri.TPort.portnumber = portnumber
}
func (diri *TPort32bit) Tulis(data uint32) {
	PortKeluardword(diri.TPort.portnumber, data)
}
func (diri *TPort32bit) Baca() {
	PortMasukdword(diri.TPort.portnumber)
}
func PortTulisdword(portnumber uint16, data uint32) {
	PortKeluardword(portnumber, data)
}
func PortBacadword(portnumber uint16) uint32 {
	var result uint32 = PortMasukdword(portnumber)
	return result
}

var bacacount uint16 = 65
var tuliscount uint16 = 66

func PortKeluarbyte(portnumber uint16, data uint8)
func PortMasukbyte(portnumber uint16) uint8

func PortKeluarperkataan(portnumber uint16, data uint16)
func PortMasukperkataan(portnumber uint16) uint16

func PortKeluardword(portnumber uint16, data uint32)
func PortMasukdword(portnumber uint16) uint32
