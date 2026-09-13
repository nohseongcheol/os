package sustavcall

import . "unsafe"

import . "prekid"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "datotekaSustav/msdospartition"
import . "datotekaSustav/fat"
import . "datotekaSustav/elf"
import mem "memorijamanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualnoMemorija"

var console_2 = TConsole{}

type TSyscall struct {
	TPrekidhandler
}

const (
	SysIzađi	uint32	= 1
	Sysfork		uint32	= 2
	SysČitaj	uint32	= 3
	SysZapiši	uint32	= 4
	SysOtvori	uint32	= 5
	SysZatvori	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syspristup	uint32	= 33
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
	SysrtIzađi	uint32	= 252

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
	maksfd				= 32
	maksOtvoriDatoteke		= 128
)

type fdentry struct {
	iskorišteno	bool
	opis		int32
	fdZastavice	uint32
}

type otvoriDatotekaOpis struct {
	iskorišteno	bool
	refs		uint32
	kind		uint32
	zastavice	uint32
	pozicija	uint32
	veličina	uint32
	ime		[12]byte
	imelen		uint32
	aux		uint32
}

const (
	fdkindNijedan		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindKorijenDirektorij	uint32	= 4
	fdkindUtorsocket	uint32	= 5

	oČitajonly	uint32	= 0
	oZapišionly	uint32	= 1
	oČitajZapiši	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oDirektorij	uint32	= 0x10000

	seekPostavi	uint32	= 0
	seekTrenutno	uint32	= 1
	seekKraj	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fPostavifd	uint32	= 2
	fgetfl		uint32	= 3
	fPostavifl	uint32	= 4
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
	makssockets		= 32
	maksUtorsocketpaketi	= 8
	maksdatagramVeličina	= 512
)

type utorsocketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type utorsocketpacket struct {
	iskorišteno	bool
	veličina	uint32
	izvor		utorsocketaddressipv4
	data		[maksdatagramVeličina]byte
}

type localdatagramUtorsocket struct {
	iskorišteno	bool
	bound		bool
	connected	bool
	local		utorsocketaddressipv4
	udaljeno	utorsocketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	paketi		[maksUtorsocketpaketi]utorsocketpacket
}

type posixstat struct {
	Uređaj		uint32
	Ino		uint32
	NAČIN		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Veličina_2	int32
	Blksize		int32
	Blokiraj	int32
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
	Inačica		[65]byte
	Machine		[65]byte
}

const (
	maksIzvršivectorentry		= 16
	maksIzvršiZnakovninizDužina	= 63
)

type izvršivector struct {
	count		uint32
	lengths		[maksIzvršivectorentry]uint32
	vrijednosti	[maksIzvršivectorentry][maksIzvršiZnakovninizDužina + 1]byte
}

type procesentry struct {
	iskorišteno	bool
	pid		uint32
	roditelj	uint32
	exited		bool
	stanje		uint32
	programbreak	uint32
	fds		[maksfd]fdentry
}

type znakovninizheader struct {
	Data	uintptr
	Len	int
}

func syscallGreška(greška int32) uint32 {
	return *(*uint32)(Pointer(&greška))
}

var otvoriDatotekaTablica [maksOtvoriDatoteke]otvoriDatotekaOpis
var procesTablica [32]procesentry
var localsockets [makssockets]localdatagramUtorsocket
var slijedećeephemeralport uint16 = 49152

const (
	korisnikheapbase	uint32	= 0x06000000
	korisnikheapOgraničenje	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinČitaj uint32
var stdinZapiši uint32

func Prekid(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIzađi_2(kazalo uint32) {
	Syscall(SysIzađi, kazalo)
}

func SysČitaj_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysČitaj, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysIspisstr(buffer string) {
	h := (*znakovninizheader)(Pointer(&buffer))
	Syscall(SysZapiši, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysIspisunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysZapiši, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOtvori_2(pUTANJA uintptr, zastavice uint32, nAČIN uint32) int32 {
	return int32(Syscall(SysOtvori, uint32(pUTANJA), zastavice, nAČIN))
}

func SysZatvori_2(fd uint32) int32 {
	return int32(Syscall(SysZatvori, fd))
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
		return Prekid(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Prekid(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Prekid(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Prekid(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Prekid(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Prekid(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallGreška(Enosys)
	}
}

func (sam *TSyscall) Init(manager *TPrekidmanager) {
	initDatotekadescriptor()

	prekidhandler = ručkaPrekid

	var address uintptr
	address = uintptr(Pointer(&prekidhandler))

	sam.TPrekidhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var prekidhandler func(uint32) uint32

func ručkaPrekid(esp uint32) uint32 {
	var procesor = (*TcpuStanje)(Pointer(uintptr(esp)))

	switch procesor.Eax {
	case SysIzađi:
		sysIzađi(procesor.Ebx)
		return uint32(uintptr(Pointer(ZaustaviTrenutnothread(procesor))))
	case SysrtIzađi:
		sysIzađi(procesor.Ebx)
		return uint32(uintptr(Pointer(ZaustaviTrenutnothread(procesor))))
	case Sysfork:
		procesor.Eax = uint32(sysfork(procesor))
		return esp
	case SysČitaj:
		procesor.Eax = uint32(sysČitaj(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysZapiši:
		procesor.Eax = uint32(sysZapiši(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysOtvori:
		procesor.Eax = uint32(sysOtvori(procesor.Ebx, procesor.Ecx, procesor.Edx))
		return esp
	case Syscreat:
		procesor.Eax = uint32(sysOtvori(procesor.Ebx, ocreate|oZapišionly|otruncate, procesor.Ecx))
		return esp
	case SysZatvori:
		procesor.Eax = uint32(sysZatvori(int32(procesor.Ebx)))
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
		procesor.Eax = Trenutnopid()
		return esp
	case Sysgetppid:
		procesor.Eax = Trenutnoroditeljpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		procesor.Eax = 0
		return esp
	case Syspristup:
		procesor.Eax = uint32(syspristup(procesor.Ebx, procesor.Ecx))
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
		procesor.Eax = uint32(sysUtorsocketcall(procesor.Ebx, procesor.Ecx))
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
		console_2.MUnsignedinteger32Ispis(procesor.Ebx)
		return esp

	default:
		console_2.MIspisxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Ispis(esp)
		console_2.MIspis(([]byte)(":"))
		console_2.MUnsignedinteger32Ispis(procesor.Eax)
		console_2.MIspis(([]byte)(":"))
		console_2.MUnsignedinteger32Ispis(procesor.Ebx)
		console_2.MIspis(([]byte)(":"))
		console_2.MUnsignedinteger32Ispis(procesor.Ecx)
		console_2.MIspis(([]byte)(":"))
		console_2.MUnsignedinteger32Ispis(procesor.Edx)
		console_2.MIspis(([]byte)("]"))
		procesor.Eax = syscallGreška(Enosys)
		return esp
	}

	return esp
}

func initDatotekadescriptor() {
	for i := 0; i < maksOtvoriDatoteke; i++ {
		otvoriDatotekaTablica[i] = otvoriDatotekaOpis{}
	}
	for i := 0; i < len(procesTablica); i++ {
		procesTablica[i] = procesentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramUtorsocket{}
	}
	slijedećeephemeralport = 49152
	otvoriDatotekaTablica[0] = otvoriDatotekaOpis{iskorišteno: true, kind: fdkindstdin, zastavice: oČitajonly}
	otvoriDatotekaTablica[1] = otvoriDatotekaOpis{iskorišteno: true, kind: fdkindconsole, zastavice: oZapišionly}
	otvoriDatotekaTablica[2] = otvoriDatotekaOpis{iskorišteno: true, kind: fdkindconsole, zastavice: oZapišionly}
}

func nađiProces(pid uint32) *procesentry {
	for i := 0; i < len(procesTablica); i++ {
		if procesTablica[i].iskorišteno && procesTablica[i].pid == pid {
			return &procesTablica[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procesentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		proces.fds[fd] = fdentry{iskorišteno: true, opis: fd}
		otvoriDatotekaTablica[fd].refs++
	}
}

func ensureTrenutnoProces() *procesentry {
	pid := Trenutnopid()
	if proces := nađiProces(pid); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTablica); i++ {
		if !procesTablica[i].iskorišteno {
			procesTablica[i] = procesentry{
				iskorišteno:	true,
				pid:		pid,
				roditelj:	Trenutnoroditeljpid(),
				programbreak:	korisnikheapbase,
			}
			initializeProcesfds(&procesTablica[i])
			return &procesTablica[i]
		}
	}
	return nil
}

func getOtvoriDatotekafor(proces *procesentry, fd int32) *otvoriDatotekaOpis {
	if proces == nil || fd < 0 || fd >= maksfd || !proces.fds[fd].iskorišteno {
		return nil
	}
	opis := proces.fds[fd].opis
	if opis < 0 || opis >= maksOtvoriDatoteke || !otvoriDatotekaTablica[opis].iskorišteno {
		return nil
	}
	return &otvoriDatotekaTablica[opis]
}

func getOtvoriDatoteka(fd int32) *otvoriDatotekaOpis {
	return getOtvoriDatotekafor(ensureTrenutnoProces(), fd)
}

func allocateOtvoriDatoteka() int32 {
	for i := int32(3); i < maksOtvoriDatoteke; i++ {
		if !otvoriDatotekaTablica[i].iskorišteno {
			otvoriDatotekaTablica[i] = otvoriDatotekaOpis{iskorišteno: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(proces *procesentry, opis int32, najniže int32) int32 {
	if proces == nil {
		return Enfile
	}
	if najniže < 0 || najniže >= maksfd {
		return Einval
	}
	for fd := najniže; fd < maksfd; fd++ {
		if !proces.fds[fd].iskorišteno {
			proces.fds[fd] = fdentry{iskorišteno: true, opis: opis}
			return fd
		}
	}
	return Emfile
}

func releaseOtvoriDatoteka(opis int32) {
	if opis < 0 || opis >= maksOtvoriDatoteke {
		return
	}
	entry := &otvoriDatotekaTablica[opis]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && opis > stderrfd {
		if entry.kind == fdkindUtorsocket && entry.aux < makssockets {
			localsockets[entry.aux] = localdatagramUtorsocket{}
		}
		*entry = otvoriDatotekaOpis{}
	}
}

func zatvoriProcesfd(proces *procesentry, fd int32) int32 {
	if proces == nil || getOtvoriDatotekafor(proces, fd) == nil {
		return Ebadf
	}
	opis := proces.fds[fd].opis
	proces.fds[fd] = fdentry{}
	releaseOtvoriDatoteka(opis)
	return 0
}

func sysZapiši(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getOtvoriDatoteka(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindUtorsocket {
			return utorsocketPošaljito(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindKorijenDirektorij {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBajtovafromPokazivač(uintptr(address), int(count), int(count))
	console_2.MIspis(buffer)
	return int32(count)
}

func sysČitaj(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getOtvoriDatoteka(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return čitajstdin(address, count)
	}
	if entry.kind == fdkindKorijenDirektorij {
		return Eisdir
	}
	if entry.kind == fdkindUtorsocket {
		return utorsocketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.pozicija >= entry.veličina {
		return 0
	}
	remaining := entry.veličina - entry.pozicija
	if count > remaining {
		count = remaining
	}
	buffer := GetBajtovafromPokazivač(uintptr(address), int(count), int(count))
	return čitajvfsDatoteka(entry, buffer, count)
}

func sysOtvori(pUTANJAaddress uint32, zastavice uint32, nAČIN uint32) int32 {
	_ = nAČIN
	if pUTANJAaddress == 0 {
		return Efault
	}
	pristupNAČIN := zastavice & 3
	if pristupNAČIN == oZapišionly || pristupNAČIN == oČitajZapiši || (zastavice&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	proces := ensureTrenutnoProces()
	if proces == nil {
		return Enfile
	}
	opis := allocateOtvoriDatoteka()
	if opis < 0 {
		return opis
	}
	entry := &otvoriDatotekaTablica[opis]
	entry.zastavice = zastavice
	if isKorijenPUTANJA(pUTANJAaddress) {
		entry.kind = fdkindKorijenDirektorij
		entry.veličina = 0
	} else {
		imelen, ime := kopirajPUTANJA(pUTANJAaddress)
		if imelen == 0 {
			*entry = otvoriDatotekaOpis{}
			return Enoent
		}
		veličina := datotekaVeličina(ime[:imelen])
		if veličina == 0 {
			*entry = otvoriDatotekaOpis{}
			return Enoent
		}
		if (zastavice & oDirektorij) != 0 {
			*entry = otvoriDatotekaOpis{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.veličina = veličina
		entry.imelen = imelen
		entry.ime = ime
	}

	fd := allocatefd(proces, opis, 3)
	if fd < 0 {
		*entry = otvoriDatotekaOpis{}
		return fd
	}
	return fd
}

func sysZatvori(fd int32) int32 {
	return zatvoriProcesfd(ensureTrenutnoProces(), fd)
}

func sysdup(fd int32, najniže int32) int32 {
	proces := ensureTrenutnoProces()
	entry := getOtvoriDatotekafor(proces, fd)
	if entry == nil {
		return Ebadf
	}
	novifd := allocatefd(proces, proces.fds[fd].opis, najniže)
	if novifd >= 0 {
		entry.refs++
	}
	return novifd
}

func sysdup2(oldfd int32, novifd int32) int32 {
	proces := ensureTrenutnoProces()
	entry := getOtvoriDatotekafor(proces, oldfd)
	if entry == nil {
		return Ebadf
	}
	if novifd < 0 || novifd >= maksfd {
		return Ebadf
	}
	if oldfd == novifd {
		return novifd
	}
	if proces.fds[novifd].iskorišteno {
		zatvoriProcesfd(proces, novifd)
	}
	proces.fds[novifd] = fdentry{iskorišteno: true, opis: proces.fds[oldfd].opis}
	entry.refs++
	return novifd
}

func sysfcntl(fd int32, naredba uint32, argument uint32) int32 {
	proces := ensureTrenutnoProces()
	entry := getOtvoriDatotekafor(proces, fd)
	if entry == nil {
		return Ebadf
	}
	switch naredba {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(proces.fds[fd].fdZastavice)
	case fPostavifd:
		proces.fds[fd].fdZastavice = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.zastavice)
	case fPostavifl:
		entry.zastavice = (entry.zastavice & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getOtvoriDatoteka(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekPostavi:
		base = 0
	case seekTrenutno:
		base = int64(entry.pozicija)
	case seekKraj:
		base = int64(entry.veličina)
	default:
		return Einval
	}
	pozicija_2 := base + int64(offset)
	if pozicija_2 < 0 || pozicija_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.pozicija = uint32(pozicija_2)
	return int32(entry.pozicija)
}

func čitajvfsDatoteka(entry *otvoriDatotekaOpis, odredište_2 []byte, count uint32) int32 {
	memorijamanager := &mem.TMemorijamanager{}
	tmpPokazivač := memorijamanager.Malloc(entry.veličina)
	if tmpPokazivač == nil {
		return Einval
	}
	tmp := GetBajtovafromPokazivač(uintptr(tmpPokazivač), int(entry.veličina), int(entry.veličina))
	čitajDatoteka(entry.ime[:entry.imelen], tmp)
	copy(odredište_2[:count], tmp[entry.pozicija:entry.pozicija+count])
	entry.pozicija += count
	memorijamanager.Slobodno(tmpPokazivač)
	return int32(count)
}

func isKorijenPUTANJA(pUTANJAaddress uint32) bool {
	if pUTANJAaddress == 0 {
		return false
	}
	pUTANJA := GetBajtovafromPokazivač(uintptr(pUTANJAaddress), 4, 4)
	if pUTANJA[0] == '/' && pUTANJA[1] == 0 {
		return true
	}
	if pUTANJA[0] == '.' && pUTANJA[1] == 0 {
		return true
	}
	if pUTANJA[0] == '/' && pUTANJA[1] == '.' && pUTANJA[2] == 0 {
		return true
	}
	return false
}

func syspristup(pUTANJAaddress uint32, nAČIN uint32) int32 {
	if pUTANJAaddress == 0 {
		return Efault
	}
	if (nAČIN & ^uint32(7)) != 0 {
		return Einval
	}
	isKorijen := isKorijenPUTANJA(pUTANJAaddress)
	exists := isKorijen
	if !exists {
		imelen, ime := kopirajPUTANJA(pUTANJAaddress)
		exists = imelen != 0 && datotekaVeličina(ime[:imelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (nAČIN & 2) != 0 {
		return Eacces
	}

	if (nAČIN&1) != 0 && !isKorijen {
		return Eacces
	}
	return 0
}

func syschdir(pUTANJAaddress uint32) int32 {
	if pUTANJAaddress == 0 {
		return Efault
	}
	if !isKorijenPUTANJA(pUTANJAaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, veličina uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if veličina < 2 {
		return Erange
	}
	buffer_2 := GetBajtovafromPokazivač(uintptr(bufferaddress), int(veličina), int(veličina))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, nAČIN uint32, veličina uint32, indeksničvor uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Uređaj = 1
	stat.Ino = indeksničvor
	stat.NAČIN = nAČIN
	stat.Nlink = 1
	stat.Veličina_2 = int32(veličina)
	stat.Blksize = 512
	stat.Blokiraj = int32((veličina + 511) / 512)
	return 0
}

func sysstat(pUTANJAaddress uint32, stataddress uint32) int32 {
	if pUTANJAaddress == 0 {
		return Efault
	}
	if isKorijenPUTANJA(pUTANJAaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	imelen, ime := kopirajPUTANJA(pUTANJAaddress)
	if imelen == 0 {
		return Enoent
	}
	veličina := datotekaVeličina(ime[:imelen])
	if veličina == 0 {
		return Enoent
	}
	indeksničvor := uint32(2)
	for i := uint32(0); i < imelen; i++ {
		indeksničvor = indeksničvor*33 + uint32(ime[i])
	}
	return fillposixstat(stataddress, sifreg|0444, veličina, indeksničvor)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getOtvoriDatoteka(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindKorijenDirektorij:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.veličina, uint32(fd+2))
	case fdkindUtorsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getOtvoriDatoteka(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proces := ensureTrenutnoProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = korisnikheapbase
	}
	if address_2 == 0 {
		return proces.programbreak
	}
	if address_2 < korisnikheapbase || address_2 > korisnikheapOgraničenje {
		return proces.programbreak
	}
	proces.programbreak = address_2
	return proces.programbreak
}

func kopirajutsfield(odredište *[65]byte, vrijednost string) {
	ograničenje := len(vrijednost)
	if ograničenje > 64 {
		ograničenje = 64
	}
	for i := 0; i < ograničenje; i++ {
		odredište[i] = vrijednost[i]
	}
	odredište[ograničenje] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	ime := (*posixutsname)(Pointer(uintptr(address_2)))
	*ime = posixutsname{}
	kopirajutsfield(&ime.Sysname, "EngOS")
	kopirajutsfield(&ime.Nodename, "engos")
	kopirajutsfield(&ime.Release, "0.1-posix")
	kopirajutsfield(&ime.Inačica, "POSIX.1-2017 phase 1")
	kopirajutsfield(&ime.Machine, "i386")
	return 0
}

func swapunsignedinteger16(vrijednost uint16) uint16 {
	return (vrijednost << 8) | (vrijednost >> 8)
}

func utorsocketcallargument(argumenti_2 uint32, kazalo uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenti_2 + kazalo*4)))
}

func utorsocketforfd(fd int32) (*localdatagramUtorsocket, int32) {
	entry := getOtvoriDatoteka(fd)
	if entry == nil || entry.kind != fdkindUtorsocket || entry.aux >= makssockets {
		return nil, Ebadf
	}
	utorsocket := &localsockets[entry.aux]
	if !utorsocket.iskorišteno {
		return nil, Ebadf
	}
	return utorsocket, 0
}

func allocateUtorsocket(domena uint32, utorsocketVrsta uint32, protocol uint32) int32 {
	if domena != afinet {
		return Eafnosupport
	}
	if utorsocketVrsta != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureTrenutnoProces()
	if proces == nil {
		return Enfile
	}
	utorsocketKazalo := -1
	for i := 0; i < makssockets; i++ {
		if !localsockets[i].iskorišteno {
			utorsocketKazalo = i
			break
		}
	}
	if utorsocketKazalo < 0 {
		return Enfile
	}
	opis := allocateOtvoriDatoteka()
	if opis < 0 {
		return opis
	}
	localsockets[utorsocketKazalo] = localdatagramUtorsocket{iskorišteno: true}
	entry := &otvoriDatotekaTablica[opis]
	entry.kind = fdkindUtorsocket
	entry.zastavice = oČitajZapiši
	entry.aux = uint32(utorsocketKazalo)
	fd := allocatefd(proces, opis, 3)
	if fd < 0 {
		localsockets[utorsocketKazalo] = localdatagramUtorsocket{}
		*entry = otvoriDatotekaOpis{}
		return fd
	}
	return fd
}

func utorsocketaddress(address_2 uint32, dužina uint32) (*utorsocketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if dužina < 16 {
		return nil, Einval
	}
	rEZULTAT := (*utorsocketaddressipv4)(Pointer(uintptr(address_2)))
	if rEZULTAT.Family != afinet {
		return nil, Eafnosupport
	}
	return rEZULTAT, 0
}

func portPovećajKoristi(port uint16, except *localdatagramUtorsocket) bool {
	for i := 0; i < makssockets; i++ {
		utorsocket := &localsockets[i]
		if utorsocket != except && utorsocket.iskorišteno && utorsocket.bound && utorsocket.local.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(utorsocket *localdatagramUtorsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(slijedećeephemeralport)
		slijedećeephemeralport++
		if slijedećeephemeralport < 49152 {
			slijedećeephemeralport = 49152
		}
		if !portPovećajKoristi(port, utorsocket) {
			utorsocket.local = utorsocketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			utorsocket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func utorsocketbind(fd int32, address_2 uint32, dužina uint32) int32 {
	utorsocket, greška := utorsocketforfd(fd)
	if greška != 0 {
		return greška
	}
	requested, greška := utorsocketaddress(address_2, dužina)
	if greška != 0 {
		return greška
	}
	if utorsocket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(utorsocket)
	}
	if portPovećajKoristi(requested.Port, utorsocket) {
		return Eaddrinuse
	}
	utorsocket.local = *requested
	utorsocket.bound = true
	return 0
}

func utorsocketSpojise(fd int32, address_2 uint32, dužina uint32) int32 {
	utorsocket, greška := utorsocketforfd(fd)
	if greška != 0 {
		return greška
	}
	udaljeno, greška := utorsocketaddress(address_2, dužina)
	if greška != 0 {
		return greška
	}
	if !utorsocket.bound {
		if greška := bindephemeral(utorsocket); greška != 0 {
			return greška
		}
	}
	utorsocket.udaljeno = *udaljeno
	utorsocket.connected = true
	return 0
}

func utorsocketPošaljito(fd int32, bufferaddress_2 uint32, dužina uint32, odredišteaddress uint32, odredišteDužina uint32) int32 {
	utorsocket, greška := utorsocketforfd(fd)
	if greška != 0 {
		return greška
	}
	if dužina > maksdatagramVeličina {
		return Emsgsize
	}
	if dužina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var odredište utorsocketaddressipv4
	if odredišteaddress != 0 {
		address_2, addressGreška := utorsocketaddress(odredišteaddress, odredišteDužina)
		if addressGreška != 0 {
			return addressGreška
		}
		odredište = *address_2
	} else {
		if !utorsocket.connected {
			return Enotconn
		}
		odredište = utorsocket.udaljeno
	}
	if !utorsocket.bound {
		if bindGreška := bindephemeral(utorsocket); bindGreška != 0 {
			return bindGreška
		}
	}
	var receiver *localdatagramUtorsocket
	for i := 0; i < makssockets; i++ {
		candidate := &localsockets[i]
		if candidate.iskorišteno && candidate.bound && candidate.local.Port == odredište.Port &&
			(candidate.local.Address == 0 || candidate.local.Address == odredište.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksUtorsocketpaketi {
		return Eagain
	}
	packet := &receiver.paketi[receiver.tail]
	*packet = utorsocketpacket{iskorišteno: true, veličina: dužina, izvor: utorsocket.local}
	if dužina != 0 {
		izvor := GetBajtovafromPokazivač(uintptr(bufferaddress_2), int(dužina), int(dužina))
		copy(packet.data[:dužina], izvor)
	}
	receiver.tail = (receiver.tail + 1) % maksUtorsocketpaketi
	receiver.count++
	return int32(dužina)
}

func utorsocketreceivefrom(fd int32, bufferaddress_2 uint32, dužina uint32, izvoraddress uint32, izvorDužinaaddress uint32) int32 {
	utorsocket, greška := utorsocketforfd(fd)
	if greška != 0 {
		return greška
	}
	if dužina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if utorsocket.count == 0 {
		return Eagain
	}
	packet := &utorsocket.paketi[utorsocket.head]
	kopirajDužina := packet.veličina
	if kopirajDužina > dužina {
		kopirajDužina = dužina
	}
	if kopirajDužina != 0 {
		odredište := GetBajtovafromPokazivač(uintptr(bufferaddress_2), int(kopirajDužina), int(kopirajDužina))
		copy(odredište, packet.data[:kopirajDužina])
	}
	if izvoraddress != 0 {
		if izvorDužinaaddress == 0 {
			return Efault
		}
		providedDužina := (*uint32)(Pointer(uintptr(izvorDužinaaddress)))
		if *providedDužina >= 16 {
			*(*utorsocketaddressipv4)(Pointer(uintptr(izvoraddress))) = packet.izvor
		}
		*providedDužina = 16
	}
	*packet = utorsocketpacket{}
	utorsocket.head = (utorsocket.head + 1) % maksUtorsocketpaketi
	utorsocket.count--
	return int32(kopirajDužina)
}

func kopirajUtorsocketIme(fd int32, address_2 uint32, dužinaaddress uint32, peer bool) int32 {
	utorsocket, greška := utorsocketforfd(fd)
	if greška != 0 {
		return greška
	}
	if address_2 == 0 || dužinaaddress == 0 {
		return Efault
	}
	dužina := (*uint32)(Pointer(uintptr(dužinaaddress)))
	if *dužina < 16 {
		*dužina = 16
		return Einval
	}
	if peer {
		if !utorsocket.connected {
			return Enotconn
		}
		*(*utorsocketaddressipv4)(Pointer(uintptr(address_2))) = utorsocket.udaljeno
	} else {
		if !utorsocket.bound {
			if bindGreška := bindephemeral(utorsocket); bindGreška != 0 {
				return bindGreška
			}
		}
		*(*utorsocketaddressipv4)(Pointer(uintptr(address_2))) = utorsocket.local
	}
	*dužina = 16
	return 0
}

func sysUtorsocketcall(call uint32, argumenti_2 uint32) int32 {
	if argumenti_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateUtorsocket(utorsocketcallargument(argumenti_2, 0), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2))
	case 2:
		return utorsocketbind(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2))
	case 3:
		return utorsocketSpojise(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopirajUtorsocketIme(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2), false)
	case 7:
		return kopirajUtorsocketIme(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2), true)
	case 9:
		return utorsocketPošaljito(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2), 0, 0)
	case 10:
		return utorsocketreceivefrom(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2), 0, 0)
	case 11:
		return utorsocketPošaljito(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2), utorsocketcallargument(argumenti_2, 4), utorsocketcallargument(argumenti_2, 5))
	case 12:
		return utorsocketreceivefrom(int32(utorsocketcallargument(argumenti_2, 0)), utorsocketcallargument(argumenti_2, 1), utorsocketcallargument(argumenti_2, 2), utorsocketcallargument(argumenti_2, 4), utorsocketcallargument(argumenti_2, 5))
	case 13:
		if _, greška := utorsocketforfd(int32(utorsocketcallargument(argumenti_2, 0))); greška != 0 {
			return greška
		}
		return 0
	case 14:
		if _, greška := utorsocketforfd(int32(utorsocketcallargument(argumenti_2, 0))); greška != 0 {
			return greška
		}
		return 0
	}
	return Eopnotsupp
}

func čitajstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBajtovafromPokazivač(uintptr(address), int(count), int(count))
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
	slijedeće := (stdinZapiši + 1) % uint32(len(stdinbuffer))
	if slijedeće == stdinČitaj {
		return
	}
	stdinbuffer[stdinZapiši] = c
	stdinZapiši = slijedeće
}

func stdingetblocking() byte {
	for stdinČitaj == stdinZapiši {
		sc := pollTipkovnicascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinČitaj]
	stdinČitaj = (stdinČitaj + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTipkovnicascancode() byte {
	for (PortČitajbyte(0x64) & 0x01) == 0 {
	}
	sc := PortČitajbyte(0x60)
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

func kopirajIzvršivector(address_2 uint32, rEZULTAT *izvršivector) int32 {
	*rEZULTAT = izvršivector{}
	if address_2 == 0 {
		return 0
	}
	for kazalo := uint32(0); kazalo < maksIzvršivectorentry; kazalo++ {
		znakovninizaddress := *(*uint32)(Pointer(uintptr(address_2 + kazalo*4)))
		if znakovninizaddress == 0 {
			rEZULTAT.count = kazalo
			return 0
		}
		terminated := false
		for dužina := uint32(0); dužina <= maksIzvršiZnakovninizDužina; dužina++ {
			vrijednost := *(*byte)(Pointer(uintptr(znakovninizaddress + dužina)))
			rEZULTAT.vrijednosti[kazalo][dužina] = vrijednost
			if vrijednost == 0 {
				rEZULTAT.lengths[kazalo] = dužina
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

func pushIzvršiunsignedinteger32(stack *uint32, vrijednost uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = vrijednost
}

func setupIzvršistack(procesor *TcpuStanje, argumenti_2 *izvršivector, environment *izvršivector) int32 {
	const stackBajtova uint32 = 4096
	if !MakeOpsegPrivatnowritable(getcr3(), KorisnikstackVrh-stackBajtova, stackBajtova) {
		return Enomem
	}
	stack := KorisnikstackVrh
	var argumentpointers [maksIzvršivectorentry]uint32
	var environmentpointers [maksIzvršivectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		dužina := environment.lengths[i] + 1
		stack -= dužina
		odredište := GetBajtovafromPokazivač(uintptr(stack), int(dužina), int(dužina))
		copy(odredište, environment.vrijednosti[i][:dužina])
		environmentpointers[i] = stack
	}
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		dužina := argumenti_2.lengths[i] + 1
		stack -= dužina
		odredište := GetBajtovafromPokazivač(uintptr(stack), int(dužina), int(dužina))
		copy(odredište, argumenti_2.vrijednosti[i][:dužina])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushIzvršiunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushIzvršiunsignedinteger32(&stack, environmentpointers[i])
	}
	pushIzvršiunsignedinteger32(&stack, 0)
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		pushIzvršiunsignedinteger32(&stack, argumentpointers[i])
	}
	pushIzvršiunsignedinteger32(&stack, argumenti_2.count)
	procesor.Esp = stack
	procesor.Ebp = 0
	return 0
}

func zatvoriUključenoIzvrši(proces *procesentry) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if proces.fds[fd].iskorišteno && (proces.fds[fd].fdZastavice&fdcloexec) != 0 {
			zatvoriProcesfd(proces, fd)
		}
	}
}

func sysexecve(procesor *TcpuStanje, pUTANJAaddress uint32) int32 {
	if pUTANJAaddress == 0 {
		return Efault
	}
	var argumenti_2 izvršivector
	var environment izvršivector
	if rEZULTAT := kopirajIzvršivector(procesor.Ecx, &argumenti_2); rEZULTAT < 0 {
		return rEZULTAT
	}
	if rEZULTAT := kopirajIzvršivector(procesor.Edx, &environment); rEZULTAT < 0 {
		return rEZULTAT
	}
	imelen, ime := kopirajPUTANJA(pUTANJAaddress)
	if imelen == 0 {
		return Enoent
	}
	veličina := datotekaVeličina(ime[:imelen])
	if veličina == 0 {
		return Enoent
	}
	memorijamanager := &mem.TMemorijamanager{}
	datotekaPokazivač := memorijamanager.Malloc(veličina)
	if datotekaPokazivač == nil {
		return Einval
	}
	data := GetBajtovafromPokazivač(uintptr(datotekaPokazivač), int(veličina), int(veličina))
	čitajDatoteka(ime[:imelen], data)
	if veličina < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorijamanager.Slobodno(datotekaPokazivač)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	memorijamanager.Slobodno(datotekaPokazivač)
	if rEZULTAT := setupIzvršistack(procesor, &argumenti_2, &environment); rEZULTAT < 0 {
		return rEZULTAT
	}
	zatvoriUključenoIzvrši(ensureTrenutnoProces())
	procesor.Eip = entry
	procesor.Eax = 0
	return 0
}

func sysfork(procesor *TcpuStanje) int32 {
	roditeljpid := Trenutnopid()
	if ensureTrenutnoProces() == nil {
		return Enfile
	}
	pid := allocateProces(roditeljpid)
	if pid == 0 {
		return Einval
	}
	memorijamanager := &mem.TMemorijamanager{}
	threadPokazivač := memorijamanager.Malloc(uint32(Sizeof(TThread{})))
	stackPokazivač := memorijamanager.Malloc(ThreadstackVeličina)
	dijeteStranicaDirektorij := CloneaddressRazmaknicacow(getcr3())
	if threadPokazivač == nil || stackPokazivač == nil || dijeteStranicaDirektorij == 0 {
		discardProces(pid)
		return Einval
	}
	dijete := (*TThread)(threadPokazivač)
	dijete.Stack = uint32(uintptr(stackPokazivač))
	dijete.ProcesorStanje = (*TcpuStanje)(Pointer(uintptr(stackPokazivač) + ThreadstackVeličina - Sizeof(TcpuStanje{})))
	*dijete.ProcesorStanje = *procesor
	dijete.ProcesorStanje.Eax = 0
	dijete.Korisnikstack_2 = procesor.Esp
	dijete.KorisnikstackVeličina_2 = 0
	dijete.Pid = pid
	dijete.Roditeljpid = roditeljpid
	dijete.StranicaDirektorijentry = dijeteStranicaDirektorij
	dijete.ThreadStanje = Spreman
	dijete.Fpuoffset = 0xffffffff
	dijete.Iskernel = false
	Dodajrunnablethread(dijete)
	return int32(pid)
}

func sysIzađi(stanje uint32) {
	pid := Trenutnopid()
	for i := 0; i < len(procesTablica); i++ {
		if procesTablica[i].iskorišteno && procesTablica[i].pid == pid {
			zatvoriSveProcesfds(&procesTablica[i])
			procesTablica[i].exited = true
			procesTablica[i].stanje = (stanje & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, stanjeaddress uint32, opcije uint32) int32 {
	if (opcije & ^uint32(1)) != 0 {
		return Einval
	}
	roditeljpid := Trenutnopid()
	founddijete := false
	for i := 0; i < len(procesTablica); i++ {
		p := &procesTablica[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.iskorišteno && matches && p.roditelj == roditeljpid {
			founddijete = true
			if p.exited {
				if stanjeaddress != 0 {
					*(*uint32)(Pointer(uintptr(stanjeaddress))) = p.stanje
				}
				dijetepid := p.pid
				*p = procesentry{}
				return int32(dijetepid)
			}
		}
	}
	if !founddijete {
		return Echild
	}

	if (opcije & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(roditelj uint32) uint32 {
	roditeljProces := nađiProces(roditelj)
	pid := Allocatepid()
	for i := 0; i < len(procesTablica); i++ {
		if !procesTablica[i].iskorišteno {
			procesTablica[i] = procesentry{
				iskorišteno:	true,
				pid:		pid,
				roditelj:	roditelj,
				programbreak:	korisnikheapbase,
			}
			if roditeljProces != nil {
				procesTablica[i].programbreak = roditeljProces.programbreak
				for fd := 0; fd < maksfd; fd++ {
					if roditeljProces.fds[fd].iskorišteno {
						procesTablica[i].fds[fd] = roditeljProces.fds[fd]
						opis := roditeljProces.fds[fd].opis
						if opis >= 0 && opis < maksOtvoriDatoteke {
							otvoriDatotekaTablica[opis].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTablica[i])
			}
			return pid
		}
	}
	return 0
}

func zatvoriSveProcesfds(proces *procesentry) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if proces.fds[fd].iskorišteno {
			zatvoriProcesfd(proces, fd)
		}
	}
}

func discardProces(pid uint32) {
	proces := nađiProces(pid)
	if proces == nil {
		return
	}
	zatvoriSveProcesfds(proces)
	*proces = procesentry{}
}

func kopirajPUTANJA(pUTANJAaddress uint32) (uint32, [12]byte) {
	var ime [12]byte
	if pUTANJAaddress == 0 {
		return 0, ime
	}
	raw := GetBajtovafromPokazivač(uintptr(pUTANJAaddress), 64, 64)
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

func datotekaVeličina(imedatoteke []byte) uint32 {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablica{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterBlokiraj32{}
	veličina := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	ata0s.Flush()
	return veličina
}

func čitajDatoteka(imedatoteke []byte, data []byte) {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablica{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterBlokiraj32{}
	bios.Čitaj(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)
	ata0s.Flush()
}

func getcr3() uint32
