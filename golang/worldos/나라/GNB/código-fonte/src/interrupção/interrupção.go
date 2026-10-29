/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupção

import . "unsafe"
import . "reflect"

import . "porto"
import . "gdt"
import . "múltiplogestãoTarefas"
import . "console"

func interrupçãoignore()

func interrupçãoexceptionhandler()
func interrupçãoexceptionhandler0x00()
func interrupçãoexceptionhandler0x01()
func interrupçãoexceptionhandler0x02()
func interrupçãoexceptionhandler0x03()
func interrupçãoexceptionhandler0x04()
func interrupçãoexceptionhandler0x05()
func interrupçãoexceptionhandler0x06()
func interrupçãoexceptionhandler0x07()
func interrupçãoexceptionhandler0x08()
func interrupçãoexceptionhandler0x09()
func interrupçãoexceptionhandler0x0a()
func interrupçãoexceptionhandler0x0b()
func interrupçãoexceptionhandler0x0c()
func interrupçãoexceptionhandler0x0d()
func interrupçãoexceptionhandler0x0e()
func interrupçãoexceptionhandler0x0f()
func interrupçãoexceptionhandler0x10()
func interrupçãoexceptionhandler0x11()
func interrupçãoexceptionhandler0x12()
func interrupçãoexceptionhandler0x13()

func interrupçãorequesthandler0x00()
func interrupçãorequesthandler0x01()
func interrupçãorequesthandler0x02()
func interrupçãorequesthandler0x03()
func interrupçãorequesthandler0x04()
func interrupçãorequesthandler0x05()
func interrupçãorequesthandler0x06()
func interrupçãorequesthandler0x07()
func interrupçãorequesthandler0x08()
func interrupçãorequesthandler0x09()
func interrupçãorequesthandler0x0a()
func interrupçãorequesthandler0x0b()
func interrupçãorequesthandler0x0c()
func interrupçãorequesthandler0x0d()
func interrupçãorequesthandler0x0e()
func interrupçãorequesthandler0x0f()

func interrupçãorequesthandler0x80()
func interrupçãorequesthandler0x81()
func interrupçãorequesthandler0x82()

func TestarImprimir(posição uint8, dados uint8)
func conjuntods(dssegment uint32)
func conjuntogs(gssegment uint32)
func interrupçãoSairloop()

type TInterrupçãohandler struct {
	InterrupçãoNúmero	uint8
	Interrupçãogestor	uintptr
}
type IInterrupçãohandler interface {
	Manípulointerrupção(uint32) uint32
}

func Novointerrupçãohandler(Interrupçãogestor uintptr, InterrupçãoNúmero uint8) *TInterrupçãohandler {
	interrupçãohandler_2 := new(TInterrupçãohandler)
	interrupçãohandler_2.InterrupçãoNúmero = InterrupçãoNúmero
	interrupçãohandler_2.Interrupçãogestor = Interrupçãogestor
	return interrupçãohandler_2

}

var handler_2 [256]uintptr

func (próprio *TInterrupçãohandler) Init(InterrupçãoNúmero uint8, Interrupçãogestor uintptr, funcEndereço uintptr) {

	handler_2[InterrupçãoNúmero] = funcEndereço

	próprio.InterrupçãoNúmero = InterrupçãoNúmero
	próprio.Interrupçãogestor = Interrupçãogestor

}
func (próprio *TInterrupçãohandler) ConjuntoManípulointerrupçãofuction(InterrupçãoNúmero uint32, endereço uintptr) {
	handler_2[InterrupçãoNúmero] = endereço
}
func (próprio *TInterrupçãohandler) Destruir() {
	própriouintptr := uintptr(Pointer(próprio))
	Interrupçãogestor := (*TInterrupçãogestor)(Pointer(próprio.Interrupçãogestor))
	if própriouintptr == Interrupçãogestor.Gethandler(próprio.InterrupçãoNúmero) {
		Interrupçãogestor.Conjuntohandler(0, próprio.InterrupçãoNúmero)
	}

}
func (próprio *TInterrupçãohandler) Conjuntointerrupçãogestor(Interrupçãogestor uintptr) {
}
func (próprio *TInterrupçãohandler) ConjuntointerrupçãoNúmero(InterrupçãoNúmero uint8) {
	próprio.InterrupçãoNúmero = InterrupçãoNúmero
}
func (próprio *TInterrupçãohandler) Manípulointerrupção(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MImprimir(buffer)
	return esp
}
func Manípulointerrupção1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MImprimir(buffer)
}

type TPortadescriptor struct {
	portadados [8]uint8
}
type TInterrupçãodescriptorTabelaPonteiro struct {
}

var idtdados [256 * 8]uint8
var Ativointerrupçãogestor uintptr = 0

const interrupçãoDepurar = false

type TInterrupçãogestor struct {
	handler_2	[256]uintptr

	equipamentointerrupçãoDeslocamento	uint16

	tarefagestor	*TTarefagestor
}

var PrimarypicComandoESporto uint16 = 0x20
var PrimarypicdadosESporto uint16 = 0x21
var SecondarypicComandoESporto uint16 = 0xA0
var SecondarypicdadosESporto uint16 = 0xA1

func (próprio *TInterrupçãogestor) Init(equipamentointerrupçãoDeslocamento uint16, globaldescriptorTabela *TShareddescriptorTabela, tarefagestor *TTarefagestor) {

	próprio.tarefagestor = tarefagestor

	próprio.equipamentointerrupçãoDeslocamento = equipamentointerrupçãoDeslocamento
	codesegment := uint16(Segnúcleocode)

	for i := 0; i < (256 * 8); i++ {
		idtdados[i] = 0
	}
	var endereço uint32
	var Idtinterrupçãoporta uint8 = 0xE
	endereço = uint32(ValueOf(interrupçãoignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0f).Pointer())
		próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(i, codesegment, endereço, 0, Idtinterrupçãoporta)
	}

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x00).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x00, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x01).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x01, codesegment, endereço, 0, Idtinterrupçãoporta)
	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x02).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x02, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x03).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x03, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x04).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x04, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x05).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x05, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x06).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x06, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x07).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x07, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x08).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x08, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x09).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x09, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0a).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x0A, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0b).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x0B, codesegment, endereço, 0, Idtinterrupçãoporta)
	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0c).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x0C, codesegment, endereço, 0, Idtinterrupçãoporta)
	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0d).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x0D, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0e).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x0E, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x0f).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x0F, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x10).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x10, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x11).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x11, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x12).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x12, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãoexceptionhandler0x13).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x13, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x00).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x20, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x01).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x21, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x02).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x22, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x03).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x23, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x04).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x24, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x05).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x25, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x06).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x26, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x07).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x27, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x08).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x28, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x09).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x29, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x0a).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x2A, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x0b).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x2B, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x0c).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x2C, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x0d).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x2D, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x0e).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x2E, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x0f).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x2F, codesegment, endereço, 0, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x80).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x80, codesegment, endereço, 3, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x81).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x81, codesegment, endereço, 3, Idtinterrupçãoporta)

	endereço = uint32(ValueOf(interrupçãorequesthandler0x82).Pointer())
	próprio.InterrupçãodescriptorTabelapontodeentradaconjunto(0x82, codesegment, endereço, 3, Idtinterrupçãoporta)

	Portoescreverocteto(PrimarypicComandoESporto, 0x11)
	Portoescreverocteto(SecondarypicComandoESporto, 0x11)

	Portoescreverocteto(PrimarypicdadosESporto, 0x20)
	Portoescreverocteto(SecondarypicdadosESporto, 0x28)

	Portoescreverocteto(PrimarypicdadosESporto, 0x04)
	Portoescreverocteto(SecondarypicdadosESporto, 0x02)

	Portoescreverocteto(PrimarypicdadosESporto, 0x01)
	Portoescreverocteto(SecondarypicdadosESporto, 0x01)

	Portoescreverocteto(PrimarypicdadosESporto, 0xF8)
	Portoescreverocteto(SecondarypicdadosESporto, 0xEF)

	idtPonteiro := [6]uint8{0, 0, 0, 0, 0, 0}
	tamanho := (*uint16)(Pointer(&idtPonteiro[0]))
	(*tamanho) = (uint16)(Sizeof(idtdados) - 1)

	base := (*uint32)(Pointer(&idtPonteiro[2]))
	(*base) = uint32(uintptr(Pointer(&idtdados)))

	Lidt(uintptr(Pointer(&idtPonteiro)))
}
func Lidt(lidtaddr uintptr)

func (próprio *TInterrupçãogestor) InterrupçãodescriptorTabelapontodeentradaconjunto(interrupção int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptortipo uint8) {

	handlerEndereçoBaixobits := (*uint16)(Pointer(&idtdados[interrupção*8+0]))
	(*handlerEndereçoBaixobits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdados[interrupção*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reservado := (*uint8)(Pointer(&idtdados[interrupção*8+4]))
	(*reservado) = 0

	var IdtdescriptorPresente uint8 = 0x80
	acesso := (*uint8)(Pointer(&idtdados[interrupção*8+5]))
	(*acesso) = (IdtdescriptorPresente | Descriptortipo | ((Descriptorprivilegelevel & 3) << 5))

	handlerEndereçoAltobits := (*uint16)(Pointer(&idtdados[interrupção*8+6]))
	(*handlerEndereçoAltobits) = uint16((handler >> 16) & 0xFFFF)

}

func (próprio *TInterrupçãogestor) Conjuntohandler(handler uintptr, InterrupçãoNúmero uint8) {
	handler_2[InterrupçãoNúmero] = handler
}
func (próprio *TInterrupçãogestor) Gethandler(InterrupçãoNúmero uint8) uintptr {
	return handler_2[InterrupçãoNúmero]
}
func (próprio *TInterrupçãogestor) DoManípulointerrupção(interrupção uint8, esp uint32) uint32 {

	if interrupçãoDepurar {
		console_2.MImprimirxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Imprimir(uint32(interrupção))
		console_2.MImprimir(":")
		console_2.MUnsignedinteger32Imprimir(esp)
	}
	handlerExecutar := false
	if handler_2[interrupção] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupção])))
		esp = myfunction(esp)
		handlerExecutar = true

	}

	if !handlerExecutar && interrupção == uint8(próprio.equipamentointerrupçãoDeslocamento) && próprio.tarefagestor != nil {
		esp = uint32(uintptr(Pointer(próprio.tarefagestor.Schedule((*TcpuEstado)(Pointer(uintptr(esp)))))))

	}
	if !handlerExecutar && interrupção == 0x80 {
		esp = manípulounhandledsyscall(esp)
	}

	if interrupção <= 0x1F {
	}
	if 0x20 <= interrupção && interrupção < 0x30 {
		if 0x28 <= interrupção {
			Portoescreverocteto(SecondarypicComandoESporto, 0x20)
		}
		Portoescreverocteto(PrimarypicComandoESporto, 0x20)
	}
	return esp
}

var contar2 uint8 = 1

func conjuntocr3(endereço uint32)

var console_2 TConsole = TConsole{}

func Manípulointerrupção(esp uint32, interrupção uint32) uint32 {

	if interrupçãoDepurar && interrupção != 0x80 && interrupção != 0x20 {
		console_2.MImprimirxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Imprimir(uint32(interrupção))
		console_2.MImprimir(":")
		console_2.MUnsignedinteger32Imprimir(esp)
	}

	if Ativointerrupçãogestor != 0 {
		p := (*TInterrupçãogestor)(Pointer(Ativointerrupçãogestor))
		esp = p.DoManípulointerrupção(uint8(interrupção), esp)
		return esp
	}
	if handler_2[interrupção] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupção])))
		esp = myfunction(esp)
	}
	if interrupção == 0x80 {
		return manípulounhandledsyscall(esp)
	}
	if 0x20 <= interrupção && interrupção < 0x30 {
		if 0x28 <= interrupção {
			Portoescreverocteto(SecondarypicComandoESporto, 0x20)
		}
		Portoescreverocteto(PrimarypicComandoESporto, 0x20)
	}

	return esp
}

func manípulounhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuEstado)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interrupçãoSairloop).Pointer())
		cpu.Cs = Segnúcleocode
		cpu.Ds = Segnúcleodados
		cpu.Es = Segnúcleodados
		cpu.Fs = Segnúcleodados
		cpu.Gs = Segnúcleogs
		cpu.Ss = Segnúcleodados
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasErrocode(interrupção uint32) bool {
	switch interrupção {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNome(interrupção uint32) string {
	switch interrupção {
	case 0x00:
		return "#DE divide error"
	case 0x06:
		return "#UD invalid opcode"
	case 0x08:
		return "#DF double fault"
	case 0x0A:
		return "#TS invalid TSS"
	case 0x0B:
		return "#NP segment not present"
	case 0x0C:
		return "#SS stack fault"
	case 0x0D:
		return "#GP general protection"
	case 0x0E:
		return "#PF page fault"
	case 0x11:
		return "#AC alignment check"
	}
	return "#EX exception"
}

func exceptionquadroValor(quadro uint32, deslocamento uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(quadro + deslocamento)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func imprimirpáginafalhaInformações(erro uint32) {
	MEmergencyRegistolinha(" pf=[")
	if (erro & 0x01) != 0 {
		MEmergencyRegistolinha("protection")
	} else {
		MEmergencyRegistolinha("not-present")
	}
	if (erro & 0x02) != 0 {
		MEmergencyRegistolinha(",write")
	} else {
		MEmergencyRegistolinha(",read")
	}
	if (erro & 0x04) != 0 {
		MEmergencyRegistolinha(",user")
	} else {
		MEmergencyRegistolinha(",kernel")
	}
	if (erro & 0x08) != 0 {
		MEmergencyRegistolinha(",reserved-bit")
	}
	if (erro & 0x10) != 0 {
		MEmergencyRegistolinha(",instruction-fetch")
	}
	MEmergencyRegistolinha("]")
}

func imprimirexceptionselectorInformações(erro uint32) {
	MEmergencyRegistolinha(" selector=")
	MEmergencyRegistounsignedinteger32(erro & 0xFFFFFFF8)
	MEmergencyRegistolinha(" index=")
	MEmergencyRegistounsignedinteger32(erro >> 3)
	MEmergencyRegistolinha(" table=")
	if (erro & 0x02) != 0 {
		MEmergencyRegistolinha("IDT")
	} else if (erro & 0x04) != 0 {
		MEmergencyRegistolinha("LDT")
	} else {
		MEmergencyRegistolinha("GDT")
	}
	MEmergencyRegistolinha(" ext=")
	MEmergencyRegistounsignedinteger32(erro & 0x01)
}

func Manípuloexception(esp uint32, interrupção uint32) uint32 {
	MEmergencyRegistolinha("\nEXCEPTION vec=")
	MEmergencyRegistohexadecimal8(uint8(interrupção))
	MEmergencyRegistolinha(" ")
	MEmergencyRegistolinha(exceptionNome(interrupção))
	MEmergencyRegistolinha(" frame=")
	MEmergencyRegistounsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyRegistolinha(" invalid-frame")
		if exceptionhasErrocode(interrupção) {
			MEmergencyRegistolinha(" raw-error-or-bad-esp=")
			MEmergencyRegistounsignedinteger32(esp)
			imprimirexceptionselectorInformações(esp)
		}
		MEmergencyRegistolinha("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var erro uint32 = 0
	var eipDeslocamento uint32 = 0
	if exceptionhasErrocode(interrupção) {
		erro = exceptionquadroValor(esp, 0)
		eipDeslocamento = 4
	}
	eip := exceptionquadroValor(esp, eipDeslocamento)
	cs := exceptionquadroValor(esp, eipDeslocamento+4)
	eflags := exceptionquadroValor(esp, eipDeslocamento+8)

	MEmergencyRegistolinha(" err=")
	MEmergencyRegistounsignedinteger32(erro)
	MEmergencyRegistolinha(" eip=")
	MEmergencyRegistounsignedinteger32(eip)
	MEmergencyRegistolinha(" cs=")
	MEmergencyRegistounsignedinteger32(cs)
	MEmergencyRegistolinha(" eflags=")
	MEmergencyRegistounsignedinteger32(eflags)
	MEmergencyRegistolinha(" cr0=")
	MEmergencyRegistounsignedinteger32(exceptioncr0())
	MEmergencyRegistolinha(" cr3=")
	MEmergencyRegistounsignedinteger32(exceptioncr3())

	if interrupção == 0x0E {
		MEmergencyRegistolinha(" cr2=")
		MEmergencyRegistounsignedinteger32(exceptioncr2())
		imprimirpáginafalhaInformações(erro)
	}

	if (cs & 0x03) != 0 {
		MEmergencyRegistolinha(" useresp=")
		MEmergencyRegistounsignedinteger32(exceptionquadroValor(esp, eipDeslocamento+12))
		MEmergencyRegistolinha(" ss=")
		MEmergencyRegistounsignedinteger32(exceptionquadroValor(esp, eipDeslocamento+16))
	}

	if exceptionhasErrocode(interrupção) {
		imprimirexceptionselectorInformações(erro)
	}
	MEmergencyRegistolinha("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltDepoisfatalexception()

func Manípulofatalinterrupçãoquadro(guardadoesp uint32, interrupção uint32) uint32 {
	Manípuloexception(guardadoesp+52, interrupção)
	haltDepoisfatalexception()
	return guardadoesp
}

func InterrupçãoAtivo()
func (próprio *TInterrupçãogestor) Ativo() {
	if Ativointerrupçãogestor != 0 {
		próprio.Deactive()
	}
	endereço := uintptr(Pointer(próprio))
	Ativointerrupçãogestor = endereço
	InterrupçãoAtivo()
}
func Interrupçãodeactive()
func (próprio *TInterrupçãogestor) Deactive() {
	Ativointerrupçãogestor = 0
	Interrupçãodeactive()
}

func MyManípulointerrupção(interrupção uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MImprimir(buffer)
	return esp
}
func MyTestar(interrupção uint8, esp uint32)

func Unhandleinterrupção() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MImprimir(buffer)
}

func interrupçãohandler_2(interrupção uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MImprimir(buffer)
	console_2.MHexadecimalImprimir(0x40)
	return esp
}
func imprimiresp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Imprimirxy(esp, 20, 21)
}
func gettls() uint32
func Imprimirtls() {

}
