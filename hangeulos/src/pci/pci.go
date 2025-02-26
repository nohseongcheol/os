/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package pci

//import . "unsafe"
//import . "memorymanager"
import . "port"
import . "interrupt"
import . "콘솔"
import . "drivers/드라이버"

/////////////////////////////////////////////////////////////////////////////////////
//
//	주변부품연결컨트롤러 = PeripheralComponentInterconnectController
//
////////////////////////////////////////////////////////////////////////////////////
type I주변부품연결컨트롤러_처리기 interface{
	M드라이버_갖는동시(dev T주변부품연결장치_서술자)
}
var i주변부품연결컨트롤러_처리기 I주변부품연결컨트롤러_처리기
type T기본주변부품연결컨트롤러_처리기 struct{
}
func (자신 T기본주변부품연결컨트롤러_처리기) M드라이버_갖는동시(dev T주변부품연결장치_서술자) {
}

type T기준주소_레지스터 struct {	// BaseAddressRegister
	선행입출가능 bool		// prefatchable
	주소 uint32			// address
	레지스터타입 uint8		// register type
}
type T주변부품연결장치_서술자 struct {
	P포트베이스 uint32		// PortBase
	P인터럽트 uint32		// Interrupt
	
	버스 uint16			// bus
	디바이스 uint16 		// device
	함수 uint16			// function
	
	P벤더_아이디 uint16		// vendor_id
	P디바이스_아이디 uint16		// device_id

	클래스_아이디 uint8		// class_id
	부클래스_아이디 uint8		// subclass_id
	인터페이스_아이디 uint8		// interface_id

	리비전 uint8			// revision
	
}

func (자신 *T주변부품연결장치_서술자) M초기화() {
}

//////////////////////////////////////////////////////////////////////////////
type T주변부품연결컨트롤러 struct {
	i주변부품연결컨트롤러_처리기 I주변부품연결컨트롤러_처리기
	자료포트 T더블워드포트
	명령포트 T더블워드포트
}

func (자신 *T주변부품연결컨트롤러) M초기화(i주변부품연결컨트롤러_처리기 I주변부품연결컨트롤러_처리기) {
	자신.자료포트.M초기화(0xCFC)
	자신.명령포트.M초기화(0xCF8)
	
	자신.i주변부품연결컨트롤러_처리기 = T기본주변부품연결컨트롤러_처리기{}
	if i주변부품연결컨트롤러_처리기 != nil{
		자신.i주변부품연결컨트롤러_처리기 = i주변부품연결컨트롤러_처리기
	}
}
func (자신 *T주변부품연결컨트롤러) M읽기(버스 uint16, 디바이스 uint16, 함수 uint16, 레지스터_오프셋 uint32) uint32{
	var 아이디 uint32 = 0
	아이디 = 0x1<<31 | (uint32(버스 & 0xFF) << 16)  | (uint32(디바이스 & 0x1f) << 11) | (uint32(함수 & 0x07) << 8) | uint32(레지스터_오프셋 & 0xFC)

	자신.명령포트.M쓰기(아이디)
	
	결과1 := 자신.자료포트.M읽기()
	결과2 := (결과1 >> (8*(레지스터_오프셋 %4)))

	return 결과2
}

func (자신 *T주변부품연결컨트롤러) M쓰기(버스 uint16, 디바이스 uint16, 함수 uint16, 레지스터_오프셋 uint32, 값 uint32) {
	var 아이디 uint32
	아이디 = 0x1 << 31 | uint32((버스 & 0xFF) << 16)  | uint32((디바이스 & 0x1f) << 11) | uint32((함수 & 0x07) << 8) | uint32(레지스터_오프셋 & 0xFC)
	자신.명령포트.M쓰기(아이디)
	자신.자료포트.M쓰기(값)
}
func (자신 *T주변부품연결컨트롤러) DeviceHasFunctions(버스 uint16, 디바이스 uint16) bool{
	결과 := 자신.M읽기(버스, 디바이스, 0, 0x0E)
	if (결과 & (1<<7)) != 0 {
		return true
	}else {
		return false
	}
}
var 콘솔 T콘솔 = T콘솔{}
func (자신 *T주변부품연결컨트롤러) M드라이버들선택(드라이버_관리자 *T드라이버관리자, 인터럽트들 *T인터럽트_관리자) {
	for 버스:=0; 버스<8; 버스++ {
		for 디바이스:=0; 디바이스<32; 디바이스++ {

			var 함수들_갯수 int = 1
			if 자신.DeviceHasFunctions(uint16(버스), uint16(디바이스)) == true {
				함수들_갯수 = 8
			}else{
				함수들_갯수 = 1
			}
		

			for 함수:=0; 함수<함수들_갯수; 함수++ {
				var 디바이스서술자 T주변부품연결장치_서술자
				디바이스서술자 = 자신.M장비서술자_갖기(uint16(버스), uint16(디바이스), uint16(함수))
				if 디바이스서술자.P벤더_아이디 == 0x0000 || 디바이스서술자.P벤더_아이디 == 0xFFFF {
					continue
				}
	
				for 기준주소레지스터_번호:=0; 기준주소레지스터_번호<6; 기준주소레지스터_번호++ {
					var 기준주소_레지스터 T기준주소_레지스터 = 자신.기준주소_레지스터_갖기(uint16(버스), uint16(디바이스), uint16(함수), 
															uint16(기준주소레지스터_번호))
					if 기준주소_레지스터.주소 != 0 && (기준주소_레지스터.레지스터타입 == 1) { // 기준주소_레지스터.레지스터타입 == inputoutput
						디바이스서술자.P포트베이스 = 기준주소_레지스터.주소
					}
				
					자신.M드라이버_갖기(디바이스서술자, 인터럽트들)
			
				}

			}

		}
	}
}
func (자신 *T주변부품연결컨트롤러) M장비서술자_갖기(버스 uint16, 디바이스 uint16, 함수 uint16) T주변부품연결장치_서술자{
	var 주변부품연결장치_서술자 T주변부품연결장치_서술자
	주변부품연결장치_서술자 = T주변부품연결장치_서술자{}
	주변부품연결장치_서술자.버스 = 버스
	주변부품연결장치_서술자.디바이스 = 디바이스
	주변부품연결장치_서술자.함수 = 함수

	주변부품연결장치_서술자.P벤더_아이디 = uint16(자신.M읽기(버스, 디바이스, 함수, 0x00))
	주변부품연결장치_서술자.P디바이스_아이디 = uint16(자신.M읽기(버스, 디바이스, 함수, 0x02))

	주변부품연결장치_서술자.클래스_아이디 = uint8(자신.M읽기(버스, 디바이스, 함수, 0x0b))
	주변부품연결장치_서술자.부클래스_아이디 = uint8(자신.M읽기(버스, 디바이스, 함수, 0x0a))
	주변부품연결장치_서술자.인터페이스_아이디 = uint8(자신.M읽기(버스, 디바이스, 함수, 0x09))

	주변부품연결장치_서술자.리비전 = uint8(자신.M읽기(버스, 디바이스, 함수, 0x08))
	주변부품연결장치_서술자.P인터럽트 = uint32(자신.M읽기(버스, 디바이스, 함수, 0x3C))

	return 주변부품연결장치_서술자
}
func (자신 *T주변부품연결컨트롤러) 기준주소_레지스터_갖기(버스 uint16, 디바이스 uint16, 함수 uint16, 기준주소_레지스터 uint16) T기준주소_레지스터 {
	var 결과 T기준주소_레지스터
	
	헤더타입 := 자신.M읽기(버스, 디바이스, 함수, 0x0E) & 0x7F
	var 최대기준주소_레지스터들 int = int(6-(4*헤더타입))
	if 기준주소_레지스터 >= uint16(최대기준주소_레지스터들) {
		return 결과
	}

	기준주소_레지스터_값 := 자신.M읽기(버스, 디바이스, 함수, uint32(0x10+4*기준주소_레지스터))

	if (기준주소_레지스터_값 & 0x1) != 0 {
		결과.레지스터타입 = 1
	} else {
		결과.레지스터타입 = 0
	}

	if 결과.레지스터타입 == 0 { // memorymapping
	} else {
		결과.주소 = 기준주소_레지스터_값 & ^uint32(0x3)
		결과.선행입출가능 = false
	}

	return 결과
}
func (자신 *T주변부품연결컨트롤러) M드라이버_갖기(연결디바이스_서술자 T주변부품연결장치_서술자, interrupts *T인터럽트_관리자) {//IDriver {

	자신.i주변부품연결컨트롤러_처리기.M드라이버_갖는동시(연결디바이스_서술자)
	/*
	switch dev.P벤더_아이디 {
		case 0x1022:	 // AMD
			switch dev.P디바이스_아이디 {
				case 0x2000:
					//iDriver = *(*IDriver)(Pointer(ActiveMemoryManager.Malloc(100)))
					if iDriver != nil {
						//(IDriver) amd_am79c973.M초기화(&dev, interrupts)
					}
					return iDriver
					break
			}
			break

		case 0x8086:	//INTEL
			break
	}

	switch dev.클래스_아이디 {
		case 0x03:
			switch dev.부클래스_아이디 {
				case 0x00: // vga	
				break
			}
			break
	}
	return iDriver
	*/

}
