package paging

import unsafe "unsafe"
import . "переривання"
import . "памятьmanager"
import . "util"

type СторінкаТеказапис_2 uintptr

const (
	СторінкаПрисутній	uint32	= 0x001
	Сторінкаwritable	uint32	= 0x002
	СторінкаКористувач	uint32	= 0x004
	СторінкаБлок		uint32	= 0xFFFFF000
	Сторінкаcow		uint32	= 0x200
)

func МножинаbyteatАдреса(x byte, адреса uint32)
func Множинаunsignedinteger8atАдреса(x uint8, адреса uint32)
func Множинаunsignedinteger32atАдреса(x uint32, адреса uint32)

func getcr2() uint32

func множинаcr3(каталог_сторінок uint32)
func getcr3() uint32

type Paging struct {
	TПерериванняhandler
}
type TcowБлокmanager struct {
	mem		*TПамятьmanager
	refs		[]uint16
	блокВідлік	uint32
}

var (
	СторінкаТеказапис	uintptr
	СторінкаТаблицязапис	uint32
	pdelen			uint32
	virtlen			uint32
	cowБлокmanager		TcowБлокmanager
)

func (поточний *TcowБлокmanager) Init(mem *TПамятьmanager, блокВідлік uint32) bool {
	поточний.mem = mem
	поточний.блокВідлік = блокВідлік
	referenceБайт := блокВідлік * uint32(unsafe.Sizeof(uint16(0)))
	referenceВказівник := mem.Виділити_памʼять(referenceБайт)
	if referenceВказівник == nil {
		поточний.refs = nil
		поточний.блокВідлік = 0
		return false
	}
	поточний.refs = (*[1 << 28]uint16)(referenceВказівник)[:блокВідлік:блокВідлік]
	for i := uint32(0); i < блокВідлік; i++ {
		поточний.refs[i] = 0
	}
	return true
}

func (поточний *TcowБлокmanager) Reference(блок uint32) uint16 {
	idx := блок >> 12
	if idx >= поточний.блокВідлік || поточний.refs == nil {
		return 0
	}
	return поточний.refs[idx]
}

func (поточний *TcowБлокmanager) Increment(блок uint32) {
	idx := блок >> 12
	if idx >= поточний.блокВідлік || поточний.refs == nil {
		return
	}
	if поточний.refs[idx] == 0 {
		поточний.refs[idx] = 2
	} else {
		поточний.refs[idx]++
	}
}

func (поточний *TcowБлокmanager) Decrement(блок uint32) {
	idx := блок >> 12
	if idx >= поточний.блокВідлік || поточний.refs == nil || поточний.refs[idx] == 0 {
		return
	}
	поточний.refs[idx]--
}

func (поточний *Paging) Init(сторінкаТеказапис uintptr, сторінкаТаблицязапис uint32, памятьmanager *TПамятьmanager) {

	СторінкаТеказапис = сторінкаТеказапис
	СторінкаТаблицязапис = сторінкаТаблицязапис

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowБлокmanager.Init(памятьmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			адресаВказівник, _ := памятьmanager.Alignedmalloc(0x1000)
			if адресаВказівник == nil {
				return
			}
			адреса := uint32(uintptr(адресаВказівник))

			Множинаunsignedinteger32atАдреса(адреса|0x87, uint32(сторінкаТеказапис)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Множинаunsignedinteger32atАдреса((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, адреса+pte*4)
			}
		}
		сторінкаТеказапис = сторінкаТеказапис + 0x1000
	}

}
func (поточний *Paging) SharedПамятьregion() {

	сторінкаТеказапис := СторінкаТеказапис
	kСторінкаТеказапис := СторінкаТеказапис

	for i := uint32(1); i <= virtlen; i++ {

		сторінкаТеказапис = сторінкаТеказапис + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetЗначення(uint32(kСторінкаТеказапис) + pde*4)
			v = (v & 0xFFFFF000)
			Множинаunsignedinteger32atАдреса(v|0x87, uint32(сторінкаТеказапис)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetЗначення(uint32(kСторінкаТеказапис) + pde*4)
			v = (v & 0xFFFFF000)
			Множинаunsignedinteger32atАдреса(v|0x87, uint32(сторінкаТеказапис)+pde*4)

		}

	}
}
func (поточний *Paging) Сторінкаfault(manager *TПерериванняmanager) {
	перериванняhandler = елементкеруванняpagingПереривання

	var адреса uintptr
	адреса = uintptr(unsafe.Pointer(&перериванняhandler))
	поточний.TПерериванняhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), адреса)
}

var перериванняhandler func(uint32) uint32

func елементкеруванняpagingПереривання(esp uint32) uint32 {
	if ResolveКопіюватиУвімкненоЗаписfault() {
		return esp
	}
	return ЕлементкеруванняfatalПерериванняБлок(esp, 0x0E)
}

func CloneАдресаПробілcow(джерелоСторінкаТека uint32) uint32 {
	if АктивнийПамятьmanager == nil || джерелоСторінкаТека == 0 {
		return 0
	}
	призначенняВказівник, _ := АктивнийПамятьmanager.Alignedmalloc(0x1000)
	if призначенняВказівник == nil {
		return 0
	}
	призначенняСторінкаТека := uint32(uintptr(призначенняВказівник))
	for i := uint32(0); i < 1024; i++ {
		Множинаunsignedinteger32atАдреса(0, призначенняСторінкаТека+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		джерелоpdeАдреса := джерелоСторінкаТека + pde*4
		джерелоpde := GetЗначення(джерелоpdeАдреса)
		if (джерелоpde & СторінкаПрисутній) == 0 {
			continue
		}
		if issharedpde(pde) {
			Множинаunsignedinteger32atАдреса(джерелоpde, призначенняСторінкаТека+pde*4)
			continue
		}

		призначенняptВказівник, _ := АктивнийПамятьmanager.Alignedmalloc(0x1000)
		if призначенняptВказівник == nil {
			continue
		}
		джерелоpt := джерелоpde & СторінкаБлок
		призначенняpt := uint32(uintptr(призначенняptВказівник))
		Множинаunsignedinteger32atАдреса((призначенняpt | (джерелоpde & 0xFFF)), призначенняСторінкаТека+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteАдреса := джерелоpt + pte*4
			запис := GetЗначення(pteАдреса)
			if (запис & СторінкаПрисутній) != 0 {
				if (запис & Сторінкаwritable) != 0 {
					запис = (запис &^ Сторінкаwritable) | Сторінкаcow
					Множинаunsignedinteger32atАдреса(запис, pteАдреса)
					cowБлокmanager.Increment(запис & СторінкаБлок)
				} else if (запис & Сторінкаcow) != 0 {
					cowБлокmanager.Increment(запис & СторінкаБлок)
				}
			}
			Множинаunsignedinteger32atАдреса(запис, призначенняpt+pte*4)
		}
	}
	перезавантажитиcr3()
	return призначенняСторінкаТека
}

func ResolveКопіюватиУвімкненоЗаписfault() bool {
	if АктивнийПамятьmanager == nil {
		return false
	}
	faultАдреса := getcr2()
	каталог_сторінок := getcr3()
	pdeАдреса := каталог_сторінок + ((faultАдреса>>22)&0x3FF)*4
	pde := GetЗначення(pdeАдреса)
	if (pde & СторінкаПрисутній) == 0 {
		return false
	}
	pt := pde & СторінкаБлок
	pteАдреса := pt + ((faultАдреса>>12)&0x3FF)*4
	pte := GetЗначення(pteАдреса)
	if (pte&Сторінкаcow) == 0 || (pte&СторінкаПрисутній) == 0 {
		return false
	}
	oldБлок := pte & СторінкаБлок
	if cowБлокmanager.Reference(oldБлок) <= 1 {
		Множинаunsignedinteger32atАдреса((pte|Сторінкаwritable)&^Сторінкаcow, pteАдреса)
		перезавантажитиcr3()
		return true
	}

	новийВказівник, _ := АктивнийПамятьmanager.Alignedmalloc(0x1000)
	if новийВказівник == nil {
		return false
	}
	новийБлок := uint32(uintptr(новийВказівник)) & СторінкаБлок

	джерело_2 := GetБайтзВказівник(uintptr(faultАдреса&СторінкаБлок), 0x1000, 0x1000)
	призначення_2 := GetБайтзВказівник(uintptr(новийБлок), 0x1000, 0x1000)
	copy(призначення_2, джерело_2)
	cowБлокmanager.Decrement(oldБлок)
	Множинаunsignedinteger32atАдреса((новийБлок|(pte&0xFFF)|Сторінкаwritable)&^Сторінкаcow, pteАдреса)
	перезавантажитиcr3()
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

func перезавантажитиcr3() {
	cr3 := getcr3()
	множинаcr3(cr3)
}

func МножинаbyteВхіднийСторінкаТека(x byte, адреса uint32, каталог_сторінок uint32) {
	oldcr3 := getcr3()
	множинаcr3(каталог_сторінок)
	МножинаbyteatАдреса(x, адреса)
	множинаcr3(oldcr3)
}

func МножинаБлокВхіднийСторінкаТека(джерело_2 []byte, призначення_2 []byte, розмір uint32, каталог_сторінок uint32) {
	if розмір == 0 || каталог_сторінок == 0 {
		return
	}
	oldcr3 := getcr3()
	множинаcr3(каталог_сторінок)
	makeДіяпазонЗакритаwritableПоточна(каталог_сторінок, uint32(uintptr(unsafe.Pointer(&призначення_2[0]))), розмір)

	for i := uint32(0); i < розмір; i++ {
		призначення_2[i] = джерело_2[i]
	}
	множинаcr3(oldcr3)
}

func НульБлокВхіднийСторінкаТека(адреса uint32, розмір uint32, каталог_сторінок uint32) {
	if розмір == 0 || каталог_сторінок == 0 {
		return
	}
	oldcr3 := getcr3()
	множинаcr3(каталог_сторінок)
	makeДіяпазонЗакритаwritableПоточна(каталог_сторінок, адреса, розмір)
	призначення_2 := GetБайтзВказівник(uintptr(адреса), int(розмір), int(розмір))
	for i := uint32(0); i < розмір; i++ {
		призначення_2[i] = 0
	}
	множинаcr3(oldcr3)
}

func makeСторінкаЗакритаwritableПоточна(каталог_сторінок uint32, віртуальнийАдреса uint32) bool {
	pde := GetЗначення(каталог_сторінок + ((віртуальнийАдреса>>22)&0x3FF)*4)
	if (pde & СторінкаПрисутній) == 0 {
		return false
	}
	pteАдреса := (pde & СторінкаБлок) + ((віртуальнийАдреса>>12)&0x3FF)*4
	pte := GetЗначення(pteАдреса)
	if (pte & СторінкаПрисутній) == 0 {
		return false
	}
	if (pte & Сторінкаcow) == 0 {
		return (pte & Сторінкаwritable) != 0
	}
	if АктивнийПамятьmanager == nil {
		return false
	}
	новийВказівник, _ := АктивнийПамятьmanager.Alignedmalloc(0x1000)
	if новийВказівник == nil {
		return false
	}
	новийБлок := uint32(uintptr(новийВказівник)) & СторінкаБлок
	джерело_2 := GetБайтзВказівник(uintptr(віртуальнийАдреса&СторінкаБлок), 0x1000, 0x1000)
	призначення_2 := GetБайтзВказівник(uintptr(новийБлок), 0x1000, 0x1000)
	copy(призначення_2, джерело_2)
	cowБлокmanager.Decrement(pte & СторінкаБлок)
	Множинаunsignedinteger32atАдреса((новийБлок|(pte&0xFFF)|Сторінкаwritable)&^Сторінкаcow, pteАдреса)
	// Publish the new physical frame before writing through its virtual address.
	перезавантажитиcr3()
	return true
}

func makeДіяпазонЗакритаwritableПоточна(каталог_сторінок uint32, адреса uint32, розмір uint32) bool {
	if розмір == 0 {
		return true
	}
	останнє := адреса + розмір - 1
	if останнє < адреса {
		return false
	}
	for сторінка := адреса & СторінкаБлок; ; сторінка += 0x1000 {
		if !makeСторінкаЗакритаwritableПоточна(каталог_сторінок, сторінка) {
			return false
		}
		if сторінка == (останнє & СторінкаБлок) {
			break
		}
	}
	return true
}

func MakeДіяпазонЗакритаwritable(каталог_сторінок uint32, адреса uint32, розмір uint32) bool {
	if каталог_сторінок == 0 {
		return false
	}
	oldcr3 := getcr3()
	множинаcr3(каталог_сторінок)
	гаразд := makeДіяпазонЗакритаwritableПоточна(каталог_сторінок, адреса, розмір)
	множинаcr3(oldcr3)
	return гаразд
}

func Множинаunsignedinteger32ВхіднийСторінкаТека(x uint32, адреса uint32, каталог_сторінок uint32) {
	if каталог_сторінок == 0 {
		return
	}
	oldcr3 := getcr3()
	множинаcr3(каталог_сторінок)
	Множинаunsignedinteger32atАдреса(x, адреса)
	множинаcr3(oldcr3)
}

func GetЗначення(адреса uint32) uint32 {
	var orgЗначення uint32 = *(*uint32)(unsafe.Pointer(uintptr(адреса)))
	return orgЗначення
}
func GetЗначенняВхіднийСторінкаТека(адреса uint32, каталог_сторінок uint32) uint32 {
	if каталог_сторінок == 0 {
		return 0
	}
	oldcr3 := getcr3()
	множинаcr3(каталог_сторінок)
	v := GetЗначення(адреса)
	множинаcr3(oldcr3)
	return v
}

var v uint32 = 0

func КопіюватиСторінкаБлокБлок(xСторінкаТека uint32, yСторінкаТека uint32, vАдреса uint32) {
	if xСторінкаТека == 0 || yСторінкаТека == 0 {
		return
	}
	oldcr3 := getcr3()
	множинаcr3(xСторінкаТека)
	v = GetЗначення(vАдреса)
	Множинаunsignedinteger32ВхіднийСторінкаТека(v, vАдреса, yСторінкаТека)

	множинаcr3(oldcr3)
}
