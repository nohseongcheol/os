package таймер

import . "unsafe"

import . "переривання"
import . "консоль"

type IТаймерПодіяhandler interface {
	Увімкненоtick()
}

var iТаймерПодіяhandler IТаймерПодіяhandler

type TТиповийТаймерПодіяhandler struct {
}

func (поточний *TТиповийТаймерПодіяhandler) Увімкненоtick() {
}

type TТаймерdriver struct {
	TПерериванняhandler
}

var перериванняhandler func(*TТаймерdriver, uint32) uint32

func (поточний *TТаймерdriver) Init(manager *TПерериванняmanager, клавіатураПодіяhandler IТаймерПодіяhandler) {
	iТаймерПодіяhandler = &TТиповийТаймерПодіяhandler{}
	if клавіатураПодіяhandler != nil {
		iТаймерПодіяhandler = клавіатураПодіяhandler
	}

	перериванняhandler = (*TТаймерdriver).ЕлементкеруванняПереривання
	var адреса uintptr
	адреса = uintptr(Pointer(&перериванняhandler))

	поточний.TПерериванняhandler.Init(0x20, uintptr(Pointer(manager)), адреса)

}

var tickВідлік uint32 = 0

func (поточний *TТаймерdriver) ЕлементкеруванняПереривання(esp uint32) uint32 {
	консоль_2 := TКонсоль{}
	консоль_2.MUnsignedinteger32Друкxy(tickВідлік, 3, 1)
	tickВідлік++

	return esp
}
