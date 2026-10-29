/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package Interrupt

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "작업관리자"
import . "단말기"

///////////////////////////////////////////////////////////////////////////////
//
// 	개입중단 = 개입중단 = Interrupt
//
///////////////////////////////////////////////////////////////////////////////
func 개입중단_무시하기()

func 개입중단_예외처리()
func 개입중단_예외처리0x00()
func 개입중단_예외처리0x01()
func 개입중단_예외처리0x02()
func 개입중단_예외처리0x03()
func 개입중단_예외처리0x04()
func 개입중단_예외처리0x05()
func 개입중단_예외처리0x06()
func 개입중단_예외처리0x07()
func 개입중단_예외처리0x08()
func 개입중단_예외처리0x09()
func 개입중단_예외처리0x0A()
func 개입중단_예외처리0x0B()
func 개입중단_예외처리0x0C()
func 개입중단_예외처리0x0D()
func 개입중단_예외처리0x0E()
func 개입중단_예외처리0x0F()

func 개입중단_요청처리0x00()
func 개입중단_요청처리0x01()
func 개입중단_요청처리0x02()
func 개입중단_요청처리0x03()
func 개입중단_요청처리0x04()
func 개입중단_요청처리0x05()
func 개입중단_요청처리0x06()
func 개입중단_요청처리0x07()
func 개입중단_요청처리0x08()
func 개입중단_요청처리0x09()
func 개입중단_요청처리0x0A()
func 개입중단_요청처리0x0B()
func 개입중단_요청처리0x0C()
func 개입중단_요청처리0x0D()
func 개입중단_요청처리0x0E()
func 개입중단_요청처리0x0F()

func 개입중단_요청처리0x80()


///////////////////////////////////////////////////////////////////////////////
//
//	개입중단_처리기 = InteruptHandler, 개입중단번호 = interruptnumber
//
///////////////////////////////////////////////////////////////////////////////
type T개입중단_처리기 struct{
	개입중단번호 uint8
	개입중단_관리자 uintptr 
}
var 처리기들 [256] uintptr  // handler

func (자신 *T개입중단_처리기) M초기화(개입중단번호 uint8, 개입중단_관리자 uintptr, 함수주소 uintptr){

	처리기들[개입중단번호] = 함수주소

	자신.개입중단번호 = 개입중단번호 
	자신.개입중단_관리자 = 개입중단_관리자

}
func (자신 *T개입중단_처리기) SetHandleInterruptFuction(주소 uintptr){
	처리기들[자신.개입중단번호] = 주소 
}
func (자신 *T개입중단_처리기) M소멸하기(){
	자신정수주소 := uintptr(Pointer(자신))
	개입중단_관리자 := (*T개입중단_관리자)(Pointer(자신.개입중단_관리자))
	if 자신정수주소 == 개입중단_관리자.M처리기_갖기(자신.개입중단번호) {
		개입중단_관리자.M처리기_설정(0, 자신.개입중단번호)
	}

}
func (자신 *T개입중단_처리기) 개입중단_관리자설정(개입중단_관리자 uintptr){
}
func (자신 *T개입중단_처리기) 개입중단_관리자번호설정(개입중단번호 uint8){
	자신.개입중단번호 = 개입중단번호
}
///////////////////////////////////////////////////////////////////////////////
type TGateDescriptor struct{
	gateData [8] uint8

	// handlerAddrressLowBits uint16 -- 낮은비트주소 다루기
	// gdt_codeSegmentSelector uint16 --
	// reserved uint8 // 예약여부
	// access uint8   // 접근
	// handlerAddressHightBits uint16 -- 높은빝으 주소 다루기
}
var 개입중단서술자표_자료 [256*8] uint8
var 활성개입중단_관리자 uintptr = 0
///////////////////////////////////////////////////////////////////////////////
//
//		개입중단_관리자 = InterruptManager
//
///////////////////////////////////////////////////////////////////////////////
type T개입중단_관리자 struct {
	처리기들 [256] uintptr
	하드웨어개입중단위치 int
	작업관리자 *T작업관리자

	// PIC = Programable Interrupt Controller = 프로그램 가능 인터럽트 제어기
	주PIC_명령_입출력단자 T바이트입출력단자 // pic master command port
	주PIC_자료_입출력단자 T바이트입출력단자 // pic master data port
	보조PIC_명령_입출력단자 T바이트입출력단자 // pic slave command port
	보조PIC_자료_입출력단자 T바이트입출력단자 // pic slave datga port

}

func (자신 *T개입중단_관리자) M초기화(하드웨어개입중단위치 uint16, 공용서술자표 *T공용서술자표, 작업관리자 *T작업관리자){
	
	자신.작업관리자 = 작업관리자
	자신.하드웨어개입중단위치 = int(하드웨어개입중단위치)

	코드조각 := uint16(SEG_KERNEL_CODE)

	for i:=0; i<(256*8); i++{
		개입중단서술자표_자료[i] = 0
	}
	var 주소 uint32
	var IDT_INTERRUPT_GATE uint8 = 0xE // 개입중단 32bit

	주소 = uint32(ValueOf(개입중단_무시하기).Pointer())
	for i:=0; i<256; i++ {
		처리기들[i] = 0
		주소 = uint32(ValueOf(개입중단_예외처리0x0F).Pointer())
		자신.개입중단서술자표항목설정(i, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 
	} 

	주소 = uint32(ValueOf(개입중단_예외처리0x00).Pointer())
	자신.개입중단서술자표항목설정(0x00, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x01).Pointer())
	자신.개입중단서술자표항목설정(0x01, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(개입중단_예외처리0x02).Pointer())
	자신.개입중단서술자표항목설정(0x02, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x03).Pointer())
	자신.개입중단서술자표항목설정(0x03, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x04).Pointer())
	자신.개입중단서술자표항목설정(0x04, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x05).Pointer())
	자신.개입중단서술자표항목설정(0x05, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x06).Pointer())
	자신.개입중단서술자표항목설정(0x06, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x07).Pointer())
	자신.개입중단서술자표항목설정(0x07, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x08).Pointer())
	자신.개입중단서술자표항목설정(0x08, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x09).Pointer())
	자신.개입중단서술자표항목설정(0x09, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x0A).Pointer())
	자신.개입중단서술자표항목설정(0x0A, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x0B).Pointer())
	자신.개입중단서술자표항목설정(0x0B, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(개입중단_예외처리0x0C).Pointer())
	자신.개입중단서술자표항목설정(0x0C, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(개입중단_예외처리0x0D).Pointer())
	자신.개입중단서술자표항목설정(0x0D, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x0E).Pointer())
	자신.개입중단서술자표항목설정(0x0E, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_예외처리0x0F).Pointer())
	자신.개입중단서술자표항목설정(0x0F, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 
	///////////////////////////////////////////////////////////////////////////

	주소 = uint32(ValueOf(개입중단_요청처리0x00).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x00, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 
	
	주소 = uint32(ValueOf(개입중단_요청처리0x01).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x01, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x02).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x02, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x03).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x03, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x04).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x04, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x05).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x05, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x06).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x06, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x07).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x07, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x08).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x08, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x09).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x09, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x0A).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x0A, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x0B).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x0B, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x0C).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x0C, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x0D).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x0D, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x0E).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x0E, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x0F).Pointer())
	자신.개입중단서술자표항목설정(자신.하드웨어개입중단위치+0x0F, 코드조각, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(개입중단_요청처리0x80).Pointer())
	자신.개입중단서술자표항목설정(0x80, 코드조각, 주소, 3, IDT_INTERRUPT_GATE) 


	자신.주PIC_명령_입출력단자 = T바이트입출력단자{}
	자신.주PIC_자료_입출력단자 = T바이트입출력단자{}
	
	자신.보조PIC_명령_입출력단자 = T바이트입출력단자{}
	자신.보조PIC_자료_입출력단자 = T바이트입출력단자{}	

	자신.주PIC_명령_입출력단자.M초기화(0x20)
	자신.주PIC_자료_입출력단자.M초기화(0x21)

	자신.보조PIC_명령_입출력단자.M초기화(0xA0)
	자신.보조PIC_자료_입출력단자.M초기화(0xA1)

	자신.주PIC_명령_입출력단자.M쓰기(0x11)
	자신.보조PIC_명령_입출력단자.M쓰기(0x11)

	자신.주PIC_자료_입출력단자.M쓰기(0x20)
	자신.보조PIC_자료_입출력단자.M쓰기(0x28)

	자신.주PIC_자료_입출력단자.M쓰기(0x04)
	자신.보조PIC_자료_입출력단자.M쓰기(0x02)

	자신.주PIC_자료_입출력단자.M쓰기(0x01)
	자신.보조PIC_자료_입출력단자.M쓰기(0x01)

	자신.주PIC_자료_입출력단자.M쓰기(0x00) // all master pic
	자신.보조PIC_자료_입출력단자.M쓰기(0x00) // all slave pic


	개입중단서술자표_주소 := [6]uint8{0, 0, 0, 0, 0, 0}
	크기 := (*uint16)(Pointer(&개입중단서술자표_주소[0]))
	(*크기) = (uint16)(Sizeof(개입중단서술자표_자료) -1)
	
	기준 := (*uint32)(Pointer(&개입중단서술자표_주소[2]))
	(*기준) = uint32(uintptr(Pointer(&개입중단서술자표_자료)))
	
	개입중단서술자표_적재(uintptr(Pointer(&개입중단서술자표_주소)))
}
func 개입중단서술자표_적재(개입중단서술자표_주소 uintptr)

func (자신 *T개입중단_관리자) 개입중단서술자표항목설정(개입중단 int, 
							코드조각 uint16,
							처리기 uint32,
							서술자권한단계 uint8,
							서술자유형 uint8){ 

	처리기주소_낮은영역비트 := (*uint16)(Pointer(&개입중단서술자표_자료[개입중단*8+0]))
	(*처리기주소_낮은영역비트) = uint16(처리기 & 0xFFFF)

	gdt_codeSegmentSelector := (*uint16)(Pointer(&개입중단서술자표_자료[개입중단*8+2]))
	(*gdt_codeSegmentSelector) = 코드조각

	예약되어진 := (*uint8)(Pointer(&개입중단서술자표_자료[개입중단*8+4]))
	(*예약되어진) = 0

	var IDT_DESC_PRESENT uint8 = 0x80
	접근권한 := (*uint8)(Pointer(&개입중단서술자표_자료[개입중단*8+5]))
	(*접근권한) = (IDT_DESC_PRESENT | 서술자유형 | ((서술자권한단계 & 3) << 5)) 

	처리기주소_높은영역비트 := (*uint16)(Pointer(&개입중단서술자표_자료[개입중단*8+6]))
	(*처리기주소_높은영역비트) = uint16((처리기 >> 16) & 0xFFFF)

}

func (자신 *T개입중단_관리자) M처리기_설정(처리기 uintptr, 개입중단번호 uint8){
	처리기들[개입중단번호] = 처리기
}
func (자신 *T개입중단_관리자) M처리기_갖기(개입중단번호 uint8) uintptr{
	return 처리기들[개입중단번호]
}
func (자신 *T개입중단_관리자) 개입중단_처리하기(개입중단 uint8, esp uint32) uint32{
	단말기 := T단말기{}
	단말기.M출력(esp, 2, 14)
	단말기.M출력(":")
	단말기.M출력(개입중단)
	단말기.M출력("]")


	if 처리기들[개입중단] != 0 {
		사용자함수 := (*(*func(uint32, uint32))(Pointer(처리기들[개입중단])))
		사용자함수(esp, esp)
	} else if 개입중단 !=  uint8(자신.하드웨어개입중단위치){ // ?? 
		단말기.M출력("unhandle interrupt 0x")
		단말기.M출력(개입중단)
	}

	if 개입중단 == uint8(자신.하드웨어개입중단위치) {
		esp = uint32(uintptr(Pointer(자신.작업관리자.M작업일정((*T중앙처리장치_상태)(Pointer(uintptr(esp)))))))
	}

	if uint8(자신.하드웨어개입중단위치) <= 개입중단 && 개입중단 < uint8(자신.하드웨어개입중단위치+16){
		자신.주PIC_명령_입출력단자.M쓰기(0x20)
		if uint8(자신.하드웨어개입중단위치+8) <= 개입중단 {
			자신.보조PIC_명령_입출력단자.M쓰기(0x20)
		}
	}
	return esp
}
func 개입중단처리(esp uint32, 개입중단 uint8) uint32{

	if 활성개입중단_관리자 != 0 {
		개입중단_관리자 := (*T개입중단_관리자)(Pointer(활성개입중단_관리자))
		return 개입중단_관리자.개입중단_처리하기(개입중단, esp)
	}

	return esp
}
var 예외번호 uint8
func 예외처리(esp uint32, 개입중단 uint8) uint32{
	hex := []byte("0123456789ABCDEF");
        임시 := []byte("\n           HandleException :   ")
	임시[29] = 예외번호
	임시[31] = hex[개입중단 & 0x0F]
	임시[30] = hex[(개입중단 & 0xF0)>>2]
	예외번호++

        단말기 := new(T단말기)
	단말기.M출력(임시)
	단말기.M출력("esp[")
	단말기.M출력(esp)
	단말기.M출력(":")
	단말기.M출력(개입중단)
	단말기.M출력(":")
	단말기.M출력(예외번호)
	단말기.M출력("]")

	return esp
}

func 개입중단활성화()
func (자신 *T개입중단_관리자) M활성화(){
	if 활성개입중단_관리자 != 0 {
		자신.M비활성화()
	}
	주소 := uintptr(Pointer(자신))
	활성개입중단_관리자 = 주소
	개입중단활성화()
}

func 개입중단비활성화()
func (자신 *T개입중단_관리자) M비활성화(){
	활성개입중단_관리자 = 0
	개입중단비활성화()
}

