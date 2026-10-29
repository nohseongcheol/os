/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const МаксимумочередьРазмер uint32 = 0x1FFFFFF
const ОчередьПускaddress uint32 = 0x1000000

type TПамятьchunk struct {
	далее		*TПамятьchunk
	previous	*TПамятьchunk
	allocated	bool

	размер	uint32
}

type TПамятьдиспетчер struct {
}

var first *TПамятьchunk
var Активнопамятьдиспетчер *TПамятьдиспетчер = nil
var памятьchunkРазмер uint32

func (текущий *TПамятьдиспетчер) Init(пуск uint32, размер uint32) {

	Активнопамятьдиспетчер = текущий

	памятьchunkРазмер = uint32(Sizeof(TПамятьchunk{}))

	if размер < памятьchunkРазмер {
		first = nil
	} else {
		first = (*TПамятьchunk)(Pointer(uintptr(ОчередьПускaddress) + uintptr(пуск)))
		first.allocated = false
		first.previous = nil
		first.далее = nil
		first.размер = размер - памятьchunkРазмер
	}
}
func (текущий *TПамятьдиспетчер) Уничтожить() {
	if Активнопамятьдиспетчер == текущий {
		Активнопамятьдиспетчер = nil
	}
}
func (текущий *TПамятьдиспетчер) Выделить_память(размер uint32) Pointer {
	var рЕЗУЛЬТАТ *TПамятьchunk = nil

	var chunk *TПамятьchunk = first
	for ; chunk != nil && рЕЗУЛЬТАТ == nil; chunk = chunk.далее {
		if chunk.размер > размер && !chunk.allocated {
			рЕЗУЛЬТАТ = chunk
		}
	}

	if рЕЗУЛЬТАТ == nil {
		return nil
	}

	if рЕЗУЛЬТАТ.размер >= (размер + памятьchunkРазмер + 1) {

		var temporary *TПамятьchunk
		temporary = (*TПамятьchunk)(Pointer(uintptr(uint32(uintptr(Pointer(рЕЗУЛЬТАТ))) + памятьchunkРазмер + размер)))

		temporary.allocated = false
		temporary.размер = рЕЗУЛЬТАТ.размер - размер - памятьchunkРазмер
		temporary.previous = рЕЗУЛЬТАТ
		temporary.далее = рЕЗУЛЬТАТ.далее

		if temporary.далее != nil {
			temporary.далее.previous = temporary
		}

		рЕЗУЛЬТАТ.размер = размер
		рЕЗУЛЬТАТ.далее = temporary
	}
	рЕЗУЛЬТАТ.allocated = true

	return Pointer(uintptr(Pointer(рЕЗУЛЬТАТ)) + uintptr(памятьchunkРазмер))
}
func (текущий *TПамятьдиспетчер) Alignedmalloc(размер uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if размер == 0 || размер > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var рЕЗУЛЬТАТ *TПамятьchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.далее {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(памятьchunkРазмер))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.размер && размер <= chunk.размер-diff {
			рЕЗУЛЬТАТ = chunk
			break
		}
	}
	if рЕЗУЛЬТАТ == nil {
		return nil, 0
	}
	размер += diff
	if рЕЗУЛЬТАТ.размер-размер >= памятьchunkРазмер+1 {
		temporary := (*TПамятьchunk)(Pointer(uintptr(Pointer(рЕЗУЛЬТАТ)) + uintptr(памятьchunkРазмер) + uintptr(размер)))
		temporary.allocated = false
		temporary.размер = рЕЗУЛЬТАТ.размер - размер - памятьchunkРазмер
		temporary.previous = рЕЗУЛЬТАТ
		temporary.далее = рЕЗУЛЬТАТ.далее
		if temporary.далее != nil {
			temporary.далее.previous = temporary
		}
		рЕЗУЛЬТАТ.размер = размер
		рЕЗУЛЬТАТ.далее = temporary
	}
	рЕЗУЛЬТАТ.allocated = true
	return Pointer(uintptr(Pointer(рЕЗУЛЬТАТ)) + uintptr(памятьchunkРазмер) + uintptr(diff)), diff
}
func (текущий *TПамятьдиспетчер) Свободно(ссылка_на_адрес_2 Pointer) {
	var chunk *TПамятьchunk = (*TПамятьchunk)(Pointer(uintptr(ссылка_на_адрес_2) - uintptr(памятьchunkРазмер)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.далее = chunk.далее
		chunk.previous.размер += chunk.размер + памятьchunkРазмер
		if chunk.далее != nil {
			chunk.далее.previous = chunk.previous
		}
	}

	if chunk.далее != nil && !chunk.далее.allocated {
		chunk.размер += chunk.далее.размер + памятьchunkРазмер
		chunk.далее = chunk.далее.далее
		if chunk.далее != nil {
			chunk.далее.previous = chunk
		}
	}
}
func Новый(размер int) Pointer {
	if Активнопамятьдиспетчер == nil {
		return nil
	}
	return Активнопамятьдиспетчер.Выделить_память(uint32(размер))
}
func Удалить(ссылка_на_адрес_2 Pointer) {
	if Активнопамятьдиспетчер != nil {
		Активнопамятьдиспетчер.Свободно(ссылка_на_адрес_2)
	}
}
