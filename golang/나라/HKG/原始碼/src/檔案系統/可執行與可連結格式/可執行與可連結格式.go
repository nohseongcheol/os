package 可執行與可連結格式

import . "unsafe"

import . "控制台"
import . "工具"
import . "記憶體管理器"
import . "分頁管理"

type Elf標頭 struct {
	eident		[16]byte
	e類型		uint16
	emachine	uint16
	e版本		uint32
	e項目		uint32
	ephoff		uint32
	eshoff		uint32
	e旗標		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elf區段標頭 struct {
	sh名稱		uint32
	sh類型		uint32
	sh旗標		uint32
	shaddress	uint32
	sh位移		uint32
	sh大小		uint32
	sh連結		uint32
	sh資訊		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elf程式標頭 struct {
	p類型	uint32
	p位移	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	p旗標	uint32
	p對齊	uint32
}
type Elf32備註 struct {
	nnamesz	uint32
	ndescsz	uint32
	n類型	uint32
}
type Elf32dyn struct {
	d標籤	uint32
	dval指標	uint32
}
type Elf32rel struct {
	r位移	uint32
	r資訊	uint32
}
type Elf32rela struct {
	r位移	uint32
	r資訊	uint32
	raddend	uint32
}
type Elf32sym struct {
	st名稱	uint32
	st數值	uint32
	st大小	uint32
	st資訊	uint8
	st其他	uint8
	stshndx	uint16
}
type relocation文字 struct {
	位移		uint32
	數字		uint32
	oaddress	uint32
}
type Elf struct {
	文字		[]byte
	文字len		uint32
	rel文字		[100]relocation文字
	rel文字len	uint32
	strtab		[100]string
	Got		uint32
	D動態		uint32
}

func (self *Elf) Get項目(資料 []byte) uint32 {
	elf標頭 := (*Elf標頭)(Pointer(&資料[0]))
	return elf標頭.e項目
}

func (self *Elf) Parse(資料 []byte, P頁目錄項目 uint32) {

	記憶體管理器 := T記憶體管理器{}
	var 文字指標 Pointer = nil

	var 控制台_2 = T控制台{}

	elf標頭 := (*Elf標頭)(Pointer(&資料[0]))

	if elf標頭.eshnum != 0 {
		strtab := (*Elf區段標頭)(Pointer(&資料[elf標頭.eshoff+uint32(elf標頭.eshentsize*elf標頭.eshstrndx)]))
		sect標頭大小 := uint32(Sizeof(Elf區段標頭{}))

		for i := uint32(0); i < uint32(elf標頭.eshnum); i++ {
			sect標頭 := (*Elf區段標頭)(Pointer(&資料[elf標頭.eshoff+sect標頭大小*i]))

			var sect名稱 []byte
			啟動 := uint32(strtab.sh位移 + sect標頭.sh名稱)
			結束 := 啟動
			for ; ; 結束++ {
				if 資料[結束] == 0x0 || 資料[結束] == ' ' {
					break
				}
			}
			sect名稱 = 資料[啟動:結束]

			var sect數值 []byte
			if sect標頭.sh類型 != 8 {
				結束位移 := sect標頭.sh位移 + sect標頭.sh大小
				if 結束位移 < sect標頭.sh位移 || 結束位移 > uint32(len(資料)) {
					continue
				}
				sect數值 = 資料[sect標頭.sh位移:結束位移]
			}

			if E相等位元組(sect名稱, ([]byte)(".got.plt")) {
				控制台_2.M列印("[")
				控制台_2.M列印(sect名稱)
				控制台_2.M列印(":")
				self.Got = sect標頭.shaddress
				控制台_2.MUnsignedinteger32列印(self.Got)
				控制台_2.M列印("]")
			}
			if E相等位元組(sect名稱, ([]byte)(".dynamic")) {
				控制台_2.M列印("[")
				控制台_2.M列印(sect名稱)
				控制台_2.M列印(":")
				動態 := sect標頭.shaddress
				self.D動態 = 動態
				控制台_2.MUnsignedinteger32列印(動態)
				控制台_2.M列印("]")
			}

			if sect標頭.shaddress > 0x1000 {
				大小 := sect標頭.sh大小
				if sect標頭.sh類型 == 8 {
					Z零區塊進頁目錄(sect標頭.shaddress, 大小, P頁目錄項目)
				} else {
					目的地_2 := Get位元組from指標(uintptr(sect標頭.shaddress), int(大小), int(大小))
					S設定區塊進頁目錄(sect數值, 目的地_2, 大小, P頁目錄項目)
				}
			}

			continue

			if E相等位元組(sect名稱, ([]byte)(".text")) {
				控制台_2.M列印(".text")
				控制台_2.M列印("[")
				控制台_2.MUnsignedinteger32列印(sect標頭.shaddress)
				控制台_2.M列印(":")
				控制台_2.MUnsignedinteger32列印(sect標頭.sh位移)
				控制台_2.M列印(":")
				控制台_2.MUnsignedinteger32列印(sect標頭.sh大小)
				控制台_2.M列印("]")
				copy(self.文字[:sect標頭.sh大小], sect數值[:sect標頭.sh大小])
				self.文字len = sect標頭.sh大小
			}
			if E相等位元組(sect名稱, ([]byte)(".rel.text")) {
				控制台_2.M列印(".rel.text")
				控制台_2.M列印("[")
				控制台_2.MUnsignedinteger32列印(sect標頭.shaddress)
				控制台_2.M列印(":")
				控制台_2.MUnsignedinteger32列印(sect標頭.sh大小)
				控制台_2.M列印("]")
				for rt := uint32(0); rt < sect標頭.sh大小/8; rt++ {
					位移 := *(*uint32)(Pointer(&sect數值[rt*8]))
					self.rel文字[rt].位移 = 位移
					self.rel文字[rt].oaddress = *(*uint32)(Pointer(&self.文字[位移]))
					self.rel文字[rt].數字 = *(*uint32)(Pointer(&sect數值[rt*8+4]))
					self.rel文字len++
				}
			}
			if E相等位元組(sect名稱, ([]byte)(".dynsym")) {
				控制台_2.M列印(".dynsym")
				控制台_2.M列印("[")
				控制台_2.MUnsignedinteger32列印(sect標頭.shaddress)
				控制台_2.M列印(":")
				控制台_2.MUnsignedinteger32列印(sect標頭.sh大小)
				控制台_2.M列印("]")
				for rt := uint32(0); rt < sect標頭.sh大小/8; rt++ {
					位移 := *(*uint32)(Pointer(&sect數值[rt*8]))
					self.rel文字[rt].位移 = 位移
					self.rel文字[rt].oaddress = *(*uint32)(Pointer(&self.文字[位移]))
					self.rel文字[rt].數字 = *(*uint32)(Pointer(&sect數值[rt*8+4]))
					self.rel文字len++
				}
			}
			if E相等位元組(sect名稱, ([]byte)(".dynstr")) {
				控制台_2.M列印(".dynstr")
				控制台_2.M列印("[")
				控制台_2.MUnsignedinteger32列印(sect標頭.shaddress)
				控制台_2.M列印(":")
				控制台_2.MUnsignedinteger32列印(sect標頭.sh大小)
				控制台_2.M列印("]")
			}
			if E相等位元組(sect名稱, ([]byte)(".strtab")) {
				控制台_2.M列印(".strtab")
				控制台_2.M列印("[")
				控制台_2.MUnsignedinteger32列印(sect標頭.shaddress)
				控制台_2.M列印("]")
				rt := uint32(0)
				啟動 := uint32(0)

				for st := uint32(1); st < sect標頭.sh大小; st++ {
					if sect數值[st] == 0x0 || sect數值[st] == ' ' {
						func名稱 := sect數值[啟動+1 : st]
						控制台_2.M列印("+")
						控制台_2.M列印(func名稱)
						self.strtab[rt] = B位元組to字串(func名稱)
						啟動 = st
						rt++
					}
				}

			}

		}

		控制台_2.M列印(([]byte)("<------------"))
		for rt := uint32(0); rt < self.rel文字len; rt++ {
			控制台_2.M列印("[")
			控制台_2.M列印(([]byte)(self.strtab[rt]))
			控制台_2.M列印(":")
			控制台_2.MUnsignedinteger32列印(self.rel文字[rt].數字)
			控制台_2.M列印(":")

			控制台_2.M列印(([]byte)("]"))
		}
		控制台_2.M列印(([]byte)("------------>"))

		if 文字指標 != nil {
			記憶體管理器.F剩餘(文字指標)
		}

	}

}
