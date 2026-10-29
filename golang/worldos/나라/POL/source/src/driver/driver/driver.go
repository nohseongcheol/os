/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Włącz()
	Wyzeruj() int
	Wyłącz()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var liczbadriver int

func (bieżący *TDrivermanager) Init() {
	liczbadriver = 0
}

func (bieżący *TDrivermanager) Dodajdriver(driver_2 IDriver) {
	idriver[liczbadriver] = driver_2
	liczbadriver++
}
func (bieżący *TDrivermanager) WłączWszystkie() {
	for i := 0; i < liczbadriver; i++ {
		idriver[i].Włącz()
	}
}
