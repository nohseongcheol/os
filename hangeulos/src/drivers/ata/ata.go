/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

//import . "unsafe"

import . "port"
import . "콘솔"

const BytesPerSector int = 512

type T고급기술결합 struct{
	마스터 bool
	자료포트 T워드포트		
	에러포트 T바이트포트
	섹터갯수포트 T바이트포트
	논리블록주소_낮은포트 T바이트포트 	// logical block address 
	논리블록주소_중간포트 T바이트포트 	// logical block address
	논리블록주소_높은포트 T바이트포트 	// logical block address
	장치포트 T바이트포트
	명령포트 T바이트포트
	컨트롤포트 T바이트포트
}

func (자신 *T고급기술결합) M초기화(마스터 bool, 포트기준 uint16){
        자신.마스터 = 마스터
        자신.자료포트.M초기화(포트기준)
        자신.에러포트.M초기화(포트기준+0x1)
        자신.섹터갯수포트.M초기화(포트기준+0x2)
        자신.논리블록주소_낮은포트.M초기화(포트기준+0x3)
        자신.논리블록주소_중간포트.M초기화(포트기준+0x4)
        자신.논리블록주소_높은포트.M초기화(포트기준+0x5)
        자신.장치포트.M초기화(포트기준+0x6)
        자신.명령포트.M초기화(포트기준+0x7)
        자신.컨트롤포트.M초기화(포트기준+0x8)
	
}

func (자신 *T고급기술결합)Identify() {

	var 콘솔 = T콘솔{}

	if 자신.마스터{
		자신.장치포트.M쓰기(0xA0)
	}else{
		자신.장치포트.M쓰기(0xB0)
	}
	자신.컨트롤포트.M쓰기(0)
	자신.장치포트.M쓰기(0xA0)

	var 상태 uint8 = 자신.명령포트.M읽기()
	if 상태 == 0xFF {
		콘솔.M출력("Invalid Status")
		return
	}


	if 자신.마스터{
		자신.장치포트.M쓰기(0xA0)
	}else{
		자신.장치포트.M쓰기(0xB0)
	}
	자신.섹터갯수포트.M쓰기(0)
	자신.논리블록주소_낮은포트.M쓰기(0)
	자신.논리블록주소_중간포트.M쓰기(0)
	자신.논리블록주소_높은포트.M쓰기(0)
	자신.명령포트.M쓰기(0xEC)
	
	상태 = 자신.명령포트.M읽기()
	if 상태 == 0x00 {
		콘솔.M출력("HDD Does not exist, ignoreign ")
		return
	}
	for ;(상태 & 0x80) == 0x80 && (상태 & 0x01) != 0x01; {
		상태 = 자신.명령포트.M읽기()
	}

	if (상태 & 0x01) != 0 {
		콘솔.M출력("error reading ATA")	
		return
	}
	
	for i:=0; i<256; i++ {
		var 자료  = 자신.자료포트.M읽기()
		텍스트 := []byte("  ")
		텍스트[0] = uint8((자료 >> 8) & 0xFF)
		텍스트[1] = uint8(자료 & 0xFF)
	}
	콘솔.M출력XY("ata ok", 10, 22)

}
func (자신 *T고급기술결합)M읽기28(섹터 uint32, 자료 *[]byte, 갯수 int) {
	var 콘솔 = T콘솔{}
	if (섹터 & 0xF0000000)!=0 {
		콘솔.M출력(([]byte)("ata read error "))
		return
	}
	if 갯수 > BytesPerSector {
		콘솔.M출력(([]byte)("ata read error "))
		return
	}
	
	if 자신.마스터 {
		자신.장치포트.M쓰기(uint8(0xE0 | uint8((섹터 & 0x0F000000) >> 24)))
	}else {
		자신.장치포트.M쓰기(uint8(0xF0 | uint8((섹터 & 0x0F000000) >> 24)))
	}
	자신.에러포트.M쓰기(0)
	자신.섹터갯수포트.M쓰기(1)

	자신.논리블록주소_낮은포트.M쓰기(uint8(섹터 & 0x000000FF))
	자신.논리블록주소_중간포트.M쓰기(uint8((섹터 & 0x0000FF00) >> 8))
	자신.논리블록주소_높은포트.M쓰기(uint8((섹터 & 0x00FF0000) >> 16))
	자신.명령포트.M쓰기(0x20)


	var 상태 uint8 = 자신.명령포트.M읽기()
	for ; ((상태 & 0x80) == 0x80) && ((상태 & 0x01) != 0x01); {
		상태 = 자신.명령포트.M읽기()
	}
	
	if (상태 & 0x01) != 0  {
		콘솔.M출력(([]byte)("ata read error "))
		return
	}

	콘솔.M출력XY("Reading ATA Drive:", 1, 24)

	var i int = 0
	for ; i<갯수; i+=2{
		var 쓰기자료 uint16 = 자신.자료포트.M읽기()
		(*자료)[i] = uint8(쓰기자료 & 0x00FF)

		if i+1 < 갯수 {
			(*자료)[i+1] = uint8((쓰기자료 >> 8) & 0x00FF)
		}
	}
	

	for i:=(갯수+(갯수%2)); i<BytesPerSector; i+=2 {
		자신.자료포트.M읽기()
	}
}
func (자신 *T고급기술결합) M쓰기28(섹터번호 uint32, 자료 []byte, 갯수 uint32){

	if 섹터번호 > 0x0FFFFFFF {
		return
	}

	if 갯수 > 512 {
		return
	}

        if 자신.마스터 {
                자신.장치포트.M쓰기(uint8(0xE0 | uint8((섹터번호 & 0x0F000000) >> 24)))
        }else {
                자신.장치포트.M쓰기(uint8(0xF0 | uint8((섹터번호 & 0x0F000000) >> 24)))
        }

        자신.에러포트.M쓰기(0)
        자신.섹터갯수포트.M쓰기(1)
        자신.논리블록주소_낮은포트.M쓰기(uint8(섹터번호 & 0x000000FF))
        자신.논리블록주소_중간포트.M쓰기(uint8((섹터번호 & 0x0000FF00) >> 8))
        자신.논리블록주소_높은포트.M쓰기(uint8((섹터번호 & 0x00FF0000) >> 16))
        자신.명령포트.M쓰기(0x30)

	var 콘솔 = T콘솔{}
        콘솔.M출력(([]byte)("Writing to ATA Drive:"))
        
        for i:=uint32(0) ; i<갯수; i+=2{ 

                var 쓰기자료 uint16 = uint16(자료[i])

		if i+1 < 갯수 {
			쓰기자료 = 쓰기자료 | (uint16(자료[i+1]) << 8)
		}

		자신.자료포트.M쓰기(쓰기자료)
	
		텍스트 := []byte("  ")
		텍스트[0] = uint8((쓰기자료 >>8) & 0xFF)
		텍스트[1] = uint8(쓰기자료 & 0xFF)

        }

        for i:=(갯수+(갯수%2)); i<512; i+=2 {
                자신.자료포트.M쓰기(0x0000)
        }

}

func (자신 *T고급기술결합) Flush() {
        if 자신.마스터 {
                자신.장치포트.M쓰기(0xE0)
        }else { 
                자신.장치포트.M쓰기(0xF0)
        }
        자신.명령포트.M쓰기(0xE7)

        var 콘솔 = T콘솔{}

        var 상태 uint8 = 자신.명령포트.M읽기()
        if 상태 ==0x00 {
                return
        }

	for ; ((상태 & 0x80) == 0x80) && ((상태 & 0x01) != 0x01); {
		상태 = 자신.명령포트.M읽기()
	}
	if (상태 & 0x01) != 0 {
		콘솔.M출력(([]byte)(" ata flush error"))
		return
	}

}
