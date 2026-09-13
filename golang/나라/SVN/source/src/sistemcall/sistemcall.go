package sistemcall

import . "unsafe"

import . "prekinitev"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "datotekaSistem/fat"
import . "datotekaSistem/elf"
import mem "pomnilnikmanager"
import . "paging"
import . "vrata"
import . "tasking/scheduler"
import . "tasking/thread"
import . "navideznoPomnilnik"

var console_2 = TConsole{}

type TSyscall struct {
	TPrekinitevhandler
}

const (
	SysIzhod	uint32	= 1
	Sysfork		uint32	= 2
	SysBranje	uint32	= 3
	SysPisanje	uint32	= 4
	SysOdpri	uint32	= 5
	SysZapri	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysdostop	uint32	= 33
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
	SysrtIzhod	uint32	= 252

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
	maxfd				= 32
	maxOdpriDatoteke		= 128
)

type fdvnos struct {
	uporabljeno	bool
	opis		int32
	fdZastavice	uint32
}

type odpriDatotekaOpis struct {
	uporabljeno	bool
	refs		uint32
	vrsta		uint32
	zastavice	uint32
	položaj		uint32
	velikost	uint32
	ime		[12]byte
	imelen		uint32
	aux		uint32
}

const (
	fdVrstaBrez	uint32	= 0
	fdVrstafat	uint32	= 1
	fdVrstastdin	uint32	= 2
	fdVrstaconsole	uint32	= 3
	fdVrstaVrhMapa	uint32	= 4
	fdVrstaVti	uint32	= 5

	oBranjeonly	uint32	= 0
	oPisanjeonly	uint32	= 1
	oBranjePisanje	uint32	= 2
	ocreate		uint32	= 0x40
	oRazdeli	uint32	= 0x200
	oappend		uint32	= 0x400
	oMapa		uint32	= 0x10000

	seekmnožica	uint32	= 0
	seekcurrent	uint32	= 1
	seekend		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fmnožicafd	uint32	= 2
	fgetfl		uint32	= 3
	fmnožicafl	uint32	= 4
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
	maxsockets		= 32
	maxVtipaketov		= 8
	maxdatagramVelikost	= 512
)

type vtiaddressipv4 struct {
	Family	uint16
	Vrata	uint16
	Address	uint32
	Zero	[8]byte
}

type vtipacket struct {
	uporabljeno	bool
	velikost	uint32
	vir		vtiaddressipv4
	data		[maxdatagramVelikost]byte
}

type krajevnodatagramVti struct {
	uporabljeno	bool
	bound		bool
	connected	bool
	krajevno	vtiaddressipv4
	oddaljeno	vtiaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	paketov		[maxVtipaketov]vtipacket
}

type posixstat struct {
	Naprava		uint32
	Ino		uint32
	NAČIN		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Velikost_2	int32
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
	Različica	[65]byte
	Machine		[65]byte
}

const (
	maxIzvedljivovectorvnos	= 16
	maxIzvedljivoNizDolžina	= 63
)

type izvedljivovector struct {
	count	uint32
	lengths	[maxIzvedljivovectorvnos]uint32
	values	[maxIzvedljivovectorvnos][maxIzvedljivoNizDolžina + 1]byte
}

type opravilovnos struct {
	uporabljeno		bool
	pid			uint32
	nadrejenipredmet	uint32
	končal			bool
	stanje			uint32
	programbreak		uint32
	fds			[maxfd]fdvnos
}

type nizheader struct {
	Data	uintptr
	Len	int
}

func syscallNapaka(napaka int32) uint32 {
	return *(*uint32)(Pointer(&napaka))
}

var odpriDatotekaPreglednica [maxOdpriDatoteke]odpriDatotekaOpis
var opraviloPreglednica [32]opravilovnos
var krajevnosockets [maxsockets]krajevnodatagramVti
var naslednjeephemeralVrata uint16 = 49152

const (
	uporabnikheapbase	uint32	= 0x06000000
	uporabnikheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinBranje uint32
var stdinPisanje uint32

func Prekinitev(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIzhod_2(kazalo uint32) {
	Syscall(SysIzhod, kazalo)
}

func SysBranje_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysBranje, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysNatisnistr(buffer string) {
	h := (*nizheader)(Pointer(&buffer))
	Syscall(SysPisanje, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysNatisniunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysPisanje, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOdpri_2(pOT uintptr, zastavice uint32, nAČIN uint32) int32 {
	return int32(Syscall(SysOdpri, uint32(pOT), zastavice, nAČIN))
}

func SysZapri_2(fd uint32) int32 {
	return int32(Syscall(SysZapri, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametri ...uint32) uint32 {

	l := len(parametri)
	switch l {
	case 1:
		return Prekinitev(parametri[0], 0, 0, 0, 0, 0)
	case 2:
		return Prekinitev(parametri[0], parametri[1], 0, 0, 0, 0)
	case 3:
		return Prekinitev(parametri[0], parametri[1], parametri[2], 0, 0, 0)
	case 4:
		return Prekinitev(parametri[0], parametri[1], parametri[2], parametri[3], 0, 0)
	case 5:
		return Prekinitev(parametri[0], parametri[1], parametri[2], parametri[3], parametri[4], 0)
	case 6:
		return Prekinitev(parametri[0], parametri[1], parametri[2], parametri[3], parametri[4], parametri[5])
	default:
		return syscallNapaka(Enosys)
	}
}

func (sam *TSyscall) Init(manager *TPrekinitevmanager) {
	initDatotekadescriptor()

	prekinitevhandler = ročicaPrekinitev

	var address uintptr
	address = uintptr(Pointer(&prekinitevhandler))

	sam.TPrekinitevhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var prekinitevhandler func(uint32) uint32

func ročicaPrekinitev(esp uint32) uint32 {
	var cPE = (*TcpuStanje)(Pointer(uintptr(esp)))

	switch cPE.Eax {
	case SysIzhod:
		sysIzhod(cPE.Ebx)
		return uint32(uintptr(Pointer(Zaustavicurrentthread(cPE))))
	case SysrtIzhod:
		sysIzhod(cPE.Ebx)
		return uint32(uintptr(Pointer(Zaustavicurrentthread(cPE))))
	case Sysfork:
		cPE.Eax = uint32(sysfork(cPE))
		return esp
	case SysBranje:
		cPE.Eax = uint32(sysBranje(int32(cPE.Ebx), cPE.Ecx, cPE.Edx))
		return esp
	case SysPisanje:
		cPE.Eax = uint32(sysPisanje(int32(cPE.Ebx), cPE.Ecx, cPE.Edx))
		return esp
	case SysOdpri:
		cPE.Eax = uint32(sysOdpri(cPE.Ebx, cPE.Ecx, cPE.Edx))
		return esp
	case Syscreat:
		cPE.Eax = uint32(sysOdpri(cPE.Ebx, ocreate|oPisanjeonly|oRazdeli, cPE.Ecx))
		return esp
	case SysZapri:
		cPE.Eax = uint32(sysZapri(int32(cPE.Ebx)))
		return esp
	case Syswaitpid:
		cPE.Eax = uint32(syswaitpid(int32(cPE.Ebx), cPE.Ecx, cPE.Edx))
		return esp
	case Syslseek:
		cPE.Eax = uint32(syslseek(int32(cPE.Ebx), int32(cPE.Ecx), cPE.Edx))
		return esp
	case Sysexecve:
		cPE.Eax = uint32(sysexecve(cPE, cPE.Ebx))
		return esp
	case Sysgetpid:
		cPE.Eax = Currentpid()
		return esp
	case Sysgetppid:
		cPE.Eax = Currentnadrejenipredmetpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cPE.Eax = 0
		return esp
	case Sysdostop:
		cPE.Eax = uint32(sysdostop(cPE.Ebx, cPE.Ecx))
		return esp
	case Syschdir:
		cPE.Eax = uint32(syschdir(cPE.Ebx))
		return esp
	case Sysgetcwd:
		cPE.Eax = uint32(sysgetcwd(cPE.Ebx, cPE.Ecx))
		return esp
	case Sysdup:
		cPE.Eax = uint32(sysdup(int32(cPE.Ebx), 0))
		return esp
	case Sysdup2:
		cPE.Eax = uint32(sysdup2(int32(cPE.Ebx), int32(cPE.Ecx)))
		return esp
	case Syssocketcall:
		cPE.Eax = uint32(sysVticall(cPE.Ebx, cPE.Ecx))
		return esp
	case Sysfcntl:
		cPE.Eax = uint32(sysfcntl(int32(cPE.Ebx), cPE.Ecx, cPE.Edx))
		return esp
	case Sysstat, Syslstat:
		cPE.Eax = uint32(sysstat(cPE.Ebx, cPE.Ecx))
		return esp
	case Sysfstat:
		cPE.Eax = uint32(sysfstat(int32(cPE.Ebx), cPE.Ecx))
		return esp
	case Sysfsync:
		cPE.Eax = uint32(sysfsync(int32(cPE.Ebx)))
		return esp
	case Syssync:
		cPE.Eax = 0
		return esp
	case Sysuname:
		cPE.Eax = uint32(sysuname(cPE.Ebx))
		return esp
	case Sysbrk:
		cPE.Eax = sysbrk(cPE.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Natisni(cPE.Ebx)
		return esp

	default:
		console_2.MNatisnixy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Natisni(esp)
		console_2.MNatisni(([]byte)(":"))
		console_2.MUnsignedinteger32Natisni(cPE.Eax)
		console_2.MNatisni(([]byte)(":"))
		console_2.MUnsignedinteger32Natisni(cPE.Ebx)
		console_2.MNatisni(([]byte)(":"))
		console_2.MUnsignedinteger32Natisni(cPE.Ecx)
		console_2.MNatisni(([]byte)(":"))
		console_2.MUnsignedinteger32Natisni(cPE.Edx)
		console_2.MNatisni(([]byte)("]"))
		cPE.Eax = syscallNapaka(Enosys)
		return esp
	}

	return esp
}

func initDatotekadescriptor() {
	for i := 0; i < maxOdpriDatoteke; i++ {
		odpriDatotekaPreglednica[i] = odpriDatotekaOpis{}
	}
	for i := 0; i < len(opraviloPreglednica); i++ {
		opraviloPreglednica[i] = opravilovnos{}
	}
	for i := 0; i < len(krajevnosockets); i++ {
		krajevnosockets[i] = krajevnodatagramVti{}
	}
	naslednjeephemeralVrata = 49152
	odpriDatotekaPreglednica[0] = odpriDatotekaOpis{uporabljeno: true, vrsta: fdVrstastdin, zastavice: oBranjeonly}
	odpriDatotekaPreglednica[1] = odpriDatotekaOpis{uporabljeno: true, vrsta: fdVrstaconsole, zastavice: oPisanjeonly}
	odpriDatotekaPreglednica[2] = odpriDatotekaOpis{uporabljeno: true, vrsta: fdVrstaconsole, zastavice: oPisanjeonly}
}

func najdiOpravilo(pid uint32) *opravilovnos {
	for i := 0; i < len(opraviloPreglednica); i++ {
		if opraviloPreglednica[i].uporabljeno && opraviloPreglednica[i].pid == pid {
			return &opraviloPreglednica[i]
		}
	}
	return nil
}

func initializeOpravilofds(opravilo *opravilovnos) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		opravilo.fds[fd] = fdvnos{uporabljeno: true, opis: fd}
		odpriDatotekaPreglednica[fd].refs++
	}
}

func ensurecurrentOpravilo() *opravilovnos {
	pid := Currentpid()
	if opravilo := najdiOpravilo(pid); opravilo != nil {
		return opravilo
	}
	for i := 0; i < len(opraviloPreglednica); i++ {
		if !opraviloPreglednica[i].uporabljeno {
			opraviloPreglednica[i] = opravilovnos{
				uporabljeno:		true,
				pid:			pid,
				nadrejenipredmet:	Currentnadrejenipredmetpid(),
				programbreak:		uporabnikheapbase,
			}
			initializeOpravilofds(&opraviloPreglednica[i])
			return &opraviloPreglednica[i]
		}
	}
	return nil
}

func getOdpriDatotekafor(opravilo *opravilovnos, fd int32) *odpriDatotekaOpis {
	if opravilo == nil || fd < 0 || fd >= maxfd || !opravilo.fds[fd].uporabljeno {
		return nil
	}
	opis := opravilo.fds[fd].opis
	if opis < 0 || opis >= maxOdpriDatoteke || !odpriDatotekaPreglednica[opis].uporabljeno {
		return nil
	}
	return &odpriDatotekaPreglednica[opis]
}

func getOdpriDatoteka(fd int32) *odpriDatotekaOpis {
	return getOdpriDatotekafor(ensurecurrentOpravilo(), fd)
}

func allocateOdpriDatoteka() int32 {
	for i := int32(3); i < maxOdpriDatoteke; i++ {
		if !odpriDatotekaPreglednica[i].uporabljeno {
			odpriDatotekaPreglednica[i] = odpriDatotekaOpis{uporabljeno: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(opravilo *opravilovnos, opis int32, najmanj int32) int32 {
	if opravilo == nil {
		return Enfile
	}
	if najmanj < 0 || najmanj >= maxfd {
		return Einval
	}
	for fd := najmanj; fd < maxfd; fd++ {
		if !opravilo.fds[fd].uporabljeno {
			opravilo.fds[fd] = fdvnos{uporabljeno: true, opis: opis}
			return fd
		}
	}
	return Emfile
}

func releaseOdpriDatoteka(opis int32) {
	if opis < 0 || opis >= maxOdpriDatoteke {
		return
	}
	vnos := &odpriDatotekaPreglednica[opis]
	if vnos.refs > 0 {
		vnos.refs--
	}

	if vnos.refs == 0 && opis > stderrfd {
		if vnos.vrsta == fdVrstaVti && vnos.aux < maxsockets {
			krajevnosockets[vnos.aux] = krajevnodatagramVti{}
		}
		*vnos = odpriDatotekaOpis{}
	}
}

func zapriOpravilofd(opravilo *opravilovnos, fd int32) int32 {
	if opravilo == nil || getOdpriDatotekafor(opravilo, fd) == nil {
		return Ebadf
	}
	opis := opravilo.fds[fd].opis
	opravilo.fds[fd] = fdvnos{}
	releaseOdpriDatoteka(opis)
	return 0
}

func sysPisanje(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	vnos := getOdpriDatoteka(fd)
	if vnos == nil {
		return Ebadf
	}
	if vnos.vrsta != fdVrstaconsole {
		if vnos.vrsta == fdVrstaVti {
			return vtiPošljito(fd, address, count, 0, 0)
		}
		if vnos.vrsta == fdVrstafat || vnos.vrsta == fdVrstaVrhMapa {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBajtovfromKazalnik(uintptr(address), int(count), int(count))
	console_2.MNatisni(buffer)
	return int32(count)
}

func sysBranje(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	vnos := getOdpriDatoteka(fd)
	if vnos == nil {
		return Ebadf
	}
	if vnos.vrsta == fdVrstastdin {
		return branjestdin(address, count)
	}
	if vnos.vrsta == fdVrstaVrhMapa {
		return Eisdir
	}
	if vnos.vrsta == fdVrstaVti {
		return vtireceivefrom(fd, address, count, 0, 0)
	}
	if vnos.vrsta != fdVrstafat {
		return Ebadf
	}
	if vnos.položaj >= vnos.velikost {
		return 0
	}
	remaining := vnos.velikost - vnos.položaj
	if count > remaining {
		count = remaining
	}
	buffer := GetBajtovfromKazalnik(uintptr(address), int(count), int(count))
	return branjevfsDatoteka(vnos, buffer, count)
}

func sysOdpri(pOTaddress uint32, zastavice uint32, nAČIN uint32) int32 {
	_ = nAČIN
	if pOTaddress == 0 {
		return Efault
	}
	dostopNAČIN := zastavice & 3
	if dostopNAČIN == oPisanjeonly || dostopNAČIN == oBranjePisanje || (zastavice&(ocreate|oRazdeli|oappend)) != 0 {
		return Erofs
	}

	opravilo := ensurecurrentOpravilo()
	if opravilo == nil {
		return Enfile
	}
	opis := allocateOdpriDatoteka()
	if opis < 0 {
		return opis
	}
	vnos := &odpriDatotekaPreglednica[opis]
	vnos.zastavice = zastavice
	if isVrhPOT(pOTaddress) {
		vnos.vrsta = fdVrstaVrhMapa
		vnos.velikost = 0
	} else {
		imelen, ime := kopirajPOT(pOTaddress)
		if imelen == 0 {
			*vnos = odpriDatotekaOpis{}
			return Enoent
		}
		velikost := datotekaVelikost(ime[:imelen])
		if velikost == 0 {
			*vnos = odpriDatotekaOpis{}
			return Enoent
		}
		if (zastavice & oMapa) != 0 {
			*vnos = odpriDatotekaOpis{}
			return Enotdir
		}
		vnos.vrsta = fdVrstafat
		vnos.velikost = velikost
		vnos.imelen = imelen
		vnos.ime = ime
	}

	fd := allocatefd(opravilo, opis, 3)
	if fd < 0 {
		*vnos = odpriDatotekaOpis{}
		return fd
	}
	return fd
}

func sysZapri(fd int32) int32 {
	return zapriOpravilofd(ensurecurrentOpravilo(), fd)
}

func sysdup(fd int32, najmanj int32) int32 {
	opravilo := ensurecurrentOpravilo()
	vnos := getOdpriDatotekafor(opravilo, fd)
	if vnos == nil {
		return Ebadf
	}
	novafd := allocatefd(opravilo, opravilo.fds[fd].opis, najmanj)
	if novafd >= 0 {
		vnos.refs++
	}
	return novafd
}

func sysdup2(oldfd int32, novafd int32) int32 {
	opravilo := ensurecurrentOpravilo()
	vnos := getOdpriDatotekafor(opravilo, oldfd)
	if vnos == nil {
		return Ebadf
	}
	if novafd < 0 || novafd >= maxfd {
		return Ebadf
	}
	if oldfd == novafd {
		return novafd
	}
	if opravilo.fds[novafd].uporabljeno {
		zapriOpravilofd(opravilo, novafd)
	}
	opravilo.fds[novafd] = fdvnos{uporabljeno: true, opis: opravilo.fds[oldfd].opis}
	vnos.refs++
	return novafd
}

func sysfcntl(fd int32, ukaz uint32, argument uint32) int32 {
	opravilo := ensurecurrentOpravilo()
	vnos := getOdpriDatotekafor(opravilo, fd)
	if vnos == nil {
		return Ebadf
	}
	switch ukaz {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(opravilo.fds[fd].fdZastavice)
	case fmnožicafd:
		opravilo.fds[fd].fdZastavice = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(vnos.zastavice)
	case fmnožicafl:
		vnos.zastavice = (vnos.zastavice & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	vnos := getOdpriDatoteka(fd)
	if vnos == nil {
		return Ebadf
	}
	if vnos.vrsta != fdVrstafat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekmnožica:
		base = 0
	case seekcurrent:
		base = int64(vnos.položaj)
	case seekend:
		base = int64(vnos.velikost)
	default:
		return Einval
	}
	položaj_2 := base + int64(offset)
	if položaj_2 < 0 || položaj_2 > 0x7FFFFFFF {
		return Einval
	}
	vnos.položaj = uint32(položaj_2)
	return int32(vnos.položaj)
}

func branjevfsDatoteka(vnos *odpriDatotekaOpis, cilj_2 []byte, count uint32) int32 {
	pomnilnikmanager := &mem.TPomnilnikmanager{}
	tmpKazalnik := pomnilnikmanager.Malloc(vnos.velikost)
	if tmpKazalnik == nil {
		return Einval
	}
	tmp := GetBajtovfromKazalnik(uintptr(tmpKazalnik), int(vnos.velikost), int(vnos.velikost))
	branjeDatoteka(vnos.ime[:vnos.imelen], tmp)
	copy(cilj_2[:count], tmp[vnos.položaj:vnos.položaj+count])
	vnos.položaj += count
	pomnilnikmanager.Prosto(tmpKazalnik)
	return int32(count)
}

func isVrhPOT(pOTaddress uint32) bool {
	if pOTaddress == 0 {
		return false
	}
	pOT := GetBajtovfromKazalnik(uintptr(pOTaddress), 4, 4)
	if pOT[0] == '/' && pOT[1] == 0 {
		return true
	}
	if pOT[0] == '.' && pOT[1] == 0 {
		return true
	}
	if pOT[0] == '/' && pOT[1] == '.' && pOT[2] == 0 {
		return true
	}
	return false
}

func sysdostop(pOTaddress uint32, nAČIN uint32) int32 {
	if pOTaddress == 0 {
		return Efault
	}
	if (nAČIN & ^uint32(7)) != 0 {
		return Einval
	}
	isVrh := isVrhPOT(pOTaddress)
	exists := isVrh
	if !exists {
		imelen, ime := kopirajPOT(pOTaddress)
		exists = imelen != 0 && datotekaVelikost(ime[:imelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (nAČIN & 2) != 0 {
		return Eacces
	}

	if (nAČIN&1) != 0 && !isVrh {
		return Eacces
	}
	return 0
}

func syschdir(pOTaddress uint32) int32 {
	if pOTaddress == 0 {
		return Efault
	}
	if !isVrhPOT(pOTaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, velikost uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if velikost < 2 {
		return Erange
	}
	buffer_2 := GetBajtovfromKazalnik(uintptr(bufferaddress), int(velikost), int(velikost))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, nAČIN uint32, velikost uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Naprava = 1
	stat.Ino = inode
	stat.NAČIN = nAČIN
	stat.Nlink = 1
	stat.Velikost_2 = int32(velikost)
	stat.Blksize = 512
	stat.Blok = int32((velikost + 511) / 512)
	return 0
}

func sysstat(pOTaddress uint32, stataddress uint32) int32 {
	if pOTaddress == 0 {
		return Efault
	}
	if isVrhPOT(pOTaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	imelen, ime := kopirajPOT(pOTaddress)
	if imelen == 0 {
		return Enoent
	}
	velikost := datotekaVelikost(ime[:imelen])
	if velikost == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < imelen; i++ {
		inode = inode*33 + uint32(ime[i])
	}
	return fillposixstat(stataddress, sifreg|0444, velikost, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	vnos := getOdpriDatoteka(fd)
	if vnos == nil {
		return Ebadf
	}
	switch vnos.vrsta {
	case fdVrstastdin, fdVrstaconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdVrstaVrhMapa:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdVrstafat:
		return fillposixstat(stataddress, sifreg|0444, vnos.velikost, uint32(fd+2))
	case fdVrstaVti:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getOdpriDatoteka(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	opravilo := ensurecurrentOpravilo()
	if opravilo == nil {
		return 0
	}
	if opravilo.programbreak == 0 {
		opravilo.programbreak = uporabnikheapbase
	}
	if address_2 == 0 {
		return opravilo.programbreak
	}
	if address_2 < uporabnikheapbase || address_2 > uporabnikheaplimit {
		return opravilo.programbreak
	}
	opravilo.programbreak = address_2
	return opravilo.programbreak
}

func kopirajutspolje(cilj *[65]byte, vrednost string) {
	limit := len(vrednost)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		cilj[i] = vrednost[i]
	}
	cilj[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	ime := (*posixutsname)(Pointer(uintptr(address_2)))
	*ime = posixutsname{}
	kopirajutspolje(&ime.Sysname, "EngOS")
	kopirajutspolje(&ime.Nodename, "engos")
	kopirajutspolje(&ime.Release, "0.1-posix")
	kopirajutspolje(&ime.Različica, "POSIX.1-2017 phase 1")
	kopirajutspolje(&ime.Machine, "i386")
	return 0
}

func izmenjevalnirazdelekunsignedinteger16(vrednost uint16) uint16 {
	return (vrednost << 8) | (vrednost >> 8)
}

func vticallargument(argumenti_2 uint32, kazalo uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenti_2 + kazalo*4)))
}

func vtiforfd(fd int32) (*krajevnodatagramVti, int32) {
	vnos := getOdpriDatoteka(fd)
	if vnos == nil || vnos.vrsta != fdVrstaVti || vnos.aux >= maxsockets {
		return nil, Ebadf
	}
	vti := &krajevnosockets[vnos.aux]
	if !vti.uporabljeno {
		return nil, Ebadf
	}
	return vti, 0
}

func allocateVti(domena uint32, vtiVrsta uint32, protocol uint32) int32 {
	if domena != afinet {
		return Eafnosupport
	}
	if vtiVrsta != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	opravilo := ensurecurrentOpravilo()
	if opravilo == nil {
		return Enfile
	}
	vtiKazalo := -1
	for i := 0; i < maxsockets; i++ {
		if !krajevnosockets[i].uporabljeno {
			vtiKazalo = i
			break
		}
	}
	if vtiKazalo < 0 {
		return Enfile
	}
	opis := allocateOdpriDatoteka()
	if opis < 0 {
		return opis
	}
	krajevnosockets[vtiKazalo] = krajevnodatagramVti{uporabljeno: true}
	vnos := &odpriDatotekaPreglednica[opis]
	vnos.vrsta = fdVrstaVti
	vnos.zastavice = oBranjePisanje
	vnos.aux = uint32(vtiKazalo)
	fd := allocatefd(opravilo, opis, 3)
	if fd < 0 {
		krajevnosockets[vtiKazalo] = krajevnodatagramVti{}
		*vnos = odpriDatotekaOpis{}
		return fd
	}
	return fd
}

func vtiaddress(address_2 uint32, dolžina uint32) (*vtiaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if dolžina < 16 {
		return nil, Einval
	}
	rEZULTAT := (*vtiaddressipv4)(Pointer(uintptr(address_2)))
	if rEZULTAT.Family != afinet {
		return nil, Eafnosupport
	}
	return rEZULTAT, 0
}

func vrataVhodnoUporabi(vrata uint16, except *krajevnodatagramVti) bool {
	for i := 0; i < maxsockets; i++ {
		vti := &krajevnosockets[i]
		if vti != except && vti.uporabljeno && vti.bound && vti.krajevno.Vrata == vrata {
			return true
		}
	}
	return false
}

func bindephemeral(vti *krajevnodatagramVti) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		vrata := izmenjevalnirazdelekunsignedinteger16(naslednjeephemeralVrata)
		naslednjeephemeralVrata++
		if naslednjeephemeralVrata < 49152 {
			naslednjeephemeralVrata = 49152
		}
		if !vrataVhodnoUporabi(vrata, vti) {
			vti.krajevno = vtiaddressipv4{Family: afinet, Vrata: vrata, Address: 0x0100007F}
			vti.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func vtibind(fd int32, address_2 uint32, dolžina uint32) int32 {
	vti, napaka := vtiforfd(fd)
	if napaka != 0 {
		return napaka
	}
	requested, napaka := vtiaddress(address_2, dolžina)
	if napaka != 0 {
		return napaka
	}
	if vti.bound {
		return Einval
	}
	if requested.Vrata == 0 {
		return bindephemeral(vti)
	}
	if vrataVhodnoUporabi(requested.Vrata, vti) {
		return Eaddrinuse
	}
	vti.krajevno = *requested
	vti.bound = true
	return 0
}

func vtiPoveži(fd int32, address_2 uint32, dolžina uint32) int32 {
	vti, napaka := vtiforfd(fd)
	if napaka != 0 {
		return napaka
	}
	oddaljeno, napaka := vtiaddress(address_2, dolžina)
	if napaka != 0 {
		return napaka
	}
	if !vti.bound {
		if napaka := bindephemeral(vti); napaka != 0 {
			return napaka
		}
	}
	vti.oddaljeno = *oddaljeno
	vti.connected = true
	return 0
}

func vtiPošljito(fd int32, bufferaddress_2 uint32, dolžina uint32, ciljaddress uint32, ciljDolžina uint32) int32 {
	vti, napaka := vtiforfd(fd)
	if napaka != 0 {
		return napaka
	}
	if dolžina > maxdatagramVelikost {
		return Emsgsize
	}
	if dolžina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var cilj vtiaddressipv4
	if ciljaddress != 0 {
		address_2, addressNapaka := vtiaddress(ciljaddress, ciljDolžina)
		if addressNapaka != 0 {
			return addressNapaka
		}
		cilj = *address_2
	} else {
		if !vti.connected {
			return Enotconn
		}
		cilj = vti.oddaljeno
	}
	if !vti.bound {
		if bindNapaka := bindephemeral(vti); bindNapaka != 0 {
			return bindNapaka
		}
	}
	var receiver *krajevnodatagramVti
	for i := 0; i < maxsockets; i++ {
		candidate := &krajevnosockets[i]
		if candidate.uporabljeno && candidate.bound && candidate.krajevno.Vrata == cilj.Vrata &&
			(candidate.krajevno.Address == 0 || candidate.krajevno.Address == cilj.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxVtipaketov {
		return Eagain
	}
	packet := &receiver.paketov[receiver.tail]
	*packet = vtipacket{uporabljeno: true, velikost: dolžina, vir: vti.krajevno}
	if dolžina != 0 {
		vir := GetBajtovfromKazalnik(uintptr(bufferaddress_2), int(dolžina), int(dolžina))
		copy(packet.data[:dolžina], vir)
	}
	receiver.tail = (receiver.tail + 1) % maxVtipaketov
	receiver.count++
	return int32(dolžina)
}

func vtireceivefrom(fd int32, bufferaddress_2 uint32, dolžina uint32, viraddress uint32, virDolžinaaddress uint32) int32 {
	vti, napaka := vtiforfd(fd)
	if napaka != 0 {
		return napaka
	}
	if dolžina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if vti.count == 0 {
		return Eagain
	}
	packet := &vti.paketov[vti.head]
	kopirajDolžina := packet.velikost
	if kopirajDolžina > dolžina {
		kopirajDolžina = dolžina
	}
	if kopirajDolžina != 0 {
		cilj := GetBajtovfromKazalnik(uintptr(bufferaddress_2), int(kopirajDolžina), int(kopirajDolžina))
		copy(cilj, packet.data[:kopirajDolžina])
	}
	if viraddress != 0 {
		if virDolžinaaddress == 0 {
			return Efault
		}
		providedDolžina := (*uint32)(Pointer(uintptr(virDolžinaaddress)))
		if *providedDolžina >= 16 {
			*(*vtiaddressipv4)(Pointer(uintptr(viraddress))) = packet.vir
		}
		*providedDolžina = 16
	}
	*packet = vtipacket{}
	vti.head = (vti.head + 1) % maxVtipaketov
	vti.count--
	return int32(kopirajDolžina)
}

func kopirajVtiIme(fd int32, address_2 uint32, dolžinaaddress uint32, peer bool) int32 {
	vti, napaka := vtiforfd(fd)
	if napaka != 0 {
		return napaka
	}
	if address_2 == 0 || dolžinaaddress == 0 {
		return Efault
	}
	dolžina := (*uint32)(Pointer(uintptr(dolžinaaddress)))
	if *dolžina < 16 {
		*dolžina = 16
		return Einval
	}
	if peer {
		if !vti.connected {
			return Enotconn
		}
		*(*vtiaddressipv4)(Pointer(uintptr(address_2))) = vti.oddaljeno
	} else {
		if !vti.bound {
			if bindNapaka := bindephemeral(vti); bindNapaka != 0 {
				return bindNapaka
			}
		}
		*(*vtiaddressipv4)(Pointer(uintptr(address_2))) = vti.krajevno
	}
	*dolžina = 16
	return 0
}

func sysVticall(call uint32, argumenti_2 uint32) int32 {
	if argumenti_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateVti(vticallargument(argumenti_2, 0), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2))
	case 2:
		return vtibind(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2))
	case 3:
		return vtiPoveži(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopirajVtiIme(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2), false)
	case 7:
		return kopirajVtiIme(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2), true)
	case 9:
		return vtiPošljito(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2), 0, 0)
	case 10:
		return vtireceivefrom(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2), 0, 0)
	case 11:
		return vtiPošljito(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2), vticallargument(argumenti_2, 4), vticallargument(argumenti_2, 5))
	case 12:
		return vtireceivefrom(int32(vticallargument(argumenti_2, 0)), vticallargument(argumenti_2, 1), vticallargument(argumenti_2, 2), vticallargument(argumenti_2, 4), vticallargument(argumenti_2, 5))
	case 13:
		if _, napaka := vtiforfd(int32(vticallargument(argumenti_2, 0))); napaka != 0 {
			return napaka
		}
		return 0
	case 14:
		if _, napaka := vtiforfd(int32(vticallargument(argumenti_2, 0))); napaka != 0 {
			return napaka
		}
		return 0
	}
	return Eopnotsupp
}

func branjestdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBajtovfromKazalnik(uintptr(address), int(count), int(count))
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
	naslednje := (stdinPisanje + 1) % uint32(len(stdinbuffer))
	if naslednje == stdinBranje {
		return
	}
	stdinbuffer[stdinPisanje] = c
	stdinPisanje = naslednje
}

func stdingetblocking() byte {
	for stdinBranje == stdinPisanje {
		sc := pollTipkovnicascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinBranje]
	stdinBranje = (stdinBranje + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTipkovnicascancode() byte {
	for (VrataBranjebyte(0x64) & 0x01) == 0 {
	}
	sc := VrataBranjebyte(0x60)
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

func kopirajIzvedljivovector(address_2 uint32, rEZULTAT *izvedljivovector) int32 {
	*rEZULTAT = izvedljivovector{}
	if address_2 == 0 {
		return 0
	}
	for kazalo := uint32(0); kazalo < maxIzvedljivovectorvnos; kazalo++ {
		nizaddress := *(*uint32)(Pointer(uintptr(address_2 + kazalo*4)))
		if nizaddress == 0 {
			rEZULTAT.count = kazalo
			return 0
		}
		terminated := false
		for dolžina := uint32(0); dolžina <= maxIzvedljivoNizDolžina; dolžina++ {
			vrednost := *(*byte)(Pointer(uintptr(nizaddress + dolžina)))
			rEZULTAT.values[kazalo][dolžina] = vrednost
			if vrednost == 0 {
				rEZULTAT.lengths[kazalo] = dolžina
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

func pushIzvedljivounsignedinteger32(stack *uint32, vrednost uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = vrednost
}

func setupIzvedljivostack(cPE *TcpuStanje, argumenti_2 *izvedljivovector, environment *izvedljivovector) int32 {
	const stackBajtov uint32 = 4096
	if !MakeObmočjeZasebnowritable(getcr3(), UporabnikstackVrh-stackBajtov, stackBajtov) {
		return Enomem
	}
	stack := UporabnikstackVrh
	var argumentpointers [maxIzvedljivovectorvnos]uint32
	var environmentpointers [maxIzvedljivovectorvnos]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		dolžina := environment.lengths[i] + 1
		stack -= dolžina
		cilj := GetBajtovfromKazalnik(uintptr(stack), int(dolžina), int(dolžina))
		copy(cilj, environment.values[i][:dolžina])
		environmentpointers[i] = stack
	}
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		dolžina := argumenti_2.lengths[i] + 1
		stack -= dolžina
		cilj := GetBajtovfromKazalnik(uintptr(stack), int(dolžina), int(dolžina))
		copy(cilj, argumenti_2.values[i][:dolžina])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushIzvedljivounsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushIzvedljivounsignedinteger32(&stack, environmentpointers[i])
	}
	pushIzvedljivounsignedinteger32(&stack, 0)
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		pushIzvedljivounsignedinteger32(&stack, argumentpointers[i])
	}
	pushIzvedljivounsignedinteger32(&stack, argumenti_2.count)
	cPE.Esp = stack
	cPE.Ebp = 0
	return 0
}

func zapriVključenoIzvedljivo(opravilo *opravilovnos) {
	if opravilo == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if opravilo.fds[fd].uporabljeno && (opravilo.fds[fd].fdZastavice&fdcloexec) != 0 {
			zapriOpravilofd(opravilo, fd)
		}
	}
}

func sysexecve(cPE *TcpuStanje, pOTaddress uint32) int32 {
	if pOTaddress == 0 {
		return Efault
	}
	var argumenti_2 izvedljivovector
	var environment izvedljivovector
	if rEZULTAT := kopirajIzvedljivovector(cPE.Ecx, &argumenti_2); rEZULTAT < 0 {
		return rEZULTAT
	}
	if rEZULTAT := kopirajIzvedljivovector(cPE.Edx, &environment); rEZULTAT < 0 {
		return rEZULTAT
	}
	imelen, ime := kopirajPOT(pOTaddress)
	if imelen == 0 {
		return Enoent
	}
	velikost := datotekaVelikost(ime[:imelen])
	if velikost == 0 {
		return Enoent
	}
	pomnilnikmanager := &mem.TPomnilnikmanager{}
	datotekaKazalnik := pomnilnikmanager.Malloc(velikost)
	if datotekaKazalnik == nil {
		return Einval
	}
	data := GetBajtovfromKazalnik(uintptr(datotekaKazalnik), int(velikost), int(velikost))
	branjeDatoteka(ime[:imelen], data)
	if velikost < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		pomnilnikmanager.Prosto(datotekaKazalnik)
		return Enoexec
	}
	loader := Elf{}
	vnos := loader.Getvnos(data)
	loader.Parse(data, getcr3())
	pomnilnikmanager.Prosto(datotekaKazalnik)
	if rEZULTAT := setupIzvedljivostack(cPE, &argumenti_2, &environment); rEZULTAT < 0 {
		return rEZULTAT
	}
	zapriVključenoIzvedljivo(ensurecurrentOpravilo())
	cPE.Eip = vnos
	cPE.Eax = 0
	return 0
}

func sysfork(cPE *TcpuStanje) int32 {
	nadrejenipredmetpid := Currentpid()
	if ensurecurrentOpravilo() == nil {
		return Enfile
	}
	pid := allocateOpravilo(nadrejenipredmetpid)
	if pid == 0 {
		return Einval
	}
	pomnilnikmanager := &mem.TPomnilnikmanager{}
	threadKazalnik := pomnilnikmanager.Malloc(uint32(Sizeof(TThread{})))
	stackKazalnik := pomnilnikmanager.Malloc(ThreadstackVelikost)
	podrejenipredmetStranMapa := CloneaddressPresledekcow(getcr3())
	if threadKazalnik == nil || stackKazalnik == nil || podrejenipredmetStranMapa == 0 {
		zavrziOpravilo(pid)
		return Einval
	}
	podrejenipredmet := (*TThread)(threadKazalnik)
	podrejenipredmet.Stack = uint32(uintptr(stackKazalnik))
	podrejenipredmet.CPEStanje = (*TcpuStanje)(Pointer(uintptr(stackKazalnik) + ThreadstackVelikost - Sizeof(TcpuStanje{})))
	*podrejenipredmet.CPEStanje = *cPE
	podrejenipredmet.CPEStanje.Eax = 0
	podrejenipredmet.Uporabnikstack_2 = cPE.Esp
	podrejenipredmet.UporabnikstackVelikost_2 = 0
	podrejenipredmet.Pid = pid
	podrejenipredmet.Nadrejenipredmetpid = nadrejenipredmetpid
	podrejenipredmet.StranMapavnos = podrejenipredmetStranMapa
	podrejenipredmet.ThreadStanje = Pripravljen
	podrejenipredmet.Fpuoffset = 0xffffffff
	podrejenipredmet.Iskernel = false
	Dodajrunnablethread(podrejenipredmet)
	return int32(pid)
}

func sysIzhod(stanje uint32) {
	pid := Currentpid()
	for i := 0; i < len(opraviloPreglednica); i++ {
		if opraviloPreglednica[i].uporabljeno && opraviloPreglednica[i].pid == pid {
			zapriVseOpravilofds(&opraviloPreglednica[i])
			opraviloPreglednica[i].končal = true
			opraviloPreglednica[i].stanje = (stanje & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, stanjeaddress uint32, možnosti uint32) int32 {
	if (možnosti & ^uint32(1)) != 0 {
		return Einval
	}
	nadrejenipredmetpid := Currentpid()
	foundpodrejenipredmet := false
	for i := 0; i < len(opraviloPreglednica); i++ {
		p := &opraviloPreglednica[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.uporabljeno && matches && p.nadrejenipredmet == nadrejenipredmetpid {
			foundpodrejenipredmet = true
			if p.končal {
				if stanjeaddress != 0 {
					*(*uint32)(Pointer(uintptr(stanjeaddress))) = p.stanje
				}
				podrejenipredmetpid := p.pid
				*p = opravilovnos{}
				return int32(podrejenipredmetpid)
			}
		}
	}
	if !foundpodrejenipredmet {
		return Echild
	}

	if (možnosti & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateOpravilo(nadrejenipredmet uint32) uint32 {
	nadrejenipredmetOpravilo := najdiOpravilo(nadrejenipredmet)
	pid := Allocatepid()
	for i := 0; i < len(opraviloPreglednica); i++ {
		if !opraviloPreglednica[i].uporabljeno {
			opraviloPreglednica[i] = opravilovnos{
				uporabljeno:		true,
				pid:			pid,
				nadrejenipredmet:	nadrejenipredmet,
				programbreak:		uporabnikheapbase,
			}
			if nadrejenipredmetOpravilo != nil {
				opraviloPreglednica[i].programbreak = nadrejenipredmetOpravilo.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if nadrejenipredmetOpravilo.fds[fd].uporabljeno {
						opraviloPreglednica[i].fds[fd] = nadrejenipredmetOpravilo.fds[fd]
						opis := nadrejenipredmetOpravilo.fds[fd].opis
						if opis >= 0 && opis < maxOdpriDatoteke {
							odpriDatotekaPreglednica[opis].refs++
						}
					}
				}
			} else {
				initializeOpravilofds(&opraviloPreglednica[i])
			}
			return pid
		}
	}
	return 0
}

func zapriVseOpravilofds(opravilo *opravilovnos) {
	if opravilo == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if opravilo.fds[fd].uporabljeno {
			zapriOpravilofd(opravilo, fd)
		}
	}
}

func zavrziOpravilo(pid uint32) {
	opravilo := najdiOpravilo(pid)
	if opravilo == nil {
		return
	}
	zapriVseOpravilofds(opravilo)
	*opravilo = opravilovnos{}
}

func kopirajPOT(pOTaddress uint32) (uint32, [12]byte) {
	var ime [12]byte
	if pOTaddress == 0 {
		return 0, ime
	}
	raw := GetBajtovfromKazalnik(uintptr(pOTaddress), 64, 64)
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
		ime[n] = c
		n++
	}
	return n, ime
}

func datotekaVelikost(imedatoteke []byte) uint32 {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionPreglednica{}
	partition.Branjepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	velikost := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	ata0s.Flush()
	return velikost
}

func branjeDatoteka(imedatoteke []byte, data []byte) {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionPreglednica{}
	partition.Branjepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Branje(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)
	ata0s.Flush()
}

func getcr3() uint32
