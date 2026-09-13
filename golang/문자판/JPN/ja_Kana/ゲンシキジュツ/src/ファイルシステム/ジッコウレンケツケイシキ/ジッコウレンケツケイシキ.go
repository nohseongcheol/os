package ジッコウレンケツケイシキ

import . "unsafe"

import . "コンソール"
import . "ハンヨウ"
import . "メモリカンリシャ"
import . "ページカンリ"

type Elfヘッダ struct {
	eident		[16]byte
	eカタ		uint16
	emachine	uint16
	eバージョン		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eフラグ		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfクカクヘッダ struct {
	shナマエ		uint32
	shカタ		uint32
	shフラグ		uint32
	shaddress	uint32
	shoffset	uint32
	shサイズ		uint32
	shレンケツ		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfプログラムヘッダ struct {
	pカタ	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pフラグ	uint32
	pセイレツ	uint32
}
type Elf32ビコウ struct {
	nnamesz	uint32
	ndescsz	uint32
	nカタ	uint32
}
type Elf32dyn struct {
	dタグ		uint32
	dvalポインタ	uint32
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
	stナマエ	uint32
	stアタイ	uint32
	stサイズ	uint32
	stinfo	uint8
	stソノホカ	uint8
	stshndx	uint16
}
type relocationテキスト struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	テキスト		[]byte
	テキストlen		uint32
	relテキスト		[100]relocationテキスト
	relテキストlen	uint32
	strtab		[100]string
	Got		uint32
	Dドウテキニ		uint32
}

func (self *Elf) Getentry(データ []byte) uint32 {
	elfヘッダ := (*Elfヘッダ)(Pointer(&データ[0]))
	return elfヘッダ.eentry
}

func (self *Elf) Parse(データ []byte, Pページディレクトリentry uint32) {

	メモリカンリシャ := Tメモリカンリシャ{}
	var テキストポインタ Pointer = nil

	var コンソール_2 = Tコンソール{}

	elfヘッダ := (*Elfヘッダ)(Pointer(&データ[0]))

	if elfヘッダ.eshnum != 0 {
		strtab := (*Elfクカクヘッダ)(Pointer(&データ[elfヘッダ.eshoff+uint32(elfヘッダ.eshentsize*elfヘッダ.eshstrndx)]))
		sectヘッダサイズ := uint32(Sizeof(Elfクカクヘッダ{}))

		for i := uint32(0); i < uint32(elfヘッダ.eshnum); i++ {
			sectヘッダ := (*Elfクカクヘッダ)(Pointer(&データ[elfヘッダ.eshoff+sectヘッダサイズ*i]))

			var sectナマエ []byte
			カイシ := uint32(strtab.shoffset + sectヘッダ.shナマエ)
			ブンマツ := カイシ
			for ; ; ブンマツ++ {
				if データ[ブンマツ] == 0x0 || データ[ブンマツ] == ' ' {
					break
				}
			}
			sectナマエ = データ[カイシ:ブンマツ]

			var sectアタイ []byte
			if sectヘッダ.shカタ != 8 {
				ブンマツoffset := sectヘッダ.shoffset + sectヘッダ.shサイズ
				if ブンマツoffset < sectヘッダ.shoffset || ブンマツoffset > uint32(len(データ)) {
					continue
				}
				sectアタイ = データ[sectヘッダ.shoffset:ブンマツoffset]
			}

			if Eスベテオナジバイト(sectナマエ, ([]byte)(".got.plt")) {
				コンソール_2.Mインサツ("[")
				コンソール_2.Mインサツ(sectナマエ)
				コンソール_2.Mインサツ(":")
				self.Got = sectヘッダ.shaddress
				コンソール_2.MUnsignedinteger32インサツ(self.Got)
				コンソール_2.Mインサツ("]")
			}
			if Eスベテオナジバイト(sectナマエ, ([]byte)(".dynamic")) {
				コンソール_2.Mインサツ("[")
				コンソール_2.Mインサツ(sectナマエ)
				コンソール_2.Mインサツ(":")
				ドウテキニ := sectヘッダ.shaddress
				self.Dドウテキニ = ドウテキニ
				コンソール_2.MUnsignedinteger32インサツ(ドウテキニ)
				コンソール_2.Mインサツ("]")
			}

			if sectヘッダ.shaddress > 0x1000 {
				サイズ := sectヘッダ.shサイズ
				if sectヘッダ.shカタ == 8 {
					Zスウチノ0ブロックジュシンページディレクトリ(sectヘッダ.shaddress, サイズ, Pページディレクトリentry)
				} else {
					テンソウサキ_2 := Getバイトカラポインタ(uintptr(sectヘッダ.shaddress), int(サイズ), int(サイズ))
					Sアリブロックジュシンページディレクトリ(sectアタイ, テンソウサキ_2, サイズ, Pページディレクトリentry)
				}
			}

			continue

			if Eスベテオナジバイト(sectナマエ, ([]byte)(".text")) {
				コンソール_2.Mインサツ(".text")
				コンソール_2.Mインサツ("[")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shaddress)
				コンソール_2.Mインサツ(":")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shoffset)
				コンソール_2.Mインサツ(":")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shサイズ)
				コンソール_2.Mインサツ("]")
				copy(self.テキスト[:sectヘッダ.shサイズ], sectアタイ[:sectヘッダ.shサイズ])
				self.テキストlen = sectヘッダ.shサイズ
			}
			if Eスベテオナジバイト(sectナマエ, ([]byte)(".rel.text")) {
				コンソール_2.Mインサツ(".rel.text")
				コンソール_2.Mインサツ("[")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shaddress)
				コンソール_2.Mインサツ(":")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shサイズ)
				コンソール_2.Mインサツ("]")
				for rt := uint32(0); rt < sectヘッダ.shサイズ/8; rt++ {
					offset := *(*uint32)(Pointer(&sectアタイ[rt*8]))
					self.relテキスト[rt].offset = offset
					self.relテキスト[rt].oaddress = *(*uint32)(Pointer(&self.テキスト[offset]))
					self.relテキスト[rt].number = *(*uint32)(Pointer(&sectアタイ[rt*8+4]))
					self.relテキストlen++
				}
			}
			if Eスベテオナジバイト(sectナマエ, ([]byte)(".dynsym")) {
				コンソール_2.Mインサツ(".dynsym")
				コンソール_2.Mインサツ("[")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shaddress)
				コンソール_2.Mインサツ(":")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shサイズ)
				コンソール_2.Mインサツ("]")
				for rt := uint32(0); rt < sectヘッダ.shサイズ/8; rt++ {
					offset := *(*uint32)(Pointer(&sectアタイ[rt*8]))
					self.relテキスト[rt].offset = offset
					self.relテキスト[rt].oaddress = *(*uint32)(Pointer(&self.テキスト[offset]))
					self.relテキスト[rt].number = *(*uint32)(Pointer(&sectアタイ[rt*8+4]))
					self.relテキストlen++
				}
			}
			if Eスベテオナジバイト(sectナマエ, ([]byte)(".dynstr")) {
				コンソール_2.Mインサツ(".dynstr")
				コンソール_2.Mインサツ("[")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shaddress)
				コンソール_2.Mインサツ(":")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shサイズ)
				コンソール_2.Mインサツ("]")
			}
			if Eスベテオナジバイト(sectナマエ, ([]byte)(".strtab")) {
				コンソール_2.Mインサツ(".strtab")
				コンソール_2.Mインサツ("[")
				コンソール_2.MUnsignedinteger32インサツ(sectヘッダ.shaddress)
				コンソール_2.Mインサツ("]")
				rt := uint32(0)
				カイシ := uint32(0)

				for st := uint32(1); st < sectヘッダ.shサイズ; st++ {
					if sectアタイ[st] == 0x0 || sectアタイ[st] == ' ' {
						funcナマエ := sectアタイ[カイシ+1 : st]
						コンソール_2.Mインサツ("+")
						コンソール_2.Mインサツ(funcナマエ)
						self.strtab[rt] = Bバイトtoモジレツ(funcナマエ)
						カイシ = st
						rt++
					}
				}

			}

		}

		コンソール_2.Mインサツ(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relテキストlen; rt++ {
			コンソール_2.Mインサツ("[")
			コンソール_2.Mインサツ(([]byte)(self.strtab[rt]))
			コンソール_2.Mインサツ(":")
			コンソール_2.MUnsignedinteger32インサツ(self.relテキスト[rt].number)
			コンソール_2.Mインサツ(":")

			コンソール_2.Mインサツ(([]byte)("]"))
		}
		コンソール_2.Mインサツ(([]byte)("------------>"))

		if テキストポインタ != nil {
			メモリカンリシャ.Fアキ(テキストポインタ)
		}

	}

}
