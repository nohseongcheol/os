/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const HámarkqueueStærð uint32 = 0x1FFFFFF
const QueueRæsaaddress uint32 = 0x1000000

type TMinnichunk struct {
	næsta		*TMinnichunk
	previous	*TMinnichunk
	allocated	bool

	stærð	uint32
}

type TMinnimanager struct {
}

var first *TMinnichunk
var VirktMinnimanager *TMinnimanager = nil
var minnichunkStærð uint32

func (sjálft *TMinnimanager) Init(ræsa uint32, stærð uint32) {

	VirktMinnimanager = sjálft

	minnichunkStærð = uint32(Sizeof(TMinnichunk{}))

	if stærð < minnichunkStærð {
		first = nil
	} else {
		first = (*TMinnichunk)(Pointer(uintptr(QueueRæsaaddress) + uintptr(ræsa)))
		first.allocated = false
		first.previous = nil
		first.næsta = nil
		first.stærð = stærð - minnichunkStærð
	}
}
func (sjálft *TMinnimanager) Eyðileggja() {
	if VirktMinnimanager == sjálft {
		VirktMinnimanager = nil
	}
}
func (sjálft *TMinnimanager) Malloc(stærð uint32) Pointer {
	var nIÐURSTAÐA *TMinnichunk = nil

	var chunk *TMinnichunk = first
	for ; chunk != nil && nIÐURSTAÐA == nil; chunk = chunk.næsta {
		if chunk.stærð > stærð && !chunk.allocated {
			nIÐURSTAÐA = chunk
		}
	}

	if nIÐURSTAÐA == nil {
		return nil
	}

	if nIÐURSTAÐA.stærð >= (stærð + minnichunkStærð + 1) {

		var temporary *TMinnichunk
		temporary = (*TMinnichunk)(Pointer(uintptr(uint32(uintptr(Pointer(nIÐURSTAÐA))) + minnichunkStærð + stærð)))

		temporary.allocated = false
		temporary.stærð = nIÐURSTAÐA.stærð - stærð - minnichunkStærð
		temporary.previous = nIÐURSTAÐA
		temporary.næsta = nIÐURSTAÐA.næsta

		if temporary.næsta != nil {
			temporary.næsta.previous = temporary
		}

		nIÐURSTAÐA.stærð = stærð
		nIÐURSTAÐA.næsta = temporary
	}
	nIÐURSTAÐA.allocated = true

	return Pointer(uintptr(Pointer(nIÐURSTAÐA)) + uintptr(minnichunkStærð))
}
func (sjálft *TMinnimanager) Alignedmalloc(stærð uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if stærð == 0 || stærð > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var nIÐURSTAÐA *TMinnichunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.næsta {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(minnichunkStærð))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.stærð && stærð <= chunk.stærð-diff {
			nIÐURSTAÐA = chunk
			break
		}
	}
	if nIÐURSTAÐA == nil {
		return nil, 0
	}
	stærð += diff
	if nIÐURSTAÐA.stærð-stærð >= minnichunkStærð+1 {
		temporary := (*TMinnichunk)(Pointer(uintptr(Pointer(nIÐURSTAÐA)) + uintptr(minnichunkStærð) + uintptr(stærð)))
		temporary.allocated = false
		temporary.stærð = nIÐURSTAÐA.stærð - stærð - minnichunkStærð
		temporary.previous = nIÐURSTAÐA
		temporary.næsta = nIÐURSTAÐA.næsta
		if temporary.næsta != nil {
			temporary.næsta.previous = temporary
		}
		nIÐURSTAÐA.stærð = stærð
		nIÐURSTAÐA.næsta = temporary
	}
	nIÐURSTAÐA.allocated = true
	return Pointer(uintptr(Pointer(nIÐURSTAÐA)) + uintptr(minnichunkStærð) + uintptr(diff)), diff
}
func (sjálft *TMinnimanager) Laust(bendill_2 Pointer) {
	var chunk *TMinnichunk = (*TMinnichunk)(Pointer(uintptr(bendill_2) - uintptr(minnichunkStærð)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.næsta = chunk.næsta
		chunk.previous.stærð += chunk.stærð + minnichunkStærð
		if chunk.næsta != nil {
			chunk.næsta.previous = chunk.previous
		}
	}

	if chunk.næsta != nil && !chunk.næsta.allocated {
		chunk.stærð += chunk.næsta.stærð + minnichunkStærð
		chunk.næsta = chunk.næsta.næsta
		if chunk.næsta != nil {
			chunk.næsta.previous = chunk
		}
	}
}
func Nýtt(stærð int) Pointer {
	if VirktMinnimanager == nil {
		return nil
	}
	return VirktMinnimanager.Malloc(uint32(stærð))
}
func Eyða(bendill_2 Pointer) {
	if VirktMinnimanager != nil {
		VirktMinnimanager.Laust(bendill_2)
	}
}
