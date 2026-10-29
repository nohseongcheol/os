/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueՉափս uint32 = 0x1FFFFFF
const QueueՍկիզբaddress uint32 = 0x1000000

type TՀիշողությունchunk struct {
	հաջորդ		*TՀիշողությունchunk
	previous	*TՀիշողությունchunk
	allocated	bool

	չափս	uint32
}

type TՀիշողությունmanager struct {
}

var first *TՀիշողությունchunk
var ԱկտիվՀիշողությունmanager *TՀիշողությունmanager = nil
var հիշողությունchunkՉափս uint32

func (ինքնուրույն *TՀիշողությունmanager) Init(սկիզբ uint32, չափս uint32) {

	ԱկտիվՀիշողությունmanager = ինքնուրույն

	հիշողությունchunkՉափս = uint32(Sizeof(TՀիշողությունchunk{}))

	if չափս < հիշողությունchunkՉափս {
		first = nil
	} else {
		first = (*TՀիշողությունchunk)(Pointer(uintptr(QueueՍկիզբaddress) + uintptr(սկիզբ)))
		first.allocated = false
		first.previous = nil
		first.հաջորդ = nil
		first.չափս = չափս - հիշողությունchunkՉափս
	}
}
func (ինքնուրույն *TՀիշողությունmanager) Destroy() {
	if ԱկտիվՀիշողությունmanager == ինքնուրույն {
		ԱկտիվՀիշողությունmanager = nil
	}
}
func (ինքնուրույն *TՀիշողությունmanager) Malloc(չափս uint32) Pointer {
	var result *TՀիշողությունchunk = nil

	var chunk *TՀիշողությունchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.հաջորդ {
		if chunk.չափս > չափս && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.չափս >= (չափս + հիշողությունchunkՉափս + 1) {

		var temporary *TՀիշողությունchunk
		temporary = (*TՀիշողությունchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + հիշողությունchunkՉափս + չափս)))

		temporary.allocated = false
		temporary.չափս = result.չափս - չափս - հիշողությունchunkՉափս
		temporary.previous = result
		temporary.հաջորդ = result.հաջորդ

		if temporary.հաջորդ != nil {
			temporary.հաջորդ.previous = temporary
		}

		result.չափս = չափս
		result.հաջորդ = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(հիշողությունchunkՉափս))
}
func (ինքնուրույն *TՀիշողությունmanager) Alignedmalloc(չափս uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if չափս == 0 || չափս > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TՀիշողությունchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.հաջորդ {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(հիշողությունchunkՉափս))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.չափս && չափս <= chunk.չափս-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	չափս += diff
	if result.չափս-չափս >= հիշողությունchunkՉափս+1 {
		temporary := (*TՀիշողությունchunk)(Pointer(uintptr(Pointer(result)) + uintptr(հիշողությունchunkՉափս) + uintptr(չափս)))
		temporary.allocated = false
		temporary.չափս = result.չափս - չափս - հիշողությունchunkՉափս
		temporary.previous = result
		temporary.հաջորդ = result.հաջորդ
		if temporary.հաջորդ != nil {
			temporary.հաջորդ.previous = temporary
		}
		result.չափս = չափս
		result.հաջորդ = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(հիշողությունchunkՉափս) + uintptr(diff)), diff
}
func (ինքնուրույն *TՀիշողությունmanager) Ազատ(ցուցիչ_2 Pointer) {
	var chunk *TՀիշողությունchunk = (*TՀիշողությունchunk)(Pointer(uintptr(ցուցիչ_2) - uintptr(հիշողությունchunkՉափս)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.հաջորդ = chunk.հաջորդ
		chunk.previous.չափս += chunk.չափս + հիշողությունchunkՉափս
		if chunk.հաջորդ != nil {
			chunk.հաջորդ.previous = chunk.previous
		}
	}

	if chunk.հաջորդ != nil && !chunk.հաջորդ.allocated {
		chunk.չափս += chunk.հաջորդ.չափս + հիշողությունchunkՉափս
		chunk.հաջորդ = chunk.հաջորդ.հաջորդ
		if chunk.հաջորդ != nil {
			chunk.հաջորդ.previous = chunk
		}
	}
}
func Նոր(չափս int) Pointer {
	if ԱկտիվՀիշողությունmanager == nil {
		return nil
	}
	return ԱկտիվՀիշողությունmanager.Malloc(uint32(չափս))
}
func Հեռացնել(ցուցիչ_2 Pointer) {
	if ԱկտիվՀիշողությունmanager != nil {
		ԱկտիվՀիշողությունmanager.Ազատ(ցուցիչ_2)
	}
}
