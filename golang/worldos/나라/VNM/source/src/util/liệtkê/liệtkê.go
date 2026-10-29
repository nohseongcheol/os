/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package liệtkê

import . "unsafe"
import . "console"
import mem "bộnhớmanager"

type TNút_danh_sách struct {
	tham_chiếu_địa_chỉ		uintptr
	previous	*TNút_danh_sách
	kế		*TNút_danh_sách
}

type Linkedliệtkê struct {
	head	*TNút_danh_sách
	tail	*TNút_danh_sách
	Cỡ_2	int

	mem	*mem.TBộnhớmanager
}

func (mình *Linkedliệtkê) Init(mem *mem.TBộnhớmanager) {
	mình.head = nil
	mình.tail = nil
	mình.Cỡ_2 = 0

	mình.mem = mem
}
func (mình *Linkedliệtkê) Thêm_vào_đầu_danh_sách(tham_chiếu_địa_chỉ uintptr) {
	mớinode := (*TNút_danh_sách)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(TNút_danh_sách{}))))
	if mớinode == nil {
		return
	}
	mớinode.tham_chiếu_địa_chỉ = tham_chiếu_địa_chỉ
	mớinode.previous = nil
	mớinode.kế = mình.head
	if mình.head != nil {
		mình.head.previous = mớinode
	}
	mình.head = mớinode
	mình.Cỡ_2++

	if mình.head.kế == nil {
		mình.tail = mình.head
	}

}
func (mình *Linkedliệtkê) Thêm_vào_cuối_danh_sách(tham_chiếu_địa_chỉ uintptr) {
	if mình.Cỡ_2 == 0 {
		mình.Thêm_vào_đầu_danh_sách(tham_chiếu_địa_chỉ)
	} else {
		mớinode := (*TNút_danh_sách)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(TNút_danh_sách{}))))
		if mớinode == nil {
			return
		}
		mớinode.tham_chiếu_địa_chỉ = tham_chiếu_địa_chỉ
		mớinode.previous = mình.tail
		mớinode.kế = nil
		mình.tail.kế = mớinode
		mình.tail = mớinode
		mình.Cỡ_2++
	}
}
func (mình *Linkedliệtkê) Chèn_tại_chỉ_số(chỉmục int, tham_chiếu_địa_chỉ uintptr) {
	if chỉmục == 0 {
		mình.Thêm_vào_đầu_danh_sách(tham_chiếu_địa_chỉ)
	} else {
		previousnode := mình.Getnodeat(chỉmục - 1)
		kếnode := previousnode.kế
		mớinode := (*TNút_danh_sách)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(TNút_danh_sách{}))))
		if mớinode == nil {
			return
		}
		mớinode.tham_chiếu_địa_chỉ = tham_chiếu_địa_chỉ

		previousnode.kế = mớinode
		mớinode.previous = previousnode
		mớinode.kế = kếnode
		if kếnode != nil {
			kếnode.previous = mớinode
		}

		mình.Cỡ_2++

		if mớinode.kế == nil {
			mình.tail = mớinode
		}
	}
}
func (mình *Linkedliệtkê) Getnodeat(chỉmục int) *TNút_danh_sách {
	if chỉmục < 0 || chỉmục >= mình.Cỡ_2 {
		return nil
	}
	var x *TNút_danh_sách = mình.head
	for i := 0; i < chỉmục; i++ {
		x = x.kế
	}
	return x
}

func (mình *Linkedliệtkê) Đặtnodeat(chỉmục int, tham_chiếu_địa_chỉ uintptr) {
	var x *TNút_danh_sách = mình.head
	for i := 0; i < chỉmục; i++ {
		x = x.kế
	}
	if x != nil {
		x.tham_chiếu_địa_chỉ = tham_chiếu_địa_chỉ
	}
}
func (mình *Linkedliệtkê) Getat(chỉmục int) Pointer {
	nút_danh_sách := mình.Getnodeat(chỉmục)
	if nút_danh_sách == nil {
		return nil
	}
	var tham_chiếu_địa_chỉ uintptr = nút_danh_sách.tham_chiếu_địa_chỉ
	return Pointer(tham_chiếu_địa_chỉ)
}
func (mình *Linkedliệtkê) Chỉmụctrên(tham_chiếu_địa_chỉ uintptr) int {
	var n *TNút_danh_sách = mình.head
	i := 0
	for ; i < mình.Cỡ_2; i++ {
		if tham_chiếu_địa_chỉ == n.tham_chiếu_địa_chỉ {
			return i
		}
		n = n.kế
	}
	return -1
}
func (mình *Linkedliệtkê) Bỏ(tham_chiếu_địa_chỉ uintptr) {
	chỉmục := mình.Chỉmụctrên(tham_chiếu_địa_chỉ)
	if chỉmục < 0 {
		return
	}
	mình.Bỏat(chỉmục)
}
func (mình *Linkedliệtkê) Bỏat(chỉmục int) {
	if chỉmục < 0 || chỉmục >= mình.Cỡ_2 {
		return
	}
	nút_danh_sách := mình.Getnodeat(chỉmục)
	if nút_danh_sách == nil {
		return
	}
	if nút_danh_sách.previous != nil {
		nút_danh_sách.previous.kế = nút_danh_sách.kế
	} else {
		mình.head = nút_danh_sách.kế
	}
	if nút_danh_sách.kế != nil {
		nút_danh_sách.kế.previous = nút_danh_sách.previous
	} else {
		mình.tail = nút_danh_sách.previous
	}
	mình.Cỡ_2 = mình.Cỡ_2 - 1

	if mình.mem != nil {
		mình.mem.Rảnh(Pointer(nút_danh_sách))
	}
}

var console_2 = TConsole{}

func (mình *Linkedliệtkê) In() {
	console_2.MInxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32In(uint32(uintptr(Pointer(mình))))
	for i := 0; i < mình.Cỡ_2; i++ {
		nút_danh_sách := (*TNút_danh_sách)(mình.Getat(i))
		console_2.MUnsignedinteger32In(uint32(nút_danh_sách.tham_chiếu_địa_chỉ))
		console_2.MIn(":")
	}
}
