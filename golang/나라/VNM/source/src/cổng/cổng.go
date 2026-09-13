package cổng

var vịtrí uint16 = 1

type TCổng struct {
	portnumber uint16
}

type TCổng8bit struct {
	TCổng
	đọcSốlượng	uint16
	ghiSốlượng	uint16
}

func (mình *TCổng8bit) Init(portnumber uint16) {
	mình.portnumber = portnumber
	mình.đọcSốlượng = 65
	mình.ghiSốlượng = 65
}
func (mình *TCổng8bit) Ghi(data uint8) {
	CổngRabyte(mình.portnumber, data)
}
func (mình *TCổng8bit) Đọc() uint8 {
	var result = CổngVàobyte(mình.portnumber)
	return result
}
func CổngGhibyte(portnumber uint16, data uint8) {
	CổngRabyte(portnumber, data)
}
func CổngĐọcbyte(portnumber uint16) uint8 {
	result := CổngVàobyte(portnumber)
	return result
}

type TCổng16bit struct {
	TCổng
}

func (mình *TCổng16bit) Init(portnumber uint16) {
	mình.TCổng.portnumber = portnumber
}
func (mình *TCổng16bit) Ghi(data uint16) {
	CổngRatừ(mình.TCổng.portnumber, data)
}
func (mình *TCổng16bit) Đọc() uint16 {
	var result = CổngVàotừ(mình.TCổng.portnumber)
	return result
}
func CổngGhitừ(portnumber uint16, data uint16) {
	CổngRatừ(portnumber, data)
}
func CổngĐọctừ(portnumber uint16) uint16 {
	var result uint16 = CổngVàotừ(portnumber)
	return result
}

type TCổng32bit struct {
	TCổng
}

func (mình *TCổng32bit) Init(portnumber uint16) {
	mình.TCổng.portnumber = portnumber
}
func (mình *TCổng32bit) Ghi(data uint32) {
	CổngRadword(mình.TCổng.portnumber, data)
}
func (mình *TCổng32bit) Đọc() {
	CổngVàodword(mình.TCổng.portnumber)
}
func CổngGhidword(portnumber uint16, data uint32) {
	CổngRadword(portnumber, data)
}
func CổngĐọcdword(portnumber uint16) uint32 {
	var result uint32 = CổngVàodword(portnumber)
	return result
}

var đọcSốlượng uint16 = 65
var ghiSốlượng uint16 = 66

func CổngRabyte(portnumber uint16, data uint8)
func CổngVàobyte(portnumber uint16) uint8

func CổngRatừ(portnumber uint16, data uint16)
func CổngVàotừ(portnumber uint16) uint16

func CổngRadword(portnumber uint16, data uint32)
func CổngVàodword(portnumber uint16) uint32
