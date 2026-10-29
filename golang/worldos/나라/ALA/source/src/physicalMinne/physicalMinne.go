/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMinne

import (
	. "gemensam"
	. "unsafe"
)

const (
	BlockStorlek	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootMinnemap struct {
	storlek		uint32
	baseAdressLåg	uint64
	baseAdressHög	uint64
	längdLåg	uint64
	längdHög	uint64
	Typ		uint32
}

func PhymemTesta() {
}

var minneoper Minneoper = Minneoper{}

type PhysicalMinnemanager struct {
	minneStorlek	uint32
	använtblock	uint32
	maximaltblock	uint32
	minneVektor	[]uint32
}

var (
	maximaltblock		uint32	= 0
	minneVektor		[]uint32
	grubmultibootMinnemapt	multibootMinnemap
)

func (själv *PhysicalMinnemanager) Mängdbit(bit uint32) uint32 {
	själv.minneVektor[bit/32] = själv.minneVektor[bit/32] | (1 << (bit % 32))
	return själv.minneVektor[bit/32]
}
func (själv *PhysicalMinnemanager) Invertera_tilldelningsbit(bit uint32) uint32 {
	själv.minneVektor[bit/32] = själv.minneVektor[bit/32] ^ (1 << (bit % 32))
	return själv.minneVektor[bit/32]
}
func (själv *PhysicalMinnemanager) Testabit(bit uint32) uint32 {
	ret := själv.minneVektor[bit/32] & (1 << (bit % 32))
	return ret
}
func (själv *PhysicalMinnemanager) Totaltblock() uint32 {
	return själv.maximaltblock
}
func (själv *PhysicalMinnemanager) Använtblock() uint32 {
	return själv.använtblock
}
func (själv *PhysicalMinnemanager) MängdavMinne() uint32 {
	return själv.minneStorlek
}
func (själv *PhysicalMinnemanager) GetbitmaspStorlek() uint32 {
	return själv.minneStorlek / BlockStorlek / Blockperbyte
}

func (själv *PhysicalMinnemanager) FirstLedigt() uint32 {
	for i := uint32(0); i < själv.Totaltblock(); i++ {
		if själv.minneVektor[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (minneVektor[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (själv *PhysicalMinnemanager) FirstLedigtStorlek(storlek uint32) uint32 {
	if storlek == 0 {
		return 0xffffffff
	}
	if storlek == 1 {
		return själv.FirstLedigt()
	}

	for i := uint32(0); i < själv.Totaltblock(); i++ {
		if själv.minneVektor[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if själv.minneVektor[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var ledigt uint32 = 0
					for antal := uint32(0); antal <= storlek; antal++ {
						if själv.Testabit(startingbit+antal) == 0 {
							ledigt++
						}

						if ledigt == storlek {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (själv *PhysicalMinnemanager) Init(storlek uint32, tilldelningskarta []uint32) {
	själv.minneStorlek = storlek
	själv.minneVektor = tilldelningskarta
	själv.maximaltblock = storlek / BlockStorlek
	själv.använtblock = själv.maximaltblock
	minneoper.Memmängd(uintptr(Pointer(&själv.minneVektor)), 0xFF, själv.använtblock/Blockperbyte)
}
func (själv *PhysicalMinnemanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (själv *PhysicalMinnemanager) SidaAvrundaUpp(adress_2 uint32) uint32 {
	if (adress_2 & 0xFFFFF000) != adress_2 {
		adress_2 = adress_2 & 0xFFFFF000
		adress_2 = adress_2 + 0x1000
	}
	return adress_2
}
func (själv *PhysicalMinnemanager) SidaAvrundaNer(adress_2 uint32) uint32 {
	return adress_2 & 0xFFFFF000
}
