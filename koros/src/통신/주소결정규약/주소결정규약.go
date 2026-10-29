/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 주소결정규약

import . "unsafe"
import . "단말기"
import . "통신/신호통신망형태"
import . "util"

var 단말기 T단말기 = T단말기{}
/////////////////////////////////////////////////////////////////////////////
//
//		주소결정규약 = Address Resolution Protocol = ARP
//
/////////////////////////////////////////////////////////////////////////////
type T주소결정규약_메시지_임시저장공간 struct{
	하드웨어유형 [2]byte 	// hardware type
	규약유형 [2]byte	// protcotol type
	하드웨어주소_길이 byte 	// hardware address length = 6(mac address length)
	규약주소_길이 byte 	// protocol address length = internet protocol address = 4 (ip address length)
	수행작업 [2]byte	// operation

	출발지_매체주소 [6]byte			// source mac address
	출발지_상호통신망규약_주소 [4] byte	// source IP address
	목적지_매체주소 [6]byte			// destination mac address
	목적지_상호통신망규약_주소 [4]byte	// destination ip address
}
var 주소결정규약_메시지_크기 uint32 =(64+92+64)/8+2

type T주소결정규약_메시지 struct{
	하드웨어유형 uint16	// hardware type
	규약유형 uint16		// protocol type
	하드웨어주소_길이 uint8	// hardware address length = 6(mac address length)
	규약주소_길이 uint8	// protocol address length = 4(ip address length)
	수행작업 uint16		// operation

	출발지_매체주소 uint64			// source mac address
	출발지_상호통신망규약_주소 uint32	// source ip address
	목적지_매체주소 uint64			// destination mac address
	목적지_상호통신망규약_주소 uint32	// destination ip address
}
func (자신 *T주소결정규약_메시지) Init(임시저장공간 *T주소결정규약_메시지_임시저장공간) {

	자신.하드웨어유형 = Uint16_R(ArrayToUint16(임시저장공간.하드웨어유형))
	자신.규약유형 = Uint16_R(ArrayToUint16(임시저장공간.규약유형))
	자신.하드웨어주소_길이 = byte(임시저장공간.하드웨어주소_길이)
	자신.규약주소_길이 = byte(임시저장공간.규약주소_길이)
	자신.수행작업 = Uint16_R(ArrayToUint16(임시저장공간.수행작업))

        자신.출발지_매체주소 = Uint48_R(ArrayToUint48(임시저장공간.출발지_매체주소))
        자신.출발지_상호통신망규약_주소 = Uint32_R(ArrayToUint32(임시저장공간.출발지_상호통신망규약_주소))
        자신.목적지_매체주소 = Uint48_R(ArrayToUint48(임시저장공간.목적지_매체주소))
        자신.목적지_상호통신망규약_주소 = Uint32_R(ArrayToUint32(임시저장공간.목적지_상호통신망규약_주소))
}
func (자신 *T주소결정규약_메시지) 임시저장공간_설정(임시저장공간 *T주소결정규약_메시지_임시저장공간) {
	임시저장공간.하드웨어유형 = Uint16ToArray(자신.하드웨어유형)
	임시저장공간.규약유형 = Uint16ToArray(자신.규약유형)
	임시저장공간.하드웨어주소_길이 = uint8(자신.하드웨어주소_길이)
	임시저장공간.규약주소_길이= uint8(자신.규약주소_길이)

	임시저장공간.수행작업 = Uint16ToArray(자신.수행작업)
        임시저장공간.출발지_매체주소 = Uint48ToArray(자신.출발지_매체주소)
        임시저장공간.출발지_상호통신망규약_주소 = Uint32ToArray(자신.출발지_상호통신망규약_주소)
        임시저장공간.목적지_매체주소 = Uint48ToArray(자신.목적지_매체주소)
        임시저장공간.목적지_상호통신망규약_주소 = Uint32ToArray(자신.목적지_상호통신망규약_주소)
}
/////////////////////////////////////////////////////////////////////////////
type T주소결정규약_제공자_자료 struct{
	상호통신규약_일시저장공간 [128] uint32	// IP Cache
	매체접근주소_일시저장공간 [128] uint64  // MAC Cache
	일시저장공간목록_갯수 int		// num CacheEntries
}
var 자료 T주소결정규약_제공자_자료

type T주소결정규약_제공자 struct {
	T신호통신망형태_처리기
}
func (자신 *T주소결정규약_제공자) M초기화(후단부 T신호통신망형태_제공자) {
	자신.T신호통신망형태_처리기.M초기화(후단부)
	자신.T신호통신망형태_처리기.M처리기설정(자신, 0x0806)
	자료.일시저장공간목록_갯수 = 0

}
func (자신 *T주소결정규약_제공자) M신호통신망형태_받는동시(자료주소 uintptr, 크기 uint32) bool{

	if 크기 < 주소결정규약_메시지_크기 {
		return false
	}
	var 주소결정규약_임시저장공간 *T주소결정규약_메시지_임시저장공간 = (*T주소결정규약_메시지_임시저장공간)(Pointer(자료주소))
	var 주소결정규약 T주소결정규약_메시지 = T주소결정규약_메시지{}
	주소결정규약.Init(주소결정규약_임시저장공간)

	if 주소결정규약.하드웨어유형 == 0x0100 {
		if 주소결정규약.규약유형 == 0x0008 && 
			주소결정규약.하드웨어주소_길이 == 6 && 
			주소결정규약.규약주소_길이 == 4 && 
			uint64(주소결정규약.목적지_상호통신망규약_주소) == 자신.M상호통신망주소_갖기() {

			switch 주소결정규약.수행작업 {
				case 0x0100: // requested 
					if 자신.GetMACFromCache(주소결정규약.출발지_상호통신망규약_주소) == 0xFFFFFFFFFFFF {
						if 자료.일시저장공간목록_갯수 < 128 {
							자료.상호통신규약_일시저장공간[자료.일시저장공간목록_갯수] = 주소결정규약.출발지_상호통신망규약_주소
							자료.매체접근주소_일시저장공간[자료.일시저장공간목록_갯수] = 주소결정규약.출발지_매체주소
							자료.일시저장공간목록_갯수++
						}
					}
					주소결정규약.수행작업 = 0x0200
					주소결정규약.목적지_상호통신망규약_주소 = 주소결정규약.출발지_상호통신망규약_주소
					주소결정규약.목적지_매체주소 = 주소결정규약.출발지_매체주소
					주소결정규약.출발지_상호통신망규약_주소 = uint32(자신.M상호통신망주소_갖기())
					주소결정규약.출발지_매체주소 = 자신.M매체주소_갖기()
					주소결정규약.임시저장공간_설정(주소결정규약_임시저장공간)

					return true
					break

				case 0x0200: // 
					if 자료.일시저장공간목록_갯수 < 128 {
						자료.상호통신규약_일시저장공간[자료.일시저장공간목록_갯수] = 주소결정규약.출발지_상호통신망규약_주소
						자료.매체접근주소_일시저장공간[자료.일시저장공간목록_갯수] = 주소결정규약.출발지_매체주소
						자료.일시저장공간목록_갯수++
					}
					break
			}
		
		}
	}
	return false
	
}

func (자신 *T주소결정규약_제공자) M물리주소_방송(IP_BE uint32){

	var 주소결정규약 T주소결정규약_메시지 = T주소결정규약_메시지{}
	주소결정규약.하드웨어유형 = 0x0100
	주소결정규약.규약유형 = 0x0008
	주소결정규약.하드웨어주소_길이 = 6
	주소결정규약.규약주소_길이 = 4
	주소결정규약.수행작업 = 0x0200


	주소결정규약.출발지_상호통신망규약_주소 = uint32(자신.M상호통신망주소_갖기())
	
	주소결정규약.목적지_매체주소 = 자신.Resolve(IP_BE) // infinite loop
	주소결정규약.목적지_상호통신망규약_주소 = IP_BE
	단말기.M출력("broad mac", 0, 15)

	주소결정규약.출발지_매체주소 = 자신.M매체주소_갖기()

	var 주소결정규약_임시저장공간 T주소결정규약_메시지_임시저장공간 = T주소결정규약_메시지_임시저장공간{}
	주소결정규약.임시저장공간_설정(&주소결정규약_임시저장공간)

	var 주소 uintptr = uintptr(Pointer(&주소결정규약_임시저장공간))
	자신.M신호보내기(주소결정규약.목적지_매체주소, Uint16_R(0x0806), 주소, 주소결정규약_메시지_크기)
}
func (자신 *T주소결정규약_제공자) RequestMacAddress(IP_BE uint32){

	var 주소결정규약 T주소결정규약_메시지 = T주소결정규약_메시지{}
	주소결정규약.하드웨어유형 = 0x0100
	주소결정규약.규약유형 = 0x0008
	주소결정규약.하드웨어주소_길이 = 6
	주소결정규약.규약주소_길이 = 4
	주소결정규약.수행작업 = 0x0100

	주소결정규약.출발지_매체주소 = 자신.M매체주소_갖기()
	주소결정규약.출발지_상호통신망규약_주소 = uint32(자신.M상호통신망주소_갖기())


	주소결정규약.목적지_매체주소 = 0xFFFFFFFFFFFF // broadcast
	주소결정규약.목적지_상호통신망규약_주소 = IP_BE

	var 주소결정규약_임시저장공간 T주소결정규약_메시지_임시저장공간 = T주소결정규약_메시지_임시저장공간{}
	주소결정규약.임시저장공간_설정(&주소결정규약_임시저장공간)
	
	var 주소 uintptr = uintptr(Pointer(&주소결정규약_임시저장공간))
	자신.M신호보내기(주소결정규약.목적지_매체주소, Uint16_R(0x0806), 주소, 주소결정규약_메시지_크기)
}

func (자신 *T주소결정규약_제공자) GetMACFromCache(IP_BE uint32) uint64{
	for i:=0; i<자료.일시저장공간목록_갯수; i++ {
		for ipIdx:=0; ipIdx<4; ipIdx++ {
			//printfHex(
		}
		//print \n
		
		for macIdx:=0; macIdx<6; macIdx++ {
			//printfHex
		}

		if 자료.상호통신규약_일시저장공간[i] == IP_BE {
			//단말기.M출력("getmacfromcache")
			return 자료.매체접근주소_일시저장공간[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (자신 *T주소결정규약_제공자) Resolve(IP_BE uint32) uint64{
	var 결과 uint64 = 자신.GetMACFromCache(IP_BE)
	if 결과 == 0xFFFFFFFFFFFF {
		자신.RequestMacAddress(IP_BE)
	}
	for i:=0; i<=128 && 결과 == 0xFFFFFFFFFFFF; i++ {
		결과 = 자신.GetMACFromCache(IP_BE)
	}
	
	return 결과
}
