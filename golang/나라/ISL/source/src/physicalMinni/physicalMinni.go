package physicalMinni

import (
	. "algengt"
	. "unsafe"
)

const (
	BlokkStærð	uint32	= 4 * 1024
	Blokkperbyte	uint32	= 8
)

type multibootMinnimap struct {
	stærð		uint32
	baseaddressLágt	uint64
	baseaddressHátt	uint64
	lengdLágt	uint64
	lengdHátt	uint64
	Tegund		uint32
}

func PhymemPrófun() {
}

var minnioper Minnioper = Minnioper{}

type PhysicalMinnimanager struct {
	minniStærð	uint32
	notaðBlokk	uint32
	hámarkBlokk	uint32
	minniFylki	[]uint32
}

var (
	hámarkBlokk		uint32	= 0
	minniFylki		[]uint32
	grubmultibootMinnimapt	multibootMinnimap
)

func (sjálft *PhysicalMinnimanager) Setjabit(bit uint32) uint32 {
	sjálft.minniFylki[bit/32] = sjálft.minniFylki[bit/32] | (1 << (bit % 32))
	return sjálft.minniFylki[bit/32]
}
func (sjálft *PhysicalMinnimanager) Toggle_allocation_bit(bit uint32) uint32 {
	sjálft.minniFylki[bit/32] = sjálft.minniFylki[bit/32] ^ (1 << (bit % 32))
	return sjálft.minniFylki[bit/32]
}
func (sjálft *PhysicalMinnimanager) Prófunbit(bit uint32) uint32 {
	ret := sjálft.minniFylki[bit/32] & (1 << (bit % 32))
	return ret
}
func (sjálft *PhysicalMinnimanager) TotalBlokk() uint32 {
	return sjálft.hámarkBlokk
}
func (sjálft *PhysicalMinnimanager) NotaðBlokk() uint32 {
	return sjálft.notaðBlokk
}
func (sjálft *PhysicalMinnimanager) UpphæðafMinni() uint32 {
	return sjálft.minniStærð
}
func (sjálft *PhysicalMinnimanager) GetbitmaspStærð() uint32 {
	return sjálft.minniStærð / BlokkStærð / Blokkperbyte
}

func (sjálft *PhysicalMinnimanager) Firstlaust() uint32 {
	for i := uint32(0); i < sjálft.TotalBlokk(); i++ {
		if sjálft.minniFylki[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (minniFylki[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (sjálft *PhysicalMinnimanager) FirstlaustStærð(stærð uint32) uint32 {
	if stærð == 0 {
		return 0xffffffff
	}
	if stærð == 1 {
		return sjálft.Firstlaust()
	}

	for i := uint32(0); i < sjálft.TotalBlokk(); i++ {
		if sjálft.minniFylki[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if sjálft.minniFylki[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var laust uint32 = 0
					for count := uint32(0); count <= stærð; count++ {
						if sjálft.Prófunbit(startingbit+count) == 0 {
							laust++
						}

						if laust == stærð {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (sjálft *PhysicalMinnimanager) Init(stærð uint32, bitmap []uint32) {
	sjálft.minniStærð = stærð
	sjálft.minniFylki = bitmap
	sjálft.hámarkBlokk = stærð / BlokkStærð
	sjálft.notaðBlokk = sjálft.hámarkBlokk
	minnioper.MemSetja(uintptr(Pointer(&sjálft.minniFylki)), 0xFF, sjálft.notaðBlokk/Blokkperbyte)
}
func (sjálft *PhysicalMinnimanager) AllocateBlokk() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (sjálft *PhysicalMinnimanager) SíðaroundUpp(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (sjálft *PhysicalMinnimanager) SíðaroundNiður(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
