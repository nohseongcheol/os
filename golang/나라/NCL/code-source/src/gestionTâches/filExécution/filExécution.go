package FilExécution

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multiplegestionTâches"
import mem "mémoiregestionnaire"
import . "virtuelmémoire"

const (
	Blocked	= 1
	Prêt	= 2
	Stoppé	= 3
	Démarré	= 4
)

const FilExécutionstackTaille = 32 * 1024

type TFilExécution struct {
	ProcesseurÉtat			*TcpuÉtat
	Stack				uint32
	Utilisateurstack_2		uint32
	UtilisateurstackTaille_2	uint32
	Pid				uint32
	Parentpid			uint32

	Pagerépertoireélément	uint32

	FilExécutionÉtat	uint8
	BlockedÉtat		uint8

	heuredelta	uint32

	Tlssegments	[Gdtélément]TSegmentdescriptor
	FpuDécalage	uintptr
	Fpubuffer	[512 + 16]byte
	Isnoyau		bool
}

func (self *TFilExécution) Nouveau() {
}

type TFilExécutionhelper struct {
	mem *mem.TMémoiregestionnaire
}

var console_2 = TConsole{}

func (self *TFilExécutionhelper) Init(mem *mem.TMémoiregestionnaire) {
	self.mem = mem
	console_2.MImprimerxy(([]byte)("thread:"), 1, 14)
}
func (self *TFilExécutionhelper) CréerdeFonction(élémentpoint_2 func(), Pagerépertoireélément uint32, isnoyau bool) TFilExécution {
	rÉSULTAT := TFilExécution{}

	rÉSULTAT.Stack = uint32(uintptr(self.mem.Allouer_la_mémoire(FilExécutionstackTaille)))
	if rÉSULTAT.Stack == 0 {
		return rÉSULTAT
	}
	console_2.MImprimer(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Imprimer(rÉSULTAT.Stack)

	rÉSULTAT.ProcesseurÉtat = (*TcpuÉtat)(Pointer(uintptr(rÉSULTAT.Stack) + FilExécutionstackTaille - Sizeof(TcpuÉtat{})))
	rÉSULTAT.ProcesseurÉtat.Esp = rÉSULTAT.Stack + FilExécutionstackTaille
	rÉSULTAT.ProcesseurÉtat.Ebp = rÉSULTAT.ProcesseurÉtat.Esp
	rÉSULTAT.ProcesseurÉtat.Eip = uint32(ValueOf(élémentpoint_2).Pointer())
	rÉSULTAT.Utilisateurstack_2 = Utilisateurstack
	rÉSULTAT.UtilisateurstackTaille_2 = UtilisateurstackTaille
	rÉSULTAT.Pid = 0
	rÉSULTAT.Parentpid = 0
	rÉSULTAT.Pagerépertoireélément = Pagerépertoireélément
	console_2.MImprimer((([]byte)("cpu")))

	console_2.MUnsignedinteger32Imprimer(uint32(uintptr(Pointer(rÉSULTAT.ProcesseurÉtat))))

	console_2.MImprimer((([]byte)(":")))
	console_2.MUnsignedinteger32Imprimer(rÉSULTAT.ProcesseurÉtat.Eip)

	console_2.MImprimer("]")
	if isnoyau == true {
		rÉSULTAT.ProcesseurÉtat.Cs = Segnoyaucode
		rÉSULTAT.ProcesseurÉtat.Ds = Segnoyaudonnées
		rÉSULTAT.ProcesseurÉtat.Es = Segnoyaudonnées
		rÉSULTAT.ProcesseurÉtat.Fs = Segnoyaudonnées
		rÉSULTAT.ProcesseurÉtat.Gs = Segnoyaugs
		rÉSULTAT.ProcesseurÉtat.Ss = Segnoyaudonnées
		rÉSULTAT.FilExécutionÉtat = Prêt
		rÉSULTAT.ProcesseurÉtat.Eflags = 0x202
	} else {
		rÉSULTAT.ProcesseurÉtat.Cs = Segutilisateurcode
		rÉSULTAT.ProcesseurÉtat.Ds = Segutilisateurdonnées
		rÉSULTAT.ProcesseurÉtat.Es = Segutilisateurdonnées
		rÉSULTAT.ProcesseurÉtat.Fs = Segutilisateurdonnées
		rÉSULTAT.ProcesseurÉtat.Gs = Segutilisateurgs
		rÉSULTAT.ProcesseurÉtat.Ss = Segutilisateurdonnées
		rÉSULTAT.FilExécutionÉtat = Démarré
		rÉSULTAT.ProcesseurÉtat.Eflags = 0x222
	}
	rÉSULTAT.Isnoyau = isnoyau
	rÉSULTAT.FpuDécalage = 0xffffffff

	return rÉSULTAT
}

func (self *TFilExécutionhelper) CréerPointeurdeFonction(élémentpoint_2 func(), Pagerépertoireélément uint32, isnoyau bool) *TFilExécution {
	rÉSULTAT := (*TFilExécution)(self.mem.Allouer_la_mémoire(uint32(Sizeof(TFilExécution{}))))
	if rÉSULTAT == nil {
		return nil
	}
	*rÉSULTAT = self.CréerdeFonction(élémentpoint_2, Pagerépertoireélément, isnoyau)
	if rÉSULTAT.ProcesseurÉtat == nil {
		self.mem.Libre(Pointer(rÉSULTAT))
		return nil
	}
	return rÉSULTAT
}
