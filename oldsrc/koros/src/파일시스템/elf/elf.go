package elf

import . "unsafe"

import . "단말기"
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
type relocation_text struct{
	offset uint32
	num uint32
	o_addr uint32
}
type Elf struct{
	text [4096]byte
	text_len uint32
	rel_text [100]relocation_text
	rel_text_len uint32
	strtab [100] string
}
func (self *Elf) MTest(){
}
func (self *Elf) Parse(data []byte, func_map map[string] uintptr, code *[4096]byte){

	var 단말기  = T단말기{}	
	단말기.M출력(([]byte)("["))
	//단말기.M출력(data)	
	단말기.M출력(([]byte)(":len"))
	단말기.MUint32출력(uint32(len(data)))
	단말기.M출력(([]byte)("]"))

	elfHeader := (*ElfHeader)(Pointer(&data[0]))
	/*
	단말기.M출력(([]byte)("["))
	for i:=0; i<16; i++{
		단말기.M출력(([]byte)(":"))
		단말기.MHex출력(elfHeader.e_ident[i])
	}	 
	단말기.M출력(([]byte)("]"))
	*/
	
	단말기.M출력(([]byte)("["))
	단말기.MUint16출력(elfHeader.e_type)
	단말기.M출력(([]byte)(":"))
	단말기.MUint16출력(elfHeader.e_machine)
	단말기.M출력(([]byte)(":"))
	단말기.MUint32출력(elfHeader.e_entry)
	단말기.M출력(([]byte)(":"))
	단말기.MUint32출력(elfHeader.e_shoff)
	단말기.M출력(([]byte)(":"))
	단말기.MUint16출력(elfHeader.e_shnum)
	단말기.M출력(([]byte)(":"))
	단말기.MUint16출력(elfHeader.e_phnum)
	단말기.M출력(([]byte)("]"))




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

				for rt:=uint32(0); rt<sectHeader.sh_size/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValue[rt*8]))
					self.rel_text[rt].offset = offset
					self.rel_text[rt].o_addr = *(*uint32)(Pointer(&self.text[offset]))
					self.rel_text[rt].num= *(*uint32)(Pointer(&sectValue[rt*8+4]))
					self.rel_text_len++
				}
			}
			if EqualBytes(sectName, ([]byte)(".strtab")){

				rt := uint32(0)
				start := uint32(0)

				for st:=uint32(1); st<sectHeader.sh_size; st++{
					if sectValue[st] == 0x0 || sectValue[st] == ' ' {
						func_name := sectValue[start+1:st]
						self.strtab[rt] = BytesToString(func_name)
						start = st
						rt++
					}
				}

			}

		}

		단말기.M출력(([]byte)("<------------"))
		for rt:=uint32(0); rt<self.rel_text_len; rt++{
			단말기.M출력(([]byte)("["))
			단말기.M출력(([]byte)(self.strtab[rt]))
			단말기.M출력(([]byte)("["))
			kfunc_addr, kok := func_map[self.strtab[rt]]
			if !kok {
				단말기.M출력(([]byte)("not k exist"))
			}else{
				단말기.MUint32출력(uint32(kfunc_addr))
			}

			단말기.M출력(([]byte)("|"))
			code_addr, cok := func_map["code_addr"]
			if !cok {
				단말기.M출력(([]byte)("not c exist"))
			}else{
				단말기.MUint32출력(uint32(code_addr))
			}

			diff := uint32(kfunc_addr - code_addr - uintptr(self.rel_text[rt].offset - self.rel_text[rt].o_addr)) 
			diff_addr := Uint32ToArray(diff)
			for i:=uint32(0); i<4; i++{
				self.text[self.rel_text[rt].offset+i] = diff_addr[i]
			}
			단말기.M출력(([]byte)("]"))
		}
		단말기.M출력(([]byte)("------------>"))

		for t:=uint32(0); t<self.text_len; t++{
			code[t] = self.text[t]
		}
	}
}
