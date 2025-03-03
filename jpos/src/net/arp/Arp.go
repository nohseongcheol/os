/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 주소결정규약

import . "unsafe"
import . "console"
import . "net/etherframe"
import . "util"

var 端末機 T端末機 = T端末機{}
/////////////////////////////////////////////////////////////////////////////
//
//		アドレス解決プロトコル = Address Resolution Protocol = ARP
//
/////////////////////////////////////////////////////////////////////////////
type Tアドレス解決プロトコル_メッセージ_緩衝器 struct{
	ハードウェア流刑 [2]byte 	// hardware type
	プロトコル流刑 [2]byte		// protcotol type
	ハードウェア住所_長さ byte 	// hardware address length = 6(mac address length)
	プロトコル住所_長さ byte 	// protocol address length = internet protocol address = 4 (ip address length)
	修行作業 [2]byte		// operation

	送信元ハードウェア住所 [6]byte	// source mac address
	送信元_アイピー_住所 [4] byte	// source IP address
	宛先ハードウェア住所 [6]byte	// destination mac address
	宛先_アイピー_住所 [4]byte	// destination ip address
}
var アドレス解決プロトコル_メッセージ_大きさ uint32 =(64+92+64)/8+2

type Tアドレス解決プロトコル_メッセージ struct{
	ハードウェア流刑 uint16		// hardware type
	プロトコル流刑 uint16		// protocol type
	ハードウェア住所_長さ uint8	// hardware address length = 6(mac address length)
	プロトコル住所_長さ uint8	// protocol address length = 4(ip address length)
	修行作業 uint16			// operation

	送信元ハードウェア住所 uint64	// source mac address
	送信元_アイピー_住所 uint32	// source ip address
	宛先ハードウェア住所 uint64	// destination mac address
	宛先_アイピー_住所 uint32	// destination ip address
}
func (自身 *Tアドレス解決プロトコル_メッセージ) Init(緩衝器 *Tアドレス解決プロトコル_メッセージ_緩衝器) {

	自身.ハードウェア流刑 = Uint16_R(ArrayToUint16(緩衝器.ハードウェア流刑))
	自身.プロトコル流刑 = Uint16_R(ArrayToUint16(緩衝器.プロトコル流刑))
	自身.ハードウェア住所_長さ = byte(緩衝器.ハードウェア住所_長さ)
	自身.プロトコル住所_長さ = byte(緩衝器.プロトコル住所_長さ)
	自身.修行作業 = Uint16_R(ArrayToUint16(緩衝器.修行作業))

        自身.送信元ハードウェア住所 = Uint48_R(ArrayToUint48(緩衝器.送信元ハードウェア住所))
        自身.送信元_アイピー_住所 = Uint32_R(ArrayToUint32(緩衝器.送信元_アイピー_住所))
        自身.宛先ハードウェア住所 = Uint48_R(ArrayToUint48(緩衝器.宛先ハードウェア住所))
        自身.宛先_アイピー_住所 = Uint32_R(ArrayToUint32(緩衝器.宛先_アイピー_住所))
}
func (自身 *Tアドレス解決プロトコル_メッセージ) 緩衝器_設定(緩衝器 *Tアドレス解決プロトコル_メッセージ_緩衝器) {
	緩衝器.ハードウェア流刑 = Uint16ToArray(自身.ハードウェア流刑)
	緩衝器.プロトコル流刑 = Uint16ToArray(自身.プロトコル流刑)
	緩衝器.ハードウェア住所_長さ = uint8(自身.ハードウェア住所_長さ)
	緩衝器.プロトコル住所_長さ= uint8(自身.プロトコル住所_長さ)

	緩衝器.修行作業 = Uint16ToArray(自身.修行作業)
        緩衝器.送信元ハードウェア住所 = Uint48ToArray(自身.送信元ハードウェア住所)
        緩衝器.送信元_アイピー_住所 = Uint32ToArray(自身.送信元_アイピー_住所)
        緩衝器.宛先ハードウェア住所 = Uint48ToArray(自身.宛先ハードウェア住所)
        緩衝器.宛先_アイピー_住所 = Uint32ToArray(自身.宛先_アイピー_住所)
}
/////////////////////////////////////////////////////////////////////////////
type Tアドレス解決プロトコル_提供者_資料 struct{
	IPキャッシュ [128] uint32	// IP Cache
	MACキャッシュ [128] uint64  	// MAC Cache
	キャッシュエントリ数 int	// num CacheEntries
}
var 資料 Tアドレス解決プロトコル_提供者_資料

type Tアドレス解決プロトコル_提供者 struct {
	Tイーサネットフレーム_處理器
}
func (自身 *Tアドレス解決プロトコル_提供者) M初期化(後端部 Tイーサネットフレーム_提供者) {
	自身.Tイーサネットフレーム_處理器.M初期化(後端部)
	自身.Tイーサネットフレーム_處理器.M處理器を設定(自身, 0x0806)
	資料.キャッシュエントリ数 = 0

}
func (自身 *Tアドレス解決プロトコル_提供者) Mイーサネットフレーム_受信と同時(資料住所 uintptr, 大きさ uint32) bool{

	if 大きさ < アドレス解決プロトコル_メッセージ_大きさ {
		return false
	}
	var アドレス解決プロトコル_緩衝器 *Tアドレス解決プロトコル_メッセージ_緩衝器 = (*Tアドレス解決プロトコル_メッセージ_緩衝器)(Pointer(資料住所))
	var アドレス解決プロトコル Tアドレス解決プロトコル_メッセージ = Tアドレス解決プロトコル_メッセージ{}
	アドレス解決プロトコル.Init(アドレス解決プロトコル_緩衝器)

	if アドレス解決プロトコル.ハードウェア流刑 == 0x0100 {
		if アドレス解決プロトコル.プロトコル流刑 == 0x0008 && 
			アドレス解決プロトコル.ハードウェア住所_長さ == 6 && 
			アドレス解決プロトコル.プロトコル住所_長さ == 4 && 
			uint64(アドレス解決プロトコル.宛先_アイピー_住所) == 自身.Mアイピー住所を取得する() {

			switch アドレス解決プロトコル.修行作業 {
				case 0x0100: // requested 
					if 自身.GetMACFromCache(アドレス解決プロトコル.送信元_アイピー_住所) == 0xFFFFFFFFFFFF {
						if 資料.キャッシュエントリ数 < 128 {
							資料.IPキャッシュ[資料.キャッシュエントリ数] = アドレス解決プロトコル.送信元_アイピー_住所
							資料.MACキャッシュ[資料.キャッシュエントリ数] = アドレス解決プロトコル.送信元ハードウェア住所
							資料.キャッシュエントリ数++
						}
					}
					アドレス解決プロトコル.修行作業 = 0x0200
					アドレス解決プロトコル.宛先_アイピー_住所 = アドレス解決プロトコル.送信元_アイピー_住所
					アドレス解決プロトコル.宛先ハードウェア住所 = アドレス解決プロトコル.送信元ハードウェア住所
					アドレス解決プロトコル.送信元_アイピー_住所 = uint32(自身.Mアイピー住所を取得する())
					アドレス解決プロトコル.送信元ハードウェア住所 = 自身.M媒体住所を取得する()
					アドレス解決プロトコル.緩衝器_設定(アドレス解決プロトコル_緩衝器)

					return true
					break

				case 0x0200: // 
					if 資料.キャッシュエントリ数 < 128 {
						資料.IPキャッシュ[資料.キャッシュエントリ数] = アドレス解決プロトコル.送信元_アイピー_住所
						資料.MACキャッシュ[資料.キャッシュエントリ数] = アドレス解決プロトコル.送信元ハードウェア住所
						資料.キャッシュエントリ数++
					}
					break
			}
		
		}
	}
	return false
	
}

func (自身 *Tアドレス解決プロトコル_提供者) M物理住所の放送(IP_BE uint32){

	var アドレス解決プロトコル Tアドレス解決プロトコル_メッセージ = Tアドレス解決プロトコル_メッセージ{}
	アドレス解決プロトコル.ハードウェア流刑 = 0x0100
	アドレス解決プロトコル.プロトコル流刑 = 0x0008
	アドレス解決プロトコル.ハードウェア住所_長さ = 6
	アドレス解決プロトコル.プロトコル住所_長さ = 4
	アドレス解決プロトコル.修行作業 = 0x0200


	アドレス解決プロトコル.送信元_アイピー_住所 = uint32(自身.Mアイピー住所を取得する())
	
	アドレス解決プロトコル.宛先ハードウェア住所 = 自身.Resolve(IP_BE) // infinite loop
	アドレス解決プロトコル.宛先_アイピー_住所 = IP_BE
	端末機.M出力("broad mac", 0, 15)

	アドレス解決プロトコル.送信元ハードウェア住所 = 自身.M媒体住所を取得する()

	var アドレス解決プロトコル_緩衝器 Tアドレス解決プロトコル_メッセージ_緩衝器 = Tアドレス解決プロトコル_メッセージ_緩衝器{}
	アドレス解決プロトコル.緩衝器_設定(&アドレス解決プロトコル_緩衝器)

	var 住所 uintptr = uintptr(Pointer(&アドレス解決プロトコル_緩衝器))
	自身.Mフレーム送信(アドレス解決プロトコル.宛先ハードウェア住所, Uint16_R(0x0806), 住所, アドレス解決プロトコル_メッセージ_大きさ)
}
func (自身 *Tアドレス解決プロトコル_提供者) RequestMacAddress(IP_BE uint32){

	var アドレス解決プロトコル Tアドレス解決プロトコル_メッセージ = Tアドレス解決プロトコル_メッセージ{}
	アドレス解決プロトコル.ハードウェア流刑 = 0x0100
	アドレス解決プロトコル.プロトコル流刑 = 0x0008
	アドレス解決プロトコル.ハードウェア住所_長さ = 6
	アドレス解決プロトコル.プロトコル住所_長さ = 4
	アドレス解決プロトコル.修行作業 = 0x0100

	アドレス解決プロトコル.送信元ハードウェア住所 = 自身.M媒体住所を取得する()
	アドレス解決プロトコル.送信元_アイピー_住所 = uint32(自身.Mアイピー住所を取得する())


	アドレス解決プロトコル.宛先ハードウェア住所 = 0xFFFFFFFFFFFF // broadcast
	アドレス解決プロトコル.宛先_アイピー_住所 = IP_BE

	var アドレス解決プロトコル_緩衝器 Tアドレス解決プロトコル_メッセージ_緩衝器 = Tアドレス解決プロトコル_メッセージ_緩衝器{}
	アドレス解決プロトコル.緩衝器_設定(&アドレス解決プロトコル_緩衝器)
	
	var 住所 uintptr = uintptr(Pointer(&アドレス解決プロトコル_緩衝器))
	自身.Mフレーム送信(アドレス解決プロトコル.宛先ハードウェア住所, Uint16_R(0x0806), 住所, アドレス解決プロトコル_メッセージ_大きさ)
}

func (自身 *Tアドレス解決プロトコル_提供者) GetMACFromCache(IP_BE uint32) uint64{
	for i:=0; i<資料.キャッシュエントリ数; i++ {
		for ipIdx:=0; ipIdx<4; ipIdx++ {
			//printfHex(
		}
		//print \n
		
		for macIdx:=0; macIdx<6; macIdx++ {
			//printfHex
		}

		if 資料.IPキャッシュ[i] == IP_BE {
			//端末機.M出力("getmacfromcache")
			return 資料.MACキャッシュ[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (自身 *Tアドレス解決プロトコル_提供者) Resolve(IP_BE uint32) uint64{
	var けっか uint64 = 自身.GetMACFromCache(IP_BE)
	if けっか == 0xFFFFFFFFFFFF {
		自身.RequestMacAddress(IP_BE)
	}
	for i:=0; i<=128 && けっか == 0xFFFFFFFFFFFF; i++ {
		けっか = 自身.GetMACFromCache(IP_BE)
	}
	
	return けっか
}
