package systemAufruf

import . "unsafe"

import . "unterbrechung"
import . "konsole"
import . "hilfswerkzeug"
import . "mehrfachAufgabenverwaltung"
import . "treiber/ata"
import . "dateiSystem/msdosPartition"
import . "dateiSystem/fat"
import . "dateiSystem/ausführbares_und_bindbares_Format"
import mem "speicherVerwalter"
import . "seitenverwaltung"
import . "anschluss"
import . "aufgabenverwaltung/planer"
import . "aufgabenverwaltung/ausführungsfaden"
import . "virtuellSpeicher"

var konsole_2 = TKonsole{}

type TSyscall struct {
	TUnterbrechunghandler
}

const (
	SysBeenden	uint32	= 1
	Sysfork		uint32	= 2
	SysLesen	uint32	= 3
	SysSchreiben	uint32	= 4
	SysÖffnen	uint32	= 5
	SysSchließen	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syszugreifen	uint32	= 33
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
	SysrtBeenden	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2Groß		int32	= -7
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
	stdinfd			int32	= 0
	stdoutfd		int32	= 1
	stderrfd		int32	= 2
	maximumfd			= 32
	maximumÖffnenDATEIEN		= 128
)

type fdEintrag struct {
	belegt		bool
	beschreibung	int32
	fdOptionen	uint32
}

type öffnenDateiBeschreibung struct {
	belegt		bool
	refs		uint32
	art		uint32
	optionen	uint32
	position	uint32
	größe		uint32
	elementname	[12]byte
	elementnamelen	uint32
	aux		uint32
}

const (
	fdArtKeine		uint32	= 0
	fdArtfat		uint32	= 1
	fdArtstdin		uint32	= 2
	fdArtKonsole		uint32	= 3
	fdArtBasisordnerOrdner	uint32	= 4
	fdArtNetzanschluss	uint32	= 5

	oLesennur		uint32	= 0
	oSchreibennur		uint32	= 1
	oLesenSchreiben		uint32	= 2
	oErstellen		uint32	= 0x40
	oWertabschneiden	uint32	= 0x200
	oappend			uint32	= 0x400
	oOrdner			uint32	= 0x10000

	seekSetzen	uint32	= 0
	seekSystemzeit	uint32	= 1
	seekEnde	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fSetzenfd	uint32	= 2
	fgetfl		uint32	= 3
	fSetzenfl	uint32	= 4
	fdcloexec	uint32	= 1

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
	maximumsockets			= 32
	maximumNetzanschlussPakete	= 8
	maximumdatagramGröße		= 512
)

type netzanschlussaddressiBw4 struct {
	Family		uint16
	Anschluss	uint16
	Address		uint32
	Null		[8]byte
}

type netzanschlussPAKET struct {
	belegt	bool
	größe	uint32
	quelle	netzanschlussaddressiBw4
	daten	[maximumdatagramGröße]byte
}

type lokaldatagramNetzanschluss struct {
	belegt		bool
	bound		bool
	connected	bool
	lokal		netzanschlussaddressiBw4
	entfernt	netzanschlussaddressiBw4
	head		uint32
	tail		uint32
	anzahl		uint32
	pakete		[maximumNetzanschlussPakete]netzanschlussPAKET
}

type posixstat struct {
	Gerät		uint32
	Ino		uint32
	Modus		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Größe_2		int32
	Blksize		int32
	Rechteck	int32
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
	Version		[65]byte
	Machine		[65]byte
}

const (
	maximumAusführenvectorEintrag		= 16
	maximumAusführenZeichenketteLänge	= 63
)

type ausführenvector struct {
	anzahl	uint32
	lengths	[maximumAusführenvectorEintrag]uint32
	werte	[maximumAusführenvectorEintrag][maximumAusführenZeichenketteLänge + 1]byte
}

type prozessEintrag struct {
	belegt		bool
	prozesskennung	uint32
	elternelement	uint32
	beendet		bool
	status		uint32
	programmbreak	uint32
	fds		[maximumfd]fdEintrag
}

type zeichenketteKopf struct {
	Data	uintptr
	Len	int
}

func syscallFehler(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var öffnenDateiTabelle [maximumÖffnenDATEIEN]öffnenDateiBeschreibung
var prozessTabelle [32]prozessEintrag
var lokalsockets [maximumsockets]lokaldatagramNetzanschluss
var weiterephemeralAnschluss uint16 = 49152

const (
	benutzerheapbase		uint32	= 0x06000000
	benutzerheapBeschränkung	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLesen uint32
var stdinSchreiben uint32

func Unterbrechung(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysBeenden_2(inhalt uint32) {
	Syscall(SysBeenden, inhalt)
}

func SysLesen_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLesen, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysDruckenstr(buffer string) {
	h := (*zeichenketteKopf)(Pointer(&buffer))
	Syscall(SysSchreiben, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysDruckenunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysSchreiben, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysÖffnen_2(pFAD uintptr, optionen uint32, modus uint32) int32 {
	return int32(Syscall(SysÖffnen, uint32(pFAD), optionen, modus))
}

func SysSchließen_2(fd uint32) int32 {
	return int32(Syscall(SysSchließen, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parameter ...uint32) uint32 {

	l := len(parameter)
	switch l {
	case 1:
		return Unterbrechung(parameter[0], 0, 0, 0, 0, 0)
	case 2:
		return Unterbrechung(parameter[0], parameter[1], 0, 0, 0, 0)
	case 3:
		return Unterbrechung(parameter[0], parameter[1], parameter[2], 0, 0, 0)
	case 4:
		return Unterbrechung(parameter[0], parameter[1], parameter[2], parameter[3], 0, 0)
	case 5:
		return Unterbrechung(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4], 0)
	case 6:
		return Unterbrechung(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4], parameter[5])
	default:
		return syscallFehler(Enosys)
	}
}

func (selbst *TSyscall) Init(verwalter *TUnterbrechungVerwalter) {
	initDateidescriptor()

	unterbrechunghandler = griffUnterbrechung

	var address uintptr
	address = uintptr(Pointer(&unterbrechunghandler))

	selbst.TUnterbrechunghandler.Init(0x80, uintptr(Pointer(verwalter)), address)
}

var unterbrechunghandler func(uint32) uint32

func griffUnterbrechung(esp uint32) uint32 {
	var cpu = (*TcpuStatus)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysBeenden:
		sysBeenden(cpu.Ebx)
		return uint32(uintptr(Pointer(AnhaltenSystemzeitAusführungsfaden(cpu))))
	case SysrtBeenden:
		sysBeenden(cpu.Ebx)
		return uint32(uintptr(Pointer(AnhaltenSystemzeitAusführungsfaden(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLesen:
		cpu.Eax = uint32(sysLesen(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysSchreiben:
		cpu.Eax = uint32(sysSchreiben(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysÖffnen:
		cpu.Eax = uint32(sysÖffnen(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysÖffnen(cpu.Ebx, oErstellen|oSchreibennur|oWertabschneiden, cpu.Ecx))
		return esp
	case SysSchließen:
		cpu.Eax = uint32(sysSchließen(int32(cpu.Ebx)))
		return esp
	case Syswaitpid:
		cpu.Eax = uint32(syswaitpid(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Syslseek:
		cpu.Eax = uint32(syslseek(int32(cpu.Ebx), int32(cpu.Ecx), cpu.Edx))
		return esp
	case Sysexecve:
		cpu.Eax = uint32(sysexecve(cpu, cpu.Ebx))
		return esp
	case Sysgetpid:
		cpu.Eax = SystemzeitProzesskennung()
		return esp
	case Sysgetppid:
		cpu.Eax = SystemzeitElternelementProzesskennung()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Syszugreifen:
		cpu.Eax = uint32(syszugreifen(cpu.Ebx, cpu.Ecx))
		return esp
	case Syschdir:
		cpu.Eax = uint32(syschdir(cpu.Ebx))
		return esp
	case Sysgetcwd:
		cpu.Eax = uint32(sysgetcwd(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysdup:
		cpu.Eax = uint32(sysdup(int32(cpu.Ebx), 0))
		return esp
	case Sysdup2:
		cpu.Eax = uint32(sysdup2(int32(cpu.Ebx), int32(cpu.Ecx)))
		return esp
	case Syssocketcall:
		cpu.Eax = uint32(sysNetzanschlussAufruf(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysfcntl:
		cpu.Eax = uint32(sysfcntl(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysstat, Syslstat:
		cpu.Eax = uint32(sysstat(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysfstat:
		cpu.Eax = uint32(sysfstat(int32(cpu.Ebx), cpu.Ecx))
		return esp
	case Sysfsync:
		cpu.Eax = uint32(sysfsync(int32(cpu.Ebx)))
		return esp
	case Syssync:
		cpu.Eax = 0
		return esp
	case Sysuname:
		cpu.Eax = uint32(sysuname(cpu.Ebx))
		return esp
	case Sysbrk:
		cpu.Eax = sysbrk(cpu.Ebx)
		return esp
	case 9:
		konsole_2.MUnsignedinteger32Drucken(cpu.Ebx)
		return esp

	default:
		konsole_2.MDruckenxy(([]byte)("sys["), 1, 23)
		konsole_2.MUnsignedinteger32Drucken(esp)
		konsole_2.MDrucken(([]byte)(":"))
		konsole_2.MUnsignedinteger32Drucken(cpu.Eax)
		konsole_2.MDrucken(([]byte)(":"))
		konsole_2.MUnsignedinteger32Drucken(cpu.Ebx)
		konsole_2.MDrucken(([]byte)(":"))
		konsole_2.MUnsignedinteger32Drucken(cpu.Ecx)
		konsole_2.MDrucken(([]byte)(":"))
		konsole_2.MUnsignedinteger32Drucken(cpu.Edx)
		konsole_2.MDrucken(([]byte)("]"))
		cpu.Eax = syscallFehler(Enosys)
		return esp
	}

	return esp
}

func initDateidescriptor() {
	for i := 0; i < maximumÖffnenDATEIEN; i++ {
		öffnenDateiTabelle[i] = öffnenDateiBeschreibung{}
	}
	for i := 0; i < len(prozessTabelle); i++ {
		prozessTabelle[i] = prozessEintrag{}
	}
	for i := 0; i < len(lokalsockets); i++ {
		lokalsockets[i] = lokaldatagramNetzanschluss{}
	}
	weiterephemeralAnschluss = 49152
	öffnenDateiTabelle[0] = öffnenDateiBeschreibung{belegt: true, art: fdArtstdin, optionen: oLesennur}
	öffnenDateiTabelle[1] = öffnenDateiBeschreibung{belegt: true, art: fdArtKonsole, optionen: oSchreibennur}
	öffnenDateiTabelle[2] = öffnenDateiBeschreibung{belegt: true, art: fdArtKonsole, optionen: oSchreibennur}
}

func suchenProzess(prozesskennung uint32) *prozessEintrag {
	for i := 0; i < len(prozessTabelle); i++ {
		if prozessTabelle[i].belegt && prozessTabelle[i].prozesskennung == prozesskennung {
			return &prozessTabelle[i]
		}
	}
	return nil
}

func initializeProzessfds(prozess *prozessEintrag) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		prozess.fds[fd] = fdEintrag{belegt: true, beschreibung: fd}
		öffnenDateiTabelle[fd].refs++
	}
}

func ensureSystemzeitProzess() *prozessEintrag {
	prozesskennung := SystemzeitProzesskennung()
	if prozess := suchenProzess(prozesskennung); prozess != nil {
		return prozess
	}
	for i := 0; i < len(prozessTabelle); i++ {
		if !prozessTabelle[i].belegt {
			prozessTabelle[i] = prozessEintrag{
				belegt:		true,
				prozesskennung:	prozesskennung,
				elternelement:	SystemzeitElternelementProzesskennung(),
				programmbreak:	benutzerheapbase,
			}
			initializeProzessfds(&prozessTabelle[i])
			return &prozessTabelle[i]
		}
	}
	return nil
}

func getÖffnenDateifor(prozess *prozessEintrag, fd int32) *öffnenDateiBeschreibung {
	if prozess == nil || fd < 0 || fd >= maximumfd || !prozess.fds[fd].belegt {
		return nil
	}
	beschreibung := prozess.fds[fd].beschreibung
	if beschreibung < 0 || beschreibung >= maximumÖffnenDATEIEN || !öffnenDateiTabelle[beschreibung].belegt {
		return nil
	}
	return &öffnenDateiTabelle[beschreibung]
}

func getÖffnenDatei(fd int32) *öffnenDateiBeschreibung {
	return getÖffnenDateifor(ensureSystemzeitProzess(), fd)
}

func allocateÖffnenDatei() int32 {
	for i := int32(3); i < maximumÖffnenDATEIEN; i++ {
		if !öffnenDateiTabelle[i].belegt {
			öffnenDateiTabelle[i] = öffnenDateiBeschreibung{belegt: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(prozess *prozessEintrag, beschreibung int32, minimum int32) int32 {
	if prozess == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maximumfd {
		return Einval
	}
	for fd := minimum; fd < maximumfd; fd++ {
		if !prozess.fds[fd].belegt {
			prozess.fds[fd] = fdEintrag{belegt: true, beschreibung: beschreibung}
			return fd
		}
	}
	return Emfile
}

func releaseÖffnenDatei(beschreibung int32) {
	if beschreibung < 0 || beschreibung >= maximumÖffnenDATEIEN {
		return
	}
	eintrag := &öffnenDateiTabelle[beschreibung]
	if eintrag.refs > 0 {
		eintrag.refs--
	}

	if eintrag.refs == 0 && beschreibung > stderrfd {
		if eintrag.art == fdArtNetzanschluss && eintrag.aux < maximumsockets {
			lokalsockets[eintrag.aux] = lokaldatagramNetzanschluss{}
		}
		*eintrag = öffnenDateiBeschreibung{}
	}
}

func schließenProzessfd(prozess *prozessEintrag, fd int32) int32 {
	if prozess == nil || getÖffnenDateifor(prozess, fd) == nil {
		return Ebadf
	}
	beschreibung := prozess.fds[fd].beschreibung
	prozess.fds[fd] = fdEintrag{}
	releaseÖffnenDatei(beschreibung)
	return 0
}

func sysSchreiben(fd int32, address uint32, anzahl uint32) int32 {
	if anzahl == 0 {
		return 0
	}
	if address == 0 || address+anzahl < address {
		return Efault
	}
	if anzahl > 4096 {
		return Einval
	}
	eintrag := getÖffnenDatei(fd)
	if eintrag == nil {
		return Ebadf
	}
	if eintrag.art != fdArtKonsole {
		if eintrag.art == fdArtNetzanschluss {
			return netzanschlussSendento(fd, address, anzahl, 0, 0)
		}
		if eintrag.art == fdArtfat || eintrag.art == fdArtBasisordnerOrdner {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytevonZeiger(uintptr(address), int(anzahl), int(anzahl))
	konsole_2.MDrucken(buffer)
	return int32(anzahl)
}

func sysLesen(fd int32, address uint32, anzahl uint32) int32 {
	if anzahl == 0 {
		return 0
	}
	if address == 0 || address+anzahl < address {
		return Efault
	}
	eintrag := getÖffnenDatei(fd)
	if eintrag == nil {
		return Ebadf
	}
	if eintrag.art == fdArtstdin {
		return lesenstdin(address, anzahl)
	}
	if eintrag.art == fdArtBasisordnerOrdner {
		return Eisdir
	}
	if eintrag.art == fdArtNetzanschluss {
		return netzanschlussreceivevon(fd, address, anzahl, 0, 0)
	}
	if eintrag.art != fdArtfat {
		return Ebadf
	}
	if eintrag.position >= eintrag.größe {
		return 0
	}
	remaining := eintrag.größe - eintrag.position
	if anzahl > remaining {
		anzahl = remaining
	}
	buffer := GetBytevonZeiger(uintptr(address), int(anzahl), int(anzahl))
	return lesenvfsDatei(eintrag, buffer, anzahl)
}

func sysÖffnen(pFADaddress uint32, optionen uint32, modus uint32) int32 {
	_ = modus
	if pFADaddress == 0 {
		return Efault
	}
	zugreifenModus := optionen & 3
	if zugreifenModus == oSchreibennur || zugreifenModus == oLesenSchreiben || (optionen&(oErstellen|oWertabschneiden|oappend)) != 0 {
		return Erofs
	}

	prozess := ensureSystemzeitProzess()
	if prozess == nil {
		return Enfile
	}
	beschreibung := allocateÖffnenDatei()
	if beschreibung < 0 {
		return beschreibung
	}
	eintrag := &öffnenDateiTabelle[beschreibung]
	eintrag.optionen = optionen
	if isBasisordnerPFAD(pFADaddress) {
		eintrag.art = fdArtBasisordnerOrdner
		eintrag.größe = 0
	} else {
		elementnamelen, elementname := kopierenPFAD(pFADaddress)
		if elementnamelen == 0 {
			*eintrag = öffnenDateiBeschreibung{}
			return Enoent
		}
		größe := dateiGröße(elementname[:elementnamelen])
		if größe == 0 {
			*eintrag = öffnenDateiBeschreibung{}
			return Enoent
		}
		if (optionen & oOrdner) != 0 {
			*eintrag = öffnenDateiBeschreibung{}
			return Enotdir
		}
		eintrag.art = fdArtfat
		eintrag.größe = größe
		eintrag.elementnamelen = elementnamelen
		eintrag.elementname = elementname
	}

	fd := allocatefd(prozess, beschreibung, 3)
	if fd < 0 {
		*eintrag = öffnenDateiBeschreibung{}
		return fd
	}
	return fd
}

func sysSchließen(fd int32) int32 {
	return schließenProzessfd(ensureSystemzeitProzess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	prozess := ensureSystemzeitProzess()
	eintrag := getÖffnenDateifor(prozess, fd)
	if eintrag == nil {
		return Ebadf
	}
	neufd := allocatefd(prozess, prozess.fds[fd].beschreibung, minimum)
	if neufd >= 0 {
		eintrag.refs++
	}
	return neufd
}

func sysdup2(altfd int32, neufd int32) int32 {
	prozess := ensureSystemzeitProzess()
	eintrag := getÖffnenDateifor(prozess, altfd)
	if eintrag == nil {
		return Ebadf
	}
	if neufd < 0 || neufd >= maximumfd {
		return Ebadf
	}
	if altfd == neufd {
		return neufd
	}
	if prozess.fds[neufd].belegt {
		schließenProzessfd(prozess, neufd)
	}
	prozess.fds[neufd] = fdEintrag{belegt: true, beschreibung: prozess.fds[altfd].beschreibung}
	eintrag.refs++
	return neufd
}

func sysfcntl(fd int32, befehl uint32, argument uint32) int32 {
	prozess := ensureSystemzeitProzess()
	eintrag := getÖffnenDateifor(prozess, fd)
	if eintrag == nil {
		return Ebadf
	}
	switch befehl {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(prozess.fds[fd].fdOptionen)
	case fSetzenfd:
		prozess.fds[fd].fdOptionen = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(eintrag.optionen)
	case fSetzenfl:
		eintrag.optionen = (eintrag.optionen & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, versatz int32, whence uint32) int32 {
	eintrag := getÖffnenDatei(fd)
	if eintrag == nil {
		return Ebadf
	}
	if eintrag.art != fdArtfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekSetzen:
		base = 0
	case seekSystemzeit:
		base = int64(eintrag.position)
	case seekEnde:
		base = int64(eintrag.größe)
	default:
		return Einval
	}
	position_2 := base + int64(versatz)
	if position_2 < 0 || position_2 > 0x7FFFFFFF {
		return Einval
	}
	eintrag.position = uint32(position_2)
	return int32(eintrag.position)
}

func lesenvfsDatei(eintrag *öffnenDateiBeschreibung, ziel_2 []byte, anzahl uint32) int32 {
	speicherVerwalter := &mem.TSpeicherVerwalter{}
	tmpZeiger := speicherVerwalter.Speicher_reservieren(eintrag.größe)
	if tmpZeiger == nil {
		return Einval
	}
	tmp := GetBytevonZeiger(uintptr(tmpZeiger), int(eintrag.größe), int(eintrag.größe))
	lesenDatei(eintrag.elementname[:eintrag.elementnamelen], tmp)
	copy(ziel_2[:anzahl], tmp[eintrag.position:eintrag.position+anzahl])
	eintrag.position += anzahl
	speicherVerwalter.Frei(tmpZeiger)
	return int32(anzahl)
}

func isBasisordnerPFAD(pFADaddress uint32) bool {
	if pFADaddress == 0 {
		return false
	}
	pFAD := GetBytevonZeiger(uintptr(pFADaddress), 4, 4)
	if pFAD[0] == '/' && pFAD[1] == 0 {
		return true
	}
	if pFAD[0] == '.' && pFAD[1] == 0 {
		return true
	}
	if pFAD[0] == '/' && pFAD[1] == '.' && pFAD[2] == 0 {
		return true
	}
	return false
}

func syszugreifen(pFADaddress uint32, modus uint32) int32 {
	if pFADaddress == 0 {
		return Efault
	}
	if (modus & ^uint32(7)) != 0 {
		return Einval
	}
	isBasisordner := isBasisordnerPFAD(pFADaddress)
	exists := isBasisordner
	if !exists {
		elementnamelen, elementname := kopierenPFAD(pFADaddress)
		exists = elementnamelen != 0 && dateiGröße(elementname[:elementnamelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (modus & 2) != 0 {
		return Eacces
	}

	if (modus&1) != 0 && !isBasisordner {
		return Eacces
	}
	return 0
}

func syschdir(pFADaddress uint32) int32 {
	if pFADaddress == 0 {
		return Efault
	}
	if !isBasisordnerPFAD(pFADaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, größe uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if größe < 2 {
		return Erange
	}
	buffer_2 := GetBytevonZeiger(uintptr(bufferaddress), int(größe), int(größe))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, modus uint32, größe uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Gerät = 1
	stat.Ino = inode
	stat.Modus = modus
	stat.Nlink = 1
	stat.Größe_2 = int32(größe)
	stat.Blksize = 512
	stat.Rechteck = int32((größe + 511) / 512)
	return 0
}

func sysstat(pFADaddress uint32, stataddress uint32) int32 {
	if pFADaddress == 0 {
		return Efault
	}
	if isBasisordnerPFAD(pFADaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	elementnamelen, elementname := kopierenPFAD(pFADaddress)
	if elementnamelen == 0 {
		return Enoent
	}
	größe := dateiGröße(elementname[:elementnamelen])
	if größe == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < elementnamelen; i++ {
		inode = inode*33 + uint32(elementname[i])
	}
	return fillposixstat(stataddress, sifreg|0444, größe, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	eintrag := getÖffnenDatei(fd)
	if eintrag == nil {
		return Ebadf
	}
	switch eintrag.art {
	case fdArtstdin, fdArtKonsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdArtBasisordnerOrdner:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdArtfat:
		return fillposixstat(stataddress, sifreg|0444, eintrag.größe, uint32(fd+2))
	case fdArtNetzanschluss:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getÖffnenDatei(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	prozess := ensureSystemzeitProzess()
	if prozess == nil {
		return 0
	}
	if prozess.programmbreak == 0 {
		prozess.programmbreak = benutzerheapbase
	}
	if address_2 == 0 {
		return prozess.programmbreak
	}
	if address_2 < benutzerheapbase || address_2 > benutzerheapBeschränkung {
		return prozess.programmbreak
	}
	prozess.programmbreak = address_2
	return prozess.programmbreak
}

func kopierenutsFeld(ziel *[65]byte, wert string) {
	beschränkung := len(wert)
	if beschränkung > 64 {
		beschränkung = 64
	}
	for i := 0; i < beschränkung; i++ {
		ziel[i] = wert[i]
	}
	ziel[beschränkung] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	elementname := (*posixutsname)(Pointer(uintptr(address_2)))
	*elementname = posixutsname{}
	kopierenutsFeld(&elementname.Sysname, "EngOS")
	kopierenutsFeld(&elementname.Nodename, "engos")
	kopierenutsFeld(&elementname.Release, "0.1-posix")
	kopierenutsFeld(&elementname.Version, "POSIX.1-2017 phase 1")
	kopierenutsFeld(&elementname.Machine, "i386")
	return 0
}

func auslagerungsspeicherunsignedinteger16(wert uint16) uint16 {
	return (wert << 8) | (wert >> 8)
}

func netzanschlussAufrufargument(argumente_2 uint32, inhalt uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumente_2 + inhalt*4)))
}

func netzanschlussforfd(fd int32) (*lokaldatagramNetzanschluss, int32) {
	eintrag := getÖffnenDatei(fd)
	if eintrag == nil || eintrag.art != fdArtNetzanschluss || eintrag.aux >= maximumsockets {
		return nil, Ebadf
	}
	netzanschluss := &lokalsockets[eintrag.aux]
	if !netzanschluss.belegt {
		return nil, Ebadf
	}
	return netzanschluss, 0
}

func allocateNetzanschluss(domäne uint32, netzanschlussTyp uint32, protocol uint32) int32 {
	if domäne != afinet {
		return Eafnosupport
	}
	if netzanschlussTyp != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	prozess := ensureSystemzeitProzess()
	if prozess == nil {
		return Enfile
	}
	netzanschlussInhalt := -1
	for i := 0; i < maximumsockets; i++ {
		if !lokalsockets[i].belegt {
			netzanschlussInhalt = i
			break
		}
	}
	if netzanschlussInhalt < 0 {
		return Enfile
	}
	beschreibung := allocateÖffnenDatei()
	if beschreibung < 0 {
		return beschreibung
	}
	lokalsockets[netzanschlussInhalt] = lokaldatagramNetzanschluss{belegt: true}
	eintrag := &öffnenDateiTabelle[beschreibung]
	eintrag.art = fdArtNetzanschluss
	eintrag.optionen = oLesenSchreiben
	eintrag.aux = uint32(netzanschlussInhalt)
	fd := allocatefd(prozess, beschreibung, 3)
	if fd < 0 {
		lokalsockets[netzanschlussInhalt] = lokaldatagramNetzanschluss{}
		*eintrag = öffnenDateiBeschreibung{}
		return fd
	}
	return fd
}

func netzanschlussaddress(address_2 uint32, länge uint32) (*netzanschlussaddressiBw4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if länge < 16 {
		return nil, Einval
	}
	ergebnis := (*netzanschlussaddressiBw4)(Pointer(uintptr(address_2)))
	if ergebnis.Family != afinet {
		return nil, Eafnosupport
	}
	return ergebnis, 0
}

func anschlussEinVerwenden(anschluss uint16, except *lokaldatagramNetzanschluss) bool {
	for i := 0; i < maximumsockets; i++ {
		netzanschluss := &lokalsockets[i]
		if netzanschluss != except && netzanschluss.belegt && netzanschluss.bound && netzanschluss.lokal.Anschluss == anschluss {
			return true
		}
	}
	return false
}

func bindungephemeral(netzanschluss *lokaldatagramNetzanschluss) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		anschluss := auslagerungsspeicherunsignedinteger16(weiterephemeralAnschluss)
		weiterephemeralAnschluss++
		if weiterephemeralAnschluss < 49152 {
			weiterephemeralAnschluss = 49152
		}
		if !anschlussEinVerwenden(anschluss, netzanschluss) {
			netzanschluss.lokal = netzanschlussaddressiBw4{Family: afinet, Anschluss: anschluss, Address: 0x0100007F}
			netzanschluss.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func netzanschlussBindung(fd int32, address_2 uint32, länge uint32) int32 {
	netzanschluss, err := netzanschlussforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := netzanschlussaddress(address_2, länge)
	if err != 0 {
		return err
	}
	if netzanschluss.bound {
		return Einval
	}
	if requested.Anschluss == 0 {
		return bindungephemeral(netzanschluss)
	}
	if anschlussEinVerwenden(requested.Anschluss, netzanschluss) {
		return Eaddrinuse
	}
	netzanschluss.lokal = *requested
	netzanschluss.bound = true
	return 0
}

func netzanschlussVerbinden(fd int32, address_2 uint32, länge uint32) int32 {
	netzanschluss, err := netzanschlussforfd(fd)
	if err != 0 {
		return err
	}
	entfernt, err := netzanschlussaddress(address_2, länge)
	if err != 0 {
		return err
	}
	if !netzanschluss.bound {
		if err := bindungephemeral(netzanschluss); err != 0 {
			return err
		}
	}
	netzanschluss.entfernt = *entfernt
	netzanschluss.connected = true
	return 0
}

func netzanschlussSendento(fd int32, bufferaddress_2 uint32, länge uint32, zieladdress uint32, zielLänge uint32) int32 {
	netzanschluss, err := netzanschlussforfd(fd)
	if err != 0 {
		return err
	}
	if länge > maximumdatagramGröße {
		return Emsgsize
	}
	if länge != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var ziel netzanschlussaddressiBw4
	if zieladdress != 0 {
		address_2, addressFehler := netzanschlussaddress(zieladdress, zielLänge)
		if addressFehler != 0 {
			return addressFehler
		}
		ziel = *address_2
	} else {
		if !netzanschluss.connected {
			return Enotconn
		}
		ziel = netzanschluss.entfernt
	}
	if !netzanschluss.bound {
		if bindungFehler := bindungephemeral(netzanschluss); bindungFehler != 0 {
			return bindungFehler
		}
	}
	var receiver *lokaldatagramNetzanschluss
	for i := 0; i < maximumsockets; i++ {
		candidate := &lokalsockets[i]
		if candidate.belegt && candidate.bound && candidate.lokal.Anschluss == ziel.Anschluss &&
			(candidate.lokal.Address == 0 || candidate.lokal.Address == ziel.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.anzahl >= maximumNetzanschlussPakete {
		return Eagain
	}
	pAKET := &receiver.pakete[receiver.tail]
	*pAKET = netzanschlussPAKET{belegt: true, größe: länge, quelle: netzanschluss.lokal}
	if länge != 0 {
		quelle := GetBytevonZeiger(uintptr(bufferaddress_2), int(länge), int(länge))
		copy(pAKET.daten[:länge], quelle)
	}
	receiver.tail = (receiver.tail + 1) % maximumNetzanschlussPakete
	receiver.anzahl++
	return int32(länge)
}

func netzanschlussreceivevon(fd int32, bufferaddress_2 uint32, länge uint32, quelleaddress uint32, quelleLängeaddress uint32) int32 {
	netzanschluss, err := netzanschlussforfd(fd)
	if err != 0 {
		return err
	}
	if länge != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if netzanschluss.anzahl == 0 {
		return Eagain
	}
	pAKET := &netzanschluss.pakete[netzanschluss.head]
	kopierenLänge := pAKET.größe
	if kopierenLänge > länge {
		kopierenLänge = länge
	}
	if kopierenLänge != 0 {
		ziel := GetBytevonZeiger(uintptr(bufferaddress_2), int(kopierenLänge), int(kopierenLänge))
		copy(ziel, pAKET.daten[:kopierenLänge])
	}
	if quelleaddress != 0 {
		if quelleLängeaddress == 0 {
			return Efault
		}
		providedLänge := (*uint32)(Pointer(uintptr(quelleLängeaddress)))
		if *providedLänge >= 16 {
			*(*netzanschlussaddressiBw4)(Pointer(uintptr(quelleaddress))) = pAKET.quelle
		}
		*providedLänge = 16
	}
	*pAKET = netzanschlussPAKET{}
	netzanschluss.head = (netzanschluss.head + 1) % maximumNetzanschlussPakete
	netzanschluss.anzahl--
	return int32(kopierenLänge)
}

func kopierenNetzanschlussElementname(fd int32, address_2 uint32, längeaddress uint32, peer bool) int32 {
	netzanschluss, err := netzanschlussforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || längeaddress == 0 {
		return Efault
	}
	länge := (*uint32)(Pointer(uintptr(längeaddress)))
	if *länge < 16 {
		*länge = 16
		return Einval
	}
	if peer {
		if !netzanschluss.connected {
			return Enotconn
		}
		*(*netzanschlussaddressiBw4)(Pointer(uintptr(address_2))) = netzanschluss.entfernt
	} else {
		if !netzanschluss.bound {
			if bindungFehler := bindungephemeral(netzanschluss); bindungFehler != 0 {
				return bindungFehler
			}
		}
		*(*netzanschlussaddressiBw4)(Pointer(uintptr(address_2))) = netzanschluss.lokal
	}
	*länge = 16
	return 0
}

func sysNetzanschlussAufruf(aufruf uint32, argumente_2 uint32) int32 {
	if argumente_2 == 0 {
		return Efault
	}
	switch aufruf {
	case 1:
		return allocateNetzanschluss(netzanschlussAufrufargument(argumente_2, 0), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2))
	case 2:
		return netzanschlussBindung(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2))
	case 3:
		return netzanschlussVerbinden(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopierenNetzanschlussElementname(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2), false)
	case 7:
		return kopierenNetzanschlussElementname(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2), true)
	case 9:
		return netzanschlussSendento(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2), 0, 0)
	case 10:
		return netzanschlussreceivevon(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2), 0, 0)
	case 11:
		return netzanschlussSendento(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2), netzanschlussAufrufargument(argumente_2, 4), netzanschlussAufrufargument(argumente_2, 5))
	case 12:
		return netzanschlussreceivevon(int32(netzanschlussAufrufargument(argumente_2, 0)), netzanschlussAufrufargument(argumente_2, 1), netzanschlussAufrufargument(argumente_2, 2), netzanschlussAufrufargument(argumente_2, 4), netzanschlussAufrufargument(argumente_2, 5))
	case 13:
		if _, err := netzanschlussforfd(int32(netzanschlussAufrufargument(argumente_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := netzanschlussforfd(int32(netzanschlussAufrufargument(argumente_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func lesenstdin(address uint32, anzahl uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBytevonZeiger(uintptr(address), int(anzahl), int(anzahl))
	var n uint32
	for n < anzahl {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func StdinputByte(c byte) {
	weiter := (stdinSchreiben + 1) % uint32(len(stdinbuffer))
	if weiter == stdinLesen {
		return
	}
	stdinbuffer[stdinSchreiben] = c
	stdinSchreiben = weiter
}

func stdingetblocking() byte {
	for stdinLesen == stdinSchreiben {
		sc := pollTastaturscancode()
		if sc != 0 {
			StdinputByte(sc)
		}
	}
	c := stdinbuffer[stdinLesen]
	stdinLesen = (stdinLesen + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastaturscancode() byte {
	for (AnschlussLesenByte(0x64) & 0x01) == 0 {
	}
	sc := AnschlussLesenByte(0x60)
	return scancodetoByte(sc)
}

func scancodetoByte(sc uint8) byte {
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

func kopierenAusführenvector(address_2 uint32, ergebnis *ausführenvector) int32 {
	*ergebnis = ausführenvector{}
	if address_2 == 0 {
		return 0
	}
	for inhalt := uint32(0); inhalt < maximumAusführenvectorEintrag; inhalt++ {
		zeichenketteaddress := *(*uint32)(Pointer(uintptr(address_2 + inhalt*4)))
		if zeichenketteaddress == 0 {
			ergebnis.anzahl = inhalt
			return 0
		}
		terminated := false
		for länge := uint32(0); länge <= maximumAusführenZeichenketteLänge; länge++ {
			wert := *(*byte)(Pointer(uintptr(zeichenketteaddress + länge)))
			ergebnis.werte[inhalt][länge] = wert
			if wert == 0 {
				ergebnis.lengths[inhalt] = länge
				terminated = true
				break
			}
		}
		if !terminated {
			return E2Groß
		}
	}
	return E2Groß
}

func pushAusführenunsignedinteger32(stapelspeicher *uint32, wert uint32) {
	*stapelspeicher -= 4
	*(*uint32)(Pointer(uintptr(*stapelspeicher))) = wert
}

func setupAusführenstack(cpu *TcpuStatus, argumente_2 *ausführenvector, environment *ausführenvector) int32 {
	const stackByte uint32 = 4096
	if !MakeSpannweitePrivatwritable(getcr3(), BenutzerstackOben-stackByte, stackByte) {
		return Enomem
	}
	stapelspeicher := BenutzerstackOben
	var argumentpointers [maximumAusführenvectorEintrag]uint32
	var environmentpointers [maximumAusführenvectorEintrag]uint32

	for i := int(environment.anzahl) - 1; i >= 0; i-- {
		länge := environment.lengths[i] + 1
		stapelspeicher -= länge
		ziel := GetBytevonZeiger(uintptr(stapelspeicher), int(länge), int(länge))
		copy(ziel, environment.werte[i][:länge])
		environmentpointers[i] = stapelspeicher
	}
	for i := int(argumente_2.anzahl) - 1; i >= 0; i-- {
		länge := argumente_2.lengths[i] + 1
		stapelspeicher -= länge
		ziel := GetBytevonZeiger(uintptr(stapelspeicher), int(länge), int(länge))
		copy(ziel, argumente_2.werte[i][:länge])
		argumentpointers[i] = stapelspeicher
	}
	stapelspeicher &= ^uint32(3)
	pushAusführenunsignedinteger32(&stapelspeicher, 0)
	for i := int(environment.anzahl) - 1; i >= 0; i-- {
		pushAusführenunsignedinteger32(&stapelspeicher, environmentpointers[i])
	}
	pushAusführenunsignedinteger32(&stapelspeicher, 0)
	for i := int(argumente_2.anzahl) - 1; i >= 0; i-- {
		pushAusführenunsignedinteger32(&stapelspeicher, argumentpointers[i])
	}
	pushAusführenunsignedinteger32(&stapelspeicher, argumente_2.anzahl)
	cpu.Esp = stapelspeicher
	cpu.Ebp = 0
	return 0
}

func schließenbeiAusführen(prozess *prozessEintrag) {
	if prozess == nil {
		return
	}
	for fd := int32(0); fd < maximumfd; fd++ {
		if prozess.fds[fd].belegt && (prozess.fds[fd].fdOptionen&fdcloexec) != 0 {
			schließenProzessfd(prozess, fd)
		}
	}
}

func sysexecve(cpu *TcpuStatus, pFADaddress uint32) int32 {
	if pFADaddress == 0 {
		return Efault
	}
	var argumente_2 ausführenvector
	var environment ausführenvector
	if ergebnis := kopierenAusführenvector(cpu.Ecx, &argumente_2); ergebnis < 0 {
		return ergebnis
	}
	if ergebnis := kopierenAusführenvector(cpu.Edx, &environment); ergebnis < 0 {
		return ergebnis
	}
	elementnamelen, elementname := kopierenPFAD(pFADaddress)
	if elementnamelen == 0 {
		return Enoent
	}
	größe := dateiGröße(elementname[:elementnamelen])
	if größe == 0 {
		return Enoent
	}
	speicherVerwalter := &mem.TSpeicherVerwalter{}
	dateiZeiger := speicherVerwalter.Speicher_reservieren(größe)
	if dateiZeiger == nil {
		return Einval
	}
	daten := GetBytevonZeiger(uintptr(dateiZeiger), int(größe), int(größe))
	lesenDatei(elementname[:elementnamelen], daten)
	if größe < 52 || daten[0] != 0x7F || daten[1] != 'E' || daten[2] != 'L' || daten[3] != 'F' {
		speicherVerwalter.Frei(dateiZeiger)
		return Enoexec
	}
	loader := Elf{}
	eintrag := loader.GetEintrag(daten)
	loader.Parse(daten, getcr3())
	speicherVerwalter.Frei(dateiZeiger)
	if ergebnis := setupAusführenstack(cpu, &argumente_2, &environment); ergebnis < 0 {
		return ergebnis
	}
	schließenbeiAusführen(ensureSystemzeitProzess())
	cpu.Eip = eintrag
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStatus) int32 {
	elternelementProzesskennung := SystemzeitProzesskennung()
	if ensureSystemzeitProzess() == nil {
		return Enfile
	}
	prozesskennung := allocateProzess(elternelementProzesskennung)
	if prozesskennung == 0 {
		return Einval
	}
	speicherVerwalter := &mem.TSpeicherVerwalter{}
	ausführungsfadenZeiger := speicherVerwalter.Speicher_reservieren(uint32(Sizeof(TAusführungsfaden{})))
	stackZeiger := speicherVerwalter.Speicher_reservieren(AusführungsfadenstackGröße)
	kindSeiteOrdner := CloneaddressLeerzeichencow(getcr3())
	if ausführungsfadenZeiger == nil || stackZeiger == nil || kindSeiteOrdner == 0 {
		verwerfenProzess(prozesskennung)
		return Einval
	}
	kind := (*TAusführungsfaden)(ausführungsfadenZeiger)
	kind.Stack = uint32(uintptr(stackZeiger))
	kind.CpuStatus = (*TcpuStatus)(Pointer(uintptr(stackZeiger) + AusführungsfadenstackGröße - Sizeof(TcpuStatus{})))
	*kind.CpuStatus = *cpu
	kind.CpuStatus.Eax = 0
	kind.Benutzerstack_2 = cpu.Esp
	kind.BenutzerstackGröße_2 = 0
	kind.Prozesskennung = prozesskennung
	kind.ElternelementProzesskennung = elternelementProzesskennung
	kind.SeiteOrdnerEintrag = kindSeiteOrdner
	kind.AusführungsfadenStatus = Bereit
	kind.FpuVersatz = 0xffffffff
	kind.IsKern = false
	HinzufügenrunnableAusführungsfaden(kind)
	return int32(prozesskennung)
}

func sysBeenden(status uint32) {
	prozesskennung := SystemzeitProzesskennung()
	for i := 0; i < len(prozessTabelle); i++ {
		if prozessTabelle[i].belegt && prozessTabelle[i].prozesskennung == prozesskennung {
			schließenAlleProzessfds(&prozessTabelle[i])
			prozessTabelle[i].beendet = true
			prozessTabelle[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(prozesskennung int32, statusaddress uint32, optionen_2 uint32) int32 {
	if (optionen_2 & ^uint32(1)) != 0 {
		return Einval
	}
	elternelementProzesskennung := SystemzeitProzesskennung()
	foundKind := false
	for i := 0; i < len(prozessTabelle); i++ {
		p := &prozessTabelle[i]
		matches := prozesskennung == -1 || prozesskennung == 0 || p.prozesskennung == uint32(prozesskennung)
		if p.belegt && matches && p.elternelement == elternelementProzesskennung {
			foundKind = true
			if p.beendet {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				kindProzesskennung := p.prozesskennung
				*p = prozessEintrag{}
				return int32(kindProzesskennung)
			}
		}
	}
	if !foundKind {
		return Echild
	}

	if (optionen_2 & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProzess(elternelement uint32) uint32 {
	elternelementProzess := suchenProzess(elternelement)
	prozesskennung := AllocateProzesskennung()
	for i := 0; i < len(prozessTabelle); i++ {
		if !prozessTabelle[i].belegt {
			prozessTabelle[i] = prozessEintrag{
				belegt:		true,
				prozesskennung:	prozesskennung,
				elternelement:	elternelement,
				programmbreak:	benutzerheapbase,
			}
			if elternelementProzess != nil {
				prozessTabelle[i].programmbreak = elternelementProzess.programmbreak
				for fd := 0; fd < maximumfd; fd++ {
					if elternelementProzess.fds[fd].belegt {
						prozessTabelle[i].fds[fd] = elternelementProzess.fds[fd]
						beschreibung := elternelementProzess.fds[fd].beschreibung
						if beschreibung >= 0 && beschreibung < maximumÖffnenDATEIEN {
							öffnenDateiTabelle[beschreibung].refs++
						}
					}
				}
			} else {
				initializeProzessfds(&prozessTabelle[i])
			}
			return prozesskennung
		}
	}
	return 0
}

func schließenAlleProzessfds(prozess *prozessEintrag) {
	if prozess == nil {
		return
	}
	for fd := int32(0); fd < maximumfd; fd++ {
		if prozess.fds[fd].belegt {
			schließenProzessfd(prozess, fd)
		}
	}
}

func verwerfenProzess(prozesskennung uint32) {
	prozess := suchenProzess(prozesskennung)
	if prozess == nil {
		return
	}
	schließenAlleProzessfds(prozess)
	*prozess = prozessEintrag{}
}

func kopierenPFAD(pFADaddress uint32) (uint32, [12]byte) {
	var elementname [12]byte
	if pFADaddress == 0 {
		return 0, elementname
	}
	raw := GetBytevonZeiger(uintptr(pFADaddress), 64, 64)
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
		elementname[n] = c
		n++
	}
	return n, elementname
}

func dateiGröße(dateiname []byte) uint32 {
	var ata0s = TErweitertTechnikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdosPartitionTabelle{}
	partition.LesenPartition(&ata0s)

	bios := TDateisystemparameter32{}
	größe := bios.Len(&ata0s, partition.Mbr.PrimaryPartition[0], dateiname)
	ata0s.Flush()
	return größe
}

func lesenDatei(dateiname []byte, daten []byte) {
	var ata0s = TErweitertTechnikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdosPartitionTabelle{}
	partition.LesenPartition(&ata0s)

	bios := TDateisystemparameter32{}
	bios.Lesen(&ata0s, partition.Mbr.PrimaryPartition[0], dateiname, daten)
	ata0s.Flush()
}

func getcr3() uint32
