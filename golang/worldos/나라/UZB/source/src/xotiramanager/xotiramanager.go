/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueHajmi uint32 = 0x1FFFFFF
const QueueBoshlashaddress uint32 = 0x1000000

type TXotirachunk struct {
	keyingi		*TXotirachunk
	previous	*TXotirachunk
	allocated	bool

	hajmi	uint32
}

type TXotiramanager struct {
}

var first *TXotirachunk
var FaolXotiramanager *TXotiramanager = nil
var xotirachunkHajmi uint32

func (self *TXotiramanager) Init(boshlash uint32, hajmi uint32) {

	FaolXotiramanager = self

	xotirachunkHajmi = uint32(Sizeof(TXotirachunk{}))

	if hajmi < xotirachunkHajmi {
		first = nil
	} else {
		first = (*TXotirachunk)(Pointer(uintptr(QueueBoshlashaddress) + uintptr(boshlash)))
		first.allocated = false
		first.previous = nil
		first.keyingi = nil
		first.hajmi = hajmi - xotirachunkHajmi
	}
}
func (self *TXotiramanager) Destroy() {
	if FaolXotiramanager == self {
		FaolXotiramanager = nil
	}
}
func (self *TXotiramanager) Malloc(hajmi uint32) Pointer {
	var result *TXotirachunk = nil

	var chunk *TXotirachunk = first
	for ; chunk != nil && result == nil; chunk = chunk.keyingi {
		if chunk.hajmi > hajmi && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.hajmi >= (hajmi + xotirachunkHajmi + 1) {

		var temporary *TXotirachunk
		temporary = (*TXotirachunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + xotirachunkHajmi + hajmi)))

		temporary.allocated = false
		temporary.hajmi = result.hajmi - hajmi - xotirachunkHajmi
		temporary.previous = result
		temporary.keyingi = result.keyingi

		if temporary.keyingi != nil {
			temporary.keyingi.previous = temporary
		}

		result.hajmi = hajmi
		result.keyingi = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(xotirachunkHajmi))
}
func (self *TXotiramanager) Alignedmalloc(hajmi uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if hajmi == 0 || hajmi > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TXotirachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.keyingi {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(xotirachunkHajmi))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.hajmi && hajmi <= chunk.hajmi-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	hajmi += diff
	if result.hajmi-hajmi >= xotirachunkHajmi+1 {
		temporary := (*TXotirachunk)(Pointer(uintptr(Pointer(result)) + uintptr(xotirachunkHajmi) + uintptr(hajmi)))
		temporary.allocated = false
		temporary.hajmi = result.hajmi - hajmi - xotirachunkHajmi
		temporary.previous = result
		temporary.keyingi = result.keyingi
		if temporary.keyingi != nil {
			temporary.keyingi.previous = temporary
		}
		result.hajmi = hajmi
		result.keyingi = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(xotirachunkHajmi) + uintptr(diff)), diff
}
func (self *TXotiramanager) Bosh(korsatgich_2 Pointer) {
	var chunk *TXotirachunk = (*TXotirachunk)(Pointer(uintptr(korsatgich_2) - uintptr(xotirachunkHajmi)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.keyingi = chunk.keyingi
		chunk.previous.hajmi += chunk.hajmi + xotirachunkHajmi
		if chunk.keyingi != nil {
			chunk.keyingi.previous = chunk.previous
		}
	}

	if chunk.keyingi != nil && !chunk.keyingi.allocated {
		chunk.hajmi += chunk.keyingi.hajmi + xotirachunkHajmi
		chunk.keyingi = chunk.keyingi.keyingi
		if chunk.keyingi != nil {
			chunk.keyingi.previous = chunk
		}
	}
}
func Yangi(hajmi int) Pointer {
	if FaolXotiramanager == nil {
		return nil
	}
	return FaolXotiramanager.Malloc(uint32(hajmi))
}
func Olibtashlash(korsatgich_2 Pointer) {
	if FaolXotiramanager != nil {
		FaolXotiramanager.Bosh(korsatgich_2)
	}
}
