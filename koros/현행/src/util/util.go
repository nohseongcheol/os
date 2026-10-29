package 유티아이엘

import . "콘솔"
import . "unsafe"
import . "reflect"

var util콘솔 T콘솔 = T콘솔{}

func U유아이엔티16티오어레이(엔유엠 uint16) [2]byte {
	var 어레이 [2]byte
	var 아이 uint
	for 아이 = 0; 아이 < 2; 아이++ {
		어레이[아이] = byte(엔유엠 >> (8 * 아이) & 0x00FF)
	}
	return 어레이
}
func U유아이엔티16티오어레이비이(엔유엠 uint16) [2]byte {
	var 어레이 [2]byte
	var 아이 uint
	for 아이 = 0; 아이 < 2; 아이++ {
		어레이[2-아이] = byte(엔유엠 >> (8 * 아이) & 0x00FF)
	}
	return 어레이
}

func U유아이엔티32티오어레이(엔유엠 uint32) [4]byte {
	var 어레이 [4]byte
	var 아이 uint
	for 아이 = 0; 아이 < 4; 아이++ {
		어레이[아이] = byte(엔유엠 >> (8 * 아이) & 0x000000FF)
	}
	return 어레이
}
func U유아이엔티48티오어레이(엔유엠 uint64) [6]byte {
	var 어레이 [6]byte
	var 아이 uint
	for 아이 = 0; 아이 < 6; 아이++ {
		어레이[아이] = byte(엔유엠 >> (8 * 아이) & 0x00000000FF)
	}
	return 어레이
}
func U유아이엔티48티오어레이비이(엔유엠 uint64) [6]byte {
	var 어레이 [6]byte
	var 아이 uint
	for 아이 = 0; 아이 < 6; 아이++ {
		어레이[5-아이] = byte(엔유엠 >> (8 * 아이) & 0x00000000FF)
	}
	return 어레이
}
func U유아이엔티64티오어레이(엔유엠 uint64) [8]byte {
	var 어레이 [8]byte
	var 아이 uint
	for 아이 = 0; 아이 < 4; 아이++ {
		어레이[1-아이] = byte(엔유엠 >> (8 * 아이) & 0x00000000000000FF)
	}
	return 어레이
}
func A어레이티오유아이엔티16(어레이 [2]byte) uint16 {
	var 엔유엠 uint16
	var 아이 uint
	for 아이 = 0; 아이 < 2; 아이++ {
		엔유엠 = 엔유엠 | (uint16(어레이[1-아이]) << (8 * 아이))
	}
	return 엔유엠
}
func A어레이티오유아이엔티32(어레이 [4]byte) uint32 {
	var 엔유엠 uint32
	var 아이 uint
	for 아이 = 0; 아이 < 4; 아이++ {
		엔유엠 = 엔유엠 | (uint32(어레이[3-아이]) << (8 * 아이))
	}
	return 엔유엠
}
func A어레이티오유아이엔티48(어레이 [6]byte) uint64 {
	var 엔유엠 uint64
	var 아이 uint
	for 아이 = 0; 아이 < 6; 아이++ {
		엔유엠 = 엔유엠 | (uint64(어레이[5-아이]) << (8 * 아이))
	}
	return 엔유엠

}
func A어레이티오유아이엔티48비이(어레이 [6]byte) uint64 {
	var 엔유엠 uint64
	var 아이 uint
	for 아이 = 0; 아이 < 6; 아이++ {
		엔유엠 = 엔유엠 | (uint64(어레이[아이]) << (8 * 아이))
	}
	return 엔유엠
}
func A어레이티오유아이엔티64(어레이 [8]byte) uint64 {
	var 엔유엠 uint64
	var 아이 uint
	for 아이 = 0; 아이 < 8; 아이++ {
		엔유엠 = 엔유엠 | (uint64(어레이[7-아이]) << (8 * 아이))
	}
	return 엔유엠
}
func U유아이엔티64알(엔유엠 uint64) uint64 {
	var 티이엠피 uint64
	var 아이 uint
	for 아이 = 0; 아이 < 8; 아이++ {
		티이엠피 = 티이엠피 | (uint64(엔유엠>>(8*(7-아이))&0x00000000000000FF) << (8 * 아이))
	}
	return 티이엠피
}
func U유아이엔티48알(엔유엠 uint64) uint64 {
	var 티이엠피 uint64
	var 아이 uint
	for 아이 = 0; 아이 < 6; 아이++ {
		티이엠피 = 티이엠피 | (uint64(엔유엠>>(8*(5-아이))&0x00000000000000FF) << (8 * 아이))
	}
	return 티이엠피
}
func U유아이엔티32알(엔유엠 uint32) uint32 {
	var 티이엠피 uint32
	var 아이 uint
	for 아이 = 0; 아이 < 4; 아이++ {
		티이엠피 = 티이엠피 | (uint32(엔유엠>>(8*(3-아이))&0x000000FF) << (8 * 아이))
	}
	return 티이엠피
}
func U유아이엔티16알(엔유엠 uint16) uint16 {
	var 티이엠피 uint16
	var 아이 uint
	for 아이 = 0; 아이 < 2; 아이++ {
		티이엠피 = 티이엠피 | (uint16(엔유엠>>(8*(1-아이))&0x000000FF) << (8 * 아이))
	}
	return 티이엠피
}
func P피알아이엔티비와이티이에스(데이터포인터 uintptr, 사이즈 int) {
	var 버퍼 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(데이터포인터))
	var 아이 int
	util콘솔.M출력([]byte("util["))
	for 아이 = 0; 아이 < 사이즈; 아이++ {
		util콘솔.MHex출력(버퍼[아이])
	}
	util콘솔.M출력([]byte("]"))
}

func P피알아이엔티티이에스티(피에이알에이엠에스 ...interface{}) {
	for _, 피에이알에이엠 := range 피에이알에이엠에스 {
		util콘솔.M출력([]byte(TypeOf(피에이알에이엠).Name()))

	}
}
func E이큐유에이엘비와이티이에스(에이, 비 []byte) bool {
	if len(에이) != len(비) {
		return false
	}
	for 아이, 브이 := range 에이 {
		if 브이 != 비[아이] {
			return false
		}
	}
	return true
}
func B비와이티이에스티오에스티알아이엔지(비 []byte) string {
	비에이치 := (*SliceHeader)(Pointer(&비))
	에스에이치 := StringHeader{비에이치.Data, 비에이치.Len}
	return *(*string)(Pointer(&에스에이치))
}
func G겟유아이엔티피티알어레이에프알오엠피티알(피티알 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var 에스엘 = struct {
		에이디디알	uintptr
		len	int
		cap	int
	}{피티알, len, cap}
	return *(*[]uintptr)(Pointer(&에스엘))
}
func G겟유아이엔티32어레이에프알오엠피티알(피티알 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var 에스엘 = struct {
		에이디디알	uintptr
		len	int
		cap	int
	}{피티알, len, cap}
	return *(*[]uint32)(Pointer(&에스엘))
}

func G겟비와이티이에스에프알오엠피티알(피티알 uintptr, len int, cap int) []byte {
	var 에스엘 = struct {
		에이디디알	uintptr
		len	int
		cap	int
	}{피티알, len, cap}
	return *(*[]byte)(Pointer(&에스엘))
}

func G겟에프유엔시피티알에프알오엠피티알(피티알 uintptr) func() {
	시오디이1피티알_시오디이1피티알 := uintptr(Pointer(&피티알))
	return *(*func())(Pointer(&시오디이1피티알_시오디이1피티알))
}
