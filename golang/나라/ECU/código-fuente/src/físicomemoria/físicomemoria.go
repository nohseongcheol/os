package físicomemoria

import (
	. "común"
	. "unsafe"
)

const (
	BloqueTamaño	uint32	= 4 * 1024
	Bloqueperocteto	uint32	= 8
)

type multibootmemoriamapa struct {
	tamaño			uint32
	baseDirecciónBaja	uint64
	baseDirecciónAlta	uint64
	duraciónBaja		uint64
	duraciónAlta		uint64
	Tipo			uint32
}

func PhymemProbar() {
}

var memoriaoper Memoriaoper = Memoriaoper{}

type Físicomemoriagestor struct {
	memoriaTamaño	uint32
	enusoBloque	uint32
	máximoBloque	uint32
	memoriamatriz	[]uint32
}

var (
	máximoBloque			uint32	= 0
	memoriamatriz			[]uint32
	grubmultibootmemoriamapat	multibootmemoriamapa
)

func (propio *Físicomemoriagestor) Establecerbit(bit uint32) uint32 {
	propio.memoriamatriz[bit/32] = propio.memoriamatriz[bit/32] | (1 << (bit % 32))
	return propio.memoriamatriz[bit/32]
}
func (propio *Físicomemoriagestor) Invertir_el_bit_de_asignación(bit uint32) uint32 {
	propio.memoriamatriz[bit/32] = propio.memoriamatriz[bit/32] ^ (1 << (bit % 32))
	return propio.memoriamatriz[bit/32]
}
func (propio *Físicomemoriagestor) Probarbit(bit uint32) uint32 {
	ret := propio.memoriamatriz[bit/32] & (1 << (bit % 32))
	return ret
}
func (propio *Físicomemoriagestor) TotalBloque() uint32 {
	return propio.máximoBloque
}
func (propio *Físicomemoriagestor) EnusoBloque() uint32 {
	return propio.enusoBloque
}
func (propio *Físicomemoriagestor) Cantidaddememoria() uint32 {
	return propio.memoriaTamaño
}
func (propio *Físicomemoriagestor) GetbitmaspTamaño() uint32 {
	return propio.memoriaTamaño / BloqueTamaño / Bloqueperocteto
}

func (propio *Físicomemoriagestor) FirstLibre() uint32 {
	for i := uint32(0); i < propio.TotalBloque(); i++ {
		if propio.memoriamatriz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memoriamatriz[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (propio *Físicomemoriagestor) FirstLibreTamaño(tamaño uint32) uint32 {
	if tamaño == 0 {
		return 0xffffffff
	}
	if tamaño == 1 {
		return propio.FirstLibre()
	}

	for i := uint32(0); i < propio.TotalBloque(); i++ {
		if propio.memoriamatriz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if propio.memoriamatriz[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var libre uint32 = 0
					for recuento := uint32(0); recuento <= tamaño; recuento++ {
						if propio.Probarbit(startingbit+recuento) == 0 {
							libre++
						}

						if libre == tamaño {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (propio *Físicomemoriagestor) Init(tamaño uint32, mapa_de_asignación []uint32) {
	propio.memoriaTamaño = tamaño
	propio.memoriamatriz = mapa_de_asignación
	propio.máximoBloque = tamaño / BloqueTamaño
	propio.enusoBloque = propio.máximoBloque
	memoriaoper.Memestablecer(uintptr(Pointer(&propio.memoriamatriz)), 0xFF, propio.enusoBloque/Bloqueperocteto)
}
func (propio *Físicomemoriagestor) AllocateBloque() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (propio *Físicomemoriagestor) PáginaRedondearSubir(dirección_2 uint32) uint32 {
	if (dirección_2 & 0xFFFFF000) != dirección_2 {
		dirección_2 = dirección_2 & 0xFFFFF000
		dirección_2 = dirección_2 + 0x1000
	}
	return dirección_2
}
func (propio *Físicomemoriagestor) PáginaRedondearAbajo(dirección_2 uint32) uint32 {
	return dirección_2 & 0xFFFFF000
}
