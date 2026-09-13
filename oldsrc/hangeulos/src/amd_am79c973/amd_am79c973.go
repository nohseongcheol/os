/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package amd_am79c973

import . "unsafe"
import . "util"
import . "interrupt"
import . "콘솔"
import . "port"
import . "pci"

var 콘솔 T콘솔= T콘솔{}
type T초기화블록 struct{
	상태 uint16
	보내는버퍼들_갯수 uint8 // 4bit reserved1, 4bit 보내는버퍼들_갯수
	받은버퍼들_갯수 uint8 // 4bit reserved2, 4bit 받은버퍼들_갯수
	물리주소 uint64		// physicalAddress
	논리주소 uint64		// logicalAddress
	받은버퍼_서술자_주소 uintptr
	보내는버퍼서술자_주소 uintptr
}
type T버퍼서술자 struct{
	주소 uint32
	표시들 uint32
	표시들2 uint32
	활용여부 uint32 //avail
}

type I원시자료_처리기 interface{
	M원시자료_받는동시(자료주소 uintptr, 크기 uint32) bool
	M보내기(자료주소 uintptr, 크기 uint32)
}

var 원시자료_후단부 Tamd_am79c973
type T원시자료_처리기 struct{
}
func (자신 *T원시자료_처리기) 후단부_설정(후단부 Tamd_am79c973){
	원시자료_후단부 = 후단부
}
func (자신 *T원시자료_처리기) 후단부_갖기() Tamd_am79c973{
	return 원시자료_후단부
}
func (자신 *T원시자료_처리기) M원시자료_받는동시(자료주소 uintptr, 크기 uint32) bool{
	콘솔.M출력XY(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (자신 *T원시자료_처리기) M보내기(자료주소 uintptr, 크기 uint32) {
	원시자료_후단부.M보내기(자료주소 , 크기)
}

var 맥주소_0_포트 T워드포트
var 맥주소_2_포트 T워드포트
var 맥주소_4_포트 T워드포트
var 레지스터_자료포트 T워드포트
var 레지스터_주소포트 T워드포트
var 리셋포트 T워드포트
var 버스컨트롤러_레지스터_자료포트 T워드포트

var 초기화블록 T초기화블록

var 보내는버퍼_서술자 [8]T버퍼서술자
var 보내는버퍼들_서술자_메모리 [2048+15] byte
var 보내는버퍼들 [2*1024+15][8] uint8
var 현재보내는버퍼 uint8

var 받은버퍼_서술자 [8]T버퍼서술자
var 받은버퍼들_서술자_메모리 [2048+15] uint8
var 받은버퍼들[2*1024+15][8] uint8
var 현재받은버퍼 uint8

var 함수변수 func(*Tamd_am79c973, uint32) uint32

type Tamd_am79c973 struct {
	T인터럽트_처리기
	주변부품연결장치_서술자 T주변부품연결장치_서술자
	인터럽트 *T인터럽트_관리자
	원시자료_처리기 *T원시자료_처리기
}

var i원시자료_처리기 I원시자료_처리기 
func (자신 *Tamd_am79c973) M드라이버_초기화(인터럽트 *T인터럽트_관리자, 주변부품연결장치_서술자 T주변부품연결장치_서술자, 원시자료_처리기 I원시자료_처리기) {
	
	자신.주변부품연결장치_서술자 = 주변부품연결장치_서술자
	

        함수변수 = (*Tamd_am79c973).M인터럽트_처리
        var 함수변수_주소 uintptr
        함수변수_주소 = uintptr(Pointer(&함수변수))	


	자신.M초기화(uint8(0x20+주변부품연결장치_서술자.P인터럽트), uintptr(Pointer(인터럽트)), 함수변수_주소)
	
	맥주소_0_포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스))
	맥주소_2_포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스) + 0x02)
	맥주소_4_포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스) + 0x04)
	레지스터_자료포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스) + 0x10)
	레지스터_주소포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스) + 0x12)
	리셋포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스) + 0x14)
	버스컨트롤러_레지스터_자료포트.M초기화(uint16(주변부품연결장치_서술자.P포트베이스) + 0x16)


	i원시자료_처리기 = &T원시자료_처리기{}	
	if 원시자료_처리기 != nil {
		i원시자료_처리기 = 원시자료_처리기
	}

	현재보내는버퍼 = 0
	현재받은버퍼 = 0

	var 매체0 uint64 =  uint64(맥주소_0_포트.M읽기()%256)
	var 매체1 uint64 =  uint64(맥주소_0_포트.M읽기()/256)
	var 매체2 uint64 =  uint64(맥주소_2_포트.M읽기()%256)	
	var 매체3 uint64 =  uint64(맥주소_2_포트.M읽기()/256)	
	var 매체4 uint64 =  uint64(맥주소_4_포트.M읽기()%256)	
	var 매체5 uint64 =  uint64(맥주소_4_포트.M읽기()/256)	

	var 물리주소 uint64 = (매체5 << 40) | (매체4 << 32) | (매체3 << 24) | (매체2 << 16) | (매체1 << 8) | 매체0
	
	콘솔.M출력XY(([]byte)("[interrupt num : "), 0, 13)
	콘솔.MHex출력(uint8(주변부품연결장치_서술자.P인터럽트))
	콘솔.M출력(([]byte)("]"))
	콘솔.M출력(([]byte)("[MAC address : "))
	콘솔.MUint48출력(Uint48_R(물리주소))
	콘솔.M출력(([]byte)("]"))


	레지스터_주소포트.M쓰기(20)
	버스컨트롤러_레지스터_자료포트.M쓰기(0x102)

	레지스터_주소포트.M쓰기(0)
	레지스터_자료포트.M쓰기(0x04)

	초기화블록.상태 = 0x0000
	초기화블록.보내는버퍼들_갯수 = 3
	초기화블록.받은버퍼들_갯수 = 3

	초기화블록.물리주소 = 물리주소

	초기화블록.논리주소 = 0

	보내는버퍼_서술자 = *(*([8]T버퍼서술자))(Pointer((uintptr((Pointer)(&보내는버퍼들_서술자_메모리))+15) & ^(uintptr)(0xF)))
	초기화블록.보내는버퍼서술자_주소 = uintptr(Pointer(&보내는버퍼_서술자))
	받은버퍼_서술자 = *(*([8]T버퍼서술자))(Pointer((uintptr((Pointer)(&받은버퍼들_서술자_메모리))+15) & ^(uintptr)(0xF)))
	초기화블록.받은버퍼_서술자_주소 = uintptr(Pointer(&받은버퍼_서술자))

	

	for i:=0; i<8; i++ {
		보내는버퍼_서술자[i].주소 = uint32((uintptr(Pointer(&보내는버퍼들[i])) + 15) & ^(uintptr(0xF))) 
		보내는버퍼_서술자[i].표시들 = 0x7FF | 0xF000
		보내는버퍼_서술자[i].표시들2 = 0
		보내는버퍼_서술자[i].활용여부 = 0

		받은버퍼_서술자[i].주소 = uint32((uintptr(Pointer(&받은버퍼들[i])) + 15) & ^(uintptr(0xF)))
		받은버퍼_서술자[i].표시들 = 0xF7FF | 0x80000000
	
	}

	레지스터_주소포트.M쓰기(1)
	레지스터_자료포트.M쓰기(uint16(uintptr(Pointer(&초기화블록))  & 0xFFFF ))

	레지스터_주소포트.M쓰기(2)
	레지스터_자료포트.M쓰기(uint16((uintptr(Pointer(&초기화블록)) >> 16) & 0xFFFF))

}
func (자신 *Tamd_am79c973) M활성화(){
        레지스터_주소포트.M쓰기(0)
        레지스터_자료포트.M쓰기(0x41)

        레지스터_주소포트.M쓰기(4)
        temp := 레지스터_자료포트.M읽기()
	레지스터_주소포트.M쓰기(4)
	레지스터_자료포트.M쓰기(temp | 0xC00)

	레지스터_주소포트.M쓰기(0)
	레지스터_자료포트.M쓰기(0x42)

}
func (자신 *Tamd_am79c973) M리셋() int{
	리셋포트.M읽기()	
	리셋포트.M쓰기(0)
	return 10
}
func (자신 *Tamd_am79c973) M인터럽트_처리(esp uint32) uint32{

	레지스터_주소포트.M쓰기(0)
	임시 := uint32(레지스터_자료포트.M읽기())

	if (임시 & 0x8000) == 0x8000 {
		콘솔.M출력(([]byte)("am79c973 error"))
	}
	if (임시 & 0x2000) == 0x2000 {
		콘솔.M출력(([]byte)("am79c973 collision error"))
	}
	if (임시 & 0x1000) == 0x1000 {
		콘솔.M출력(([]byte)("am79c973 missed frame"))
	}
	if (임시 & 0x0800) == 0x0800 {
		콘솔.M출력(([]byte)("am79c973 memory error"))
	}
	if (임시 & 0x0400) == 0x0400 {
		//콘솔.M출력(([]byte)("am79c973 data received"))
		자신.M받기()
	}
	if (임시 & 0x0200) == 0x0200 {
		//콘솔.M출력(([]byte)("am79c973 data sent"))
	}

	// ack	
	레지스터_주소포트.M쓰기(0)
	레지스터_자료포트.M쓰기(uint16(임시))

	if (임시 & 0x0100) == 0x0100 {
		콘솔.M출력(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (자신 *Tamd_am79c973) M보내기(자료주소 uintptr, 크기 uint32){
	//var 현재보내는버퍼 uint16 = uint16(현재보내는버퍼)
	현재보내는버퍼 = 0
	if(크기 > 1518) {
		크기 = 1518
	}
	
	var 원문버퍼 [4096] byte = *(*([4096]byte))(Pointer(자료주소))
	var 복사버퍼 uint32=보내는버퍼_서술자[현재보내는버퍼].주소 + 크기 -1
	for i:=0; i<int(크기); i++{
		*(*byte)(Pointer(uintptr(복사버퍼))) = 원문버퍼[int(크기)-i-1]
		복사버퍼--
	}


	var 자료 [4096] byte = *(*([4096]byte))(Pointer(자료주소))
	콘솔.M출력XY(([]byte)("send packet"), 0, 2)
	for i:=0; i<64; i++{
		콘솔.MHex출력(자료[i])
		콘솔.M출력(([]byte)(":"))
	}
	콘솔.M출력(([]byte)("\n"))


	보내는버퍼_서술자[현재보내는버퍼].활용여부 = 0
	보내는버퍼_서술자[현재보내는버퍼].표시들2 = 0
	보내는버퍼_서술자[현재보내는버퍼].표시들 = 0x8300F000 | uint32((-크기) & 0xFFF)
	

	레지스터_주소포트.M쓰기(0)
	레지스터_자료포트.M쓰기(0x48)
}
func (자신 *Tamd_am79c973) M받기(){

	현재받은버퍼 = 0

	for ; (받은버퍼_서술자[현재받은버퍼].표시들 & 0x80000000)==0; 현재받은버퍼=(현재받은버퍼+1)%8 {
		if !(받은버퍼_서술자[현재받은버퍼].표시들 & 0x40000000 != 0) &&
		   ((받은버퍼_서술자[현재받은버퍼].표시들 & 0x03000000) == 0x03000000) {

			var 크기 uint32 = 받은버퍼_서술자[현재받은버퍼].표시들 & 0xFFF
			if 크기 > 64 { // remove checksum
				크기 -= 4
			}

			var 버퍼 [4096]byte= *(*([4096]byte))(Pointer(uintptr(받은버퍼_서술자[현재받은버퍼].주소)))
			var 주소 uintptr = uintptr(Pointer(&버퍼))
			if i원시자료_처리기 != nil {
				if i원시자료_처리기.M원시자료_받는동시(주소, 크기) {
					var 주소 uintptr = uintptr(Pointer(&버퍼))
					자신.M보내기(주소, 크기)
				}
			}

			var 자료 [4096] byte = *(*([4096]byte))(Pointer(&버퍼))
			콘솔.M출력XY(([]byte)("recv packet"), 0, 6)
			for i:=0; i<64; i++{
				콘솔.MHex출력(자료[i])
				콘솔.M출력(([]byte)(":"))
			}
			콘솔.M출력(([]byte)("\n"))

		}
		받은버퍼_서술자[현재받은버퍼].표시들2=0
		받은버퍼_서술자[현재받은버퍼].표시들=0x8000F7FF 
	}
}
func (자신 *Tamd_am79c973)M처리기_설정(원시자료_처리기 *T원시자료_처리기){
	자신.원시자료_처리기 = 원시자료_처리기
}
func (자신 *Tamd_am79c973)M맥주소_갖기() uint64{
	return 초기화블록.물리주소
}
func (자신 *Tamd_am79c973)M아이피주소_설정(아이피주소 uint64){
	초기화블록.논리주소 = 아이피주소
}
func (자신 *Tamd_am79c973)M아이피주소_갖기() uint64{
	return 초기화블록.논리주소
}
