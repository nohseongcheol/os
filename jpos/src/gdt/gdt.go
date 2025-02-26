package gdt

import . "unsafe"

func 大域記述子表を搭載(x uintptr)

///////////////////////////////////////////////////////////////////////////////////////////
//
//		分節記述子 = Segment Descriptor
//
///////////////////////////////////////////////////////////////////////////////////////////
type T分節記述子 struct{
	限度lo 		uint16	// limit low
	基準lo 		uint16	// base low
	基準hi 		uint8	// base high
	類型		uint8	// type
	標示の限度hi 	uint8	// flags limit high
	基準vhi		uint8	// base very high
}

func (自身 *T分節記述子) M初期化(基準 uint32, 限度 uint32, 標示 uint8) {

	if(限度 <= 65536) {
		自身.標示の限度hi = 0x40
	} else {
		if((限度 & 0xFFF) != 0xFFF){
			限度 = (限度 >> 12) -1
		}else{
			限度 = 限度 >> 12
		}
		自身.標示の限度hi = 0xC0
	}


	自身.限度lo = uint16(限度)
	自身.基準lo  = uint16(基準)

	自身.基準hi = uint8((基準 >> 16) & 0xFF)
	自身.基準vhi= uint8((基準 >> 24) & 0xFF)

	自身.類型 = 標示
	自身.標示の限度hi = 自身.標示の限度hi | uint8((限度 >> 16) & 0xF)

}
///////////////////////////////////////////////////////////////////////////////////////////
//
//		大域記述子表 = global descriptor table
//
///////////////////////////////////////////////////////////////////////////////////////////
type T大域記述子表_資料 struct{
	空白の分節記述子 	T分節記述子
	符号の分節記述子 	T分節記述子
	資料の分節記述子 	T分節記述子
}
var 資料 T大域記述子表_資料

type T大域記述子表 struct{
}
func (自身 *T大域記述子表) M初期化(){

	資料.空白の分節記述子.M初期化(0, 0, 0)
	資料.符号の分節記述子.M初期化(0, 64*1024*1024, 0x9A)
	資料.資料の分節記述子.M初期化(0, 64*1024*1024, 0x92)

	標的 := [6]uint8{0,0,0,0,0,0}
	基準住所 := (*uint32)(Pointer(&標的[2]))
	(*基準住所) = uint32(uintptr(Pointer(&資料)))
	
	大きさ := (*uint16)(Pointer(&標的[0]))
	(*大きさ) = (uint16)((Sizeof(資料)))

	大域記述子表を搭載(uintptr(Pointer(&標的)))

}
func (自身 *T大域記述子表) M符号の分節を選択() uint16{
	return uint16(uintptr(Pointer(&資料.符号の分節記述子)) - uintptr(Pointer(&資料)))
}
func (自身 *T大域記述子表) M資料の分節を選択() uint16{
	return uint16(uintptr(Pointer(&資料.資料の分節記述子)) - uintptr(Pointer(&資料)))
}
