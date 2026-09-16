/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package processo

import . "unsafe"
import . "utilitário/lista"
import mem "memóriagestor"
import . "gestãoTarefas/fluxoExecução"
import . "gestãoTarefas/escalonador"
import . "utilitário"

const ProcutilizadorheapTamanho = 1 * 1024 * 1024

type Processo struct {
	id			uint32
	syscallid		int
	IsutilizadorEspaço	bool
	argumentos		*[]byte

	FluxoExecuçãolista	Linkedlista
	Threads			*Linkedlista
	FicheiroNome		[]byte

	Páginadiretóriopontodeentrada	uintptr
}

func (próprio *Processo) Init(mem *mem.TMemóriagestor) {
	próprio.FluxoExecuçãolista = Linkedlista{}
	próprio.Threads = &próprio.FluxoExecuçãolista
	próprio.Threads.Init(mem)
}

type Processohelper struct {
	processos				Linkedlista
	mem					*mem.TMemóriagestor
	núcleopáginadiretóriopontodeentrada	uintptr
}

func (próprio *Processohelper) Init(mem *mem.TMemóriagestor, núcleopáginadiretóriopontodeentrada uintptr) {
	próprio.mem = mem
	próprio.processos = Linkedlista{}
	próprio.processos.Init(próprio.mem)
	próprio.núcleopáginadiretóriopontodeentrada = núcleopáginadiretóriopontodeentrada
}

func (próprio *Processohelper) Criar(pontodeentradapoint func(), fluxoExecuçãohelper *TFluxoExecuçãohelper, Páginadiretóriopontodeentrada uint32, isnúcleo bool) Processo {
	processo := (*Processo)(próprio.mem.Alocar_memória(uint32(Sizeof(Processo{}))))
	if processo == nil {
		return Processo{}
	}
	processo.Init(próprio.mem)
	processo.id = Allocatepid()
	processo.Páginadiretóriopontodeentrada = uintptr(Páginadiretóriopontodeentrada)
	principalfluxoExecução := fluxoExecuçãohelper.CriarPonteirodeFunção(pontodeentradapoint, Páginadiretóriopontodeentrada, isnúcleo)
	if principalfluxoExecução != nil {
		principalfluxoExecução.Pid = processo.id
		principalfluxoExecução.Superiorpid = 0
		processo.Threads.Adicionar_ao_fim_da_lista(uintptr(Pointer(principalfluxoExecução)))
	}

	próprio.processos.Adicionar_ao_fim_da_lista(uintptr(Pointer(processo)))

	return *processo
}

func (próprio *Processohelper) Spawn(pontodeentradapoint func(), fluxoExecuçãohelper *TFluxoExecuçãohelper, escalonador *Escalonador, Páginadiretóriopontodeentrada uint32, isnúcleo bool) Processo {
	processo := próprio.Criar(pontodeentradapoint, fluxoExecuçãohelper, Páginadiretóriopontodeentrada, isnúcleo)
	if processo.Threads != nil && processo.Threads.Tamanho_2 > 0 {
		fluxoExecução := (*TFluxoExecução)(processo.Threads.Getat(0))
		if fluxoExecução != nil && escalonador != nil {
			escalonador.AdicionarfluxoExecução(fluxoExecução)
		}
	}
	return processo
}

func (próprio *Processohelper) copiarpáginadiretório(origempontodeentrada uintptr, destinopontodeentrada uintptr) {
	origem_2 := Getunsignedinteger32matrizdePonteiro(origempontodeentrada, 1024, 1024)
	destino_2 := Getunsignedinteger32matrizdePonteiro(destinopontodeentrada, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destino_2[i] = origem_2[i]
	}
}
func (próprio *Processohelper) Criardedados() Processo {
	processo := Processo{}
	return processo
}
