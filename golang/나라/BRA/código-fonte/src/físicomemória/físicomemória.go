/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package físicomemória

import (
	. "comum"
	. "unsafe"
)

const (
	BlocoTamanho	uint32	= 4 * 1024
	Blocoperocteto	uint32	= 8
)

type multibootmemóriamapa struct {
	tamanho			uint32
	baseEndereçoBaixo	uint64
	baseEndereçoAlto	uint64
	duraçãoBaixo		uint64
	duraçãoAlto		uint64
	Tipo			uint32
}

func PhymemTestar() {
}

var memóriaoper Memóriaoper = Memóriaoper{}

type Físicomemóriagestor struct {
	memóriaTamanho	uint32
	utilizadoBloco	uint32
	máximoBloco	uint32
	memóriamatriz	[]uint32
}

var (
	máximoBloco			uint32	= 0
	memóriamatriz			[]uint32
	grubmultibootmemóriamapat	multibootmemóriamapa
)

func (próprio *Físicomemóriagestor) Conjuntobit(bit uint32) uint32 {
	próprio.memóriamatriz[bit/32] = próprio.memóriamatriz[bit/32] | (1 << (bit % 32))
	return próprio.memóriamatriz[bit/32]
}
func (próprio *Físicomemóriagestor) Inverter_o_bit_de_alocação(bit uint32) uint32 {
	próprio.memóriamatriz[bit/32] = próprio.memóriamatriz[bit/32] ^ (1 << (bit % 32))
	return próprio.memóriamatriz[bit/32]
}
func (próprio *Físicomemóriagestor) Testarbit(bit uint32) uint32 {
	ret := próprio.memóriamatriz[bit/32] & (1 << (bit % 32))
	return ret
}
func (próprio *Físicomemóriagestor) TotalBloco() uint32 {
	return próprio.máximoBloco
}
func (próprio *Físicomemóriagestor) UtilizadoBloco() uint32 {
	return próprio.utilizadoBloco
}
func (próprio *Físicomemóriagestor) Montantedememória() uint32 {
	return próprio.memóriaTamanho
}
func (próprio *Físicomemóriagestor) GetbitmaspTamanho() uint32 {
	return próprio.memóriaTamanho / BlocoTamanho / Blocoperocteto
}

func (próprio *Físicomemóriagestor) FirstLivre() uint32 {
	for i := uint32(0); i < próprio.TotalBloco(); i++ {
		if próprio.memóriamatriz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memóriamatriz[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (próprio *Físicomemóriagestor) FirstLivreTamanho(tamanho uint32) uint32 {
	if tamanho == 0 {
		return 0xffffffff
	}
	if tamanho == 1 {
		return próprio.FirstLivre()
	}

	for i := uint32(0); i < próprio.TotalBloco(); i++ {
		if próprio.memóriamatriz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if próprio.memóriamatriz[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var livre uint32 = 0
					for contar := uint32(0); contar <= tamanho; contar++ {
						if próprio.Testarbit(startingbit+contar) == 0 {
							livre++
						}

						if livre == tamanho {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (próprio *Físicomemóriagestor) Init(tamanho uint32, mapa_de_alocação []uint32) {
	próprio.memóriaTamanho = tamanho
	próprio.memóriamatriz = mapa_de_alocação
	próprio.máximoBloco = tamanho / BlocoTamanho
	próprio.utilizadoBloco = próprio.máximoBloco
	memóriaoper.Memconjunto(uintptr(Pointer(&próprio.memóriamatriz)), 0xFF, próprio.utilizadoBloco/Blocoperocteto)
}
func (próprio *Físicomemóriagestor) AllocateBloco() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (próprio *Físicomemóriagestor) PáginaArredondarParacima(endereço_2 uint32) uint32 {
	if (endereço_2 & 0xFFFFF000) != endereço_2 {
		endereço_2 = endereço_2 & 0xFFFFF000
		endereço_2 = endereço_2 + 0x1000
	}
	return endereço_2
}
func (próprio *Físicomemóriagestor) PáginaArredondarAbaixo(endereço_2 uint32) uint32 {
	return endereço_2 & 0xFFFFF000
}
