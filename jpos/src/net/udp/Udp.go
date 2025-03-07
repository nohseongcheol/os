/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package ユーザデータグラムプロトコル

import . "unsafe"
import . "console"
import . "util"
import . "memorymanager"
import . "net/ipv4"


///////////////////////////////////////////////////////////////////////////
var 端末機 = T端末機{}
///////////////////////////////////////////////////////////////////////////
//
//		ユーザデータグラムプロトコル = UserDatagram Protocol = UDP
//		입출구 = Port
//		ユーザデータグラムプロトコル_ソケット = UserDatagramProtocolSocket = UDPSocket
//		受信待ち = listen
///////////////////////////////////////////////////////////////////////////
type Tユーザデータグラムプロトコル_ヘッダ_緩衝器 struct{
	送信元ポート番号 [2]byte	// source port number
	宛先ポート番号 [2]byte		// destination port number

	長さ [2]byte			// length
	検査合計 [2]byte		// checksum
}
var UDP頭文字大きさ uint32 = 8
type Tユーザデータグラムプロトコル_ヘッダ struct{
	送信元ポート番号 uint16		// source port number
	宛先ポート番号 uint16		// destination port number

	長さ uint16			// length
	検査合計 uint16			// checksum
}
func (自身 *Tユーザデータグラムプロトコル_ヘッダ) M初期化(緩衝器 *Tユーザデータグラムプロトコル_ヘッダ_緩衝器){
	自身.送信元ポート番号 = ArrayToUint16(緩衝器.送信元ポート番号)
	自身.宛先ポート番号 = ArrayToUint16(緩衝器.宛先ポート番号)
	
	自身.長さ = ArrayToUint16(緩衝器.長さ)
	自身.検査合計 = ArrayToUint16(緩衝器.検査合計)
}
func (自身 *Tユーザデータグラムプロトコル_ヘッダ) 緩衝器_設定(緩衝器 *Tユーザデータグラムプロトコル_ヘッダ_緩衝器){

	緩衝器.送信元ポート番号 = Uint16ToArray(自身.送信元ポート番号)
	緩衝器.宛先ポート番号 = Uint16ToArray(自身.宛先ポート番号)

	緩衝器.長さ = Uint16ToArray(自身.長さ)
	緩衝器.検査合計 = Uint16ToArray(自身.検査合計)

}

///////////////////////////////////////////////////////////////////////////
type Iユーザデータグラムプロトコル_處理器 interface{
	ユーザデータグラムプロトコル_メッセージ_処理する(ソケット *Tユーザデータグラムプロトコル_ソケット, data uintptr, 大きさ uint16)
}
///////////////////////////////////////////////////////////////////////////
type Tユーザデータグラムプロトコル_處理器 struct{
}
func (自身 *Tユーザデータグラムプロトコル_處理器) M初期化(backend Tインターネットプロトコル_提供者) {
}
func (自身 *Tユーザデータグラムプロトコル_處理器) ユーザデータグラムプロトコル_メッセージ_処理する(ソケット *Tユーザデータグラムプロトコル_ソケット, data uintptr, 大きさ uint16){
}

///////////////////////////////////////////////////////////////////////////
type Iユーザデータグラムプロトコル_ソケット interface{
	ユーザデータグラムプロトコル_メッセージ_処理する(data uintptr, 大きさ uint16)
}
type Tユーザデータグラムプロトコル_ソケット struct{
	遠隔ポート番号 uint16
	遠隔アイピー住所 uint32
	自身ポート番号 uint16
	自身アイピー住所 uint32

	受信待ち bool

	Pユーザデータグラムプロトコル_提供者 Tユーザデータグラムプロトコル_提供者
	Pユーザデータグラムプロトコル_處理器 Iユーザデータグラムプロトコル_處理器
}

func (自身 *Tユーザデータグラムプロトコル_ソケット) M初期化(p_ユーザデータグラムプロトコル_提供者 Tユーザデータグラムプロトコル_提供者){ 
	自身.Pユーザデータグラムプロトコル_提供者 = p_ユーザデータグラムプロトコル_提供者
	/*
	if 自身.Pユーザデータグラムプロトコル_處理器 == nil  && p_ユーザデータグラムプロトコル_處理器 != nil{
		自身.Pユーザデータグラムプロトコル_處理器 = p_ユーザデータグラムプロトコル_處理器
	}
	*/
	自身.受信待ち = false
}
func (自身 *Tユーザデータグラムプロトコル_ソケット) ユーザデータグラムプロトコル_メッセージ_処理する(data uintptr, 大きさ uint16){

	if 自身.Pユーザデータグラムプロトコル_處理器 != nil {
		自身.Pユーザデータグラムプロトコル_處理器.ユーザデータグラムプロトコル_メッセージ_処理する(自身, data, 大きさ)
	}
}
func (自身 *Tユーザデータグラムプロトコル_ソケット) M送信(p_資料 []byte, 大きさ uint16){
	var 緩衝器 [4096] byte
	for i:=0; i<int(大きさ); i++ {
		緩衝器[i] = p_資料[i]
	}
	var data = uintptr(Pointer(&緩衝器))
	自身.Pユーザデータグラムプロトコル_提供者.M送信(自身, data, 大きさ)
}
func (自身 *Tユーザデータグラムプロトコル_ソケット) M切断する(){
	自身.Pユーザデータグラムプロトコル_提供者.M切断する(自身)
}
///////////////////////////////////////////////////////////////////////////
type Tユーザデータグラムプロトコル_提供者_資料 struct{
	ソケット [65535] Tユーザデータグラムプロトコル_ソケット
	ソケット数 int
	余裕ポート番号 uint16 // freePort
}
var 資料 Tユーザデータグラムプロトコル_提供者_資料

type Tユーザデータグラムプロトコル_提供者 struct{
	Tインターネットプロトコル_處理器
}
func (自身 *Tユーザデータグラムプロトコル_提供者) M初期化(p_ipProvider Tインターネットプロトコル_提供者){
	自身.Tインターネットプロトコル_處理器.M初期化(p_ipProvider, 自身, 0x11)
	資料.ソケット数 = 0
	資料.余裕ポート番号 = 1024
}
func (自身 *Tユーザデータグラムプロトコル_提供者) Mインターネットプロトコル_受信と同時(送信元IP住所_逆順 uint32, 宛先IP住所_逆順 uint32, IP搭載資料 uintptr, 大きさ uint32) bool{
	if 大きさ < UDP頭文字大きさ {
		return false
	}
	
	var 緩衝器 *Tユーザデータグラムプロトコル_ヘッダ_緩衝器 = (*Tユーザデータグラムプロトコル_ヘッダ_緩衝器)(Pointer(IP搭載資料))
	var ヘッダ Tユーザデータグラムプロトコル_ヘッダ
	ヘッダ.M初期化(緩衝器)


	var ソケット *Tユーザデータグラムプロトコル_ソケット = nil
	
	for i:=0; i<資料.ソケット数 && ソケット==nil; i++ {

		if 資料.ソケット[i].自身ポート番号 == ヘッダ.宛先ポート番号 && 
		   資料.ソケット[i].自身アイピー住所 == 宛先IP住所_逆順 && 
		   資料.ソケット[i].受信待ち == true 	{

			ソケット = &資料.ソケット[i]
			ソケット.受信待ち = false
			ソケット.遠隔ポート番号 = ヘッダ.送信元ポート番号
			ソケット.遠隔アイピー住所 = 送信元IP住所_逆順

		}else if 資料.ソケット[i].自身ポート番号 == ヘッダ.宛先ポート番号 && 
		  資料.ソケット[i].自身アイピー住所 == 宛先IP住所_逆順 && 
		  資料.ソケット[i].遠隔ポート番号 == ヘッダ.送信元ポート番号 && 
		  資料.ソケット[i].遠隔アイピー住所 == 送信元IP住所_逆順	{

			ソケット = &資料.ソケット[i]
	
		}
	}
	
	ヘッダ.緩衝器_設定(緩衝器)
	if ソケット != nil {
		ソケット.ユーザデータグラムプロトコル_メッセージ_処理する(IP搭載資料 + uintptr(UDP頭文字大きさ), uint16(大きさ - UDP頭文字大きさ))
	}

	return false
}

func (自身 *Tユーザデータグラムプロトコル_提供者) M接続する(アイピー住所 uint32, ポート番号 uint16) *Tユーザデータグラムプロトコル_ソケット{
	var memoryManager = &TMemoryManager{}
	var ソケット = (*Tユーザデータグラムプロトコル_ソケット)(memoryManager.Malloc(50))

	if ソケット != nil {
		
		ソケット.M初期化(*自身)
		ソケット.遠隔ポート番号 = ポート番号
		ソケット.遠隔アイピー住所 = アイピー住所
		ソケット.自身ポート番号 = 資料.余裕ポート番号 
		資料.余裕ポート番号++
		ソケット.自身アイピー住所 = uint32((*自身.Tインターネットプロトコル_處理器.M提供者を得る()).Mアイピー住所を取得する())

		ソケット.遠隔ポート番号 = Uint16_R(ソケット.遠隔ポート番号)
		ソケット.自身ポート番号 = Uint16_R(ソケット.自身ポート番号)
		
		資料.ソケット[資料.ソケット数] = *ソケット
		資料.ソケット数++

	}
	return ソケット
	
}
func (自身 *Tユーザデータグラムプロトコル_提供者) M受信待ち(ポート番号 uint16) *Tユーザデータグラムプロトコル_ソケット{
	var memoryManager = &TMemoryManager{}
	var ソケット = (*Tユーザデータグラムプロトコル_ソケット)(memoryManager.Malloc(50))
	if ソケット != nil {
		
		ソケット.M初期化(*自身)
		ソケット.受信待ち = true
		ソケット.自身ポート番号 = ポート番号
		ソケット.自身アイピー住所 = uint32((*自身.Tインターネットプロトコル_處理器.M提供者を得る()).Mアイピー住所を取得する())

		ソケット.自身ポート番号 = ソケット.自身ポート番号

		//端末機.M出力XY(ソケット.自身ポート番号, 5, 19)
	}
	return ソケット
}
func (自身 *Tユーザデータグラムプロトコル_提供者) M切断する(ソケット *Tユーザデータグラムプロトコル_ソケット){
	for i:=0; i<資料.ソケット数 && ソケット==nil; i++ {
		if 資料.ソケット[i] == *ソケット {
			資料.ソケット数--
			資料.ソケット[i] = 資料.ソケット[資料.ソケット数]
			break
		}
	}
}
func (自身 *Tユーザデータグラムプロトコル_提供者) M送信(ソケット *Tユーザデータグラムプロトコル_ソケット, p_資料 uintptr, 大きさ uint16){
	var 全体の長さ = uint32(大きさ) + UDP頭文字大きさ
	
	var 緩衝器 [4096]byte
	var ヘッダ_緩衝器 = (*Tユーザデータグラムプロトコル_ヘッダ_緩衝器)(Pointer(&緩衝器))
	
	var ヘッダ = Tユーザデータグラムプロトコル_ヘッダ{}

	ヘッダ.送信元ポート番号 = ソケット.自身ポート番号
	ヘッダ.宛先ポート番号 = ソケット.遠隔ポート番号
	ヘッダ.長さ = Uint16_R(uint16(全体の長さ))

	ヘッダ.検査合計 = 0x0
	ヘッダ.緩衝器_設定(ヘッダ_緩衝器)

	var dataBytes [4096]byte = *(*[4096]byte)(Pointer(p_資料))
	for i:=0; i<int(大きさ); i++ {
		緩衝器[int(UDP頭文字大きさ)+i] = dataBytes[i]
	}

	var 資料住所 uintptr = uintptr(Pointer(&緩衝器))
	

	自身.Tインターネットプロトコル_處理器.Mパケット送信(ソケット.遠隔アイピー住所, 0x11, 資料住所, 全体の長さ)
	
}
func (自身 *Tユーザデータグラムプロトコル_提供者) M結合する(ソケット *Tユーザデータグラムプロトコル_ソケット, 處理器 *Tユーザデータグラムプロトコル_處理器){
	ソケット.Pユーザデータグラムプロトコル_處理器 = 處理器
}
