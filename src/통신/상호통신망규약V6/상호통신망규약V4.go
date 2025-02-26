/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 상호통신망규약V6

import . "unsafe"
import . "util"
import . "단말기"
import . "통신/신호통신망형태"
import . "통신/주소결정규약"

var 단말기 T단말기 = T단말기{}
////////////////////////////////////////////////////////////////////
//
//	상호통신망규약 = 인터넷규약= InternetProtocol = IP
//
////////////////////////////////////////////////////////////////////
type T상호통신망규약V4메시지_임시저장공간 struct{
	길이_버전 byte			// ip 개정=4, header length
	서비스유형 byte			// type of service
	전체길이 [2]byte		// Total Length
	
	식별자 [2] byte 		// identification
	표시와변위차[2] byte		// flagsAndOffset
	
	수명 byte 			// time to Live
	규약 byte			// protocol
	검사합 [2] byte			// checksum
	
	출발지IP주소 [4] byte			// source ip address
	목적지IP주소 [4] byte			// destination ip address
}
var 상호통신망규약_머리말_크기 uint8 = (4+4+4+8)
type T상호통신망규약V4메시지 struct{
	머리말_길이 uint8		// header length
	개정 uint8			// version
	서비스유형 uint8		// type of service
	전체길이 uint16			// total length

	식별자 uint16			// identification
	표시와변위차 uint16		/// flag and offset
	
	수명 uint8			// time ot live
	규약 uint8			// protocol
	검사합 uint16			// checksum

	출발지IP주소 uint32
	목적지IP주소 uint32
}
func (자신 *T상호통신망규약V4메시지) M초기화(임시저장공간 *T상호통신망규약V4메시지_임시저장공간){
	자신.개정 = ((임시저장공간.길이_버전 & 0xF0) >> 4)
	자신.머리말_길이 = 임시저장공간.길이_버전 & 0x0F
	자신.서비스유형 = 임시저장공간.서비스유형
	자신.전체길이 = Uint16_R(ArrayToUint16(임시저장공간.전체길이))

	자신.식별자 = Uint16_R(ArrayToUint16(임시저장공간.식별자))
	자신.표시와변위차 = Uint16_R(ArrayToUint16(임시저장공간.표시와변위차))
	
	자신.수명 = 임시저장공간.수명
	자신.규약 = 임시저장공간.규약
	자신.검사합 = Uint16_R(ArrayToUint16(임시저장공간.검사합))

	자신.출발지IP주소 = Uint32_R(ArrayToUint32(임시저장공간.출발지IP주소))
	자신.목적지IP주소 = Uint32_R(ArrayToUint32(임시저장공간.목적지IP주소))

}
func (자신 *T상호통신망규약V4메시지) M임시저장공간_설정(임시저장공간 *T상호통신망규약V4메시지_임시저장공간){
	임시저장공간.길이_버전 = byte(((자신.개정 & 0x0F) << 4) | (자신.머리말_길이 & 0x0F))
	임시저장공간.서비스유형 = 자신.서비스유형
	임시저장공간.전체길이 = Uint16ToArray(자신.전체길이)

	임시저장공간.식별자 = Uint16ToArray(자신.식별자)
	임시저장공간.표시와변위차 = Uint16ToArray(자신.표시와변위차)

	임시저장공간.수명 = 자신.수명
	임시저장공간.규약 = 자신.규약
	임시저장공간.검사합 = Uint16ToArray(자신.검사합)

	임시저장공간.출발지IP주소 = Uint32ToArray(자신.출발지IP주소)
	임시저장공간.목적지IP주소 = Uint32ToArray(자신.목적지IP주소)
	
}
/////////////////////////////////////////////////////////////////////////////////////////////////////
type I상호통신망규약_처리기 interface{
	M상호통신망규약_받은동시(출발지IP주소_BE uint32, 목적지IP주소_BE uint32, 자료주소 uintptr, 크기 uint32) bool
	M패킷보내기(목적지IP주소_BE uint32, p_규약 uint8, 자료주소 uintptr, 크기 uint32) // Packet 보내기
	M제공자_갖기() *T상호통신망규약_제공자
}

/////////////////////////////////////////////////////////////////////////////////////////////////////
type T상호통신망규약_처리기_자료 struct{
	후단부 T상호통신망규약_제공자
	규약 uint8
}
var 처리기_자료 T상호통신망규약_처리기_자료

type T상호통신망규약_처리기 struct{
}
func (자신 *T상호통신망규약_처리기) M초기화(후단부 T상호통신망규약_제공자, 상호통신망규약_처리기 I상호통신망규약_처리기, 규약 uint8){
	처리기_자료.규약 = 규약
	처리기_자료.후단부 = 후단부
	자료.상호통신망규약_처리기들[규약] = 상호통신망규약_처리기
}
func (자신 *T상호통신망규약_처리기) M상호통신망규약_받은동시(출발지IP주소_BE uint32, 목적지IP주소_BE uint32, 자료주소 uintptr, 크기 uint32) bool{
	return false
}
func (자신 *T상호통신망규약_처리기) M패킷보내기(목적지IP주소_BE uint32, 규약 uint8, 자료주소 uintptr, 크기 uint32){
	처리기_자료.후단부.M패킷보내기(목적지IP주소_BE, 규약, 자료주소, 크기)
}
func (자신 *T상호통신망규약_처리기) M제공자_갖기() *T상호통신망규약_제공자 {
	return &처리기_자료.후단부
}
/////////////////////////////////////////////////////////////////////////////////////////////////////
type T상호통신망규약_제공자_자료 struct{
	주소결정규약_제공자 T주소결정규약_제공자
	통신망관문_주소 uint32
	부분통신망_영역숨김 uint32
	상호통신망규약_처리기들 [255]I상호통신망규약_처리기
}
var 자료 T상호통신망규약_제공자_자료

type T상호통신망규약_제공자 struct{
	T신호통신망형태_처리기
}
func (자신 *T상호통신망규약_제공자) M초기화(후단부 T신호통신망형태_제공자) { //, 
	
	자신.T신호통신망형태_처리기.M초기화(후단부)
	자신.T신호통신망형태_처리기.M처리기설정(자신, 0x0800)

	for i:=0; i<255; i++ {
		자료.상호통신망규약_처리기들[i] = nil
	}
	
}
func (자신 *T상호통신망규약_제공자) M주소설정(주소결정규약_제공자 T주소결정규약_제공자, 통신망관문_주소 uint32, 부분통신망_영역숨김 uint32){
	자료.주소결정규약_제공자 = 주소결정규약_제공자
	자료.통신망관문_주소 = 통신망관문_주소
	자료.부분통신망_영역숨김 = 부분통신망_영역숨김
}

func (자신 *T상호통신망규약_제공자) M신호통신망형태_받는동시(etherframePayload uintptr, 크기 uint32) bool{

	if 크기 < uint32(상호통신망규약_머리말_크기) {
		return false
	}
	
	var 임시저장공간 *T상호통신망규약V4메시지_임시저장공간 = (*T상호통신망규약V4메시지_임시저장공간)(Pointer(etherframePayload))
	var 메시지 T상호통신망규약V4메시지
	메시지.M초기화(임시저장공간)

	var sendBack bool = false

	if 메시지.목적지IP주소 == uint32(자신.M상호통신망주소_갖기()) {

		var length uint32 = uint32(메시지.전체길이)
		if length > 크기 {
			length = 크기
		}
		if 자료.상호통신망규약_처리기들[메시지.규약] != nil {
			sendBack  = 자료.상호통신망규약_처리기들[메시지.규약].M상호통신망규약_받은동시(메시지.출발지IP주소, 
									메시지.목적지IP주소, 
									etherframePayload + uintptr(4*메시지.머리말_길이), 
									uint32(length-uint32(4*메시지.머리말_길이)))

		}
	}

	if(sendBack) {
		var 임시 = 메시지.목적지IP주소
		메시지.목적지IP주소 = 메시지.출발지IP주소
		메시지.출발지IP주소 = 임시

		메시지.수명 = 0x40
		메시지.검사합 = 0
		
		메시지.M임시저장공간_설정(임시저장공간)
		메시지.검사합 = 자신.M검사합((*([4096]uint16))(Pointer(etherframePayload)), uint32(4*메시지.머리말_길이))
		메시지.M임시저장공간_설정(임시저장공간)

	}

	return sendBack

}
func (자신 *T상호통신망규약_제공자) M패킷보내기(목적지IP주소_BE uint32, 규약 uint8, 자료주소 uintptr, 크기 uint32) {
	var 임시저장공간1 [4096] byte
	var 임시저장공간 *T상호통신망규약V4메시지_임시저장공간 = (*T상호통신망규약V4메시지_임시저장공간)(Pointer(&임시저장공간1))
	var 메시지 T상호통신망규약V4메시지  = T상호통신망규약V4메시지{}
	메시지.개정 = 4
	메시지.머리말_길이 = 상호통신망규약_머리말_크기/4
	메시지.서비스유형 = 0
	메시지.전체길이 = Uint16_R(uint16(크기 + uint32(상호통신망규약_머리말_크기)))

	메시지.식별자 = 0x0100
	메시지.표시와변위차 = 0x0040
	메시지.수명 = 0x40
	메시지.규약 = 규약
	
	메시지.목적지IP주소 = 목적지IP주소_BE

	메시지.출발지IP주소 = uint32(자신.M상호통신망주소_갖기())

	메시지.검사합 = 0

	메시지.M임시저장공간_설정(임시저장공간)
	메시지.검사합 = 자신.M검사합((*([4096]uint16))(Pointer(&임시저장공간1)), uint32(상호통신망규약_머리말_크기))
	메시지.M임시저장공간_설정(임시저장공간)

	var 자료_임시저장공간 [4096] byte = *(*([4096]byte))(Pointer(자료주소))
	for i:=0; i<int(크기); i++ {
		임시저장공간1[i+int(상호통신망규약_머리말_크기)] = 자료_임시저장공간[i]
	}

	var 경로 uint32 = 목적지IP주소_BE
	if (목적지IP주소_BE & 자료.부분통신망_영역숨김) != (메시지.출발지IP주소 & 자료.부분통신망_영역숨김) {
		경로 = 자료.통신망관문_주소
	}

	var 보낼자료공간_주소 = uintptr(Pointer(&임시저장공간1))

	var etherType_BE = Uint16_R(0x0800)
	자신.M신호보내기(자료.주소결정규약_제공자.Resolve(경로), etherType_BE, 보낼자료공간_주소, uint32(상호통신망규약_머리말_크기)+uint32(크기))
}
func (자신 *T상호통신망규약_제공자) M검사합(p_data *[4096]uint16, lengthInBytes uint32) uint16{
	var data [4096] uint16 = *p_data

	var 임시 uint32 = 0
	for i:=0; i<int(lengthInBytes/2); i++ {
		임시 += uint32(Uint16_R(data[i]))
	}
	var dataBytes [4096] byte = *(*([4096]byte))(Pointer(&data))
	if (lengthInBytes%2) !=0 {
		임시 += uint32(uint16(dataBytes[lengthInBytes-1]) << 8)
	}

	for (임시 & 0xFFFF0000) != 0 {
		임시 = (임시 & 0xFFFF) + (임시 >> 16)
	}

	return uint16(((^임시 & 0xFF00) >> 8) | ((^임시 & 0x00FF) << 8))
}
func (자신 *T상호통신망규약_제공자) M상호통신망주소_갖기() uint64{
        return 자신.T신호통신망형태_처리기.M상호통신망주소_갖기()
}

