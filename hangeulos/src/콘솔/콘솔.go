/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 콘솔

import . "unsafe"


const (
        넓이            = 80
        높이           = 25
        실메모리주소 uintptr = 0xb8000
)

type T콘솔 struct{
        x위치 uint16
        y위치 uint16
}
func (자신 *T콘솔)M출력(매개값 ...interface{}){
	var x uint16 = 1000
	var y uint16 = 1000 
	var 값 interface{}

	for i, p := range 매개값{
		switch i {
			case 0:
				param, _ := p.(interface{})
				값 = param
			case 1:
				switch p.(type) {
					case uint16:
						param, _ := p.(uint16)
						x = param
					case int:
						param, _ := p.(int)
						x = uint16(param)
				}
			case 2:
				switch p.(type) {
					case uint16:
						param, _ := p.(uint16)
						y = param
					case int:
						param, _ := p.(int)
						y = uint16(param)
				}
		}
	}

	자신.M출력XY(값, x, y)

}
func (자신 *T콘솔)M출력XY(임시 interface{}, x uint16, y uint16){

	switch 임시.(type) {
		case string:
			자료, _ := 임시.(string)
			자신.M출력BytesXY(([]byte)(자료), x, y)
		case uint8:
			자료, _ := 임시.(uint8)
			자신.MHex출력XY(자료, x, y)
		case uint16:
			자료, _ := 임시.(uint16)
			자신.MUint16출력XY(자료, x, y)
		case uint32:
			자료, _ := 임시.(uint32)
			자신.MUint32출력XY(자료, x, y)
		case uint64:
			자료, _ := 임시.(uint64)
			자신.MUint64출력XY(자료, x, y)
		default:
			자료, _ := 임시.([]byte)
			자신.M출력BytesXY(자료, x, y)
	}

}
func (자신 *T콘솔)M출력Bytes(임시 []byte){
	자신.M출력XY(임시, 1000, 1000)
}

func (자신 *T콘솔)M출력BytesXY(임시 []byte, x uint16, y uint16){

        if x <=999  {
                자신.x위치 = x
        }
        if y <=999 {
                자신.y위치 = y
        }


        속성 := uint16(0x0F)
        for i:=0; i<len(임시); i++ {
                switch 임시[i] {
                case '\n':
                        자신.y위치++
                        자신.x위치 = 0
                default:
                        *(*uint16)(Pointer(실메모리주소 + uintptr((80*자신.y위치+자신.x위치)*2))) = 속성<<8 | uint16(임시[i])
                        자신.x위치++
                }
        }

        if 자신.x위치 >= 80 {
                자신.y위치++
                자신.x위치 = 0
        }

        if 자신.y위치 >= 25 {
                for 자신.y위치=0; 자신.y위치<25; 자신.y위치++ {
                        for 자신.x위치=0; 자신.x위치<80; 자신.x위치++ {
                        *(*uint16)(Pointer(실메모리주소 + uintptr((80*자신.y위치+자신.x위치)*2))) = 속성<<8 | ' '
                        }
                }
                자신.x위치 = 0
                자신.y위치 = 0
        }

	
}
func (자신 *T콘솔)MHex출력(key uint8){
	임시 := []byte {'0', '0'}
	hex := [16] byte{'0', '1', '2', '3', 
			'4', '5', '6', '7', 
			'8', '9', 'A', 'B', 
			'C', 'D', 'E', 'F'}
	임시[0] = hex[(key >> 4) & 0xF]
	임시[1] = hex[key  & 0xF]
	자신.M출력(임시)
}
func (자신 *T콘솔)MHex출력XY(key uint8, x uint16, y uint16){
        임시 := []byte {'0', '0', 0}
        hex := [16] byte{'0', '1', '2', '3',
                        '4', '5', '6', '7',
                        '8', '9', 'A', 'B',
                        'C', 'D', 'E', 'F'}
        임시[0] = hex[(key >> 4) & 0xF]
        임시[1] = hex[key  & 0xF]
        자신.M출력XY(임시, x, y)
}
func (자신 *T콘솔)MUint16출력(key uint16){
        자신.MHex출력(uint8(key>>8))
        자신.MHex출력(uint8(key))
}
func (자신 *T콘솔)MUint16출력XY(key uint16, x uint16, y uint16){
        자신.MHex출력XY(uint8(key>>8), x, y)
        자신.MHex출력XY(uint8(key), x, y)
}
func (자신 *T콘솔)MUint32출력(자료 uint32) {
        자신.MHex출력(uint8(자료>>24))
        자신.MHex출력(uint8(자료>>16))
        자신.MHex출력(uint8(자료>>8))
        자신.MHex출력(uint8(자료))
}

func (자신 *T콘솔)MUint32출력XY(자료 uint32, x uint16, y uint16) {

        자신.MHex출력XY(uint8(자료>>24), x+0, y)
        자신.MHex출력XY(uint8(자료>>16), x+2, y)
        자신.MHex출력XY(uint8(자료>>8),  x+4, y)
        자신.MHex출력XY(uint8(자료),     x+6, y)
}
func (자신 *T콘솔)MUint48출력(자료 uint64) {
        자신.MHex출력(uint8(자료>>40))
        자신.MHex출력(uint8(자료>>32))
        자신.MHex출력(uint8(자료>>24))
        자신.MHex출력(uint8(자료>>16))
        자신.MHex출력(uint8(자료>>8))
        자신.MHex출력(uint8(자료))
}
func (자신 *T콘솔)MUint48출력XY(자료 uint64, x uint16, y uint16) {
        자신.MHex출력XY(uint8(자료>>40), x+0, y)
        자신.MHex출력XY(uint8(자료>>32), x+2, y)
        자신.MHex출력XY(uint8(자료>>24), x+6, y)
        자신.MHex출력XY(uint8(자료>>16), x+8, y)
        자신.MHex출력XY(uint8(자료>>8),  x+10, y)
        자신.MHex출력XY(uint8(자료),     x+12, y)
}
func (자신 *T콘솔)MUint64출력(자료 uint64) {
        자신.MHex출력(uint8(자료>>56))
        자신.MHex출력(uint8(자료>>48))
        자신.MHex출력(uint8(자료>>40))
        자신.MHex출력(uint8(자료>>32))
        자신.MHex출력(uint8(자료>>24))
        자신.MHex출력(uint8(자료>>16))
        자신.MHex출력(uint8(자료>>8))
        자신.MHex출력(uint8(자료))
}
func (자신 *T콘솔)MUint64출력XY(자료 uint64, x uint16, y uint16) {
        자신.MHex출력XY(uint8(자료>>56), x+0, y)
        자신.MHex출력XY(uint8(자료>>48), x+2, y)
        자신.MHex출력XY(uint8(자료>>40), x+4, y)
        자신.MHex출력XY(uint8(자료>>32), x+6, y)
        자신.MHex출력XY(uint8(자료>>24), x+8, y)
        자신.MHex출력XY(uint8(자료>>16), x+10, y)
        자신.MHex출력XY(uint8(자료>>8),  x+12, y)
        자신.MHex출력XY(uint8(자료),     x+14, y)
}


