package 공통

type T기억공간연산 struct {
}

func (자신 *T기억공간연산) M기억공간채우기(임시공간주소참조 uintptr, 값 byte, 크기 uint32) uintptr {
	return 임시공간주소참조
}
func (자신 *T기억공간연산) M기억공간이동(목적지주소참조_2 uintptr, 출발지주소_2 uintptr, 크기 uint32) uintptr {
	return 목적지주소참조_2
}

func (자신 *T기억공간연산) M기억공간복사(목적지주소참조_2 uintptr, 출발지주소_2 uintptr, 크기 uint32) uintptr {
	return 목적지주소참조_2
}
func (자신 *T기억공간연산) M기억공간비교(목적지주소참조_2 uintptr, 출발지주소_2 uintptr, 크기 uint32) bool {
	return true
}
