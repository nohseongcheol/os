/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package định_dạng_thực_thi_và_liên_kết

import . "unsafe"
import . "console"

import mem "bộnhớmanager"

type Liênkết struct {
	Năngđộng	uintptr
	Previous	*Liênkết
	Kế		*Liênkết
}
type Liênkếtmap struct {
	Đầu	*Liênkết
	Cuối	*Liênkết

	Cỡ_2	int

	mem	*mem.TBộnhớmanager
}

func (mình *Liênkếtmap) Init(mem *mem.TBộnhớmanager) {
	mình.mem = mem
}
func (mình *Liênkếtmap) Clone() Liênkếtmap {
	var liênkếtmap Liênkếtmap

	liênkếtmap.Init(mình.mem)

	Liênkết := mình.Đầu

	for ; Liênkết != nil; Liênkết = Liênkết.Kế {
		liênkếtmap.Thêm_vào_cuối_danh_sách(Liênkết.Năngđộng)
	}
	return liênkếtmap
}
func (mình *Liênkếtmap) Thêm_vào_đầu_danh_sách(Năngđộng uintptr) {
	mớiLiênkết := (*Liênkết)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(Liênkết{}))))
	mớiLiênkết.Năngđộng = Năngđộng
	mớiLiênkết.Kế = mình.Đầu
	mình.Đầu = mớiLiênkết
	mình.Cỡ_2++

	if mình.Đầu.Kế == nil {
		mình.Cuối = mình.Đầu
	}
}
func (mình *Liênkếtmap) Thêm_vào_cuối_danh_sách(Năngđộng uintptr) {
	if Năngđộng == 0 {
		return
	}

	if mình.Cỡ_2 == 0 {
		mình.Thêm_vào_đầu_danh_sách(Năngđộng)
	} else {
		mớiLiênkết := (*Liênkết)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(Liênkết{}))))
		mớiLiênkết.Năngđộng = Năngđộng
		mớiLiênkết.Kế = nil
		mình.Cuối.Kế = mớiLiênkết
		mình.Cuối = mớiLiênkết
		mình.Cỡ_2++
	}
}
func (mình *Liênkếtmap) In(x uint16, y uint16) {
	Liênkết := mình.Đầu
	console_2 := TConsole{}
	console_2.MInxy("linkmap : ", x, y)
	for ; Liênkết != nil; Liênkết = Liênkết.Kế {
		console_2.MUnsignedinteger32In(uint32(Liênkết.Năngđộng))
		console_2.MIn("+")

	}
}
