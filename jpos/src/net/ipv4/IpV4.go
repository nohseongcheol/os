/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package インターネットプロトコル

import . "unsafe"
import . "util"
import . "console"
import . "net/etherframe"
import . "net/arp"

var 端末機 T端末機 = T端末機{}
////////////////////////////////////////////////////////////////////
//
//	インターネットプロトコル = InternetProtocol = IP
//
////////////////////////////////////////////////////////////////////
type TインターネットプロトコルV4メッセージ_緩衝器 struct{
	長さとバージョン byte			// ip 校閲=4, header length
	サービス流刑 byte			// type of service
	全体の長さ [2]byte		// Total Length
	
	識別子 [2] byte 		// identification
	表示と変位差[2] byte		// flagsAndOffset
	
	寿命 byte 			// time to Live
	プロトコル byte			// protocol
	検査合計 [2] byte			// checksum
	
	送信元アイピー住所 [4] byte			// source ip address
	宛先アイピー住所 [4] byte			// destination ip address
}
var インターネットプロトコル_頭文字_大きさ uint8 = (4+4+4+8)
type TインターネットプロトコルV4メッセージ struct{
	頭文字の長さ uint8		// header length
	校閲 uint8			// version
	サービス流刑 uint8		// type of service
	全体の長さ uint16			// total length

	識別子 uint16			// identification
	表示と変位差 uint16		/// flag and offset
	
	寿命 uint8			// time ot live
	プロトコル uint8			// protocol
	検査合計 uint16			// checksum

	送信元アイピー住所 uint32
	宛先アイピー住所 uint32
}
func (自身 *TインターネットプロトコルV4メッセージ) M初期化(緩衝器 *TインターネットプロトコルV4メッセージ_緩衝器){
	自身.校閲 = ((緩衝器.長さとバージョン & 0xF0) >> 4)
	自身.頭文字の長さ = 緩衝器.長さとバージョン & 0x0F
	自身.サービス流刑 = 緩衝器.サービス流刑
	自身.全体の長さ = Uint16_R(ArrayToUint16(緩衝器.全体の長さ))

	自身.識別子 = Uint16_R(ArrayToUint16(緩衝器.識別子))
	自身.表示と変位差 = Uint16_R(ArrayToUint16(緩衝器.表示と変位差))
	
	自身.寿命 = 緩衝器.寿命
	自身.プロトコル = 緩衝器.プロトコル
	自身.検査合計 = Uint16_R(ArrayToUint16(緩衝器.検査合計))

	自身.送信元アイピー住所 = Uint32_R(ArrayToUint32(緩衝器.送信元アイピー住所))
	自身.宛先アイピー住所 = Uint32_R(ArrayToUint32(緩衝器.宛先アイピー住所))

}
func (自身 *TインターネットプロトコルV4メッセージ) M緩衝器_設定(緩衝器 *TインターネットプロトコルV4メッセージ_緩衝器){
	緩衝器.長さとバージョン = byte(((自身.校閲 & 0x0F) << 4) | (自身.頭文字の長さ & 0x0F))
	緩衝器.サービス流刑 = 自身.サービス流刑
	緩衝器.全体の長さ = Uint16ToArray(自身.全体の長さ)

	緩衝器.識別子 = Uint16ToArray(自身.識別子)
	緩衝器.表示と変位差 = Uint16ToArray(自身.表示と変位差)

	緩衝器.寿命 = 自身.寿命
	緩衝器.プロトコル = 自身.プロトコル
	緩衝器.検査合計 = Uint16ToArray(自身.検査合計)

	緩衝器.送信元アイピー住所 = Uint32ToArray(自身.送信元アイピー住所)
	緩衝器.宛先アイピー住所 = Uint32ToArray(自身.宛先アイピー住所)
	
}
/////////////////////////////////////////////////////////////////////////////////////////////////////
type Iインターネットプロトコル_處理器 interface{
	Mインターネットプロトコル_受信と同時(送信元アイピー住所_BE uint32, 宛先アイピー住所_BE uint32, 資料住所 uintptr, 大きさ uint32) bool
	Mパケット送信(宛先アイピー住所_BE uint32, p_プロトコル uint8, 資料住所 uintptr, 大きさ uint32) // send Packet 
	M提供者を得る() *Tインターネットプロトコル_提供者
}

/////////////////////////////////////////////////////////////////////////////////////////////////////
type Tインターネットプロトコル_處理器_資料 struct{
	後端部 Tインターネットプロトコル_提供者
	プロトコル uint8
}
var 處理器_資料 Tインターネットプロトコル_處理器_資料

type Tインターネットプロトコル_處理器 struct{
}
func (自身 *Tインターネットプロトコル_處理器) M初期化(後端部 Tインターネットプロトコル_提供者, インターネットプロトコル_處理器 Iインターネットプロトコル_處理器, プロトコル uint8){
	處理器_資料.プロトコル = プロトコル
	處理器_資料.後端部 = 後端部
	資料.インターネットプロトコル_處理器[プロトコル] = インターネットプロトコル_處理器
}
func (自身 *Tインターネットプロトコル_處理器) Mインターネットプロトコル_受信と同時(送信元アイピー住所_BE uint32, 宛先アイピー住所_BE uint32, 資料住所 uintptr, 大きさ uint32) bool{
	return false
}
func (自身 *Tインターネットプロトコル_處理器) Mパケット送信(宛先アイピー住所_BE uint32, プロトコル uint8, 資料住所 uintptr, 大きさ uint32){
	處理器_資料.後端部.Mパケット送信(宛先アイピー住所_BE, プロトコル, 資料住所, 大きさ)
}
func (自身 *Tインターネットプロトコル_處理器) M提供者を得る() *Tインターネットプロトコル_提供者 {
	return &處理器_資料.後端部
}
/////////////////////////////////////////////////////////////////////////////////////////////////////
type Tインターネットプロトコル_提供者_資料 struct{
	アドレス解決プロトコル_提供者 Tアドレス解決プロトコル_提供者
	ゲートウェイ住所 uint32
	サブネットマスク uint32
	インターネットプロトコル_處理器 [255]Iインターネットプロトコル_處理器
}
var 資料 Tインターネットプロトコル_提供者_資料

type Tインターネットプロトコル_提供者 struct{
	Tイーサネットフレーム_處理器
}
func (自身 *Tインターネットプロトコル_提供者) M初期化(後端部 Tイーサネットフレーム_提供者) { //, 
	
	自身.Tイーサネットフレーム_處理器.M初期化(後端部)
	自身.Tイーサネットフレーム_處理器.M處理器を設定(自身, 0x0800)

	for i:=0; i<255; i++ {
		資料.インターネットプロトコル_處理器[i] = nil
	}
	
}
func (自身 *Tインターネットプロトコル_提供者) M住所設定(アドレス解決プロトコル_提供者 Tアドレス解決プロトコル_提供者, ゲートウェイ住所 uint32, サブネットマスク uint32){
	資料.アドレス解決プロトコル_提供者 = アドレス解決プロトコル_提供者
	資料.ゲートウェイ住所 = ゲートウェイ住所
	資料.サブネットマスク = サブネットマスク
}

func (自身 *Tインターネットプロトコル_提供者) Mイーサネットフレーム_受信と同時(イーサネット搭載資料 uintptr, 大きさ uint32) bool{

	if 大きさ < uint32(インターネットプロトコル_頭文字_大きさ) {
		return false
	}
	
	var 緩衝器 *TインターネットプロトコルV4メッセージ_緩衝器 = (*TインターネットプロトコルV4メッセージ_緩衝器)(Pointer(イーサネット搭載資料))
	var メッセージ TインターネットプロトコルV4メッセージ
	メッセージ.M初期化(緩衝器)

	var sendBack bool = false

	if メッセージ.宛先アイピー住所 == uint32(自身.Mアイピー住所を取得する()) {

		var length uint32 = uint32(メッセージ.全体の長さ)
		if length > 大きさ {
			length = 大きさ
		}
		if 資料.インターネットプロトコル_處理器[メッセージ.プロトコル] != nil {
			sendBack  = 資料.インターネットプロトコル_處理器[メッセージ.プロトコル].Mインターネットプロトコル_受信と同時(メッセージ.送信元アイピー住所, 
									メッセージ.宛先アイピー住所, 
									イーサネット搭載資料 + uintptr(4*メッセージ.頭文字の長さ), 
									uint32(length-uint32(4*メッセージ.頭文字の長さ)))

		}
	}

	if(sendBack) {
		var 臨時 = メッセージ.宛先アイピー住所
		メッセージ.宛先アイピー住所 = メッセージ.送信元アイピー住所
		メッセージ.送信元アイピー住所 = 臨時

		メッセージ.寿命 = 0x40
		メッセージ.検査合計 = 0
		
		メッセージ.M緩衝器_設定(緩衝器)
		メッセージ.検査合計 = 自身.M検査合計((*([4096]uint16))(Pointer(イーサネット搭載資料)), uint32(4*メッセージ.頭文字の長さ))
		メッセージ.M緩衝器_設定(緩衝器)

	}

	return sendBack

}
func (自身 *Tインターネットプロトコル_提供者) Mパケット送信(宛先アイピー住所_BE uint32, プロトコル uint8, 資料住所 uintptr, 大きさ uint32) {
	var 緩衝器1 [4096] byte
	var 緩衝器 *TインターネットプロトコルV4メッセージ_緩衝器 = (*TインターネットプロトコルV4メッセージ_緩衝器)(Pointer(&緩衝器1))
	var メッセージ TインターネットプロトコルV4メッセージ  = TインターネットプロトコルV4メッセージ{}
	メッセージ.校閲 = 4
	メッセージ.頭文字の長さ = インターネットプロトコル_頭文字_大きさ/4
	メッセージ.サービス流刑 = 0
	メッセージ.全体の長さ = Uint16_R(uint16(大きさ + uint32(インターネットプロトコル_頭文字_大きさ)))

	メッセージ.識別子 = 0x0100
	メッセージ.表示と変位差 = 0x0040
	メッセージ.寿命 = 0x40
	メッセージ.プロトコル = プロトコル
	
	メッセージ.宛先アイピー住所 = 宛先アイピー住所_BE

	メッセージ.送信元アイピー住所 = uint32(自身.Mアイピー住所を取得する())

	メッセージ.検査合計 = 0

	メッセージ.M緩衝器_設定(緩衝器)
	メッセージ.検査合計 = 自身.M検査合計((*([4096]uint16))(Pointer(&緩衝器1)), uint32(インターネットプロトコル_頭文字_大きさ))
	メッセージ.M緩衝器_設定(緩衝器)

	var 자료_緩衝器 [4096] byte = *(*([4096]byte))(Pointer(資料住所))
	for i:=0; i<int(大きさ); i++ {
		緩衝器1[i+int(インターネットプロトコル_頭文字_大きさ)] = 자료_緩衝器[i]
	}

	var 経路 uint32 = 宛先アイピー住所_BE
	if (宛先アイピー住所_BE & 資料.サブネットマスク) != (メッセージ.送信元アイピー住所 & 資料.サブネットマスク) {
		経路 = 資料.ゲートウェイ住所
	}

	var 送る資料の住所 = uintptr(Pointer(&緩衝器1))

	var etherType_BE = Uint16_R(0x0800)
	自身.Mフレーム送信(資料.アドレス解決プロトコル_提供者.Resolve(経路), etherType_BE, 送る資料の住所, uint32(インターネットプロトコル_頭文字_大きさ)+uint32(大きさ))
}
func (自身 *Tインターネットプロトコル_提供者) M検査合計(p_data *[4096]uint16, lengthInBytes uint32) uint16{
	var data [4096] uint16 = *p_data

	var 臨時 uint32 = 0
	for i:=0; i<int(lengthInBytes/2); i++ {
		臨時 += uint32(Uint16_R(data[i]))
	}
	var dataBytes [4096] byte = *(*([4096]byte))(Pointer(&data))
	if (lengthInBytes%2) !=0 {
		臨時 += uint32(uint16(dataBytes[lengthInBytes-1]) << 8)
	}

	for (臨時 & 0xFFFF0000) != 0 {
		臨時 = (臨時 & 0xFFFF) + (臨時 >> 16)
	}

	return uint16(((^臨時 & 0xFF00) >> 8) | ((^臨時 & 0x00FF) << 8))
}
func (自身 *Tインターネットプロトコル_提供者) Mアイピー住所を取得する() uint64{
        return 自身.Tイーサネットフレーム_處理器.Mアイピー住所を取得する()
}

