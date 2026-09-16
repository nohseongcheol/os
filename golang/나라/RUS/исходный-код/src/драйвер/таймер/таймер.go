/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package таймер

import . "unsafe"

import . "прерывание"
import . "консоль"

type IТаймерсобытиеhandler interface {
	Приtick()
}

var iтаймерсобытиеhandler IТаймерсобытиеhandler

type TПоумолчаниютаймерсобытиеhandler struct {
}

func (текущий *TПоумолчаниютаймерсобытиеhandler) Приtick() {
}

type TТаймердрайвер struct {
	TПрерываниеhandler
}

var прерываниеhandler func(*TТаймердрайвер, uint32) uint32

func (текущий *TТаймердрайвер) Init(диспетчер *TПрерываниедиспетчер, клавиатурасобытиеhandler IТаймерсобытиеhandler) {
	iтаймерсобытиеhandler = &TПоумолчаниютаймерсобытиеhandler{}
	if клавиатурасобытиеhandler != nil {
		iтаймерсобытиеhandler = клавиатурасобытиеhandler
	}

	прерываниеhandler = (*TТаймердрайвер).Ручкапрерывание
	var address uintptr
	address = uintptr(Pointer(&прерываниеhandler))

	текущий.TПрерываниеhandler.Init(0x20, uintptr(Pointer(диспетчер)), address)

}

var tickКоличество uint32 = 0

func (текущий *TТаймердрайвер) Ручкапрерывание(esp uint32) uint32 {
	консоль_2 := TКонсоль{}
	консоль_2.MUnsignedinteger32Печатьxy(tickКоличество, 3, 1)
	tickКоличество++

	return esp
}
