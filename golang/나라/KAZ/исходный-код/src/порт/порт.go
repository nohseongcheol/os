package порт

var позиция uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	читатьКоличество	uint16
	писатьКоличество	uint16
}

func (текущий *TПорт8bit) Init(portnumber uint16) {
	текущий.portnumber = portnumber
	текущий.читатьКоличество = 65
	текущий.писатьКоличество = 65
}
func (текущий *TПорт8bit) Писать(данные uint8) {
	ПортВходящийбайт(текущий.portnumber, данные)
}
func (текущий *TПорт8bit) Читать() uint8 {
	var рЕЗУЛЬТАТ = ПортИсходящийбайт(текущий.portnumber)
	return рЕЗУЛЬТАТ
}
func Портписатьбайт(portnumber uint16, данные uint8) {
	ПортВходящийбайт(portnumber, данные)
}
func Портчитатьбайт(portnumber uint16) uint8 {
	рЕЗУЛЬТАТ := ПортИсходящийбайт(portnumber)
	return рЕЗУЛЬТАТ
}

type TПорт16bit struct {
	TПорт
}

func (текущий *TПорт16bit) Init(portnumber uint16) {
	текущий.TПорт.portnumber = portnumber
}
func (текущий *TПорт16bit) Писать(данные uint16) {
	ПортВходящийслово(текущий.TПорт.portnumber, данные)
}
func (текущий *TПорт16bit) Читать() uint16 {
	var рЕЗУЛЬТАТ = ПортИсходящийслово(текущий.TПорт.portnumber)
	return рЕЗУЛЬТАТ
}
func Портписатьслово(portnumber uint16, данные uint16) {
	ПортВходящийслово(portnumber, данные)
}
func Портчитатьслово(portnumber uint16) uint16 {
	var рЕЗУЛЬТАТ uint16 = ПортИсходящийслово(portnumber)
	return рЕЗУЛЬТАТ
}

type TПорт32bit struct {
	TПорт
}

func (текущий *TПорт32bit) Init(portnumber uint16) {
	текущий.TПорт.portnumber = portnumber
}
func (текущий *TПорт32bit) Писать(данные uint32) {
	ПортВходящийdword(текущий.TПорт.portnumber, данные)
}
func (текущий *TПорт32bit) Читать() {
	ПортИсходящийdword(текущий.TПорт.portnumber)
}
func Портписатьdword(portnumber uint16, данные uint32) {
	ПортВходящийdword(portnumber, данные)
}
func Портчитатьdword(portnumber uint16) uint32 {
	var рЕЗУЛЬТАТ uint32 = ПортИсходящийdword(portnumber)
	return рЕЗУЛЬТАТ
}

var читатьКоличество uint16 = 65
var писатьКоличество uint16 = 66

func ПортВходящийбайт(portnumber uint16, данные uint8)
func ПортИсходящийбайт(portnumber uint16) uint8

func ПортВходящийслово(portnumber uint16, данные uint16)
func ПортИсходящийслово(portnumber uint16) uint16

func ПортВходящийdword(portnumber uint16, данные uint32)
func ПортИсходящийdword(portnumber uint16) uint32
