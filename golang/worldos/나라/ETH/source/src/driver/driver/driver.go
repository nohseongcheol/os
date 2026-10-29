/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aማስጀመሪያ()
	Rእንደነበረመመለሻ() int
	Dአታስጀምር()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var ቁጥርdriver int

func (self *TDrivermanager) Init() {
	ቁጥርdriver = 0
}

func (self *TDrivermanager) Aመጨመሪያdriver(driver_2 IDriver) {
	idriver[ቁጥርdriver] = driver_2
	ቁጥርdriver++
}
func (self *TDrivermanager) Aማስጀመሪያሁሉንም() {
	for i := 0; i < ቁጥርdriver; i++ {
		idriver[i].Aማስጀመሪያ()
	}
}
