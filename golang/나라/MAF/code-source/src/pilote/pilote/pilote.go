package pilote

type IPilote interface {
	Activer()
	Réinitialiser() int
	Désactiver()
}

type TPilotegestionnaire struct {
}

var ipilote [256]IPilote
var nombrepilote int

func (self *TPilotegestionnaire) Init() {
	nombrepilote = 0
}

func (self *TPilotegestionnaire) Ajouterpilote(pilote_2 IPilote) {
	ipilote[nombrepilote] = pilote_2
	nombrepilote++
}
func (self *TPilotegestionnaire) ActiverTout() {
	for i := 0; i < nombrepilote; i++ {
		ipilote[i].Activer()
	}
}
