package süsteemcall

import . "unsafe"

import . "katkestus"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "failSüsteem/msdospartition"
import . "failSüsteem/fat"
import . "failSüsteem/elf"
import mem "mälumanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuaalMälu"

var console_2 = TConsole{}

type TSyscall struct {
	TKatkestushandler
}

const (
	SysVälju	uint32	= 1
	Sysfork		uint32	= 2
	SysLugemine	uint32	= 3
	SysKirjutamine	uint32	= 4
	SysAva		uint32	= 5
	SysSulge	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysligipääs	uint32	= 33
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
	SysrtVälju	uint32	= 252

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
	stdinfd		int32	= 0
	stdoutfd	int32	= 1
	stderrfd	int32	= 2
	suurimfd		= 32
	suurimAvaFAILID		= 128
)

type fdkirje struct {
	kasutuses	bool
	kirjeldus	int32
	fdLipud		uint32
}

type avaFailKirjeldus struct {
	kasutuses	bool
	refs		uint32
	liik		uint32
	lipud		uint32
	asukoht		uint32
	suurus		uint32
	nimi		[12]byte
	nimilen		uint32
	aux		uint32
}

const (
	fdLiikPuudub		uint32	= 0
	fdLiikfat		uint32	= 1
	fdLiikstdin		uint32	= 2
	fdLiikconsole		uint32	= 3
	fdLiikJuurKataloog	uint32	= 4
	fdLiikSokkel		uint32	= 5

	oLugemineonly		uint32	= 0
	oKirjutamineonly	uint32	= 1
	oLugemineKirjutamine	uint32	= 2
	ocreate			uint32	= 0x40
	oKärpimine		uint32	= 0x200
	oappend			uint32	= 0x400
	oKataloog		uint32	= 0x10000

	seekMäära	uint32	= 0
	seekKäesolev	uint32	= 1
	seekLõpp	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fMäärafd	uint32	= 2
	fgetfl		uint32	= 3
	fMäärafl	uint32	= 4
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
	suurimsockets		= 32
	suurimSokkelpaketti	= 8
	suurimdatagramSuurus	= 512
)

type sokkeladdressiNv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type sokkelpacket struct {
	kasutuses	bool
	suurus		uint32
	aLLIKAS		sokkeladdressiNv4
	data		[suurimdatagramSuurus]byte
}

type kohalikdatagramSokkel struct {
	kasutuses	bool
	bound		bool
	connected	bool
	kohalik		sokkeladdressiNv4
	võrgus		sokkeladdressiNv4
	head		uint32
	tail		uint32
	count		uint32
	paketti		[suurimSokkelpaketti]sokkelpacket
}

type posixstat struct {
	Seade		uint32
	Ino		uint32
	REŽIIM		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Suurus_2	int32
	Blksize		int32
	Kast		int32
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
	Versioon	[65]byte
	Machine		[65]byte
}

const (
	suurimKäivitaminevectorkirje	= 16
	suurimKäivitaminestringKestus	= 63
)

type käivitaminevector struct {
	count	uint32
	lengths	[suurimKäivitaminevectorkirje]uint32
	values	[suurimKäivitaminevectorkirje][suurimKäivitaminestringKestus + 1]byte
}

type protsesskirje struct {
	kasutuses	bool
	pid		uint32
	vanem		uint32
	exited		bool
	olek		uint32
	programmbreak	uint32
	fds		[suurimfd]fdkirje
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallViga(viga int32) uint32 {
	return *(*uint32)(Pointer(&viga))
}

var avaFailTabel [suurimAvaFAILID]avaFailKirjeldus
var protsessTabel [32]protsesskirje
var kohaliksockets [suurimsockets]kohalikdatagramSokkel
var järgmineephemeralport uint16 = 49152

const (
	kasutajaheapbase	uint32	= 0x06000000
	kasutajaheapPiir	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLugemine uint32
var stdinKirjutamine uint32

func Katkestus(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysVälju_2(sisukord uint32) {
	Syscall(SysVälju, sisukord)
}

func SysLugemine_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLugemine, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysPrindistr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(SysKirjutamine, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysPrindiunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysKirjutamine, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysAva_2(rADA uintptr, lipud uint32, rEŽIIM uint32) int32 {
	return int32(Syscall(SysAva, uint32(rADA), lipud, rEŽIIM))
}

func SysSulge_2(fd uint32) int32 {
	return int32(Syscall(SysSulge, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parameetrid ...uint32) uint32 {

	l := len(parameetrid)
	switch l {
	case 1:
		return Katkestus(parameetrid[0], 0, 0, 0, 0, 0)
	case 2:
		return Katkestus(parameetrid[0], parameetrid[1], 0, 0, 0, 0)
	case 3:
		return Katkestus(parameetrid[0], parameetrid[1], parameetrid[2], 0, 0, 0)
	case 4:
		return Katkestus(parameetrid[0], parameetrid[1], parameetrid[2], parameetrid[3], 0, 0)
	case 5:
		return Katkestus(parameetrid[0], parameetrid[1], parameetrid[2], parameetrid[3], parameetrid[4], 0)
	case 6:
		return Katkestus(parameetrid[0], parameetrid[1], parameetrid[2], parameetrid[3], parameetrid[4], parameetrid[5])
	default:
		return syscallViga(Enosys)
	}
}

func (ise *TSyscall) Init(manager *TKatkestusmanager) {
	initFaildescriptor()

	katkestushandler = handleKatkestus

	var address uintptr
	address = uintptr(Pointer(&katkestushandler))

	ise.TKatkestushandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var katkestushandler func(uint32) uint32

func handleKatkestus(esp uint32) uint32 {
	var protsessor = (*TcpuOlek)(Pointer(uintptr(esp)))

	switch protsessor.Eax {
	case SysVälju:
		sysVälju(protsessor.Ebx)
		return uint32(uintptr(Pointer(PeataKäesolevthread(protsessor))))
	case SysrtVälju:
		sysVälju(protsessor.Ebx)
		return uint32(uintptr(Pointer(PeataKäesolevthread(protsessor))))
	case Sysfork:
		protsessor.Eax = uint32(sysfork(protsessor))
		return esp
	case SysLugemine:
		protsessor.Eax = uint32(sysLugemine(int32(protsessor.Ebx), protsessor.Ecx, protsessor.Edx))
		return esp
	case SysKirjutamine:
		protsessor.Eax = uint32(sysKirjutamine(int32(protsessor.Ebx), protsessor.Ecx, protsessor.Edx))
		return esp
	case SysAva:
		protsessor.Eax = uint32(sysAva(protsessor.Ebx, protsessor.Ecx, protsessor.Edx))
		return esp
	case Syscreat:
		protsessor.Eax = uint32(sysAva(protsessor.Ebx, ocreate|oKirjutamineonly|oKärpimine, protsessor.Ecx))
		return esp
	case SysSulge:
		protsessor.Eax = uint32(sysSulge(int32(protsessor.Ebx)))
		return esp
	case Syswaitpid:
		protsessor.Eax = uint32(syswaitpid(int32(protsessor.Ebx), protsessor.Ecx, protsessor.Edx))
		return esp
	case Syslseek:
		protsessor.Eax = uint32(syslseek(int32(protsessor.Ebx), int32(protsessor.Ecx), protsessor.Edx))
		return esp
	case Sysexecve:
		protsessor.Eax = uint32(sysexecve(protsessor, protsessor.Ebx))
		return esp
	case Sysgetpid:
		protsessor.Eax = Käesolevpid()
		return esp
	case Sysgetppid:
		protsessor.Eax = Käesolevvanempid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		protsessor.Eax = 0
		return esp
	case Sysligipääs:
		protsessor.Eax = uint32(sysligipääs(protsessor.Ebx, protsessor.Ecx))
		return esp
	case Syschdir:
		protsessor.Eax = uint32(syschdir(protsessor.Ebx))
		return esp
	case Sysgetcwd:
		protsessor.Eax = uint32(sysgetcwd(protsessor.Ebx, protsessor.Ecx))
		return esp
	case Sysdup:
		protsessor.Eax = uint32(sysdup(int32(protsessor.Ebx), 0))
		return esp
	case Sysdup2:
		protsessor.Eax = uint32(sysdup2(int32(protsessor.Ebx), int32(protsessor.Ecx)))
		return esp
	case Syssocketcall:
		protsessor.Eax = uint32(sysSokkelcall(protsessor.Ebx, protsessor.Ecx))
		return esp
	case Sysfcntl:
		protsessor.Eax = uint32(sysfcntl(int32(protsessor.Ebx), protsessor.Ecx, protsessor.Edx))
		return esp
	case Sysstat, Syslstat:
		protsessor.Eax = uint32(sysstat(protsessor.Ebx, protsessor.Ecx))
		return esp
	case Sysfstat:
		protsessor.Eax = uint32(sysfstat(int32(protsessor.Ebx), protsessor.Ecx))
		return esp
	case Sysfsync:
		protsessor.Eax = uint32(sysfsync(int32(protsessor.Ebx)))
		return esp
	case Syssync:
		protsessor.Eax = 0
		return esp
	case Sysuname:
		protsessor.Eax = uint32(sysuname(protsessor.Ebx))
		return esp
	case Sysbrk:
		protsessor.Eax = sysbrk(protsessor.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Prindi(protsessor.Ebx)
		return esp

	default:
		console_2.MPrindixy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Prindi(esp)
		console_2.MPrindi(([]byte)(":"))
		console_2.MUnsignedinteger32Prindi(protsessor.Eax)
		console_2.MPrindi(([]byte)(":"))
		console_2.MUnsignedinteger32Prindi(protsessor.Ebx)
		console_2.MPrindi(([]byte)(":"))
		console_2.MUnsignedinteger32Prindi(protsessor.Ecx)
		console_2.MPrindi(([]byte)(":"))
		console_2.MUnsignedinteger32Prindi(protsessor.Edx)
		console_2.MPrindi(([]byte)("]"))
		protsessor.Eax = syscallViga(Enosys)
		return esp
	}

	return esp
}

func initFaildescriptor() {
	for i := 0; i < suurimAvaFAILID; i++ {
		avaFailTabel[i] = avaFailKirjeldus{}
	}
	for i := 0; i < len(protsessTabel); i++ {
		protsessTabel[i] = protsesskirje{}
	}
	for i := 0; i < len(kohaliksockets); i++ {
		kohaliksockets[i] = kohalikdatagramSokkel{}
	}
	järgmineephemeralport = 49152
	avaFailTabel[0] = avaFailKirjeldus{kasutuses: true, liik: fdLiikstdin, lipud: oLugemineonly}
	avaFailTabel[1] = avaFailKirjeldus{kasutuses: true, liik: fdLiikconsole, lipud: oKirjutamineonly}
	avaFailTabel[2] = avaFailKirjeldus{kasutuses: true, liik: fdLiikconsole, lipud: oKirjutamineonly}
}

func otsiProtsess(pid uint32) *protsesskirje {
	for i := 0; i < len(protsessTabel); i++ {
		if protsessTabel[i].kasutuses && protsessTabel[i].pid == pid {
			return &protsessTabel[i]
		}
	}
	return nil
}

func initializeProtsessfds(protsess *protsesskirje) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		protsess.fds[fd] = fdkirje{kasutuses: true, kirjeldus: fd}
		avaFailTabel[fd].refs++
	}
}

func ensureKäesolevProtsess() *protsesskirje {
	pid := Käesolevpid()
	if protsess := otsiProtsess(pid); protsess != nil {
		return protsess
	}
	for i := 0; i < len(protsessTabel); i++ {
		if !protsessTabel[i].kasutuses {
			protsessTabel[i] = protsesskirje{
				kasutuses:	true,
				pid:		pid,
				vanem:		Käesolevvanempid(),
				programmbreak:	kasutajaheapbase,
			}
			initializeProtsessfds(&protsessTabel[i])
			return &protsessTabel[i]
		}
	}
	return nil
}

func getAvaFailfor(protsess *protsesskirje, fd int32) *avaFailKirjeldus {
	if protsess == nil || fd < 0 || fd >= suurimfd || !protsess.fds[fd].kasutuses {
		return nil
	}
	kirjeldus := protsess.fds[fd].kirjeldus
	if kirjeldus < 0 || kirjeldus >= suurimAvaFAILID || !avaFailTabel[kirjeldus].kasutuses {
		return nil
	}
	return &avaFailTabel[kirjeldus]
}

func getAvaFail(fd int32) *avaFailKirjeldus {
	return getAvaFailfor(ensureKäesolevProtsess(), fd)
}

func allocateAvaFail() int32 {
	for i := int32(3); i < suurimAvaFAILID; i++ {
		if !avaFailTabel[i].kasutuses {
			avaFailTabel[i] = avaFailKirjeldus{kasutuses: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(protsess *protsesskirje, kirjeldus int32, väikseim int32) int32 {
	if protsess == nil {
		return Enfile
	}
	if väikseim < 0 || väikseim >= suurimfd {
		return Einval
	}
	for fd := väikseim; fd < suurimfd; fd++ {
		if !protsess.fds[fd].kasutuses {
			protsess.fds[fd] = fdkirje{kasutuses: true, kirjeldus: kirjeldus}
			return fd
		}
	}
	return Emfile
}

func releaseAvaFail(kirjeldus int32) {
	if kirjeldus < 0 || kirjeldus >= suurimAvaFAILID {
		return
	}
	kirje := &avaFailTabel[kirjeldus]
	if kirje.refs > 0 {
		kirje.refs--
	}

	if kirje.refs == 0 && kirjeldus > stderrfd {
		if kirje.liik == fdLiikSokkel && kirje.aux < suurimsockets {
			kohaliksockets[kirje.aux] = kohalikdatagramSokkel{}
		}
		*kirje = avaFailKirjeldus{}
	}
}

func sulgeProtsessfd(protsess *protsesskirje, fd int32) int32 {
	if protsess == nil || getAvaFailfor(protsess, fd) == nil {
		return Ebadf
	}
	kirjeldus := protsess.fds[fd].kirjeldus
	protsess.fds[fd] = fdkirje{}
	releaseAvaFail(kirjeldus)
	return 0
}

func sysKirjutamine(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	kirje := getAvaFail(fd)
	if kirje == nil {
		return Ebadf
	}
	if kirje.liik != fdLiikconsole {
		if kirje.liik == fdLiikSokkel {
			return sokkelSaadato(fd, address, count, 0, 0)
		}
		if kirje.liik == fdLiikfat || kirje.liik == fdLiikJuurKataloog {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbaitifromKursor(uintptr(address), int(count), int(count))
	console_2.MPrindi(buffer)
	return int32(count)
}

func sysLugemine(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	kirje := getAvaFail(fd)
	if kirje == nil {
		return Ebadf
	}
	if kirje.liik == fdLiikstdin {
		return lugeminestdin(address, count)
	}
	if kirje.liik == fdLiikJuurKataloog {
		return Eisdir
	}
	if kirje.liik == fdLiikSokkel {
		return sokkelreceivefrom(fd, address, count, 0, 0)
	}
	if kirje.liik != fdLiikfat {
		return Ebadf
	}
	if kirje.asukoht >= kirje.suurus {
		return 0
	}
	remaining := kirje.suurus - kirje.asukoht
	if count > remaining {
		count = remaining
	}
	buffer := GetbaitifromKursor(uintptr(address), int(count), int(count))
	return lugeminevfsFail(kirje, buffer, count)
}

func sysAva(rADAaddress uint32, lipud uint32, rEŽIIM uint32) int32 {
	_ = rEŽIIM
	if rADAaddress == 0 {
		return Efault
	}
	ligipääsREŽIIM := lipud & 3
	if ligipääsREŽIIM == oKirjutamineonly || ligipääsREŽIIM == oLugemineKirjutamine || (lipud&(ocreate|oKärpimine|oappend)) != 0 {
		return Erofs
	}

	protsess := ensureKäesolevProtsess()
	if protsess == nil {
		return Enfile
	}
	kirjeldus := allocateAvaFail()
	if kirjeldus < 0 {
		return kirjeldus
	}
	kirje := &avaFailTabel[kirjeldus]
	kirje.lipud = lipud
	if isJuurRADA(rADAaddress) {
		kirje.liik = fdLiikJuurKataloog
		kirje.suurus = 0
	} else {
		nimilen, nimi := kopeeriRADA(rADAaddress)
		if nimilen == 0 {
			*kirje = avaFailKirjeldus{}
			return Enoent
		}
		suurus := failSuurus(nimi[:nimilen])
		if suurus == 0 {
			*kirje = avaFailKirjeldus{}
			return Enoent
		}
		if (lipud & oKataloog) != 0 {
			*kirje = avaFailKirjeldus{}
			return Enotdir
		}
		kirje.liik = fdLiikfat
		kirje.suurus = suurus
		kirje.nimilen = nimilen
		kirje.nimi = nimi
	}

	fd := allocatefd(protsess, kirjeldus, 3)
	if fd < 0 {
		*kirje = avaFailKirjeldus{}
		return fd
	}
	return fd
}

func sysSulge(fd int32) int32 {
	return sulgeProtsessfd(ensureKäesolevProtsess(), fd)
}

func sysdup(fd int32, väikseim int32) int32 {
	protsess := ensureKäesolevProtsess()
	kirje := getAvaFailfor(protsess, fd)
	if kirje == nil {
		return Ebadf
	}
	uusfd := allocatefd(protsess, protsess.fds[fd].kirjeldus, väikseim)
	if uusfd >= 0 {
		kirje.refs++
	}
	return uusfd
}

func sysdup2(oldfd int32, uusfd int32) int32 {
	protsess := ensureKäesolevProtsess()
	kirje := getAvaFailfor(protsess, oldfd)
	if kirje == nil {
		return Ebadf
	}
	if uusfd < 0 || uusfd >= suurimfd {
		return Ebadf
	}
	if oldfd == uusfd {
		return uusfd
	}
	if protsess.fds[uusfd].kasutuses {
		sulgeProtsessfd(protsess, uusfd)
	}
	protsess.fds[uusfd] = fdkirje{kasutuses: true, kirjeldus: protsess.fds[oldfd].kirjeldus}
	kirje.refs++
	return uusfd
}

func sysfcntl(fd int32, käsk uint32, argument uint32) int32 {
	protsess := ensureKäesolevProtsess()
	kirje := getAvaFailfor(protsess, fd)
	if kirje == nil {
		return Ebadf
	}
	switch käsk {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(protsess.fds[fd].fdLipud)
	case fMäärafd:
		protsess.fds[fd].fdLipud = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(kirje.lipud)
	case fMäärafl:
		kirje.lipud = (kirje.lipud & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	kirje := getAvaFail(fd)
	if kirje == nil {
		return Ebadf
	}
	if kirje.liik != fdLiikfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekMäära:
		base = 0
	case seekKäesolev:
		base = int64(kirje.asukoht)
	case seekLõpp:
		base = int64(kirje.suurus)
	default:
		return Einval
	}
	asukoht_2 := base + int64(offset)
	if asukoht_2 < 0 || asukoht_2 > 0x7FFFFFFF {
		return Einval
	}
	kirje.asukoht = uint32(asukoht_2)
	return int32(kirje.asukoht)
}

func lugeminevfsFail(kirje *avaFailKirjeldus, sihtfail_2 []byte, count uint32) int32 {
	mälumanager := &mem.TMälumanager{}
	tmpKursor := mälumanager.Malloc(kirje.suurus)
	if tmpKursor == nil {
		return Einval
	}
	tmp := GetbaitifromKursor(uintptr(tmpKursor), int(kirje.suurus), int(kirje.suurus))
	lugemineFail(kirje.nimi[:kirje.nimilen], tmp)
	copy(sihtfail_2[:count], tmp[kirje.asukoht:kirje.asukoht+count])
	kirje.asukoht += count
	mälumanager.Vaba(tmpKursor)
	return int32(count)
}

func isJuurRADA(rADAaddress uint32) bool {
	if rADAaddress == 0 {
		return false
	}
	rADA := GetbaitifromKursor(uintptr(rADAaddress), 4, 4)
	if rADA[0] == '/' && rADA[1] == 0 {
		return true
	}
	if rADA[0] == '.' && rADA[1] == 0 {
		return true
	}
	if rADA[0] == '/' && rADA[1] == '.' && rADA[2] == 0 {
		return true
	}
	return false
}

func sysligipääs(rADAaddress uint32, rEŽIIM uint32) int32 {
	if rADAaddress == 0 {
		return Efault
	}
	if (rEŽIIM & ^uint32(7)) != 0 {
		return Einval
	}
	isJuur := isJuurRADA(rADAaddress)
	exists := isJuur
	if !exists {
		nimilen, nimi := kopeeriRADA(rADAaddress)
		exists = nimilen != 0 && failSuurus(nimi[:nimilen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (rEŽIIM & 2) != 0 {
		return Eacces
	}

	if (rEŽIIM&1) != 0 && !isJuur {
		return Eacces
	}
	return 0
}

func syschdir(rADAaddress uint32) int32 {
	if rADAaddress == 0 {
		return Efault
	}
	if !isJuurRADA(rADAaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, suurus uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if suurus < 2 {
		return Erange
	}
	buffer_2 := GetbaitifromKursor(uintptr(bufferaddress), int(suurus), int(suurus))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, rEŽIIM uint32, suurus uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Seade = 1
	stat.Ino = inode
	stat.REŽIIM = rEŽIIM
	stat.Nlink = 1
	stat.Suurus_2 = int32(suurus)
	stat.Blksize = 512
	stat.Kast = int32((suurus + 511) / 512)
	return 0
}

func sysstat(rADAaddress uint32, stataddress uint32) int32 {
	if rADAaddress == 0 {
		return Efault
	}
	if isJuurRADA(rADAaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nimilen, nimi := kopeeriRADA(rADAaddress)
	if nimilen == 0 {
		return Enoent
	}
	suurus := failSuurus(nimi[:nimilen])
	if suurus == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nimilen; i++ {
		inode = inode*33 + uint32(nimi[i])
	}
	return fillposixstat(stataddress, sifreg|0444, suurus, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	kirje := getAvaFail(fd)
	if kirje == nil {
		return Ebadf
	}
	switch kirje.liik {
	case fdLiikstdin, fdLiikconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdLiikJuurKataloog:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdLiikfat:
		return fillposixstat(stataddress, sifreg|0444, kirje.suurus, uint32(fd+2))
	case fdLiikSokkel:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getAvaFail(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	protsess := ensureKäesolevProtsess()
	if protsess == nil {
		return 0
	}
	if protsess.programmbreak == 0 {
		protsess.programmbreak = kasutajaheapbase
	}
	if address_2 == 0 {
		return protsess.programmbreak
	}
	if address_2 < kasutajaheapbase || address_2 > kasutajaheapPiir {
		return protsess.programmbreak
	}
	protsess.programmbreak = address_2
	return protsess.programmbreak
}

func kopeeriutsväli(sihtfail *[65]byte, väärtus string) {
	piir := len(väärtus)
	if piir > 64 {
		piir = 64
	}
	for i := 0; i < piir; i++ {
		sihtfail[i] = väärtus[i]
	}
	sihtfail[piir] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nimi := (*posixutsname)(Pointer(uintptr(address_2)))
	*nimi = posixutsname{}
	kopeeriutsväli(&nimi.Sysname, "EngOS")
	kopeeriutsväli(&nimi.Nodename, "engos")
	kopeeriutsväli(&nimi.Release, "0.1-posix")
	kopeeriutsväli(&nimi.Versioon, "POSIX.1-2017 phase 1")
	kopeeriutsväli(&nimi.Machine, "i386")
	return 0
}

func saalealaunsignedinteger16(väärtus uint16) uint16 {
	return (väärtus << 8) | (väärtus >> 8)
}

func sokkelcallargument(argumendid_2 uint32, sisukord uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumendid_2 + sisukord*4)))
}

func sokkelforfd(fd int32) (*kohalikdatagramSokkel, int32) {
	kirje := getAvaFail(fd)
	if kirje == nil || kirje.liik != fdLiikSokkel || kirje.aux >= suurimsockets {
		return nil, Ebadf
	}
	sokkel := &kohaliksockets[kirje.aux]
	if !sokkel.kasutuses {
		return nil, Ebadf
	}
	return sokkel, 0
}

func allocateSokkel(domeen uint32, sokkelLiik uint32, protocol uint32) int32 {
	if domeen != afinet {
		return Eafnosupport
	}
	if sokkelLiik != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	protsess := ensureKäesolevProtsess()
	if protsess == nil {
		return Enfile
	}
	sokkelSisukord := -1
	for i := 0; i < suurimsockets; i++ {
		if !kohaliksockets[i].kasutuses {
			sokkelSisukord = i
			break
		}
	}
	if sokkelSisukord < 0 {
		return Enfile
	}
	kirjeldus := allocateAvaFail()
	if kirjeldus < 0 {
		return kirjeldus
	}
	kohaliksockets[sokkelSisukord] = kohalikdatagramSokkel{kasutuses: true}
	kirje := &avaFailTabel[kirjeldus]
	kirje.liik = fdLiikSokkel
	kirje.lipud = oLugemineKirjutamine
	kirje.aux = uint32(sokkelSisukord)
	fd := allocatefd(protsess, kirjeldus, 3)
	if fd < 0 {
		kohaliksockets[sokkelSisukord] = kohalikdatagramSokkel{}
		*kirje = avaFailKirjeldus{}
		return fd
	}
	return fd
}

func sokkeladdress(address_2 uint32, kestus uint32) (*sokkeladdressiNv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if kestus < 16 {
		return nil, Einval
	}
	tULEMUS := (*sokkeladdressiNv4)(Pointer(uintptr(address_2)))
	if tULEMUS.Family != afinet {
		return nil, Eafnosupport
	}
	return tULEMUS, 0
}

func portSisseKasutada(port uint16, except *kohalikdatagramSokkel) bool {
	for i := 0; i < suurimsockets; i++ {
		sokkel := &kohaliksockets[i]
		if sokkel != except && sokkel.kasutuses && sokkel.bound && sokkel.kohalik.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(sokkel *kohalikdatagramSokkel) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := saalealaunsignedinteger16(järgmineephemeralport)
		järgmineephemeralport++
		if järgmineephemeralport < 49152 {
			järgmineephemeralport = 49152
		}
		if !portSisseKasutada(port, sokkel) {
			sokkel.kohalik = sokkeladdressiNv4{Family: afinet, Port: port, Address: 0x0100007F}
			sokkel.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func sokkelbind(fd int32, address_2 uint32, kestus uint32) int32 {
	sokkel, viga := sokkelforfd(fd)
	if viga != 0 {
		return viga
	}
	requested, viga := sokkeladdress(address_2, kestus)
	if viga != 0 {
		return viga
	}
	if sokkel.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(sokkel)
	}
	if portSisseKasutada(requested.Port, sokkel) {
		return Eaddrinuse
	}
	sokkel.kohalik = *requested
	sokkel.bound = true
	return 0
}

func sokkelÜhendu(fd int32, address_2 uint32, kestus uint32) int32 {
	sokkel, viga := sokkelforfd(fd)
	if viga != 0 {
		return viga
	}
	võrgus, viga := sokkeladdress(address_2, kestus)
	if viga != 0 {
		return viga
	}
	if !sokkel.bound {
		if viga := bindephemeral(sokkel); viga != 0 {
			return viga
		}
	}
	sokkel.võrgus = *võrgus
	sokkel.connected = true
	return 0
}

func sokkelSaadato(fd int32, bufferaddress_2 uint32, kestus uint32, sihtfailaddress uint32, sihtfailKestus uint32) int32 {
	sokkel, viga := sokkelforfd(fd)
	if viga != 0 {
		return viga
	}
	if kestus > suurimdatagramSuurus {
		return Emsgsize
	}
	if kestus != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var sihtfail sokkeladdressiNv4
	if sihtfailaddress != 0 {
		address_2, addressViga := sokkeladdress(sihtfailaddress, sihtfailKestus)
		if addressViga != 0 {
			return addressViga
		}
		sihtfail = *address_2
	} else {
		if !sokkel.connected {
			return Enotconn
		}
		sihtfail = sokkel.võrgus
	}
	if !sokkel.bound {
		if bindViga := bindephemeral(sokkel); bindViga != 0 {
			return bindViga
		}
	}
	var receiver *kohalikdatagramSokkel
	for i := 0; i < suurimsockets; i++ {
		candidate := &kohaliksockets[i]
		if candidate.kasutuses && candidate.bound && candidate.kohalik.Port == sihtfail.Port &&
			(candidate.kohalik.Address == 0 || candidate.kohalik.Address == sihtfail.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= suurimSokkelpaketti {
		return Eagain
	}
	packet := &receiver.paketti[receiver.tail]
	*packet = sokkelpacket{kasutuses: true, suurus: kestus, aLLIKAS: sokkel.kohalik}
	if kestus != 0 {
		aLLIKAS := GetbaitifromKursor(uintptr(bufferaddress_2), int(kestus), int(kestus))
		copy(packet.data[:kestus], aLLIKAS)
	}
	receiver.tail = (receiver.tail + 1) % suurimSokkelpaketti
	receiver.count++
	return int32(kestus)
}

func sokkelreceivefrom(fd int32, bufferaddress_2 uint32, kestus uint32, aLLIKASaddress uint32, aLLIKASKestusaddress uint32) int32 {
	sokkel, viga := sokkelforfd(fd)
	if viga != 0 {
		return viga
	}
	if kestus != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if sokkel.count == 0 {
		return Eagain
	}
	packet := &sokkel.paketti[sokkel.head]
	kopeeriKestus := packet.suurus
	if kopeeriKestus > kestus {
		kopeeriKestus = kestus
	}
	if kopeeriKestus != 0 {
		sihtfail := GetbaitifromKursor(uintptr(bufferaddress_2), int(kopeeriKestus), int(kopeeriKestus))
		copy(sihtfail, packet.data[:kopeeriKestus])
	}
	if aLLIKASaddress != 0 {
		if aLLIKASKestusaddress == 0 {
			return Efault
		}
		providedKestus := (*uint32)(Pointer(uintptr(aLLIKASKestusaddress)))
		if *providedKestus >= 16 {
			*(*sokkeladdressiNv4)(Pointer(uintptr(aLLIKASaddress))) = packet.aLLIKAS
		}
		*providedKestus = 16
	}
	*packet = sokkelpacket{}
	sokkel.head = (sokkel.head + 1) % suurimSokkelpaketti
	sokkel.count--
	return int32(kopeeriKestus)
}

func kopeeriSokkelNimi(fd int32, address_2 uint32, kestusaddress uint32, peer bool) int32 {
	sokkel, viga := sokkelforfd(fd)
	if viga != 0 {
		return viga
	}
	if address_2 == 0 || kestusaddress == 0 {
		return Efault
	}
	kestus := (*uint32)(Pointer(uintptr(kestusaddress)))
	if *kestus < 16 {
		*kestus = 16
		return Einval
	}
	if peer {
		if !sokkel.connected {
			return Enotconn
		}
		*(*sokkeladdressiNv4)(Pointer(uintptr(address_2))) = sokkel.võrgus
	} else {
		if !sokkel.bound {
			if bindViga := bindephemeral(sokkel); bindViga != 0 {
				return bindViga
			}
		}
		*(*sokkeladdressiNv4)(Pointer(uintptr(address_2))) = sokkel.kohalik
	}
	*kestus = 16
	return 0
}

func sysSokkelcall(call uint32, argumendid_2 uint32) int32 {
	if argumendid_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateSokkel(sokkelcallargument(argumendid_2, 0), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2))
	case 2:
		return sokkelbind(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2))
	case 3:
		return sokkelÜhendu(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopeeriSokkelNimi(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2), false)
	case 7:
		return kopeeriSokkelNimi(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2), true)
	case 9:
		return sokkelSaadato(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2), 0, 0)
	case 10:
		return sokkelreceivefrom(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2), 0, 0)
	case 11:
		return sokkelSaadato(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2), sokkelcallargument(argumendid_2, 4), sokkelcallargument(argumendid_2, 5))
	case 12:
		return sokkelreceivefrom(int32(sokkelcallargument(argumendid_2, 0)), sokkelcallargument(argumendid_2, 1), sokkelcallargument(argumendid_2, 2), sokkelcallargument(argumendid_2, 4), sokkelcallargument(argumendid_2, 5))
	case 13:
		if _, viga := sokkelforfd(int32(sokkelcallargument(argumendid_2, 0))); viga != 0 {
			return viga
		}
		return 0
	case 14:
		if _, viga := sokkelforfd(int32(sokkelcallargument(argumendid_2, 0))); viga != 0 {
			return viga
		}
		return 0
	}
	return Eopnotsupp
}

func lugeminestdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetbaitifromKursor(uintptr(address), int(count), int(count))
	var n uint32
	for n < count {
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
	järgmine := (stdinKirjutamine + 1) % uint32(len(stdinbuffer))
	if järgmine == stdinLugemine {
		return
	}
	stdinbuffer[stdinKirjutamine] = c
	stdinKirjutamine = järgmine
}

func stdingetblocking() byte {
	for stdinLugemine == stdinKirjutamine {
		sc := pollKlaviatuurscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLugemine]
	stdinLugemine = (stdinLugemine + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlaviatuurscancode() byte {
	for (PortLugeminebyte(0x64) & 0x01) == 0 {
	}
	sc := PortLugeminebyte(0x60)
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

func kopeeriKäivitaminevector(address_2 uint32, tULEMUS *käivitaminevector) int32 {
	*tULEMUS = käivitaminevector{}
	if address_2 == 0 {
		return 0
	}
	for sisukord := uint32(0); sisukord < suurimKäivitaminevectorkirje; sisukord++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + sisukord*4)))
		if stringaddress == 0 {
			tULEMUS.count = sisukord
			return 0
		}
		terminated := false
		for kestus := uint32(0); kestus <= suurimKäivitaminestringKestus; kestus++ {
			väärtus := *(*byte)(Pointer(uintptr(stringaddress + kestus)))
			tULEMUS.values[sisukord][kestus] = väärtus
			if väärtus == 0 {
				tULEMUS.lengths[sisukord] = kestus
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

func pushKäivitamineunsignedinteger32(stack *uint32, väärtus uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = väärtus
}

func setupKäivitaminestack(protsessor *TcpuOlek, argumendid_2 *käivitaminevector, environment *käivitaminevector) int32 {
	const stackbaiti uint32 = 4096
	if !MakeVahemikPrivaatwritable(getcr3(), KasutajastackÜleval-stackbaiti, stackbaiti) {
		return Enomem
	}
	stack := KasutajastackÜleval
	var argumentpointers [suurimKäivitaminevectorkirje]uint32
	var environmentpointers [suurimKäivitaminevectorkirje]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		kestus := environment.lengths[i] + 1
		stack -= kestus
		sihtfail := GetbaitifromKursor(uintptr(stack), int(kestus), int(kestus))
		copy(sihtfail, environment.values[i][:kestus])
		environmentpointers[i] = stack
	}
	for i := int(argumendid_2.count) - 1; i >= 0; i-- {
		kestus := argumendid_2.lengths[i] + 1
		stack -= kestus
		sihtfail := GetbaitifromKursor(uintptr(stack), int(kestus), int(kestus))
		copy(sihtfail, argumendid_2.values[i][:kestus])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushKäivitamineunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushKäivitamineunsignedinteger32(&stack, environmentpointers[i])
	}
	pushKäivitamineunsignedinteger32(&stack, 0)
	for i := int(argumendid_2.count) - 1; i >= 0; i-- {
		pushKäivitamineunsignedinteger32(&stack, argumentpointers[i])
	}
	pushKäivitamineunsignedinteger32(&stack, argumendid_2.count)
	protsessor.Esp = stack
	protsessor.Ebp = 0
	return 0
}

func sulgeSeesKäivitamine(protsess *protsesskirje) {
	if protsess == nil {
		return
	}
	for fd := int32(0); fd < suurimfd; fd++ {
		if protsess.fds[fd].kasutuses && (protsess.fds[fd].fdLipud&fdcloexec) != 0 {
			sulgeProtsessfd(protsess, fd)
		}
	}
}

func sysexecve(protsessor *TcpuOlek, rADAaddress uint32) int32 {
	if rADAaddress == 0 {
		return Efault
	}
	var argumendid_2 käivitaminevector
	var environment käivitaminevector
	if tULEMUS := kopeeriKäivitaminevector(protsessor.Ecx, &argumendid_2); tULEMUS < 0 {
		return tULEMUS
	}
	if tULEMUS := kopeeriKäivitaminevector(protsessor.Edx, &environment); tULEMUS < 0 {
		return tULEMUS
	}
	nimilen, nimi := kopeeriRADA(rADAaddress)
	if nimilen == 0 {
		return Enoent
	}
	suurus := failSuurus(nimi[:nimilen])
	if suurus == 0 {
		return Enoent
	}
	mälumanager := &mem.TMälumanager{}
	failKursor := mälumanager.Malloc(suurus)
	if failKursor == nil {
		return Einval
	}
	data := GetbaitifromKursor(uintptr(failKursor), int(suurus), int(suurus))
	lugemineFail(nimi[:nimilen], data)
	if suurus < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		mälumanager.Vaba(failKursor)
		return Enoexec
	}
	loader := Elf{}
	kirje := loader.Getkirje(data)
	loader.Parse(data, getcr3())
	mälumanager.Vaba(failKursor)
	if tULEMUS := setupKäivitaminestack(protsessor, &argumendid_2, &environment); tULEMUS < 0 {
		return tULEMUS
	}
	sulgeSeesKäivitamine(ensureKäesolevProtsess())
	protsessor.Eip = kirje
	protsessor.Eax = 0
	return 0
}

func sysfork(protsessor *TcpuOlek) int32 {
	vanempid := Käesolevpid()
	if ensureKäesolevProtsess() == nil {
		return Enfile
	}
	pid := allocateProtsess(vanempid)
	if pid == 0 {
		return Einval
	}
	mälumanager := &mem.TMälumanager{}
	threadKursor := mälumanager.Malloc(uint32(Sizeof(TThread{})))
	stackKursor := mälumanager.Malloc(ThreadstackSuurus)
	lapsLehekülgKataloog := CloneaddressTühikcow(getcr3())
	if threadKursor == nil || stackKursor == nil || lapsLehekülgKataloog == 0 {
		unustaProtsess(pid)
		return Einval
	}
	laps := (*TThread)(threadKursor)
	laps.Stack = uint32(uintptr(stackKursor))
	laps.ProtsessorOlek = (*TcpuOlek)(Pointer(uintptr(stackKursor) + ThreadstackSuurus - Sizeof(TcpuOlek{})))
	*laps.ProtsessorOlek = *protsessor
	laps.ProtsessorOlek.Eax = 0
	laps.Kasutajastack_2 = protsessor.Esp
	laps.KasutajastackSuurus_2 = 0
	laps.Pid = pid
	laps.Vanempid = vanempid
	laps.LehekülgKataloogkirje = lapsLehekülgKataloog
	laps.ThreadOlek = Valmis
	laps.Fpuoffset = 0xffffffff
	laps.Iskernel = false
	Lisarunnablethread(laps)
	return int32(pid)
}

func sysVälju(olek uint32) {
	pid := Käesolevpid()
	for i := 0; i < len(protsessTabel); i++ {
		if protsessTabel[i].kasutuses && protsessTabel[i].pid == pid {
			sulgeKõikProtsessfds(&protsessTabel[i])
			protsessTabel[i].exited = true
			protsessTabel[i].olek = (olek & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, olekaddress uint32, valikud uint32) int32 {
	if (valikud & ^uint32(1)) != 0 {
		return Einval
	}
	vanempid := Käesolevpid()
	foundlaps := false
	for i := 0; i < len(protsessTabel); i++ {
		p := &protsessTabel[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.kasutuses && matches && p.vanem == vanempid {
			foundlaps = true
			if p.exited {
				if olekaddress != 0 {
					*(*uint32)(Pointer(uintptr(olekaddress))) = p.olek
				}
				lapspid := p.pid
				*p = protsesskirje{}
				return int32(lapspid)
			}
		}
	}
	if !foundlaps {
		return Echild
	}

	if (valikud & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProtsess(vanem uint32) uint32 {
	vanemProtsess := otsiProtsess(vanem)
	pid := Allocatepid()
	for i := 0; i < len(protsessTabel); i++ {
		if !protsessTabel[i].kasutuses {
			protsessTabel[i] = protsesskirje{
				kasutuses:	true,
				pid:		pid,
				vanem:		vanem,
				programmbreak:	kasutajaheapbase,
			}
			if vanemProtsess != nil {
				protsessTabel[i].programmbreak = vanemProtsess.programmbreak
				for fd := 0; fd < suurimfd; fd++ {
					if vanemProtsess.fds[fd].kasutuses {
						protsessTabel[i].fds[fd] = vanemProtsess.fds[fd]
						kirjeldus := vanemProtsess.fds[fd].kirjeldus
						if kirjeldus >= 0 && kirjeldus < suurimAvaFAILID {
							avaFailTabel[kirjeldus].refs++
						}
					}
				}
			} else {
				initializeProtsessfds(&protsessTabel[i])
			}
			return pid
		}
	}
	return 0
}

func sulgeKõikProtsessfds(protsess *protsesskirje) {
	if protsess == nil {
		return
	}
	for fd := int32(0); fd < suurimfd; fd++ {
		if protsess.fds[fd].kasutuses {
			sulgeProtsessfd(protsess, fd)
		}
	}
}

func unustaProtsess(pid uint32) {
	protsess := otsiProtsess(pid)
	if protsess == nil {
		return
	}
	sulgeKõikProtsessfds(protsess)
	*protsess = protsesskirje{}
}

func kopeeriRADA(rADAaddress uint32) (uint32, [12]byte) {
	var nimi [12]byte
	if rADAaddress == 0 {
		return 0, nimi
	}
	raw := GetbaitifromKursor(uintptr(rADAaddress), 64, 64)
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
		nimi[n] = c
		n++
	}
	return n, nimi
}

func failSuurus(failinimi []byte) uint32 {
	var ata0s = TLaiendatudTehnoloogiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lugeminepartition(&ata0s)

	bios := TBiosparameterKast32{}
	suurus := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failinimi)
	ata0s.Flush()
	return suurus
}

func lugemineFail(failinimi []byte, data []byte) {
	var ata0s = TLaiendatudTehnoloogiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lugeminepartition(&ata0s)

	bios := TBiosparameterKast32{}
	bios.Lugemine(&ata0s, partition.Mbr.Primarypartition[0], failinimi, data)
	ata0s.Flush()
}

func getcr3() uint32
