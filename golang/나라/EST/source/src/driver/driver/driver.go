/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Lülitasisse()
	Lähtesta() int
	Lülitavälja()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var arvdriver int

func (ise *TDrivermanager) Init() {
	arvdriver = 0
}

func (ise *TDrivermanager) Lisadriver(driver_2 IDriver) {
	idriver[arvdriver] = driver_2
	arvdriver++
}
func (ise *TDrivermanager) LülitasisseKõik() {
	for i := 0; i < arvdriver; i++ {
		idriver[i].Lülitasisse()
	}
}
