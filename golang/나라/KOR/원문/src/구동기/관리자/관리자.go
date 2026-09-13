package 관리자_2

type I구동기 interface {
	M활성화()
	M재설정() int
	M비활성화()
}

type T구동기관리자 struct {
}

var i구동기 [256]I구동기
var 번호구동기 int

func (자신 *T구동기관리자) F관문초기화() {
	번호구동기 = 0
}

func (자신 *T구동기관리자) M구동기추가(구동기_2 I구동기) {
	i구동기[번호구동기] = 구동기_2
	번호구동기++
}
func (자신 *T구동기관리자) M모두활성화() {
	for i := 0; i < 번호구동기; i++ {
		i구동기[i].M활성화()
	}
}
