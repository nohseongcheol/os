/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package port

var pos uint16=1
/////////////////////////////////////////////////////////////////
//
// 		Port = 포트				      //
//
/////////////////////////////////////////////////////////////////
type T포트 struct{
	포트번호 uint16
}
/////////////////////////////////////////////////////////////////
type T바이트포트 struct{
	T포트
}
func (자신 *T바이트포트) M초기화(p_포트번호 uint16){
	자신.포트번호= p_포트번호
}
func (자신 *T바이트포트) M쓰기(p_자료 uint8){
	바이트출력포트(자신.포트번호, p_자료)
}
func (자신 *T바이트포트) M읽기() uint8{
	return 바이트입력포트(자신.포트번호)
}

/////////////////////////////////////////////////////////////////
type T워드포트 struct{
	T포트
}
func (자신 *T워드포트) M초기화(p_포트번호 uint16){
        자신.포트번호= p_포트번호
}
func (자신 *T워드포트) M쓰기(p_자료 uint16){
        워드출력포트(자신.포트번호, p_자료)
}
func (자신 *T워드포트) M읽기() uint16{
        return 워드입력포트(자신.포트번호)
}
/////////////////////////////////////////////////////////////////
type T더블워드포트 struct{
	T포트
}
func (자신 *T더블워드포트) M초기화(p_포트번호 uint16){
	자신.포트번호 = p_포트번호
}
func (자신 *T더블워드포트) M쓰기(p_자료 uint32){
	더블워드출력포트(자신.포트번호, p_자료)
}
func (자신 *T더블워드포트) M읽기() uint32{
	return 더블워드입력포트(자신.포트번호)
}
/////////////////////////////////////////////////////////////////

func 바이트출력포트(portnumber uint16, data uint8)
func 바이트입력포트(portnumber uint16) uint8

func 워드출력포트(portnumber uint16, data uint16)
func 워드입력포트(portnumber uint16) uint16

func 더블워드출력포트(portnumber uint16, data uint32)
func 더블워드입력포트(portnumber uint16) uint32

