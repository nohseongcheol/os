/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Otakäyttöön()
	Palauta() int
	Poistakäytöstä()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numerodriver int

func (itse *TDrivermanager) Init() {
	numerodriver = 0
}

func (itse *TDrivermanager) Lisäädriver(driver_2 IDriver) {
	idriver[numerodriver] = driver_2
	numerodriver++
}
func (itse *TDrivermanager) OtakäyttöönKaikki() {
	for i := 0; i < numerodriver; i++ {
		idriver[i].Otakäyttöön()
	}
}
