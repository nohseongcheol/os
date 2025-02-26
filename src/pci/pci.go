/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package pci

//import . "unsafe"
//import . "기억공간관리자"
//import . "amd_am79c973"
import . "port"
import . "interrupt"
import . "단말기"
import . "구동장치들/장치제어기관리자"

/////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//		Register = 기록회로
//		BaseAddress = 기준주소
//		BUS = 공유전송매체(공유전송회로)
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////
type I주변부품연결제어기_처리기 interface{
	M구동장치_갖은동시(장치서술자 T주변부품연결장치_서술자)
}
var i주변부품연결제어기_처리기 I주변부품연결제어기_처리기
type T기본주변부품연결제어기_처리기 struct{
}
func (자신 T기본주변부품연결제어기_처리기) M구동장치_갖은동시(장치서술자 T주변부품연결장치_서술자) {
}

type T기준주소_기록회로 struct {		// BaseAddressRegister
	선행입출가능 bool			// prefetchable
	주소 uint32				// address
	기록회로_유형 uint8			// register type
}
type T주변부품연결장치_서술자 struct {
	P입출력단자기준 uint32
	P개입중단 uint32
	
	공용전송회로 uint16
	장치 uint16			// device
	함수 uint16			// function
	
	P판매회사_식별자 uint16		// vendor id
	P장치_식별자 uint16		// device id

	종류_식별자 uint8		// class id
	부종류_식별자 uint8		// subclass id
	접속_식별자 uint8		// interface id

	변경 uint8			// revision
	
}

func (자신 *T주변부품연결장치_서술자) Init() {
}

//////////////////////////////////////////////////////////////////////////////
type T주변부품연결제어기 struct {
	i주변부품연결제어기_처리기 I주변부품연결제어기_처리기
	자료입출력단자 T두배워드입출력단자
	명령입출력단자 T두배워드입출력단자
}

func (자신 *T주변부품연결제어기) M초기화(i주변부품연결제어기_처리기 I주변부품연결제어기_처리기) {
	자신.자료입출력단자.M초기화(0xCFC)
	자신.명령입출력단자.M초기화(0xCF8)
	
	자신.i주변부품연결제어기_처리기 = T기본주변부품연결제어기_처리기{}
	if i주변부품연결제어기_처리기 != nil{
		자신.i주변부품연결제어기_처리기 = i주변부품연결제어기_처리기
	}
}
func (자신 *T주변부품연결제어기) M읽기(공용전송회로 uint16, 장치 uint16, 함수 uint16, registeroffset uint32) uint32{
	var id uint32 = 0
	id = 0x1<<31 | (uint32(공용전송회로 & 0xFF) << 16)  | (uint32(장치 & 0x1f) << 11) | (uint32(함수 & 0x07) << 8) | uint32(registeroffset & 0xFC)

	자신.명령입출력단자.M쓰기(id)
	
	결과1 := 자신.자료입출력단자.M읽기()
	결과2 := (결과1 >> (8*(registeroffset %4)))

	return 결과2
}

func (자신 *T주변부품연결제어기) M쓰기(공용전송회로 uint16, 장치 uint16, 함수 uint16, registeroffset uint32, 값 uint32) {
	var id uint32
	id = 0x1 << 31 | uint32((공용전송회로 & 0xFF) << 16)  | uint32((장치 & 0x1f) << 11) | uint32((함수 & 0x07) << 8) | uint32(registeroffset & 0xFC)
	자신.명령입출력단자.M쓰기(id)
	자신.자료입출력단자.M쓰기(값)
}
func (자신 *T주변부품연결제어기) DeviceHasFunctions(공용전송회로 uint16, 장치 uint16) bool{
	결과 := 자신.M읽기(공용전송회로, 장치, 0, 0x0E)
	if (결과 & (1<<7)) != 0 {
		return true
	}else {
		return false
	}
}
var 단말기 T단말기 = T단말기{}
func (자신 *T주변부품연결제어기) M장치제어기들_선택(장치제어기_관리자 *T장치제어기_관리자, 개입중단들 *T개입중단_관리자) {
	for 공용전송회로:=0; 공용전송회로<8; 공용전송회로++ {
		for 장치:=0; 장치<32; 장치++ {

			var 함수갯수 int = 1
			if 자신.DeviceHasFunctions(uint16(공용전송회로), uint16(장치)) == true {
				함수갯수 = 8
			}else{
				함수갯수 = 1
			}
		

			for 함수:=0; 함수<함수갯수; 함수++ {
				var 장치서술자 T주변부품연결장치_서술자
				장치서술자 = 자신.M장치서술자_갖기(uint16(공용전송회로), uint16(장치), uint16(함수))
				if 장치서술자.P판매회사_식별자 == 0x0000 || 장치서술자.P판매회사_식별자 == 0xFFFF {
					continue
				}
	
				for 기본주소_기록회로_번호:=0; 기본주소_기록회로_번호<6; 기본주소_기록회로_번호++ {
					var 기준주소_기록회로 T기준주소_기록회로 = 자신.M기본주소회로_갖기(uint16(공용전송회로), uint16(장치), uint16(함수), uint16(기본주소_기록회로_번호))
					if 기준주소_기록회로.주소 != 0 && (기준주소_기록회로.기록회로_유형 == 1) { // 기준주소_기록회로.기록회로_유형 == inputoutput
						장치서술자.P입출력단자기준 = 기준주소_기록회로.주소
					}
				
					자신.M구동장치_갖기(장치서술자, 개입중단들)
			
				}

			}

		}
	}
}
func (자신 *T주변부품연결제어기) M장치서술자_갖기(공용전송회로 uint16, 장치 uint16, 함수 uint16) T주변부품연결장치_서술자{
	var 주변부품연결장치_서술자 T주변부품연결장치_서술자
	주변부품연결장치_서술자 = T주변부품연결장치_서술자{}
	주변부품연결장치_서술자.공용전송회로 = 공용전송회로
	주변부품연결장치_서술자.장치 = 장치
	주변부품연결장치_서술자.함수 = 함수

	주변부품연결장치_서술자.P판매회사_식별자 = uint16(자신.M읽기(공용전송회로, 장치, 함수, 0x00))
	주변부품연결장치_서술자.P장치_식별자 = uint16(자신.M읽기(공용전송회로, 장치, 함수, 0x02))

	주변부품연결장치_서술자.종류_식별자 = uint8(자신.M읽기(공용전송회로, 장치, 함수, 0x0b))
	주변부품연결장치_서술자.부종류_식별자 = uint8(자신.M읽기(공용전송회로, 장치, 함수, 0x0a))
	주변부품연결장치_서술자.접속_식별자 = uint8(자신.M읽기(공용전송회로, 장치, 함수, 0x09))

	주변부품연결장치_서술자.변경 = uint8(자신.M읽기(공용전송회로, 장치, 함수, 0x08))
	주변부품연결장치_서술자.P개입중단 = uint32(자신.M읽기(공용전송회로, 장치, 함수, 0x3C))

	return 주변부품연결장치_서술자
}
func (자신 *T주변부품연결제어기) M기본주소회로_갖기(공용전송회로 uint16, 장치 uint16, 함수 uint16, bar uint16) T기준주소_기록회로 {
	var 결과 T기준주소_기록회로
	
	머리말_유형 := 자신.M읽기(공용전송회로, 장치, 함수, 0x0E) & 0x7F
	var 최대기준주소_기록회로들 int = int(6-(4*머리말_유형))
	if bar >= uint16(최대기준주소_기록회로들) {
		return 결과
	}

	기준주소기록회로_값 := 자신.M읽기(공용전송회로, 장치, 함수, uint32(0x10+4*bar))

	if (기준주소기록회로_값 & 0x1) != 0 {
		결과.기록회로_유형 = 1
	} else {
		결과.기록회로_유형 = 0
	}

	if 결과.기록회로_유형 == 0 { // memorymapping
	} else {
		결과.주소 = 기준주소기록회로_값 & ^uint32(0x3)
		결과.선행입출가능 = false
	}

	return 결과
}
func (자신 *T주변부품연결제어기) M구동장치_갖기(장치서술자 T주변부품연결장치_서술자, interrupts *T개입중단_관리자) {//IDriver {
	//var iDriver IDriver = nil

	자신.i주변부품연결제어기_처리기.M구동장치_갖은동시(장치서술자)
	/*
	switch 장치서술자.P판매회사_식별자 {
		case 0x1022:	 // AMD
			switch 장치서술자.P장치_식별자 {
				case 0x2000:
					//iDriver = *(*IDriver)(Pointer(활성기억공간관리자.MM할당(100)))
					if iDriver != nil {
						//(IDriver) amd_am79c973.Init(&장치서술자, interrupts)
					}
					return iDriver
					break
			}
			break

		case 0x8086:	//INTEL
			break
	}

	switch 장치서술자.종류_식별자 {
		case 0x03:
			switch 장치서술자.부종류_식별자 {
				case 0x00: // vga	
				break
			}
			break
	}
	return iDriver
	*/

}
