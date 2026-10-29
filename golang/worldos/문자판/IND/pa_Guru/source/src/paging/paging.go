/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "ਯਾਦਾਸ਼ਤ"
import . "util"

type PageDirectoryEntry uintptr

const (
	PAGE_PRESENT	uint32	= 0x001
	PAGE_WRITABLE	uint32	= 0x002
	PAGE_USER	uint32	= 0x004
	PAGE_FRAME	uint32	= 0xFFFFF000
	PAGE_COW		uint32	= 0x200
)

func SetByteAtAddr(x byte, addr uint32)
func SetUint8AtAddr(x uint8, addr uint32)
func SetUint32AtAddr(x uint32, addr uint32)

func getCR2() uint32

func setCR3(pageDir uint32)
func getCR3() uint32

type Paging struct {
	TInterruptHandler
}
type TCOWFrameManager struct {
	mem		*TMemoryManager
	refs		[]uint16
	frameCount	uint32
}

var (
	PageDirEntry	uintptr
	PageTableEntry		uint32
	pdelen			uint32
	virtlen			uint32
	cowFrameManager		TCOWFrameManager
)

func (self *TCOWFrameManager) Vਆਰੰਭ_ਕਰਨਾ(mem *TMemoryManager, frameCount uint32) bool {
	self.mem = mem
	self.frameCount = frameCount
	refBytes := frameCount * uint32(unsafe.Sizeof(uint16(0)))
	refPtr := mem.Malloc(refBytes)
	if refPtr == nil {
		self.refs = nil
		self.frameCount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(refPtr)[:frameCount:frameCount]
	for i := uint32(0); i < frameCount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TCOWFrameManager) Ref(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= self.frameCount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TCOWFrameManager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= self.frameCount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TCOWFrameManager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= self.frameCount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Vਆਰੰਭ_ਕਰਨਾ(pageDirEntry uintptr, pageTableEntry uint32, memoryManager *TMemoryManager) {

	PageDirEntry = pageDirEntry
	PageTableEntry = pageTableEntry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowFrameManager.Vਆਰੰਭ_ਕਰਨਾ(memoryManager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addrPtr, _ := memoryManager.AlignedMalloc(0x1000)
			if addrPtr == nil {
				return
			}
			addr := uint32(uintptr(addrPtr))

			SetUint32AtAddr(addr|0x87, uint32(pageDirEntry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				SetUint32AtAddr((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, addr+pte*4)
			}
		}
		pageDirEntry = pageDirEntry + 0x1000
	}

}
func (self *Paging) SharedMemoryRegion() {

	pageDirEntry := PageDirEntry
	kPageDirEntry := PageDirEntry

	for i := uint32(1); i <= virtlen; i++ {

		pageDirEntry = pageDirEntry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValue(uint32(kPageDirEntry) + pde*4)
			v = (v & 0xFFFFF000)
			SetUint32AtAddr(v|0x87, uint32(pageDirEntry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValue(uint32(kPageDirEntry) + pde*4)
			v = (v & 0xFFFFF000)
			SetUint32AtAddr(v|0x87, uint32(pageDirEntry)+pde*4)

		}

	}
}
func (self *Paging) PageFault(manager *TInterruptManager) {
	interruptHandler = handlePagingInterrupt

	var addr uintptr
	addr = uintptr(unsafe.Pointer(&interruptHandler))
	self.TInterruptHandler.Vਆਰੰਭ_ਕਰਨਾ(0xE, uintptr(unsafe.Pointer(manager)), addr)
}

var interruptHandler func(uint32) uint32

func handlePagingInterrupt(esp uint32) uint32 {
	if ResolveCopyOnWriteFault() {
		return esp
	}
	return HandleFatalInterruptFrame(esp, 0x0E)
}

func CloneAddressSpaceCOW(srcPageDir uint32) uint32 {
	if ActiveMemoryManager == nil || srcPageDir == 0 {
		return 0
	}
	dstPtr, _ := ActiveMemoryManager.AlignedMalloc(0x1000)
	if dstPtr == nil {
		return 0
	}
	dstPageDir := uint32(uintptr(dstPtr))
	for i := uint32(0); i < 1024; i++ {
		SetUint32AtAddr(0, dstPageDir+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		srcPdeAddr := srcPageDir + pde*4
		srcPde := GetValue(srcPdeAddr)
		if (srcPde & PAGE_PRESENT) == 0 {
			continue
		}
		if isSharedPDE(pde) {
			SetUint32AtAddr(srcPde, dstPageDir+pde*4)
			continue
		}

		dstPtPtr, _ := ActiveMemoryManager.AlignedMalloc(0x1000)
		if dstPtPtr == nil {
			continue
		}
		srcPt := srcPde & PAGE_FRAME
		dstPt := uint32(uintptr(dstPtPtr))
		SetUint32AtAddr((dstPt | (srcPde & 0xFFF)), dstPageDir+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteAddr := srcPt + pte*4
			entry := GetValue(pteAddr)
			if (entry & PAGE_PRESENT) != 0 {
				if (entry & PAGE_WRITABLE) != 0 {
					entry = (entry &^ PAGE_WRITABLE) | PAGE_COW
					SetUint32AtAddr(entry, pteAddr)
					cowFrameManager.Increment(entry & PAGE_FRAME)
				} else if (entry & PAGE_COW) != 0 {
					cowFrameManager.Increment(entry & PAGE_FRAME)
				}
			}
			SetUint32AtAddr(entry, dstPt+pte*4)
		}
	}
	reloadCR3()
	return dstPageDir
}

func ResolveCopyOnWriteFault() bool {
	if ActiveMemoryManager == nil {
		return false
	}
	faultAddr := getCR2()
	pageDir := getCR3()
	pdeAddr := pageDir + ((faultAddr>>22)&0x3FF)*4
	pde := GetValue(pdeAddr)
	if (pde & PAGE_PRESENT) == 0 {
		return false
	}
	pt := pde & PAGE_FRAME
	pteAddr := pt + ((faultAddr>>12)&0x3FF)*4
	pte := GetValue(pteAddr)
	if (pte&PAGE_COW) == 0 || (pte&PAGE_PRESENT) == 0 {
		return false
	}
	oldFrame := pte & PAGE_FRAME
	if cowFrameManager.Ref(oldFrame) <= 1 {
		SetUint32AtAddr((pte|PAGE_WRITABLE)&^PAGE_COW, pteAddr)
		reloadCR3()
		return true
	}

	newPtr, _ := ActiveMemoryManager.AlignedMalloc(0x1000)
	if newPtr == nil {
		return false
	}
	newFrame := uint32(uintptr(newPtr)) & PAGE_FRAME

	src := GetBytesFromPtr(uintptr(faultAddr&PAGE_FRAME), 0x1000, 0x1000)
	dst := GetBytesFromPtr(uintptr(newFrame), 0x1000, 0x1000)
	copy(dst, src)
	cowFrameManager.Decrement(oldFrame)
	SetUint32AtAddr((newFrame|(pte&0xFFF)|PAGE_WRITABLE)&^PAGE_COW, pteAddr)
	reloadCR3()
	return true
}

func isSharedPDE(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func reloadCR3() {
	cr3 := getCR3()
	setCR3(cr3)
}

func SetByteInPageDir(x byte, addr uint32, pageDir uint32) {
	oldCR3 := getCR3()
	setCR3(pageDir)
	SetByteAtAddr(x, addr)
	setCR3(oldCR3)
}

func SetBlockInPageDir(src []byte, dst []byte, ਆਕਾਰ uint32, pageDir uint32) {
	if ਆਕਾਰ == 0 || pageDir == 0 {
		return
	}
	oldCR3 := getCR3()
	setCR3(pageDir)
	makeRangePrivateWritableCurrent(pageDir, uint32(uintptr(unsafe.Pointer(&dst[0]))), ਆਕਾਰ)

	for i := uint32(0); i < ਆਕਾਰ; i++ {
		dst[i] = src[i]
	}
	setCR3(oldCR3)
}

func ZeroBlockInPageDir(addr uint32, ਆਕਾਰ uint32, pageDir uint32) {
	if ਆਕਾਰ == 0 || pageDir == 0 {
		return
	}
	oldCR3 := getCR3()
	setCR3(pageDir)
	makeRangePrivateWritableCurrent(pageDir, addr, ਆਕਾਰ)
	dst := GetBytesFromPtr(uintptr(addr), int(ਆਕਾਰ), int(ਆਕਾਰ))
	for i := uint32(0); i < ਆਕਾਰ; i++ {
		dst[i] = 0
	}
	setCR3(oldCR3)
}

func makePagePrivateWritableCurrent(pageDir uint32, virtualAddr uint32) bool {
	pde := GetValue(pageDir + ((virtualAddr>>22)&0x3FF)*4)
	if (pde & PAGE_PRESENT) == 0 {
		return false
	}
	pteAddr := (pde & PAGE_FRAME) + ((virtualAddr>>12)&0x3FF)*4
	pte := GetValue(pteAddr)
	if (pte & PAGE_PRESENT) == 0 {
		return false
	}
	if (pte & PAGE_COW) == 0 {
		return (pte & PAGE_WRITABLE) != 0
	}
	if ActiveMemoryManager == nil {
		return false
	}
	newPtr, _ := ActiveMemoryManager.AlignedMalloc(0x1000)
	if newPtr == nil {
		return false
	}
	newFrame := uint32(uintptr(newPtr)) & PAGE_FRAME
	src := GetBytesFromPtr(uintptr(virtualAddr&PAGE_FRAME), 0x1000, 0x1000)
	dst := GetBytesFromPtr(uintptr(newFrame), 0x1000, 0x1000)
	copy(dst, src)
	cowFrameManager.Decrement(pte & PAGE_FRAME)
	SetUint32AtAddr((newFrame|(pte&0xFFF)|PAGE_WRITABLE)&^PAGE_COW, pteAddr)
	// Publish the new physical frame before writing through its virtual address.
	reloadCR3()
	return true
}

func makeRangePrivateWritableCurrent(pageDir uint32, addr uint32, ਆਕਾਰ uint32) bool {
	if ਆਕਾਰ == 0 {
		return true
	}
	last := addr + ਆਕਾਰ - 1
	if last < addr {
		return false
	}
	for page := addr & PAGE_FRAME; ; page += 0x1000 {
		if !makePagePrivateWritableCurrent(pageDir, page) {
			return false
		}
		if page == (last & PAGE_FRAME) {
			break
		}
	}
	return true
}

func MakeRangePrivateWritable(pageDir uint32, addr uint32, ਆਕਾਰ uint32) bool {
	if pageDir == 0 {
		return false
	}
	oldCR3 := getCR3()
	setCR3(pageDir)
	ok := makeRangePrivateWritableCurrent(pageDir, addr, ਆਕਾਰ)
	setCR3(oldCR3)
	return ok
}

func SetUint32InPageDir(x uint32, addr uint32, pageDir uint32) {
	if pageDir == 0 {
		return
	}
	oldCR3 := getCR3()
	setCR3(pageDir)
	SetUint32AtAddr(x, addr)
	setCR3(oldCR3)
}

func GetValue(addr uint32) uint32 {
	var orgValue uint32 = *(*uint32)(unsafe.Pointer(uintptr(addr)))
	return orgValue
}
func GetValueInPageDir(addr uint32, pageDir uint32) uint32 {
	if pageDir == 0 {
		return 0
	}
	oldCR3 := getCR3()
	setCR3(pageDir)
	v := GetValue(addr)
	setCR3(oldCR3)
	return v
}

var v uint32 = 0

func CopyPageFrameBlock(xPageDir uint32, yPageDir uint32, vAddr uint32) {
	if xPageDir == 0 || yPageDir == 0 {
		return
	}
	oldCR3 := getCR3()
	setCR3(xPageDir)
	v = GetValue(vAddr)
	SetUint32InPageDir(v, vAddr, yPageDir)

	setCR3(oldCR3)
}
