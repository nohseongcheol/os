package physicalBộnhớ

import (
	. "chung"
	. "unsafe"
)

const (
	TắcnghẽnCỡ	uint32	= 4 * 1024
	Tắcnghẽnperbyte	uint32	= 8
)

type multibootBộnhớmap struct {
	cỡ		uint32
	baseaddressThấp	uint64
	baseaddressCao	uint64
	độdàiThấp	uint64
	độdàiCao	uint64
	Kiểu		uint32
}

func PhymemThử() {
}

var bộnhớoper Bộnhớoper = Bộnhớoper{}

type PhysicalBộnhớmanager struct {
	bộnhớCỡ		uint32
	dùngTắcnghẽn	uint32
	tốiđaTắcnghẽn	uint32
	bộnhớMảng	[]uint32
}

var (
	tốiđaTắcnghẽn		uint32	= 0
	bộnhớMảng		[]uint32
	grubmultibootBộnhớmapt	multibootBộnhớmap
)

func (mình *PhysicalBộnhớmanager) Đặtbit(bit uint32) uint32 {
	mình.bộnhớMảng[bit/32] = mình.bộnhớMảng[bit/32] | (1 << (bit % 32))
	return mình.bộnhớMảng[bit/32]
}
func (mình *PhysicalBộnhớmanager) Đảo_bit_cấp_phát(bit uint32) uint32 {
	mình.bộnhớMảng[bit/32] = mình.bộnhớMảng[bit/32] ^ (1 << (bit % 32))
	return mình.bộnhớMảng[bit/32]
}
func (mình *PhysicalBộnhớmanager) Thửbit(bit uint32) uint32 {
	ret := mình.bộnhớMảng[bit/32] & (1 << (bit % 32))
	return ret
}
func (mình *PhysicalBộnhớmanager) TổngTắcnghẽn() uint32 {
	return mình.tốiđaTắcnghẽn
}
func (mình *PhysicalBộnhớmanager) DùngTắcnghẽn() uint32 {
	return mình.dùngTắcnghẽn
}
func (mình *PhysicalBộnhớmanager) SốtiềntrênBộnhớ() uint32 {
	return mình.bộnhớCỡ
}
func (mình *PhysicalBộnhớmanager) GetbitmaspCỡ() uint32 {
	return mình.bộnhớCỡ / TắcnghẽnCỡ / Tắcnghẽnperbyte
}

func (mình *PhysicalBộnhớmanager) ĐầuRảnh() uint32 {
	for i := uint32(0); i < mình.TổngTắcnghẽn(); i++ {
		if mình.bộnhớMảng[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (bộnhớMảng[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (mình *PhysicalBộnhớmanager) ĐầuRảnhCỡ(cỡ uint32) uint32 {
	if cỡ == 0 {
		return 0xffffffff
	}
	if cỡ == 1 {
		return mình.ĐầuRảnh()
	}

	for i := uint32(0); i < mình.TổngTắcnghẽn(); i++ {
		if mình.bộnhớMảng[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if mình.bộnhớMảng[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var rảnh uint32 = 0
					for sốlượng := uint32(0); sốlượng <= cỡ; sốlượng++ {
						if mình.Thửbit(startingbit+sốlượng) == 0 {
							rảnh++
						}

						if rảnh == cỡ {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (mình *PhysicalBộnhớmanager) Init(cỡ uint32, bản_đồ_cấp_phát []uint32) {
	mình.bộnhớCỡ = cỡ
	mình.bộnhớMảng = bản_đồ_cấp_phát
	mình.tốiđaTắcnghẽn = cỡ / TắcnghẽnCỡ
	mình.dùngTắcnghẽn = mình.tốiđaTắcnghẽn
	bộnhớoper.MemĐặt(uintptr(Pointer(&mình.bộnhớMảng)), 0xFF, mình.dùngTắcnghẽn/Tắcnghẽnperbyte)
}
func (mình *PhysicalBộnhớmanager) AllocateTắcnghẽn() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (mình *PhysicalBộnhớmanager) TrangLàmtrònLên(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (mình *PhysicalBộnhớmanager) TrangLàmtròndown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
