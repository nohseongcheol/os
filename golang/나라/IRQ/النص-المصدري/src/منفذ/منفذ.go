package منفذ

var الموضع uint16 = 1

type Tمنفذ struct {
	portnumber uint16
}

type Tمنفذ8bit struct {
	Tمنفذ
	قراءةcount	uint16
	كتابةcount	uint16
}

func (نفسه *Tمنفذ8bit) Init(portnumber uint16) {
	نفسه.portnumber = portnumber
	نفسه.قراءةcount = 65
	نفسه.كتابةcount = 65
}
func (نفسه *Tمنفذ8bit) Wكتابة(بيانات uint8) {
	Pمنفذخارجبايت(نفسه.portnumber, بيانات)
}
func (نفسه *Tمنفذ8bit) Rقراءة() uint8 {
	var result = Pمنفذداخلبايت(نفسه.portnumber)
	return result
}
func Pمنفذكتابةبايت(portnumber uint16, بيانات uint8) {
	Pمنفذخارجبايت(portnumber, بيانات)
}
func Pمنفذقراءةبايت(portnumber uint16) uint8 {
	result := Pمنفذداخلبايت(portnumber)
	return result
}

type Tمنفذ16bit struct {
	Tمنفذ
}

func (نفسه *Tمنفذ16bit) Init(portnumber uint16) {
	نفسه.Tمنفذ.portnumber = portnumber
}
func (نفسه *Tمنفذ16bit) Wكتابة(بيانات uint16) {
	Pمنفذخارجكلمة(نفسه.Tمنفذ.portnumber, بيانات)
}
func (نفسه *Tمنفذ16bit) Rقراءة() uint16 {
	var result = Pمنفذداخلكلمة(نفسه.Tمنفذ.portnumber)
	return result
}
func Pمنفذكتابةكلمة(portnumber uint16, بيانات uint16) {
	Pمنفذخارجكلمة(portnumber, بيانات)
}
func Pمنفذقراءةكلمة(portnumber uint16) uint16 {
	var result uint16 = Pمنفذداخلكلمة(portnumber)
	return result
}

type Tمنفذ32bit struct {
	Tمنفذ
}

func (نفسه *Tمنفذ32bit) Init(portnumber uint16) {
	نفسه.Tمنفذ.portnumber = portnumber
}
func (نفسه *Tمنفذ32bit) Wكتابة(بيانات uint32) {
	Pمنفذخارجdword(نفسه.Tمنفذ.portnumber, بيانات)
}
func (نفسه *Tمنفذ32bit) Rقراءة() {
	Pمنفذداخلdword(نفسه.Tمنفذ.portnumber)
}
func Pمنفذكتابةdword(portnumber uint16, بيانات uint32) {
	Pمنفذخارجdword(portnumber, بيانات)
}
func Pمنفذقراءةdword(portnumber uint16) uint32 {
	var result uint32 = Pمنفذداخلdword(portnumber)
	return result
}

var قراءةcount uint16 = 65
var كتابةcount uint16 = 66

func Pمنفذخارجبايت(portnumber uint16, بيانات uint8)
func Pمنفذداخلبايت(portnumber uint16) uint8

func Pمنفذخارجكلمة(portnumber uint16, بيانات uint16)
func Pمنفذداخلكلمة(portnumber uint16) uint16

func Pمنفذخارجdword(portnumber uint16, بيانات uint32)
func Pمنفذداخلdword(portnumber uint16) uint32
