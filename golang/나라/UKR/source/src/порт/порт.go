package порт

var позиція uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8біт struct {
	TПорт
	читанняВідлік	uint16
	записВідлік	uint16
}

func (поточний *TПорт8біт) Init(portnumber uint16) {
	поточний.portnumber = portnumber
	поточний.читанняВідлік = 65
	поточний.записВідлік = 65
}
func (поточний *TПорт8біт) Запис(data uint8) {
	ПортВихіднийbyte(поточний.portnumber, data)
}
func (поточний *TПорт8біт) Читання() uint8 {
	var яРЛИК = ПортВхіднийbyte(поточний.portnumber)
	return яРЛИК
}
func ПортЗаписbyte(portnumber uint16, data uint8) {
	ПортВихіднийbyte(portnumber, data)
}
func ПортЧитанняbyte(portnumber uint16) uint8 {
	яРЛИК := ПортВхіднийbyte(portnumber)
	return яРЛИК
}

type TПорт16біт struct {
	TПорт
}

func (поточний *TПорт16біт) Init(portnumber uint16) {
	поточний.TПорт.portnumber = portnumber
}
func (поточний *TПорт16біт) Запис(data uint16) {
	ПортВихіднийслово(поточний.TПорт.portnumber, data)
}
func (поточний *TПорт16біт) Читання() uint16 {
	var яРЛИК = ПортВхіднийслово(поточний.TПорт.portnumber)
	return яРЛИК
}
func ПортЗаписслово(portnumber uint16, data uint16) {
	ПортВихіднийслово(portnumber, data)
}
func ПортЧитанняслово(portnumber uint16) uint16 {
	var яРЛИК uint16 = ПортВхіднийслово(portnumber)
	return яРЛИК
}

type TПорт32біт struct {
	TПорт
}

func (поточний *TПорт32біт) Init(portnumber uint16) {
	поточний.TПорт.portnumber = portnumber
}
func (поточний *TПорт32біт) Запис(data uint32) {
	ПортВихіднийdword(поточний.TПорт.portnumber, data)
}
func (поточний *TПорт32біт) Читання() {
	ПортВхіднийdword(поточний.TПорт.portnumber)
}
func ПортЗаписdword(portnumber uint16, data uint32) {
	ПортВихіднийdword(portnumber, data)
}
func ПортЧитанняdword(portnumber uint16) uint32 {
	var яРЛИК uint32 = ПортВхіднийdword(portnumber)
	return яРЛИК
}

var читанняВідлік uint16 = 65
var записВідлік uint16 = 66

func ПортВихіднийbyte(portnumber uint16, data uint8)
func ПортВхіднийbyte(portnumber uint16) uint8

func ПортВихіднийслово(portnumber uint16, data uint16)
func ПортВхіднийслово(portnumber uint16) uint16

func ПортВихіднийdword(portnumber uint16, data uint32)
func ПортВхіднийdword(portnumber uint16) uint32
