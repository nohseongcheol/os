/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMemori

import (
	. "umum"
	. "unsafe"
)

const (
	BlokUkuran	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootMemorimap struct {
	ukuran			uint32
	baseaddressRendah	uint64
	baseaddressTinggi	uint64
	panjangRendah		uint64
	panjangTinggi		uint64
	Tipe			uint32
}

func PhymemTes() {
}

var memorioper Memorioper = Memorioper{}

type PhysicalMemorimanager struct {
	memoriUkuran	uint32
	dipakaiBlok	uint32
	maksimalBlok	uint32
	memoriJajaran	[]uint32
}

var (
	maksimalBlok		uint32	= 0
	memoriJajaran		[]uint32
	grubmultibootMemorimapt	multibootMemorimap
)

func (dirisendiri *PhysicalMemorimanager) Aturbit(bit uint32) uint32 {
	dirisendiri.memoriJajaran[bit/32] = dirisendiri.memoriJajaran[bit/32] | (1 << (bit % 32))
	return dirisendiri.memoriJajaran[bit/32]
}
func (dirisendiri *PhysicalMemorimanager) Balik_bit_alokasi(bit uint32) uint32 {
	dirisendiri.memoriJajaran[bit/32] = dirisendiri.memoriJajaran[bit/32] ^ (1 << (bit % 32))
	return dirisendiri.memoriJajaran[bit/32]
}
func (dirisendiri *PhysicalMemorimanager) Tesbit(bit uint32) uint32 {
	ret := dirisendiri.memoriJajaran[bit/32] & (1 << (bit % 32))
	return ret
}
func (dirisendiri *PhysicalMemorimanager) TotalBlok() uint32 {
	return dirisendiri.maksimalBlok
}
func (dirisendiri *PhysicalMemorimanager) DipakaiBlok() uint32 {
	return dirisendiri.dipakaiBlok
}
func (dirisendiri *PhysicalMemorimanager) JumlahdariMemori() uint32 {
	return dirisendiri.memoriUkuran
}
func (dirisendiri *PhysicalMemorimanager) GetbitmaspUkuran() uint32 {
	return dirisendiri.memoriUkuran / BlokUkuran / Blokperbyte
}

func (dirisendiri *PhysicalMemorimanager) FirstBebas() uint32 {
	for i := uint32(0); i < dirisendiri.TotalBlok(); i++ {
		if dirisendiri.memoriJajaran[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memoriJajaran[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (dirisendiri *PhysicalMemorimanager) FirstBebasUkuran(ukuran uint32) uint32 {
	if ukuran == 0 {
		return 0xffffffff
	}
	if ukuran == 1 {
		return dirisendiri.FirstBebas()
	}

	for i := uint32(0); i < dirisendiri.TotalBlok(); i++ {
		if dirisendiri.memoriJajaran[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if dirisendiri.memoriJajaran[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var bebas uint32 = 0
					for count := uint32(0); count <= ukuran; count++ {
						if dirisendiri.Tesbit(startingbit+count) == 0 {
							bebas++
						}

						if bebas == ukuran {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (dirisendiri *PhysicalMemorimanager) Init(ukuran uint32, peta_alokasi []uint32) {
	dirisendiri.memoriUkuran = ukuran
	dirisendiri.memoriJajaran = peta_alokasi
	dirisendiri.maksimalBlok = ukuran / BlokUkuran
	dirisendiri.dipakaiBlok = dirisendiri.maksimalBlok
	memorioper.MemAtur(uintptr(Pointer(&dirisendiri.memoriJajaran)), 0xFF, dirisendiri.dipakaiBlok/Blokperbyte)
}
func (dirisendiri *PhysicalMemorimanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (dirisendiri *PhysicalMemorimanager) HalamanPembulatanNaik(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (dirisendiri *PhysicalMemorimanager) HalamanPembulatanBawah(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
