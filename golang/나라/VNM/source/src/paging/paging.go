/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "giánđoạn"
import . "bộnhớmanager"
import . "util"

type TrangThưmụcentry_2 uintptr

const (
	TrangCó		uint32	= 0x001
	Trangwritable	uint32	= 0x002
	TrangNgườidùng	uint32	= 0x004
	Trangframe	uint32	= 0xFFFFF000
	Trangcow	uint32	= 0x200
)

func Đặtbyteataddress(x byte, address uint32)
func Đặtunsignedinteger8ataddress(x uint8, address uint32)
func Đặtunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func đặtcr3(thư_mục_trang uint32)
func getcr3() uint32

type Paging struct {
	TGiánđoạnhandler
}
type Tcowframemanager struct {
	mem		*TBộnhớmanager
	refs		[]uint16
	frameSốlượng	uint32
}

var (
	TrangThưmụcentry	uintptr
	TrangBảngentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (mình *Tcowframemanager) Init(mem *TBộnhớmanager, frameSốlượng uint32) bool {
	mình.mem = mem
	mình.frameSốlượng = frameSốlượng
	referenceByte := frameSốlượng * uint32(unsafe.Sizeof(uint16(0)))
	referenceContrỏ := mem.Cấp_phát_bộ_nhớ(referenceByte)
	if referenceContrỏ == nil {
		mình.refs = nil
		mình.frameSốlượng = 0
		return false
	}
	mình.refs = (*[1 << 28]uint16)(referenceContrỏ)[:frameSốlượng:frameSốlượng]
	for i := uint32(0); i < frameSốlượng; i++ {
		mình.refs[i] = 0
	}
	return true
}

func (mình *Tcowframemanager) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= mình.frameSốlượng || mình.refs == nil {
		return 0
	}
	return mình.refs[idx]
}

func (mình *Tcowframemanager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= mình.frameSốlượng || mình.refs == nil {
		return
	}
	if mình.refs[idx] == 0 {
		mình.refs[idx] = 2
	} else {
		mình.refs[idx]++
	}
}

func (mình *Tcowframemanager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= mình.frameSốlượng || mình.refs == nil || mình.refs[idx] == 0 {
		return
	}
	mình.refs[idx]--
}

func (mình *Paging) Init(trangThưmụcentry uintptr, trangBảngentry uint32, bộnhớmanager *TBộnhớmanager) {

	TrangThưmụcentry = trangThưmụcentry
	TrangBảngentry = trangBảngentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(bộnhớmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressContrỏ, _ := bộnhớmanager.Alignedmalloc(0x1000)
			if addressContrỏ == nil {
				return
			}
			address := uint32(uintptr(addressContrỏ))

			Đặtunsignedinteger32ataddress(address|0x87, uint32(trangThưmụcentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Đặtunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		trangThưmụcentry = trangThưmụcentry + 0x1000
	}

}
func (mình *Paging) SharedBộnhớregion() {

	trangThưmụcentry := TrangThưmụcentry
	kTrangThưmụcentry := TrangThưmụcentry

	for i := uint32(1); i <= virtlen; i++ {

		trangThưmụcentry = trangThưmụcentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetGiátrị(uint32(kTrangThưmụcentry) + pde*4)
			v = (v & 0xFFFFF000)
			Đặtunsignedinteger32ataddress(v|0x87, uint32(trangThưmụcentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetGiátrị(uint32(kTrangThưmụcentry) + pde*4)
			v = (v & 0xFFFFF000)
			Đặtunsignedinteger32ataddress(v|0x87, uint32(trangThưmụcentry)+pde*4)

		}

	}
}
func (mình *Paging) Trangfault(manager *TGiánđoạnmanager) {
	giánđoạnhandler = handlepagingGiánđoạn

	var address uintptr
	address = uintptr(unsafe.Pointer(&giánđoạnhandler))
	mình.TGiánđoạnhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var giánđoạnhandler func(uint32) uint32

func handlepagingGiánđoạn(esp uint32) uint32 {
	if ResolveSaochépBậtGhifault() {
		return esp
	}
	return HandlefatalGiánđoạnframe(esp, 0x0E)
}

func Cloneaddressspacecow(mãnguồnTrangThưmục uint32) uint32 {
	if HoạtđộngBộnhớmanager == nil || mãnguồnTrangThưmục == 0 {
		return 0
	}
	destinationContrỏ, _ := HoạtđộngBộnhớmanager.Alignedmalloc(0x1000)
	if destinationContrỏ == nil {
		return 0
	}
	destinationTrangThưmục := uint32(uintptr(destinationContrỏ))
	for i := uint32(0); i < 1024; i++ {
		Đặtunsignedinteger32ataddress(0, destinationTrangThưmục+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		mãnguồnpdeaddress := mãnguồnTrangThưmục + pde*4
		mãnguồnpde := GetGiátrị(mãnguồnpdeaddress)
		if (mãnguồnpde & TrangCó) == 0 {
			continue
		}
		if issharedpde(pde) {
			Đặtunsignedinteger32ataddress(mãnguồnpde, destinationTrangThưmục+pde*4)
			continue
		}

		destinationptContrỏ, _ := HoạtđộngBộnhớmanager.Alignedmalloc(0x1000)
		if destinationptContrỏ == nil {
			continue
		}
		mãnguồnpt := mãnguồnpde & Trangframe
		destinationpt := uint32(uintptr(destinationptContrỏ))
		Đặtunsignedinteger32ataddress((destinationpt | (mãnguồnpde & 0xFFF)), destinationTrangThưmục+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := mãnguồnpt + pte*4
			entry := GetGiátrị(pteaddress)
			if (entry & TrangCó) != 0 {
				if (entry & Trangwritable) != 0 {
					entry = (entry &^ Trangwritable) | Trangcow
					Đặtunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Trangframe)
				} else if (entry & Trangcow) != 0 {
					cowframemanager.Increment(entry & Trangframe)
				}
			}
			Đặtunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	nạplạicr3()
	return destinationTrangThưmục
}

func ResolveSaochépBậtGhifault() bool {
	if HoạtđộngBộnhớmanager == nil {
		return false
	}
	faultaddress := getcr2()
	thư_mục_trang := getcr3()
	pdeaddress := thư_mục_trang + ((faultaddress>>22)&0x3FF)*4
	pde := GetGiátrị(pdeaddress)
	if (pde & TrangCó) == 0 {
		return false
	}
	pt := pde & Trangframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetGiátrị(pteaddress)
	if (pte&Trangcow) == 0 || (pte&TrangCó) == 0 {
		return false
	}
	oldframe := pte & Trangframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Đặtunsignedinteger32ataddress((pte|Trangwritable)&^Trangcow, pteaddress)
		nạplạicr3()
		return true
	}

	mớiContrỏ, _ := HoạtđộngBộnhớmanager.Alignedmalloc(0x1000)
	if mớiContrỏ == nil {
		return false
	}
	mớiframe := uint32(uintptr(mớiContrỏ)) & Trangframe

	mãnguồn_2 := GetBytefromContrỏ(uintptr(faultaddress&Trangframe), 0x1000, 0x1000)
	destination_2 := GetBytefromContrỏ(uintptr(mớiframe), 0x1000, 0x1000)
	copy(destination_2, mãnguồn_2)
	cowframemanager.Decrement(oldframe)
	Đặtunsignedinteger32ataddress((mớiframe|(pte&0xFFF)|Trangwritable)&^Trangcow, pteaddress)
	nạplạicr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func nạplạicr3() {
	cr3 := getcr3()
	đặtcr3(cr3)
}

func ĐặtbyteVàoTrangThưmục(x byte, address uint32, thư_mục_trang uint32) {
	oldcr3 := getcr3()
	đặtcr3(thư_mục_trang)
	Đặtbyteataddress(x, address)
	đặtcr3(oldcr3)
}

func ĐặtTắcnghẽnVàoTrangThưmục(mãnguồn_2 []byte, destination_2 []byte, cỡ uint32, thư_mục_trang uint32) {
	if cỡ == 0 || thư_mục_trang == 0 {
		return
	}
	oldcr3 := getcr3()
	đặtcr3(thư_mục_trang)
	makePhạmviRiêngwritableHiệnhành(thư_mục_trang, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), cỡ)

	for i := uint32(0); i < cỡ; i++ {
		destination_2[i] = mãnguồn_2[i]
	}
	đặtcr3(oldcr3)
}

func ZeroTắcnghẽnVàoTrangThưmục(address uint32, cỡ uint32, thư_mục_trang uint32) {
	if cỡ == 0 || thư_mục_trang == 0 {
		return
	}
	oldcr3 := getcr3()
	đặtcr3(thư_mục_trang)
	makePhạmviRiêngwritableHiệnhành(thư_mục_trang, address, cỡ)
	destination_2 := GetBytefromContrỏ(uintptr(address), int(cỡ), int(cỡ))
	for i := uint32(0); i < cỡ; i++ {
		destination_2[i] = 0
	}
	đặtcr3(oldcr3)
}

func makeTrangRiêngwritableHiệnhành(thư_mục_trang uint32, ảoaddress uint32) bool {
	pde := GetGiátrị(thư_mục_trang + ((ảoaddress>>22)&0x3FF)*4)
	if (pde & TrangCó) == 0 {
		return false
	}
	pteaddress := (pde & Trangframe) + ((ảoaddress>>12)&0x3FF)*4
	pte := GetGiátrị(pteaddress)
	if (pte & TrangCó) == 0 {
		return false
	}
	if (pte & Trangcow) == 0 {
		return (pte & Trangwritable) != 0
	}
	if HoạtđộngBộnhớmanager == nil {
		return false
	}
	mớiContrỏ, _ := HoạtđộngBộnhớmanager.Alignedmalloc(0x1000)
	if mớiContrỏ == nil {
		return false
	}
	mớiframe := uint32(uintptr(mớiContrỏ)) & Trangframe
	mãnguồn_2 := GetBytefromContrỏ(uintptr(ảoaddress&Trangframe), 0x1000, 0x1000)
	destination_2 := GetBytefromContrỏ(uintptr(mớiframe), 0x1000, 0x1000)
	copy(destination_2, mãnguồn_2)
	cowframemanager.Decrement(pte & Trangframe)
	Đặtunsignedinteger32ataddress((mớiframe|(pte&0xFFF)|Trangwritable)&^Trangcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	nạplạicr3()
	return true
}

func makePhạmviRiêngwritableHiệnhành(thư_mục_trang uint32, address uint32, cỡ uint32) bool {
	if cỡ == 0 {
		return true
	}
	cuối := address + cỡ - 1
	if cuối < address {
		return false
	}
	for trang := address & Trangframe; ; trang += 0x1000 {
		if !makeTrangRiêngwritableHiệnhành(thư_mục_trang, trang) {
			return false
		}
		if trang == (cuối & Trangframe) {
			break
		}
	}
	return true
}

func MakePhạmviRiêngwritable(thư_mục_trang uint32, address uint32, cỡ uint32) bool {
	if thư_mục_trang == 0 {
		return false
	}
	oldcr3 := getcr3()
	đặtcr3(thư_mục_trang)
	đồngý := makePhạmviRiêngwritableHiệnhành(thư_mục_trang, address, cỡ)
	đặtcr3(oldcr3)
	return đồngý
}

func Đặtunsignedinteger32VàoTrangThưmục(x uint32, address uint32, thư_mục_trang uint32) {
	if thư_mục_trang == 0 {
		return
	}
	oldcr3 := getcr3()
	đặtcr3(thư_mục_trang)
	Đặtunsignedinteger32ataddress(x, address)
	đặtcr3(oldcr3)
}

func GetGiátrị(address uint32) uint32 {
	var orgGiátrị uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgGiátrị
}
func GetGiátrịVàoTrangThưmục(address uint32, thư_mục_trang uint32) uint32 {
	if thư_mục_trang == 0 {
		return 0
	}
	oldcr3 := getcr3()
	đặtcr3(thư_mục_trang)
	v := GetGiátrị(address)
	đặtcr3(oldcr3)
	return v
}

var v uint32 = 0

func SaochépTrangframeTắcnghẽn(xTrangThưmục uint32, yTrangThưmục uint32, vaddress uint32) {
	if xTrangThưmục == 0 || yTrangThưmục == 0 {
		return
	}
	oldcr3 := getcr3()
	đặtcr3(xTrangThưmục)
	v = GetGiátrị(vaddress)
	Đặtunsignedinteger32VàoTrangThưmục(v, vaddress, yTrangThưmục)

	đặtcr3(oldcr3)
}
