package physicalMemoria

import (
	. "tëpërbashkët"
	. "unsafe"
)

const (
	BlockMadhësia	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootMemoriamap struct {
	madhësia		uint32
	baseaddressUlët		uint64
	baseaddressLartë	uint64
	gjatësiUlët		uint64
	gjatësiLartë		uint64
	Lloji			uint32
}

func PhymemProvo() {
}

var memoriaoper Memoriaoper = Memoriaoper{}

type PhysicalMemoriaManazhuesi struct {
	memoriaMadhësia		uint32
	përdorurblock		uint32
	maksimumblock		uint32
	memoriaRreshtimi	[]uint32
}

var (
	maksimumblock			uint32	= 0
	memoriaRreshtimi		[]uint32
	grubmultibootMemoriamapt	multibootMemoriamap
)

func (vetvetja *PhysicalMemoriaManazhuesi) Caktonibit(bit uint32) uint32 {
	vetvetja.memoriaRreshtimi[bit/32] = vetvetja.memoriaRreshtimi[bit/32] | (1 << (bit % 32))
	return vetvetja.memoriaRreshtimi[bit/32]
}
func (vetvetja *PhysicalMemoriaManazhuesi) Toggle_allocation_bit(bit uint32) uint32 {
	vetvetja.memoriaRreshtimi[bit/32] = vetvetja.memoriaRreshtimi[bit/32] ^ (1 << (bit % 32))
	return vetvetja.memoriaRreshtimi[bit/32]
}
func (vetvetja *PhysicalMemoriaManazhuesi) Provobit(bit uint32) uint32 {
	ret := vetvetja.memoriaRreshtimi[bit/32] & (1 << (bit % 32))
	return ret
}
func (vetvetja *PhysicalMemoriaManazhuesi) Gjithsejblock() uint32 {
	return vetvetja.maksimumblock
}
func (vetvetja *PhysicalMemoriaManazhuesi) Përdorurblock() uint32 {
	return vetvetja.përdorurblock
}
func (vetvetja *PhysicalMemoriaManazhuesi) SasiangaMemoria() uint32 {
	return vetvetja.memoriaMadhësia
}
func (vetvetja *PhysicalMemoriaManazhuesi) GetbitmaspMadhësia() uint32 {
	return vetvetja.memoriaMadhësia / BlockMadhësia / Blockperbyte
}

func (vetvetja *PhysicalMemoriaManazhuesi) FirstElirë() uint32 {
	for i := uint32(0); i < vetvetja.Gjithsejblock(); i++ {
		if vetvetja.memoriaRreshtimi[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memoriaRreshtimi[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (vetvetja *PhysicalMemoriaManazhuesi) FirstElirëMadhësia(madhësia uint32) uint32 {
	if madhësia == 0 {
		return 0xffffffff
	}
	if madhësia == 1 {
		return vetvetja.FirstElirë()
	}

	for i := uint32(0); i < vetvetja.Gjithsejblock(); i++ {
		if vetvetja.memoriaRreshtimi[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if vetvetja.memoriaRreshtimi[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var elirë uint32 = 0
					for count := uint32(0); count <= madhësia; count++ {
						if vetvetja.Provobit(startingbit+count) == 0 {
							elirë++
						}

						if elirë == madhësia {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (vetvetja *PhysicalMemoriaManazhuesi) Init(madhësia uint32, bitmap []uint32) {
	vetvetja.memoriaMadhësia = madhësia
	vetvetja.memoriaRreshtimi = bitmap
	vetvetja.maksimumblock = madhësia / BlockMadhësia
	vetvetja.përdorurblock = vetvetja.maksimumblock
	memoriaoper.MemCaktoni(uintptr(Pointer(&vetvetja.memoriaRreshtimi)), 0xFF, vetvetja.përdorurblock/Blockperbyte)
}
func (vetvetja *PhysicalMemoriaManazhuesi) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (vetvetja *PhysicalMemoriaManazhuesi) FaqeroundSipër(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (vetvetja *PhysicalMemoriaManazhuesi) FaqeroundPoshtë(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
