package escalonador

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "porto"
import . "utilitário/lista"

import . "interrupção"
import . "gestãoTarefas/fluxoExecução"
import . "gestãoTarefas/tss"
import . "múltiplogestãoTarefas"
import mem "memóriagestor"

const EscalonadorFrequência = 1
const NúcleoheapIniciar = 1024 * 1024
const escalonadorDepurar = false
const pitFrequência = 100

var lista Linkedlista

type Escalonadordados struct {
	frequência	uint32
	tickContar	uint32

	switchforced	bool

	Ativado	bool

	atualfluxoExecução	*TFluxoExecução
	tss			*Tsspontodeentrada
}

var schedados Escalonadordados = Escalonadordados{}

func (próprio *Escalonadordados) Init() {
	schedados.tickContar = 0
	schedados.frequência = EscalonadorFrequência
	schedados.atualfluxoExecução = nil
	schedados.Ativado = false
	schedados.switchforced = false

}

var console_2 = TConsole{}
var atualfluxoExecuçãoÍndice int = 0
var seguinteprocessoid uint32 = 1

func Allocatepid() uint32 {
	pid := seguinteprocessoid
	seguinteprocessoid++
	return pid
}

func (próprio *Escalonadordados) GetSeguinteProntofluxoExecução() *TFluxoExecução {
	if lista.Tamanho_2 <= 0 {
		return nil
	}

	if schedados.atualfluxoExecução != nil {
		atualfluxoExecuçãoÍndice = lista.Índicede(uintptr(Pointer(schedados.atualfluxoExecução)))
		if atualfluxoExecuçãoÍndice < 0 {
			atualfluxoExecuçãoÍndice = 0
		}
	} else {
		atualfluxoExecuçãoÍndice = -1
	}

	for checked := 0; checked < lista.Tamanho_2; checked++ {
		atualfluxoExecuçãoÍndice++
		if atualfluxoExecuçãoÍndice >= lista.Tamanho_2 {
			atualfluxoExecuçãoÍndice = 0
		}
		fluxoExecução := (*TFluxoExecução)(lista.Getat(atualfluxoExecuçãoÍndice))
		if fluxoExecução != nil && fluxoExecução.FluxoExecuçãoEstado != Blocked && fluxoExecução.FluxoExecuçãoEstado != Parado {
			if escalonadorDepurar {
				console_2.MImprimir("ti:")
				console_2.MUnsignedinteger32Imprimir(uint32(atualfluxoExecuçãoÍndice))
				console_2.MImprimir(":")
				console_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(fluxoExecução))))
			}
			return fluxoExecução
		}
	}
	return schedados.atualfluxoExecução

}
func (próprio *Escalonador) AdicionarfluxoExecução(fluxoExecução *TFluxoExecução) {
	if fluxoExecução == nil {
		return
	}
	lista.Adicionar_ao_fim_da_lista(uintptr(Pointer(fluxoExecução)))
}
func AdicionarrunnablefluxoExecução(fluxoExecução *TFluxoExecução) {
	if fluxoExecução == nil {
		return
	}
	lista.Adicionar_ao_fim_da_lista(uintptr(Pointer(fluxoExecução)))
}

func Atualpid() uint32 {
	if schedados.atualfluxoExecução == nil || schedados.atualfluxoExecução.Pid == 0 {
		return 1
	}
	return schedados.atualfluxoExecução.Pid
}

func Atualsuperiorpid() uint32 {
	if schedados.atualfluxoExecução == nil {
		return 0
	}
	return schedados.atualfluxoExecução.Superiorpid
}
func (próprio *Escalonador) RemoverfluxoExecução(fluxoExecução *TFluxoExecução) {
	lista.Remover(uintptr(Pointer(fluxoExecução)))
}

func (próprio *Escalonador) RemoverfluxoExecuçãoat(índice int) {
	lista.Removerat(índice)
}

type Escalonador struct {
	TInterrupçãohandler
}

func (próprio *Escalonador) Init(gestor *TInterrupçãogestor, mem *mem.TMemóriagestor, tss *Tsspontodeentrada) {
	schedados.Init()
	schedados.tss = tss
	initpit(pitFrequência)

	lista = Linkedlista{}
	lista.Init(mem)
	console_2.MImprimir("list:")
	console_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(&lista))))

	interrupçãohandler = manípulointerrupção
	var endereço uintptr
	endereço = uintptr(Pointer(&interrupçãohandler))
	próprio.TInterrupçãohandler.Init(0x20, uintptr(Pointer(gestor)), endereço)
}

func (próprio *Escalonador) Ativado(ativado bool) {
	schedados.Ativado = ativado
}

func initpit(frequência uint32) {
	if frequência == 0 {
		return
	}
	divisor := uint32(1193180) / frequência
	Portoescreverocteto(0x43, 0x36)
	Portoescreverocteto(0x40, uint8(divisor&0xFF))
	Portoescreverocteto(0x40, uint8((divisor>>8)&0xFF))
}

func conjuntods(dssegment uint32)
func conjuntogs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restaurarfpregs(buffer_2 uintptr)

var jmputilizador uint32 = 0
var interrupçãohandler func(uint32) uint32

func schedulestack(fn func())
func conjuntocr3(endereço uint32)
func getcr3() uint32

func manípulointerrupção(esp uint32) uint32 {

	schedados.tickContar++

	if escalonadorDepurar {
		console_2.MImprimirxy(([]byte)("sche1:"), 1, 17)

		console_2.MImprimir(":")
		console_2.MUnsignedinteger32Imprimir(esp)
		console_2.MImprimir(":")

		console_2.MUnsignedinteger32Imprimir(uint32(schedados.tickContar))
		console_2.MImprimir(":")
		console_2.MUnsignedinteger32Imprimir(NúcleoheapIniciar)
	}

	if schedados.tickContar == schedados.frequência {
		schedados.tickContar = 0

		if lista.Tamanho_2 > 0 && schedados.Ativado == true {
			var seguintefluxoExecução = schedados.GetSeguinteProntofluxoExecução()
			if seguintefluxoExecução == nil {
				return esp
			}
			if schedados.atualfluxoExecução == nil {
				MEmergencyRegistolinha("\nSCHED first esp=")
				MEmergencyRegistounsignedinteger32(esp)
				MEmergencyRegistolinha(" thread=")
				MEmergencyRegistounsignedinteger32(uint32(uintptr(Pointer(seguintefluxoExecução))))
				MEmergencyRegistolinha(" cpu=")
				MEmergencyRegistounsignedinteger32(uint32(uintptr(Pointer(seguintefluxoExecução.CpuEstado))))
				MEmergencyRegistolinha(" state=")
				MEmergencyRegistounsignedinteger32(uint32(seguintefluxoExecução.FluxoExecuçãoEstado))
				MEmergencyRegistolinha(" eip=")
				MEmergencyRegistounsignedinteger32(seguintefluxoExecução.CpuEstado.Eip)
				MEmergencyRegistolinha(" cs=")
				MEmergencyRegistounsignedinteger32(seguintefluxoExecução.CpuEstado.Cs)
				MEmergencyRegistolinha("\n")
			}

			if esp >= NúcleoheapIniciar && schedados.atualfluxoExecução != nil {
				schedados.atualfluxoExecução.CpuEstado = (*TcpuEstado)(Pointer(uintptr(esp)))

				endereço := uintptr(Pointer(&(schedados.atualfluxoExecução.Fpubuffer)))
				deslocamento := (16 - (endereço % 16)) & 0xF
				schedados.atualfluxoExecução.FpuDeslocamento = deslocamento
				backupfpregs(endereço + deslocamento)
				if escalonadorDepurar {
					console_2.MImprimir(([]byte)("backup"))
					console_2.MUnsignedinteger32Imprimir(esp)
				}
			}

			endereço := uintptr(Pointer(&(seguintefluxoExecução.Fpubuffer)))
			deslocamento := seguintefluxoExecução.FpuDeslocamento
			if deslocamento != 0xffffffff {
				restaurarfpregs(endereço + deslocamento)
				if escalonadorDepurar {
					console_2.MImprimir(([]byte)("restore"))
				}
			}

			schedados.atualfluxoExecução = seguintefluxoExecução

			if schedados.atualfluxoExecução.FluxoExecuçãoEstado == Iniciado {
				schedados.atualfluxoExecução.FluxoExecuçãoEstado = Pronto

				InitialfluxoExecuçãoutilizadorjump(schedados.atualfluxoExecução)
				return esp
			}

			esp = uint32(uintptr(Pointer(seguintefluxoExecução.CpuEstado)))
			if seguintefluxoExecução.Stack != 0 {
				schedados.tss.Conjuntostack(Segnúcleodados, seguintefluxoExecução.Stack+FluxoExecuçãostackTamanho)
			}

			conjuntocr3(seguintefluxoExecução.Páginadiretóriopontodeentrada)
			conjuntogs(seguintefluxoExecução.CpuEstado.Gs)

		}

	}

	return esp
}

func jumpMododeutilizadoriret(uint32, uint32, uint32, uint32, uint32, uint32)
func Desativarint()

func getesp() uint32
func fluxoExecuçãoSairloop()

func conjuntofluxoExecuçãoSairloopEstado(cpuEstado *TcpuEstado) {
	cpuEstado.Eip = uint32(ValueOf(fluxoExecuçãoSairloop).Pointer())
	cpuEstado.Cs = Segnúcleocode
	cpuEstado.Ds = Segnúcleodados
	cpuEstado.Es = Segnúcleodados
	cpuEstado.Fs = Segnúcleodados
	cpuEstado.Gs = Segnúcleogs
	cpuEstado.Ss = Segnúcleodados
	cpuEstado.Eflags = 0x202
}

func PararAtualfluxoExecução(cpuEstado *TcpuEstado) *TcpuEstado {
	if schedados.atualfluxoExecução == nil {
		conjuntofluxoExecuçãoSairloopEstado(cpuEstado)
		return cpuEstado
	}

	paradofluxoExecução := schedados.atualfluxoExecução
	for i := 0; i < lista.Tamanho_2; i++ {
		fluxoExecução := (*TFluxoExecução)(lista.Getat(i))
		if fluxoExecução != nil && fluxoExecução.CpuEstado == cpuEstado {
			paradofluxoExecução = fluxoExecução
			break
		}
	}
	paradofluxoExecução.CpuEstado = cpuEstado
	paradofluxoExecução.FluxoExecuçãoEstado = Parado
	schedados.atualfluxoExecução = paradofluxoExecução

	seguintefluxoExecução := schedados.GetSeguinteProntofluxoExecução()
	if seguintefluxoExecução == nil || seguintefluxoExecução == paradofluxoExecução || seguintefluxoExecução.CpuEstado == nil || seguintefluxoExecução.CpuEstado == cpuEstado {
		conjuntofluxoExecuçãoSairloopEstado(cpuEstado)
		return cpuEstado
	}

	schedados.atualfluxoExecução = seguintefluxoExecução
	if seguintefluxoExecução.Stack != 0 && schedados.tss != nil {
		schedados.tss.Conjuntostack(Segnúcleodados, seguintefluxoExecução.Stack+FluxoExecuçãostackTamanho)
	}
	conjuntocr3(seguintefluxoExecução.Páginadiretóriopontodeentrada)
	conjuntogs(seguintefluxoExecução.CpuEstado.Gs)
	return seguintefluxoExecução.CpuEstado
}

func InitialfluxoExecuçãoutilizadorjump(fluxoExecução *TFluxoExecução) {

	Desativarint()

	schedados.tss.Conjuntostack(Segnúcleodados, fluxoExecução.Stack+FluxoExecuçãostackTamanho)

	conjuntocr3(fluxoExecução.Páginadiretóriopontodeentrada)
	conjuntogs(fluxoExecução.CpuEstado.Gs)

	schedados.atualfluxoExecução = fluxoExecução
	schedados.Ativado = true

	eip := fluxoExecução.CpuEstado.Eip
	utilizadoresp := fluxoExecução.Utilizadorstack_2 + fluxoExecução.UtilizadorstackTamanho_2
	eflags := fluxoExecução.CpuEstado.Eflags
	cs := fluxoExecução.CpuEstado.Cs
	esp := schedados.tss.Getesp0()

	console_2.MImprimir(([]byte)("jump["))
	console_2.MUnsignedinteger32Imprimir(eip)
	console_2.MImprimir(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimir(utilizadoresp)
	console_2.MImprimir(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimir(eflags)
	console_2.MImprimir(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimir(cs)
	console_2.MImprimir(([]byte)(":"))

	console_2.MUnsignedinteger32Imprimir(esp)
	console_2.MImprimir(([]byte)("]"))

	userprocpontodeentrada := fluxoExecução.CpuEstado.Ecx
	globalDeslocamentoTabela_2 := fluxoExecução.CpuEstado.Edx
	dinâmico := fluxoExecução.CpuEstado.Esi

	Portoescreverocteto(0x20, 0x20)
	jumpMododeutilizadoriret(eip, utilizadoresp, eflags, userprocpontodeentrada, globalDeslocamentoTabela_2, dinâmico)
	console_2.MImprimir(([]byte)("usermode end"))
}
func imprimiresp(esp uint32) {
	console_2.MImprimir(([]byte)("esp["))
	console_2.MUnsignedinteger32Imprimir(esp)
}
