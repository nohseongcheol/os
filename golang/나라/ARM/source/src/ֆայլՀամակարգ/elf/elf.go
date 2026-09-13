package elf

import . "unsafe"

import . "console"
import . "util"
import . "հիշողությունmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eՏիպ		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eԴրոշներ	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shԱնուն		uint32
	shՏիպ		uint32
	shԴրոշներ	uint32
	shaddress	uint32
	shoffset	uint32
	shՉափս		uint32
	shհղում		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfծրագիրheader struct {
	pՏիպ		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pԴրոշներ	uint32
	pՀավասարեցնել	uint32
}
type Elf32Նշում struct {
	nnamesz	uint32
	ndescsz	uint32
	nՏիպ	uint32
}
type Elf32dyn struct {
	dԹեգ		uint32
	dvalՑուցիչ	uint32
}
type Elf32rel struct {
	roffset	uint32
	rinfo	uint32
}
type Elf32rela struct {
	roffset	uint32
	rinfo	uint32
	raddend	uint32
}
type Elf32sym struct {
	stԱնուն	uint32
	stԱրժեք	uint32
	stՉափս	uint32
	stinfo	uint8
	stԱյլ	uint8
	stshndx	uint16
}
type relocationՏեքստ struct {
	offset		uint32
	հԱՄԱՐ		uint32
	oaddress	uint32
}
type Elf struct {
	տեքստ		[]byte
	տեքստlen	uint32
	relՏեքստ	[100]relocationՏեքստ
	relՏեքստlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (ինքնուրույն *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (ինքնուրույն *Elf) Parse(data []byte, Էջֆայլապանակentry uint32) {

	հիշողությունmanager := TՀիշողությունmanager{}
	var տեքստՑուցիչ Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderՉափս := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderՉափս*i]))

			var sectԱնուն []byte
			սկիզբ := uint32(strtab.shoffset + sectheader.shԱնուն)
			վերջ := սկիզբ
			for ; ; վերջ++ {
				if data[վերջ] == 0x0 || data[վերջ] == ' ' {
					break
				}
			}
			sectԱնուն = data[սկիզբ:վերջ]

			var sectԱրժեք []byte
			if sectheader.shՏիպ != 8 {
				վերջoffset := sectheader.shoffset + sectheader.shՉափս
				if վերջoffset < sectheader.shoffset || վերջoffset > uint32(len(data)) {
					continue
				}
				sectԱրժեք = data[sectheader.shoffset:վերջoffset]
			}

			if EqualԲայթեր(sectԱնուն, ([]byte)(".got.plt")) {
				console_2.MՏպել("[")
				console_2.MՏպել(sectԱնուն)
				console_2.MՏպել(":")
				ինքնուրույն.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Տպել(ինքնուրույն.Got)
				console_2.MՏպել("]")
			}
			if EqualԲայթեր(sectԱնուն, ([]byte)(".dynamic")) {
				console_2.MՏպել("[")
				console_2.MՏպել(sectԱնուն)
				console_2.MՏպել(":")
				dynamic := sectheader.shaddress
				ինքնուրույն.Dynamic = dynamic
				console_2.MUnsignedinteger32Տպել(dynamic)
				console_2.MՏպել("]")
			}

			if sectheader.shaddress > 0x1000 {
				չափս := sectheader.shՉափս
				if sectheader.shՏիպ == 8 {
					ZeroԱրգելափակելՄեջԷջֆայլապանակ(sectheader.shaddress, չափս, Էջֆայլապանակentry)
				} else {
					destination_2 := GetԲայթերիցՑուցիչ(uintptr(sectheader.shaddress), int(չափս), int(չափս))
					SetԱրգելափակելՄեջԷջֆայլապանակ(sectԱրժեք, destination_2, չափս, Էջֆայլապանակentry)
				}
			}

			continue

			if EqualԲայթեր(sectԱնուն, ([]byte)(".text")) {
				console_2.MՏպել(".text")
				console_2.MՏպել("[")
				console_2.MUnsignedinteger32Տպել(sectheader.shaddress)
				console_2.MՏպել(":")
				console_2.MUnsignedinteger32Տպել(sectheader.shoffset)
				console_2.MՏպել(":")
				console_2.MUnsignedinteger32Տպել(sectheader.shՉափս)
				console_2.MՏպել("]")
				copy(ինքնուրույն.տեքստ[:sectheader.shՉափս], sectԱրժեք[:sectheader.shՉափս])
				ինքնուրույն.տեքստlen = sectheader.shՉափս
			}
			if EqualԲայթեր(sectԱնուն, ([]byte)(".rel.text")) {
				console_2.MՏպել(".rel.text")
				console_2.MՏպել("[")
				console_2.MUnsignedinteger32Տպել(sectheader.shaddress)
				console_2.MՏպել(":")
				console_2.MUnsignedinteger32Տպել(sectheader.shՉափս)
				console_2.MՏպել("]")
				for rt := uint32(0); rt < sectheader.shՉափս/8; rt++ {
					offset := *(*uint32)(Pointer(&sectԱրժեք[rt*8]))
					ինքնուրույն.relՏեքստ[rt].offset = offset
					ինքնուրույն.relՏեքստ[rt].oaddress = *(*uint32)(Pointer(&ինքնուրույն.տեքստ[offset]))
					ինքնուրույն.relՏեքստ[rt].հԱՄԱՐ = *(*uint32)(Pointer(&sectԱրժեք[rt*8+4]))
					ինքնուրույն.relՏեքստlen++
				}
			}
			if EqualԲայթեր(sectԱնուն, ([]byte)(".dynsym")) {
				console_2.MՏպել(".dynsym")
				console_2.MՏպել("[")
				console_2.MUnsignedinteger32Տպել(sectheader.shaddress)
				console_2.MՏպել(":")
				console_2.MUnsignedinteger32Տպել(sectheader.shՉափս)
				console_2.MՏպել("]")
				for rt := uint32(0); rt < sectheader.shՉափս/8; rt++ {
					offset := *(*uint32)(Pointer(&sectԱրժեք[rt*8]))
					ինքնուրույն.relՏեքստ[rt].offset = offset
					ինքնուրույն.relՏեքստ[rt].oaddress = *(*uint32)(Pointer(&ինքնուրույն.տեքստ[offset]))
					ինքնուրույն.relՏեքստ[rt].հԱՄԱՐ = *(*uint32)(Pointer(&sectԱրժեք[rt*8+4]))
					ինքնուրույն.relՏեքստlen++
				}
			}
			if EqualԲայթեր(sectԱնուն, ([]byte)(".dynstr")) {
				console_2.MՏպել(".dynstr")
				console_2.MՏպել("[")
				console_2.MUnsignedinteger32Տպել(sectheader.shaddress)
				console_2.MՏպել(":")
				console_2.MUnsignedinteger32Տպել(sectheader.shՉափս)
				console_2.MՏպել("]")
			}
			if EqualԲայթեր(sectԱնուն, ([]byte)(".strtab")) {
				console_2.MՏպել(".strtab")
				console_2.MՏպել("[")
				console_2.MUnsignedinteger32Տպել(sectheader.shaddress)
				console_2.MՏպել("]")
				rt := uint32(0)
				սկիզբ := uint32(0)

				for st := uint32(1); st < sectheader.shՉափս; st++ {
					if sectԱրժեք[st] == 0x0 || sectԱրժեք[st] == ' ' {
						funcԱնուն := sectԱրժեք[սկիզբ+1 : st]
						console_2.MՏպել("+")
						console_2.MՏպել(funcԱնուն)
						ինքնուրույն.strtab[rt] = ԲայթերtoՏՈՂ(funcԱնուն)
						սկիզբ = st
						rt++
					}
				}

			}

		}

		console_2.MՏպել(([]byte)("<------------"))
		for rt := uint32(0); rt < ինքնուրույն.relՏեքստlen; rt++ {
			console_2.MՏպել("[")
			console_2.MՏպել(([]byte)(ինքնուրույն.strtab[rt]))
			console_2.MՏպել(":")
			console_2.MUnsignedinteger32Տպել(ինքնուրույն.relՏեքստ[rt].հԱՄԱՐ)
			console_2.MՏպել(":")

			console_2.MՏպել(([]byte)("]"))
		}
		console_2.MՏպել(([]byte)("------------>"))

		if տեքստՑուցիչ != nil {
			հիշողությունmanager.Ազատ(տեքստՑուցիչ)
		}

	}

}
