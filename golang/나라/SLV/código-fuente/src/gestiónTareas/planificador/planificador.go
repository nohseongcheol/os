package planificador

import . "unsafe"
import . "reflect"

import . "consola"
import . "gdt"
import . "puerto"
import . "utilidad/lista"

import . "interrupción"
import . "gestiónTareas/hilo"
import . "gestiónTareas/tss"
import . "múltiplegestiónTareas"
import mem "memoriagestor"

const PlanificadorFrecuencia = 1
const NúcleoheapIniciar = 1024 * 1024
const planificadorDepurar = false
const pitFrecuencia = 100

var lista Linkedlista

type Planificadordatos struct {
	frecuencia	uint32
	tickRecuento	uint32

	switchforced	bool

	Activado	bool

	actualhilo	*THilo
	tss		*Tssentrada
}

var schedatos Planificadordatos = Planificadordatos{}

func (propio *Planificadordatos) Init() {
	schedatos.tickRecuento = 0
	schedatos.frecuencia = PlanificadorFrecuencia
	schedatos.actualhilo = nil
	schedatos.Activado = false
	schedatos.switchforced = false

}

var consola_2 = TConsola{}
var actualhiloÍndice int = 0
var siguienteprocesoid uint32 = 1

func Allocatepid() uint32 {
	pid := siguienteprocesoid
	siguienteprocesoid++
	return pid
}

func (propio *Planificadordatos) GetSiguientePreparadohilo() *THilo {
	if lista.Tamaño_2 <= 0 {
		return nil
	}

	if schedatos.actualhilo != nil {
		actualhiloÍndice = lista.Índicede(uintptr(Pointer(schedatos.actualhilo)))
		if actualhiloÍndice < 0 {
			actualhiloÍndice = 0
		}
	} else {
		actualhiloÍndice = -1
	}

	for checked := 0; checked < lista.Tamaño_2; checked++ {
		actualhiloÍndice++
		if actualhiloÍndice >= lista.Tamaño_2 {
			actualhiloÍndice = 0
		}
		hilo := (*THilo)(lista.Getat(actualhiloÍndice))
		if hilo != nil && hilo.HiloEstado != Blocked && hilo.HiloEstado != Parado {
			if planificadorDepurar {
				consola_2.MImprimir("ti:")
				consola_2.MUnsignedinteger32Imprimir(uint32(actualhiloÍndice))
				consola_2.MImprimir(":")
				consola_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(hilo))))
			}
			return hilo
		}
	}
	return schedatos.actualhilo

}
func (propio *Planificador) Añadirhilo(hilo *THilo) {
	if hilo == nil {
		return
	}
	lista.Añadir_al_final_de_la_lista(uintptr(Pointer(hilo)))
}
func Añadirrunnablehilo(hilo *THilo) {
	if hilo == nil {
		return
	}
	lista.Añadir_al_final_de_la_lista(uintptr(Pointer(hilo)))
}

func Actualpid() uint32 {
	if schedatos.actualhilo == nil || schedatos.actualhilo.Pid == 0 {
		return 1
	}
	return schedatos.actualhilo.Pid
}

func Actualpadrepid() uint32 {
	if schedatos.actualhilo == nil {
		return 0
	}
	return schedatos.actualhilo.Padrepid
}
func (propio *Planificador) Eliminarhilo(hilo *THilo) {
	lista.Eliminar_2(uintptr(Pointer(hilo)))
}

func (propio *Planificador) Eliminarhiloat(índice int) {
	lista.Eliminarat(índice)
}

type Planificador struct {
	TInterrupciónhandler
}

func (propio *Planificador) Init(gestor *TInterrupcióngestor, mem *mem.TMemoriagestor, tss *Tssentrada) {
	schedatos.Init()
	schedatos.tss = tss
	initpit(pitFrecuencia)

	lista = Linkedlista{}
	lista.Init(mem)
	consola_2.MImprimir("list:")
	consola_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(&lista))))

	interrupciónhandler = manijainterrupción
	var dirección uintptr
	dirección = uintptr(Pointer(&interrupciónhandler))
	propio.TInterrupciónhandler.Init(0x20, uintptr(Pointer(gestor)), dirección)
}

func (propio *Planificador) Activado(activado bool) {
	schedatos.Activado = activado
}

func initpit(frecuencia uint32) {
	if frecuencia == 0 {
		return
	}
	divisor := uint32(1193180) / frecuencia
	Puertoescribirocteto(0x43, 0x36)
	Puertoescribirocteto(0x40, uint8(divisor&0xFF))
	Puertoescribirocteto(0x40, uint8((divisor>>8)&0xFF))
}

func establecerds(dssegment uint32)
func establecergs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restaurarfpregs(buffer_2 uintptr)

var jmpusuario uint32 = 0
var interrupciónhandler func(uint32) uint32

func schedulestack(fn func())
func establecercr3(dirección uint32)
func getcr3() uint32

func manijainterrupción(esp uint32) uint32 {

	schedatos.tickRecuento++

	if planificadorDepurar {
		consola_2.MImprimirxy(([]byte)("sche1:"), 1, 17)

		consola_2.MImprimir(":")
		consola_2.MUnsignedinteger32Imprimir(esp)
		consola_2.MImprimir(":")

		consola_2.MUnsignedinteger32Imprimir(uint32(schedatos.tickRecuento))
		consola_2.MImprimir(":")
		consola_2.MUnsignedinteger32Imprimir(NúcleoheapIniciar)
	}

	if schedatos.tickRecuento == schedatos.frecuencia {
		schedatos.tickRecuento = 0

		if lista.Tamaño_2 > 0 && schedatos.Activado == true {
			var siguientehilo = schedatos.GetSiguientePreparadohilo()
			if siguientehilo == nil {
				return esp
			}
			if schedatos.actualhilo == nil {
				MEmergencyRegistroCadena("\nSCHED first esp=")
				MEmergencyRegistrounsignedinteger32(esp)
				MEmergencyRegistroCadena(" thread=")
				MEmergencyRegistrounsignedinteger32(uint32(uintptr(Pointer(siguientehilo))))
				MEmergencyRegistroCadena(" cpu=")
				MEmergencyRegistrounsignedinteger32(uint32(uintptr(Pointer(siguientehilo.CpuEstado))))
				MEmergencyRegistroCadena(" state=")
				MEmergencyRegistrounsignedinteger32(uint32(siguientehilo.HiloEstado))
				MEmergencyRegistroCadena(" eip=")
				MEmergencyRegistrounsignedinteger32(siguientehilo.CpuEstado.Eip)
				MEmergencyRegistroCadena(" cs=")
				MEmergencyRegistrounsignedinteger32(siguientehilo.CpuEstado.Cs)
				MEmergencyRegistroCadena("\n")
			}

			if esp >= NúcleoheapIniciar && schedatos.actualhilo != nil {
				schedatos.actualhilo.CpuEstado = (*TcpuEstado)(Pointer(uintptr(esp)))

				dirección := uintptr(Pointer(&(schedatos.actualhilo.Fpubuffer)))
				desplazamiento := (16 - (dirección % 16)) & 0xF
				schedatos.actualhilo.FpuDesplazamiento = desplazamiento
				backupfpregs(dirección + desplazamiento)
				if planificadorDepurar {
					consola_2.MImprimir(([]byte)("backup"))
					consola_2.MUnsignedinteger32Imprimir(esp)
				}
			}

			dirección := uintptr(Pointer(&(siguientehilo.Fpubuffer)))
			desplazamiento := siguientehilo.FpuDesplazamiento
			if desplazamiento != 0xffffffff {
				restaurarfpregs(dirección + desplazamiento)
				if planificadorDepurar {
					consola_2.MImprimir(([]byte)("restore"))
				}
			}

			schedatos.actualhilo = siguientehilo

			if schedatos.actualhilo.HiloEstado == Iniciado {
				schedatos.actualhilo.HiloEstado = Preparado

				Initialhilousuariojump(schedatos.actualhilo)
				return esp
			}

			esp = uint32(uintptr(Pointer(siguientehilo.CpuEstado)))
			if siguientehilo.Stack != 0 {
				schedatos.tss.Establecerstack(Segnúcleodatos, siguientehilo.Stack+HilostackTamaño)
			}

			establecercr3(siguientehilo.Páginadirectorioentrada)
			establecergs(siguientehilo.CpuEstado.Gs)

		}

	}

	return esp
}

func jumpMododeusuarioiret(uint32, uint32, uint32, uint32, uint32, uint32)
func DesactivarEntero()

func getesp() uint32
func hiloSalirBucle()

func establecerhiloSalirBucleEstado(cpuEstado *TcpuEstado) {
	cpuEstado.Eip = uint32(ValueOf(hiloSalirBucle).Pointer())
	cpuEstado.Cs = Segnúcleocode
	cpuEstado.Ds = Segnúcleodatos
	cpuEstado.Es = Segnúcleodatos
	cpuEstado.Fs = Segnúcleodatos
	cpuEstado.Gs = Segnúcleogs
	cpuEstado.Ss = Segnúcleodatos
	cpuEstado.Eflags = 0x202
}

func DetenerActualhilo(cpuEstado *TcpuEstado) *TcpuEstado {
	if schedatos.actualhilo == nil {
		establecerhiloSalirBucleEstado(cpuEstado)
		return cpuEstado
	}

	paradohilo := schedatos.actualhilo
	for i := 0; i < lista.Tamaño_2; i++ {
		hilo := (*THilo)(lista.Getat(i))
		if hilo != nil && hilo.CpuEstado == cpuEstado {
			paradohilo = hilo
			break
		}
	}
	paradohilo.CpuEstado = cpuEstado
	paradohilo.HiloEstado = Parado
	schedatos.actualhilo = paradohilo

	siguientehilo := schedatos.GetSiguientePreparadohilo()
	if siguientehilo == nil || siguientehilo == paradohilo || siguientehilo.CpuEstado == nil || siguientehilo.CpuEstado == cpuEstado {
		establecerhiloSalirBucleEstado(cpuEstado)
		return cpuEstado
	}

	schedatos.actualhilo = siguientehilo
	if siguientehilo.Stack != 0 && schedatos.tss != nil {
		schedatos.tss.Establecerstack(Segnúcleodatos, siguientehilo.Stack+HilostackTamaño)
	}
	establecercr3(siguientehilo.Páginadirectorioentrada)
	establecergs(siguientehilo.CpuEstado.Gs)
	return siguientehilo.CpuEstado
}

func Initialhilousuariojump(hilo *THilo) {

	DesactivarEntero()

	schedatos.tss.Establecerstack(Segnúcleodatos, hilo.Stack+HilostackTamaño)

	establecercr3(hilo.Páginadirectorioentrada)
	establecergs(hilo.CpuEstado.Gs)

	schedatos.actualhilo = hilo
	schedatos.Activado = true

	eip := hilo.CpuEstado.Eip
	usuarioesp := hilo.Usuariostack_2 + hilo.UsuariostackTamaño_2
	eflags := hilo.CpuEstado.Eflags
	cs := hilo.CpuEstado.Cs
	esp := schedatos.tss.Getesp0()

	consola_2.MImprimir(([]byte)("jump["))
	consola_2.MUnsignedinteger32Imprimir(eip)
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimir(usuarioesp)
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimir(eflags)
	consola_2.MImprimir(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimir(cs)
	consola_2.MImprimir(([]byte)(":"))

	consola_2.MUnsignedinteger32Imprimir(esp)
	consola_2.MImprimir(([]byte)("]"))

	userprocentrada := hilo.CpuEstado.Ecx
	globalDesplazamientoTabla_2 := hilo.CpuEstado.Edx
	dinámico := hilo.CpuEstado.Esi

	Puertoescribirocteto(0x20, 0x20)
	jumpMododeusuarioiret(eip, usuarioesp, eflags, userprocentrada, globalDesplazamientoTabla_2, dinámico)
	consola_2.MImprimir(([]byte)("usermode end"))
}
func imprimiresp(esp uint32) {
	consola_2.MImprimir(([]byte)("esp["))
	consola_2.MUnsignedinteger32Imprimir(esp)
}
