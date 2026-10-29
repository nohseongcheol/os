/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 実行連結形式

import . "unsafe"

import . "コンソール"
import . "汎用"
import . "メモリ管理者"
import . "ページ管理"

type Elfヘッダ struct {
	eident		[16]byte
	e型		uint16
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
type Elf区画ヘッダ struct {
	sh名前		uint32
	sh型		uint32
	shフラグ		uint32
	shaddress	uint32
	shoffset	uint32
	shサイズ		uint32
	sh連結		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfプログラムヘッダ struct {
	p型	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pフラグ	uint32
	p整列	uint32
}
type Elf32備考 struct {
	nnamesz	uint32
	ndescsz	uint32
	n型	uint32
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
	st名前	uint32
	st値	uint32
	stサイズ	uint32
	stinfo	uint8
	stその他	uint8
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
	D動的に		uint32
}

func (self *Elf) Getentry(データ []byte) uint32 {
	elfヘッダ := (*Elfヘッダ)(Pointer(&データ[0]))
	return elfヘッダ.eentry
}

func (self *Elf) Parse(データ []byte, Pページディレクトリentry uint32) {

	メモリ管理者 := Tメモリ管理者{}
	var テキストポインタ Pointer = nil

	var コンソール_2 = Tコンソール{}

	elfヘッダ := (*Elfヘッダ)(Pointer(&データ[0]))

	if elfヘッダ.eshnum != 0 {
		strtab := (*Elf区画ヘッダ)(Pointer(&データ[elfヘッダ.eshoff+uint32(elfヘッダ.eshentsize*elfヘッダ.eshstrndx)]))
		sectヘッダサイズ := uint32(Sizeof(Elf区画ヘッダ{}))

		for i := uint32(0); i < uint32(elfヘッダ.eshnum); i++ {
			sectヘッダ := (*Elf区画ヘッダ)(Pointer(&データ[elfヘッダ.eshoff+sectヘッダサイズ*i]))

			var sect名前 []byte
			開始 := uint32(strtab.shoffset + sectヘッダ.sh名前)
			文末 := 開始
			for ; ; 文末++ {
				if データ[文末] == 0x0 || データ[文末] == ' ' {
					break
				}
			}
			sect名前 = データ[開始:文末]

			var sect値 []byte
			if sectヘッダ.sh型 != 8 {
				文末offset := sectヘッダ.shoffset + sectヘッダ.shサイズ
				if 文末offset < sectヘッダ.shoffset || 文末offset > uint32(len(データ)) {
					continue
				}
				sect値 = データ[sectヘッダ.shoffset:文末offset]
			}

			if Eすべて同じバイト(sect名前, ([]byte)(".got.plt")) {
				コンソール_2.M印刷("[")
				コンソール_2.M印刷(sect名前)
				コンソール_2.M印刷(":")
				self.Got = sectヘッダ.shaddress
				コンソール_2.MUnsignedinteger32印刷(self.Got)
				コンソール_2.M印刷("]")
			}
			if Eすべて同じバイト(sect名前, ([]byte)(".dynamic")) {
				コンソール_2.M印刷("[")
				コンソール_2.M印刷(sect名前)
				コンソール_2.M印刷(":")
				動的に := sectヘッダ.shaddress
				self.D動的に = 動的に
				コンソール_2.MUnsignedinteger32印刷(動的に)
				コンソール_2.M印刷("]")
			}

			if sectヘッダ.shaddress > 0x1000 {
				サイズ := sectヘッダ.shサイズ
				if sectヘッダ.sh型 == 8 {
					Z数値の0ブロック受信ページディレクトリ(sectヘッダ.shaddress, サイズ, Pページディレクトリentry)
				} else {
					転送先_2 := Getバイトからポインタ(uintptr(sectヘッダ.shaddress), int(サイズ), int(サイズ))
					Sありブロック受信ページディレクトリ(sect値, 転送先_2, サイズ, Pページディレクトリentry)
				}
			}

			continue

			if Eすべて同じバイト(sect名前, ([]byte)(".text")) {
				コンソール_2.M印刷(".text")
				コンソール_2.M印刷("[")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shaddress)
				コンソール_2.M印刷(":")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shoffset)
				コンソール_2.M印刷(":")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shサイズ)
				コンソール_2.M印刷("]")
				copy(self.テキスト[:sectヘッダ.shサイズ], sect値[:sectヘッダ.shサイズ])
				self.テキストlen = sectヘッダ.shサイズ
			}
			if Eすべて同じバイト(sect名前, ([]byte)(".rel.text")) {
				コンソール_2.M印刷(".rel.text")
				コンソール_2.M印刷("[")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shaddress)
				コンソール_2.M印刷(":")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shサイズ)
				コンソール_2.M印刷("]")
				for rt := uint32(0); rt < sectヘッダ.shサイズ/8; rt++ {
					offset := *(*uint32)(Pointer(&sect値[rt*8]))
					self.relテキスト[rt].offset = offset
					self.relテキスト[rt].oaddress = *(*uint32)(Pointer(&self.テキスト[offset]))
					self.relテキスト[rt].number = *(*uint32)(Pointer(&sect値[rt*8+4]))
					self.relテキストlen++
				}
			}
			if Eすべて同じバイト(sect名前, ([]byte)(".dynsym")) {
				コンソール_2.M印刷(".dynsym")
				コンソール_2.M印刷("[")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shaddress)
				コンソール_2.M印刷(":")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shサイズ)
				コンソール_2.M印刷("]")
				for rt := uint32(0); rt < sectヘッダ.shサイズ/8; rt++ {
					offset := *(*uint32)(Pointer(&sect値[rt*8]))
					self.relテキスト[rt].offset = offset
					self.relテキスト[rt].oaddress = *(*uint32)(Pointer(&self.テキスト[offset]))
					self.relテキスト[rt].number = *(*uint32)(Pointer(&sect値[rt*8+4]))
					self.relテキストlen++
				}
			}
			if Eすべて同じバイト(sect名前, ([]byte)(".dynstr")) {
				コンソール_2.M印刷(".dynstr")
				コンソール_2.M印刷("[")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shaddress)
				コンソール_2.M印刷(":")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shサイズ)
				コンソール_2.M印刷("]")
			}
			if Eすべて同じバイト(sect名前, ([]byte)(".strtab")) {
				コンソール_2.M印刷(".strtab")
				コンソール_2.M印刷("[")
				コンソール_2.MUnsignedinteger32印刷(sectヘッダ.shaddress)
				コンソール_2.M印刷("]")
				rt := uint32(0)
				開始 := uint32(0)

				for st := uint32(1); st < sectヘッダ.shサイズ; st++ {
					if sect値[st] == 0x0 || sect値[st] == ' ' {
						func名前 := sect値[開始+1 : st]
						コンソール_2.M印刷("+")
						コンソール_2.M印刷(func名前)
						self.strtab[rt] = Bバイトto文字列(func名前)
						開始 = st
						rt++
					}
				}

			}

		}

		コンソール_2.M印刷(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relテキストlen; rt++ {
			コンソール_2.M印刷("[")
			コンソール_2.M印刷(([]byte)(self.strtab[rt]))
			コンソール_2.M印刷(":")
			コンソール_2.MUnsignedinteger32印刷(self.relテキスト[rt].number)
			コンソール_2.M印刷(":")

			コンソール_2.M印刷(([]byte)("]"))
		}
		コンソール_2.M印刷(([]byte)("------------>"))

		if テキストポインタ != nil {
			メモリ管理者.F空き(テキストポインタ)
		}

	}

}
