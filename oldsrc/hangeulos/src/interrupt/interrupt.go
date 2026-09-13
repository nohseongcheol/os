/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package Interrupt

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "작업관리자"
import . "콘솔"

///////////////////////////////////////////////////////////////////////////////
//
// 	인터럽트 = 인터럽트 = Interrupt
//
///////////////////////////////////////////////////////////////////////////////
func 인터럽트_무시하기()

func 인터럽트_예외처리()
func 인터럽트_예외처리0x00()
func 인터럽트_예외처리0x01()
func 인터럽트_예외처리0x02()
func 인터럽트_예외처리0x03()
func 인터럽트_예외처리0x04()
func 인터럽트_예외처리0x05()
func 인터럽트_예외처리0x06()
func 인터럽트_예외처리0x07()
func 인터럽트_예외처리0x08()
func 인터럽트_예외처리0x09()
func 인터럽트_예외처리0x0A()
func 인터럽트_예외처리0x0B()
func 인터럽트_예외처리0x0C()
func 인터럽트_예외처리0x0D()
func 인터럽트_예외처리0x0E()
func 인터럽트_예외처리0x0F()

func 인터럽트_요청처리0x00()
func 인터럽트_요청처리0x01()
func 인터럽트_요청처리0x02()
func 인터럽트_요청처리0x03()
func 인터럽트_요청처리0x04()
func 인터럽트_요청처리0x05()
func 인터럽트_요청처리0x06()
func 인터럽트_요청처리0x07()
func 인터럽트_요청처리0x08()
func 인터럽트_요청처리0x09()
func 인터럽트_요청처리0x0A()
func 인터럽트_요청처리0x0B()
func 인터럽트_요청처리0x0C()
func 인터럽트_요청처리0x0D()
func 인터럽트_요청처리0x0E()
func 인터럽트_요청처리0x0F()

func 인터럽트_요청처리0x80()


///////////////////////////////////////////////////////////////////////////////
//
//	인터럽트_처리기 = InteruptHandler, 인터럽트번호 = interruptnumber
//
///////////////////////////////////////////////////////////////////////////////
type T인터럽트_처리기 struct{
	인터럽트번호 uint8
	인터럽트_관리자 uintptr 
}

var 처리기들 [256] uintptr  // handler

func (자신 *T인터럽트_처리기) M초기화(인터럽트번호 uint8, 인터럽트_관리자 uintptr, 함수주소 uintptr){

	처리기들[인터럽트번호] = 함수주소

	자신.인터럽트번호 = 인터럽트번호 
	자신.인터럽트_관리자 = 인터럽트_관리자

}
func (자신 *T인터럽트_처리기) M인터럽트함수처리_설정(주소 uintptr){
	처리기들[자신.인터럽트번호] = 주소 
}
func (자신 *T인터럽트_처리기) M소멸자(){
	자신주소 := uintptr(Pointer(자신))
	인터럽트_관리자 := (*T인터럽트_관리자)(Pointer(자신.인터럽트_관리자))
	if 자신주소 == 인터럽트_관리자.M처리기_갖기(자신.인터럽트번호) {
		인터럽트_관리자.M처리기_설정(0, 자신.인터럽트번호)
	}

}
func (자신 *T인터럽트_처리기) 인터럽트_관리자설정(인터럽트_관리자 uintptr){
}
func (자신 *T인터럽트_처리기) 인터럽트_관리자번호설정(인터럽트번호 uint8){
	자신.인터럽트번호 = 인터럽트번호
}
func (자신 *T인터럽트_처리기) HandleInterrupt(esp uint32) uint32{
        임시 := []byte("\n\n\n\n\n   T인터럽트_처리기")
        콘솔 := new(T콘솔)
	콘솔.M출력(임시)
	return esp
}
///////////////////////////////////////////////////////////////////////////////
type T게이트서술자 struct{
	게이트자료 [8] uint8

	// handlerAddrressLowBits uint16 -- 낮은비트주소 다루기
	// 서술자표_코드세그먼트_선택자 uint16 --
	// reserved uint8 // 예약여부
	// access uint8   // 접근
	// handlerAddressHightBits uint16 -- 높은빝으 주소 다루기
}
type T인터럽트서술자테이블포인터 struct{
}
var 인터럽트서술자테이블_자료 [256*8] uint8
var 활성인터럽트_관리자 uintptr = 0

///////////////////////////////////////////////////////////////////////////////
//
//		인터럽트_관리자 = InterruptManager
//
///////////////////////////////////////////////////////////////////////////////
type T인터럽트_관리자 struct {
	처리기들 [256] uintptr
	하드웨어인터럽트위치 uint16
	작업관리자 *T작업관리자

	// PIC = Programable Interrupt Controller = 프로그램 가능한 인터럽트 제어기
	주PIC_명령_포트 T바이트포트 // pic master command port
	주PIC_자료_포트 T바이트포트 // pic master data port
	보조PIC_명령_포트 T바이트포트 // pic slave command port
	보조PIC_자료_포트 T바이트포트 // pic slave datga port

}

func (자신 *T인터럽트_관리자) M초기화(하드웨어인터럽트위치 uint16, 공용서술자표 *T공용서술자표, 작업관리자 *T작업관리자){
	
	자신.작업관리자 = 작업관리자
	자신.하드웨어인터럽트위치 = 하드웨어인터럽트위치	

	명령어코드_세그먼트 := uint16(SEG_KERNEL_CODE)


	for i:=0; i<(256*8); i++{
		인터럽트서술자테이블_자료[i] = 0
	}
	var 주소 uint32
	var IDT_INTERRUPT_GATE uint8 = 0xE // 인터럽트 32bit

	주소 = uint32(ValueOf(인터럽트_무시하기).Pointer())
	for i:=0; i<256; i++ {
		처리기들[i] = 0
		주소 = uint32(ValueOf(인터럽트_예외처리0x0F).Pointer())
		자신.인터럽트서술자표항목설정(i, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	} 

	주소 = uint32(ValueOf(인터럽트_예외처리0x00).Pointer())
	자신.인터럽트서술자표항목설정(0x00, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x01).Pointer())
	자신.인터럽트서술자표항목설정(0x01, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(인터럽트_예외처리0x02).Pointer())
	자신.인터럽트서술자표항목설정(0x02, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x03).Pointer())
	자신.인터럽트서술자표항목설정(0x03, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x04).Pointer())
	자신.인터럽트서술자표항목설정(0x04, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x05).Pointer())
	자신.인터럽트서술자표항목설정(0x05, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x06).Pointer())
	자신.인터럽트서술자표항목설정(0x06, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x07).Pointer())
	자신.인터럽트서술자표항목설정(0x07, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x08).Pointer())
	자신.인터럽트서술자표항목설정(0x08, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x09).Pointer())
	자신.인터럽트서술자표항목설정(0x09, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x0A).Pointer())
	자신.인터럽트서술자표항목설정(0x0A, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x0B).Pointer())
	자신.인터럽트서술자표항목설정(0x0B, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(인터럽트_예외처리0x0C).Pointer())
	자신.인터럽트서술자표항목설정(0x0C, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(인터럽트_예외처리0x0D).Pointer())
	자신.인터럽트서술자표항목설정(0x0D, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x0E).Pointer())
	자신.인터럽트서술자표항목설정(0x0E, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_예외처리0x0F).Pointer())
	자신.인터럽트서술자표항목설정(0x0F, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	///////////////////////////////////////////////////////////////////////////

	주소 = uint32(ValueOf(인터럽트_요청처리0x00).Pointer())
	자신.인터럽트서술자표항목설정(0x20, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	
	주소 = uint32(ValueOf(인터럽트_요청처리0x01).Pointer())
	자신.인터럽트서술자표항목설정(0x21, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(인터럽트_요청처리0x02).Pointer())
	자신.인터럽트서술자표항목설정(0x22, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x03).Pointer())
	자신.인터럽트서술자표항목설정(0x23, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x04).Pointer())
	자신.인터럽트서술자표항목설정(0x24, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x05).Pointer())
	자신.인터럽트서술자표항목설정(0x25, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x06).Pointer())
	자신.인터럽트서술자표항목설정(0x26, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x07).Pointer())
	자신.인터럽트서술자표항목설정(0x27, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x08).Pointer())
	자신.인터럽트서술자표항목설정(0x28, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x09).Pointer())
	자신.인터럽트서술자표항목설정(0x29, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x0A).Pointer())
	자신.인터럽트서술자표항목설정(0x2A, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x0B).Pointer())
	자신.인터럽트서술자표항목설정(0x2B, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(인터럽트_요청처리0x0C).Pointer())
	자신.인터럽트서술자표항목설정(0x2C, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 
	주소 = uint32(ValueOf(인터럽트_요청처리0x0D).Pointer())
	자신.인터럽트서술자표항목설정(0x2D, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x0E).Pointer())
	자신.인터럽트서술자표항목설정(0x2E, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x0F).Pointer())
	자신.인터럽트서술자표항목설정(0x2F, 명령어코드_세그먼트, 주소, 0, IDT_INTERRUPT_GATE) 

	주소 = uint32(ValueOf(인터럽트_요청처리0x80).Pointer())
	자신.인터럽트서술자표항목설정(0x80, 명령어코드_세그먼트, 주소, 3, IDT_INTERRUPT_GATE) 

	자신.주PIC_명령_포트 = T바이트포트{}
	자신.주PIC_자료_포트 = T바이트포트{}
	
	자신.보조PIC_명령_포트 = T바이트포트{}
	자신.보조PIC_자료_포트 = T바이트포트{}	

	자신.주PIC_명령_포트.M초기화(0x20)
	자신.주PIC_자료_포트.M초기화(0x21)

	자신.보조PIC_명령_포트.M초기화(0xA0)
	자신.보조PIC_자료_포트.M초기화(0xA1)

	자신.주PIC_명령_포트.M쓰기(0x11)
	자신.보조PIC_명령_포트.M쓰기(0x11)

	자신.주PIC_자료_포트.M쓰기(0x20)
	자신.보조PIC_자료_포트.M쓰기(0x28)

	자신.주PIC_자료_포트.M쓰기(0x04)
	자신.보조PIC_자료_포트.M쓰기(0x02)

	자신.주PIC_자료_포트.M쓰기(0x01)
	자신.보조PIC_자료_포트.M쓰기(0x01)

	자신.주PIC_자료_포트.M쓰기(0x00) // all master pic
	자신.보조PIC_자료_포트.M쓰기(0x00) // all slave pic


	인터럽트서술자테이블_정보 := [6]uint8{0, 0, 0, 0, 0, 0}
	크기 := (*uint16)(Pointer(&인터럽트서술자테이블_정보[0]))
	(*크기) = (uint16)(Sizeof(인터럽트서술자테이블_자료) -1)
	
	기준점 := (*uint32)(Pointer(&인터럽트서술자테이블_정보[2]))
	(*기준점) = uint32(uintptr(Pointer(&인터럽트서술자테이블_자료)))
	
	인터럽트테이블_적재하기(uintptr(Pointer(&인터럽트서술자테이블_정보)))
}

func 인터럽트테이블_적재하기(인터럽트서술자테이블_정보_주소 uintptr)

func (자신 *T인터럽트_관리자) 인터럽트서술자표항목설정(인터럽트 int, 
							코드세그먼트 uint16,
							처리기 uint32,
							서술자권한단계 uint8,
							서술자타입 uint8){ 

	처리기주소낮은비트들 := (*uint16)(Pointer(&인터럽트서술자테이블_자료[인터럽트*8+0]))
	(*처리기주소낮은비트들) = uint16(처리기 & 0xFFFF)

	서술자표_코드세그먼트_선택자 := (*uint16)(Pointer(&인터럽트서술자테이블_자료[인터럽트*8+2]))
	(*서술자표_코드세그먼트_선택자) = 코드세그먼트

	예약되어진 := (*uint8)(Pointer(&인터럽트서술자테이블_자료[인터럽트*8+4]))
	(*예약되어진) = 0

	var IDT_DESC_PRESENT uint8 = 0x80
	접근권한 := (*uint8)(Pointer(&인터럽트서술자테이블_자료[인터럽트*8+5]))
	(*접근권한) = (IDT_DESC_PRESENT | 서술자타입 | ((서술자권한단계 & 3) << 5)) 

	처리기주소높은비트들 := (*uint16)(Pointer(&인터럽트서술자테이블_자료[인터럽트*8+6]))
	(*처리기주소높은비트들) = uint16((처리기 >> 16) & 0xFFFF)

}

func (자신 *T인터럽트_관리자) M처리기_설정(p_처리기 uintptr, 인터럽트번호 uint8){
	처리기들[인터럽트번호] = p_처리기
}
func (자신 *T인터럽트_관리자) M처리기_갖기(인터럽트번호 uint8) uintptr{
	return 처리기들[인터럽트번호]
}


func (자신 *T인터럽트_관리자) DoHandleInterrupt(인터럽트 uint8, esp uint32) uint32{
	콘솔 := T콘솔{}
	콘솔.MUint32출력XY(esp, 2, 14)

	if 처리기들[인터럽트] != 0 {

		사용자함수 := (*(*func(uint32) uint32)(Pointer(처리기들[인터럽트])))
		esp = 사용자함수(esp)

	}

	/*
	if 인터럽트 == uint8(자신.하드웨어인터럽트위치) {
		//esp = uint32(uintptr(Pointer(자신.작업관리자.M작업일정((*T시피유상태)(Pointer(uintptr(esp)))))))
		//콘솔.M출력(esp)		
	}
	if 인터럽트 <= 0x1F{
	}	
	*/
	if 0x20 <= 인터럽트 && 인터럽트 < 0x30 {
		자신.주PIC_명령_포트.M쓰기(0x20)
		if 0x28 <= 인터럽트 {
			자신.보조PIC_명령_포트.M쓰기(0x20)
		}
	}
	//콘솔.M출력(":")
	//콘솔.MUint32출력(esp)
	return esp
}
func 인터럽트처리(esp uint32, 인터럽트 uint8) uint32{

	if 활성인터럽트_관리자 != 0 {
		p := (*T인터럽트_관리자)(Pointer(활성인터럽트_관리자))
		return p.DoHandleInterrupt(uint8(인터럽트), esp)
	}

	return esp
}
var 예외번호 uint8
func 예외처리(esp uint32, 인터럽트 uint8) uint32{
	hex := []byte("0123456789ABCDEF");
        임시 := []byte("\n           HandleException :   ")
	임시[29] = 예외번호
	임시[31] = hex[인터럽트 & 0x0F]
	임시[30] = hex[(인터럽트 & 0xF0)>>2]
	예외번호++

        콘솔 := new(T콘솔)
	콘솔.M출력(임시)
	콘솔.M출력(esp)

	return esp
}

func 인터럽트활성화()
func (자신 *T인터럽트_관리자) M활성화(){
	if 활성인터럽트_관리자 != 0 {
		자신.M비활성화()
	}
	주소 := uintptr(Pointer(자신))
	활성인터럽트_관리자 = 주소
	인터럽트활성화()
}

func 인터럽트비활성화()
func (자신 *T인터럽트_관리자) M비활성화(){
	활성인터럽트_관리자 = 0
	인터럽트비활성화()
}

