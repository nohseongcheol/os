/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package  tcp

import . "unsafe"
import . "util"
import . "memorymanager"
import . "net/ipv4" 

//////////////////////////////////////////////////////////////////////////
//
//	TCP = Transmission Control Protocol = 전송제어프로토콜
//	Socket = 소켓
//	PortNumber = 입출력번호
//	Client = 클라이언트
//	Server = 서버 
//	Listen = 수신대기
//	Bind = 결합하기
//
//////////////////////////////////////////////////////////////////////////

const (
	CLOSED uint8 = 1
	LISTEN uint8 = 2
	SYN_SENT uint8 = 3
	SYN_RECEIVED uint8 = 4

	ESTABLISHED uint8 = 5

	FIN_WAIT1 uint8 = 6
	FIN_WAIT2 uint8 = 7
	CLOSING uint8 = 8
	TIME_WAIT uint8 = 9

	CLOSE_WAIT uint8 = 10
)
type TCPFlags byte
const (
	FIN  TCPFlags = 1
	SYN  TCPFlags = 2
	RST  TCPFlags = 4
	PSH  TCPFlags = 8
	ACK  TCPFlags = 16
	URG  TCPFlags = 32
	/*
	ECE  TCPFlags = 64
	CWR  TCPFlags = 128
	NS  TCPFlags = 256
	*/
)


type T전송제어프로토콜_머리말_임시저장공간 struct{
	출발지포트번호 [2]byte
	목적지포트번호 [2]byte
	순서번호 [4] byte
	응답번호 [4] byte

	헤더크기 byte
	표시들 byte
	
	윈도우크기 [2] byte
	검사합 [2] byte
	긴급자료지시자 [2] byte

	옵션 [4] byte
}
var 전송제어프로토콜_머리말_크기 uint16 = uint16(Sizeof(T전송제어프로토콜_머리말_임시저장공간{}))
type T전송제어프로토콜_머리말 struct{
	출발지포트번호 uint16
	목적지포트번호 uint16
	순서번호 uint32
	응답번호 uint32
	
	헤더크기 uint8
	표시들 uint8

	윈도우크기 uint16
	검사합 uint16
	긴급자료지시자 uint16
	
	옵션 uint32
}
func (자신 *T전송제어프로토콜_머리말)M초기화(임시저장공간 *T전송제어프로토콜_머리말_임시저장공간){
	자신.출발지포트번호 = ArrayToUint16(임시저장공간.출발지포트번호)
	자신.목적지포트번호 = ArrayToUint16(임시저장공간.목적지포트번호)
	자신.순서번호 = ArrayToUint32(임시저장공간.순서번호)
	자신.응답번호 = ArrayToUint32(임시저장공간.응답번호)

	자신.헤더크기 = 임시저장공간.헤더크기
	자신.표시들 = 임시저장공간.표시들

	자신.윈도우크기 = ArrayToUint16(임시저장공간.윈도우크기)
	자신.검사합 = ArrayToUint16(임시저장공간.검사합)
	자신.긴급자료지시자 = ArrayToUint16(임시저장공간.긴급자료지시자)

	자신.옵션 = ArrayToUint32(임시저장공간.옵션)
}
func (자신 *T전송제어프로토콜_머리말)M임시저장공간_설정(임시저장공간 *T전송제어프로토콜_머리말_임시저장공간){
	임시저장공간.출발지포트번호 = Uint16ToArray(자신.출발지포트번호)
	임시저장공간.목적지포트번호 = Uint16ToArray(자신.목적지포트번호)
	임시저장공간.순서번호 = Uint32ToArray(자신.순서번호)
	임시저장공간.응답번호 = Uint32ToArray(자신.응답번호)

	임시저장공간.헤더크기 = 자신.헤더크기
	임시저장공간.표시들 = 자신.표시들

	임시저장공간.윈도우크기 = Uint16ToArray(자신.윈도우크기)
	임시저장공간.검사합 = Uint16ToArray(자신.검사합)
	임시저장공간.긴급자료지시자 = Uint16ToArray(자신.긴급자료지시자)

	임시저장공간.옵션 = Uint32ToArray(자신.옵션)
}

type 전송제어프로토콜_유사_머리말_임시저장공간 struct{
	출발지IP주소 [4] byte
	목적지IP주소 [4] byte
	규약 [2] byte
	전체길이 [2] byte
}
var 전송제어프로토콜_유사_머리말_크기 uint16 = uint16(Sizeof(전송제어프로토콜_유사_머리말_임시저장공간{}))
type 전송제어프로토콜_유사_머리말 struct{
	출발지IP주소 uint32
	목적지IP주소 uint32
	규약 uint16
	전체길이 uint16
}
func (자신 *전송제어프로토콜_유사_머리말) M초기화(buffer *전송제어프로토콜_유사_머리말_임시저장공간){
	자신.출발지IP주소 = ArrayToUint32(buffer.출발지IP주소)
	자신.목적지IP주소 = ArrayToUint32(buffer.목적지IP주소)
	자신.규약 = ArrayToUint16(buffer.규약)
	자신.전체길이 = ArrayToUint16(buffer.전체길이)
}
func (자신 *전송제어프로토콜_유사_머리말) M임시저장공간_설정(임시저장공간 *전송제어프로토콜_유사_머리말_임시저장공간){
	임시저장공간.출발지IP주소 = Uint32ToArray(자신.출발지IP주소)
	임시저장공간.목적지IP주소 = Uint32ToArray(자신.목적지IP주소)
	임시저장공간.규약 = Uint16ToArray(자신.규약)
	임시저장공간.전체길이 = Uint16ToArray(자신.전체길이)
}

////////////////////////////////////////////////////////////////////////////////////
type I클라이언트_전송제어프로토콜_처리기 interface{
	M연결성립_동시(소켓 *T전송제어프로토콜_소켓)
	M자료받은동시(자료 []byte, 크기 uint32)
}
type T클라이언트_전송제어프로토콜_처리기 struct{
}
func (자신 *T클라이언트_전송제어프로토콜_처리기) M연결성립_동시(소켓 *T전송제어프로토콜_소켓){
}
func (자신 *T클라이언트_전송제어프로토콜_처리기) M자료받은동시(자료 []byte, 크기 uint32){
}

type I서버_전송제어프로토콜_처리기 interface{
	M연결성립_동시(소켓 *T전송제어프로토콜_소켓)
	M자료받은동시(자료 []byte, 크기 uint32)
}
type T서버_전송제어프로토콜_처리기 struct{
}
func (자신 *T서버_전송제어프로토콜_처리기) M연결성립_동시(소켓 *T전송제어프로토콜_소켓){
}
func (자신 *T서버_전송제어프로토콜_처리기) M자료받은동시(자료 []byte, 크기 uint32){
}
////////////////////////////////////////////////////////////////////////////////////
type T전송제어프로토콜_처리기 struct{
}
func (자신 *T전송제어프로토콜_처리기) M전송제어프로토콜_메시지_처리기(소켓 *T전송제어프로토콜_소켓, 자료 uintptr, 크기 uint16) bool{
	return true
}

////////////////////////////////////////////////////////////////////////////////////
type T전송제어프로토콜_소켓 struct{
	원격입출구번호 uint16
	원격IP주소 uint32
	자신입출구번호 uint16
	자신IP주소 uint32
	순서번호 uint32
	응답번호 uint32

	후단부 *T전송제어프로토콜_제공자
	처리기 *T전송제어프로토콜_처리기

	상태 uint8

}
var 소켓자료 T전송제어프로토콜_소켓
func (자신 *T전송제어프로토콜_소켓) M초기화(후단부 *T전송제어프로토콜_제공자){
	자신.후단부 = 후단부
	자신.처리기 = nil
	자신.상태 = CLOSED
}
func (자신 *T전송제어프로토콜_소켓) M전송제어프로토콜_메시지_처리기(자료 uintptr, 크기 uint16) bool{
	if 자신.처리기 != nil {
		return 자신.처리기.M전송제어프로토콜_메시지_처리기(자신, 자료, 크기)
	}
	return false
}
func (자신 *T전송제어프로토콜_소켓) M보내기(자료 []byte, 크기 uint16){

	var 주소 = uintptr(Pointer(&자료))
	자신.후단부.M보내기(자신, 주소, 크기, uint16(PSH|ACK))
}
func (자신 *T전송제어프로토콜_소켓) M연결끊기(){
	자신.후단부.M연결끊기(자신)
}
////////////////////////////////////////////////////////////////////////////////////
type T전송제어프로토콜_제공자_자료 struct{
	소켓들 [65535] *T전송제어프로토콜_소켓
	소켓갯수들 uint16
	여유포트번호 uint16
	
	전송제어프로토콜_처리기 T전송제어프로토콜_처리기
	클라이언트_전송제어프로토콜_처리기 I클라이언트_전송제어프로토콜_처리기
	서버_전송제어프로토콜_처리기 I서버_전송제어프로토콜_처리기
	
}
var 자료 T전송제어프로토콜_제공자_자료

type T전송제어프로토콜_제공자 struct{
	T인터넷규약_처리기
}
func (자신 *T전송제어프로토콜_제공자) M초기화(후단부 T인터넷규약_제공자, 클라이언트_전송제어프로토콜_처리기 I클라이언트_전송제어프로토콜_처리기){

	if 클라이언트_전송제어프로토콜_처리기 != nil {
		자료.클라이언트_전송제어프로토콜_처리기 = 클라이언트_전송제어프로토콜_처리기
	} else{
		자료.클라이언트_전송제어프로토콜_처리기 = &T클라이언트_전송제어프로토콜_처리기{}	
	}

	자신.T인터넷규약_처리기.M초기화(후단부, 자신, 0x06)
	자료.클라이언트_전송제어프로토콜_처리기 = 클라이언트_전송제어프로토콜_처리기
	for i:=0; i<65535; i++{
		자료.소켓들[i] = nil
	}
	자료.소켓갯수들 = 0
	자료.여유포트번호 = 1024

}
func (자신 *T전송제어프로토콜_제공자) M인터넷규약_받은동시(출발지IP주소_BE uint32, 목적지IP주소_BE uint32, 인터넷프로토콜_페이로드 uintptr, 크기 uint32) bool{
	if 크기 < 20{
		return false
	}

	var 메시지_임시저장공간 = (*T전송제어프로토콜_머리말_임시저장공간)(Pointer(인터넷프로토콜_페이로드))
	var 메시지 = T전송제어프로토콜_머리말{}
	메시지.M초기화(메시지_임시저장공간)
	

	var 소켓  *T전송제어프로토콜_소켓 = nil

	var i = 0	
	for i=0; i<int(자료.소켓갯수들) && 소켓 == nil; i++ {
		if 자료.소켓들[i].자신입출구번호 == Uint16_R(메시지.목적지포트번호) &&
			자료.소켓들[i].자신IP주소 == 목적지IP주소_BE &&
			자료.소켓들[i].상태 == LISTEN &&
			//((TCPFlags(메시지.표시들) & (SYN | ACK)) == SYN) {
			((메시지.표시들 & uint8(SYN | ACK)) == uint8(SYN)) {
				소켓 = 자료.소켓들[i]
		}else if 자료.소켓들[i].자신입출구번호 == Uint16_R(메시지.목적지포트번호) &&
			자료.소켓들[i].자신IP주소 == 목적지IP주소_BE &&
			자료.소켓들[i].원격입출구번호 == Uint16_R(메시지.출발지포트번호) &&
			자료.소켓들[i].원격IP주소 == 출발지IP주소_BE {
				소켓 = 자료.소켓들[i]
		}
	
	}
	

	var 재설정 = false
	
	if 소켓 != nil && ((메시지.표시들 & uint8(RST)) != 0) {
		소켓.상태 = CLOSED
	}


	if 소켓 != nil && 소켓.상태 != CLOSED {
		//switch TCPFlags(메시지.표시들) & (SYN | ACK | FIN) {
		switch 메시지.표시들 {
		case uint8(SYN):
			if 소켓.상태 == LISTEN {
				소켓.상태 = SYN_RECEIVED
				소켓.원격입출구번호 = Uint16_R(메시지.출발지포트번호)
				소켓.원격IP주소 = 출발지IP주소_BE
				소켓.응답번호 = 메시지.순서번호 + 1
				소켓.순서번호 = 0xbeefcafe

				자신.M보내기(소켓, 0, 0, uint16(SYN|ACK))
				소켓.순서번호++

			}else{
				재설정 = true
			}

		case uint8(SYN | ACK):
			if 소켓.상태 == SYN_SENT {
				소켓.상태 = ESTABLISHED
				소켓.응답번호 = 메시지.순서번호 + 1
				소켓.순서번호++
				자신.M보내기(소켓, 0, 0, uint16(ACK))
			
				자료.클라이언트_전송제어프로토콜_처리기.M연결성립_동시(소켓)

			}else{
				재설정 = true
			}

		case uint8(SYN | FIN) :
			fallthrough
		case uint8(SYN | FIN | ACK) :
			재설정 = true

		case uint8(FIN):
			fallthrough
		case uint8(FIN | ACK):
			if 소켓.상태 == ESTABLISHED {
				소켓.상태 = CLOSE_WAIT
				소켓.응답번호++
				자신.M보내기(소켓, 0, 0, uint16(ACK))
				자신.M보내기(소켓, 0, 0, uint16(FIN|ACK))
			}else if 소켓.상태 == CLOSE_WAIT {
				소켓.상태 = CLOSED
			}else if 소켓.상태 == FIN_WAIT1 || 
					소켓.상태 == FIN_WAIT2 {
				소켓.상태 = CLOSED
				소켓.응답번호++
				자신.M보내기(소켓, 0, 0, uint16(ACK))
			}else{
				재설정 = true
			}

		case uint8(ACK):

			if 소켓.상태 == SYN_RECEIVED {
				소켓.상태 = ESTABLISHED
				자료.서버_전송제어프로토콜_처리기.M연결성립_동시(소켓)
				return false
			}else if 소켓.상태 == FIN_WAIT1 {
				소켓.상태 = FIN_WAIT2
				return false
			}else if 소켓.상태 == CLOSE_WAIT {
				소켓.상태 = CLOSED
				break
			}

			if TCPFlags(메시지.표시들) == ACK {
				break
			}
			fallthrough
		default:
			if 메시지.순서번호 == 소켓.응답번호 {
				재설정 = !(소켓.M전송제어프로토콜_메시지_처리기(인터넷프로토콜_페이로드 + uintptr(메시지.헤더크기*4), uint16(크기-uint32(메시지.헤더크기*4))))
				if !재설정 {
					var x uint8 = 0
					var 탑재_바이트들 []byte = *(*[]byte)(Pointer(인터넷프로토콜_페이로드))
					자료.클라이언트_전송제어프로토콜_처리기.M자료받은동시(탑재_바이트들, 크기)
					자료.서버_전송제어프로토콜_처리기.M자료받은동시(탑재_바이트들, 크기)
					for i:=int(메시지.헤더크기*4); i<int(크기); i++{
						if 탑재_바이트들[i] != 0 {
							x = uint8(i)
						}
					}
					소켓.응답번호 += uint32(x - 메시지.헤더크기*4 + 1)
					자신.M보내기(소켓, 0, 0, uint16(ACK))
				}else{
					재설정 = true
				}

			}
		}

	}
	if 재설정 {
		if 소켓 != nil {
			자신.M보내기(소켓, 0, 0, uint16(RST))
		}else{
			var 소켓 T전송제어프로토콜_소켓
			소켓.원격입출구번호 = 메시지.출발지포트번호
			소켓.원격IP주소 = 출발지IP주소_BE
			소켓.자신입출구번호 = 메시지.목적지포트번호
			소켓.자신IP주소 = 목적지IP주소_BE
			소켓.순서번호 = Uint32_R(메시지.응답번호)
			소켓.응답번호 = Uint32_R(메시지.순서번호) + 1
			자신.M보내기(&소켓, 0, 0, uint16(RST))
		}
	}

	if 소켓 != nil && 소켓.상태 == CLOSED {
		for i:=0; i<int(자료.소켓갯수들) && 소켓 == nil; i++ {
			if 자료.소켓들[i] == 소켓 {
				자료.소켓갯수들--
				자료.소켓들[i] = 자료.소켓들[자료.소켓갯수들]
				break
			}
		}
	}

	return false
}
func (자신 *T전송제어프로토콜_제공자) M보내기(소켓 *T전송제어프로토콜_소켓, 자료 uintptr, 크기 uint16, 표시들 uint16){
	
	var 전체길이 = 크기 + 전송제어프로토콜_머리말_크기
	var lengthInclPHdr = 전체길이 + 전송제어프로토콜_유사_머리말_크기

	var 임시저장공간 [4096]byte

	var 유사머리말_임시저장공간 = (*전송제어프로토콜_유사_머리말_임시저장공간)(Pointer(&임시저장공간))
	var 메시지_임시저장공간 = (*T전송제어프로토콜_머리말_임시저장공간)(Pointer(&임시저장공간[전송제어프로토콜_유사_머리말_크기]))
	

	var 메시지 = T전송제어프로토콜_머리말{}
	메시지.헤더크기 = uint8(전송제어프로토콜_머리말_크기/4) << 4
	메시지.출발지포트번호 = 소켓.자신입출구번호
	메시지.목적지포트번호 = 소켓.원격입출구번호

	메시지.응답번호 = Uint32_R(소켓.응답번호)
	메시지.순서번호 = Uint32_R(소켓.순서번호)
	메시지.표시들 = uint8(표시들 & 0x00FF)
	메시지.윈도우크기 = 0xFFFF
	메시지.긴급자료지시자 = 0


	if (TCPFlags(표시들) & SYN) != 0 {
		메시지.옵션 = 0xB4050402
	}else{
		메시지.옵션 = 0
	}

	소켓.순서번호 += uint32(크기)

	var 자료바이트들 = *(*[]byte)(Pointer(자료))
	for i:=0; i<int(크기); i++{
		임시저장공간[int(전송제어프로토콜_머리말_크기+전송제어프로토콜_유사_머리말_크기)+i] = 자료바이트들[i]
	}

	var 유사_머리말 = 전송제어프로토콜_유사_머리말{}

	유사_머리말.출발지IP주소 = 소켓.자신IP주소
	유사_머리말.목적지IP주소 = 소켓.원격IP주소
	유사_머리말.규약 = 0x0600
	유사_머리말.전체길이 = Uint16_R(전체길이)
	유사_머리말.M임시저장공간_설정(유사머리말_임시저장공간)

	메시지.검사합 = 0
	메시지.M임시저장공간_설정(메시지_임시저장공간)
	메시지.검사합 = 자신.T인터넷규약_처리기.M제공자_갖기().M검사합((*([4096]uint16))(Pointer(&임시저장공간)), uint32(lengthInclPHdr))
	메시지.M임시저장공간_설정(메시지_임시저장공간)
	var 자료주소 = uintptr(Pointer(메시지_임시저장공간))


	자신.T인터넷규약_처리기.M패킷보내기(소켓.원격IP주소, 0x06, 자료주소, uint32(전체길이))
}
func (자신 *T전송제어프로토콜_제공자) M연결하기(ip주소 uint32, 입출구번호 uint16) *T전송제어프로토콜_소켓{
	var memoryManager = &T메모리_관리자{}
	var 소켓 = (*T전송제어프로토콜_소켓)(memoryManager.Malloc(512))
	
	if 소켓 != nil {
		소켓.M초기화(자신)
		
		소켓.원격입출구번호 = 입출구번호
		소켓.원격IP주소 = ip주소
		소켓.자신입출구번호 = 자료.여유포트번호
		자료.여유포트번호++
		소켓.자신IP주소 = uint32(자신.T인터넷규약_처리기.M제공자_갖기().M아이피주소_갖기())

		소켓.원격입출구번호 = Uint16_R(소켓.원격입출구번호)
		소켓.자신입출구번호 = Uint16_R(소켓.자신입출구번호)

		자료.소켓들[자료.소켓갯수들] = 소켓
		자료.소켓갯수들++
	
		소켓.상태 = SYN_SENT	
		소켓.순서번호 = 0xbeefcafe
		
		자신.M보내기(소켓, 0, 0, uint16(SYN))

	}
	return 소켓
}
func (자신 *T전송제어프로토콜_제공자) M연결끊기(소켓 *T전송제어프로토콜_소켓){
	소켓.상태 = FIN_WAIT1
	자신.M보내기(소켓, 0, 0, uint16(FIN+ACK))
	소켓.순서번호++
}
func (자신 *T전송제어프로토콜_제공자) M수신대기(port uint16) *T전송제어프로토콜_소켓{
	var memoryManager = &T메모리_관리자{}
	var 소켓 = (*T전송제어프로토콜_소켓)(memoryManager.Malloc(50))

	if 소켓 != nil {

		소켓.M초기화(자신)
	
		소켓.상태 = LISTEN
		소켓.자신IP주소 = uint32(자신.T인터넷규약_처리기.M제공자_갖기().M아이피주소_갖기())
		소켓.자신입출구번호 = Uint16_R(port)
		자료.소켓들[자료.소켓갯수들]  = 소켓
		자료.소켓갯수들++
	}
	return 소켓
}
func (자신 *T전송제어프로토콜_제공자) M바인드(소켓 *T전송제어프로토콜_소켓, 처리기 I서버_전송제어프로토콜_처리기){
	if 처리기 != nil{
		자료.서버_전송제어프로토콜_처리기 = 처리기
	}else {
		자료.서버_전송제어프로토콜_처리기 = &T서버_전송제어프로토콜_처리기{}
	}

}
