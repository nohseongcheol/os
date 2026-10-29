/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systeemcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "bestandSysteem/msdospartition"
import . "bestandSysteem/fat"
import . "bestandSysteem/uitvoerbaar_en_koppelbaar_formaat"
import mem "geheugenmanager"
import . "paging"
import . "poort"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtueelGeheugen"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysAfsluiten	uint32	= 1
	Sysfork		uint32	= 2
	SysLezen	uint32	= 3
	SysSchrijven	uint32	= 4
	SysOpenen	uint32	= 5
	SysSluiten	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Systoegang	uint32	= 33
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
	SysrtAfsluiten	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2Groot		int32	= -7
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
	stdinBB			int32	= 0
	stdoutBB		int32	= 1
	stderrBB		int32	= 2
	maxBB				= 32
	maxOpenenBestanden		= 128
)

type bBItem struct {
	gebruikt	bool
	beschrijving	int32
	bBVlaggen	uint32
}

type openenBestandBeschrijving struct {
	gebruikt	bool
	refs		uint32
	soort		uint32
	vlaggen		uint32
	positie		uint32
	grootte		uint32
	naam		[12]byte
	naamlen		uint32
	aux		uint32
}

const (
	bBSoortGeen		uint32	= 0
	bBSoortfat		uint32	= 1
	bBSoortstdin		uint32	= 2
	bBSoortconsole		uint32	= 3
	bBSoortHoofdmapMap	uint32	= 4
	bBSoortContactpunt	uint32	= 5

	oLezenonly	uint32	= 0
	oSchrijvenonly	uint32	= 1
	oLezenSchrijven	uint32	= 2
	ocreate		uint32	= 0x40
	oAfkappen	uint32	= 0x200
	oappend		uint32	= 0x400
	oMap		uint32	= 0x10000

	seekInstellen	uint32	= 0
	seekHuidig	uint32	= 1
	seekEind	uint32	= 2

	fdupBB		uint32	= 0
	fgetBB		uint32	= 1
	fInstellenBB	uint32	= 2
	fgetfl		uint32	= 3
	fInstellenfl	uint32	= 4
	bBcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet			= 2
	sockdatagram		= 2
	ipprotocoludp		= 17
	maxsockets		= 32
	maxContactpuntpakketten	= 8
	maxdatagramGrootte	= 512
)

type contactpuntaddressiHw4 struct {
	Family	uint16
	Poort	uint16
	Address	uint32
	Zero	[8]byte
}

type contactpuntPAKKET struct {
	gebruikt	bool
	grootte		uint32
	bron		contactpuntaddressiHw4
	data		[maxdatagramGrootte]byte
}

type lokaaldatagramContactpunt struct {
	gebruikt	bool
	bound		bool
	connected	bool
	lokaal		contactpuntaddressiHw4
	opafstand	contactpuntaddressiHw4
	head		uint32
	tail		uint32
	aantal		uint32
	pakketten	[maxContactpuntpakketten]contactpuntPAKKET
}

type posixstat struct {
	Apparaat	uint32
	Ino		uint32
	Modus		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Grootte_2	int32
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
	Versie		[65]byte
	Machine		[65]byte
}

const (
	maxUitvoerenvectorItem		= 16
	maxUitvoerenTekstsnoerLengte	= 63
)

type uitvoerenvector struct {
	aantal	uint32
	lengths	[maxUitvoerenvectorItem]uint32
	waarden	[maxUitvoerenvectorItem][maxUitvoerenTekstsnoerLengte + 1]byte
}

type procesItem struct {
	gebruikt	bool
	pid		uint32
	ouder		uint32
	afgesloten	bool
	status		uint32
	programmabreak	uint32
	fds		[maxBB]bBItem
}

type tekstsnoerheader struct {
	Data	uintptr
	Len	int
}

func syscallFout(fout int32) uint32 {
	return *(*uint32)(Pointer(&fout))
}

var openenBestandTabel [maxOpenenBestanden]openenBestandBeschrijving
var procesTabel [32]procesItem
var lokaalsockets [maxsockets]lokaaldatagramContactpunt
var volgendeephemeralPoort uint16 = 49152

const (
	gebruikerheapbase	uint32	= 0x06000000
	gebruikerheapBeperken	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLezen uint32
var stdinSchrijven uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysAfsluiten_2(index uint32) {
	Syscall(SysAfsluiten, index)
}

func SysLezen_2(bB uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLezen, bB, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysAfdrukkenstr(buffer string) {
	h := (*tekstsnoerheader)(Pointer(&buffer))
	Syscall(SysSchrijven, uint32(stdoutBB), uint32(h.Data), uint32(h.Len))
}

func SysAfdrukkenunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysSchrijven, uint32(stdoutBB), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOpenen_2(pAD uintptr, vlaggen uint32, modus uint32) int32 {
	return int32(Syscall(SysOpenen, uint32(pAD), vlaggen, modus))
}

func SysSluiten_2(bB uint32) int32 {
	return int32(Syscall(SysSluiten, bB))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(params ...uint32) uint32 {

	l := len(params)
	switch l {
	case 1:
		return Interrupt(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupt(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Interrupt(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Interrupt(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallFout(Enosys)
	}
}

func (zelf *TSyscall) Init(manager *TInterruptmanager) {
	initBestanddescriptor()

	interrupthandler = handgreepinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	zelf.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handgreepinterrupt(esp uint32) uint32 {
	var cpu = (*TcpuStatus)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysAfsluiten:
		sysAfsluiten(cpu.Ebx)
		return uint32(uintptr(Pointer(StoppenHuidigthread(cpu))))
	case SysrtAfsluiten:
		sysAfsluiten(cpu.Ebx)
		return uint32(uintptr(Pointer(StoppenHuidigthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLezen:
		cpu.Eax = uint32(sysLezen(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysSchrijven:
		cpu.Eax = uint32(sysSchrijven(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysOpenen:
		cpu.Eax = uint32(sysOpenen(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysOpenen(cpu.Ebx, ocreate|oSchrijvenonly|oAfkappen, cpu.Ecx))
		return esp
	case SysSluiten:
		cpu.Eax = uint32(sysSluiten(int32(cpu.Ebx)))
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
		cpu.Eax = Huidigpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Huidigouderpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Systoegang:
		cpu.Eax = uint32(systoegang(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysContactpuntcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Afdrukken(cpu.Ebx)
		return esp

	default:
		console_2.MAfdrukkenxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Afdrukken(esp)
		console_2.MAfdrukken(([]byte)(":"))
		console_2.MUnsignedinteger32Afdrukken(cpu.Eax)
		console_2.MAfdrukken(([]byte)(":"))
		console_2.MUnsignedinteger32Afdrukken(cpu.Ebx)
		console_2.MAfdrukken(([]byte)(":"))
		console_2.MUnsignedinteger32Afdrukken(cpu.Ecx)
		console_2.MAfdrukken(([]byte)(":"))
		console_2.MUnsignedinteger32Afdrukken(cpu.Edx)
		console_2.MAfdrukken(([]byte)("]"))
		cpu.Eax = syscallFout(Enosys)
		return esp
	}

	return esp
}

func initBestanddescriptor() {
	for i := 0; i < maxOpenenBestanden; i++ {
		openenBestandTabel[i] = openenBestandBeschrijving{}
	}
	for i := 0; i < len(procesTabel); i++ {
		procesTabel[i] = procesItem{}
	}
	for i := 0; i < len(lokaalsockets); i++ {
		lokaalsockets[i] = lokaaldatagramContactpunt{}
	}
	volgendeephemeralPoort = 49152
	openenBestandTabel[0] = openenBestandBeschrijving{gebruikt: true, soort: bBSoortstdin, vlaggen: oLezenonly}
	openenBestandTabel[1] = openenBestandBeschrijving{gebruikt: true, soort: bBSoortconsole, vlaggen: oSchrijvenonly}
	openenBestandTabel[2] = openenBestandBeschrijving{gebruikt: true, soort: bBSoortconsole, vlaggen: oSchrijvenonly}
}

func zoekenProces(pid uint32) *procesItem {
	for i := 0; i < len(procesTabel); i++ {
		if procesTabel[i].gebruikt && procesTabel[i].pid == pid {
			return &procesTabel[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procesItem) {
	for bB := int32(0); bB <= stderrBB; bB++ {
		proces.fds[bB] = bBItem{gebruikt: true, beschrijving: bB}
		openenBestandTabel[bB].refs++
	}
}

func ensureHuidigProces() *procesItem {
	pid := Huidigpid()
	if proces := zoekenProces(pid); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabel); i++ {
		if !procesTabel[i].gebruikt {
			procesTabel[i] = procesItem{
				gebruikt:	true,
				pid:		pid,
				ouder:		Huidigouderpid(),
				programmabreak:	gebruikerheapbase,
			}
			initializeProcesfds(&procesTabel[i])
			return &procesTabel[i]
		}
	}
	return nil
}

func getOpenenBestandfor(proces *procesItem, bB int32) *openenBestandBeschrijving {
	if proces == nil || bB < 0 || bB >= maxBB || !proces.fds[bB].gebruikt {
		return nil
	}
	beschrijving := proces.fds[bB].beschrijving
	if beschrijving < 0 || beschrijving >= maxOpenenBestanden || !openenBestandTabel[beschrijving].gebruikt {
		return nil
	}
	return &openenBestandTabel[beschrijving]
}

func getOpenenBestand(bB int32) *openenBestandBeschrijving {
	return getOpenenBestandfor(ensureHuidigProces(), bB)
}

func allocateOpenenBestand() int32 {
	for i := int32(3); i < maxOpenenBestanden; i++ {
		if !openenBestandTabel[i].gebruikt {
			openenBestandTabel[i] = openenBestandBeschrijving{gebruikt: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateBB(proces *procesItem, beschrijving int32, minimum int32) int32 {
	if proces == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxBB {
		return Einval
	}
	for bB := minimum; bB < maxBB; bB++ {
		if !proces.fds[bB].gebruikt {
			proces.fds[bB] = bBItem{gebruikt: true, beschrijving: beschrijving}
			return bB
		}
	}
	return Emfile
}

func releaseOpenenBestand(beschrijving int32) {
	if beschrijving < 0 || beschrijving >= maxOpenenBestanden {
		return
	}
	item := &openenBestandTabel[beschrijving]
	if item.refs > 0 {
		item.refs--
	}

	if item.refs == 0 && beschrijving > stderrBB {
		if item.soort == bBSoortContactpunt && item.aux < maxsockets {
			lokaalsockets[item.aux] = lokaaldatagramContactpunt{}
		}
		*item = openenBestandBeschrijving{}
	}
}

func sluitenProcesBB(proces *procesItem, bB int32) int32 {
	if proces == nil || getOpenenBestandfor(proces, bB) == nil {
		return Ebadf
	}
	beschrijving := proces.fds[bB].beschrijving
	proces.fds[bB] = bBItem{}
	releaseOpenenBestand(beschrijving)
	return 0
}

func sysSchrijven(bB int32, address uint32, aantal uint32) int32 {
	if aantal == 0 {
		return 0
	}
	if address == 0 || address+aantal < address {
		return Efault
	}
	if aantal > 4096 {
		return Einval
	}
	item := getOpenenBestand(bB)
	if item == nil {
		return Ebadf
	}
	if item.soort != bBSoortconsole {
		if item.soort == bBSoortContactpunt {
			return contactpuntVerzendennaar(bB, address, aantal, 0, 0)
		}
		if item.soort == bBSoortfat || item.soort == bBSoortHoofdmapMap {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbytesvanMuisaanwijzer(uintptr(address), int(aantal), int(aantal))
	console_2.MAfdrukken(buffer)
	return int32(aantal)
}

func sysLezen(bB int32, address uint32, aantal uint32) int32 {
	if aantal == 0 {
		return 0
	}
	if address == 0 || address+aantal < address {
		return Efault
	}
	item := getOpenenBestand(bB)
	if item == nil {
		return Ebadf
	}
	if item.soort == bBSoortstdin {
		return lezenstdin(address, aantal)
	}
	if item.soort == bBSoortHoofdmapMap {
		return Eisdir
	}
	if item.soort == bBSoortContactpunt {
		return contactpuntreceivevan(bB, address, aantal, 0, 0)
	}
	if item.soort != bBSoortfat {
		return Ebadf
	}
	if item.positie >= item.grootte {
		return 0
	}
	remaining := item.grootte - item.positie
	if aantal > remaining {
		aantal = remaining
	}
	buffer := GetbytesvanMuisaanwijzer(uintptr(address), int(aantal), int(aantal))
	return lezenvfsBestand(item, buffer, aantal)
}

func sysOpenen(pADaddress uint32, vlaggen uint32, modus uint32) int32 {
	_ = modus
	if pADaddress == 0 {
		return Efault
	}
	toegangmodus := vlaggen & 3
	if toegangmodus == oSchrijvenonly || toegangmodus == oLezenSchrijven || (vlaggen&(ocreate|oAfkappen|oappend)) != 0 {
		return Erofs
	}

	proces := ensureHuidigProces()
	if proces == nil {
		return Enfile
	}
	beschrijving := allocateOpenenBestand()
	if beschrijving < 0 {
		return beschrijving
	}
	item := &openenBestandTabel[beschrijving]
	item.vlaggen = vlaggen
	if isHoofdmapPAD(pADaddress) {
		item.soort = bBSoortHoofdmapMap
		item.grootte = 0
	} else {
		naamlen, naam := kopiërenPAD(pADaddress)
		if naamlen == 0 {
			*item = openenBestandBeschrijving{}
			return Enoent
		}
		grootte := bestandGrootte(naam[:naamlen])
		if grootte == 0 {
			*item = openenBestandBeschrijving{}
			return Enoent
		}
		if (vlaggen & oMap) != 0 {
			*item = openenBestandBeschrijving{}
			return Enotdir
		}
		item.soort = bBSoortfat
		item.grootte = grootte
		item.naamlen = naamlen
		item.naam = naam
	}

	bB := allocateBB(proces, beschrijving, 3)
	if bB < 0 {
		*item = openenBestandBeschrijving{}
		return bB
	}
	return bB
}

func sysSluiten(bB int32) int32 {
	return sluitenProcesBB(ensureHuidigProces(), bB)
}

func sysdup(bB int32, minimum int32) int32 {
	proces := ensureHuidigProces()
	item := getOpenenBestandfor(proces, bB)
	if item == nil {
		return Ebadf
	}
	nieuwBB := allocateBB(proces, proces.fds[bB].beschrijving, minimum)
	if nieuwBB >= 0 {
		item.refs++
	}
	return nieuwBB
}

func sysdup2(oudBB int32, nieuwBB int32) int32 {
	proces := ensureHuidigProces()
	item := getOpenenBestandfor(proces, oudBB)
	if item == nil {
		return Ebadf
	}
	if nieuwBB < 0 || nieuwBB >= maxBB {
		return Ebadf
	}
	if oudBB == nieuwBB {
		return nieuwBB
	}
	if proces.fds[nieuwBB].gebruikt {
		sluitenProcesBB(proces, nieuwBB)
	}
	proces.fds[nieuwBB] = bBItem{gebruikt: true, beschrijving: proces.fds[oudBB].beschrijving}
	item.refs++
	return nieuwBB
}

func sysfcntl(bB int32, opdracht uint32, argument uint32) int32 {
	proces := ensureHuidigProces()
	item := getOpenenBestandfor(proces, bB)
	if item == nil {
		return Ebadf
	}
	switch opdracht {
	case fdupBB:
		return sysdup(bB, int32(argument))
	case fgetBB:
		return int32(proces.fds[bB].bBVlaggen)
	case fInstellenBB:
		proces.fds[bB].bBVlaggen = argument & bBcloexec
		return 0
	case fgetfl:
		return int32(item.vlaggen)
	case fInstellenfl:
		item.vlaggen = (item.vlaggen & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(bB int32, verschuiving int32, whence uint32) int32 {
	item := getOpenenBestand(bB)
	if item == nil {
		return Ebadf
	}
	if item.soort != bBSoortfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekInstellen:
		base = 0
	case seekHuidig:
		base = int64(item.positie)
	case seekEind:
		base = int64(item.grootte)
	default:
		return Einval
	}
	positie_2 := base + int64(verschuiving)
	if positie_2 < 0 || positie_2 > 0x7FFFFFFF {
		return Einval
	}
	item.positie = uint32(positie_2)
	return int32(item.positie)
}

func lezenvfsBestand(item *openenBestandBeschrijving, bestemming_2 []byte, aantal uint32) int32 {
	geheugenmanager := &mem.TGeheugenmanager{}
	tmpMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(item.grootte)
	if tmpMuisaanwijzer == nil {
		return Einval
	}
	tmp := GetbytesvanMuisaanwijzer(uintptr(tmpMuisaanwijzer), int(item.grootte), int(item.grootte))
	lezenBestand(item.naam[:item.naamlen], tmp)
	copy(bestemming_2[:aantal], tmp[item.positie:item.positie+aantal])
	item.positie += aantal
	geheugenmanager.Vrij(tmpMuisaanwijzer)
	return int32(aantal)
}

func isHoofdmapPAD(pADaddress uint32) bool {
	if pADaddress == 0 {
		return false
	}
	pAD := GetbytesvanMuisaanwijzer(uintptr(pADaddress), 4, 4)
	if pAD[0] == '/' && pAD[1] == 0 {
		return true
	}
	if pAD[0] == '.' && pAD[1] == 0 {
		return true
	}
	if pAD[0] == '/' && pAD[1] == '.' && pAD[2] == 0 {
		return true
	}
	return false
}

func systoegang(pADaddress uint32, modus uint32) int32 {
	if pADaddress == 0 {
		return Efault
	}
	if (modus & ^uint32(7)) != 0 {
		return Einval
	}
	isHoofdmap := isHoofdmapPAD(pADaddress)
	exists := isHoofdmap
	if !exists {
		naamlen, naam := kopiërenPAD(pADaddress)
		exists = naamlen != 0 && bestandGrootte(naam[:naamlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (modus & 2) != 0 {
		return Eacces
	}

	if (modus&1) != 0 && !isHoofdmap {
		return Eacces
	}
	return 0
}

func syschdir(pADaddress uint32) int32 {
	if pADaddress == 0 {
		return Efault
	}
	if !isHoofdmapPAD(pADaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, grootte uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if grootte < 2 {
		return Erange
	}
	buffer_2 := GetbytesvanMuisaanwijzer(uintptr(bufferaddress), int(grootte), int(grootte))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, modus uint32, grootte uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Apparaat = 1
	stat.Ino = inode
	stat.Modus = modus
	stat.Nlink = 1
	stat.Grootte_2 = int32(grootte)
	stat.Blksize = 512
	stat.Blok = int32((grootte + 511) / 512)
	return 0
}

func sysstat(pADaddress uint32, stataddress uint32) int32 {
	if pADaddress == 0 {
		return Efault
	}
	if isHoofdmapPAD(pADaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	naamlen, naam := kopiërenPAD(pADaddress)
	if naamlen == 0 {
		return Enoent
	}
	grootte := bestandGrootte(naam[:naamlen])
	if grootte == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < naamlen; i++ {
		inode = inode*33 + uint32(naam[i])
	}
	return fillposixstat(stataddress, sifreg|0444, grootte, inode)
}

func sysfstat(bB int32, stataddress uint32) int32 {
	item := getOpenenBestand(bB)
	if item == nil {
		return Ebadf
	}
	switch item.soort {
	case bBSoortstdin, bBSoortconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(bB+1))
	case bBSoortHoofdmapMap:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case bBSoortfat:
		return fillposixstat(stataddress, sifreg|0444, item.grootte, uint32(bB+2))
	case bBSoortContactpunt:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(bB+2))
	}
	return Ebadf
}

func sysfsync(bB int32) int32 {
	if getOpenenBestand(bB) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proces := ensureHuidigProces()
	if proces == nil {
		return 0
	}
	if proces.programmabreak == 0 {
		proces.programmabreak = gebruikerheapbase
	}
	if address_2 == 0 {
		return proces.programmabreak
	}
	if address_2 < gebruikerheapbase || address_2 > gebruikerheapBeperken {
		return proces.programmabreak
	}
	proces.programmabreak = address_2
	return proces.programmabreak
}

func kopiërenutsveld(bestemming *[65]byte, waarde string) {
	beperken := len(waarde)
	if beperken > 64 {
		beperken = 64
	}
	for i := 0; i < beperken; i++ {
		bestemming[i] = waarde[i]
	}
	bestemming[beperken] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	naam := (*posixutsname)(Pointer(uintptr(address_2)))
	*naam = posixutsname{}
	kopiërenutsveld(&naam.Sysname, "EngOS")
	kopiërenutsveld(&naam.Nodename, "engos")
	kopiërenutsveld(&naam.Release, "0.1-posix")
	kopiërenutsveld(&naam.Versie, "POSIX.1-2017 phase 1")
	kopiërenutsveld(&naam.Machine, "i386")
	return 0
}

func wisselgeheugenunsignedinteger16(waarde uint16) uint16 {
	return (waarde << 8) | (waarde >> 8)
}

func contactpuntcallargument(argumenten_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenten_2 + index*4)))
}

func contactpuntforBB(bB int32) (*lokaaldatagramContactpunt, int32) {
	item := getOpenenBestand(bB)
	if item == nil || item.soort != bBSoortContactpunt || item.aux >= maxsockets {
		return nil, Ebadf
	}
	contactpunt := &lokaalsockets[item.aux]
	if !contactpunt.gebruikt {
		return nil, Ebadf
	}
	return contactpunt, 0
}

func allocateContactpunt(domein uint32, contactpuntSoort uint32, protocol uint32) int32 {
	if domein != afinet {
		return Eafnosupport
	}
	if contactpuntSoort != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureHuidigProces()
	if proces == nil {
		return Enfile
	}
	contactpuntindex := -1
	for i := 0; i < maxsockets; i++ {
		if !lokaalsockets[i].gebruikt {
			contactpuntindex = i
			break
		}
	}
	if contactpuntindex < 0 {
		return Enfile
	}
	beschrijving := allocateOpenenBestand()
	if beschrijving < 0 {
		return beschrijving
	}
	lokaalsockets[contactpuntindex] = lokaaldatagramContactpunt{gebruikt: true}
	item := &openenBestandTabel[beschrijving]
	item.soort = bBSoortContactpunt
	item.vlaggen = oLezenSchrijven
	item.aux = uint32(contactpuntindex)
	bB := allocateBB(proces, beschrijving, 3)
	if bB < 0 {
		lokaalsockets[contactpuntindex] = lokaaldatagramContactpunt{}
		*item = openenBestandBeschrijving{}
		return bB
	}
	return bB
}

func contactpuntaddress(address_2 uint32, lengte uint32) (*contactpuntaddressiHw4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if lengte < 16 {
		return nil, Einval
	}
	rESULTAAT := (*contactpuntaddressiHw4)(Pointer(uintptr(address_2)))
	if rESULTAAT.Family != afinet {
		return nil, Eafnosupport
	}
	return rESULTAAT, 0
}

func poortinGebruik(poort uint16, except *lokaaldatagramContactpunt) bool {
	for i := 0; i < maxsockets; i++ {
		contactpunt := &lokaalsockets[i]
		if contactpunt != except && contactpunt.gebruikt && contactpunt.bound && contactpunt.lokaal.Poort == poort {
			return true
		}
	}
	return false
}

func bindephemeral(contactpunt *lokaaldatagramContactpunt) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		poort := wisselgeheugenunsignedinteger16(volgendeephemeralPoort)
		volgendeephemeralPoort++
		if volgendeephemeralPoort < 49152 {
			volgendeephemeralPoort = 49152
		}
		if !poortinGebruik(poort, contactpunt) {
			contactpunt.lokaal = contactpuntaddressiHw4{Family: afinet, Poort: poort, Address: 0x0100007F}
			contactpunt.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func contactpuntbind(bB int32, address_2 uint32, lengte uint32) int32 {
	contactpunt, fout := contactpuntforBB(bB)
	if fout != 0 {
		return fout
	}
	requested, fout := contactpuntaddress(address_2, lengte)
	if fout != 0 {
		return fout
	}
	if contactpunt.bound {
		return Einval
	}
	if requested.Poort == 0 {
		return bindephemeral(contactpunt)
	}
	if poortinGebruik(requested.Poort, contactpunt) {
		return Eaddrinuse
	}
	contactpunt.lokaal = *requested
	contactpunt.bound = true
	return 0
}

func contactpuntVerbinden(bB int32, address_2 uint32, lengte uint32) int32 {
	contactpunt, fout := contactpuntforBB(bB)
	if fout != 0 {
		return fout
	}
	opafstand, fout := contactpuntaddress(address_2, lengte)
	if fout != 0 {
		return fout
	}
	if !contactpunt.bound {
		if fout := bindephemeral(contactpunt); fout != 0 {
			return fout
		}
	}
	contactpunt.opafstand = *opafstand
	contactpunt.connected = true
	return 0
}

func contactpuntVerzendennaar(bB int32, bufferaddress_2 uint32, lengte uint32, bestemmingaddress uint32, bestemmingLengte uint32) int32 {
	contactpunt, fout := contactpuntforBB(bB)
	if fout != 0 {
		return fout
	}
	if lengte > maxdatagramGrootte {
		return Emsgsize
	}
	if lengte != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var bestemming contactpuntaddressiHw4
	if bestemmingaddress != 0 {
		address_2, addressFout := contactpuntaddress(bestemmingaddress, bestemmingLengte)
		if addressFout != 0 {
			return addressFout
		}
		bestemming = *address_2
	} else {
		if !contactpunt.connected {
			return Enotconn
		}
		bestemming = contactpunt.opafstand
	}
	if !contactpunt.bound {
		if bindFout := bindephemeral(contactpunt); bindFout != 0 {
			return bindFout
		}
	}
	var receiver *lokaaldatagramContactpunt
	for i := 0; i < maxsockets; i++ {
		candidate := &lokaalsockets[i]
		if candidate.gebruikt && candidate.bound && candidate.lokaal.Poort == bestemming.Poort &&
			(candidate.lokaal.Address == 0 || candidate.lokaal.Address == bestemming.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.aantal >= maxContactpuntpakketten {
		return Eagain
	}
	pAKKET := &receiver.pakketten[receiver.tail]
	*pAKKET = contactpuntPAKKET{gebruikt: true, grootte: lengte, bron: contactpunt.lokaal}
	if lengte != 0 {
		bron := GetbytesvanMuisaanwijzer(uintptr(bufferaddress_2), int(lengte), int(lengte))
		copy(pAKKET.data[:lengte], bron)
	}
	receiver.tail = (receiver.tail + 1) % maxContactpuntpakketten
	receiver.aantal++
	return int32(lengte)
}

func contactpuntreceivevan(bB int32, bufferaddress_2 uint32, lengte uint32, bronaddress uint32, bronLengteaddress uint32) int32 {
	contactpunt, fout := contactpuntforBB(bB)
	if fout != 0 {
		return fout
	}
	if lengte != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if contactpunt.aantal == 0 {
		return Eagain
	}
	pAKKET := &contactpunt.pakketten[contactpunt.head]
	kopiërenLengte := pAKKET.grootte
	if kopiërenLengte > lengte {
		kopiërenLengte = lengte
	}
	if kopiërenLengte != 0 {
		bestemming := GetbytesvanMuisaanwijzer(uintptr(bufferaddress_2), int(kopiërenLengte), int(kopiërenLengte))
		copy(bestemming, pAKKET.data[:kopiërenLengte])
	}
	if bronaddress != 0 {
		if bronLengteaddress == 0 {
			return Efault
		}
		providedLengte := (*uint32)(Pointer(uintptr(bronLengteaddress)))
		if *providedLengte >= 16 {
			*(*contactpuntaddressiHw4)(Pointer(uintptr(bronaddress))) = pAKKET.bron
		}
		*providedLengte = 16
	}
	*pAKKET = contactpuntPAKKET{}
	contactpunt.head = (contactpunt.head + 1) % maxContactpuntpakketten
	contactpunt.aantal--
	return int32(kopiërenLengte)
}

func kopiërenContactpuntNaam(bB int32, address_2 uint32, lengteaddress uint32, peer bool) int32 {
	contactpunt, fout := contactpuntforBB(bB)
	if fout != 0 {
		return fout
	}
	if address_2 == 0 || lengteaddress == 0 {
		return Efault
	}
	lengte := (*uint32)(Pointer(uintptr(lengteaddress)))
	if *lengte < 16 {
		*lengte = 16
		return Einval
	}
	if peer {
		if !contactpunt.connected {
			return Enotconn
		}
		*(*contactpuntaddressiHw4)(Pointer(uintptr(address_2))) = contactpunt.opafstand
	} else {
		if !contactpunt.bound {
			if bindFout := bindephemeral(contactpunt); bindFout != 0 {
				return bindFout
			}
		}
		*(*contactpuntaddressiHw4)(Pointer(uintptr(address_2))) = contactpunt.lokaal
	}
	*lengte = 16
	return 0
}

func sysContactpuntcall(call uint32, argumenten_2 uint32) int32 {
	if argumenten_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateContactpunt(contactpuntcallargument(argumenten_2, 0), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2))
	case 2:
		return contactpuntbind(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2))
	case 3:
		return contactpuntVerbinden(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopiërenContactpuntNaam(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2), false)
	case 7:
		return kopiërenContactpuntNaam(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2), true)
	case 9:
		return contactpuntVerzendennaar(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2), 0, 0)
	case 10:
		return contactpuntreceivevan(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2), 0, 0)
	case 11:
		return contactpuntVerzendennaar(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2), contactpuntcallargument(argumenten_2, 4), contactpuntcallargument(argumenten_2, 5))
	case 12:
		return contactpuntreceivevan(int32(contactpuntcallargument(argumenten_2, 0)), contactpuntcallargument(argumenten_2, 1), contactpuntcallargument(argumenten_2, 2), contactpuntcallargument(argumenten_2, 4), contactpuntcallargument(argumenten_2, 5))
	case 13:
		if _, fout := contactpuntforBB(int32(contactpuntcallargument(argumenten_2, 0))); fout != 0 {
			return fout
		}
		return 0
	case 14:
		if _, fout := contactpuntforBB(int32(contactpuntcallargument(argumenten_2, 0))); fout != 0 {
			return fout
		}
		return 0
	}
	return Eopnotsupp
}

func lezenstdin(address uint32, aantal uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetbytesvanMuisaanwijzer(uintptr(address), int(aantal), int(aantal))
	var n uint32
	for n < aantal {
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
	volgende := (stdinSchrijven + 1) % uint32(len(stdinbuffer))
	if volgende == stdinLezen {
		return
	}
	stdinbuffer[stdinSchrijven] = c
	stdinSchrijven = volgende
}

func stdingetblocking() byte {
	for stdinLezen == stdinSchrijven {
		sc := pollToetsenbordscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLezen]
	stdinLezen = (stdinLezen + 1) % uint32(len(stdinbuffer))
	return c
}

func pollToetsenbordscancode() byte {
	for (PoortLezenbyte(0x64) & 0x01) == 0 {
	}
	sc := PoortLezenbyte(0x60)
	return scancodenaarbyte(sc)
}

func scancodenaarbyte(sc uint8) byte {
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

func kopiërenUitvoerenvector(address_2 uint32, rESULTAAT *uitvoerenvector) int32 {
	*rESULTAAT = uitvoerenvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxUitvoerenvectorItem; index++ {
		tekstsnoeraddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if tekstsnoeraddress == 0 {
			rESULTAAT.aantal = index
			return 0
		}
		terminated := false
		for lengte := uint32(0); lengte <= maxUitvoerenTekstsnoerLengte; lengte++ {
			waarde := *(*byte)(Pointer(uintptr(tekstsnoeraddress + lengte)))
			rESULTAAT.waarden[index][lengte] = waarde
			if waarde == 0 {
				rESULTAAT.lengths[index] = lengte
				terminated = true
				break
			}
		}
		if !terminated {
			return E2Groot
		}
	}
	return E2Groot
}

func pushUitvoerenunsignedinteger32(stapelgeheugen *uint32, waarde uint32) {
	*stapelgeheugen -= 4
	*(*uint32)(Pointer(uintptr(*stapelgeheugen))) = waarde
}

func setupUitvoerenstack(cpu *TcpuStatus, argumenten_2 *uitvoerenvector, environment *uitvoerenvector) int32 {
	const stackbytes uint32 = 4096
	if !MakeBereikPrivéwritable(getcr3(), GebruikerstackBovenaan-stackbytes, stackbytes) {
		return Enomem
	}
	stapelgeheugen := GebruikerstackBovenaan
	var argumentpointers [maxUitvoerenvectorItem]uint32
	var environmentpointers [maxUitvoerenvectorItem]uint32

	for i := int(environment.aantal) - 1; i >= 0; i-- {
		lengte := environment.lengths[i] + 1
		stapelgeheugen -= lengte
		bestemming := GetbytesvanMuisaanwijzer(uintptr(stapelgeheugen), int(lengte), int(lengte))
		copy(bestemming, environment.waarden[i][:lengte])
		environmentpointers[i] = stapelgeheugen
	}
	for i := int(argumenten_2.aantal) - 1; i >= 0; i-- {
		lengte := argumenten_2.lengths[i] + 1
		stapelgeheugen -= lengte
		bestemming := GetbytesvanMuisaanwijzer(uintptr(stapelgeheugen), int(lengte), int(lengte))
		copy(bestemming, argumenten_2.waarden[i][:lengte])
		argumentpointers[i] = stapelgeheugen
	}
	stapelgeheugen &= ^uint32(3)
	pushUitvoerenunsignedinteger32(&stapelgeheugen, 0)
	for i := int(environment.aantal) - 1; i >= 0; i-- {
		pushUitvoerenunsignedinteger32(&stapelgeheugen, environmentpointers[i])
	}
	pushUitvoerenunsignedinteger32(&stapelgeheugen, 0)
	for i := int(argumenten_2.aantal) - 1; i >= 0; i-- {
		pushUitvoerenunsignedinteger32(&stapelgeheugen, argumentpointers[i])
	}
	pushUitvoerenunsignedinteger32(&stapelgeheugen, argumenten_2.aantal)
	cpu.Esp = stapelgeheugen
	cpu.Ebp = 0
	return 0
}

func sluitenAanUitvoeren(proces *procesItem) {
	if proces == nil {
		return
	}
	for bB := int32(0); bB < maxBB; bB++ {
		if proces.fds[bB].gebruikt && (proces.fds[bB].bBVlaggen&bBcloexec) != 0 {
			sluitenProcesBB(proces, bB)
		}
	}
}

func sysexecve(cpu *TcpuStatus, pADaddress uint32) int32 {
	if pADaddress == 0 {
		return Efault
	}
	var argumenten_2 uitvoerenvector
	var environment uitvoerenvector
	if rESULTAAT := kopiërenUitvoerenvector(cpu.Ecx, &argumenten_2); rESULTAAT < 0 {
		return rESULTAAT
	}
	if rESULTAAT := kopiërenUitvoerenvector(cpu.Edx, &environment); rESULTAAT < 0 {
		return rESULTAAT
	}
	naamlen, naam := kopiërenPAD(pADaddress)
	if naamlen == 0 {
		return Enoent
	}
	grootte := bestandGrootte(naam[:naamlen])
	if grootte == 0 {
		return Enoent
	}
	geheugenmanager := &mem.TGeheugenmanager{}
	bestandMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(grootte)
	if bestandMuisaanwijzer == nil {
		return Einval
	}
	data := GetbytesvanMuisaanwijzer(uintptr(bestandMuisaanwijzer), int(grootte), int(grootte))
	lezenBestand(naam[:naamlen], data)
	if grootte < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		geheugenmanager.Vrij(bestandMuisaanwijzer)
		return Enoexec
	}
	loader := Elf{}
	item := loader.GetItem(data)
	loader.Parse(data, getcr3())
	geheugenmanager.Vrij(bestandMuisaanwijzer)
	if rESULTAAT := setupUitvoerenstack(cpu, &argumenten_2, &environment); rESULTAAT < 0 {
		return rESULTAAT
	}
	sluitenAanUitvoeren(ensureHuidigProces())
	cpu.Eip = item
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStatus) int32 {
	ouderpid := Huidigpid()
	if ensureHuidigProces() == nil {
		return Enfile
	}
	pid := allocateProces(ouderpid)
	if pid == 0 {
		return Einval
	}
	geheugenmanager := &mem.TGeheugenmanager{}
	threadMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(uint32(Sizeof(TThread{})))
	stackMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(ThreadstackGrootte)
	kindPaginaMap := CloneaddressSpatiecow(getcr3())
	if threadMuisaanwijzer == nil || stackMuisaanwijzer == nil || kindPaginaMap == 0 {
		verwerpenProces(pid)
		return Einval
	}
	kind := (*TThread)(threadMuisaanwijzer)
	kind.Stack = uint32(uintptr(stackMuisaanwijzer))
	kind.CpuStatus = (*TcpuStatus)(Pointer(uintptr(stackMuisaanwijzer) + ThreadstackGrootte - Sizeof(TcpuStatus{})))
	*kind.CpuStatus = *cpu
	kind.CpuStatus.Eax = 0
	kind.Gebruikerstack_2 = cpu.Esp
	kind.GebruikerstackGrootte_2 = 0
	kind.Pid = pid
	kind.Ouderpid = ouderpid
	kind.PaginaMapItem = kindPaginaMap
	kind.ThreadStatus = Klaar
	kind.FpuVerschuiving = 0xffffffff
	kind.Iskernel = false
	Toevoegenrunnablethread(kind)
	return int32(pid)
}

func sysAfsluiten(status uint32) {
	pid := Huidigpid()
	for i := 0; i < len(procesTabel); i++ {
		if procesTabel[i].gebruikt && procesTabel[i].pid == pid {
			sluitenAlleProcesfds(&procesTabel[i])
			procesTabel[i].afgesloten = true
			procesTabel[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statusaddress uint32, opties uint32) int32 {
	if (opties & ^uint32(1)) != 0 {
		return Einval
	}
	ouderpid := Huidigpid()
	foundkind := false
	for i := 0; i < len(procesTabel); i++ {
		p := &procesTabel[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.gebruikt && matches && p.ouder == ouderpid {
			foundkind = true
			if p.afgesloten {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				kindpid := p.pid
				*p = procesItem{}
				return int32(kindpid)
			}
		}
	}
	if !foundkind {
		return Echild
	}

	if (opties & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(ouder uint32) uint32 {
	ouderProces := zoekenProces(ouder)
	pid := Allocatepid()
	for i := 0; i < len(procesTabel); i++ {
		if !procesTabel[i].gebruikt {
			procesTabel[i] = procesItem{
				gebruikt:	true,
				pid:		pid,
				ouder:		ouder,
				programmabreak:	gebruikerheapbase,
			}
			if ouderProces != nil {
				procesTabel[i].programmabreak = ouderProces.programmabreak
				for bB := 0; bB < maxBB; bB++ {
					if ouderProces.fds[bB].gebruikt {
						procesTabel[i].fds[bB] = ouderProces.fds[bB]
						beschrijving := ouderProces.fds[bB].beschrijving
						if beschrijving >= 0 && beschrijving < maxOpenenBestanden {
							openenBestandTabel[beschrijving].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabel[i])
			}
			return pid
		}
	}
	return 0
}

func sluitenAlleProcesfds(proces *procesItem) {
	if proces == nil {
		return
	}
	for bB := int32(0); bB < maxBB; bB++ {
		if proces.fds[bB].gebruikt {
			sluitenProcesBB(proces, bB)
		}
	}
}

func verwerpenProces(pid uint32) {
	proces := zoekenProces(pid)
	if proces == nil {
		return
	}
	sluitenAlleProcesfds(proces)
	*proces = procesItem{}
}

func kopiërenPAD(pADaddress uint32) (uint32, [12]byte) {
	var naam [12]byte
	if pADaddress == 0 {
		return 0, naam
	}
	raw := GetbytesvanMuisaanwijzer(uintptr(pADaddress), 64, 64)
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
		naam[n] = c
		n++
	}
	return n, naam
}

func bestandGrootte(bestandsnaam []byte) uint32 {
	var ata0s = TGeavanceerdTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lezenpartition(&ata0s)

	bios := TBestandssysteemparameters32{}
	grootte := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], bestandsnaam)
	ata0s.Flush()
	return grootte
}

func lezenBestand(bestandsnaam []byte, data []byte) {
	var ata0s = TGeavanceerdTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lezenpartition(&ata0s)

	bios := TBestandssysteemparameters32{}
	bios.Lezen(&ata0s, partition.Mbr.Primarypartition[0], bestandsnaam, data)
	ata0s.Flush()
}

func getcr3() uint32
