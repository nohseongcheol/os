/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package format_exécutable_et_liable

import . "unsafe"

import . "console"
import . "utilitaire"
import . "mémoiregestionnaire"
import . "pagination"

type ElfenTête struct {
	eident		[16]byte
	etype		uint16
	emachine	uint16
	eversion	uint32
	eélément	uint32
	ephoff		uint32
	eshoff		uint32
	eAttributs	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type ElfsectionenTête struct {
	shNom		uint32
	shtype		uint32
	shAttributs	uint32
	shaddress	uint32
	shDécalage	uint32
	shTaille	uint32
	shlien		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type ElfprogrammeenTête struct {
	ptype		uint32
	pDécalage	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pAttributs	uint32
	pAligner	uint32
}
type Elf32note struct {
	nnamesz	uint32
	ndescsz	uint32
	ntype	uint32
}
type Elf32dyn struct {
	dÉtiquette	uint32
	dvalPointeur	uint32
}
type Elf32rel struct {
	rDécalage	uint32
	rinfo		uint32
}
type Elf32rela struct {
	rDécalage	uint32
	rinfo		uint32
	raddend		uint32
}
type Elf32sym struct {
	stNom		uint32
	stValeur	uint32
	stTaille	uint32
	stinfo		uint8
	stAutre		uint8
	stshndx		uint16
}
type relocationtexte struct {
	décalage	uint32
	nombre_2	uint32
	oaddress	uint32
}
type Elf struct {
	texte		[]byte
	textelen	uint32
	reltexte	[100]relocationtexte
	reltextelen	uint32
	strtab		[100]string
	Got		uint32
	Dynamique	uint32
}

func (self *Elf) Getélément(données []byte) uint32 {
	elfenTête := (*ElfenTête)(Pointer(&données[0]))
	return elfenTête.eélément
}

func (self *Elf) Parse(données []byte, Pagerépertoireélément uint32) {

	mémoiregestionnaire := TMémoiregestionnaire{}
	var textePointeur Pointer = nil

	var console_2 = TConsole{}

	elfenTête := (*ElfenTête)(Pointer(&données[0]))

	if elfenTête.eshnum != 0 {
		strtab := (*ElfsectionenTête)(Pointer(&données[elfenTête.eshoff+uint32(elfenTête.eshentsize*elfenTête.eshstrndx)]))
		sectenTêteTaille := uint32(Sizeof(ElfsectionenTête{}))

		for i := uint32(0); i < uint32(elfenTête.eshnum); i++ {
			sectenTête := (*ElfsectionenTête)(Pointer(&données[elfenTête.eshoff+sectenTêteTaille*i]))

			var sectNom []byte
			démarrer := uint32(strtab.shDécalage + sectenTête.shNom)
			fin := démarrer
			for ; ; fin++ {
				if données[fin] == 0x0 || données[fin] == ' ' {
					break
				}
			}
			sectNom = données[démarrer:fin]

			var sectValeur []byte
			if sectenTête.shtype != 8 {
				finDécalage := sectenTête.shDécalage + sectenTête.shTaille
				if finDécalage < sectenTête.shDécalage || finDécalage > uint32(len(données)) {
					continue
				}
				sectValeur = données[sectenTête.shDécalage:finDécalage]
			}

			if ÉgalOctets(sectNom, ([]byte)(".got.plt")) {
				console_2.MImprimer("[")
				console_2.MImprimer(sectNom)
				console_2.MImprimer(":")
				self.Got = sectenTête.shaddress
				console_2.MUnsignedinteger32Imprimer(self.Got)
				console_2.MImprimer("]")
			}
			if ÉgalOctets(sectNom, ([]byte)(".dynamic")) {
				console_2.MImprimer("[")
				console_2.MImprimer(sectNom)
				console_2.MImprimer(":")
				dynamique := sectenTête.shaddress
				self.Dynamique = dynamique
				console_2.MUnsignedinteger32Imprimer(dynamique)
				console_2.MImprimer("]")
			}

			if sectenTête.shaddress > 0x1000 {
				taille := sectenTête.shTaille
				if sectenTête.shtype == 8 {
					ZéroBlocEntrantepagerépertoire(sectenTête.shaddress, taille, Pagerépertoireélément)
				} else {
					destination_2 := GetOctetsdePointeur(uintptr(sectenTête.shaddress), int(taille), int(taille))
					EnsembleBlocEntrantepagerépertoire(sectValeur, destination_2, taille, Pagerépertoireélément)
				}
			}

			continue

			if ÉgalOctets(sectNom, ([]byte)(".text")) {
				console_2.MImprimer(".text")
				console_2.MImprimer("[")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shaddress)
				console_2.MImprimer(":")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shDécalage)
				console_2.MImprimer(":")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shTaille)
				console_2.MImprimer("]")
				copy(self.texte[:sectenTête.shTaille], sectValeur[:sectenTête.shTaille])
				self.textelen = sectenTête.shTaille
			}
			if ÉgalOctets(sectNom, ([]byte)(".rel.text")) {
				console_2.MImprimer(".rel.text")
				console_2.MImprimer("[")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shaddress)
				console_2.MImprimer(":")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shTaille)
				console_2.MImprimer("]")
				for rt := uint32(0); rt < sectenTête.shTaille/8; rt++ {
					décalage := *(*uint32)(Pointer(&sectValeur[rt*8]))
					self.reltexte[rt].décalage = décalage
					self.reltexte[rt].oaddress = *(*uint32)(Pointer(&self.texte[décalage]))
					self.reltexte[rt].nombre_2 = *(*uint32)(Pointer(&sectValeur[rt*8+4]))
					self.reltextelen++
				}
			}
			if ÉgalOctets(sectNom, ([]byte)(".dynsym")) {
				console_2.MImprimer(".dynsym")
				console_2.MImprimer("[")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shaddress)
				console_2.MImprimer(":")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shTaille)
				console_2.MImprimer("]")
				for rt := uint32(0); rt < sectenTête.shTaille/8; rt++ {
					décalage := *(*uint32)(Pointer(&sectValeur[rt*8]))
					self.reltexte[rt].décalage = décalage
					self.reltexte[rt].oaddress = *(*uint32)(Pointer(&self.texte[décalage]))
					self.reltexte[rt].nombre_2 = *(*uint32)(Pointer(&sectValeur[rt*8+4]))
					self.reltextelen++
				}
			}
			if ÉgalOctets(sectNom, ([]byte)(".dynstr")) {
				console_2.MImprimer(".dynstr")
				console_2.MImprimer("[")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shaddress)
				console_2.MImprimer(":")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shTaille)
				console_2.MImprimer("]")
			}
			if ÉgalOctets(sectNom, ([]byte)(".strtab")) {
				console_2.MImprimer(".strtab")
				console_2.MImprimer("[")
				console_2.MUnsignedinteger32Imprimer(sectenTête.shaddress)
				console_2.MImprimer("]")
				rt := uint32(0)
				démarrer := uint32(0)

				for st := uint32(1); st < sectenTête.shTaille; st++ {
					if sectValeur[st] == 0x0 || sectValeur[st] == ' ' {
						funcNom := sectValeur[démarrer+1 : st]
						console_2.MImprimer("+")
						console_2.MImprimer(funcNom)
						self.strtab[rt] = OctetstoChaîne(funcNom)
						démarrer = st
						rt++
					}
				}

			}

		}

		console_2.MImprimer(([]byte)("<------------"))
		for rt := uint32(0); rt < self.reltextelen; rt++ {
			console_2.MImprimer("[")
			console_2.MImprimer(([]byte)(self.strtab[rt]))
			console_2.MImprimer(":")
			console_2.MUnsignedinteger32Imprimer(self.reltexte[rt].nombre_2)
			console_2.MImprimer(":")

			console_2.MImprimer(([]byte)("]"))
		}
		console_2.MImprimer(([]byte)("------------>"))

		if textePointeur != nil {
			mémoiregestionnaire.Libre(textePointeur)
		}

	}

}
