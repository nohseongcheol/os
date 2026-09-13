package physicalMemoria

import (
	. "comune"
	. "unsafe"
)

const (
	BloccoDimensione	uint32	= 4 * 1024
	Bloccoperbyte		uint32	= 8
)

type multibootMemoriamap struct {
	dimensione		uint32
	baseaddressBasso	uint64
	baseaddressAlto		uint64
	durataBasso		uint64
	durataAlto		uint64
	Tipo			uint32
}

func PhymemProva() {
}

var memoriaoper Memoriaoper = Memoriaoper{}

type PhysicalMemoriamanager struct {
	memoriaDimensione	uint32
	usatoBlocco		uint32
	massimoBlocco		uint32
	memoriaSerie		[]uint32
}

var (
	massimoBlocco			uint32	= 0
	memoriaSerie			[]uint32
	grubmultibootMemoriamapt	multibootMemoriamap
)

func (séstesso *PhysicalMemoriamanager) Impostabit(bit uint32) uint32 {
	séstesso.memoriaSerie[bit/32] = séstesso.memoriaSerie[bit/32] | (1 << (bit % 32))
	return séstesso.memoriaSerie[bit/32]
}
func (séstesso *PhysicalMemoriamanager) Inverti_il_bit_di_allocazione(bit uint32) uint32 {
	séstesso.memoriaSerie[bit/32] = séstesso.memoriaSerie[bit/32] ^ (1 << (bit % 32))
	return séstesso.memoriaSerie[bit/32]
}
func (séstesso *PhysicalMemoriamanager) Provabit(bit uint32) uint32 {
	ret := séstesso.memoriaSerie[bit/32] & (1 << (bit % 32))
	return ret
}
func (séstesso *PhysicalMemoriamanager) TotaleBlocco() uint32 {
	return séstesso.massimoBlocco
}
func (séstesso *PhysicalMemoriamanager) UsatoBlocco() uint32 {
	return séstesso.usatoBlocco
}
func (séstesso *PhysicalMemoriamanager) QuantitàdiMemoria() uint32 {
	return séstesso.memoriaDimensione
}
func (séstesso *PhysicalMemoriamanager) GetbitmaspDimensione() uint32 {
	return séstesso.memoriaDimensione / BloccoDimensione / Bloccoperbyte
}

func (séstesso *PhysicalMemoriamanager) FirstLibero() uint32 {
	for i := uint32(0); i < séstesso.TotaleBlocco(); i++ {
		if séstesso.memoriaSerie[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memoriaSerie[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (séstesso *PhysicalMemoriamanager) FirstLiberoDimensione(dimensione uint32) uint32 {
	if dimensione == 0 {
		return 0xffffffff
	}
	if dimensione == 1 {
		return séstesso.FirstLibero()
	}

	for i := uint32(0); i < séstesso.TotaleBlocco(); i++ {
		if séstesso.memoriaSerie[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if séstesso.memoriaSerie[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var libero uint32 = 0
					for conteggio := uint32(0); conteggio <= dimensione; conteggio++ {
						if séstesso.Provabit(startingbit+conteggio) == 0 {
							libero++
						}

						if libero == dimensione {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (séstesso *PhysicalMemoriamanager) Init(dimensione uint32, mappa_di_allocazione []uint32) {
	séstesso.memoriaDimensione = dimensione
	séstesso.memoriaSerie = mappa_di_allocazione
	séstesso.massimoBlocco = dimensione / BloccoDimensione
	séstesso.usatoBlocco = séstesso.massimoBlocco
	memoriaoper.MemImposta(uintptr(Pointer(&séstesso.memoriaSerie)), 0xFF, séstesso.usatoBlocco/Bloccoperbyte)
}
func (séstesso *PhysicalMemoriamanager) AllocateBlocco() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (séstesso *PhysicalMemoriamanager) PAGINAArrotondaSu(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (séstesso *PhysicalMemoriamanager) PAGINAArrotondaGiù(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
