/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package định_dạng_thực_thi_và_liên_kết

import . "unsafe"

import . "console"
import . "util"
import . "bộnhớmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eKiểu		uint16
	emachine	uint16
	ePhiênbản	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eCờ		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shTên		uint32
	shKiểu		uint32
	shCờ		uint32
	shaddress	uint32
	shoffset	uint32
	shCỡ		uint32
	shLiênkết	uint32
	shThôngtin	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfchươngtrìnhheader struct {
	pKiểu	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pCờ	uint32
	pCanhlề	uint32
}
type Elf32Ghichú struct {
	nnamesz	uint32
	ndescsz	uint32
	nKiểu	uint32
}
type Elf32dyn struct {
	dThẻ		uint32
	dvalContrỏ	uint32
}
type Elf32rel struct {
	roffset		uint32
	rThôngtin	uint32
}
type Elf32rela struct {
	roffset		uint32
	rThôngtin	uint32
	raddend		uint32
}
type Elf32sym struct {
	stTên		uint32
	stGiátrị	uint32
	stCỡ		uint32
	stThôngtin	uint8
	stKhác		uint8
	stshndx		uint16
}
type relocationNhãn struct {
	offset		uint32
	sỐ		uint32
	oaddress	uint32
}
type Elf struct {
	nhãn		[]byte
	nhãnlen		uint32
	relNhãn		[100]relocationNhãn
	relNhãnlen	uint32
	strtab		[100]string
	Got		uint32
	Năngđộng	uint32
}

func (mình *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (mình *Elf) Parse(data []byte, TrangThưmụcentry uint32) {

	bộnhớmanager := TBộnhớmanager{}
	var nhãnContrỏ Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderCỡ := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderCỡ*i]))

			var sectTên []byte
			chạy := uint32(strtab.shoffset + sectheader.shTên)
			kếtthúc := chạy
			for ; ; kếtthúc++ {
				if data[kếtthúc] == 0x0 || data[kếtthúc] == ' ' {
					break
				}
			}
			sectTên = data[chạy:kếtthúc]

			var sectGiátrị []byte
			if sectheader.shKiểu != 8 {
				kếtthúcoffset := sectheader.shoffset + sectheader.shCỡ
				if kếtthúcoffset < sectheader.shoffset || kếtthúcoffset > uint32(len(data)) {
					continue
				}
				sectGiátrị = data[sectheader.shoffset:kếtthúcoffset]
			}

			if EqualByte(sectTên, ([]byte)(".got.plt")) {
				console_2.MIn("[")
				console_2.MIn(sectTên)
				console_2.MIn(":")
				mình.Got = sectheader.shaddress
				console_2.MUnsignedinteger32In(mình.Got)
				console_2.MIn("]")
			}
			if EqualByte(sectTên, ([]byte)(".dynamic")) {
				console_2.MIn("[")
				console_2.MIn(sectTên)
				console_2.MIn(":")
				năngđộng := sectheader.shaddress
				mình.Năngđộng = năngđộng
				console_2.MUnsignedinteger32In(năngđộng)
				console_2.MIn("]")
			}

			if sectheader.shaddress > 0x1000 {
				cỡ := sectheader.shCỡ
				if sectheader.shKiểu == 8 {
					ZeroTắcnghẽnVàoTrangThưmục(sectheader.shaddress, cỡ, TrangThưmụcentry)
				} else {
					destination_2 := GetBytefromContrỏ(uintptr(sectheader.shaddress), int(cỡ), int(cỡ))
					ĐặtTắcnghẽnVàoTrangThưmục(sectGiátrị, destination_2, cỡ, TrangThưmụcentry)
				}
			}

			continue

			if EqualByte(sectTên, ([]byte)(".text")) {
				console_2.MIn(".text")
				console_2.MIn("[")
				console_2.MUnsignedinteger32In(sectheader.shaddress)
				console_2.MIn(":")
				console_2.MUnsignedinteger32In(sectheader.shoffset)
				console_2.MIn(":")
				console_2.MUnsignedinteger32In(sectheader.shCỡ)
				console_2.MIn("]")
				copy(mình.nhãn[:sectheader.shCỡ], sectGiátrị[:sectheader.shCỡ])
				mình.nhãnlen = sectheader.shCỡ
			}
			if EqualByte(sectTên, ([]byte)(".rel.text")) {
				console_2.MIn(".rel.text")
				console_2.MIn("[")
				console_2.MUnsignedinteger32In(sectheader.shaddress)
				console_2.MIn(":")
				console_2.MUnsignedinteger32In(sectheader.shCỡ)
				console_2.MIn("]")
				for rt := uint32(0); rt < sectheader.shCỡ/8; rt++ {
					offset := *(*uint32)(Pointer(&sectGiátrị[rt*8]))
					mình.relNhãn[rt].offset = offset
					mình.relNhãn[rt].oaddress = *(*uint32)(Pointer(&mình.nhãn[offset]))
					mình.relNhãn[rt].sỐ = *(*uint32)(Pointer(&sectGiátrị[rt*8+4]))
					mình.relNhãnlen++
				}
			}
			if EqualByte(sectTên, ([]byte)(".dynsym")) {
				console_2.MIn(".dynsym")
				console_2.MIn("[")
				console_2.MUnsignedinteger32In(sectheader.shaddress)
				console_2.MIn(":")
				console_2.MUnsignedinteger32In(sectheader.shCỡ)
				console_2.MIn("]")
				for rt := uint32(0); rt < sectheader.shCỡ/8; rt++ {
					offset := *(*uint32)(Pointer(&sectGiátrị[rt*8]))
					mình.relNhãn[rt].offset = offset
					mình.relNhãn[rt].oaddress = *(*uint32)(Pointer(&mình.nhãn[offset]))
					mình.relNhãn[rt].sỐ = *(*uint32)(Pointer(&sectGiátrị[rt*8+4]))
					mình.relNhãnlen++
				}
			}
			if EqualByte(sectTên, ([]byte)(".dynstr")) {
				console_2.MIn(".dynstr")
				console_2.MIn("[")
				console_2.MUnsignedinteger32In(sectheader.shaddress)
				console_2.MIn(":")
				console_2.MUnsignedinteger32In(sectheader.shCỡ)
				console_2.MIn("]")
			}
			if EqualByte(sectTên, ([]byte)(".strtab")) {
				console_2.MIn(".strtab")
				console_2.MIn("[")
				console_2.MUnsignedinteger32In(sectheader.shaddress)
				console_2.MIn("]")
				rt := uint32(0)
				chạy := uint32(0)

				for st := uint32(1); st < sectheader.shCỡ; st++ {
					if sectGiátrị[st] == 0x0 || sectGiátrị[st] == ' ' {
						funcTên := sectGiátrị[chạy+1 : st]
						console_2.MIn("+")
						console_2.MIn(funcTên)
						mình.strtab[rt] = BytetoCHUỖI(funcTên)
						chạy = st
						rt++
					}
				}

			}

		}

		console_2.MIn(([]byte)("<------------"))
		for rt := uint32(0); rt < mình.relNhãnlen; rt++ {
			console_2.MIn("[")
			console_2.MIn(([]byte)(mình.strtab[rt]))
			console_2.MIn(":")
			console_2.MUnsignedinteger32In(mình.relNhãn[rt].sỐ)
			console_2.MIn(":")

			console_2.MIn(([]byte)("]"))
		}
		console_2.MIn(([]byte)("------------>"))

		if nhãnContrỏ != nil {
			bộnhớmanager.Rảnh(nhãnContrỏ)
		}

	}

}
