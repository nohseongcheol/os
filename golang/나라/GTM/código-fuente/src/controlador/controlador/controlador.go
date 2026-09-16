/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package controlador

type IControlador interface {
	Activar()
	Reiniciar() int
	Desactivar()
}

type TControladorgestor struct {
}

var icontrolador [256]IControlador
var númerocontrolador int

func (propio *TControladorgestor) Init() {
	númerocontrolador = 0
}

func (propio *TControladorgestor) Añadircontrolador(controlador_2 IControlador) {
	icontrolador[númerocontrolador] = controlador_2
	númerocontrolador++
}
func (propio *TControladorgestor) ActivarTodo() {
	for i := 0; i < númerocontrolador; i++ {
		icontrolador[i].Activar()
	}
}
