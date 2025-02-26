package elf

import . "unsafe"

import . "콘솔"
import . "util"

type ElfHeader struct{
	e_ident [16]byte
	e_type uint16
	e_machine uint16
	e_version uint32
	e_entry uint32
	e_phoff uint32
	e_shoff uint32
	e_flags uint32
	e_ehsize uint16
	e_phentsize uint16
	e_phnum uint16
	e_shentsize uint16
	e_shnum uint16
	e_shstrndx uint16
}
type ElfSectionHeader struct{
	sh_name uint32
	sh_type uint32
	sh_flags uint32
	sh_addr uint32
	sh_offset uint32
	sh_size uint32
	sh_link uint32
	sh_info uint32
	sh_addralign uint32
	sh_entsize uint32
}
type ElfProgramHeader struct{
	p_type uint32
	p_offset uint32
	p_vaddr uint32
	p_paddr uint32
	p_filesz uint32
	p_memsz uint32
	p_flags uint32
	p_align uint32
}
type rel_test_section struct{
	offset uint32
	num uint32
	o_addr uint32
}
type strtab_section struct{
	num uint32
	func_name string
}
type Elf struct{
	text [4096]byte
	text_len uint32
	rel_text [100]rel_test_section
	rel_text_len uint32
	strtab [100] strtab_section
	strtab_len uint32
}

func (self *Elf) Parse(data []byte, 함수map map[string] uintptr, code *[4096]byte){

	콘솔 := T콘솔{}

	elfHeader := (*ElfHeader)(Pointer(&data[0]))


	if elfHeader.e_shnum != 0 {
		strtab := (*ElfSectionHeader)(Pointer(&data[elfHeader.e_shoff+uint32(elfHeader.e_shentsize*elfHeader.e_shstrndx)]))
		sectHeaderSize := uint32(Sizeof(ElfSectionHeader{}))
		for i:=uint32(0); i<uint32(elfHeader.e_shnum); i++{
			sectHeader := (*ElfSectionHeader)(Pointer(&data[elfHeader.e_shoff + sectHeaderSize*i]))

			var sectName []byte
			start := uint32(strtab.sh_offset+sectHeader.sh_name)
			end := start
			for ; ;end++{
				if data[end] == 0x0 || data[end] == ' '{
					break
				}
			}
			sectName = data[start:end]

			sectValue := data[sectHeader.sh_offset:sectHeader.sh_offset+sectHeader.sh_size]

			if EqualBytes(sectName, ([]byte)(".text")) {
				copy(self.text[:sectHeader.sh_size], sectValue[:sectHeader.sh_size])
				self.text_len = sectHeader.sh_size
			}
			if EqualBytes(sectName, ([]byte)(".rel.text")){

				rt := uint32(0)
				for i:=uint32(0); i<sectHeader.sh_size/8; i++ {
					offset := *(*uint32)(Pointer(&sectValue[i*8]))
					self.rel_text[rt].offset = offset
					self.rel_text[rt].o_addr = *(*uint32)(Pointer(&self.text[offset]))
					self.rel_text[rt].num = *(*uint32)(Pointer(&sectValue[i*8+4]))
					콘솔.M출력("[")
					콘솔.MUint32출력(self.rel_text[rt].num)
					콘솔.M출력(":")
					if (self.rel_text[rt].num & 0xF) == 2{
						콘솔.MUint32출력(self.rel_text[rt].num & 0xF)
						self.rel_text_len++
						rt++
					}
					콘솔.M출력("]")
				}
			}
			if EqualBytes(sectName, ([]byte)(".strtab")){

				rt := uint32(0)
				start := uint32(0)

				for st:=uint32(1); st<sectHeader.sh_size; st++{
					if sectValue[st] == 0x0 || sectValue[st] == ' ' {
						func_name := sectValue[start+1:st]
						self.strtab[rt].func_name = BytesToString(func_name)
						self.strtab[rt].num = 0x100*rt + 0x400 + 0x2
						self.strtab_len++
						start = st
						rt++
					}
				}

			}

		}


		실행코드_주소, cok := 함수map["실행코드_주소"]
		if !cok {
			콘솔.M출력("not c exist")
			return 
		}else{
			콘솔.M출력("[code addr : ")
			콘솔.MUint32출력(uint32(실행코드_주소))
			콘솔.M출력("]")
		}

		for rt:=uint32(0); rt<self.rel_text_len; rt++{

			var func_name string

			for st:=uint32(0); st<self.strtab_len; st++{
				if self.rel_text[rt].num == self.strtab[st].num{
					func_name = self.strtab[st].func_name
					break
				}
			}
			//kfunc_addr, kok := 함수map[self.strtab[rt].func_name]
			kfunc_addr, kok := 함수map[func_name]
			if !kok {
				콘솔.M출력(([]byte)("not k exist"))
			}else{
				//콘솔.MUint32출력(uint32(kfunc_addr))
			}

			diff := uint32(kfunc_addr - 실행코드_주소 - uintptr(self.rel_text[rt].offset - self.rel_text[rt].o_addr)) 
			diff_addr := Uint32ToArray(diff)
			for i:=uint32(0); i<4; i++{
				self.text[self.rel_text[rt].offset+i] = diff_addr[i]
			}
		}

		for t:=uint32(0); t<self.text_len; t++{
			code[t] = self.text[t]
		}
	}
}
