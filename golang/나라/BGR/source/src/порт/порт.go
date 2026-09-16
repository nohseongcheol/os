/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package порт

var позиция uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	четенеcount	uint16
	писанеcount	uint16
}

func (себеси *TПорт8bit) Init(portnumber uint16) {
	себеси.portnumber = portnumber
	себеси.четенеcount = 65
	себеси.писанеcount = 65
}
func (себеси *TПорт8bit) Писане(data uint8) {
	ПортИзходящbyte(себеси.portnumber, data)
}
func (себеси *TПорт8bit) Четене() uint8 {
	var рЕЗУЛТАТ = ПортВходящbyte(себеси.portnumber)
	return рЕЗУЛТАТ
}
func ПортПисанеbyte(portnumber uint16, data uint8) {
	ПортИзходящbyte(portnumber, data)
}
func ПортЧетенеbyte(portnumber uint16) uint8 {
	рЕЗУЛТАТ := ПортВходящbyte(portnumber)
	return рЕЗУЛТАТ
}

type TПорт16bit struct {
	TПорт
}

func (себеси *TПорт16bit) Init(portnumber uint16) {
	себеси.TПорт.portnumber = portnumber
}
func (себеси *TПорт16bit) Писане(data uint16) {
	ПортИзходящдума(себеси.TПорт.portnumber, data)
}
func (себеси *TПорт16bit) Четене() uint16 {
	var рЕЗУЛТАТ = ПортВходящдума(себеси.TПорт.portnumber)
	return рЕЗУЛТАТ
}
func ПортПисанедума(portnumber uint16, data uint16) {
	ПортИзходящдума(portnumber, data)
}
func ПортЧетенедума(portnumber uint16) uint16 {
	var рЕЗУЛТАТ uint16 = ПортВходящдума(portnumber)
	return рЕЗУЛТАТ
}

type TПорт32bit struct {
	TПорт
}

func (себеси *TПорт32bit) Init(portnumber uint16) {
	себеси.TПорт.portnumber = portnumber
}
func (себеси *TПорт32bit) Писане(data uint32) {
	ПортИзходящdword(себеси.TПорт.portnumber, data)
}
func (себеси *TПорт32bit) Четене() {
	ПортВходящdword(себеси.TПорт.portnumber)
}
func ПортПисанеdword(portnumber uint16, data uint32) {
	ПортИзходящdword(portnumber, data)
}
func ПортЧетенеdword(portnumber uint16) uint32 {
	var рЕЗУЛТАТ uint32 = ПортВходящdword(portnumber)
	return рЕЗУЛТАТ
}

var четенеcount uint16 = 65
var писанеcount uint16 = 66

func ПортИзходящbyte(portnumber uint16, data uint8)
func ПортВходящbyte(portnumber uint16) uint8

func ПортИзходящдума(portnumber uint16, data uint16)
func ПортВходящдума(portnumber uint16) uint16

func ПортИзходящdword(portnumber uint16, data uint32)
func ПортВходящdword(portnumber uint16) uint32
