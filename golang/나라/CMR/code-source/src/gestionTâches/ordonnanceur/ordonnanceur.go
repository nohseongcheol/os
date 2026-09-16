/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ordonnanceur

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "utilitaire/liste"

import . "interruption"
import . "gestionTâches/filExécution"
import . "gestionTâches/tss"
import . "multiplegestionTâches"
import mem "mémoiregestionnaire"

const OrdonnanceurFréquence = 1
const NoyauheapDémarrer = 1024 * 1024
const ordonnanceurDéboguer = false
const pitFréquence = 100

var liste Linkedliste

type Ordonnanceurdonnées struct {
	fréquence	uint32
	tickNombre	uint32

	switchforced	bool

	Activé	bool

	courantefilExécution	*TFilExécution
	tss			*Tssélément
}

var schedonnées Ordonnanceurdonnées = Ordonnanceurdonnées{}

func (self *Ordonnanceurdonnées) Init() {
	schedonnées.tickNombre = 0
	schedonnées.fréquence = OrdonnanceurFréquence
	schedonnées.courantefilExécution = nil
	schedonnées.Activé = false
	schedonnées.switchforced = false

}

var console_2 = TConsole{}
var courantefilExécutionindex int = 0
var suivantprocessusIdentifiant uint32 = 1

func Allocatepid() uint32 {
	pid := suivantprocessusIdentifiant
	suivantprocessusIdentifiant++
	return pid
}

func (self *Ordonnanceurdonnées) GetSuivantPrêtfilExécution() *TFilExécution {
	if liste.Taille_2 <= 0 {
		return nil
	}

	if schedonnées.courantefilExécution != nil {
		courantefilExécutionindex = liste.Indexsur(uintptr(Pointer(schedonnées.courantefilExécution)))
		if courantefilExécutionindex < 0 {
			courantefilExécutionindex = 0
		}
	} else {
		courantefilExécutionindex = -1
	}

	for checked := 0; checked < liste.Taille_2; checked++ {
		courantefilExécutionindex++
		if courantefilExécutionindex >= liste.Taille_2 {
			courantefilExécutionindex = 0
		}
		filExécution := (*TFilExécution)(liste.Getat(courantefilExécutionindex))
		if filExécution != nil && filExécution.FilExécutionÉtat != Blocked && filExécution.FilExécutionÉtat != Stoppé {
			if ordonnanceurDéboguer {
				console_2.MImprimer("ti:")
				console_2.MUnsignedinteger32Imprimer(uint32(courantefilExécutionindex))
				console_2.MImprimer(":")
				console_2.MUnsignedinteger32Imprimer(uint32(uintptr(Pointer(filExécution))))
			}
			return filExécution
		}
	}
	return schedonnées.courantefilExécution

}
func (self *Ordonnanceur) AjouterfilExécution(filExécution *TFilExécution) {
	if filExécution == nil {
		return
	}
	liste.Ajouter_en_fin_de_liste(uintptr(Pointer(filExécution)))
}
func AjouterrunnablefilExécution(filExécution *TFilExécution) {
	if filExécution == nil {
		return
	}
	liste.Ajouter_en_fin_de_liste(uintptr(Pointer(filExécution)))
}

func Courantepid() uint32 {
	if schedonnées.courantefilExécution == nil || schedonnées.courantefilExécution.Pid == 0 {
		return 1
	}
	return schedonnées.courantefilExécution.Pid
}

func Couranteparentpid() uint32 {
	if schedonnées.courantefilExécution == nil {
		return 0
	}
	return schedonnées.courantefilExécution.Parentpid
}
func (self *Ordonnanceur) SupprimerfilExécution(filExécution *TFilExécution) {
	liste.Supprimer_2(uintptr(Pointer(filExécution)))
}

func (self *Ordonnanceur) SupprimerfilExécutionat(index int) {
	liste.Supprimerat(index)
}

type Ordonnanceur struct {
	TInterruptionhandler
}

func (self *Ordonnanceur) Init(gestionnaire *TInterruptiongestionnaire, mem *mem.TMémoiregestionnaire, tss *Tssélément) {
	schedonnées.Init()
	schedonnées.tss = tss
	initpit(pitFréquence)

	liste = Linkedliste{}
	liste.Init(mem)
	console_2.MImprimer("list:")
	console_2.MUnsignedinteger32Imprimer(uint32(uintptr(Pointer(&liste))))

	interruptionhandler = poignéeinterruption
	var address uintptr
	address = uintptr(Pointer(&interruptionhandler))
	self.TInterruptionhandler.Init(0x20, uintptr(Pointer(gestionnaire)), address)
}

func (self *Ordonnanceur) Activé(activé bool) {
	schedonnées.Activé = activé
}

func initpit(fréquence uint32) {
	if fréquence == 0 {
		return
	}
	divisor := uint32(1193180) / fréquence
	Portécrireoctet(0x43, 0x36)
	Portécrireoctet(0x40, uint8(divisor&0xFF))
	Portécrireoctet(0x40, uint8((divisor>>8)&0xFF))
}

func ensembleds(dssegment uint32)
func ensemblegs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restaurerfpregs(buffer_2 uintptr)

var jmputilisateur uint32 = 0
var interruptionhandler func(uint32) uint32

func schedulestack(fn func())
func ensemblecr3(address uint32)
func getcr3() uint32

func poignéeinterruption(esp uint32) uint32 {

	schedonnées.tickNombre++

	if ordonnanceurDéboguer {
		console_2.MImprimerxy(([]byte)("sche1:"), 1, 17)

		console_2.MImprimer(":")
		console_2.MUnsignedinteger32Imprimer(esp)
		console_2.MImprimer(":")

		console_2.MUnsignedinteger32Imprimer(uint32(schedonnées.tickNombre))
		console_2.MImprimer(":")
		console_2.MUnsignedinteger32Imprimer(NoyauheapDémarrer)
	}

	if schedonnées.tickNombre == schedonnées.fréquence {
		schedonnées.tickNombre = 0

		if liste.Taille_2 > 0 && schedonnées.Activé == true {
			var suivantfilExécution = schedonnées.GetSuivantPrêtfilExécution()
			if suivantfilExécution == nil {
				return esp
			}
			if schedonnées.courantefilExécution == nil {
				MEmergencyJournalChaîne("\nSCHED first esp=")
				MEmergencyJournalunsignedinteger32(esp)
				MEmergencyJournalChaîne(" thread=")
				MEmergencyJournalunsignedinteger32(uint32(uintptr(Pointer(suivantfilExécution))))
				MEmergencyJournalChaîne(" cpu=")
				MEmergencyJournalunsignedinteger32(uint32(uintptr(Pointer(suivantfilExécution.ProcesseurÉtat))))
				MEmergencyJournalChaîne(" state=")
				MEmergencyJournalunsignedinteger32(uint32(suivantfilExécution.FilExécutionÉtat))
				MEmergencyJournalChaîne(" eip=")
				MEmergencyJournalunsignedinteger32(suivantfilExécution.ProcesseurÉtat.Eip)
				MEmergencyJournalChaîne(" cs=")
				MEmergencyJournalunsignedinteger32(suivantfilExécution.ProcesseurÉtat.Cs)
				MEmergencyJournalChaîne("\n")
			}

			if esp >= NoyauheapDémarrer && schedonnées.courantefilExécution != nil {
				schedonnées.courantefilExécution.ProcesseurÉtat = (*TcpuÉtat)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedonnées.courantefilExécution.Fpubuffer)))
				décalage := (16 - (address % 16)) & 0xF
				schedonnées.courantefilExécution.FpuDécalage = décalage
				backupfpregs(address + décalage)
				if ordonnanceurDéboguer {
					console_2.MImprimer(([]byte)("backup"))
					console_2.MUnsignedinteger32Imprimer(esp)
				}
			}

			address := uintptr(Pointer(&(suivantfilExécution.Fpubuffer)))
			décalage := suivantfilExécution.FpuDécalage
			if décalage != 0xffffffff {
				restaurerfpregs(address + décalage)
				if ordonnanceurDéboguer {
					console_2.MImprimer(([]byte)("restore"))
				}
			}

			schedonnées.courantefilExécution = suivantfilExécution

			if schedonnées.courantefilExécution.FilExécutionÉtat == Démarré {
				schedonnées.courantefilExécution.FilExécutionÉtat = Prêt

				InitialfilExécutionutilisateurjump(schedonnées.courantefilExécution)
				return esp
			}

			esp = uint32(uintptr(Pointer(suivantfilExécution.ProcesseurÉtat)))
			if suivantfilExécution.Stack != 0 {
				schedonnées.tss.Ensemblestack(Segnoyaudonnées, suivantfilExécution.Stack+FilExécutionstackTaille)
			}

			ensemblecr3(suivantfilExécution.Pagerépertoireélément)
			ensemblegs(suivantfilExécution.ProcesseurÉtat.Gs)

		}

	}

	return esp
}

func jumpModeutilisateuriret(uint32, uint32, uint32, uint32, uint32, uint32)
func Désactiverint()

func getesp() uint32
func filExécutionQuitterBoucles()

func ensemblefilExécutionQuitterBouclesÉtat(processeurÉtat *TcpuÉtat) {
	processeurÉtat.Eip = uint32(ValueOf(filExécutionQuitterBoucles).Pointer())
	processeurÉtat.Cs = Segnoyaucode
	processeurÉtat.Ds = Segnoyaudonnées
	processeurÉtat.Es = Segnoyaudonnées
	processeurÉtat.Fs = Segnoyaudonnées
	processeurÉtat.Gs = Segnoyaugs
	processeurÉtat.Ss = Segnoyaudonnées
	processeurÉtat.Eflags = 0x202
}

func ArrêterCourantefilExécution(processeurÉtat *TcpuÉtat) *TcpuÉtat {
	if schedonnées.courantefilExécution == nil {
		ensemblefilExécutionQuitterBouclesÉtat(processeurÉtat)
		return processeurÉtat
	}

	stoppéfilExécution := schedonnées.courantefilExécution
	for i := 0; i < liste.Taille_2; i++ {
		filExécution := (*TFilExécution)(liste.Getat(i))
		if filExécution != nil && filExécution.ProcesseurÉtat == processeurÉtat {
			stoppéfilExécution = filExécution
			break
		}
	}
	stoppéfilExécution.ProcesseurÉtat = processeurÉtat
	stoppéfilExécution.FilExécutionÉtat = Stoppé
	schedonnées.courantefilExécution = stoppéfilExécution

	suivantfilExécution := schedonnées.GetSuivantPrêtfilExécution()
	if suivantfilExécution == nil || suivantfilExécution == stoppéfilExécution || suivantfilExécution.ProcesseurÉtat == nil || suivantfilExécution.ProcesseurÉtat == processeurÉtat {
		ensemblefilExécutionQuitterBouclesÉtat(processeurÉtat)
		return processeurÉtat
	}

	schedonnées.courantefilExécution = suivantfilExécution
	if suivantfilExécution.Stack != 0 && schedonnées.tss != nil {
		schedonnées.tss.Ensemblestack(Segnoyaudonnées, suivantfilExécution.Stack+FilExécutionstackTaille)
	}
	ensemblecr3(suivantfilExécution.Pagerépertoireélément)
	ensemblegs(suivantfilExécution.ProcesseurÉtat.Gs)
	return suivantfilExécution.ProcesseurÉtat
}

func InitialfilExécutionutilisateurjump(filExécution *TFilExécution) {

	Désactiverint()

	schedonnées.tss.Ensemblestack(Segnoyaudonnées, filExécution.Stack+FilExécutionstackTaille)

	ensemblecr3(filExécution.Pagerépertoireélément)
	ensemblegs(filExécution.ProcesseurÉtat.Gs)

	schedonnées.courantefilExécution = filExécution
	schedonnées.Activé = true

	eip := filExécution.ProcesseurÉtat.Eip
	utilisateuresp := filExécution.Utilisateurstack_2 + filExécution.UtilisateurstackTaille_2
	eflags := filExécution.ProcesseurÉtat.Eflags
	cs := filExécution.ProcesseurÉtat.Cs
	esp := schedonnées.tss.Getesp0()

	console_2.MImprimer(([]byte)("jump["))
	console_2.MUnsignedinteger32Imprimer(eip)
	console_2.MImprimer(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimer(utilisateuresp)
	console_2.MImprimer(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimer(eflags)
	console_2.MImprimer(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimer(cs)
	console_2.MImprimer(([]byte)(":"))

	console_2.MUnsignedinteger32Imprimer(esp)
	console_2.MImprimer(([]byte)("]"))

	userprocélément := filExécution.ProcesseurÉtat.Ecx
	globalDécalageTableau_2 := filExécution.ProcesseurÉtat.Edx
	dynamique := filExécution.ProcesseurÉtat.Esi

	Portécrireoctet(0x20, 0x20)
	jumpModeutilisateuriret(eip, utilisateuresp, eflags, userprocélément, globalDécalageTableau_2, dynamique)
	console_2.MImprimer(([]byte)("usermode end"))
}
func imprimeresp(esp uint32) {
	console_2.MImprimer(([]byte)("esp["))
	console_2.MUnsignedinteger32Imprimer(esp)
}
