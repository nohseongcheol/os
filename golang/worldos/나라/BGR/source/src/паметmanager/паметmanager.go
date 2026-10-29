/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const МаксqueueРазмер uint32 = 0x1FFFFFF
const QueueСтартиранеaddress uint32 = 0x1000000

type TПаметchunk struct {
	следващо	*TПаметchunk
	previous	*TПаметchunk
	allocated	bool

	размер	uint32
}

type TПаметmanager struct {
}

var first *TПаметchunk
var АктивнаПаметmanager *TПаметmanager = nil
var паметchunkРазмер uint32

func (себеси *TПаметmanager) Init(стартиране uint32, размер uint32) {

	АктивнаПаметmanager = себеси

	паметchunkРазмер = uint32(Sizeof(TПаметchunk{}))

	if размер < паметchunkРазмер {
		first = nil
	} else {
		first = (*TПаметchunk)(Pointer(uintptr(QueueСтартиранеaddress) + uintptr(стартиране)))
		first.allocated = false
		first.previous = nil
		first.следващо = nil
		first.размер = размер - паметchunkРазмер
	}
}
func (себеси *TПаметmanager) Унищожаване() {
	if АктивнаПаметmanager == себеси {
		АктивнаПаметmanager = nil
	}
}
func (себеси *TПаметmanager) Malloc(размер uint32) Pointer {
	var рЕЗУЛТАТ *TПаметchunk = nil

	var chunk *TПаметchunk = first
	for ; chunk != nil && рЕЗУЛТАТ == nil; chunk = chunk.следващо {
		if chunk.размер > размер && !chunk.allocated {
			рЕЗУЛТАТ = chunk
		}
	}

	if рЕЗУЛТАТ == nil {
		return nil
	}

	if рЕЗУЛТАТ.размер >= (размер + паметchunkРазмер + 1) {

		var temporary *TПаметchunk
		temporary = (*TПаметchunk)(Pointer(uintptr(uint32(uintptr(Pointer(рЕЗУЛТАТ))) + паметchunkРазмер + размер)))

		temporary.allocated = false
		temporary.размер = рЕЗУЛТАТ.размер - размер - паметchunkРазмер
		temporary.previous = рЕЗУЛТАТ
		temporary.следващо = рЕЗУЛТАТ.следващо

		if temporary.следващо != nil {
			temporary.следващо.previous = temporary
		}

		рЕЗУЛТАТ.размер = размер
		рЕЗУЛТАТ.следващо = temporary
	}
	рЕЗУЛТАТ.allocated = true

	return Pointer(uintptr(Pointer(рЕЗУЛТАТ)) + uintptr(паметchunkРазмер))
}
func (себеси *TПаметmanager) Alignedmalloc(размер uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if размер == 0 || размер > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var рЕЗУЛТАТ *TПаметchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.следващо {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(паметchunkРазмер))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.размер && размер <= chunk.размер-diff {
			рЕЗУЛТАТ = chunk
			break
		}
	}
	if рЕЗУЛТАТ == nil {
		return nil, 0
	}
	размер += diff
	if рЕЗУЛТАТ.размер-размер >= паметchunkРазмер+1 {
		temporary := (*TПаметchunk)(Pointer(uintptr(Pointer(рЕЗУЛТАТ)) + uintptr(паметchunkРазмер) + uintptr(размер)))
		temporary.allocated = false
		temporary.размер = рЕЗУЛТАТ.размер - размер - паметchunkРазмер
		temporary.previous = рЕЗУЛТАТ
		temporary.следващо = рЕЗУЛТАТ.следващо
		if temporary.следващо != nil {
			temporary.следващо.previous = temporary
		}
		рЕЗУЛТАТ.размер = размер
		рЕЗУЛТАТ.следващо = temporary
	}
	рЕЗУЛТАТ.allocated = true
	return Pointer(uintptr(Pointer(рЕЗУЛТАТ)) + uintptr(паметchunkРазмер) + uintptr(diff)), diff
}
func (себеси *TПаметmanager) Свободно(показалци_2 Pointer) {
	var chunk *TПаметchunk = (*TПаметchunk)(Pointer(uintptr(показалци_2) - uintptr(паметchunkРазмер)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.следващо = chunk.следващо
		chunk.previous.размер += chunk.размер + паметchunkРазмер
		if chunk.следващо != nil {
			chunk.следващо.previous = chunk.previous
		}
	}

	if chunk.следващо != nil && !chunk.следващо.allocated {
		chunk.размер += chunk.следващо.размер + паметchunkРазмер
		chunk.следващо = chunk.следващо.следващо
		if chunk.следващо != nil {
			chunk.следващо.previous = chunk
		}
	}
}
func Нов(размер int) Pointer {
	if АктивнаПаметmanager == nil {
		return nil
	}
	return АктивнаПаметmanager.Malloc(uint32(размер))
}
func Изтриване(показалци_2 Pointer) {
	if АктивнаПаметmanager != nil {
		АктивнаПаметmanager.Свободно(показалци_2)
	}
}
