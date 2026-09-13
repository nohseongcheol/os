package مشغل

type Iمشغل interface {
	Activate()
	Rأعدالضبط() int
	Deactivate()
}

type Tمشغلمدير struct {
}

var iمشغل [256]Iمشغل
var الأرقاممشغل int

func (نفسه *Tمشغلمدير) Init() {
	الأرقاممشغل = 0
}

func (نفسه *Tمشغلمدير) Aأضفمشغل(مشغل_2 Iمشغل) {
	iمشغل[الأرقاممشغل] = مشغل_2
	الأرقاممشغل++
}
func (نفسه *Tمشغلمدير) Activateالكل() {
	for i := 0; i < الأرقاممشغل; i++ {
		iمشغل[i].Activate()
	}
}
