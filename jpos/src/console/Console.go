package 端末機

import . "unsafe"


const (
        幅            = 80
        高           = 25
        実際メモリの住所 uintptr = 0xb8000
)

type T端末機 struct{
        x位置 uint16
        y位置 uint16
}
func (自身 *T端末機)M出力(媒介値 ...interface{}){
	var x uint16 = 1000
	var y uint16 = 1000 
	var 値 interface{}

	for i, p := range 媒介値{
		switch i {
			case 0:
				param, _ := p.(interface{})
				値 = param
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

	自身.M出力XY(値, x, y)

}
func (自身 *T端末機)M出力XY(臨時 interface{}, x uint16, y uint16){

	switch 臨時.(type) {
		case string:
			資料, _ := 臨時.(string)
			自身.M出力BytesXY(([]byte)(資料), x, y)
		case uint8:
			資料, _ := 臨時.(uint8)
			自身.MHex出力XY(資料, x, y)
		case uint16:
			資料, _ := 臨時.(uint16)
			自身.MUint16出力XY(資料, x, y)
		case uint32:
			資料, _ := 臨時.(uint32)
			自身.MUint32出力XY(資料, x, y)
		case uint64:
			資料, _ := 臨時.(uint64)
			自身.MUint64出力XY(資料, x, y)
		default:
			資料, _ := 臨時.([]byte)
			自身.M出力BytesXY(資料, x, y)
	}

}
func (自身 *T端末機)M出力Bytes(臨時 []byte){
	自身.M出力XY(臨時, 1000, 1000)
}

func (自身 *T端末機)M出力BytesXY(臨時 []byte, x uint16, y uint16){

        if x <=999  {
                自身.x位置 = x
        }
        if y <=999 {
                自身.y位置 = y
        }


        属性 := uint16(0x0F)
        for i:=0; i<len(臨時); i++ {
                switch 臨時[i] {
                case '\n':
                        自身.y位置++
                        自身.x位置 = 0
                default:
                        *(*uint16)(Pointer(実際メモリの住所 + uintptr((80*自身.y位置+自身.x位置)*2))) = 属性<<8 | uint16(臨時[i])
                        自身.x位置++
                }
        }

        if 自身.x位置 >= 80 {
                自身.y位置++
                自身.x位置 = 0
        }

        if 自身.y位置 >= 25 {
                for 自身.y位置=0; 自身.y位置<25; 自身.y位置++ {
                        for 自身.x位置=0; 自身.x位置<80; 自身.x位置++ {
                        *(*uint16)(Pointer(実際メモリの住所 + uintptr((80*自身.y位置+自身.x位置)*2))) = 属性<<8 | ' '
                        }
                }
                自身.x位置 = 0
                自身.y位置 = 0
        }

	
}
func (自身 *T端末機)MHex出力(key uint8){
	臨時 := []byte {'0', '0'}
	hex := [16] byte{'0', '1', '2', '3', 
			'4', '5', '6', '7', 
			'8', '9', 'A', 'B', 
			'C', 'D', 'E', 'F'}
	臨時[0] = hex[(key >> 4) & 0xF]
	臨時[1] = hex[key  & 0xF]
	自身.M出力(臨時)
}
func (自身 *T端末機)MHex出力XY(key uint8, x uint16, y uint16){
        臨時 := []byte {'0', '0', 0}
        hex := [16] byte{'0', '1', '2', '3',
                        '4', '5', '6', '7',
                        '8', '9', 'A', 'B',
                        'C', 'D', 'E', 'F'}
        臨時[0] = hex[(key >> 4) & 0xF]
        臨時[1] = hex[key  & 0xF]
        自身.M出力XY(臨時, x, y)
}
func (自身 *T端末機)MUint16出力(key uint16){
        自身.MHex出力(uint8(key>>8))
        自身.MHex出力(uint8(key))
}
func (自身 *T端末機)MUint16出力XY(key uint16, x uint16, y uint16){
        自身.MHex出力XY(uint8(key>>8), x, y)
        自身.MHex出力XY(uint8(key), x, y)
}
func (自身 *T端末機)MUint32出力(資料 uint32) {
        自身.MHex出力(uint8(資料>>24))
        自身.MHex出力(uint8(資料>>16))
        自身.MHex出力(uint8(資料>>8))
        自身.MHex出力(uint8(資料))
}

func (自身 *T端末機)MUint32出力XY(資料 uint32, x uint16, y uint16) {

        自身.MHex出力XY(uint8(資料>>24), x+0, y)
        自身.MHex出力XY(uint8(資料>>16), x+2, y)
        自身.MHex出力XY(uint8(資料>>8),  x+4, y)
        自身.MHex出力XY(uint8(資料),     x+6, y)
}
func (自身 *T端末機)MUint48出力(資料 uint64) {
        自身.MHex出力(uint8(資料>>40))
        自身.MHex出力(uint8(資料>>32))
        自身.MHex出力(uint8(資料>>24))
        自身.MHex出力(uint8(資料>>16))
        自身.MHex出力(uint8(資料>>8))
        自身.MHex出力(uint8(資料))
}
func (自身 *T端末機)MUint48出力XY(資料 uint64, x uint16, y uint16) {
        自身.MHex出力XY(uint8(資料>>40), x+0, y)
        自身.MHex出力XY(uint8(資料>>32), x+2, y)
        自身.MHex出力XY(uint8(資料>>24), x+6, y)
        自身.MHex出力XY(uint8(資料>>16), x+8, y)
        自身.MHex出力XY(uint8(資料>>8),  x+10, y)
        自身.MHex出力XY(uint8(資料),     x+12, y)
}
func (自身 *T端末機)MUint64出力(資料 uint64) {
        自身.MHex出力(uint8(資料>>56))
        自身.MHex出力(uint8(資料>>48))
        自身.MHex出力(uint8(資料>>40))
        自身.MHex出力(uint8(資料>>32))
        自身.MHex出力(uint8(資料>>24))
        自身.MHex出力(uint8(資料>>16))
        自身.MHex出力(uint8(資料>>8))
        自身.MHex出力(uint8(資料))
}
func (自身 *T端末機)MUint64出力XY(資料 uint64, x uint16, y uint16) {
        自身.MHex出力XY(uint8(資料>>56), x+0, y)
        自身.MHex出力XY(uint8(資料>>48), x+2, y)
        自身.MHex出力XY(uint8(資料>>40), x+4, y)
        自身.MHex出力XY(uint8(資料>>32), x+6, y)
        自身.MHex出力XY(uint8(資料>>24), x+8, y)
        自身.MHex出力XY(uint8(資料>>16), x+10, y)
        自身.MHex出力XY(uint8(資料>>8),  x+12, y)
        自身.MHex出力XY(uint8(資料),     x+14, y)
}

