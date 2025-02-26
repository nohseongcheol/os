package port

/////////////////////////////////////////////////////////////////
//
// 		Port = 入出力ポート				      //
//
/////////////////////////////////////////////////////////////////
type T入出力ポート struct{
	入出力ポート番号 uint16
}
/////////////////////////////////////////////////////////////////
type Tバイト入出力ポート struct{
	T入出力ポート
}
func (自身 *Tバイト入出力ポート) M初期化(p_入出力ポート番号 uint16){
	自身.入出力ポート番号= p_入出力ポート番号
}
func (自身 *Tバイト入出力ポート) M作成(p_データ uint8){
	PortOutByte(自身.入出力ポート番号, p_データ)
}
func (自身 *Tバイト入出力ポート) M読み取り() uint8{
	return PortInByte(自身.入出力ポート番号)
}

/////////////////////////////////////////////////////////////////
type Tワード入出力ポート struct{
	T入出力ポート
}
func (自身 *Tワード入出力ポート) M初期化(p_入出力ポート番号 uint16){
        自身.入出力ポート番号= p_入出力ポート番号
}
func (自身 *Tワード入出力ポート) M作成(p_データ uint16){
        PortOutWord(自身.入出力ポート番号, p_データ)
}
func (自身 *Tワード入出力ポート) M読み取り() uint16{
        return PortInWord(自身.入出力ポート番号)
}
/////////////////////////////////////////////////////////////////
type Tダブルワード入出力ポート struct{
	T入出力ポート
}
func (自身 *Tダブルワード入出力ポート) M初期化(p_入出力ポート番号 uint16){
	自身.入出力ポート番号 = p_入出力ポート番号
}
func (自身 *Tダブルワード入出力ポート) M作成(p_データ uint32){
	PortOutDword(自身.入出力ポート番号, p_データ)
}
func (自身 *Tダブルワード入出力ポート) M読み取り() uint32{
	return PortInDword(自身.入出力ポート番号)
}
/////////////////////////////////////////////////////////////////
func PortOutByte(portnumber uint16, data uint8)
func PortInByte(portnumber uint16) uint8

func PortOutWord(portnumber uint16, data uint16)
func PortInWord(portnumber uint16) uint16

func PortOutDword(portnumber uint16, data uint32)
func PortInDword(portnumber uint16) uint32

