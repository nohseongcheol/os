/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var pozícia uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	čítaniecount	uint16
	zápiscount	uint16
}

func (vlastný *TPort8bit) Init(portnumber uint16) {
	vlastný.portnumber = portnumber
	vlastný.čítaniecount = 65
	vlastný.zápiscount = 65
}
func (vlastný *TPort8bit) Zápis(data uint8) {
	PortVýstupbyte(vlastný.portnumber, data)
}
func (vlastný *TPort8bit) Čítanie() uint8 {
	var result = Portnabyte(vlastný.portnumber)
	return result
}
func PortZápisbyte(portnumber uint16, data uint8) {
	PortVýstupbyte(portnumber, data)
}
func PortČítaniebyte(portnumber uint16) uint8 {
	result := Portnabyte(portnumber)
	return result
}

type TPort16bit struct {
	TPort
}

func (vlastný *TPort16bit) Init(portnumber uint16) {
	vlastný.TPort.portnumber = portnumber
}
func (vlastný *TPort16bit) Zápis(data uint16) {
	PortVýstupslovo(vlastný.TPort.portnumber, data)
}
func (vlastný *TPort16bit) Čítanie() uint16 {
	var result = Portnaslovo(vlastný.TPort.portnumber)
	return result
}
func PortZápisslovo(portnumber uint16, data uint16) {
	PortVýstupslovo(portnumber, data)
}
func PortČítanieslovo(portnumber uint16) uint16 {
	var result uint16 = Portnaslovo(portnumber)
	return result
}

type TPort32bit struct {
	TPort
}

func (vlastný *TPort32bit) Init(portnumber uint16) {
	vlastný.TPort.portnumber = portnumber
}
func (vlastný *TPort32bit) Zápis(data uint32) {
	PortVýstupdword(vlastný.TPort.portnumber, data)
}
func (vlastný *TPort32bit) Čítanie() {
	Portnadword(vlastný.TPort.portnumber)
}
func PortZápisdword(portnumber uint16, data uint32) {
	PortVýstupdword(portnumber, data)
}
func PortČítaniedword(portnumber uint16) uint32 {
	var result uint32 = Portnadword(portnumber)
	return result
}

var čítaniecount uint16 = 65
var zápiscount uint16 = 66

func PortVýstupbyte(portnumber uint16, data uint8)
func Portnabyte(portnumber uint16) uint8

func PortVýstupslovo(portnumber uint16, data uint16)
func Portnaslovo(portnumber uint16) uint16

func PortVýstupdword(portnumber uint16, data uint32)
func Portnadword(portnumber uint16) uint32
