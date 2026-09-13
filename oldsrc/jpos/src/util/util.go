/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package util
import . "console"
import . "unsafe"
import . "reflect"

var util端末機 T端末機 = T端末機{}
func Uint16ToArray(num uint16) [2]byte{
	var array [2]byte
	var i uint
	for i=0; i<2; i++ {
		array[i] = byte(num >> (8*i) & 0x00FF)
	}
	return array
}
func Uint16ToArray_BE(num uint16) [2]byte{
	var array [2]byte
	var i uint
	for i=0; i<2; i++ {
		array[2-i] = byte(num >> (8*i) & 0x00FF)
	}
	return array
}
func Uint32ToArray(num uint32) [4]byte{
	var array [4]byte
	var i uint
	for i=0; i<4; i++ {
		array[i] = byte(num >> (8*i) & 0x000000FF)
	}
	return array
}
func Uint48ToArray(num uint64) [6]byte{
	var array [6]byte
	var i uint
	for i=0; i<6; i++ {
		array[i] = byte(num >> (8*i) & 0x00000000FF)
	}
	return array
}
func Uint48ToArray_BE(num uint64) [6]byte{
	var array [6]byte
	var i uint
	for i=0; i<6; i++ {
		array[5-i] = byte(num >> (8*i) & 0x00000000FF)
	}
	return array
}
func Uint64ToArray(num uint64) [8]byte{
	var array [8]byte
	var i uint
	for i=0; i<4; i++ {
		array[1-i] = byte(num >> (8*i) & 0x00000000000000FF)
	}
	return array
}
func ArrayToUint16(array [2]byte) uint16{
	var num uint16
	var i uint
	for i=0; i<2; i++ {
		num = num | (uint16(array[1-i]) << (8*i))
	}
	return num
}
func ArrayToUint32(array [4]byte) uint32{
	var num uint32
	var i uint
	for i=0; i<4; i++ {
		num = num | (uint32(array[3-i]) << (8*i))
	}
	return num
}
func ArrayToUint48(array [6] byte) uint64{
	var num uint64
	var i uint
	for i=0; i<6; i++ {
		num = num | (uint64(array[5-i]) << (8*i))
	}
	return num
	
}
func ArrayToUint48_BE(array [6] byte) uint64{
	var num uint64
	var i uint
	for i=0; i<6; i++ {
		num = num | (uint64(array[i]) << (8*i))
	}
	return num
}	
func ArrayToUint64(array [8] byte) uint64{
	var num uint64
	var i uint
	for i=0; i<8; i++ {
		num = num | (uint64(array[7-i]) << (8*i))
	}
	return num
}	
func Uint64_R(num uint64) uint64{
	var temp uint64
	var i uint
	for i=0; i<8; i++ {
		temp = temp | (uint64(num >> (8*(7-i)) & 0x00000000000000FF) << (8*i))
	}
	return temp
}
func Uint48_R(num uint64) uint64{
	var temp uint64
	var i uint
	for i=0; i<6; i++ {
		temp = temp | (uint64(num >> (8*(5-i)) & 0x00000000000000FF) << (8*i))
	}
	return temp
}
func Uint32_R(num uint32) uint32{
	var temp uint32
	var i uint
	for i=0; i<4; i++ {
		temp = temp | (uint32(num >> (8*(3-i)) & 0x000000FF) << (8*i))
	}
	return temp
}
func Uint16_R(num uint16) uint16 {
	var temp uint16
	var i uint
	for i=0; i<2; i++ {
		temp = temp | (uint16(num >> (8*(1-i)) & 0x000000FF) << (8*i))
	}
	return temp
}
func PrintBytes(dataPointer uintptr, size int) {
	var buffer [4*1024]byte = *(*([4*1024]byte))(Pointer(dataPointer))
	var i int
	util端末機.M出力([]byte("util["))
	for i=0; i<size; i++ {
		util端末機.MHex出力(buffer[i])
	}
	util端末機.M出力([]byte("]"))
}

func PrintTest(params ... interface{}){
	for _, param := range params {
		util端末機.M出力([]byte(TypeOf(param).Name()))
		/*
		if ValueOf(param) == string{
		}
		*/
	}
}
