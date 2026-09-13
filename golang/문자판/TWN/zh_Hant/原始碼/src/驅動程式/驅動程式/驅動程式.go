package 驅動程式

type I驅動程式 interface {
	A使用()
	R重設() int
	D停用()
}

type T驅動程式管理器 struct {
}

var i驅動程式 [256]I驅動程式
var 數字驅動程式 int

func (self *T驅動程式管理器) Init() {
	數字驅動程式 = 0
}

func (self *T驅動程式管理器) A加入驅動程式(驅動程式_2 I驅動程式) {
	i驅動程式[數字驅動程式] = 驅動程式_2
	數字驅動程式++
}
func (self *T驅動程式管理器) A使用全部() {
	for i := 0; i < 數字驅動程式; i++ {
		i驅動程式[i].A使用()
	}
}
