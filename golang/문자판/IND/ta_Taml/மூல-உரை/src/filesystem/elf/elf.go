package elf

import . "unsafe"

import . "console"
import . "util"
import . "நினைவகம்"
import . "paging"

type ElfHeader struct {
	e_ident		[16]byte
	e_type		uint16
	e_machine	uint16
	e_version	uint32
	e_entry		uint32
	e_phoff		uint32
	e_shoff		uint32
	e_flags		uint32
	e_ehsize		uint16
	e_phentsize	uint16
	e_phnum		uint16
	e_shentsize	uint16
	e_shnum		uint16
	e_shstrndx	uint16
}
type ElfSectionHeader struct {
	sh_name		uint32
	sh_type		uint32
	sh_flags		uint32
	sh_addr	uint32
	sh_offset	uint32
	sh_size		uint32
	sh_link		uint32
	sh_info		uint32
	sh_addralign	uint32
	sh_entsize	uint32
}
type ElfProgramHeader struct {
	p_type	uint32
	p_offset	uint32
	p_vaddr	uint32
	p_paddr	uint32
	p_filesz	uint32
	p_memsz	uint32
	p_flags	uint32
	p_align	uint32
}
type Elf32Note struct {
	n_namesz	uint32
	n_descsz	uint32
	n_type	uint32
}
type Elf32Dyn struct {
	d_tag		uint32
	d_val_ptr	uint32
}
type Elf32Rel struct {
	r_offset	uint32
	r_info	uint32
}
type Elf32Rela struct {
	r_offset	uint32
	r_info	uint32
	r_addend	uint32
}
type Elf32Sym struct {
	st_name	uint32
	st_value	uint32
	st_size	uint32
	st_info	uint8
	st_other	uint8
	st_shndx	uint16
}
type relocation_text struct {
	offset		uint32
	num		uint32
	o_addr	uint32
}
type Elf struct {
	text		[]byte
	text_len		uint32
	rel_text		[100]relocation_text
	rel_text_len	uint32
	strtab		[100]string
	GOT		uint32
	Dynamic		uint32
}

func (self *Elf) GetEntry(data []byte) uint32 {
	elfHeader := (*ElfHeader)(Pointer(&data[0]))
	return elfHeader.e_entry
}

func (self *Elf) Parse(data []byte, PageDirEntry uint32) {

	memoryManager := TMemoryManager{}
	var textPtr Pointer = nil

	var 콘솔 = T콘솔{}

	elfHeader := (*ElfHeader)(Pointer(&data[0]))

	if elfHeader.e_shnum != 0 {
		strtab := (*ElfSectionHeader)(Pointer(&data[elfHeader.e_shoff+uint32(elfHeader.e_shentsize*elfHeader.e_shstrndx)]))
		sectHeaderSize := uint32(Sizeof(ElfSectionHeader{}))

		for i := uint32(0); i < uint32(elfHeader.e_shnum); i++ {
			sectHeader := (*ElfSectionHeader)(Pointer(&data[elfHeader.e_shoff+sectHeaderSize*i]))

			var sectName []byte
			start := uint32(strtab.sh_offset + sectHeader.sh_name)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectName = data[start:end]

			var sectValue []byte
			if sectHeader.sh_type != 8 {
				endOffset := sectHeader.sh_offset + sectHeader.sh_size
				if endOffset < sectHeader.sh_offset || endOffset > uint32(len(data)) {
					continue
				}
				sectValue = data[sectHeader.sh_offset:endOffset]
			}

			if EqualBytes(sectName, ([]byte)(".got.plt")) {
				콘솔.M출력("[")
				콘솔.M출력(sectName)
				콘솔.M출력(":")
				self.GOT = sectHeader.sh_addr
				콘솔.MUint32출력(self.GOT)
				콘솔.M출력("]")
			}
			if EqualBytes(sectName, ([]byte)(".dynamic")) {
				콘솔.M출력("[")
				콘솔.M출력(sectName)
				콘솔.M출력(":")
				dynamic := sectHeader.sh_addr
				self.Dynamic = dynamic
				콘솔.MUint32출력(dynamic)
				콘솔.M출력("]")
			}

			if sectHeader.sh_addr > 0x1000 {
				அளவு := sectHeader.sh_size
				if sectHeader.sh_type == 8 {
					ZeroBlockInPageDir(sectHeader.sh_addr, அளவு, PageDirEntry)
				} else {
					dst := GetBytesFromPtr(uintptr(sectHeader.sh_addr), int(அளவு), int(அளவு))
					SetBlockInPageDir(sectValue, dst, அளவு, PageDirEntry)
				}
			}

			continue

			if EqualBytes(sectName, ([]byte)(".text")) {
				콘솔.M출력(".text")
				콘솔.M출력("[")
				콘솔.MUint32출력(sectHeader.sh_addr)
				콘솔.M출력(":")
				콘솔.MUint32출력(sectHeader.sh_offset)
				콘솔.M출력(":")
				콘솔.MUint32출력(sectHeader.sh_size)
				콘솔.M출력("]")
				copy(self.text[:sectHeader.sh_size], sectValue[:sectHeader.sh_size])
				self.text_len = sectHeader.sh_size
			}
			if EqualBytes(sectName, ([]byte)(".rel.text")) {
				콘솔.M출력(".rel.text")
				콘솔.M출력("[")
				콘솔.MUint32출력(sectHeader.sh_addr)
				콘솔.M출력(":")
				콘솔.MUint32출력(sectHeader.sh_size)
				콘솔.M출력("]")
				for rt := uint32(0); rt < sectHeader.sh_size/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValue[rt*8]))
					self.rel_text[rt].offset = offset
					self.rel_text[rt].o_addr = *(*uint32)(Pointer(&self.text[offset]))
					self.rel_text[rt].num = *(*uint32)(Pointer(&sectValue[rt*8+4]))
					self.rel_text_len++
				}
			}
			if EqualBytes(sectName, ([]byte)(".dynsym")) {
				콘솔.M출력(".dynsym")
				콘솔.M출력("[")
				콘솔.MUint32출력(sectHeader.sh_addr)
				콘솔.M출력(":")
				콘솔.MUint32출력(sectHeader.sh_size)
				콘솔.M출력("]")
				for rt := uint32(0); rt < sectHeader.sh_size/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValue[rt*8]))
					self.rel_text[rt].offset = offset
					self.rel_text[rt].o_addr = *(*uint32)(Pointer(&self.text[offset]))
					self.rel_text[rt].num = *(*uint32)(Pointer(&sectValue[rt*8+4]))
					self.rel_text_len++
				}
			}
			if EqualBytes(sectName, ([]byte)(".dynstr")) {
				콘솔.M출력(".dynstr")
				콘솔.M출력("[")
				콘솔.MUint32출력(sectHeader.sh_addr)
				콘솔.M출력(":")
				콘솔.MUint32출력(sectHeader.sh_size)
				콘솔.M출력("]")
			}
			if EqualBytes(sectName, ([]byte)(".strtab")) {
				콘솔.M출력(".strtab")
				콘솔.M출력("[")
				콘솔.MUint32출력(sectHeader.sh_addr)
				콘솔.M출력("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectHeader.sh_size; st++ {
					if sectValue[st] == 0x0 || sectValue[st] == ' ' {
						func_name := sectValue[start+1 : st]
						콘솔.M출력("+")
						콘솔.M출력(func_name)
						self.strtab[rt] = BytesToString(func_name)
						start = st
						rt++
					}
				}

			}

		}

		콘솔.M출력(([]byte)("<------------"))
		for rt := uint32(0); rt < self.rel_text_len; rt++ {
			콘솔.M출력("[")
			콘솔.M출력(([]byte)(self.strtab[rt]))
			콘솔.M출력(":")
			콘솔.MUint32출력(self.rel_text[rt].num)
			콘솔.M출력(":")

			콘솔.M출력(([]byte)("]"))
		}
		콘솔.M출력(([]byte)("------------>"))

		if textPtr != nil {
			memoryManager.Vநினைவகத்தை_விடுவி(textPtr)
		}

	}

}
