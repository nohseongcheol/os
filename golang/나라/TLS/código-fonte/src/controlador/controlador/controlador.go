package controlador

type IControlador interface {
	Ativar()
	Repor() int
	Desativar()
}

type TControladorgestor struct {
}

var icontrolador [256]IControlador
var númerocontrolador int

func (próprio *TControladorgestor) Init() {
	númerocontrolador = 0
}

func (próprio *TControladorgestor) Adicionarcontrolador(controlador_2 IControlador) {
	icontrolador[númerocontrolador] = controlador_2
	númerocontrolador++
}
func (próprio *TControladorgestor) AtivarTudo() {
	for i := 0; i < númerocontrolador; i++ {
		icontrolador[i].Ativar()
	}
}
