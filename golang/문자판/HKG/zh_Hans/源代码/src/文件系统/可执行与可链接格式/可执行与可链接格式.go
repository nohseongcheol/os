package 可执行与可链接格式

import . "unsafe"

import . "控制台"
import . "工具"
import . "内存管理器"
import . "分页管理"

type Elf头部 struct {
	eident		[16]byte
	e类型		uint16
	emachine	uint16
	e版本		uint32
	e条目		uint32
	ephoff		uint32
	eshoff		uint32
	e标志		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elf区段头部 struct {
	sh名称		uint32
	sh类型		uint32
	sh标志		uint32
	shaddress	uint32
	sh位移		uint32
	sh大小		uint32
	sh链接		uint32
	sh信息		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elf程序头部 struct {
	p类型	uint32
	p位移	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	p标志	uint32
	p对齐	uint32
}
type Elf32备忘 struct {
	nnamesz	uint32
	ndescsz	uint32
	n类型	uint32
}
type Elf32dyn struct {
	d标记	uint32
	dval指针	uint32
}
type Elf32rel struct {
	r位移	uint32
	r信息	uint32
}
type Elf32rela struct {
	r位移	uint32
	r信息	uint32
	raddend	uint32
}
type Elf32sym struct {
	st名称	uint32
	st值	uint32
	st大小	uint32
	st信息	uint8
	st其它	uint8
	stshndx	uint16
}
type relocation文本 struct {
	位移		uint32
	数字		uint32
	oaddress	uint32
}
type Elf struct {
	文本		[]byte
	文本len		uint32
	rel文本		[100]relocation文本
	rel文本len	uint32
	strtab		[100]string
	Got		uint32
	D动态		uint32
}

func (self *Elf) Get条目(数据 []byte) uint32 {
	elf头部 := (*Elf头部)(Pointer(&数据[0]))
	return elf头部.e条目
}

func (self *Elf) Parse(数据 []byte, P页目录条目 uint32) {

	内存管理器 := T内存管理器{}
	var 文本指针 Pointer = nil

	var 控制台_2 = T控制台{}

	elf头部 := (*Elf头部)(Pointer(&数据[0]))

	if elf头部.eshnum != 0 {
		strtab := (*Elf区段头部)(Pointer(&数据[elf头部.eshoff+uint32(elf头部.eshentsize*elf头部.eshstrndx)]))
		sect头部大小 := uint32(Sizeof(Elf区段头部{}))

		for i := uint32(0); i < uint32(elf头部.eshnum); i++ {
			sect头部 := (*Elf区段头部)(Pointer(&数据[elf头部.eshoff+sect头部大小*i]))

			var sect名称 []byte
			开始 := uint32(strtab.sh位移 + sect头部.sh名称)
			结尾 := 开始
			for ; ; 结尾++ {
				if 数据[结尾] == 0x0 || 数据[结尾] == ' ' {
					break
				}
			}
			sect名称 = 数据[开始:结尾]

			var sect值 []byte
			if sect头部.sh类型 != 8 {
				结尾位移 := sect头部.sh位移 + sect头部.sh大小
				if 结尾位移 < sect头部.sh位移 || 结尾位移 > uint32(len(数据)) {
					continue
				}
				sect值 = 数据[sect头部.sh位移:结尾位移]
			}

			if E相同字节(sect名称, ([]byte)(".got.plt")) {
				控制台_2.M打印("[")
				控制台_2.M打印(sect名称)
				控制台_2.M打印(":")
				self.Got = sect头部.shaddress
				控制台_2.MUnsignedinteger32打印(self.Got)
				控制台_2.M打印("]")
			}
			if E相同字节(sect名称, ([]byte)(".dynamic")) {
				控制台_2.M打印("[")
				控制台_2.M打印(sect名称)
				控制台_2.M打印(":")
				动态 := sect头部.shaddress
				self.D动态 = 动态
				控制台_2.MUnsignedinteger32打印(动态)
				控制台_2.M打印("]")
			}

			if sect头部.shaddress > 0x1000 {
				大小 := sect头部.sh大小
				if sect头部.sh类型 == 8 {
					Z零块进页目录(sect头部.shaddress, 大小, P页目录条目)
				} else {
					目的_2 := Get字节from指针(uintptr(sect头部.shaddress), int(大小), int(大小))
					S集合块进页目录(sect值, 目的_2, 大小, P页目录条目)
				}
			}

			continue

			if E相同字节(sect名称, ([]byte)(".text")) {
				控制台_2.M打印(".text")
				控制台_2.M打印("[")
				控制台_2.MUnsignedinteger32打印(sect头部.shaddress)
				控制台_2.M打印(":")
				控制台_2.MUnsignedinteger32打印(sect头部.sh位移)
				控制台_2.M打印(":")
				控制台_2.MUnsignedinteger32打印(sect头部.sh大小)
				控制台_2.M打印("]")
				copy(self.文本[:sect头部.sh大小], sect值[:sect头部.sh大小])
				self.文本len = sect头部.sh大小
			}
			if E相同字节(sect名称, ([]byte)(".rel.text")) {
				控制台_2.M打印(".rel.text")
				控制台_2.M打印("[")
				控制台_2.MUnsignedinteger32打印(sect头部.shaddress)
				控制台_2.M打印(":")
				控制台_2.MUnsignedinteger32打印(sect头部.sh大小)
				控制台_2.M打印("]")
				for rt := uint32(0); rt < sect头部.sh大小/8; rt++ {
					位移 := *(*uint32)(Pointer(&sect值[rt*8]))
					self.rel文本[rt].位移 = 位移
					self.rel文本[rt].oaddress = *(*uint32)(Pointer(&self.文本[位移]))
					self.rel文本[rt].数字 = *(*uint32)(Pointer(&sect值[rt*8+4]))
					self.rel文本len++
				}
			}
			if E相同字节(sect名称, ([]byte)(".dynsym")) {
				控制台_2.M打印(".dynsym")
				控制台_2.M打印("[")
				控制台_2.MUnsignedinteger32打印(sect头部.shaddress)
				控制台_2.M打印(":")
				控制台_2.MUnsignedinteger32打印(sect头部.sh大小)
				控制台_2.M打印("]")
				for rt := uint32(0); rt < sect头部.sh大小/8; rt++ {
					位移 := *(*uint32)(Pointer(&sect值[rt*8]))
					self.rel文本[rt].位移 = 位移
					self.rel文本[rt].oaddress = *(*uint32)(Pointer(&self.文本[位移]))
					self.rel文本[rt].数字 = *(*uint32)(Pointer(&sect值[rt*8+4]))
					self.rel文本len++
				}
			}
			if E相同字节(sect名称, ([]byte)(".dynstr")) {
				控制台_2.M打印(".dynstr")
				控制台_2.M打印("[")
				控制台_2.MUnsignedinteger32打印(sect头部.shaddress)
				控制台_2.M打印(":")
				控制台_2.MUnsignedinteger32打印(sect头部.sh大小)
				控制台_2.M打印("]")
			}
			if E相同字节(sect名称, ([]byte)(".strtab")) {
				控制台_2.M打印(".strtab")
				控制台_2.M打印("[")
				控制台_2.MUnsignedinteger32打印(sect头部.shaddress)
				控制台_2.M打印("]")
				rt := uint32(0)
				开始 := uint32(0)

				for st := uint32(1); st < sect头部.sh大小; st++ {
					if sect值[st] == 0x0 || sect值[st] == ' ' {
						func名称 := sect值[开始+1 : st]
						控制台_2.M打印("+")
						控制台_2.M打印(func名称)
						self.strtab[rt] = B字节to字符串(func名称)
						开始 = st
						rt++
					}
				}

			}

		}

		控制台_2.M打印(([]byte)("<------------"))
		for rt := uint32(0); rt < self.rel文本len; rt++ {
			控制台_2.M打印("[")
			控制台_2.M打印(([]byte)(self.strtab[rt]))
			控制台_2.M打印(":")
			控制台_2.MUnsignedinteger32打印(self.rel文本[rt].数字)
			控制台_2.M打印(":")

			控制台_2.M打印(([]byte)("]"))
		}
		控制台_2.M打印(([]byte)("------------>"))

		if 文本指针 != nil {
			内存管理器.F空闲(文本指针)
		}

	}

}
