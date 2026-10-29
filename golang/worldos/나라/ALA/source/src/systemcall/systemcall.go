/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systemcall

import . "unsafe"

import . "avbrott"
import . "konsol"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "arkivsystem/msdospartition"
import . "arkivsystem/fat"
import . "arkivsystem/körbart_och_länkbart_format"
import mem "minnemanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuellMinne"

var konsol_2 = TKonsol{}

type TSyscall struct {
	TAvbrotthandler
}

const (
	SysAvsluta	uint32	= 1
	Sysfork		uint32	= 2
	SysLäs		uint32	= 3
	SysSkriv	uint32	= 4
	SysÖppna	uint32	= 5
	SysStäng	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	SysÅtkomst	uint32	= 33
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
	SysrtAvsluta	uint32	= 252

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
	stdinfd			int32	= 0
	stdoutfd		int32	= 1
	stderrfd		int32	= 2
	maximalfd			= 32
	maximalÖppnaFILER		= 128
)

type fdpost struct {
	använt		bool
	beskrivning	int32
	fdFlaggor	uint32
}

type öppnaArkivBeskrivning struct {
	använt		bool
	refs		uint32
	sort		uint32
	flaggor		uint32
	position	uint32
	storlek		uint32
	namn		[12]byte
	namnlen		uint32
	aux		uint32
}

const (
	fdSortIngen		uint32	= 0
	fdSortfat		uint32	= 1
	fdSortstdin		uint32	= 2
	fdSortKonsol		uint32	= 3
	fdSortRotKatalog	uint32	= 4
	fdSortUttag		uint32	= 5

	oLäsonly	uint32	= 0
	oSkrivonly	uint32	= 1
	oLäsSkriv	uint32	= 2
	ocreate		uint32	= 0x40
	oKortaner	uint32	= 0x200
	oappend		uint32	= 0x400
	oKatalog	uint32	= 0x10000

	seekmängd	uint32	= 0
	seekAktuell	uint32	= 1
	seekSlut	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fmängdfd	uint32	= 2
	fgetfl		uint32	= 3
	fmängdfl	uint32	= 4
	fdcloexec	uint32	= 1

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
	maximalsockets		= 32
	maximalUttagpaket	= 8
	maximaldatagramStorlek	= 512
)

type uttagAdressiNv4 struct {
	Family	uint16
	Port	uint16
	Adress	uint32
	Noll	[8]byte
}

type uttagPAKET struct {
	använt	bool
	storlek	uint32
	källa	uttagAdressiNv4
	data	[maximaldatagramStorlek]byte
}

type lokaldatagramUttag struct {
	använt		bool
	bound		bool
	connected	bool
	lokal		uttagAdressiNv4
	fjärr		uttagAdressiNv4
	head		uint32
	tail		uint32
	antal		uint32
	paket		[maximalUttagpaket]uttagPAKET
}

type posixstat struct {
	Enhet		uint32
	Ino		uint32
	LÄGE		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Storlek_2	int32
	Blksize		int32
	Block		int32
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
	maximalKörvectorpost	= 16
	maximalKörsträngLängd	= 63
)

type körvector struct {
	antal	uint32
	lengths	[maximalKörvectorpost]uint32
	värden	[maximalKörvectorpost][maximalKörsträngLängd + 1]byte
}

type processpost struct {
	använt		bool
	processid	uint32
	förälder	uint32
	avslutade	bool
	status		uint32
	programbreak	uint32
	fds		[maximalfd]fdpost
}

type strängheader struct {
	Data	uintptr
	Len	int
}

func syscallFel(fel int32) uint32 {
	return *(*uint32)(Pointer(&fel))
}

var öppnaArkivTabell [maximalÖppnaFILER]öppnaArkivBeskrivning
var processTabell [32]processpost
var lokalsockets [maximalsockets]lokaldatagramUttag
var nästaephemeralport uint16 = 49152

const (
	användareheapbase	uint32	= 0x06000000
	användareheapGräns	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLäs uint32
var stdinSkriv uint32

func Avbrott(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysAvsluta_2(index uint32) {
	Syscall(SysAvsluta, index)
}

func SysLäs_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLäs, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysSkrivutstr(buffer string) {
	h := (*strängheader)(Pointer(&buffer))
	Syscall(SysSkriv, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysSkrivutunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysSkriv, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysÖppna_2(sÖKVÄG uintptr, flaggor uint32, lÄGE uint32) int32 {
	return int32(Syscall(SysÖppna, uint32(sÖKVÄG), flaggor, lÄGE))
}

func SysStäng_2(fd uint32) int32 {
	return int32(Syscall(SysStäng, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(adress uint32) uint32 {
	return Syscall(Sysbrk, adress)
}

func Syscall(parametrar ...uint32) uint32 {

	l := len(parametrar)
	switch l {
	case 1:
		return Avbrott(parametrar[0], 0, 0, 0, 0, 0)
	case 2:
		return Avbrott(parametrar[0], parametrar[1], 0, 0, 0, 0)
	case 3:
		return Avbrott(parametrar[0], parametrar[1], parametrar[2], 0, 0, 0)
	case 4:
		return Avbrott(parametrar[0], parametrar[1], parametrar[2], parametrar[3], 0, 0)
	case 5:
		return Avbrott(parametrar[0], parametrar[1], parametrar[2], parametrar[3], parametrar[4], 0)
	case 6:
		return Avbrott(parametrar[0], parametrar[1], parametrar[2], parametrar[3], parametrar[4], parametrar[5])
	default:
		return syscallFel(Enosys)
	}
}

func (själv *TSyscall) Init(manager *TAvbrottmanager) {
	initArkivdescriptor()

	avbrotthandler = handtagAvbrott

	var adress uintptr
	adress = uintptr(Pointer(&avbrotthandler))

	själv.TAvbrotthandler.Init(0x80, uintptr(Pointer(manager)), adress)
}

var avbrotthandler func(uint32) uint32

func handtagAvbrott(esp uint32) uint32 {
	var processor = (*TcpuTillstånd)(Pointer(uintptr(esp)))

	switch processor.Eax {
	case SysAvsluta:
		sysAvsluta(processor.Ebx)
		return uint32(uintptr(Pointer(StoppaAktuellthread(processor))))
	case SysrtAvsluta:
		sysAvsluta(processor.Ebx)
		return uint32(uintptr(Pointer(StoppaAktuellthread(processor))))
	case Sysfork:
		processor.Eax = uint32(sysfork(processor))
		return esp
	case SysLäs:
		processor.Eax = uint32(sysLäs(int32(processor.Ebx), processor.Ecx, processor.Edx))
		return esp
	case SysSkriv:
		processor.Eax = uint32(sysSkriv(int32(processor.Ebx), processor.Ecx, processor.Edx))
		return esp
	case SysÖppna:
		processor.Eax = uint32(sysÖppna(processor.Ebx, processor.Ecx, processor.Edx))
		return esp
	case Syscreat:
		processor.Eax = uint32(sysÖppna(processor.Ebx, ocreate|oSkrivonly|oKortaner, processor.Ecx))
		return esp
	case SysStäng:
		processor.Eax = uint32(sysStäng(int32(processor.Ebx)))
		return esp
	case Syswaitpid:
		processor.Eax = uint32(syswaitpid(int32(processor.Ebx), processor.Ecx, processor.Edx))
		return esp
	case Syslseek:
		processor.Eax = uint32(syslseek(int32(processor.Ebx), int32(processor.Ecx), processor.Edx))
		return esp
	case Sysexecve:
		processor.Eax = uint32(sysexecve(processor, processor.Ebx))
		return esp
	case Sysgetpid:
		processor.Eax = Aktuellprocessid()
		return esp
	case Sysgetppid:
		processor.Eax = Aktuellförälderprocessid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		processor.Eax = 0
		return esp
	case SysÅtkomst:
		processor.Eax = uint32(sysÅtkomst(processor.Ebx, processor.Ecx))
		return esp
	case Syschdir:
		processor.Eax = uint32(syschdir(processor.Ebx))
		return esp
	case Sysgetcwd:
		processor.Eax = uint32(sysgetcwd(processor.Ebx, processor.Ecx))
		return esp
	case Sysdup:
		processor.Eax = uint32(sysdup(int32(processor.Ebx), 0))
		return esp
	case Sysdup2:
		processor.Eax = uint32(sysdup2(int32(processor.Ebx), int32(processor.Ecx)))
		return esp
	case Syssocketcall:
		processor.Eax = uint32(sysUttagcall(processor.Ebx, processor.Ecx))
		return esp
	case Sysfcntl:
		processor.Eax = uint32(sysfcntl(int32(processor.Ebx), processor.Ecx, processor.Edx))
		return esp
	case Sysstat, Syslstat:
		processor.Eax = uint32(sysstat(processor.Ebx, processor.Ecx))
		return esp
	case Sysfstat:
		processor.Eax = uint32(sysfstat(int32(processor.Ebx), processor.Ecx))
		return esp
	case Sysfsync:
		processor.Eax = uint32(sysfsync(int32(processor.Ebx)))
		return esp
	case Syssync:
		processor.Eax = 0
		return esp
	case Sysuname:
		processor.Eax = uint32(sysuname(processor.Ebx))
		return esp
	case Sysbrk:
		processor.Eax = sysbrk(processor.Ebx)
		return esp
	case 9:
		konsol_2.MUnsignedinteger32Skrivut(processor.Ebx)
		return esp

	default:
		konsol_2.MSkrivutxy(([]byte)("sys["), 1, 23)
		konsol_2.MUnsignedinteger32Skrivut(esp)
		konsol_2.MSkrivut(([]byte)(":"))
		konsol_2.MUnsignedinteger32Skrivut(processor.Eax)
		konsol_2.MSkrivut(([]byte)(":"))
		konsol_2.MUnsignedinteger32Skrivut(processor.Ebx)
		konsol_2.MSkrivut(([]byte)(":"))
		konsol_2.MUnsignedinteger32Skrivut(processor.Ecx)
		konsol_2.MSkrivut(([]byte)(":"))
		konsol_2.MUnsignedinteger32Skrivut(processor.Edx)
		konsol_2.MSkrivut(([]byte)("]"))
		processor.Eax = syscallFel(Enosys)
		return esp
	}

	return esp
}

func initArkivdescriptor() {
	for i := 0; i < maximalÖppnaFILER; i++ {
		öppnaArkivTabell[i] = öppnaArkivBeskrivning{}
	}
	for i := 0; i < len(processTabell); i++ {
		processTabell[i] = processpost{}
	}
	for i := 0; i < len(lokalsockets); i++ {
		lokalsockets[i] = lokaldatagramUttag{}
	}
	nästaephemeralport = 49152
	öppnaArkivTabell[0] = öppnaArkivBeskrivning{använt: true, sort: fdSortstdin, flaggor: oLäsonly}
	öppnaArkivTabell[1] = öppnaArkivBeskrivning{använt: true, sort: fdSortKonsol, flaggor: oSkrivonly}
	öppnaArkivTabell[2] = öppnaArkivBeskrivning{använt: true, sort: fdSortKonsol, flaggor: oSkrivonly}
}

func sökprocess(processid uint32) *processpost {
	for i := 0; i < len(processTabell); i++ {
		if processTabell[i].använt && processTabell[i].processid == processid {
			return &processTabell[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processpost) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdpost{använt: true, beskrivning: fd}
		öppnaArkivTabell[fd].refs++
	}
}

func ensureAktuellprocess() *processpost {
	processid := Aktuellprocessid()
	if process := sökprocess(processid); process != nil {
		return process
	}
	for i := 0; i < len(processTabell); i++ {
		if !processTabell[i].använt {
			processTabell[i] = processpost{
				använt:		true,
				processid:	processid,
				förälder:	Aktuellförälderprocessid(),
				programbreak:	användareheapbase,
			}
			initializeprocessfds(&processTabell[i])
			return &processTabell[i]
		}
	}
	return nil
}

func getÖppnaArkivfor(process *processpost, fd int32) *öppnaArkivBeskrivning {
	if process == nil || fd < 0 || fd >= maximalfd || !process.fds[fd].använt {
		return nil
	}
	beskrivning := process.fds[fd].beskrivning
	if beskrivning < 0 || beskrivning >= maximalÖppnaFILER || !öppnaArkivTabell[beskrivning].använt {
		return nil
	}
	return &öppnaArkivTabell[beskrivning]
}

func getÖppnaArkiv(fd int32) *öppnaArkivBeskrivning {
	return getÖppnaArkivfor(ensureAktuellprocess(), fd)
}

func allocateÖppnaArkiv() int32 {
	for i := int32(3); i < maximalÖppnaFILER; i++ {
		if !öppnaArkivTabell[i].använt {
			öppnaArkivTabell[i] = öppnaArkivBeskrivning{använt: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processpost, beskrivning int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maximalfd {
		return Einval
	}
	for fd := minimum; fd < maximalfd; fd++ {
		if !process.fds[fd].använt {
			process.fds[fd] = fdpost{använt: true, beskrivning: beskrivning}
			return fd
		}
	}
	return Emfile
}

func releaseÖppnaArkiv(beskrivning int32) {
	if beskrivning < 0 || beskrivning >= maximalÖppnaFILER {
		return
	}
	post := &öppnaArkivTabell[beskrivning]
	if post.refs > 0 {
		post.refs--
	}

	if post.refs == 0 && beskrivning > stderrfd {
		if post.sort == fdSortUttag && post.aux < maximalsockets {
			lokalsockets[post.aux] = lokaldatagramUttag{}
		}
		*post = öppnaArkivBeskrivning{}
	}
}

func stängprocessfd(process *processpost, fd int32) int32 {
	if process == nil || getÖppnaArkivfor(process, fd) == nil {
		return Ebadf
	}
	beskrivning := process.fds[fd].beskrivning
	process.fds[fd] = fdpost{}
	releaseÖppnaArkiv(beskrivning)
	return 0
}

func sysSkriv(fd int32, adress uint32, antal uint32) int32 {
	if antal == 0 {
		return 0
	}
	if adress == 0 || adress+antal < adress {
		return Efault
	}
	if antal > 4096 {
		return Einval
	}
	post := getÖppnaArkiv(fd)
	if post == nil {
		return Ebadf
	}
	if post.sort != fdSortKonsol {
		if post.sort == fdSortUttag {
			return uttagSkickato(fd, adress, antal, 0, 0)
		}
		if post.sort == fdSortfat || post.sort == fdSortRotKatalog {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytefromMuspekare(uintptr(adress), int(antal), int(antal))
	konsol_2.MSkrivut(buffer)
	return int32(antal)
}

func sysLäs(fd int32, adress uint32, antal uint32) int32 {
	if antal == 0 {
		return 0
	}
	if adress == 0 || adress+antal < adress {
		return Efault
	}
	post := getÖppnaArkiv(fd)
	if post == nil {
		return Ebadf
	}
	if post.sort == fdSortstdin {
		return lässtdin(adress, antal)
	}
	if post.sort == fdSortRotKatalog {
		return Eisdir
	}
	if post.sort == fdSortUttag {
		return uttagreceivefrom(fd, adress, antal, 0, 0)
	}
	if post.sort != fdSortfat {
		return Ebadf
	}
	if post.position >= post.storlek {
		return 0
	}
	remaining := post.storlek - post.position
	if antal > remaining {
		antal = remaining
	}
	buffer := GetBytefromMuspekare(uintptr(adress), int(antal), int(antal))
	return läsvfsArkiv(post, buffer, antal)
}

func sysÖppna(sÖKVÄGAdress uint32, flaggor uint32, lÄGE uint32) int32 {
	_ = lÄGE
	if sÖKVÄGAdress == 0 {
		return Efault
	}
	åtkomstLÄGE := flaggor & 3
	if åtkomstLÄGE == oSkrivonly || åtkomstLÄGE == oLäsSkriv || (flaggor&(ocreate|oKortaner|oappend)) != 0 {
		return Erofs
	}

	process := ensureAktuellprocess()
	if process == nil {
		return Enfile
	}
	beskrivning := allocateÖppnaArkiv()
	if beskrivning < 0 {
		return beskrivning
	}
	post := &öppnaArkivTabell[beskrivning]
	post.flaggor = flaggor
	if isRotSÖKVÄG(sÖKVÄGAdress) {
		post.sort = fdSortRotKatalog
		post.storlek = 0
	} else {
		namnlen, namn := kopieraSÖKVÄG(sÖKVÄGAdress)
		if namnlen == 0 {
			*post = öppnaArkivBeskrivning{}
			return Enoent
		}
		storlek := arkivStorlek(namn[:namnlen])
		if storlek == 0 {
			*post = öppnaArkivBeskrivning{}
			return Enoent
		}
		if (flaggor & oKatalog) != 0 {
			*post = öppnaArkivBeskrivning{}
			return Enotdir
		}
		post.sort = fdSortfat
		post.storlek = storlek
		post.namnlen = namnlen
		post.namn = namn
	}

	fd := allocatefd(process, beskrivning, 3)
	if fd < 0 {
		*post = öppnaArkivBeskrivning{}
		return fd
	}
	return fd
}

func sysStäng(fd int32) int32 {
	return stängprocessfd(ensureAktuellprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensureAktuellprocess()
	post := getÖppnaArkivfor(process, fd)
	if post == nil {
		return Ebadf
	}
	nyfd := allocatefd(process, process.fds[fd].beskrivning, minimum)
	if nyfd >= 0 {
		post.refs++
	}
	return nyfd
}

func sysdup2(oldfd int32, nyfd int32) int32 {
	process := ensureAktuellprocess()
	post := getÖppnaArkivfor(process, oldfd)
	if post == nil {
		return Ebadf
	}
	if nyfd < 0 || nyfd >= maximalfd {
		return Ebadf
	}
	if oldfd == nyfd {
		return nyfd
	}
	if process.fds[nyfd].använt {
		stängprocessfd(process, nyfd)
	}
	process.fds[nyfd] = fdpost{använt: true, beskrivning: process.fds[oldfd].beskrivning}
	post.refs++
	return nyfd
}

func sysfcntl(fd int32, kommando uint32, argument_2 uint32) int32 {
	process := ensureAktuellprocess()
	post := getÖppnaArkivfor(process, fd)
	if post == nil {
		return Ebadf
	}
	switch kommando {
	case fdupfd:
		return sysdup(fd, int32(argument_2))
	case fgetfd:
		return int32(process.fds[fd].fdFlaggor)
	case fmängdfd:
		process.fds[fd].fdFlaggor = argument_2 & fdcloexec
		return 0
	case fgetfl:
		return int32(post.flaggor)
	case fmängdfl:
		post.flaggor = (post.flaggor & 3) | (argument_2 & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, förskjutning int32, whence uint32) int32 {
	post := getÖppnaArkiv(fd)
	if post == nil {
		return Ebadf
	}
	if post.sort != fdSortfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekmängd:
		base = 0
	case seekAktuell:
		base = int64(post.position)
	case seekSlut:
		base = int64(post.storlek)
	default:
		return Einval
	}
	position_2 := base + int64(förskjutning)
	if position_2 < 0 || position_2 > 0x7FFFFFFF {
		return Einval
	}
	post.position = uint32(position_2)
	return int32(post.position)
}

func läsvfsArkiv(post *öppnaArkivBeskrivning, mål_2 []byte, antal uint32) int32 {
	minnemanager := &mem.TMinnemanager{}
	tmpMuspekare := minnemanager.Tilldela_minne(post.storlek)
	if tmpMuspekare == nil {
		return Einval
	}
	tmp := GetBytefromMuspekare(uintptr(tmpMuspekare), int(post.storlek), int(post.storlek))
	läsArkiv(post.namn[:post.namnlen], tmp)
	copy(mål_2[:antal], tmp[post.position:post.position+antal])
	post.position += antal
	minnemanager.Ledigt(tmpMuspekare)
	return int32(antal)
}

func isRotSÖKVÄG(sÖKVÄGAdress uint32) bool {
	if sÖKVÄGAdress == 0 {
		return false
	}
	sÖKVÄG := GetBytefromMuspekare(uintptr(sÖKVÄGAdress), 4, 4)
	if sÖKVÄG[0] == '/' && sÖKVÄG[1] == 0 {
		return true
	}
	if sÖKVÄG[0] == '.' && sÖKVÄG[1] == 0 {
		return true
	}
	if sÖKVÄG[0] == '/' && sÖKVÄG[1] == '.' && sÖKVÄG[2] == 0 {
		return true
	}
	return false
}

func sysÅtkomst(sÖKVÄGAdress uint32, lÄGE uint32) int32 {
	if sÖKVÄGAdress == 0 {
		return Efault
	}
	if (lÄGE & ^uint32(7)) != 0 {
		return Einval
	}
	isRot := isRotSÖKVÄG(sÖKVÄGAdress)
	exists := isRot
	if !exists {
		namnlen, namn := kopieraSÖKVÄG(sÖKVÄGAdress)
		exists = namnlen != 0 && arkivStorlek(namn[:namnlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (lÄGE & 2) != 0 {
		return Eacces
	}

	if (lÄGE&1) != 0 && !isRot {
		return Eacces
	}
	return 0
}

func syschdir(sÖKVÄGAdress uint32) int32 {
	if sÖKVÄGAdress == 0 {
		return Efault
	}
	if !isRotSÖKVÄG(sÖKVÄGAdress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferAdress uint32, storlek uint32) int32 {
	if bufferAdress == 0 {
		return Efault
	}
	if storlek < 2 {
		return Erange
	}
	buffer_2 := GetBytefromMuspekare(uintptr(bufferAdress), int(storlek), int(storlek))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statAdress uint32, lÄGE uint32, storlek uint32, inod uint32) int32 {
	if statAdress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statAdress)))
	*stat = posixstat{}
	stat.Enhet = 1
	stat.Ino = inod
	stat.LÄGE = lÄGE
	stat.Nlink = 1
	stat.Storlek_2 = int32(storlek)
	stat.Blksize = 512
	stat.Block = int32((storlek + 511) / 512)
	return 0
}

func sysstat(sÖKVÄGAdress uint32, statAdress uint32) int32 {
	if sÖKVÄGAdress == 0 {
		return Efault
	}
	if isRotSÖKVÄG(sÖKVÄGAdress) {
		return fillposixstat(statAdress, sifdir|0555, 0, 1)
	}
	namnlen, namn := kopieraSÖKVÄG(sÖKVÄGAdress)
	if namnlen == 0 {
		return Enoent
	}
	storlek := arkivStorlek(namn[:namnlen])
	if storlek == 0 {
		return Enoent
	}
	inod := uint32(2)
	for i := uint32(0); i < namnlen; i++ {
		inod = inod*33 + uint32(namn[i])
	}
	return fillposixstat(statAdress, sifreg|0444, storlek, inod)
}

func sysfstat(fd int32, statAdress uint32) int32 {
	post := getÖppnaArkiv(fd)
	if post == nil {
		return Ebadf
	}
	switch post.sort {
	case fdSortstdin, fdSortKonsol:
		return fillposixstat(statAdress, sifchr|0666, 0, uint32(fd+1))
	case fdSortRotKatalog:
		return fillposixstat(statAdress, sifdir|0555, 0, 1)
	case fdSortfat:
		return fillposixstat(statAdress, sifreg|0444, post.storlek, uint32(fd+2))
	case fdSortUttag:
		return fillposixstat(statAdress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getÖppnaArkiv(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(adress_2 uint32) uint32 {
	process := ensureAktuellprocess()
	if process == nil {
		return 0
	}
	if process.programbreak == 0 {
		process.programbreak = användareheapbase
	}
	if adress_2 == 0 {
		return process.programbreak
	}
	if adress_2 < användareheapbase || adress_2 > användareheapGräns {
		return process.programbreak
	}
	process.programbreak = adress_2
	return process.programbreak
}

func kopierautsfält(mål *[65]byte, värde string) {
	gräns := len(värde)
	if gräns > 64 {
		gräns = 64
	}
	for i := 0; i < gräns; i++ {
		mål[i] = värde[i]
	}
	mål[gräns] = 0
}

func sysuname(adress_2 uint32) int32 {
	if adress_2 == 0 {
		return Efault
	}
	namn := (*posixutsname)(Pointer(uintptr(adress_2)))
	*namn = posixutsname{}
	kopierautsfält(&namn.Sysname, "EngOS")
	kopierautsfält(&namn.Nodename, "engos")
	kopierautsfält(&namn.Release, "0.1-posix")
	kopierautsfält(&namn.Version, "POSIX.1-2017 phase 1")
	kopierautsfält(&namn.Machine, "i386")
	return 0
}

func växlingsutrymmeunsignedinteger16(värde uint16) uint16 {
	return (värde << 8) | (värde >> 8)
}

func uttagcallargument(argument_3 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argument_3 + index*4)))
}

func uttagforfd(fd int32) (*lokaldatagramUttag, int32) {
	post := getÖppnaArkiv(fd)
	if post == nil || post.sort != fdSortUttag || post.aux >= maximalsockets {
		return nil, Ebadf
	}
	uttag := &lokalsockets[post.aux]
	if !uttag.använt {
		return nil, Ebadf
	}
	return uttag, 0
}

func allocateUttag(domän uint32, uttagTyp uint32, protocol uint32) int32 {
	if domän != afinet {
		return Eafnosupport
	}
	if uttagTyp != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensureAktuellprocess()
	if process == nil {
		return Enfile
	}
	uttagindex := -1
	for i := 0; i < maximalsockets; i++ {
		if !lokalsockets[i].använt {
			uttagindex = i
			break
		}
	}
	if uttagindex < 0 {
		return Enfile
	}
	beskrivning := allocateÖppnaArkiv()
	if beskrivning < 0 {
		return beskrivning
	}
	lokalsockets[uttagindex] = lokaldatagramUttag{använt: true}
	post := &öppnaArkivTabell[beskrivning]
	post.sort = fdSortUttag
	post.flaggor = oLäsSkriv
	post.aux = uint32(uttagindex)
	fd := allocatefd(process, beskrivning, 3)
	if fd < 0 {
		lokalsockets[uttagindex] = lokaldatagramUttag{}
		*post = öppnaArkivBeskrivning{}
		return fd
	}
	return fd
}

func uttagAdress(adress_2 uint32, längd uint32) (*uttagAdressiNv4, int32) {
	if adress_2 == 0 {
		return nil, Efault
	}
	if längd < 16 {
		return nil, Einval
	}
	rESULTAT := (*uttagAdressiNv4)(Pointer(uintptr(adress_2)))
	if rESULTAT.Family != afinet {
		return nil, Eafnosupport
	}
	return rESULTAT, 0
}

func portiAnvänd(port uint16, except *lokaldatagramUttag) bool {
	for i := 0; i < maximalsockets; i++ {
		uttag := &lokalsockets[i]
		if uttag != except && uttag.använt && uttag.bound && uttag.lokal.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(uttag *lokaldatagramUttag) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := växlingsutrymmeunsignedinteger16(nästaephemeralport)
		nästaephemeralport++
		if nästaephemeralport < 49152 {
			nästaephemeralport = 49152
		}
		if !portiAnvänd(port, uttag) {
			uttag.lokal = uttagAdressiNv4{Family: afinet, Port: port, Adress: 0x0100007F}
			uttag.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func uttagbind(fd int32, adress_2 uint32, längd uint32) int32 {
	uttag, fel := uttagforfd(fd)
	if fel != 0 {
		return fel
	}
	requested, fel := uttagAdress(adress_2, längd)
	if fel != 0 {
		return fel
	}
	if uttag.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(uttag)
	}
	if portiAnvänd(requested.Port, uttag) {
		return Eaddrinuse
	}
	uttag.lokal = *requested
	uttag.bound = true
	return 0
}

func uttagAnslut(fd int32, adress_2 uint32, längd uint32) int32 {
	uttag, fel := uttagforfd(fd)
	if fel != 0 {
		return fel
	}
	fjärr, fel := uttagAdress(adress_2, längd)
	if fel != 0 {
		return fel
	}
	if !uttag.bound {
		if fel := bindephemeral(uttag); fel != 0 {
			return fel
		}
	}
	uttag.fjärr = *fjärr
	uttag.connected = true
	return 0
}

func uttagSkickato(fd int32, bufferAdress_2 uint32, längd uint32, målAdress uint32, målLängd uint32) int32 {
	uttag, fel := uttagforfd(fd)
	if fel != 0 {
		return fel
	}
	if längd > maximaldatagramStorlek {
		return Emsgsize
	}
	if längd != 0 && bufferAdress_2 == 0 {
		return Efault
	}
	var mål uttagAdressiNv4
	if målAdress != 0 {
		adress_2, adressFel := uttagAdress(målAdress, målLängd)
		if adressFel != 0 {
			return adressFel
		}
		mål = *adress_2
	} else {
		if !uttag.connected {
			return Enotconn
		}
		mål = uttag.fjärr
	}
	if !uttag.bound {
		if bindFel := bindephemeral(uttag); bindFel != 0 {
			return bindFel
		}
	}
	var receiver *lokaldatagramUttag
	for i := 0; i < maximalsockets; i++ {
		candidate := &lokalsockets[i]
		if candidate.använt && candidate.bound && candidate.lokal.Port == mål.Port &&
			(candidate.lokal.Adress == 0 || candidate.lokal.Adress == mål.Adress) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.antal >= maximalUttagpaket {
		return Eagain
	}
	pAKET := &receiver.paket[receiver.tail]
	*pAKET = uttagPAKET{använt: true, storlek: längd, källa: uttag.lokal}
	if längd != 0 {
		källa := GetBytefromMuspekare(uintptr(bufferAdress_2), int(längd), int(längd))
		copy(pAKET.data[:längd], källa)
	}
	receiver.tail = (receiver.tail + 1) % maximalUttagpaket
	receiver.antal++
	return int32(längd)
}

func uttagreceivefrom(fd int32, bufferAdress_2 uint32, längd uint32, källaAdress uint32, källaLängdAdress uint32) int32 {
	uttag, fel := uttagforfd(fd)
	if fel != 0 {
		return fel
	}
	if längd != 0 && bufferAdress_2 == 0 {
		return Efault
	}
	if uttag.antal == 0 {
		return Eagain
	}
	pAKET := &uttag.paket[uttag.head]
	kopieraLängd := pAKET.storlek
	if kopieraLängd > längd {
		kopieraLängd = längd
	}
	if kopieraLängd != 0 {
		mål := GetBytefromMuspekare(uintptr(bufferAdress_2), int(kopieraLängd), int(kopieraLängd))
		copy(mål, pAKET.data[:kopieraLängd])
	}
	if källaAdress != 0 {
		if källaLängdAdress == 0 {
			return Efault
		}
		providedLängd := (*uint32)(Pointer(uintptr(källaLängdAdress)))
		if *providedLängd >= 16 {
			*(*uttagAdressiNv4)(Pointer(uintptr(källaAdress))) = pAKET.källa
		}
		*providedLängd = 16
	}
	*pAKET = uttagPAKET{}
	uttag.head = (uttag.head + 1) % maximalUttagpaket
	uttag.antal--
	return int32(kopieraLängd)
}

func kopieraUttagNamn(fd int32, adress_2 uint32, längdAdress uint32, peer bool) int32 {
	uttag, fel := uttagforfd(fd)
	if fel != 0 {
		return fel
	}
	if adress_2 == 0 || längdAdress == 0 {
		return Efault
	}
	längd := (*uint32)(Pointer(uintptr(längdAdress)))
	if *längd < 16 {
		*längd = 16
		return Einval
	}
	if peer {
		if !uttag.connected {
			return Enotconn
		}
		*(*uttagAdressiNv4)(Pointer(uintptr(adress_2))) = uttag.fjärr
	} else {
		if !uttag.bound {
			if bindFel := bindephemeral(uttag); bindFel != 0 {
				return bindFel
			}
		}
		*(*uttagAdressiNv4)(Pointer(uintptr(adress_2))) = uttag.lokal
	}
	*längd = 16
	return 0
}

func sysUttagcall(call uint32, argument_3 uint32) int32 {
	if argument_3 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateUttag(uttagcallargument(argument_3, 0), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2))
	case 2:
		return uttagbind(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2))
	case 3:
		return uttagAnslut(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopieraUttagNamn(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2), false)
	case 7:
		return kopieraUttagNamn(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2), true)
	case 9:
		return uttagSkickato(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2), 0, 0)
	case 10:
		return uttagreceivefrom(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2), 0, 0)
	case 11:
		return uttagSkickato(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2), uttagcallargument(argument_3, 4), uttagcallargument(argument_3, 5))
	case 12:
		return uttagreceivefrom(int32(uttagcallargument(argument_3, 0)), uttagcallargument(argument_3, 1), uttagcallargument(argument_3, 2), uttagcallargument(argument_3, 4), uttagcallargument(argument_3, 5))
	case 13:
		if _, fel := uttagforfd(int32(uttagcallargument(argument_3, 0))); fel != 0 {
			return fel
		}
		return 0
	case 14:
		if _, fel := uttagforfd(int32(uttagcallargument(argument_3, 0))); fel != 0 {
			return fel
		}
		return 0
	}
	return Eopnotsupp
}

func lässtdin(adress uint32, antal uint32) int32 {
	if adress == 0 {
		return Einval
	}
	buffer := GetBytefromMuspekare(uintptr(adress), int(antal), int(antal))
	var n uint32
	for n < antal {
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
	nästa := (stdinSkriv + 1) % uint32(len(stdinbuffer))
	if nästa == stdinLäs {
		return
	}
	stdinbuffer[stdinSkriv] = c
	stdinSkriv = nästa
}

func stdingetblocking() byte {
	for stdinLäs == stdinSkriv {
		sc := pollTangentbordscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLäs]
	stdinLäs = (stdinLäs + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTangentbordscancode() byte {
	for (PortLäsbyte(0x64) & 0x01) == 0 {
	}
	sc := PortLäsbyte(0x60)
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

func kopieraKörvector(adress_2 uint32, rESULTAT *körvector) int32 {
	*rESULTAT = körvector{}
	if adress_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maximalKörvectorpost; index++ {
		strängAdress := *(*uint32)(Pointer(uintptr(adress_2 + index*4)))
		if strängAdress == 0 {
			rESULTAT.antal = index
			return 0
		}
		terminated := false
		for längd := uint32(0); längd <= maximalKörsträngLängd; längd++ {
			värde := *(*byte)(Pointer(uintptr(strängAdress + längd)))
			rESULTAT.värden[index][längd] = värde
			if värde == 0 {
				rESULTAT.lengths[index] = längd
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

func pushKörunsignedinteger32(stackminne *uint32, värde uint32) {
	*stackminne -= 4
	*(*uint32)(Pointer(uintptr(*stackminne))) = värde
}

func setupKörstack(processor *TcpuTillstånd, argument_3 *körvector, environment *körvector) int32 {
	const stackByte uint32 = 4096
	if !MakeIntervallPrivatwritable(getcr3(), AnvändarestackÖverst-stackByte, stackByte) {
		return Enomem
	}
	stackminne := AnvändarestackÖverst
	var argumentpointers [maximalKörvectorpost]uint32
	var environmentpointers [maximalKörvectorpost]uint32

	for i := int(environment.antal) - 1; i >= 0; i-- {
		längd := environment.lengths[i] + 1
		stackminne -= längd
		mål := GetBytefromMuspekare(uintptr(stackminne), int(längd), int(längd))
		copy(mål, environment.värden[i][:längd])
		environmentpointers[i] = stackminne
	}
	for i := int(argument_3.antal) - 1; i >= 0; i-- {
		längd := argument_3.lengths[i] + 1
		stackminne -= längd
		mål := GetBytefromMuspekare(uintptr(stackminne), int(längd), int(längd))
		copy(mål, argument_3.värden[i][:längd])
		argumentpointers[i] = stackminne
	}
	stackminne &= ^uint32(3)
	pushKörunsignedinteger32(&stackminne, 0)
	for i := int(environment.antal) - 1; i >= 0; i-- {
		pushKörunsignedinteger32(&stackminne, environmentpointers[i])
	}
	pushKörunsignedinteger32(&stackminne, 0)
	for i := int(argument_3.antal) - 1; i >= 0; i-- {
		pushKörunsignedinteger32(&stackminne, argumentpointers[i])
	}
	pushKörunsignedinteger32(&stackminne, argument_3.antal)
	processor.Esp = stackminne
	processor.Ebp = 0
	return 0
}

func stängPåKör(process *processpost) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maximalfd; fd++ {
		if process.fds[fd].använt && (process.fds[fd].fdFlaggor&fdcloexec) != 0 {
			stängprocessfd(process, fd)
		}
	}
}

func sysexecve(processor *TcpuTillstånd, sÖKVÄGAdress uint32) int32 {
	if sÖKVÄGAdress == 0 {
		return Efault
	}
	var argument_3 körvector
	var environment körvector
	if rESULTAT := kopieraKörvector(processor.Ecx, &argument_3); rESULTAT < 0 {
		return rESULTAT
	}
	if rESULTAT := kopieraKörvector(processor.Edx, &environment); rESULTAT < 0 {
		return rESULTAT
	}
	namnlen, namn := kopieraSÖKVÄG(sÖKVÄGAdress)
	if namnlen == 0 {
		return Enoent
	}
	storlek := arkivStorlek(namn[:namnlen])
	if storlek == 0 {
		return Enoent
	}
	minnemanager := &mem.TMinnemanager{}
	arkivMuspekare := minnemanager.Tilldela_minne(storlek)
	if arkivMuspekare == nil {
		return Einval
	}
	data := GetBytefromMuspekare(uintptr(arkivMuspekare), int(storlek), int(storlek))
	läsArkiv(namn[:namnlen], data)
	if storlek < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		minnemanager.Ledigt(arkivMuspekare)
		return Enoexec
	}
	loader := Elf{}
	post := loader.Getpost(data)
	loader.Parse(data, getcr3())
	minnemanager.Ledigt(arkivMuspekare)
	if rESULTAT := setupKörstack(processor, &argument_3, &environment); rESULTAT < 0 {
		return rESULTAT
	}
	stängPåKör(ensureAktuellprocess())
	processor.Eip = post
	processor.Eax = 0
	return 0
}

func sysfork(processor *TcpuTillstånd) int32 {
	förälderprocessid := Aktuellprocessid()
	if ensureAktuellprocess() == nil {
		return Enfile
	}
	processid := allocateprocess(förälderprocessid)
	if processid == 0 {
		return Einval
	}
	minnemanager := &mem.TMinnemanager{}
	threadMuspekare := minnemanager.Tilldela_minne(uint32(Sizeof(TThread{})))
	stackMuspekare := minnemanager.Tilldela_minne(ThreadstackStorlek)
	barnSidaKatalog := CloneAdressMellanslagcow(getcr3())
	if threadMuspekare == nil || stackMuspekare == nil || barnSidaKatalog == 0 {
		kastaprocess(processid)
		return Einval
	}
	barn := (*TThread)(threadMuspekare)
	barn.Stack = uint32(uintptr(stackMuspekare))
	barn.ProcessorTillstånd = (*TcpuTillstånd)(Pointer(uintptr(stackMuspekare) + ThreadstackStorlek - Sizeof(TcpuTillstånd{})))
	*barn.ProcessorTillstånd = *processor
	barn.ProcessorTillstånd.Eax = 0
	barn.Användarestack_2 = processor.Esp
	barn.AnvändarestackStorlek_2 = 0
	barn.Processid = processid
	barn.Förälderprocessid = förälderprocessid
	barn.SidaKatalogpost = barnSidaKatalog
	barn.ThreadTillstånd = Redo
	barn.FpuFörskjutning = 0xffffffff
	barn.Iskernel = false
	Läggtillrunnablethread(barn)
	return int32(processid)
}

func sysAvsluta(status uint32) {
	processid := Aktuellprocessid()
	for i := 0; i < len(processTabell); i++ {
		if processTabell[i].använt && processTabell[i].processid == processid {
			stängAllaprocessfds(&processTabell[i])
			processTabell[i].avslutade = true
			processTabell[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(processid int32, statusAdress uint32, alternativ uint32) int32 {
	if (alternativ & ^uint32(1)) != 0 {
		return Einval
	}
	förälderprocessid := Aktuellprocessid()
	foundbarn := false
	for i := 0; i < len(processTabell); i++ {
		p := &processTabell[i]
		matches := processid == -1 || processid == 0 || p.processid == uint32(processid)
		if p.använt && matches && p.förälder == förälderprocessid {
			foundbarn = true
			if p.avslutade {
				if statusAdress != 0 {
					*(*uint32)(Pointer(uintptr(statusAdress))) = p.status
				}
				barnprocessid := p.processid
				*p = processpost{}
				return int32(barnprocessid)
			}
		}
	}
	if !foundbarn {
		return Echild
	}

	if (alternativ & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocess(förälder uint32) uint32 {
	förälderprocess := sökprocess(förälder)
	processid := Allocateprocessid()
	for i := 0; i < len(processTabell); i++ {
		if !processTabell[i].använt {
			processTabell[i] = processpost{
				använt:		true,
				processid:	processid,
				förälder:	förälder,
				programbreak:	användareheapbase,
			}
			if förälderprocess != nil {
				processTabell[i].programbreak = förälderprocess.programbreak
				for fd := 0; fd < maximalfd; fd++ {
					if förälderprocess.fds[fd].använt {
						processTabell[i].fds[fd] = förälderprocess.fds[fd]
						beskrivning := förälderprocess.fds[fd].beskrivning
						if beskrivning >= 0 && beskrivning < maximalÖppnaFILER {
							öppnaArkivTabell[beskrivning].refs++
						}
					}
				}
			} else {
				initializeprocessfds(&processTabell[i])
			}
			return processid
		}
	}
	return 0
}

func stängAllaprocessfds(process *processpost) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maximalfd; fd++ {
		if process.fds[fd].använt {
			stängprocessfd(process, fd)
		}
	}
}

func kastaprocess(processid uint32) {
	process := sökprocess(processid)
	if process == nil {
		return
	}
	stängAllaprocessfds(process)
	*process = processpost{}
}

func kopieraSÖKVÄG(sÖKVÄGAdress uint32) (uint32, [12]byte) {
	var namn [12]byte
	if sÖKVÄGAdress == 0 {
		return 0, namn
	}
	raw := GetBytefromMuspekare(uintptr(sÖKVÄGAdress), 64, 64)
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
		namn[n] = c
		n++
	}
	return n, namn
}

func arkivStorlek(filnamn []byte) uint32 {
	var ata0s = TAvanceratTeknikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Läspartition(&ata0s)

	bios := TFilsystemsparametrar32{}
	storlek := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnamn)
	ata0s.Flush()
	return storlek
}

func läsArkiv(filnamn []byte, data []byte) {
	var ata0s = TAvanceratTeknikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Läspartition(&ata0s)

	bios := TFilsystemsparametrar32{}
	bios.Läs(&ata0s, partition.Mbr.Primarypartition[0], filnamn, data)
	ata0s.Flush()
}

func getcr3() uint32
