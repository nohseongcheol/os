/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package arp

import . "unsafe"
import . "콘솔"
import . "util"
import . "net/etherframe"

var 콘솔 T콘솔 = T콘솔{}
/////////////////////////////////////////////////////////////////////////////
//
//		주소결정규약 = Address Resolution Protocol = ARP
//
/////////////////////////////////////////////////////////////////////////////
type T주소결정규약_메시지_임시저장공간 struct{
	하드웨어타입 [2]byte 	// hardware type
	프로토콜타입 [2]byte	// protcotol type
	하드웨어주소_길이 byte 	// hardware address length = 6(mac address length)
	프로토콜_길이 byte 	// protocol address length = internet protocol address = 4 (ip address length)
	커맨드 [2]byte		// command

	출발지_맥주소 [6]byte	// src mac address
	출발지_아이피 [4] byte 	// src ip address
	목적지_맥주소 [6]byte	// dst mac address
	목적지_아이피 [4]byte	// dst ip address
}
var 주소결정규약_메시지_크기 uint32 =(64+92+64)/8+2

type T주소결정규약_메시지 struct{
	하드웨어타입 uint16	// hardware type
	프로토콜타입 uint16	// protocol type
	하드웨어주소_길이 uint8	// hardware address length = 6(mac address length)
	프로토콜_길이 uint8	// protocol address length = 4(ip address length)
	커맨드 uint16		// command

	출발지_맥주소 uint64	// src mac address
	출발지_아이피 uint32	// src ip address
	목적지_맥주소 uint64	// dst mac address
	목적지_아이피 uint32	// dst ip address
}
func (자신 *T주소결정규약_메시지) M초기화(임시저장공간 *T주소결정규약_메시지_임시저장공간) {

	자신.하드웨어타입 = Uint16_R(ArrayToUint16(임시저장공간.하드웨어타입))
	자신.프로토콜타입 = Uint16_R(ArrayToUint16(임시저장공간.프로토콜타입))
	자신.하드웨어주소_길이 = byte(임시저장공간.하드웨어주소_길이)
	자신.프로토콜_길이 = byte(임시저장공간.프로토콜_길이)
	자신.커맨드 = Uint16_R(ArrayToUint16(임시저장공간.커맨드))

        자신.출발지_맥주소 = Uint48_R(ArrayToUint48(임시저장공간.출발지_맥주소))
        자신.출발지_아이피 = Uint32_R(ArrayToUint32(임시저장공간.출발지_아이피))
        자신.목적지_맥주소 = Uint48_R(ArrayToUint48(임시저장공간.목적지_맥주소))
        자신.목적지_아이피 = Uint32_R(ArrayToUint32(임시저장공간.목적지_아이피))
}
func (자신 *T주소결정규약_메시지) 버퍼설정(임시저장공간 *T주소결정규약_메시지_임시저장공간) {
	임시저장공간.하드웨어타입 = Uint16ToArray(자신.하드웨어타입)
	임시저장공간.프로토콜타입 = Uint16ToArray(자신.프로토콜타입)
	임시저장공간.하드웨어주소_길이 = uint8(자신.하드웨어주소_길이)
	임시저장공간.프로토콜_길이= uint8(자신.프로토콜_길이)

	임시저장공간.커맨드 = Uint16ToArray(자신.커맨드)
        임시저장공간.출발지_맥주소 = Uint48ToArray(자신.출발지_맥주소)
        임시저장공간.출발지_아이피 = Uint32ToArray(자신.출발지_아이피)
        임시저장공간.목적지_맥주소 = Uint48ToArray(자신.목적지_맥주소)
        임시저장공간.목적지_아이피 = Uint32ToArray(자신.목적지_아이피)
}
/////////////////////////////////////////////////////////////////////////////
type T주소결정규약_제공자_자료 struct{
	아이피주소_캐시 [128] uint32
	맥주소_캐시 [128] uint64
	캐시항목_갯수 int
}
var 자료 T주소결정규약_제공자_자료

type T주소결정규약_제공자 struct {
	T이더넷프레임_처리기
}

func (자신 *T주소결정규약_제공자) M초기화(후단부 T이더넷프레임_제공자){
	자신.T이더넷프레임_처리기.M초기화(후단부)
	자신.T이더넷프레임_처리기.M처리기설정(자신, 0x0806)
	자료.캐시항목_갯수 = 0
}
func (자신 *T주소결정규약_제공자) M이더넷프레임_받는동시(자료주소 uintptr, 크기 uint32) bool{

	if 크기 < 주소결정규약_메시지_크기 {
		return false
	}

	var 메시지_임시저장공간 *T주소결정규약_메시지_임시저장공간 = (*T주소결정규약_메시지_임시저장공간)(Pointer(자료주소))
	var 주소결정규약 T주소결정규약_메시지 = T주소결정규약_메시지{}
	주소결정규약.M초기화(메시지_임시저장공간)

	if 주소결정규약.하드웨어타입 == 0x0100 {
		if 주소결정규약.프로토콜타입 == 0x0008 && 
		   주소결정규약.하드웨어주소_길이 == 6 && 
		   주소결정규약.프로토콜_길이 == 4 && 
		   uint64(주소결정규약.목적지_아이피) == 자신.M아이피주소_갖기() {

			switch 주소결정규약.커맨드 {
				case 0x0100: // requested 
					if 자신.M캐시에서_맥주소_갖기(주소결정규약.출발지_아이피) == 0xFFFFFFFFFFFF {
						if 자료.캐시항목_갯수 < 128 {
							자료.아이피주소_캐시[자료.캐시항목_갯수] = 주소결정규약.출발지_아이피
							자료.맥주소_캐시[자료.캐시항목_갯수] = 주소결정규약.출발지_맥주소
							자료.캐시항목_갯수++
						}
					}
					주소결정규약.커맨드 = 0x0200
					주소결정규약.목적지_아이피 = 주소결정규약.출발지_아이피
					주소결정규약.목적지_맥주소 = 주소결정규약.출발지_맥주소
					주소결정규약.출발지_아이피 = uint32(자신.M아이피주소_갖기())
					주소결정규약.출발지_맥주소 = 자신.M맥주소_갖기()
					주소결정규약.버퍼설정(메시지_임시저장공간)

					return true
					break

				case 0x0200: // 
					if 자료.캐시항목_갯수 < 128 {
						자료.아이피주소_캐시[자료.캐시항목_갯수] = 주소결정규약.출발지_아이피
						자료.맥주소_캐시[자료.캐시항목_갯수] = 주소결정규약.출발지_맥주소
						자료.캐시항목_갯수++
					}
					break
			}
		
		}
	}
	return false
	
}

func (자신 *T주소결정규약_제공자) M맥주소_방송(IP_BE uint32){

	var 주소결정규약 T주소결정규약_메시지 = T주소결정규약_메시지{}
	주소결정규약.하드웨어타입 = 0x0100
	주소결정규약.프로토콜타입 = 0x0008
	주소결정규약.하드웨어주소_길이 = 6
	주소결정규약.프로토콜_길이 = 4
	주소결정규약.커맨드 = 0x0200


	주소결정규약.출발지_아이피 = uint32(자신.M아이피주소_갖기())
	
	주소결정규약.목적지_맥주소 =  자신.Resolve(IP_BE) // infinite loop
	주소결정규약.목적지_아이피 = IP_BE
	콘솔.M출력XY([]byte("broad mac"), 0, 15)

	주소결정규약.출발지_맥주소 = 자신.M맥주소_갖기()

	var 주소결정규약_버퍼 T주소결정규약_메시지_임시저장공간 = T주소결정규약_메시지_임시저장공간{}
	주소결정규약.버퍼설정(&주소결정규약_버퍼)

	var 주소 uintptr = uintptr(Pointer(&주소결정규약_버퍼))
	자신.M이더넷프레임_보내기(주소결정규약.목적지_맥주소, Uint16_R(0x0806), 주소, 주소결정규약_메시지_크기)
}
func (자신 *T주소결정규약_제공자) M맥주소_요청하기(IP_BE uint32){

	var 주소결정규약 T주소결정규약_메시지 = T주소결정규약_메시지{}
	주소결정규약.하드웨어타입 = 0x0100
	주소결정규약.프로토콜타입 = 0x0008
	주소결정규약.하드웨어주소_길이 = 6
	주소결정규약.프로토콜_길이 = 4
	주소결정규약.커맨드 = 0x0100

	주소결정규약.출발지_맥주소 = 자신.M맥주소_갖기()
	주소결정규약.출발지_아이피 = uint32(자신.M아이피주소_갖기())


	주소결정규약.목적지_맥주소 = 0xFFFFFFFFFFFF // broadcast
	주소결정규약.목적지_아이피 = IP_BE

	var 메시지_임시저장공간 T주소결정규약_메시지_임시저장공간 = T주소결정규약_메시지_임시저장공간{}
	주소결정규약.버퍼설정(&메시지_임시저장공간)
	
	var 주소 uintptr = uintptr(Pointer(&메시지_임시저장공간))
	자신.M이더넷프레임_보내기(주소결정규약.목적지_맥주소, Uint16_R(0x0806), 주소, 주소결정규약_메시지_크기)
}

func (자신 *T주소결정규약_제공자) M캐시에서_맥주소_갖기(IP_BE uint32) uint64{
	for i:=0; i<자료.캐시항목_갯수; i++ {
		for ipIdx:=0; ipIdx<4; ipIdx++ {
			//printfHex(
		}
		//print \n
		
		for macIdx:=0; macIdx<6; macIdx++ {
			//printfHex
		}

		if 자료.아이피주소_캐시[i] == IP_BE {
			콘솔.M출력([]byte("getmacfromcache"))
			return 자료.맥주소_캐시[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (자신 *T주소결정규약_제공자) Resolve(IP_BE uint32) uint64{
	var 결과 uint64 = 자신.M캐시에서_맥주소_갖기(IP_BE)
	if 결과 == 0xFFFFFFFFFFFF {
		자신.M맥주소_요청하기(IP_BE)
	}
	for i:=0; i<=128 && 결과 == 0xFFFFFFFFFFFF; i++ {
		결과 = 자신.M캐시에서_맥주소_갖기(IP_BE)
	}
	
	return 결과
}
