/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paginación

import unsafe "unsafe"
import . "interrupción"
import . "memoriagestor"
import . "utilidad"

type Páginadirectorioentrada_2 uintptr

const (
	PáginaPresente	uint32	= 0x001
	Páginawritable	uint32	= 0x002
	Páginausuario	uint32	= 0x004
	Páginatrama	uint32	= 0xFFFFF000
	Páginacow	uint32	= 0x200
)

func EstableceroctetoatDirección(x byte, dirección uint32)
func Establecerunsignedinteger8atDirección(x uint8, dirección uint32)
func Establecerunsignedinteger32atDirección(x uint32, dirección uint32)

func getcr2() uint32

func establecercr3(directorio_de_páginas uint32)
func getcr3() uint32

type Paginación struct {
	TInterrupciónhandler
}
type Tcowtramagestor struct {
	mem		*TMemoriagestor
	refs		[]uint16
	tramaRecuento	uint32
}

var (
	Páginadirectorioentrada	uintptr
	PáginaTablaentrada	uint32
	pdelen			uint32
	virtlen			uint32
	cowtramagestor		Tcowtramagestor
)

func (propio *Tcowtramagestor) Init(mem *TMemoriagestor, tramaRecuento uint32) bool {
	propio.mem = mem
	propio.tramaRecuento = tramaRecuento
	referencebytes := tramaRecuento * uint32(unsafe.Sizeof(uint16(0)))
	referencePuntero := mem.Asignar_memoria(referencebytes)
	if referencePuntero == nil {
		propio.refs = nil
		propio.tramaRecuento = 0
		return false
	}
	propio.refs = (*[1 << 28]uint16)(referencePuntero)[:tramaRecuento:tramaRecuento]
	for i := uint32(0); i < tramaRecuento; i++ {
		propio.refs[i] = 0
	}
	return true
}

func (propio *Tcowtramagestor) Reference(trama uint32) uint16 {
	idx := trama >> 12
	if idx >= propio.tramaRecuento || propio.refs == nil {
		return 0
	}
	return propio.refs[idx]
}

func (propio *Tcowtramagestor) Increment(trama uint32) {
	idx := trama >> 12
	if idx >= propio.tramaRecuento || propio.refs == nil {
		return
	}
	if propio.refs[idx] == 0 {
		propio.refs[idx] = 2
	} else {
		propio.refs[idx]++
	}
}

func (propio *Tcowtramagestor) Decrement(trama uint32) {
	idx := trama >> 12
	if idx >= propio.tramaRecuento || propio.refs == nil || propio.refs[idx] == 0 {
		return
	}
	propio.refs[idx]--
}

func (propio *Paginación) Init(páginadirectorioentrada uintptr, páginaTablaentrada uint32, memoriagestor *TMemoriagestor) {

	Páginadirectorioentrada = páginadirectorioentrada
	PáginaTablaentrada = páginaTablaentrada

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowtramagestor.Init(memoriagestor, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			direcciónPuntero, _ := memoriagestor.Alignedmalloc(0x1000)
			if direcciónPuntero == nil {
				return
			}
			dirección := uint32(uintptr(direcciónPuntero))

			Establecerunsignedinteger32atDirección(dirección|0x87, uint32(páginadirectorioentrada)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Establecerunsignedinteger32atDirección((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, dirección+pte*4)
			}
		}
		páginadirectorioentrada = páginadirectorioentrada + 0x1000
	}

}
func (propio *Paginación) Sharedmemoriaregion() {

	páginadirectorioentrada := Páginadirectorioentrada
	kpáginadirectorioentrada := Páginadirectorioentrada

	for i := uint32(1); i <= virtlen; i++ {

		páginadirectorioentrada = páginadirectorioentrada + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValor(uint32(kpáginadirectorioentrada) + pde*4)
			v = (v & 0xFFFFF000)
			Establecerunsignedinteger32atDirección(v|0x87, uint32(páginadirectorioentrada)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValor(uint32(kpáginadirectorioentrada) + pde*4)
			v = (v & 0xFFFFF000)
			Establecerunsignedinteger32atDirección(v|0x87, uint32(páginadirectorioentrada)+pde*4)

		}

	}
}
func (propio *Paginación) Páginafallo(gestor *TInterrupcióngestor) {
	interrupciónhandler = manijapaginacióninterrupción

	var dirección uintptr
	dirección = uintptr(unsafe.Pointer(&interrupciónhandler))
	propio.TInterrupciónhandler.Init(0xE, uintptr(unsafe.Pointer(gestor)), dirección)
}

var interrupciónhandler func(uint32) uint32

func manijapaginacióninterrupción(esp uint32) uint32 {
	if Resolvercopiaralescribirfallo() {
		return esp
	}
	return Manijafatalinterrupcióntrama(esp, 0x0E)
}

func CloneDirecciónEspaciocow(origenpáginadirectorio uint32) uint32 {
	if Activomemoriagestor == nil || origenpáginadirectorio == 0 {
		return 0
	}
	destinoPuntero, _ := Activomemoriagestor.Alignedmalloc(0x1000)
	if destinoPuntero == nil {
		return 0
	}
	destinopáginadirectorio := uint32(uintptr(destinoPuntero))
	for i := uint32(0); i < 1024; i++ {
		Establecerunsignedinteger32atDirección(0, destinopáginadirectorio+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		origenpdeDirección := origenpáginadirectorio + pde*4
		origenpde := GetValor(origenpdeDirección)
		if (origenpde & PáginaPresente) == 0 {
			continue
		}
		if issharedpde(pde) {
			Establecerunsignedinteger32atDirección(origenpde, destinopáginadirectorio+pde*4)
			continue
		}

		destinoptPuntero, _ := Activomemoriagestor.Alignedmalloc(0x1000)
		if destinoptPuntero == nil {
			continue
		}
		origenpt := origenpde & Páginatrama
		destinopt := uint32(uintptr(destinoptPuntero))
		Establecerunsignedinteger32atDirección((destinopt | (origenpde & 0xFFF)), destinopáginadirectorio+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteDirección := origenpt + pte*4
			entrada := GetValor(pteDirección)
			if (entrada & PáginaPresente) != 0 {
				if (entrada & Páginawritable) != 0 {
					entrada = (entrada &^ Páginawritable) | Páginacow
					Establecerunsignedinteger32atDirección(entrada, pteDirección)
					cowtramagestor.Increment(entrada & Páginatrama)
				} else if (entrada & Páginacow) != 0 {
					cowtramagestor.Increment(entrada & Páginatrama)
				}
			}
			Establecerunsignedinteger32atDirección(entrada, destinopt+pte*4)
		}
	}
	recargarcr3()
	return destinopáginadirectorio
}

func Resolvercopiaralescribirfallo() bool {
	if Activomemoriagestor == nil {
		return false
	}
	falloDirección := getcr2()
	directorio_de_páginas := getcr3()
	pdeDirección := directorio_de_páginas + ((falloDirección>>22)&0x3FF)*4
	pde := GetValor(pdeDirección)
	if (pde & PáginaPresente) == 0 {
		return false
	}
	pt := pde & Páginatrama
	pteDirección := pt + ((falloDirección>>12)&0x3FF)*4
	pte := GetValor(pteDirección)
	if (pte&Páginacow) == 0 || (pte&PáginaPresente) == 0 {
		return false
	}
	oldtrama := pte & Páginatrama
	if cowtramagestor.Reference(oldtrama) <= 1 {
		Establecerunsignedinteger32atDirección((pte|Páginawritable)&^Páginacow, pteDirección)
		recargarcr3()
		return true
	}

	nuevoPuntero, _ := Activomemoriagestor.Alignedmalloc(0x1000)
	if nuevoPuntero == nil {
		return false
	}
	nuevotrama := uint32(uintptr(nuevoPuntero)) & Páginatrama

	origen_2 := GetbytesdesdePuntero(uintptr(falloDirección&Páginatrama), 0x1000, 0x1000)
	destino_2 := GetbytesdesdePuntero(uintptr(nuevotrama), 0x1000, 0x1000)
	copy(destino_2, origen_2)
	cowtramagestor.Decrement(oldtrama)
	Establecerunsignedinteger32atDirección((nuevotrama|(pte&0xFFF)|Páginawritable)&^Páginacow, pteDirección)
	recargarcr3()
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

func recargarcr3() {
	cr3 := getcr3()
	establecercr3(cr3)
}

func EstableceroctetoEntradapáginadirectorio(x byte, dirección uint32, directorio_de_páginas uint32) {
	oldcr3 := getcr3()
	establecercr3(directorio_de_páginas)
	EstableceroctetoatDirección(x, dirección)
	establecercr3(oldcr3)
}

func EstablecerBloqueEntradapáginadirectorio(origen_2 []byte, destino_2 []byte, tamaño uint32, directorio_de_páginas uint32) {
	if tamaño == 0 || directorio_de_páginas == 0 {
		return
	}
	oldcr3 := getcr3()
	establecercr3(directorio_de_páginas)
	makeIntervaloPrivadowritableActual(directorio_de_páginas, uint32(uintptr(unsafe.Pointer(&destino_2[0]))), tamaño)

	for i := uint32(0); i < tamaño; i++ {
		destino_2[i] = origen_2[i]
	}
	establecercr3(oldcr3)
}

func CeroBloqueEntradapáginadirectorio(dirección uint32, tamaño uint32, directorio_de_páginas uint32) {
	if tamaño == 0 || directorio_de_páginas == 0 {
		return
	}
	oldcr3 := getcr3()
	establecercr3(directorio_de_páginas)
	makeIntervaloPrivadowritableActual(directorio_de_páginas, dirección, tamaño)
	destino_2 := GetbytesdesdePuntero(uintptr(dirección), int(tamaño), int(tamaño))
	for i := uint32(0); i < tamaño; i++ {
		destino_2[i] = 0
	}
	establecercr3(oldcr3)
}

func makepáginaPrivadowritableActual(directorio_de_páginas uint32, virtualDirección uint32) bool {
	pde := GetValor(directorio_de_páginas + ((virtualDirección>>22)&0x3FF)*4)
	if (pde & PáginaPresente) == 0 {
		return false
	}
	pteDirección := (pde & Páginatrama) + ((virtualDirección>>12)&0x3FF)*4
	pte := GetValor(pteDirección)
	if (pte & PáginaPresente) == 0 {
		return false
	}
	if (pte & Páginacow) == 0 {
		return (pte & Páginawritable) != 0
	}
	if Activomemoriagestor == nil {
		return false
	}
	nuevoPuntero, _ := Activomemoriagestor.Alignedmalloc(0x1000)
	if nuevoPuntero == nil {
		return false
	}
	nuevotrama := uint32(uintptr(nuevoPuntero)) & Páginatrama
	origen_2 := GetbytesdesdePuntero(uintptr(virtualDirección&Páginatrama), 0x1000, 0x1000)
	destino_2 := GetbytesdesdePuntero(uintptr(nuevotrama), 0x1000, 0x1000)
	copy(destino_2, origen_2)
	cowtramagestor.Decrement(pte & Páginatrama)
	Establecerunsignedinteger32atDirección((nuevotrama|(pte&0xFFF)|Páginawritable)&^Páginacow, pteDirección)
	// Publish the new physical frame before writing through its virtual address.
	recargarcr3()
	return true
}

func makeIntervaloPrivadowritableActual(directorio_de_páginas uint32, dirección uint32, tamaño uint32) bool {
	if tamaño == 0 {
		return true
	}
	última := dirección + tamaño - 1
	if última < dirección {
		return false
	}
	for página := dirección & Páginatrama; ; página += 0x1000 {
		if !makepáginaPrivadowritableActual(directorio_de_páginas, página) {
			return false
		}
		if página == (última & Páginatrama) {
			break
		}
	}
	return true
}

func MakeIntervaloPrivadowritable(directorio_de_páginas uint32, dirección uint32, tamaño uint32) bool {
	if directorio_de_páginas == 0 {
		return false
	}
	oldcr3 := getcr3()
	establecercr3(directorio_de_páginas)
	aceptar := makeIntervaloPrivadowritableActual(directorio_de_páginas, dirección, tamaño)
	establecercr3(oldcr3)
	return aceptar
}

func Establecerunsignedinteger32Entradapáginadirectorio(x uint32, dirección uint32, directorio_de_páginas uint32) {
	if directorio_de_páginas == 0 {
		return
	}
	oldcr3 := getcr3()
	establecercr3(directorio_de_páginas)
	Establecerunsignedinteger32atDirección(x, dirección)
	establecercr3(oldcr3)
}

func GetValor(dirección uint32) uint32 {
	var orgValor uint32 = *(*uint32)(unsafe.Pointer(uintptr(dirección)))
	return orgValor
}
func GetValorEntradapáginadirectorio(dirección uint32, directorio_de_páginas uint32) uint32 {
	if directorio_de_páginas == 0 {
		return 0
	}
	oldcr3 := getcr3()
	establecercr3(directorio_de_páginas)
	v := GetValor(dirección)
	establecercr3(oldcr3)
	return v
}

var v uint32 = 0

func CopiarpáginatramaBloque(xpáginadirectorio uint32, ypáginadirectorio uint32, vDirección uint32) {
	if xpáginadirectorio == 0 || ypáginadirectorio == 0 {
		return
	}
	oldcr3 := getcr3()
	establecercr3(xpáginadirectorio)
	v = GetValor(vDirección)
	Establecerunsignedinteger32Entradapáginadirectorio(v, vDirección, ypáginadirectorio)

	establecercr3(oldcr3)
}
