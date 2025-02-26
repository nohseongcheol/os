/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systemcall

import . "unsafe"

import . "interrupt"
import . "콘솔"
import . "작업관리자"
import . "drivers/ata"
import . "filesystem/msdospart"
import . "filesystem/fat"



type T시스템호출 struct{
	T인터럽트_처리기
}

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32)
func M시스템_읽기(임시 *[]byte, 갯수 int){
	var ebx = uint32(uintptr(Pointer(임시)))
	var ecx = uint32(갯수)
	시스템호출(5, ebx, ecx)
}
func M시스템_출력(임시 []byte){
        var ebx uint32 = uint32(uintptr(Pointer(&임시)))
        시스템호출(6, ebx)
}

func M시스템_출력XY(임시 []byte, x uint32, y uint32){
        var ebx uint32 = uint32(uintptr(Pointer(&임시)))
        시스템호출(6, ebx, x, y)
}

func 시스템호출(매개변수들 ... uint32){

	l := len(매개변수들)
	switch(l){
		case 1: 
			Interrupt(매개변수들[0], 0, 0, 0, 0, 0)
		case 2: 
			Interrupt(매개변수들[0], 매개변수들[1], 0, 0, 0, 0)
		case 3:
			Interrupt(매개변수들[0], 매개변수들[1], 매개변수들[2], 0, 0, 0)
		case 4:
			Interrupt(매개변수들[0], 매개변수들[1], 매개변수들[2], 매개변수들[3], 0, 0)
		case 5:
			Interrupt(매개변수들[0], 매개변수들[1], 매개변수들[2], 매개변수들[3], 매개변수들[4], 0)
		case 6:
			Interrupt(매개변수들[0], 매개변수들[1], 매개변수들[2], 매개변수들[3], 매개변수들[4], 매개변수들[5])
		default:
			Interrupt(매개변수들[0], 매개변수들[1], 매개변수들[2], 매개변수들[3], 매개변수들[4], 매개변수들[5])
	}
}

func (자신 *T시스템호출) M초기화(인터럽트관리자 *T인터럽트_관리자){


	인터럽트_처리기 = 인터럽트_처리함수

        var 주소 uintptr
        주소 = uintptr(Pointer(&인터럽트_처리기))

        자신.T인터럽트_처리기.M초기화(0x80, uintptr(Pointer(인터럽트관리자)), 주소)
}

var 콘솔 = T콘솔{}
var 인터럽트_처리기 func(uint32) uint32
func 인터럽트_처리함수(esp uint32) uint32{
	
	var 시피유 = (*T시피유상태)(Pointer(uintptr(esp)))
	
	switch(시피유.Eax){
		case 1:		//exit
		case 2:		//fork
			콘솔.M출력XY(([]byte)("2"), 1, 22);
		case 3:
			콘솔.M출력XY(([]byte)("3"), 1, 22);
			//콘솔.M출력XY(임시, 1, 22);
		/*
		case 4:
			//var 임시 []byte = *(*[]byte)(Pointer(uintptr(시피유.Ecx)));
			var 임시 []byte = (([]byte)("4"))
			콘솔.M출력XY(임시, 1, 22);
		*/
		case 5:

			//var 임시 *[]byte = (*[]byte)(Pointer(uintptr(시피유.Ebx)));
			//var 갯수 = int(시피유.Ecx);

       			var ata0s = T고급기술결합{}
        		ata0s.M초기화(false, 0x1F0)
        		ata0s.Identify()

        		partition := TMSDOS파티션테이블{}
        		partition.M파티션들_읽기(&ata0s)

			bios := T바이오스_파라미터_블록32{}

			for i:=0; i<4; i++ {
				var filename []byte = ([]byte)("FILE1")
				var data []byte
				bios.Read(&ata0s, partition.MBR.PrimaryPartition[i], filename, data)
			}
	
		case 6:
			var 임시 []byte = *(*[]byte)(Pointer(uintptr(시피유.Ebx)))
			x := uint16(시피유.Ecx)
			y := uint16(시피유.Edx)

			if x == 0 && y == 0{
				콘솔.M출력(임시);
			}else{
				콘솔.M출력XY(임시, x, y);
			}

		case 7:
		default:
			콘솔.M출력XY(([]byte)("sys["), 1, 23)
			콘솔.MUint32출력(esp)
			콘솔.M출력(([]byte)(":"))
			콘솔.MUint32출력(시피유.Eax)
			콘솔.M출력(([]byte)(":"))
			콘솔.MUint32출력(시피유.Ebx)
			콘솔.M출력(([]byte)("]"))
	}

	return esp
}
