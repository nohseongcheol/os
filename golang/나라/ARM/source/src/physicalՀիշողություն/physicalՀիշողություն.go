package physicalՀիշողություն

import (
	. "common"
	. "unsafe"
)

const (
	ԱրգելափակելՉափս		uint32	= 4 * 1024
	Արգելափակելperbyte	uint32	= 8
)

type multibootՀիշողությունmap struct {
	չափս			uint32
	baseaddressՑածր		uint64
	baseaddressԲարձր	uint64
	երկարությունՑածր	uint64
	երկարությունԲարձր	uint64
	Տիպ			uint32
}

func PhymemԹեստ() {
}

var հիշողությունoper Հիշողությունoper = Հիշողությունoper{}

type PhysicalՀիշողությունmanager struct {
	հիշողությունՉափս	uint32
	օգտագործվածԱրգելափակել	uint32
	առավելագույնԱրգելափակել	uint32
	հիշողությունԶանգված	[]uint32
}

var (
	առավելագույնԱրգելափակել		uint32	= 0
	հիշողությունԶանգված		[]uint32
	grubmultibootՀիշողությունmapt	multibootՀիշողությունmap
)

func (ինքնուրույն *PhysicalՀիշողությունmanager) Setbit(bit uint32) uint32 {
	ինքնուրույն.հիշողությունԶանգված[bit/32] = ինքնուրույն.հիշողությունԶանգված[bit/32] | (1 << (bit % 32))
	return ինքնուրույն.հիշողությունԶանգված[bit/32]
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) Toggle_allocation_bit(bit uint32) uint32 {
	ինքնուրույն.հիշողությունԶանգված[bit/32] = ինքնուրույն.հիշողությունԶանգված[bit/32] ^ (1 << (bit % 32))
	return ինքնուրույն.հիշողությունԶանգված[bit/32]
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) Թեստbit(bit uint32) uint32 {
	ret := ինքնուրույն.հիշողությունԶանգված[bit/32] & (1 << (bit % 32))
	return ret
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) ԸնդհանուրԱրգելափակել() uint32 {
	return ինքնուրույն.առավելագույնԱրգելափակել
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) ՕգտագործվածԱրգելափակել() uint32 {
	return ինքնուրույն.օգտագործվածԱրգելափակել
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) ՔանակofՀիշողություն() uint32 {
	return ինքնուրույն.հիշողությունՉափս
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) GetbitmaspՉափս() uint32 {
	return ինքնուրույն.հիշողությունՉափս / ԱրգելափակելՉափս / Արգելափակելperbyte
}

func (ինքնուրույն *PhysicalՀիշողությունmanager) FirstԱզատ() uint32 {
	for i := uint32(0); i < ինքնուրույն.ԸնդհանուրԱրգելափակել(); i++ {
		if ինքնուրույն.հիշողությունԶանգված[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (հիշողությունԶանգված[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) FirstԱզատՉափս(չափս uint32) uint32 {
	if չափս == 0 {
		return 0xffffffff
	}
	if չափս == 1 {
		return ինքնուրույն.FirstԱզատ()
	}

	for i := uint32(0); i < ինքնուրույն.ԸնդհանուրԱրգելափակել(); i++ {
		if ինքնուրույն.հիշողությունԶանգված[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if ինքնուրույն.հիշողությունԶանգված[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var ազատ uint32 = 0
					for count := uint32(0); count <= չափս; count++ {
						if ինքնուրույն.Թեստbit(startingbit+count) == 0 {
							ազատ++
						}

						if ազատ == չափս {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (ինքնուրույն *PhysicalՀիշողությունmanager) Init(չափս uint32, bitmap []uint32) {
	ինքնուրույն.հիշողությունՉափս = չափս
	ինքնուրույն.հիշողությունԶանգված = bitmap
	ինքնուրույն.առավելագույնԱրգելափակել = չափս / ԱրգելափակելՉափս
	ինքնուրույն.օգտագործվածԱրգելափակել = ինքնուրույն.առավելագույնԱրգելափակել
	հիշողությունoper.Memset(uintptr(Pointer(&ինքնուրույն.հիշողությունԶանգված)), 0xFF, ինքնուրույն.օգտագործվածԱրգելափակել/Արգելափակելperbyte)
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) AllocateԱրգելափակել() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) ԷջՄոտարկումՎերև(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (ինքնուրույն *PhysicalՀիշողությունmanager) ԷջՄոտարկումՆերքև(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
