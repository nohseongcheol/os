package physicalMemorie

import (
	. "comun"
	. "unsafe"
)

const (
	BlocMărime	uint32	= 4 * 1024
	Blocperbyte	uint32	= 8
)

type multibootMemoriemap struct {
	mărime			uint32
	baseaddressScăzută	uint64
	baseaddressRidicată	uint64
	duratăScăzută		uint64
	duratăRidicată		uint64
	Tip			uint32
}

func PhymemTestează() {
}

var memorieoper Memorieoper = Memorieoper{}

type PhysicalMemoriemanager struct {
	memorieMărime	uint32
	folositBloc	uint32
	maximBloc	uint32
	memorieVector	[]uint32
}

var (
	maximBloc			uint32	= 0
	memorieVector			[]uint32
	grubmultibootMemoriemapt	multibootMemoriemap
)

func (sine *PhysicalMemoriemanager) Definitbit(bit uint32) uint32 {
	sine.memorieVector[bit/32] = sine.memorieVector[bit/32] | (1 << (bit % 32))
	return sine.memorieVector[bit/32]
}
func (sine *PhysicalMemoriemanager) Toggle_allocation_bit(bit uint32) uint32 {
	sine.memorieVector[bit/32] = sine.memorieVector[bit/32] ^ (1 << (bit % 32))
	return sine.memorieVector[bit/32]
}
func (sine *PhysicalMemoriemanager) Testeazăbit(bit uint32) uint32 {
	ret := sine.memorieVector[bit/32] & (1 << (bit % 32))
	return ret
}
func (sine *PhysicalMemoriemanager) TotalBloc() uint32 {
	return sine.maximBloc
}
func (sine *PhysicalMemoriemanager) FolositBloc() uint32 {
	return sine.folositBloc
}
func (sine *PhysicalMemoriemanager) CantitatedinMemorie() uint32 {
	return sine.memorieMărime
}
func (sine *PhysicalMemoriemanager) GetbitmaspMărime() uint32 {
	return sine.memorieMărime / BlocMărime / Blocperbyte
}

func (sine *PhysicalMemoriemanager) FirstLiber() uint32 {
	for i := uint32(0); i < sine.TotalBloc(); i++ {
		if sine.memorieVector[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memorieVector[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (sine *PhysicalMemoriemanager) FirstLiberMărime(mărime uint32) uint32 {
	if mărime == 0 {
		return 0xffffffff
	}
	if mărime == 1 {
		return sine.FirstLiber()
	}

	for i := uint32(0); i < sine.TotalBloc(); i++ {
		if sine.memorieVector[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if sine.memorieVector[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var liber uint32 = 0
					for count := uint32(0); count <= mărime; count++ {
						if sine.Testeazăbit(startingbit+count) == 0 {
							liber++
						}

						if liber == mărime {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (sine *PhysicalMemoriemanager) Init(mărime uint32, bitmap []uint32) {
	sine.memorieMărime = mărime
	sine.memorieVector = bitmap
	sine.maximBloc = mărime / BlocMărime
	sine.folositBloc = sine.maximBloc
	memorieoper.Memdefinit(uintptr(Pointer(&sine.memorieVector)), 0xFF, sine.folositBloc/Blocperbyte)
}
func (sine *PhysicalMemoriemanager) AllocateBloc() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (sine *PhysicalMemoriemanager) PAGINĂRotunjireSus(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (sine *PhysicalMemoriemanager) PAGINĂRotunjireÎnjos(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
