package paging

import unsafe "unsafe"
import . "перарыванне"
import . "памяцьmanager"
import . "util"

type СтаронкаКаталогentry_2 uintptr

const (
	СтаронкаПрысутнічае	uint32	= 0x001
	Старонкаwritable	uint32	= 0x002
	СтаронкаКарыстальнік	uint32	= 0x004
	СтаронкаФрэйм		uint32	= 0xFFFFF000
	Старонкаcow		uint32	= 0x200
)

func Вызначанаbyteataddress(x byte, address uint32)
func Вызначанаunsignedinteger8ataddress(x uint8, address uint32)
func Вызначанаunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func вызначанаcr3(старонкаКаталог uint32)
func getcr3() uint32

type Paging struct {
	TПерарываннеhandler
}
type TcowФрэймmanager struct {
	mem		*TПамяцьmanager
	refs		[]uint16
	фрэймcount	uint32
}

var (
	СтаронкаКаталогentry	uintptr
	СтаронкаТабліцаentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowФрэймmanager		TcowФрэймmanager
)

func (self *TcowФрэймmanager) Init(mem *TПамяцьmanager, фрэймcount uint32) bool {
	self.mem = mem
	self.фрэймcount = фрэймcount
	referenceБайтаў := фрэймcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceПаказальнік := mem.Malloc(referenceБайтаў)
	if referenceПаказальнік == nil {
		self.refs = nil
		self.фрэймcount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceПаказальнік)[:фрэймcount:фрэймcount]
	for i := uint32(0); i < фрэймcount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowФрэймmanager) Reference(фрэйм uint32) uint16 {
	idx := фрэйм >> 12
	if idx >= self.фрэймcount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowФрэймmanager) Increment(фрэйм uint32) {
	idx := фрэйм >> 12
	if idx >= self.фрэймcount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowФрэймmanager) Decrement(фрэйм uint32) {
	idx := фрэйм >> 12
	if idx >= self.фрэймcount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(старонкаКаталогentry uintptr, старонкаТабліцаentry uint32, памяцьmanager *TПамяцьmanager) {

	СтаронкаКаталогentry = старонкаКаталогentry
	СтаронкаТабліцаentry = старонкаТабліцаentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowФрэймmanager.Init(памяцьmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressПаказальнік, _ := памяцьmanager.Alignedmalloc(0x1000)
			if addressПаказальнік == nil {
				return
			}
			address := uint32(uintptr(addressПаказальнік))

			Вызначанаunsignedinteger32ataddress(address|0x87, uint32(старонкаКаталогentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Вызначанаunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		старонкаКаталогentry = старонкаКаталогentry + 0x1000
	}

}
func (self *Paging) SharedПамяцьregion() {

	старонкаКаталогentry := СтаронкаКаталогentry
	kСтаронкаКаталогentry := СтаронкаКаталогentry

	for i := uint32(1); i <= virtlen; i++ {

		старонкаКаталогentry = старонкаКаталогentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetЗначэнне(uint32(kСтаронкаКаталогentry) + pde*4)
			v = (v & 0xFFFFF000)
			Вызначанаunsignedinteger32ataddress(v|0x87, uint32(старонкаКаталогentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetЗначэнне(uint32(kСтаронкаКаталогentry) + pde*4)
			v = (v & 0xFFFFF000)
			Вызначанаunsignedinteger32ataddress(v|0x87, uint32(старонкаКаталогentry)+pde*4)

		}

	}
}
func (self *Paging) Старонкаfault(manager *TПерарываннеmanager) {
	перарываннеhandler = handlepagingПерарыванне

	var address uintptr
	address = uintptr(unsafe.Pointer(&перарываннеhandler))
	self.TПерарываннеhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var перарываннеhandler func(uint32) uint32

func handlepagingПерарыванне(esp uint32) uint32 {
	if ResolveСкапіявацьonЗапісfault() {
		return esp
	}
	return HandlefatalПерарываннеФрэйм(esp, 0x0E)
}

func CloneaddressПрагалcow(крыніцаСтаронкаКаталог uint32) uint32 {
	if АктыўнаПамяцьmanager == nil || крыніцаСтаронкаКаталог == 0 {
		return 0
	}
	destinationПаказальнік, _ := АктыўнаПамяцьmanager.Alignedmalloc(0x1000)
	if destinationПаказальнік == nil {
		return 0
	}
	destinationСтаронкаКаталог := uint32(uintptr(destinationПаказальнік))
	for i := uint32(0); i < 1024; i++ {
		Вызначанаunsignedinteger32ataddress(0, destinationСтаронкаКаталог+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		крыніцаpdeaddress := крыніцаСтаронкаКаталог + pde*4
		крыніцаpde := GetЗначэнне(крыніцаpdeaddress)
		if (крыніцаpde & СтаронкаПрысутнічае) == 0 {
			continue
		}
		if issharedpde(pde) {
			Вызначанаunsignedinteger32ataddress(крыніцаpde, destinationСтаронкаКаталог+pde*4)
			continue
		}

		destinationptПаказальнік, _ := АктыўнаПамяцьmanager.Alignedmalloc(0x1000)
		if destinationptПаказальнік == nil {
			continue
		}
		крыніцаpt := крыніцаpde & СтаронкаФрэйм
		destinationpt := uint32(uintptr(destinationptПаказальнік))
		Вызначанаunsignedinteger32ataddress((destinationpt | (крыніцаpde & 0xFFF)), destinationСтаронкаКаталог+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := крыніцаpt + pte*4
			entry := GetЗначэнне(pteaddress)
			if (entry & СтаронкаПрысутнічае) != 0 {
				if (entry & Старонкаwritable) != 0 {
					entry = (entry &^ Старонкаwritable) | Старонкаcow
					Вызначанаunsignedinteger32ataddress(entry, pteaddress)
					cowФрэймmanager.Increment(entry & СтаронкаФрэйм)
				} else if (entry & Старонкаcow) != 0 {
					cowФрэймmanager.Increment(entry & СтаронкаФрэйм)
				}
			}
			Вызначанаunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	перачытацьcr3()
	return destinationСтаронкаКаталог
}

func ResolveСкапіявацьonЗапісfault() bool {
	if АктыўнаПамяцьmanager == nil {
		return false
	}
	faultaddress := getcr2()
	старонкаКаталог := getcr3()
	pdeaddress := старонкаКаталог + ((faultaddress>>22)&0x3FF)*4
	pde := GetЗначэнне(pdeaddress)
	if (pde & СтаронкаПрысутнічае) == 0 {
		return false
	}
	pt := pde & СтаронкаФрэйм
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetЗначэнне(pteaddress)
	if (pte&Старонкаcow) == 0 || (pte&СтаронкаПрысутнічае) == 0 {
		return false
	}
	oldФрэйм := pte & СтаронкаФрэйм
	if cowФрэймmanager.Reference(oldФрэйм) <= 1 {
		Вызначанаunsignedinteger32ataddress((pte|Старонкаwritable)&^Старонкаcow, pteaddress)
		перачытацьcr3()
		return true
	}

	новыПаказальнік, _ := АктыўнаПамяцьmanager.Alignedmalloc(0x1000)
	if новыПаказальнік == nil {
		return false
	}
	новыФрэйм := uint32(uintptr(новыПаказальнік)) & СтаронкаФрэйм

	крыніца_2 := GetБайтаўfromПаказальнік(uintptr(faultaddress&СтаронкаФрэйм), 0x1000, 0x1000)
	destination_2 := GetБайтаўfromПаказальнік(uintptr(новыФрэйм), 0x1000, 0x1000)
	copy(destination_2, крыніца_2)
	cowФрэймmanager.Decrement(oldФрэйм)
	Вызначанаunsignedinteger32ataddress((новыФрэйм|(pte&0xFFF)|Старонкаwritable)&^Старонкаcow, pteaddress)
	перачытацьcr3()
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

func перачытацьcr3() {
	cr3 := getcr3()
	вызначанаcr3(cr3)
}

func ВызначанаbyteуСтаронкаКаталог(x byte, address uint32, старонкаКаталог uint32) {
	oldcr3 := getcr3()
	вызначанаcr3(старонкаКаталог)
	Вызначанаbyteataddress(x, address)
	вызначанаcr3(oldcr3)
}

func ВызначанаБлокуСтаронкаКаталог(крыніца_2 []byte, destination_2 []byte, памер uint32, старонкаКаталог uint32) {
	if памер == 0 || старонкаКаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	вызначанаcr3(старонкаКаталог)
	makeДыяпазонПрыватныwritableДзейны(старонкаКаталог, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), памер)

	for i := uint32(0); i < памер; i++ {
		destination_2[i] = крыніца_2[i]
	}
	вызначанаcr3(oldcr3)
}

func ZeroБлокуСтаронкаКаталог(address uint32, памер uint32, старонкаКаталог uint32) {
	if памер == 0 || старонкаКаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	вызначанаcr3(старонкаКаталог)
	makeДыяпазонПрыватныwritableДзейны(старонкаКаталог, address, памер)
	destination_2 := GetБайтаўfromПаказальнік(uintptr(address), int(памер), int(памер))
	for i := uint32(0); i < памер; i++ {
		destination_2[i] = 0
	}
	вызначанаcr3(oldcr3)
}

func makeСтаронкаПрыватныwritableДзейны(старонкаКаталог uint32, virtualaddress uint32) bool {
	pde := GetЗначэнне(старонкаКаталог + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & СтаронкаПрысутнічае) == 0 {
		return false
	}
	pteaddress := (pde & СтаронкаФрэйм) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetЗначэнне(pteaddress)
	if (pte & СтаронкаПрысутнічае) == 0 {
		return false
	}
	if (pte & Старонкаcow) == 0 {
		return (pte & Старонкаwritable) != 0
	}
	if АктыўнаПамяцьmanager == nil {
		return false
	}
	новыПаказальнік, _ := АктыўнаПамяцьmanager.Alignedmalloc(0x1000)
	if новыПаказальнік == nil {
		return false
	}
	новыФрэйм := uint32(uintptr(новыПаказальнік)) & СтаронкаФрэйм
	крыніца_2 := GetБайтаўfromПаказальнік(uintptr(virtualaddress&СтаронкаФрэйм), 0x1000, 0x1000)
	destination_2 := GetБайтаўfromПаказальнік(uintptr(новыФрэйм), 0x1000, 0x1000)
	copy(destination_2, крыніца_2)
	cowФрэймmanager.Decrement(pte & СтаронкаФрэйм)
	Вызначанаunsignedinteger32ataddress((новыФрэйм|(pte&0xFFF)|Старонкаwritable)&^Старонкаcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	перачытацьcr3()
	return true
}

func makeДыяпазонПрыватныwritableДзейны(старонкаКаталог uint32, address uint32, памер uint32) bool {
	if памер == 0 {
		return true
	}
	last := address + памер - 1
	if last < address {
		return false
	}
	for старонка := address & СтаронкаФрэйм; ; старонка += 0x1000 {
		if !makeСтаронкаПрыватныwritableДзейны(старонкаКаталог, старонка) {
			return false
		}
		if старонка == (last & СтаронкаФрэйм) {
			break
		}
	}
	return true
}

func MakeДыяпазонПрыватныwritable(старонкаКаталог uint32, address uint32, памер uint32) bool {
	if старонкаКаталог == 0 {
		return false
	}
	oldcr3 := getcr3()
	вызначанаcr3(старонкаКаталог)
	добра := makeДыяпазонПрыватныwritableДзейны(старонкаКаталог, address, памер)
	вызначанаcr3(oldcr3)
	return добра
}

func Вызначанаunsignedinteger32уСтаронкаКаталог(x uint32, address uint32, старонкаКаталог uint32) {
	if старонкаКаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	вызначанаcr3(старонкаКаталог)
	Вызначанаunsignedinteger32ataddress(x, address)
	вызначанаcr3(oldcr3)
}

func GetЗначэнне(address uint32) uint32 {
	var orgЗначэнне uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgЗначэнне
}
func GetЗначэннеуСтаронкаКаталог(address uint32, старонкаКаталог uint32) uint32 {
	if старонкаКаталог == 0 {
		return 0
	}
	oldcr3 := getcr3()
	вызначанаcr3(старонкаКаталог)
	v := GetЗначэнне(address)
	вызначанаcr3(oldcr3)
	return v
}

var v uint32 = 0

func СкапіявацьСтаронкаФрэймБлок(xСтаронкаКаталог uint32, yСтаронкаКаталог uint32, vaddress uint32) {
	if xСтаронкаКаталог == 0 || yСтаронкаКаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	вызначанаcr3(xСтаронкаКаталог)
	v = GetЗначэнне(vaddress)
	Вызначанаunsignedinteger32уСтаронкаКаталог(v, vaddress, yСтаронкаКаталог)

	вызначанаcr3(oldcr3)
}
