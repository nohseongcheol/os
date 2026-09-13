package physicalحافظه

import (
	. "مشترک"
	. "unsafe"
)

const (
	Bقطعهاندازه	uint32	= 4 * 1024
	Bقطعهperbyte	uint32	= 8
)

type multibootحافظهmap struct {
	اندازه		uint32
	baseaddressاندک	uint64
	baseaddressزیاد	uint64
	طولاندک		uint64
	طولزیاد		uint64
	Tنوع		uint32
}

func Phymemtest() {
}

var حافظهoper Mحافظهoper = Mحافظهoper{}

type Physicalحافظهmanager struct {
	حافظهاندازه	uint32
	استفادهشدهقطعه	uint32
	بیشینهقطعه	uint32
	حافظهآرایه	[]uint32
}

var (
	بیشینهقطعه		uint32	= 0
	حافظهآرایه		[]uint32
	grubmultibootحافظهmapt	multibootحافظهmap
)

func (خود *Physicalحافظهmanager) Setbit(bit uint32) uint32 {
	خود.حافظهآرایه[bit/32] = خود.حافظهآرایه[bit/32] | (1 << (bit % 32))
	return خود.حافظهآرایه[bit/32]
}
func (خود *Physicalحافظهmanager) Toggle_allocation_bit(bit uint32) uint32 {
	خود.حافظهآرایه[bit/32] = خود.حافظهآرایه[bit/32] ^ (1 << (bit % 32))
	return خود.حافظهآرایه[bit/32]
}
func (خود *Physicalحافظهmanager) Testbit(bit uint32) uint32 {
	ret := خود.حافظهآرایه[bit/32] & (1 << (bit % 32))
	return ret
}
func (خود *Physicalحافظهmanager) Totalقطعه() uint32 {
	return خود.بیشینهقطعه
}
func (خود *Physicalحافظهmanager) Uاستفادهشدهقطعه() uint32 {
	return خود.استفادهشدهقطعه
}
func (خود *Physicalحافظهmanager) Aمقدارofحافظه() uint32 {
	return خود.حافظهاندازه
}
func (خود *Physicalحافظهmanager) Getbitmaspاندازه() uint32 {
	return خود.حافظهاندازه / Bقطعهاندازه / Bقطعهperbyte
}

func (خود *Physicalحافظهmanager) Firstآزاد() uint32 {
	for i := uint32(0); i < خود.Totalقطعه(); i++ {
		if خود.حافظهآرایه[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (حافظهآرایه[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (خود *Physicalحافظهmanager) Firstآزاداندازه(اندازه uint32) uint32 {
	if اندازه == 0 {
		return 0xffffffff
	}
	if اندازه == 1 {
		return خود.Firstآزاد()
	}

	for i := uint32(0); i < خود.Totalقطعه(); i++ {
		if خود.حافظهآرایه[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if خود.حافظهآرایه[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var آزاد uint32 = 0
					for count := uint32(0); count <= اندازه; count++ {
						if خود.Testbit(startingbit+count) == 0 {
							آزاد++
						}

						if آزاد == اندازه {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (خود *Physicalحافظهmanager) Init(اندازه uint32, bitmap []uint32) {
	خود.حافظهاندازه = اندازه
	خود.حافظهآرایه = bitmap
	خود.بیشینهقطعه = اندازه / Bقطعهاندازه
	خود.استفادهشدهقطعه = خود.بیشینهقطعه
	حافظهoper.Memset(uintptr(Pointer(&خود.حافظهآرایه)), 0xFF, خود.استفادهشدهقطعه/Bقطعهperbyte)
}
func (خود *Physicalحافظهmanager) Allocateقطعه() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (خود *Physicalحافظهmanager) Pصفحهگردکردنبالا(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (خود *Physicalحافظهmanager) Pصفحهگردکردنپایین(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
