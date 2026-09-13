package paging

import unsafe "unsafe"
import . "interrupt"
import . "memoriamanager"
import . "util"

type PAGINACartellavoce_2 uintptr

const (
	PAGINAPresente	uint32	= 0x001
	PAGINAwritable	uint32	= 0x002
	PAGINAUtente	uint32	= 0x004
	PAGINARiquadro	uint32	= 0xFFFFF000
	PAGINAcow	uint32	= 0x200
)

func Impostabyteataddress(x byte, address uint32)
func Impostaunsignedinteger8ataddress(x uint8, address uint32)
func Impostaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func impostacr3(indice_delle_pagine uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowRiquadromanager struct {
	mem			*TMemoriamanager
	refs			[]uint16
	riquadroConteggio	uint32
}

var (
	PAGINACartellavoce	uintptr
	PAGINATabellavoce	uint32
	pdelen			uint32
	virtlen			uint32
	cowRiquadromanager	TcowRiquadromanager
)

func (séstesso *TcowRiquadromanager) Init(mem *TMemoriamanager, riquadroConteggio uint32) bool {
	séstesso.mem = mem
	séstesso.riquadroConteggio = riquadroConteggio
	referenceByte := riquadroConteggio * uint32(unsafe.Sizeof(uint16(0)))
	referencePuntatore := mem.Alloca_memoria(referenceByte)
	if referencePuntatore == nil {
		séstesso.refs = nil
		séstesso.riquadroConteggio = 0
		return false
	}
	séstesso.refs = (*[1 << 28]uint16)(referencePuntatore)[:riquadroConteggio:riquadroConteggio]
	for i := uint32(0); i < riquadroConteggio; i++ {
		séstesso.refs[i] = 0
	}
	return true
}

func (séstesso *TcowRiquadromanager) Reference(riquadro uint32) uint16 {
	idx := riquadro >> 12
	if idx >= séstesso.riquadroConteggio || séstesso.refs == nil {
		return 0
	}
	return séstesso.refs[idx]
}

func (séstesso *TcowRiquadromanager) Increment(riquadro uint32) {
	idx := riquadro >> 12
	if idx >= séstesso.riquadroConteggio || séstesso.refs == nil {
		return
	}
	if séstesso.refs[idx] == 0 {
		séstesso.refs[idx] = 2
	} else {
		séstesso.refs[idx]++
	}
}

func (séstesso *TcowRiquadromanager) Decrement(riquadro uint32) {
	idx := riquadro >> 12
	if idx >= séstesso.riquadroConteggio || séstesso.refs == nil || séstesso.refs[idx] == 0 {
		return
	}
	séstesso.refs[idx]--
}

func (séstesso *Paging) Init(pAGINACartellavoce uintptr, pAGINATabellavoce uint32, memoriamanager *TMemoriamanager) {

	PAGINACartellavoce = pAGINACartellavoce
	PAGINATabellavoce = pAGINATabellavoce

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRiquadromanager.Init(memoriamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPuntatore, _ := memoriamanager.Alignedmalloc(0x1000)
			if addressPuntatore == nil {
				return
			}
			address := uint32(uintptr(addressPuntatore))

			Impostaunsignedinteger32ataddress(address|0x87, uint32(pAGINACartellavoce)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Impostaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		pAGINACartellavoce = pAGINACartellavoce + 0x1000
	}

}
func (séstesso *Paging) SharedMemoriaregion() {

	pAGINACartellavoce := PAGINACartellavoce
	kPAGINACartellavoce := PAGINACartellavoce

	for i := uint32(1); i <= virtlen; i++ {

		pAGINACartellavoce = pAGINACartellavoce + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValore(uint32(kPAGINACartellavoce) + pde*4)
			v = (v & 0xFFFFF000)
			Impostaunsignedinteger32ataddress(v|0x87, uint32(pAGINACartellavoce)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValore(uint32(kPAGINACartellavoce) + pde*4)
			v = (v & 0xFFFFF000)
			Impostaunsignedinteger32ataddress(v|0x87, uint32(pAGINACartellavoce)+pde*4)

		}

	}
}
func (séstesso *Paging) PAGINAfault(manager *TInterruptmanager) {
	interrupthandler = manigliapaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	séstesso.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func manigliapaginginterrupt(esp uint32) uint32 {
	if ResolveCopiaAccesoScritturafault() {
		return esp
	}
	return ManigliafatalinterruptRiquadro(esp, 0x0E)
}

func CloneaddressSpaziocow(originePAGINACartella uint32) uint32 {
	if AttivoMemoriamanager == nil || originePAGINACartella == 0 {
		return 0
	}
	destinazionePuntatore, _ := AttivoMemoriamanager.Alignedmalloc(0x1000)
	if destinazionePuntatore == nil {
		return 0
	}
	destinazionePAGINACartella := uint32(uintptr(destinazionePuntatore))
	for i := uint32(0); i < 1024; i++ {
		Impostaunsignedinteger32ataddress(0, destinazionePAGINACartella+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		originepdeaddress := originePAGINACartella + pde*4
		originepde := GetValore(originepdeaddress)
		if (originepde & PAGINAPresente) == 0 {
			continue
		}
		if issharedpde(pde) {
			Impostaunsignedinteger32ataddress(originepde, destinazionePAGINACartella+pde*4)
			continue
		}

		destinazioneptPuntatore, _ := AttivoMemoriamanager.Alignedmalloc(0x1000)
		if destinazioneptPuntatore == nil {
			continue
		}
		originept := originepde & PAGINARiquadro
		destinazionept := uint32(uintptr(destinazioneptPuntatore))
		Impostaunsignedinteger32ataddress((destinazionept | (originepde & 0xFFF)), destinazionePAGINACartella+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := originept + pte*4
			voce := GetValore(pteaddress)
			if (voce & PAGINAPresente) != 0 {
				if (voce & PAGINAwritable) != 0 {
					voce = (voce &^ PAGINAwritable) | PAGINAcow
					Impostaunsignedinteger32ataddress(voce, pteaddress)
					cowRiquadromanager.Increment(voce & PAGINARiquadro)
				} else if (voce & PAGINAcow) != 0 {
					cowRiquadromanager.Increment(voce & PAGINARiquadro)
				}
			}
			Impostaunsignedinteger32ataddress(voce, destinazionept+pte*4)
		}
	}
	ricaricacr3()
	return destinazionePAGINACartella
}

func ResolveCopiaAccesoScritturafault() bool {
	if AttivoMemoriamanager == nil {
		return false
	}
	faultaddress := getcr2()
	indice_delle_pagine := getcr3()
	pdeaddress := indice_delle_pagine + ((faultaddress>>22)&0x3FF)*4
	pde := GetValore(pdeaddress)
	if (pde & PAGINAPresente) == 0 {
		return false
	}
	pt := pde & PAGINARiquadro
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetValore(pteaddress)
	if (pte&PAGINAcow) == 0 || (pte&PAGINAPresente) == 0 {
		return false
	}
	oldRiquadro := pte & PAGINARiquadro
	if cowRiquadromanager.Reference(oldRiquadro) <= 1 {
		Impostaunsignedinteger32ataddress((pte|PAGINAwritable)&^PAGINAcow, pteaddress)
		ricaricacr3()
		return true
	}

	nuovoPuntatore, _ := AttivoMemoriamanager.Alignedmalloc(0x1000)
	if nuovoPuntatore == nil {
		return false
	}
	nuovoRiquadro := uint32(uintptr(nuovoPuntatore)) & PAGINARiquadro

	origine_2 := GetBytefromPuntatore(uintptr(faultaddress&PAGINARiquadro), 0x1000, 0x1000)
	destinazione_2 := GetBytefromPuntatore(uintptr(nuovoRiquadro), 0x1000, 0x1000)
	copy(destinazione_2, origine_2)
	cowRiquadromanager.Decrement(oldRiquadro)
	Impostaunsignedinteger32ataddress((nuovoRiquadro|(pte&0xFFF)|PAGINAwritable)&^PAGINAcow, pteaddress)
	ricaricacr3()
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

func ricaricacr3() {
	cr3 := getcr3()
	impostacr3(cr3)
}

func ImpostabyteIngressoPAGINACartella(x byte, address uint32, indice_delle_pagine uint32) {
	oldcr3 := getcr3()
	impostacr3(indice_delle_pagine)
	Impostabyteataddress(x, address)
	impostacr3(oldcr3)
}

func ImpostaBloccoIngressoPAGINACartella(origine_2 []byte, destinazione_2 []byte, dimensione uint32, indice_delle_pagine uint32) {
	if dimensione == 0 || indice_delle_pagine == 0 {
		return
	}
	oldcr3 := getcr3()
	impostacr3(indice_delle_pagine)
	makeIntervalloPrivatowritableCorrente(indice_delle_pagine, uint32(uintptr(unsafe.Pointer(&destinazione_2[0]))), dimensione)

	for i := uint32(0); i < dimensione; i++ {
		destinazione_2[i] = origine_2[i]
	}
	impostacr3(oldcr3)
}

func ZeroBloccoIngressoPAGINACartella(address uint32, dimensione uint32, indice_delle_pagine uint32) {
	if dimensione == 0 || indice_delle_pagine == 0 {
		return
	}
	oldcr3 := getcr3()
	impostacr3(indice_delle_pagine)
	makeIntervalloPrivatowritableCorrente(indice_delle_pagine, address, dimensione)
	destinazione_2 := GetBytefromPuntatore(uintptr(address), int(dimensione), int(dimensione))
	for i := uint32(0); i < dimensione; i++ {
		destinazione_2[i] = 0
	}
	impostacr3(oldcr3)
}

func makePAGINAPrivatowritableCorrente(indice_delle_pagine uint32, virtualeaddress uint32) bool {
	pde := GetValore(indice_delle_pagine + ((virtualeaddress>>22)&0x3FF)*4)
	if (pde & PAGINAPresente) == 0 {
		return false
	}
	pteaddress := (pde & PAGINARiquadro) + ((virtualeaddress>>12)&0x3FF)*4
	pte := GetValore(pteaddress)
	if (pte & PAGINAPresente) == 0 {
		return false
	}
	if (pte & PAGINAcow) == 0 {
		return (pte & PAGINAwritable) != 0
	}
	if AttivoMemoriamanager == nil {
		return false
	}
	nuovoPuntatore, _ := AttivoMemoriamanager.Alignedmalloc(0x1000)
	if nuovoPuntatore == nil {
		return false
	}
	nuovoRiquadro := uint32(uintptr(nuovoPuntatore)) & PAGINARiquadro
	origine_2 := GetBytefromPuntatore(uintptr(virtualeaddress&PAGINARiquadro), 0x1000, 0x1000)
	destinazione_2 := GetBytefromPuntatore(uintptr(nuovoRiquadro), 0x1000, 0x1000)
	copy(destinazione_2, origine_2)
	cowRiquadromanager.Decrement(pte & PAGINARiquadro)
	Impostaunsignedinteger32ataddress((nuovoRiquadro|(pte&0xFFF)|PAGINAwritable)&^PAGINAcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	ricaricacr3()
	return true
}

func makeIntervalloPrivatowritableCorrente(indice_delle_pagine uint32, address uint32, dimensione uint32) bool {
	if dimensione == 0 {
		return true
	}
	ultima := address + dimensione - 1
	if ultima < address {
		return false
	}
	for pAGINA := address & PAGINARiquadro; ; pAGINA += 0x1000 {
		if !makePAGINAPrivatowritableCorrente(indice_delle_pagine, pAGINA) {
			return false
		}
		if pAGINA == (ultima & PAGINARiquadro) {
			break
		}
	}
	return true
}

func MakeIntervalloPrivatowritable(indice_delle_pagine uint32, address uint32, dimensione uint32) bool {
	if indice_delle_pagine == 0 {
		return false
	}
	oldcr3 := getcr3()
	impostacr3(indice_delle_pagine)
	fatto := makeIntervalloPrivatowritableCorrente(indice_delle_pagine, address, dimensione)
	impostacr3(oldcr3)
	return fatto
}

func Impostaunsignedinteger32IngressoPAGINACartella(x uint32, address uint32, indice_delle_pagine uint32) {
	if indice_delle_pagine == 0 {
		return
	}
	oldcr3 := getcr3()
	impostacr3(indice_delle_pagine)
	Impostaunsignedinteger32ataddress(x, address)
	impostacr3(oldcr3)
}

func GetValore(address uint32) uint32 {
	var orgValore uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgValore
}
func GetValoreIngressoPAGINACartella(address uint32, indice_delle_pagine uint32) uint32 {
	if indice_delle_pagine == 0 {
		return 0
	}
	oldcr3 := getcr3()
	impostacr3(indice_delle_pagine)
	v := GetValore(address)
	impostacr3(oldcr3)
	return v
}

var v uint32 = 0

func CopiaPAGINARiquadroBlocco(xPAGINACartella uint32, yPAGINACartella uint32, vaddress uint32) {
	if xPAGINACartella == 0 || yPAGINACartella == 0 {
		return
	}
	oldcr3 := getcr3()
	impostacr3(xPAGINACartella)
	v = GetValore(vaddress)
	Impostaunsignedinteger32IngressoPAGINACartella(v, vaddress, yPAGINACartella)

	impostacr3(oldcr3)
}
