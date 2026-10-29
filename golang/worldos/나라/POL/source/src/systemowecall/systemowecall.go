/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systemowecall

import . "unsafe"

import . "przerwanie"
import . "konsola"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "plikSystemowe/msdospartition"
import . "plikSystemowe/fat"
import . "plikSystemowe/format_wykonywalny_i_konsolidowalny"
import mem "pamięćmanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "wirtualnePamięć"

var konsola_2 = TKonsola{}

type TSyscall struct {
	TPrzerwaniehandler
}

const (
	SysZakończ	uint32	= 1
	Sysfork		uint32	= 2
	SysOdczyt	uint32	= 3
	SysZapis	uint32	= 4
	SysOtwórz	uint32	= 5
	SysZamknij	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysdostępu	uint32	= 33
	Syssync		uint32	= 36
	Sysdup		uint32	= 41
	Sysbrk		uint32	= 45
	Sysgetgid	uint32	= 47
	Sysgeteuid	uint32	= 49
	Sysgetegid	uint32	= 50
	Sysfcntl	uint32	= 55
	Sysdup2		uint32	= 63
	Sysgetppid	uint32	= 64
	Syssocketcall	uint32	= 102
	Sysstat		uint32	= 106
	Syslstat	uint32	= 107
	Sysfstat	uint32	= 108
	Sysfsync	uint32	= 118
	Sysuname	uint32	= 122
	Sysgetcwd	uint32	= 183
	SysrtZakończ	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2big		int32	= -7
	Enoexec		int32	= -8
	Ebadf		int32	= -9
	Echild		int32	= -10
	Eagain		int32	= -11
	Enomem		int32	= -12
	Eacces		int32	= -13
	Efault		int32	= -14
	Ebusy		int32	= -16
	Eexist		int32	= -17
	Enodev		int32	= -19
	Enotdir		int32	= -20
	Eisdir		int32	= -21
	Einval		int32	= -22
	Enfile		int32	= -23
	Emfile		int32	= -24
	Enotty		int32	= -25
	Efbig		int32	= -27
	Enospc		int32	= -28
	Espipe		int32	= -29
	Erofs		int32	= -30
	Erange		int32	= -34
	Enosys		int32	= -38
	Emsgsize	int32	= -90
	Eprotonosupport	int32	= -93
	Eopnotsupp	int32	= -95
	Eafnosupport	int32	= -97
	Eaddrinuse	int32	= -98
	Enetunreach	int32	= -101
	Enotconn	int32	= -107
)

const (
	stdinDP			int32	= 0
	stdoutDP		int32	= 1
	stderrDP		int32	= 2
	maksymalnaDP			= 32
	maksymalnaOtwórzPLIKI		= 128
)

type dPwpis struct {
	użytych		bool
	opis		int32
	dPZnaczniki	uint32
}

type otwórzPlikOpis struct {
	użytych		bool
	refs		uint32
	rodzaj		uint32
	znaczniki	uint32
	pozycja		uint32
	rozmiar		uint32
	nazwa		[12]byte
	nazwalen	uint32
	aux		uint32
}

const (
	dPRodzajBrak			uint32	= 0
	dPRodzajfat			uint32	= 1
	dPRodzajstdin			uint32	= 2
	dPRodzajKonsola			uint32	= 3
	dPRodzajElementgłównyKatalog	uint32	= 4
	dPRodzajGniazdo			uint32	= 5

	oOdczytonly	uint32	= 0
	oZapisonly	uint32	= 1
	oOdczytZapis	uint32	= 2
	ocreate		uint32	= 0x40
	oObcina		uint32	= 0x200
	oappend		uint32	= 0x400
	oKatalog	uint32	= 0x10000

	seekzbiór	uint32	= 0
	seekBieżący	uint32	= 1
	seekKoniec	uint32	= 2

	fdupDP		uint32	= 0
	fgetDP		uint32	= 1
	fzbiórDP	uint32	= 2
	fgetfl		uint32	= 3
	fzbiórfl	uint32	= 4
	dPcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet				= 2
	sockdatagram			= 2
	ipprotocoludp			= 17
	maksymalnasockets		= 32
	maksymalnaGniazdopakietów	= 8
	maksymalnadatagramRozmiar	= 512
)

type gniazdoAdresiOw4 struct {
	Family	uint16
	Port	uint16
	Adres	uint32
	Zero	[8]byte
}

type gniazdoPAKIET struct {
	użytych	bool
	rozmiar	uint32
	źródło	gniazdoAdresiOw4
	data	[maksymalnadatagramRozmiar]byte
}

type lokalnydatagramGniazdo struct {
	użytych		bool
	bound		bool
	connected	bool
	lokalny		gniazdoAdresiOw4
	zdalne		gniazdoAdresiOw4
	head		uint32
	tail		uint32
	liczba		uint32
	pakietów	[maksymalnaGniazdopakietów]gniazdoPAKIET
}

type posixstat struct {
	Urządzenie	uint32
	Ino		uint32
	TRYB		uint32
	Nlink		uint32
	Użytkownik	uint32
	Gid		uint32
	Rdev		uint32
	Rozmiar_2	int32
	Blksize		int32
	Blok		int32
	Atime		int32
	Atimensec	int32
	Mtime		int32
	Mtimensec	int32
	Ctime		int32
	Ctimensec	int32
}

type posixutsname struct {
	Sysname		[65]byte
	Nodename	[65]byte
	Release		[65]byte
	Wersja		[65]byte
	Machine		[65]byte
}

const (
	maksymalnaUruchomienievectorwpis	= 16
	maksymalnaUruchomienieCIĄGDługość	= 63
)

type uruchomienievector struct {
	liczba		uint32
	lengths		[maksymalnaUruchomienievectorwpis]uint32
	wartości	[maksymalnaUruchomienievectorwpis][maksymalnaUruchomienieCIĄGDługość + 1]byte
}

type proceswpis struct {
	użytych		bool
	identyfikator_2	uint32
	rodzic		uint32
	zakończono	bool
	stan		uint32
	programbreak	uint32
	fds		[maksymalnaDP]dPwpis
}

type cIĄGheader struct {
	Data	uintptr
	Len	int
}

func syscallBłąd(błędy int32) uint32 {
	return *(*uint32)(Pointer(&błędy))
}

var otwórzPlikTabela [maksymalnaOtwórzPLIKI]otwórzPlikOpis
var procesTabela [32]proceswpis
var lokalnysockets [maksymalnasockets]lokalnydatagramGniazdo
var następnyephemeralport uint16 = 49152

const (
	użytkownikheapbase	uint32	= 0x06000000
	użytkownikheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinOdczyt uint32
var stdinZapis uint32

func Przerwanie(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysZakończ_2(indeks uint32) {
	Syscall(SysZakończ, indeks)
}

func SysOdczyt_2(dP uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysOdczyt, dP, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysWydrukujstr(buffer string) {
	h := (*cIĄGheader)(Pointer(&buffer))
	Syscall(SysZapis, uint32(stdoutDP), uint32(h.Data), uint32(h.Len))
}

func SysWydrukujunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysZapis, uint32(stdoutDP), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOtwórz_2(śCIEŻKA uintptr, znaczniki uint32, tRYB uint32) int32 {
	return int32(Syscall(SysOtwórz, uint32(śCIEŻKA), znaczniki, tRYB))
}

func SysZamknij_2(dP uint32) int32 {
	return int32(Syscall(SysZamknij, dP))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(adres uint32) uint32 {
	return Syscall(Sysbrk, adres)
}

func Syscall(parametry ...uint32) uint32 {

	l := len(parametry)
	switch l {
	case 1:
		return Przerwanie(parametry[0], 0, 0, 0, 0, 0)
	case 2:
		return Przerwanie(parametry[0], parametry[1], 0, 0, 0, 0)
	case 3:
		return Przerwanie(parametry[0], parametry[1], parametry[2], 0, 0, 0)
	case 4:
		return Przerwanie(parametry[0], parametry[1], parametry[2], parametry[3], 0, 0)
	case 5:
		return Przerwanie(parametry[0], parametry[1], parametry[2], parametry[3], parametry[4], 0)
	case 6:
		return Przerwanie(parametry[0], parametry[1], parametry[2], parametry[3], parametry[4], parametry[5])
	default:
		return syscallBłąd(Enosys)
	}
}

func (bieżący *TSyscall) Init(manager *TPrzerwaniemanager) {
	initPlikdescriptor()

	przerwaniehandler = uchwytPrzerwanie

	var adres uintptr
	adres = uintptr(Pointer(&przerwaniehandler))

	bieżący.TPrzerwaniehandler.Init(0x80, uintptr(Pointer(manager)), adres)
}

var przerwaniehandler func(uint32) uint32

func uchwytPrzerwanie(esp uint32) uint32 {
	var procesor = (*TcpuStan)(Pointer(uintptr(esp)))

	switch procesor.Eax {
	case SysZakończ:
		sysZakończ(procesor.Ebx)
		return uint32(uintptr(Pointer(ZatrzymajBieżącythread(procesor))))
	case SysrtZakończ:
		sysZakończ(procesor.Ebx)
		return uint32(uintptr(Pointer(ZatrzymajBieżącythread(procesor))))
	case Sysfork:
		procesor.Eax = uint32(sysfork(procesor))
		return esp
	case SysOdczyt:
		procesor.Eax = uint32(sysOdczyt(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysZapis:
		procesor.Eax = uint32(sysZapis(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysOtwórz:
		procesor.Eax = uint32(sysOtwórz(procesor.Ebx, procesor.Ecx, procesor.Edx))
		return esp
	case Syscreat:
		procesor.Eax = uint32(sysOtwórz(procesor.Ebx, ocreate|oZapisonly|oObcina, procesor.Ecx))
		return esp
	case SysZamknij:
		procesor.Eax = uint32(sysZamknij(int32(procesor.Ebx)))
		return esp
	case Syswaitpid:
		procesor.Eax = uint32(syswaitpid(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case Syslseek:
		procesor.Eax = uint32(syslseek(int32(procesor.Ebx), int32(procesor.Ecx), procesor.Edx))
		return esp
	case Sysexecve:
		procesor.Eax = uint32(sysexecve(procesor, procesor.Ebx))
		return esp
	case Sysgetpid:
		procesor.Eax = BieżącyIdentyfikator()
		return esp
	case Sysgetppid:
		procesor.Eax = BieżącyrodzicIdentyfikator()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		procesor.Eax = 0
		return esp
	case Sysdostępu:
		procesor.Eax = uint32(sysdostępu(procesor.Ebx, procesor.Ecx))
		return esp
	case Syschdir:
		procesor.Eax = uint32(syschdir(procesor.Ebx))
		return esp
	case Sysgetcwd:
		procesor.Eax = uint32(sysgetcwd(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysdup:
		procesor.Eax = uint32(sysdup(int32(procesor.Ebx), 0))
		return esp
	case Sysdup2:
		procesor.Eax = uint32(sysdup2(int32(procesor.Ebx), int32(procesor.Ecx)))
		return esp
	case Syssocketcall:
		procesor.Eax = uint32(sysGniazdocall(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysfcntl:
		procesor.Eax = uint32(sysfcntl(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case Sysstat, Syslstat:
		procesor.Eax = uint32(sysstat(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysfstat:
		procesor.Eax = uint32(sysfstat(int32(procesor.Ebx), procesor.Ecx))
		return esp
	case Sysfsync:
		procesor.Eax = uint32(sysfsync(int32(procesor.Ebx)))
		return esp
	case Syssync:
		procesor.Eax = 0
		return esp
	case Sysuname:
		procesor.Eax = uint32(sysuname(procesor.Ebx))
		return esp
	case Sysbrk:
		procesor.Eax = sysbrk(procesor.Ebx)
		return esp
	case 9:
		konsola_2.MUnsignedinteger32Wydrukuj(procesor.Ebx)
		return esp

	default:
		konsola_2.MWydrukujxy(([]byte)("sys["), 1, 23)
		konsola_2.MUnsignedinteger32Wydrukuj(esp)
		konsola_2.MWydrukuj(([]byte)(":"))
		konsola_2.MUnsignedinteger32Wydrukuj(procesor.Eax)
		konsola_2.MWydrukuj(([]byte)(":"))
		konsola_2.MUnsignedinteger32Wydrukuj(procesor.Ebx)
		konsola_2.MWydrukuj(([]byte)(":"))
		konsola_2.MUnsignedinteger32Wydrukuj(procesor.Ecx)
		konsola_2.MWydrukuj(([]byte)(":"))
		konsola_2.MUnsignedinteger32Wydrukuj(procesor.Edx)
		konsola_2.MWydrukuj(([]byte)("]"))
		procesor.Eax = syscallBłąd(Enosys)
		return esp
	}

	return esp
}

func initPlikdescriptor() {
	for i := 0; i < maksymalnaOtwórzPLIKI; i++ {
		otwórzPlikTabela[i] = otwórzPlikOpis{}
	}
	for i := 0; i < len(procesTabela); i++ {
		procesTabela[i] = proceswpis{}
	}
	for i := 0; i < len(lokalnysockets); i++ {
		lokalnysockets[i] = lokalnydatagramGniazdo{}
	}
	następnyephemeralport = 49152
	otwórzPlikTabela[0] = otwórzPlikOpis{użytych: true, rodzaj: dPRodzajstdin, znaczniki: oOdczytonly}
	otwórzPlikTabela[1] = otwórzPlikOpis{użytych: true, rodzaj: dPRodzajKonsola, znaczniki: oZapisonly}
	otwórzPlikTabela[2] = otwórzPlikOpis{użytych: true, rodzaj: dPRodzajKonsola, znaczniki: oZapisonly}
}

func znajdźProces(identyfikator_2 uint32) *proceswpis {
	for i := 0; i < len(procesTabela); i++ {
		if procesTabela[i].użytych && procesTabela[i].identyfikator_2 == identyfikator_2 {
			return &procesTabela[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *proceswpis) {
	for dP := int32(0); dP <= stderrDP; dP++ {
		proces.fds[dP] = dPwpis{użytych: true, opis: dP}
		otwórzPlikTabela[dP].refs++
	}
}

func ensureBieżącyProces() *proceswpis {
	identyfikator_2 := BieżącyIdentyfikator()
	if proces := znajdźProces(identyfikator_2); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabela); i++ {
		if !procesTabela[i].użytych {
			procesTabela[i] = proceswpis{
				użytych:		true,
				identyfikator_2:	identyfikator_2,
				rodzic:			BieżącyrodzicIdentyfikator(),
				programbreak:		użytkownikheapbase,
			}
			initializeProcesfds(&procesTabela[i])
			return &procesTabela[i]
		}
	}
	return nil
}

func getOtwórzPlikfor(proces *proceswpis, dP int32) *otwórzPlikOpis {
	if proces == nil || dP < 0 || dP >= maksymalnaDP || !proces.fds[dP].użytych {
		return nil
	}
	opis := proces.fds[dP].opis
	if opis < 0 || opis >= maksymalnaOtwórzPLIKI || !otwórzPlikTabela[opis].użytych {
		return nil
	}
	return &otwórzPlikTabela[opis]
}

func getOtwórzPlik(dP int32) *otwórzPlikOpis {
	return getOtwórzPlikfor(ensureBieżącyProces(), dP)
}

func allocateOtwórzPlik() int32 {
	for i := int32(3); i < maksymalnaOtwórzPLIKI; i++ {
		if !otwórzPlikTabela[i].użytych {
			otwórzPlikTabela[i] = otwórzPlikOpis{użytych: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateDP(proces *proceswpis, opis int32, minimum int32) int32 {
	if proces == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maksymalnaDP {
		return Einval
	}
	for dP := minimum; dP < maksymalnaDP; dP++ {
		if !proces.fds[dP].użytych {
			proces.fds[dP] = dPwpis{użytych: true, opis: opis}
			return dP
		}
	}
	return Emfile
}

func releaseOtwórzPlik(opis int32) {
	if opis < 0 || opis >= maksymalnaOtwórzPLIKI {
		return
	}
	wpis := &otwórzPlikTabela[opis]
	if wpis.refs > 0 {
		wpis.refs--
	}

	if wpis.refs == 0 && opis > stderrDP {
		if wpis.rodzaj == dPRodzajGniazdo && wpis.aux < maksymalnasockets {
			lokalnysockets[wpis.aux] = lokalnydatagramGniazdo{}
		}
		*wpis = otwórzPlikOpis{}
	}
}

func zamknijProcesDP(proces *proceswpis, dP int32) int32 {
	if proces == nil || getOtwórzPlikfor(proces, dP) == nil {
		return Ebadf
	}
	opis := proces.fds[dP].opis
	proces.fds[dP] = dPwpis{}
	releaseOtwórzPlik(opis)
	return 0
}

func sysZapis(dP int32, adres uint32, liczba uint32) int32 {
	if liczba == 0 {
		return 0
	}
	if adres == 0 || adres+liczba < adres {
		return Efault
	}
	if liczba > 4096 {
		return Einval
	}
	wpis := getOtwórzPlik(dP)
	if wpis == nil {
		return Ebadf
	}
	if wpis.rodzaj != dPRodzajKonsola {
		if wpis.rodzaj == dPRodzajGniazdo {
			return gniazdoWyślijto(dP, adres, liczba, 0, 0)
		}
		if wpis.rodzaj == dPRodzajfat || wpis.rodzaj == dPRodzajElementgłównyKatalog {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBajtyzKursor(uintptr(adres), int(liczba), int(liczba))
	konsola_2.MWydrukuj(buffer)
	return int32(liczba)
}

func sysOdczyt(dP int32, adres uint32, liczba uint32) int32 {
	if liczba == 0 {
		return 0
	}
	if adres == 0 || adres+liczba < adres {
		return Efault
	}
	wpis := getOtwórzPlik(dP)
	if wpis == nil {
		return Ebadf
	}
	if wpis.rodzaj == dPRodzajstdin {
		return odczytstdin(adres, liczba)
	}
	if wpis.rodzaj == dPRodzajElementgłównyKatalog {
		return Eisdir
	}
	if wpis.rodzaj == dPRodzajGniazdo {
		return gniazdoreceivez(dP, adres, liczba, 0, 0)
	}
	if wpis.rodzaj != dPRodzajfat {
		return Ebadf
	}
	if wpis.pozycja >= wpis.rozmiar {
		return 0
	}
	remaining := wpis.rozmiar - wpis.pozycja
	if liczba > remaining {
		liczba = remaining
	}
	buffer := GetBajtyzKursor(uintptr(adres), int(liczba), int(liczba))
	return odczytvfsPlik(wpis, buffer, liczba)
}

func sysOtwórz(śCIEŻKAAdres uint32, znaczniki uint32, tRYB uint32) int32 {
	_ = tRYB
	if śCIEŻKAAdres == 0 {
		return Efault
	}
	dostępuTRYB := znaczniki & 3
	if dostępuTRYB == oZapisonly || dostępuTRYB == oOdczytZapis || (znaczniki&(ocreate|oObcina|oappend)) != 0 {
		return Erofs
	}

	proces := ensureBieżącyProces()
	if proces == nil {
		return Enfile
	}
	opis := allocateOtwórzPlik()
	if opis < 0 {
		return opis
	}
	wpis := &otwórzPlikTabela[opis]
	wpis.znaczniki = znaczniki
	if isElementgłównyŚCIEŻKA(śCIEŻKAAdres) {
		wpis.rodzaj = dPRodzajElementgłównyKatalog
		wpis.rozmiar = 0
	} else {
		nazwalen, nazwa := kopiujŚCIEŻKA(śCIEŻKAAdres)
		if nazwalen == 0 {
			*wpis = otwórzPlikOpis{}
			return Enoent
		}
		rozmiar := plikRozmiar(nazwa[:nazwalen])
		if rozmiar == 0 {
			*wpis = otwórzPlikOpis{}
			return Enoent
		}
		if (znaczniki & oKatalog) != 0 {
			*wpis = otwórzPlikOpis{}
			return Enotdir
		}
		wpis.rodzaj = dPRodzajfat
		wpis.rozmiar = rozmiar
		wpis.nazwalen = nazwalen
		wpis.nazwa = nazwa
	}

	dP := allocateDP(proces, opis, 3)
	if dP < 0 {
		*wpis = otwórzPlikOpis{}
		return dP
	}
	return dP
}

func sysZamknij(dP int32) int32 {
	return zamknijProcesDP(ensureBieżącyProces(), dP)
}

func sysdup(dP int32, minimum int32) int32 {
	proces := ensureBieżącyProces()
	wpis := getOtwórzPlikfor(proces, dP)
	if wpis == nil {
		return Ebadf
	}
	nowyDP := allocateDP(proces, proces.fds[dP].opis, minimum)
	if nowyDP >= 0 {
		wpis.refs++
	}
	return nowyDP
}

func sysdup2(oldDP int32, nowyDP int32) int32 {
	proces := ensureBieżącyProces()
	wpis := getOtwórzPlikfor(proces, oldDP)
	if wpis == nil {
		return Ebadf
	}
	if nowyDP < 0 || nowyDP >= maksymalnaDP {
		return Ebadf
	}
	if oldDP == nowyDP {
		return nowyDP
	}
	if proces.fds[nowyDP].użytych {
		zamknijProcesDP(proces, nowyDP)
	}
	proces.fds[nowyDP] = dPwpis{użytych: true, opis: proces.fds[oldDP].opis}
	wpis.refs++
	return nowyDP
}

func sysfcntl(dP int32, polecenie uint32, argument uint32) int32 {
	proces := ensureBieżącyProces()
	wpis := getOtwórzPlikfor(proces, dP)
	if wpis == nil {
		return Ebadf
	}
	switch polecenie {
	case fdupDP:
		return sysdup(dP, int32(argument))
	case fgetDP:
		return int32(proces.fds[dP].dPZnaczniki)
	case fzbiórDP:
		proces.fds[dP].dPZnaczniki = argument & dPcloexec
		return 0
	case fgetfl:
		return int32(wpis.znaczniki)
	case fzbiórfl:
		wpis.znaczniki = (wpis.znaczniki & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(dP int32, przesunięcie int32, whence uint32) int32 {
	wpis := getOtwórzPlik(dP)
	if wpis == nil {
		return Ebadf
	}
	if wpis.rodzaj != dPRodzajfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekzbiór:
		base = 0
	case seekBieżący:
		base = int64(wpis.pozycja)
	case seekKoniec:
		base = int64(wpis.rozmiar)
	default:
		return Einval
	}
	pozycja_2 := base + int64(przesunięcie)
	if pozycja_2 < 0 || pozycja_2 > 0x7FFFFFFF {
		return Einval
	}
	wpis.pozycja = uint32(pozycja_2)
	return int32(wpis.pozycja)
}

func odczytvfsPlik(wpis *otwórzPlikOpis, cel_2 []byte, liczba uint32) int32 {
	pamięćmanager := &mem.TPamięćmanager{}
	tmpKursor := pamięćmanager.Przydziel_pamięć(wpis.rozmiar)
	if tmpKursor == nil {
		return Einval
	}
	tmp := GetBajtyzKursor(uintptr(tmpKursor), int(wpis.rozmiar), int(wpis.rozmiar))
	odczytPlik(wpis.nazwa[:wpis.nazwalen], tmp)
	copy(cel_2[:liczba], tmp[wpis.pozycja:wpis.pozycja+liczba])
	wpis.pozycja += liczba
	pamięćmanager.Wolne(tmpKursor)
	return int32(liczba)
}

func isElementgłównyŚCIEŻKA(śCIEŻKAAdres uint32) bool {
	if śCIEŻKAAdres == 0 {
		return false
	}
	śCIEŻKA := GetBajtyzKursor(uintptr(śCIEŻKAAdres), 4, 4)
	if śCIEŻKA[0] == '/' && śCIEŻKA[1] == 0 {
		return true
	}
	if śCIEŻKA[0] == '.' && śCIEŻKA[1] == 0 {
		return true
	}
	if śCIEŻKA[0] == '/' && śCIEŻKA[1] == '.' && śCIEŻKA[2] == 0 {
		return true
	}
	return false
}

func sysdostępu(śCIEŻKAAdres uint32, tRYB uint32) int32 {
	if śCIEŻKAAdres == 0 {
		return Efault
	}
	if (tRYB & ^uint32(7)) != 0 {
		return Einval
	}
	isElementgłówny := isElementgłównyŚCIEŻKA(śCIEŻKAAdres)
	exists := isElementgłówny
	if !exists {
		nazwalen, nazwa := kopiujŚCIEŻKA(śCIEŻKAAdres)
		exists = nazwalen != 0 && plikRozmiar(nazwa[:nazwalen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (tRYB & 2) != 0 {
		return Eacces
	}

	if (tRYB&1) != 0 && !isElementgłówny {
		return Eacces
	}
	return 0
}

func syschdir(śCIEŻKAAdres uint32) int32 {
	if śCIEŻKAAdres == 0 {
		return Efault
	}
	if !isElementgłównyŚCIEŻKA(śCIEŻKAAdres) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferAdres uint32, rozmiar uint32) int32 {
	if bufferAdres == 0 {
		return Efault
	}
	if rozmiar < 2 {
		return Erange
	}
	buffer_2 := GetBajtyzKursor(uintptr(bufferAdres), int(rozmiar), int(rozmiar))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statAdres uint32, tRYB uint32, rozmiar uint32, iwęzeł uint32) int32 {
	if statAdres == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statAdres)))
	*stat = posixstat{}
	stat.Urządzenie = 1
	stat.Ino = iwęzeł
	stat.TRYB = tRYB
	stat.Nlink = 1
	stat.Rozmiar_2 = int32(rozmiar)
	stat.Blksize = 512
	stat.Blok = int32((rozmiar + 511) / 512)
	return 0
}

func sysstat(śCIEŻKAAdres uint32, statAdres uint32) int32 {
	if śCIEŻKAAdres == 0 {
		return Efault
	}
	if isElementgłównyŚCIEŻKA(śCIEŻKAAdres) {
		return fillposixstat(statAdres, sifdir|0555, 0, 1)
	}
	nazwalen, nazwa := kopiujŚCIEŻKA(śCIEŻKAAdres)
	if nazwalen == 0 {
		return Enoent
	}
	rozmiar := plikRozmiar(nazwa[:nazwalen])
	if rozmiar == 0 {
		return Enoent
	}
	iwęzeł := uint32(2)
	for i := uint32(0); i < nazwalen; i++ {
		iwęzeł = iwęzeł*33 + uint32(nazwa[i])
	}
	return fillposixstat(statAdres, sifreg|0444, rozmiar, iwęzeł)
}

func sysfstat(dP int32, statAdres uint32) int32 {
	wpis := getOtwórzPlik(dP)
	if wpis == nil {
		return Ebadf
	}
	switch wpis.rodzaj {
	case dPRodzajstdin, dPRodzajKonsola:
		return fillposixstat(statAdres, sifchr|0666, 0, uint32(dP+1))
	case dPRodzajElementgłównyKatalog:
		return fillposixstat(statAdres, sifdir|0555, 0, 1)
	case dPRodzajfat:
		return fillposixstat(statAdres, sifreg|0444, wpis.rozmiar, uint32(dP+2))
	case dPRodzajGniazdo:
		return fillposixstat(statAdres, sifsock|0666, 0, uint32(dP+2))
	}
	return Ebadf
}

func sysfsync(dP int32) int32 {
	if getOtwórzPlik(dP) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(adres_2 uint32) uint32 {
	proces := ensureBieżącyProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = użytkownikheapbase
	}
	if adres_2 == 0 {
		return proces.programbreak
	}
	if adres_2 < użytkownikheapbase || adres_2 > użytkownikheaplimit {
		return proces.programbreak
	}
	proces.programbreak = adres_2
	return proces.programbreak
}

func kopiujutspole(cel *[65]byte, wartość string) {
	limit := len(wartość)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		cel[i] = wartość[i]
	}
	cel[limit] = 0
}

func sysuname(adres_2 uint32) int32 {
	if adres_2 == 0 {
		return Efault
	}
	nazwa := (*posixutsname)(Pointer(uintptr(adres_2)))
	*nazwa = posixutsname{}
	kopiujutspole(&nazwa.Sysname, "EngOS")
	kopiujutspole(&nazwa.Nodename, "engos")
	kopiujutspole(&nazwa.Release, "0.1-posix")
	kopiujutspole(&nazwa.Wersja, "POSIX.1-2017 phase 1")
	kopiujutspole(&nazwa.Machine, "i386")
	return 0
}

func przestrzeńwymianyunsignedinteger16(wartość uint16) uint16 {
	return (wartość << 8) | (wartość >> 8)
}

func gniazdocallargument(argumenty_2 uint32, indeks uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenty_2 + indeks*4)))
}

func gniazdoforDP(dP int32) (*lokalnydatagramGniazdo, int32) {
	wpis := getOtwórzPlik(dP)
	if wpis == nil || wpis.rodzaj != dPRodzajGniazdo || wpis.aux >= maksymalnasockets {
		return nil, Ebadf
	}
	gniazdo := &lokalnysockets[wpis.aux]
	if !gniazdo.użytych {
		return nil, Ebadf
	}
	return gniazdo, 0
}

func allocateGniazdo(domena uint32, gniazdoTyp uint32, protocol uint32) int32 {
	if domena != afinet {
		return Eafnosupport
	}
	if gniazdoTyp != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureBieżącyProces()
	if proces == nil {
		return Enfile
	}
	gniazdoIndeks := -1
	for i := 0; i < maksymalnasockets; i++ {
		if !lokalnysockets[i].użytych {
			gniazdoIndeks = i
			break
		}
	}
	if gniazdoIndeks < 0 {
		return Enfile
	}
	opis := allocateOtwórzPlik()
	if opis < 0 {
		return opis
	}
	lokalnysockets[gniazdoIndeks] = lokalnydatagramGniazdo{użytych: true}
	wpis := &otwórzPlikTabela[opis]
	wpis.rodzaj = dPRodzajGniazdo
	wpis.znaczniki = oOdczytZapis
	wpis.aux = uint32(gniazdoIndeks)
	dP := allocateDP(proces, opis, 3)
	if dP < 0 {
		lokalnysockets[gniazdoIndeks] = lokalnydatagramGniazdo{}
		*wpis = otwórzPlikOpis{}
		return dP
	}
	return dP
}

func gniazdoAdres(adres_2 uint32, długość uint32) (*gniazdoAdresiOw4, int32) {
	if adres_2 == 0 {
		return nil, Efault
	}
	if długość < 16 {
		return nil, Einval
	}
	wYNIK := (*gniazdoAdresiOw4)(Pointer(uintptr(adres_2)))
	if wYNIK.Family != afinet {
		return nil, Eafnosupport
	}
	return wYNIK, 0
}

func portWchodzącyUżyj(port uint16, except *lokalnydatagramGniazdo) bool {
	for i := 0; i < maksymalnasockets; i++ {
		gniazdo := &lokalnysockets[i]
		if gniazdo != except && gniazdo.użytych && gniazdo.bound && gniazdo.lokalny.Port == port {
			return true
		}
	}
	return false
}

func dowiążephemeral(gniazdo *lokalnydatagramGniazdo) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := przestrzeńwymianyunsignedinteger16(następnyephemeralport)
		następnyephemeralport++
		if następnyephemeralport < 49152 {
			następnyephemeralport = 49152
		}
		if !portWchodzącyUżyj(port, gniazdo) {
			gniazdo.lokalny = gniazdoAdresiOw4{Family: afinet, Port: port, Adres: 0x0100007F}
			gniazdo.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func gniazdoDowiąż(dP int32, adres_2 uint32, długość uint32) int32 {
	gniazdo, błędy := gniazdoforDP(dP)
	if błędy != 0 {
		return błędy
	}
	requested, błędy := gniazdoAdres(adres_2, długość)
	if błędy != 0 {
		return błędy
	}
	if gniazdo.bound {
		return Einval
	}
	if requested.Port == 0 {
		return dowiążephemeral(gniazdo)
	}
	if portWchodzącyUżyj(requested.Port, gniazdo) {
		return Eaddrinuse
	}
	gniazdo.lokalny = *requested
	gniazdo.bound = true
	return 0
}

func gniazdoPołącz(dP int32, adres_2 uint32, długość uint32) int32 {
	gniazdo, błędy := gniazdoforDP(dP)
	if błędy != 0 {
		return błędy
	}
	zdalne, błędy := gniazdoAdres(adres_2, długość)
	if błędy != 0 {
		return błędy
	}
	if !gniazdo.bound {
		if błędy := dowiążephemeral(gniazdo); błędy != 0 {
			return błędy
		}
	}
	gniazdo.zdalne = *zdalne
	gniazdo.connected = true
	return 0
}

func gniazdoWyślijto(dP int32, bufferAdres_2 uint32, długość uint32, celAdres uint32, celDługość uint32) int32 {
	gniazdo, błędy := gniazdoforDP(dP)
	if błędy != 0 {
		return błędy
	}
	if długość > maksymalnadatagramRozmiar {
		return Emsgsize
	}
	if długość != 0 && bufferAdres_2 == 0 {
		return Efault
	}
	var cel gniazdoAdresiOw4
	if celAdres != 0 {
		adres_2, adresBłąd := gniazdoAdres(celAdres, celDługość)
		if adresBłąd != 0 {
			return adresBłąd
		}
		cel = *adres_2
	} else {
		if !gniazdo.connected {
			return Enotconn
		}
		cel = gniazdo.zdalne
	}
	if !gniazdo.bound {
		if dowiążBłąd := dowiążephemeral(gniazdo); dowiążBłąd != 0 {
			return dowiążBłąd
		}
	}
	var receiver *lokalnydatagramGniazdo
	for i := 0; i < maksymalnasockets; i++ {
		candidate := &lokalnysockets[i]
		if candidate.użytych && candidate.bound && candidate.lokalny.Port == cel.Port &&
			(candidate.lokalny.Adres == 0 || candidate.lokalny.Adres == cel.Adres) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.liczba >= maksymalnaGniazdopakietów {
		return Eagain
	}
	pAKIET := &receiver.pakietów[receiver.tail]
	*pAKIET = gniazdoPAKIET{użytych: true, rozmiar: długość, źródło: gniazdo.lokalny}
	if długość != 0 {
		źródło := GetBajtyzKursor(uintptr(bufferAdres_2), int(długość), int(długość))
		copy(pAKIET.data[:długość], źródło)
	}
	receiver.tail = (receiver.tail + 1) % maksymalnaGniazdopakietów
	receiver.liczba++
	return int32(długość)
}

func gniazdoreceivez(dP int32, bufferAdres_2 uint32, długość uint32, źródłoAdres uint32, źródłoDługośćAdres uint32) int32 {
	gniazdo, błędy := gniazdoforDP(dP)
	if błędy != 0 {
		return błędy
	}
	if długość != 0 && bufferAdres_2 == 0 {
		return Efault
	}
	if gniazdo.liczba == 0 {
		return Eagain
	}
	pAKIET := &gniazdo.pakietów[gniazdo.head]
	kopiujDługość := pAKIET.rozmiar
	if kopiujDługość > długość {
		kopiujDługość = długość
	}
	if kopiujDługość != 0 {
		cel := GetBajtyzKursor(uintptr(bufferAdres_2), int(kopiujDługość), int(kopiujDługość))
		copy(cel, pAKIET.data[:kopiujDługość])
	}
	if źródłoAdres != 0 {
		if źródłoDługośćAdres == 0 {
			return Efault
		}
		providedDługość := (*uint32)(Pointer(uintptr(źródłoDługośćAdres)))
		if *providedDługość >= 16 {
			*(*gniazdoAdresiOw4)(Pointer(uintptr(źródłoAdres))) = pAKIET.źródło
		}
		*providedDługość = 16
	}
	*pAKIET = gniazdoPAKIET{}
	gniazdo.head = (gniazdo.head + 1) % maksymalnaGniazdopakietów
	gniazdo.liczba--
	return int32(kopiujDługość)
}

func kopiujGniazdoNazwa(dP int32, adres_2 uint32, długośćAdres uint32, peer bool) int32 {
	gniazdo, błędy := gniazdoforDP(dP)
	if błędy != 0 {
		return błędy
	}
	if adres_2 == 0 || długośćAdres == 0 {
		return Efault
	}
	długość := (*uint32)(Pointer(uintptr(długośćAdres)))
	if *długość < 16 {
		*długość = 16
		return Einval
	}
	if peer {
		if !gniazdo.connected {
			return Enotconn
		}
		*(*gniazdoAdresiOw4)(Pointer(uintptr(adres_2))) = gniazdo.zdalne
	} else {
		if !gniazdo.bound {
			if dowiążBłąd := dowiążephemeral(gniazdo); dowiążBłąd != 0 {
				return dowiążBłąd
			}
		}
		*(*gniazdoAdresiOw4)(Pointer(uintptr(adres_2))) = gniazdo.lokalny
	}
	*długość = 16
	return 0
}

func sysGniazdocall(call uint32, argumenty_2 uint32) int32 {
	if argumenty_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateGniazdo(gniazdocallargument(argumenty_2, 0), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2))
	case 2:
		return gniazdoDowiąż(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2))
	case 3:
		return gniazdoPołącz(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopiujGniazdoNazwa(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2), false)
	case 7:
		return kopiujGniazdoNazwa(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2), true)
	case 9:
		return gniazdoWyślijto(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2), 0, 0)
	case 10:
		return gniazdoreceivez(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2), 0, 0)
	case 11:
		return gniazdoWyślijto(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2), gniazdocallargument(argumenty_2, 4), gniazdocallargument(argumenty_2, 5))
	case 12:
		return gniazdoreceivez(int32(gniazdocallargument(argumenty_2, 0)), gniazdocallargument(argumenty_2, 1), gniazdocallargument(argumenty_2, 2), gniazdocallargument(argumenty_2, 4), gniazdocallargument(argumenty_2, 5))
	case 13:
		if _, błędy := gniazdoforDP(int32(gniazdocallargument(argumenty_2, 0))); błędy != 0 {
			return błędy
		}
		return 0
	case 14:
		if _, błędy := gniazdoforDP(int32(gniazdocallargument(argumenty_2, 0))); błędy != 0 {
			return błędy
		}
		return 0
	}
	return Eopnotsupp
}

func odczytstdin(adres uint32, liczba uint32) int32 {
	if adres == 0 {
		return Einval
	}
	buffer := GetBajtyzKursor(uintptr(adres), int(liczba), int(liczba))
	var n uint32
	for n < liczba {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputbyte(c byte) {
	następny := (stdinZapis + 1) % uint32(len(stdinbuffer))
	if następny == stdinOdczyt {
		return
	}
	stdinbuffer[stdinZapis] = c
	stdinZapis = następny
}

func stdingetblocking() byte {
	for stdinOdczyt == stdinZapis {
		sc := pollKlawiaturascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinOdczyt]
	stdinOdczyt = (stdinOdczyt + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlawiaturascancode() byte {
	for (PortOdczytbyte(0x64) & 0x01) == 0 {
	}
	sc := PortOdczytbyte(0x60)
	return scancodetobyte(sc)
}

func scancodetobyte(sc uint8) byte {
	if sc >= 0x80 {
		return 0
	}
	switch sc {
	case 0x02:
		return '1'
	case 0x03:
		return '2'
	case 0x04:
		return '3'
	case 0x05:
		return '4'
	case 0x06:
		return '5'
	case 0x07:
		return '6'
	case 0x08:
		return '7'
	case 0x09:
		return '8'
	case 0x0A:
		return '9'
	case 0x0B:
		return '0'
	case 0x10:
		return 'q'
	case 0x11:
		return 'w'
	case 0x12:
		return 'e'
	case 0x13:
		return 'r'
	case 0x14:
		return 't'
	case 0x15:
		return 'y'
	case 0x16:
		return 'u'
	case 0x17:
		return 'i'
	case 0x18:
		return 'o'
	case 0x19:
		return 'p'
	case 0x1E:
		return 'a'
	case 0x1F:
		return 's'
	case 0x20:
		return 'd'
	case 0x21:
		return 'f'
	case 0x22:
		return 'g'
	case 0x23:
		return 'h'
	case 0x24:
		return 'j'
	case 0x25:
		return 'k'
	case 0x26:
		return 'l'
	case 0x2C:
		return 'z'
	case 0x2D:
		return 'x'
	case 0x2E:
		return 'c'
	case 0x2F:
		return 'v'
	case 0x30:
		return 'b'
	case 0x31:
		return 'n'
	case 0x32:
		return 'm'
	case 0x33:
		return ','
	case 0x34:
		return '.'
	case 0x35:
		return '/'
	case 0x1C:
		return '\n'
	case 0x39:
		return ' '
	}
	return 0
}

func kopiujUruchomienievector(adres_2 uint32, wYNIK *uruchomienievector) int32 {
	*wYNIK = uruchomienievector{}
	if adres_2 == 0 {
		return 0
	}
	for indeks := uint32(0); indeks < maksymalnaUruchomienievectorwpis; indeks++ {
		cIĄGAdres := *(*uint32)(Pointer(uintptr(adres_2 + indeks*4)))
		if cIĄGAdres == 0 {
			wYNIK.liczba = indeks
			return 0
		}
		terminated := false
		for długość := uint32(0); długość <= maksymalnaUruchomienieCIĄGDługość; długość++ {
			wartość := *(*byte)(Pointer(uintptr(cIĄGAdres + długość)))
			wYNIK.wartości[indeks][długość] = wartość
			if wartość == 0 {
				wYNIK.lengths[indeks] = długość
				terminated = true
				break
			}
		}
		if !terminated {
			return E2big
		}
	}
	return E2big
}

func pushUruchomienieunsignedinteger32(pamięć_stosu *uint32, wartość uint32) {
	*pamięć_stosu -= 4
	*(*uint32)(Pointer(uintptr(*pamięć_stosu))) = wartość
}

func setupUruchomieniestack(procesor *TcpuStan, argumenty_2 *uruchomienievector, environment *uruchomienievector) int32 {
	const stackBajty uint32 = 4096
	if !MakeZakresPrywatnewritable(getcr3(), UżytkownikstackGóra-stackBajty, stackBajty) {
		return Enomem
	}
	pamięć_stosu := UżytkownikstackGóra
	var argumentpointers [maksymalnaUruchomienievectorwpis]uint32
	var environmentpointers [maksymalnaUruchomienievectorwpis]uint32

	for i := int(environment.liczba) - 1; i >= 0; i-- {
		długość := environment.lengths[i] + 1
		pamięć_stosu -= długość
		cel := GetBajtyzKursor(uintptr(pamięć_stosu), int(długość), int(długość))
		copy(cel, environment.wartości[i][:długość])
		environmentpointers[i] = pamięć_stosu
	}
	for i := int(argumenty_2.liczba) - 1; i >= 0; i-- {
		długość := argumenty_2.lengths[i] + 1
		pamięć_stosu -= długość
		cel := GetBajtyzKursor(uintptr(pamięć_stosu), int(długość), int(długość))
		copy(cel, argumenty_2.wartości[i][:długość])
		argumentpointers[i] = pamięć_stosu
	}
	pamięć_stosu &= ^uint32(3)
	pushUruchomienieunsignedinteger32(&pamięć_stosu, 0)
	for i := int(environment.liczba) - 1; i >= 0; i-- {
		pushUruchomienieunsignedinteger32(&pamięć_stosu, environmentpointers[i])
	}
	pushUruchomienieunsignedinteger32(&pamięć_stosu, 0)
	for i := int(argumenty_2.liczba) - 1; i >= 0; i-- {
		pushUruchomienieunsignedinteger32(&pamięć_stosu, argumentpointers[i])
	}
	pushUruchomienieunsignedinteger32(&pamięć_stosu, argumenty_2.liczba)
	procesor.Esp = pamięć_stosu
	procesor.Ebp = 0
	return 0
}

func zamknijWłączUruchomienie(proces *proceswpis) {
	if proces == nil {
		return
	}
	for dP := int32(0); dP < maksymalnaDP; dP++ {
		if proces.fds[dP].użytych && (proces.fds[dP].dPZnaczniki&dPcloexec) != 0 {
			zamknijProcesDP(proces, dP)
		}
	}
}

func sysexecve(procesor *TcpuStan, śCIEŻKAAdres uint32) int32 {
	if śCIEŻKAAdres == 0 {
		return Efault
	}
	var argumenty_2 uruchomienievector
	var environment uruchomienievector
	if wYNIK := kopiujUruchomienievector(procesor.Ecx, &argumenty_2); wYNIK < 0 {
		return wYNIK
	}
	if wYNIK := kopiujUruchomienievector(procesor.Edx, &environment); wYNIK < 0 {
		return wYNIK
	}
	nazwalen, nazwa := kopiujŚCIEŻKA(śCIEŻKAAdres)
	if nazwalen == 0 {
		return Enoent
	}
	rozmiar := plikRozmiar(nazwa[:nazwalen])
	if rozmiar == 0 {
		return Enoent
	}
	pamięćmanager := &mem.TPamięćmanager{}
	plikKursor := pamięćmanager.Przydziel_pamięć(rozmiar)
	if plikKursor == nil {
		return Einval
	}
	data := GetBajtyzKursor(uintptr(plikKursor), int(rozmiar), int(rozmiar))
	odczytPlik(nazwa[:nazwalen], data)
	if rozmiar < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		pamięćmanager.Wolne(plikKursor)
		return Enoexec
	}
	loader := Elf{}
	wpis := loader.Getwpis(data)
	loader.Parse(data, getcr3())
	pamięćmanager.Wolne(plikKursor)
	if wYNIK := setupUruchomieniestack(procesor, &argumenty_2, &environment); wYNIK < 0 {
		return wYNIK
	}
	zamknijWłączUruchomienie(ensureBieżącyProces())
	procesor.Eip = wpis
	procesor.Eax = 0
	return 0
}

func sysfork(procesor *TcpuStan) int32 {
	rodzicIdentyfikator := BieżącyIdentyfikator()
	if ensureBieżącyProces() == nil {
		return Enfile
	}
	identyfikator_2 := allocateProces(rodzicIdentyfikator)
	if identyfikator_2 == 0 {
		return Einval
	}
	pamięćmanager := &mem.TPamięćmanager{}
	threadKursor := pamięćmanager.Przydziel_pamięć(uint32(Sizeof(TThread{})))
	stackKursor := pamięćmanager.Przydziel_pamięć(ThreadstackRozmiar)
	dzieckoStronaKatalog := CloneAdresSpacjacow(getcr3())
	if threadKursor == nil || stackKursor == nil || dzieckoStronaKatalog == 0 {
		porzućProces(identyfikator_2)
		return Einval
	}
	dziecko := (*TThread)(threadKursor)
	dziecko.Stack = uint32(uintptr(stackKursor))
	dziecko.ProcesorStan = (*TcpuStan)(Pointer(uintptr(stackKursor) + ThreadstackRozmiar - Sizeof(TcpuStan{})))
	*dziecko.ProcesorStan = *procesor
	dziecko.ProcesorStan.Eax = 0
	dziecko.Użytkownikstack_2 = procesor.Esp
	dziecko.UżytkownikstackRozmiar_2 = 0
	dziecko.Identyfikator = identyfikator_2
	dziecko.RodzicIdentyfikator = rodzicIdentyfikator
	dziecko.StronaKatalogwpis = dzieckoStronaKatalog
	dziecko.ThreadStan = Gotowy
	dziecko.FpuPrzesunięcie = 0xffffffff
	dziecko.Iskernel = false
	Dodajrunnablethread(dziecko)
	return int32(identyfikator_2)
}

func sysZakończ(stan uint32) {
	identyfikator_2 := BieżącyIdentyfikator()
	for i := 0; i < len(procesTabela); i++ {
		if procesTabela[i].użytych && procesTabela[i].identyfikator_2 == identyfikator_2 {
			zamknijWszystkieProcesfds(&procesTabela[i])
			procesTabela[i].zakończono = true
			procesTabela[i].stan = (stan & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(identyfikator_2 int32, stanAdres uint32, opcje uint32) int32 {
	if (opcje & ^uint32(1)) != 0 {
		return Einval
	}
	rodzicIdentyfikator := BieżącyIdentyfikator()
	founddziecko := false
	for i := 0; i < len(procesTabela); i++ {
		p := &procesTabela[i]
		matches := identyfikator_2 == -1 || identyfikator_2 == 0 || p.identyfikator_2 == uint32(identyfikator_2)
		if p.użytych && matches && p.rodzic == rodzicIdentyfikator {
			founddziecko = true
			if p.zakończono {
				if stanAdres != 0 {
					*(*uint32)(Pointer(uintptr(stanAdres))) = p.stan
				}
				dzieckoIdentyfikator := p.identyfikator_2
				*p = proceswpis{}
				return int32(dzieckoIdentyfikator)
			}
		}
	}
	if !founddziecko {
		return Echild
	}

	if (opcje & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(rodzic uint32) uint32 {
	rodzicProces := znajdźProces(rodzic)
	identyfikator_2 := AllocateIdentyfikator()
	for i := 0; i < len(procesTabela); i++ {
		if !procesTabela[i].użytych {
			procesTabela[i] = proceswpis{
				użytych:		true,
				identyfikator_2:	identyfikator_2,
				rodzic:			rodzic,
				programbreak:		użytkownikheapbase,
			}
			if rodzicProces != nil {
				procesTabela[i].programbreak = rodzicProces.programbreak
				for dP := 0; dP < maksymalnaDP; dP++ {
					if rodzicProces.fds[dP].użytych {
						procesTabela[i].fds[dP] = rodzicProces.fds[dP]
						opis := rodzicProces.fds[dP].opis
						if opis >= 0 && opis < maksymalnaOtwórzPLIKI {
							otwórzPlikTabela[opis].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabela[i])
			}
			return identyfikator_2
		}
	}
	return 0
}

func zamknijWszystkieProcesfds(proces *proceswpis) {
	if proces == nil {
		return
	}
	for dP := int32(0); dP < maksymalnaDP; dP++ {
		if proces.fds[dP].użytych {
			zamknijProcesDP(proces, dP)
		}
	}
}

func porzućProces(identyfikator_2 uint32) {
	proces := znajdźProces(identyfikator_2)
	if proces == nil {
		return
	}
	zamknijWszystkieProcesfds(proces)
	*proces = proceswpis{}
}

func kopiujŚCIEŻKA(śCIEŻKAAdres uint32) (uint32, [12]byte) {
	var nazwa [12]byte
	if śCIEŻKAAdres == 0 {
		return 0, nazwa
	}
	raw := GetBajtyzKursor(uintptr(śCIEŻKAAdres), 64, 64)
	var n uint32
	for i := 0; i < 64 && n < 12; i++ {
		c := raw[i]
		if c == 0 {
			break
		}
		if c == '/' {
			n = 0
			continue
		}
		if c >= 'a' && c <= 'z' {
			c = c - 32
		}
		if c == '.' {
			continue
		}
		nazwa[n] = c
		n++
	}
	return n, nazwa
}

func plikRozmiar(nazwapliku []byte) uint32 {
	var ata0s = TZaawansowaneTechnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Odczytpartition(&ata0s)

	bios := TParametry_systemu_plików32{}
	rozmiar := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nazwapliku)
	ata0s.Flush()
	return rozmiar
}

func odczytPlik(nazwapliku []byte, data []byte) {
	var ata0s = TZaawansowaneTechnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Odczytpartition(&ata0s)

	bios := TParametry_systemu_plików32{}
	bios.Odczyt(&ata0s, partition.Mbr.Primarypartition[0], nazwapliku, data)
	ata0s.Flush()
}

func getcr3() uint32
