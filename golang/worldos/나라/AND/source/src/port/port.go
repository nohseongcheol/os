/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package port

var posició uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	lecturaRecompte		uint16
	escripturaRecompte	uint16
}

func (unmateix *TPort8bit) Init(portnumber uint16) {
	unmateix.portnumber = portnumber
	unmateix.lecturaRecompte = 65
	unmateix.escripturaRecompte = 65
}
func (unmateix *TPort8bit) Escriptura(data uint8) {
	PortSortidabyte(unmateix.portnumber, data)
}
func (unmateix *TPort8bit) Lectura() uint8 {
	var rESULTAT = Portabyte(unmateix.portnumber)
	return rESULTAT
}
func PortEscripturabyte(portnumber uint16, data uint8) {
	PortSortidabyte(portnumber, data)
}
func PortLecturabyte(portnumber uint16) uint8 {
	rESULTAT := Portabyte(portnumber)
	return rESULTAT
}

type TPort16bit struct {
	TPort
}

func (unmateix *TPort16bit) Init(portnumber uint16) {
	unmateix.TPort.portnumber = portnumber
}
func (unmateix *TPort16bit) Escriptura(data uint16) {
	PortSortidaparaula(unmateix.TPort.portnumber, data)
}
func (unmateix *TPort16bit) Lectura() uint16 {
	var rESULTAT = Portaparaula(unmateix.TPort.portnumber)
	return rESULTAT
}
func PortEscripturaparaula(portnumber uint16, data uint16) {
	PortSortidaparaula(portnumber, data)
}
func PortLecturaparaula(portnumber uint16) uint16 {
	var rESULTAT uint16 = Portaparaula(portnumber)
	return rESULTAT
}

type TPort32bit struct {
	TPort
}

func (unmateix *TPort32bit) Init(portnumber uint16) {
	unmateix.TPort.portnumber = portnumber
}
func (unmateix *TPort32bit) Escriptura(data uint32) {
	PortSortidadword(unmateix.TPort.portnumber, data)
}
func (unmateix *TPort32bit) Lectura() {
	Portadword(unmateix.TPort.portnumber)
}
func PortEscripturadword(portnumber uint16, data uint32) {
	PortSortidadword(portnumber, data)
}
func PortLecturadword(portnumber uint16) uint32 {
	var rESULTAT uint32 = Portadword(portnumber)
	return rESULTAT
}

var lecturaRecompte uint16 = 65
var escripturaRecompte uint16 = 66

func PortSortidabyte(portnumber uint16, data uint8)
func Portabyte(portnumber uint16) uint8

func PortSortidaparaula(portnumber uint16, data uint16)
func Portaparaula(portnumber uint16) uint16

func PortSortidadword(portnumber uint16, data uint32)
func Portadword(portnumber uint16) uint32
