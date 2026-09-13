package rendszercall

import . "unsafe"

import . "megszakítás"
import . "konzol"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "fájlRendszer/msdospartition"
import . "fájlRendszer/fat"
import . "fájlRendszer/elf"
import mem "memóriamanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualMemória"

var konzol_2 = TKonzol{}

type TSyscall struct {
	TMegszakításhandler
}

const (
	SysKilépés	uint32	= 1
	Sysfork		uint32	= 2
	SysOlvasás	uint32	= 3
	SysÍrás		uint32	= 4
	SysMegnyitás	uint32	= 5
	SysBezárás	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syselérés	uint32	= 33
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
	SysrtKilépés	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2Nagy		int32	= -7
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
	maximumMegnyitásFÁJLOK		= 128
)

type fdbejegyzés struct {
	használt	bool
	leírás		int32
	fdFlagek	uint32
}

type megnyitásFájlLeírás struct {
	használt	bool
	refs		uint32
	fajta		uint32
	flagek		uint32
	pozíció		uint32
	méret		uint32
	név		[12]byte
	névlen		uint32
	aux		uint32
}

const (
	fdFajtaNincs			uint32	= 0
	fdFajtafat			uint32	= 1
	fdFajtastdin			uint32	= 2
	fdFajtaKonzol			uint32	= 3
	fdFajtaGyökérmappaKönyvtár	uint32	= 4
	fdFajtaFoglalat			uint32	= 5

	oOlvasásonly	uint32	= 0
	oÍrásonly	uint32	= 1
	oOlvasásÍrás	uint32	= 2
	ocreate		uint32	= 0x40
	oCsonkítás	uint32	= 0x200
	oappend		uint32	= 0x400
	oKönyvtár	uint32	= 0x10000

	seekhalmaz	uint32	= 0
	seekJelenlegi	uint32	= 1
	seekVégén	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fhalmazfd	uint32	= 2
	fgetfl		uint32	= 3
	fhalmazfl	uint32	= 4
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
	maximumsockets		= 32
	maximumFoglalatcsomag	= 8
	maximumdatagramMéret	= 512
)

type foglalataddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Nulla	[8]byte
}

type foglalatpacket struct {
	használt	bool
	méret		uint32
	forrás		foglalataddressipv4
	data		[maximumdatagramMéret]byte
}

type helyidatagramFoglalat struct {
	használt	bool
	bound		bool
	connected	bool
	helyi		foglalataddressipv4
	távoli		foglalataddressipv4
	head		uint32
	tail		uint32
	számláló	uint32
	csomag		[maximumFoglalatcsomag]foglalatpacket
}

type posixstat struct {
	Eszköz		uint32
	Ino		uint32
	Mód		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Méret_2		int32
	Blksize		int32
	Blokk		int32
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
	Verzió		[65]byte
	Machine		[65]byte
}

const (
	maximumFuttatásvectorbejegyzés		= 16
	maximumFuttatásKarakterláncHossz	= 63
)

type futtatásvector struct {
	számláló	uint32
	lengths		[maximumFuttatásvectorbejegyzés]uint32
	értékek		[maximumFuttatásvectorbejegyzés][maximumFuttatásKarakterláncHossz + 1]byte
}

type folyamatbejegyzés struct {
	használt	bool
	pid		uint32
	parent		uint32
	kilépett	bool
	állapot		uint32
	programbreak	uint32
	fds		[maximumfd]fdbejegyzés
}

type karakterláncheader struct {
	Data	uintptr
	Len	int
}

func syscallHiba(hiba int32) uint32 {
	return *(*uint32)(Pointer(&hiba))
}

var megnyitásFájlTáblázat [maximumMegnyitásFÁJLOK]megnyitásFájlLeírás
var folyamatTáblázat [32]folyamatbejegyzés
var helyisockets [maximumsockets]helyidatagramFoglalat
var következőephemeralport uint16 = 49152

const (
	felhasználóheapbase		uint32	= 0x06000000
	felhasználóheapKorlátozás	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinOlvasás uint32
var stdinÍrás uint32

func Megszakítás(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysKilépés_2(index uint32) {
	Syscall(SysKilépés, index)
}

func SysOlvasás_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysOlvasás, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysNyomtatásstr(buffer string) {
	h := (*karakterláncheader)(Pointer(&buffer))
	Syscall(SysÍrás, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysNyomtatásunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysÍrás, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysMegnyitás_2(úTVONAL uintptr, flagek uint32, mód uint32) int32 {
	return int32(Syscall(SysMegnyitás, uint32(úTVONAL), flagek, mód))
}

func SysBezárás_2(fd uint32) int32 {
	return int32(Syscall(SysBezárás, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(paraméterek ...uint32) uint32 {

	l := len(paraméterek)
	switch l {
	case 1:
		return Megszakítás(paraméterek[0], 0, 0, 0, 0, 0)
	case 2:
		return Megszakítás(paraméterek[0], paraméterek[1], 0, 0, 0, 0)
	case 3:
		return Megszakítás(paraméterek[0], paraméterek[1], paraméterek[2], 0, 0, 0)
	case 4:
		return Megszakítás(paraméterek[0], paraméterek[1], paraméterek[2], paraméterek[3], 0, 0)
	case 5:
		return Megszakítás(paraméterek[0], paraméterek[1], paraméterek[2], paraméterek[3], paraméterek[4], 0)
	case 6:
		return Megszakítás(paraméterek[0], paraméterek[1], paraméterek[2], paraméterek[3], paraméterek[4], paraméterek[5])
	default:
		return syscallHiba(Enosys)
	}
}

func (self *TSyscall) Init(manager *TMegszakításmanager) {
	initFájldescriptor()

	megszakításhandler = fogantyúMegszakítás

	var address uintptr
	address = uintptr(Pointer(&megszakításhandler))

	self.TMegszakításhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var megszakításhandler func(uint32) uint32

func fogantyúMegszakítás(esp uint32) uint32 {
	var cpu = (*TcpuÁllapot)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysKilépés:
		sysKilépés(cpu.Ebx)
		return uint32(uintptr(Pointer(LeállításJelenlegithread(cpu))))
	case SysrtKilépés:
		sysKilépés(cpu.Ebx)
		return uint32(uintptr(Pointer(LeállításJelenlegithread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysOlvasás:
		cpu.Eax = uint32(sysOlvasás(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysÍrás:
		cpu.Eax = uint32(sysÍrás(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysMegnyitás:
		cpu.Eax = uint32(sysMegnyitás(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysMegnyitás(cpu.Ebx, ocreate|oÍrásonly|oCsonkítás, cpu.Ecx))
		return esp
	case SysBezárás:
		cpu.Eax = uint32(sysBezárás(int32(cpu.Ebx)))
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
		cpu.Eax = Jelenlegipid()
		return esp
	case Sysgetppid:
		cpu.Eax = Jelenlegiparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Syselérés:
		cpu.Eax = uint32(syselérés(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysFoglalatcall(cpu.Ebx, cpu.Ecx))
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
		konzol_2.MUnsignedinteger32Nyomtatás(cpu.Ebx)
		return esp

	default:
		konzol_2.MNyomtatásxy(([]byte)("sys["), 1, 23)
		konzol_2.MUnsignedinteger32Nyomtatás(esp)
		konzol_2.MNyomtatás(([]byte)(":"))
		konzol_2.MUnsignedinteger32Nyomtatás(cpu.Eax)
		konzol_2.MNyomtatás(([]byte)(":"))
		konzol_2.MUnsignedinteger32Nyomtatás(cpu.Ebx)
		konzol_2.MNyomtatás(([]byte)(":"))
		konzol_2.MUnsignedinteger32Nyomtatás(cpu.Ecx)
		konzol_2.MNyomtatás(([]byte)(":"))
		konzol_2.MUnsignedinteger32Nyomtatás(cpu.Edx)
		konzol_2.MNyomtatás(([]byte)("]"))
		cpu.Eax = syscallHiba(Enosys)
		return esp
	}

	return esp
}

func initFájldescriptor() {
	for i := 0; i < maximumMegnyitásFÁJLOK; i++ {
		megnyitásFájlTáblázat[i] = megnyitásFájlLeírás{}
	}
	for i := 0; i < len(folyamatTáblázat); i++ {
		folyamatTáblázat[i] = folyamatbejegyzés{}
	}
	for i := 0; i < len(helyisockets); i++ {
		helyisockets[i] = helyidatagramFoglalat{}
	}
	következőephemeralport = 49152
	megnyitásFájlTáblázat[0] = megnyitásFájlLeírás{használt: true, fajta: fdFajtastdin, flagek: oOlvasásonly}
	megnyitásFájlTáblázat[1] = megnyitásFájlLeírás{használt: true, fajta: fdFajtaKonzol, flagek: oÍrásonly}
	megnyitásFájlTáblázat[2] = megnyitásFájlLeírás{használt: true, fajta: fdFajtaKonzol, flagek: oÍrásonly}
}

func keresésFolyamat(pid uint32) *folyamatbejegyzés {
	for i := 0; i < len(folyamatTáblázat); i++ {
		if folyamatTáblázat[i].használt && folyamatTáblázat[i].pid == pid {
			return &folyamatTáblázat[i]
		}
	}
	return nil
}

func initializeFolyamatfds(folyamat *folyamatbejegyzés) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		folyamat.fds[fd] = fdbejegyzés{használt: true, leírás: fd}
		megnyitásFájlTáblázat[fd].refs++
	}
}

func ensureJelenlegiFolyamat() *folyamatbejegyzés {
	pid := Jelenlegipid()
	if folyamat := keresésFolyamat(pid); folyamat != nil {
		return folyamat
	}
	for i := 0; i < len(folyamatTáblázat); i++ {
		if !folyamatTáblázat[i].használt {
			folyamatTáblázat[i] = folyamatbejegyzés{
				használt:	true,
				pid:		pid,
				parent:		Jelenlegiparentpid(),
				programbreak:	felhasználóheapbase,
			}
			initializeFolyamatfds(&folyamatTáblázat[i])
			return &folyamatTáblázat[i]
		}
	}
	return nil
}

func getMegnyitásFájlfor(folyamat *folyamatbejegyzés, fd int32) *megnyitásFájlLeírás {
	if folyamat == nil || fd < 0 || fd >= maximumfd || !folyamat.fds[fd].használt {
		return nil
	}
	leírás := folyamat.fds[fd].leírás
	if leírás < 0 || leírás >= maximumMegnyitásFÁJLOK || !megnyitásFájlTáblázat[leírás].használt {
		return nil
	}
	return &megnyitásFájlTáblázat[leírás]
}

func getMegnyitásFájl(fd int32) *megnyitásFájlLeírás {
	return getMegnyitásFájlfor(ensureJelenlegiFolyamat(), fd)
}

func allocateMegnyitásFájl() int32 {
	for i := int32(3); i < maximumMegnyitásFÁJLOK; i++ {
		if !megnyitásFájlTáblázat[i].használt {
			megnyitásFájlTáblázat[i] = megnyitásFájlLeírás{használt: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(folyamat *folyamatbejegyzés, leírás int32, minimum int32) int32 {
	if folyamat == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maximumfd {
		return Einval
	}
	for fd := minimum; fd < maximumfd; fd++ {
		if !folyamat.fds[fd].használt {
			folyamat.fds[fd] = fdbejegyzés{használt: true, leírás: leírás}
			return fd
		}
	}
	return Emfile
}

func releaseMegnyitásFájl(leírás int32) {
	if leírás < 0 || leírás >= maximumMegnyitásFÁJLOK {
		return
	}
	bejegyzés := &megnyitásFájlTáblázat[leírás]
	if bejegyzés.refs > 0 {
		bejegyzés.refs--
	}

	if bejegyzés.refs == 0 && leírás > stderrfd {
		if bejegyzés.fajta == fdFajtaFoglalat && bejegyzés.aux < maximumsockets {
			helyisockets[bejegyzés.aux] = helyidatagramFoglalat{}
		}
		*bejegyzés = megnyitásFájlLeírás{}
	}
}

func bezárásFolyamatfd(folyamat *folyamatbejegyzés, fd int32) int32 {
	if folyamat == nil || getMegnyitásFájlfor(folyamat, fd) == nil {
		return Ebadf
	}
	leírás := folyamat.fds[fd].leírás
	folyamat.fds[fd] = fdbejegyzés{}
	releaseMegnyitásFájl(leírás)
	return 0
}

func sysÍrás(fd int32, address uint32, számláló uint32) int32 {
	if számláló == 0 {
		return 0
	}
	if address == 0 || address+számláló < address {
		return Efault
	}
	if számláló > 4096 {
		return Einval
	}
	bejegyzés := getMegnyitásFájl(fd)
	if bejegyzés == nil {
		return Ebadf
	}
	if bejegyzés.fajta != fdFajtaKonzol {
		if bejegyzés.fajta == fdFajtaFoglalat {
			return foglalatKüldésto(fd, address, számláló, 0, 0)
		}
		if bejegyzés.fajta == fdFajtafat || bejegyzés.fajta == fdFajtaGyökérmappaKönyvtár {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBájtfromMutató(uintptr(address), int(számláló), int(számláló))
	konzol_2.MNyomtatás(buffer)
	return int32(számláló)
}

func sysOlvasás(fd int32, address uint32, számláló uint32) int32 {
	if számláló == 0 {
		return 0
	}
	if address == 0 || address+számláló < address {
		return Efault
	}
	bejegyzés := getMegnyitásFájl(fd)
	if bejegyzés == nil {
		return Ebadf
	}
	if bejegyzés.fajta == fdFajtastdin {
		return olvasásstdin(address, számláló)
	}
	if bejegyzés.fajta == fdFajtaGyökérmappaKönyvtár {
		return Eisdir
	}
	if bejegyzés.fajta == fdFajtaFoglalat {
		return foglalatreceivefrom(fd, address, számláló, 0, 0)
	}
	if bejegyzés.fajta != fdFajtafat {
		return Ebadf
	}
	if bejegyzés.pozíció >= bejegyzés.méret {
		return 0
	}
	remaining := bejegyzés.méret - bejegyzés.pozíció
	if számláló > remaining {
		számláló = remaining
	}
	buffer := GetBájtfromMutató(uintptr(address), int(számláló), int(számláló))
	return olvasásvfsFájl(bejegyzés, buffer, számláló)
}

func sysMegnyitás(úTVONALaddress uint32, flagek uint32, mód uint32) int32 {
	_ = mód
	if úTVONALaddress == 0 {
		return Efault
	}
	elérésmód := flagek & 3
	if elérésmód == oÍrásonly || elérésmód == oOlvasásÍrás || (flagek&(ocreate|oCsonkítás|oappend)) != 0 {
		return Erofs
	}

	folyamat := ensureJelenlegiFolyamat()
	if folyamat == nil {
		return Enfile
	}
	leírás := allocateMegnyitásFájl()
	if leírás < 0 {
		return leírás
	}
	bejegyzés := &megnyitásFájlTáblázat[leírás]
	bejegyzés.flagek = flagek
	if isGyökérmappaÚTVONAL(úTVONALaddress) {
		bejegyzés.fajta = fdFajtaGyökérmappaKönyvtár
		bejegyzés.méret = 0
	} else {
		névlen, név := másolásÚTVONAL(úTVONALaddress)
		if névlen == 0 {
			*bejegyzés = megnyitásFájlLeírás{}
			return Enoent
		}
		méret := fájlMéret(név[:névlen])
		if méret == 0 {
			*bejegyzés = megnyitásFájlLeírás{}
			return Enoent
		}
		if (flagek & oKönyvtár) != 0 {
			*bejegyzés = megnyitásFájlLeírás{}
			return Enotdir
		}
		bejegyzés.fajta = fdFajtafat
		bejegyzés.méret = méret
		bejegyzés.névlen = névlen
		bejegyzés.név = név
	}

	fd := allocatefd(folyamat, leírás, 3)
	if fd < 0 {
		*bejegyzés = megnyitásFájlLeírás{}
		return fd
	}
	return fd
}

func sysBezárás(fd int32) int32 {
	return bezárásFolyamatfd(ensureJelenlegiFolyamat(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	folyamat := ensureJelenlegiFolyamat()
	bejegyzés := getMegnyitásFájlfor(folyamat, fd)
	if bejegyzés == nil {
		return Ebadf
	}
	újfd := allocatefd(folyamat, folyamat.fds[fd].leírás, minimum)
	if újfd >= 0 {
		bejegyzés.refs++
	}
	return újfd
}

func sysdup2(öregfd int32, újfd int32) int32 {
	folyamat := ensureJelenlegiFolyamat()
	bejegyzés := getMegnyitásFájlfor(folyamat, öregfd)
	if bejegyzés == nil {
		return Ebadf
	}
	if újfd < 0 || újfd >= maximumfd {
		return Ebadf
	}
	if öregfd == újfd {
		return újfd
	}
	if folyamat.fds[újfd].használt {
		bezárásFolyamatfd(folyamat, újfd)
	}
	folyamat.fds[újfd] = fdbejegyzés{használt: true, leírás: folyamat.fds[öregfd].leírás}
	bejegyzés.refs++
	return újfd
}

func sysfcntl(fd int32, parancs uint32, argument uint32) int32 {
	folyamat := ensureJelenlegiFolyamat()
	bejegyzés := getMegnyitásFájlfor(folyamat, fd)
	if bejegyzés == nil {
		return Ebadf
	}
	switch parancs {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(folyamat.fds[fd].fdFlagek)
	case fhalmazfd:
		folyamat.fds[fd].fdFlagek = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(bejegyzés.flagek)
	case fhalmazfl:
		bejegyzés.flagek = (bejegyzés.flagek & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, eltolás int32, whence uint32) int32 {
	bejegyzés := getMegnyitásFájl(fd)
	if bejegyzés == nil {
		return Ebadf
	}
	if bejegyzés.fajta != fdFajtafat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekhalmaz:
		base = 0
	case seekJelenlegi:
		base = int64(bejegyzés.pozíció)
	case seekVégén:
		base = int64(bejegyzés.méret)
	default:
		return Einval
	}
	pozíció_2 := base + int64(eltolás)
	if pozíció_2 < 0 || pozíció_2 > 0x7FFFFFFF {
		return Einval
	}
	bejegyzés.pozíció = uint32(pozíció_2)
	return int32(bejegyzés.pozíció)
}

func olvasásvfsFájl(bejegyzés *megnyitásFájlLeírás, cél_2 []byte, számláló uint32) int32 {
	memóriamanager := &mem.TMemóriamanager{}
	tmpMutató := memóriamanager.Malloc(bejegyzés.méret)
	if tmpMutató == nil {
		return Einval
	}
	tmp := GetBájtfromMutató(uintptr(tmpMutató), int(bejegyzés.méret), int(bejegyzés.méret))
	olvasásFájl(bejegyzés.név[:bejegyzés.névlen], tmp)
	copy(cél_2[:számláló], tmp[bejegyzés.pozíció:bejegyzés.pozíció+számláló])
	bejegyzés.pozíció += számláló
	memóriamanager.Szabad(tmpMutató)
	return int32(számláló)
}

func isGyökérmappaÚTVONAL(úTVONALaddress uint32) bool {
	if úTVONALaddress == 0 {
		return false
	}
	úTVONAL := GetBájtfromMutató(uintptr(úTVONALaddress), 4, 4)
	if úTVONAL[0] == '/' && úTVONAL[1] == 0 {
		return true
	}
	if úTVONAL[0] == '.' && úTVONAL[1] == 0 {
		return true
	}
	if úTVONAL[0] == '/' && úTVONAL[1] == '.' && úTVONAL[2] == 0 {
		return true
	}
	return false
}

func syselérés(úTVONALaddress uint32, mód uint32) int32 {
	if úTVONALaddress == 0 {
		return Efault
	}
	if (mód & ^uint32(7)) != 0 {
		return Einval
	}
	isGyökérmappa := isGyökérmappaÚTVONAL(úTVONALaddress)
	exists := isGyökérmappa
	if !exists {
		névlen, név := másolásÚTVONAL(úTVONALaddress)
		exists = névlen != 0 && fájlMéret(név[:névlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mód & 2) != 0 {
		return Eacces
	}

	if (mód&1) != 0 && !isGyökérmappa {
		return Eacces
	}
	return 0
}

func syschdir(úTVONALaddress uint32) int32 {
	if úTVONALaddress == 0 {
		return Efault
	}
	if !isGyökérmappaÚTVONAL(úTVONALaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, méret uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if méret < 2 {
		return Erange
	}
	buffer_2 := GetBájtfromMutató(uintptr(bufferaddress), int(méret), int(méret))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mód uint32, méret uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Eszköz = 1
	stat.Ino = inode
	stat.Mód = mód
	stat.Nlink = 1
	stat.Méret_2 = int32(méret)
	stat.Blksize = 512
	stat.Blokk = int32((méret + 511) / 512)
	return 0
}

func sysstat(úTVONALaddress uint32, stataddress uint32) int32 {
	if úTVONALaddress == 0 {
		return Efault
	}
	if isGyökérmappaÚTVONAL(úTVONALaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	névlen, név := másolásÚTVONAL(úTVONALaddress)
	if névlen == 0 {
		return Enoent
	}
	méret := fájlMéret(név[:névlen])
	if méret == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < névlen; i++ {
		inode = inode*33 + uint32(név[i])
	}
	return fillposixstat(stataddress, sifreg|0444, méret, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	bejegyzés := getMegnyitásFájl(fd)
	if bejegyzés == nil {
		return Ebadf
	}
	switch bejegyzés.fajta {
	case fdFajtastdin, fdFajtaKonzol:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdFajtaGyökérmappaKönyvtár:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdFajtafat:
		return fillposixstat(stataddress, sifreg|0444, bejegyzés.méret, uint32(fd+2))
	case fdFajtaFoglalat:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getMegnyitásFájl(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	folyamat := ensureJelenlegiFolyamat()
	if folyamat == nil {
		return 0
	}
	if folyamat.programbreak == 0 {
		folyamat.programbreak = felhasználóheapbase
	}
	if address_2 == 0 {
		return folyamat.programbreak
	}
	if address_2 < felhasználóheapbase || address_2 > felhasználóheapKorlátozás {
		return folyamat.programbreak
	}
	folyamat.programbreak = address_2
	return folyamat.programbreak
}

func másolásutsmező(cél *[65]byte, érték string) {
	korlátozás := len(érték)
	if korlátozás > 64 {
		korlátozás = 64
	}
	for i := 0; i < korlátozás; i++ {
		cél[i] = érték[i]
	}
	cél[korlátozás] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	név := (*posixutsname)(Pointer(uintptr(address_2)))
	*név = posixutsname{}
	másolásutsmező(&név.Sysname, "EngOS")
	másolásutsmező(&név.Nodename, "engos")
	másolásutsmező(&név.Release, "0.1-posix")
	másolásutsmező(&név.Verzió, "POSIX.1-2017 phase 1")
	másolásutsmező(&név.Machine, "i386")
	return 0
}

func cserehelyunsignedinteger16(érték uint16) uint16 {
	return (érték << 8) | (érték >> 8)
}

func foglalatcallargument(argumentumok_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumentumok_2 + index*4)))
}

func foglalatforfd(fd int32) (*helyidatagramFoglalat, int32) {
	bejegyzés := getMegnyitásFájl(fd)
	if bejegyzés == nil || bejegyzés.fajta != fdFajtaFoglalat || bejegyzés.aux >= maximumsockets {
		return nil, Ebadf
	}
	foglalat := &helyisockets[bejegyzés.aux]
	if !foglalat.használt {
		return nil, Ebadf
	}
	return foglalat, 0
}

func allocateFoglalat(tartomány uint32, foglalatTípus uint32, protocol uint32) int32 {
	if tartomány != afinet {
		return Eafnosupport
	}
	if foglalatTípus != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	folyamat := ensureJelenlegiFolyamat()
	if folyamat == nil {
		return Enfile
	}
	foglalatindex := -1
	for i := 0; i < maximumsockets; i++ {
		if !helyisockets[i].használt {
			foglalatindex = i
			break
		}
	}
	if foglalatindex < 0 {
		return Enfile
	}
	leírás := allocateMegnyitásFájl()
	if leírás < 0 {
		return leírás
	}
	helyisockets[foglalatindex] = helyidatagramFoglalat{használt: true}
	bejegyzés := &megnyitásFájlTáblázat[leírás]
	bejegyzés.fajta = fdFajtaFoglalat
	bejegyzés.flagek = oOlvasásÍrás
	bejegyzés.aux = uint32(foglalatindex)
	fd := allocatefd(folyamat, leírás, 3)
	if fd < 0 {
		helyisockets[foglalatindex] = helyidatagramFoglalat{}
		*bejegyzés = megnyitásFájlLeírás{}
		return fd
	}
	return fd
}

func foglalataddress(address_2 uint32, hossz uint32) (*foglalataddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if hossz < 16 {
		return nil, Einval
	}
	result := (*foglalataddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portBeHasználat(port uint16, except *helyidatagramFoglalat) bool {
	for i := 0; i < maximumsockets; i++ {
		foglalat := &helyisockets[i]
		if foglalat != except && foglalat.használt && foglalat.bound && foglalat.helyi.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(foglalat *helyidatagramFoglalat) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := cserehelyunsignedinteger16(következőephemeralport)
		következőephemeralport++
		if következőephemeralport < 49152 {
			következőephemeralport = 49152
		}
		if !portBeHasználat(port, foglalat) {
			foglalat.helyi = foglalataddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			foglalat.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func foglalatbind(fd int32, address_2 uint32, hossz uint32) int32 {
	foglalat, hiba := foglalatforfd(fd)
	if hiba != 0 {
		return hiba
	}
	requested, hiba := foglalataddress(address_2, hossz)
	if hiba != 0 {
		return hiba
	}
	if foglalat.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(foglalat)
	}
	if portBeHasználat(requested.Port, foglalat) {
		return Eaddrinuse
	}
	foglalat.helyi = *requested
	foglalat.bound = true
	return 0
}

func foglalatKapcsolódás(fd int32, address_2 uint32, hossz uint32) int32 {
	foglalat, hiba := foglalatforfd(fd)
	if hiba != 0 {
		return hiba
	}
	távoli, hiba := foglalataddress(address_2, hossz)
	if hiba != 0 {
		return hiba
	}
	if !foglalat.bound {
		if hiba := bindephemeral(foglalat); hiba != 0 {
			return hiba
		}
	}
	foglalat.távoli = *távoli
	foglalat.connected = true
	return 0
}

func foglalatKüldésto(fd int32, bufferaddress_2 uint32, hossz uint32, céladdress uint32, célHossz uint32) int32 {
	foglalat, hiba := foglalatforfd(fd)
	if hiba != 0 {
		return hiba
	}
	if hossz > maximumdatagramMéret {
		return Emsgsize
	}
	if hossz != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var cél foglalataddressipv4
	if céladdress != 0 {
		address_2, addressHiba := foglalataddress(céladdress, célHossz)
		if addressHiba != 0 {
			return addressHiba
		}
		cél = *address_2
	} else {
		if !foglalat.connected {
			return Enotconn
		}
		cél = foglalat.távoli
	}
	if !foglalat.bound {
		if bindHiba := bindephemeral(foglalat); bindHiba != 0 {
			return bindHiba
		}
	}
	var receiver *helyidatagramFoglalat
	for i := 0; i < maximumsockets; i++ {
		candidate := &helyisockets[i]
		if candidate.használt && candidate.bound && candidate.helyi.Port == cél.Port &&
			(candidate.helyi.Address == 0 || candidate.helyi.Address == cél.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.számláló >= maximumFoglalatcsomag {
		return Eagain
	}
	packet := &receiver.csomag[receiver.tail]
	*packet = foglalatpacket{használt: true, méret: hossz, forrás: foglalat.helyi}
	if hossz != 0 {
		forrás := GetBájtfromMutató(uintptr(bufferaddress_2), int(hossz), int(hossz))
		copy(packet.data[:hossz], forrás)
	}
	receiver.tail = (receiver.tail + 1) % maximumFoglalatcsomag
	receiver.számláló++
	return int32(hossz)
}

func foglalatreceivefrom(fd int32, bufferaddress_2 uint32, hossz uint32, forrásaddress uint32, forrásHosszaddress uint32) int32 {
	foglalat, hiba := foglalatforfd(fd)
	if hiba != 0 {
		return hiba
	}
	if hossz != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if foglalat.számláló == 0 {
		return Eagain
	}
	packet := &foglalat.csomag[foglalat.head]
	másolásHossz := packet.méret
	if másolásHossz > hossz {
		másolásHossz = hossz
	}
	if másolásHossz != 0 {
		cél := GetBájtfromMutató(uintptr(bufferaddress_2), int(másolásHossz), int(másolásHossz))
		copy(cél, packet.data[:másolásHossz])
	}
	if forrásaddress != 0 {
		if forrásHosszaddress == 0 {
			return Efault
		}
		providedHossz := (*uint32)(Pointer(uintptr(forrásHosszaddress)))
		if *providedHossz >= 16 {
			*(*foglalataddressipv4)(Pointer(uintptr(forrásaddress))) = packet.forrás
		}
		*providedHossz = 16
	}
	*packet = foglalatpacket{}
	foglalat.head = (foglalat.head + 1) % maximumFoglalatcsomag
	foglalat.számláló--
	return int32(másolásHossz)
}

func másolásFoglalatNév(fd int32, address_2 uint32, hosszaddress uint32, peer bool) int32 {
	foglalat, hiba := foglalatforfd(fd)
	if hiba != 0 {
		return hiba
	}
	if address_2 == 0 || hosszaddress == 0 {
		return Efault
	}
	hossz := (*uint32)(Pointer(uintptr(hosszaddress)))
	if *hossz < 16 {
		*hossz = 16
		return Einval
	}
	if peer {
		if !foglalat.connected {
			return Enotconn
		}
		*(*foglalataddressipv4)(Pointer(uintptr(address_2))) = foglalat.távoli
	} else {
		if !foglalat.bound {
			if bindHiba := bindephemeral(foglalat); bindHiba != 0 {
				return bindHiba
			}
		}
		*(*foglalataddressipv4)(Pointer(uintptr(address_2))) = foglalat.helyi
	}
	*hossz = 16
	return 0
}

func sysFoglalatcall(call uint32, argumentumok_2 uint32) int32 {
	if argumentumok_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateFoglalat(foglalatcallargument(argumentumok_2, 0), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2))
	case 2:
		return foglalatbind(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2))
	case 3:
		return foglalatKapcsolódás(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return másolásFoglalatNév(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2), false)
	case 7:
		return másolásFoglalatNév(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2), true)
	case 9:
		return foglalatKüldésto(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2), 0, 0)
	case 10:
		return foglalatreceivefrom(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2), 0, 0)
	case 11:
		return foglalatKüldésto(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2), foglalatcallargument(argumentumok_2, 4), foglalatcallargument(argumentumok_2, 5))
	case 12:
		return foglalatreceivefrom(int32(foglalatcallargument(argumentumok_2, 0)), foglalatcallargument(argumentumok_2, 1), foglalatcallargument(argumentumok_2, 2), foglalatcallargument(argumentumok_2, 4), foglalatcallargument(argumentumok_2, 5))
	case 13:
		if _, hiba := foglalatforfd(int32(foglalatcallargument(argumentumok_2, 0))); hiba != 0 {
			return hiba
		}
		return 0
	case 14:
		if _, hiba := foglalatforfd(int32(foglalatcallargument(argumentumok_2, 0))); hiba != 0 {
			return hiba
		}
		return 0
	}
	return Eopnotsupp
}

func olvasásstdin(address uint32, számláló uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBájtfromMutató(uintptr(address), int(számláló), int(számláló))
	var n uint32
	for n < számláló {
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
	következő := (stdinÍrás + 1) % uint32(len(stdinbuffer))
	if következő == stdinOlvasás {
		return
	}
	stdinbuffer[stdinÍrás] = c
	stdinÍrás = következő
}

func stdingetblocking() byte {
	for stdinOlvasás == stdinÍrás {
		sc := pollBillentyűzetscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinOlvasás]
	stdinOlvasás = (stdinOlvasás + 1) % uint32(len(stdinbuffer))
	return c
}

func pollBillentyűzetscancode() byte {
	for (PortOlvasásbyte(0x64) & 0x01) == 0 {
	}
	sc := PortOlvasásbyte(0x60)
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

func másolásFuttatásvector(address_2 uint32, result *futtatásvector) int32 {
	*result = futtatásvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maximumFuttatásvectorbejegyzés; index++ {
		karakterláncaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if karakterláncaddress == 0 {
			result.számláló = index
			return 0
		}
		terminated := false
		for hossz := uint32(0); hossz <= maximumFuttatásKarakterláncHossz; hossz++ {
			érték := *(*byte)(Pointer(uintptr(karakterláncaddress + hossz)))
			result.értékek[index][hossz] = érték
			if érték == 0 {
				result.lengths[index] = hossz
				terminated = true
				break
			}
		}
		if !terminated {
			return E2Nagy
		}
	}
	return E2Nagy
}

func pushFuttatásunsignedinteger32(stack *uint32, érték uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = érték
}

func setupFuttatásstack(cpu *TcpuÁllapot, argumentumok_2 *futtatásvector, environment *futtatásvector) int32 {
	const stackBájt uint32 = 4096
	if !MakeTartománySzemélyeswritable(getcr3(), FelhasználóstackFent-stackBájt, stackBájt) {
		return Enomem
	}
	stack := FelhasználóstackFent
	var argumentpointers [maximumFuttatásvectorbejegyzés]uint32
	var environmentpointers [maximumFuttatásvectorbejegyzés]uint32

	for i := int(environment.számláló) - 1; i >= 0; i-- {
		hossz := environment.lengths[i] + 1
		stack -= hossz
		cél := GetBájtfromMutató(uintptr(stack), int(hossz), int(hossz))
		copy(cél, environment.értékek[i][:hossz])
		environmentpointers[i] = stack
	}
	for i := int(argumentumok_2.számláló) - 1; i >= 0; i-- {
		hossz := argumentumok_2.lengths[i] + 1
		stack -= hossz
		cél := GetBájtfromMutató(uintptr(stack), int(hossz), int(hossz))
		copy(cél, argumentumok_2.értékek[i][:hossz])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushFuttatásunsignedinteger32(&stack, 0)
	for i := int(environment.számláló) - 1; i >= 0; i-- {
		pushFuttatásunsignedinteger32(&stack, environmentpointers[i])
	}
	pushFuttatásunsignedinteger32(&stack, 0)
	for i := int(argumentumok_2.számláló) - 1; i >= 0; i-- {
		pushFuttatásunsignedinteger32(&stack, argumentpointers[i])
	}
	pushFuttatásunsignedinteger32(&stack, argumentumok_2.számláló)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func bezárásBeFuttatás(folyamat *folyamatbejegyzés) {
	if folyamat == nil {
		return
	}
	for fd := int32(0); fd < maximumfd; fd++ {
		if folyamat.fds[fd].használt && (folyamat.fds[fd].fdFlagek&fdcloexec) != 0 {
			bezárásFolyamatfd(folyamat, fd)
		}
	}
}

func sysexecve(cpu *TcpuÁllapot, úTVONALaddress uint32) int32 {
	if úTVONALaddress == 0 {
		return Efault
	}
	var argumentumok_2 futtatásvector
	var environment futtatásvector
	if result := másolásFuttatásvector(cpu.Ecx, &argumentumok_2); result < 0 {
		return result
	}
	if result := másolásFuttatásvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	névlen, név := másolásÚTVONAL(úTVONALaddress)
	if névlen == 0 {
		return Enoent
	}
	méret := fájlMéret(név[:névlen])
	if méret == 0 {
		return Enoent
	}
	memóriamanager := &mem.TMemóriamanager{}
	fájlMutató := memóriamanager.Malloc(méret)
	if fájlMutató == nil {
		return Einval
	}
	data := GetBájtfromMutató(uintptr(fájlMutató), int(méret), int(méret))
	olvasásFájl(név[:névlen], data)
	if méret < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memóriamanager.Szabad(fájlMutató)
		return Enoexec
	}
	loader := Elf{}
	bejegyzés := loader.Getbejegyzés(data)
	loader.Parse(data, getcr3())
	memóriamanager.Szabad(fájlMutató)
	if result := setupFuttatásstack(cpu, &argumentumok_2, &environment); result < 0 {
		return result
	}
	bezárásBeFuttatás(ensureJelenlegiFolyamat())
	cpu.Eip = bejegyzés
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuÁllapot) int32 {
	parentpid := Jelenlegipid()
	if ensureJelenlegiFolyamat() == nil {
		return Enfile
	}
	pid := allocateFolyamat(parentpid)
	if pid == 0 {
		return Einval
	}
	memóriamanager := &mem.TMemóriamanager{}
	threadMutató := memóriamanager.Malloc(uint32(Sizeof(TThread{})))
	stackMutató := memóriamanager.Malloc(ThreadstackMéret)
	childOldalKönyvtár := CloneaddressSzóközcow(getcr3())
	if threadMutató == nil || stackMutató == nil || childOldalKönyvtár == 0 {
		eldobásFolyamat(pid)
		return Einval
	}
	child := (*TThread)(threadMutató)
	child.Stack = uint32(uintptr(stackMutató))
	child.CpuÁllapot = (*TcpuÁllapot)(Pointer(uintptr(stackMutató) + ThreadstackMéret - Sizeof(TcpuÁllapot{})))
	*child.CpuÁllapot = *cpu
	child.CpuÁllapot.Eax = 0
	child.Felhasználóstack_2 = cpu.Esp
	child.FelhasználóstackMéret_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.OldalKönyvtárbejegyzés = childOldalKönyvtár
	child.ThreadÁllapot = Kész
	child.FpuEltolás = 0xffffffff
	child.Iskernel = false
	Hozzáadásrunnablethread(child)
	return int32(pid)
}

func sysKilépés(állapot uint32) {
	pid := Jelenlegipid()
	for i := 0; i < len(folyamatTáblázat); i++ {
		if folyamatTáblázat[i].használt && folyamatTáblázat[i].pid == pid {
			bezárásÖsszesFolyamatfds(&folyamatTáblázat[i])
			folyamatTáblázat[i].kilépett = true
			folyamatTáblázat[i].állapot = (állapot & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, állapotaddress uint32, beállítások uint32) int32 {
	if (beállítások & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Jelenlegipid()
	foundchild := false
	for i := 0; i < len(folyamatTáblázat); i++ {
		p := &folyamatTáblázat[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.használt && matches && p.parent == parentpid {
			foundchild = true
			if p.kilépett {
				if állapotaddress != 0 {
					*(*uint32)(Pointer(uintptr(állapotaddress))) = p.állapot
				}
				childpid := p.pid
				*p = folyamatbejegyzés{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (beállítások & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateFolyamat(parent uint32) uint32 {
	parentFolyamat := keresésFolyamat(parent)
	pid := Allocatepid()
	for i := 0; i < len(folyamatTáblázat); i++ {
		if !folyamatTáblázat[i].használt {
			folyamatTáblázat[i] = folyamatbejegyzés{
				használt:	true,
				pid:		pid,
				parent:		parent,
				programbreak:	felhasználóheapbase,
			}
			if parentFolyamat != nil {
				folyamatTáblázat[i].programbreak = parentFolyamat.programbreak
				for fd := 0; fd < maximumfd; fd++ {
					if parentFolyamat.fds[fd].használt {
						folyamatTáblázat[i].fds[fd] = parentFolyamat.fds[fd]
						leírás := parentFolyamat.fds[fd].leírás
						if leírás >= 0 && leírás < maximumMegnyitásFÁJLOK {
							megnyitásFájlTáblázat[leírás].refs++
						}
					}
				}
			} else {
				initializeFolyamatfds(&folyamatTáblázat[i])
			}
			return pid
		}
	}
	return 0
}

func bezárásÖsszesFolyamatfds(folyamat *folyamatbejegyzés) {
	if folyamat == nil {
		return
	}
	for fd := int32(0); fd < maximumfd; fd++ {
		if folyamat.fds[fd].használt {
			bezárásFolyamatfd(folyamat, fd)
		}
	}
}

func eldobásFolyamat(pid uint32) {
	folyamat := keresésFolyamat(pid)
	if folyamat == nil {
		return
	}
	bezárásÖsszesFolyamatfds(folyamat)
	*folyamat = folyamatbejegyzés{}
}

func másolásÚTVONAL(úTVONALaddress uint32) (uint32, [12]byte) {
	var név [12]byte
	if úTVONALaddress == 0 {
		return 0, név
	}
	raw := GetBájtfromMutató(uintptr(úTVONALaddress), 64, 64)
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
		név[n] = c
		n++
	}
	return n, név
}

func fájlMéret(fájlnév []byte) uint32 {
	var ata0s = THaladóTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTáblázat{}
	partition.Olvasáspartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	méret := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], fájlnév)
	ata0s.Flush()
	return méret
}

func olvasásFájl(fájlnév []byte, data []byte) {
	var ata0s = THaladóTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTáblázat{}
	partition.Olvasáspartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	bios.Olvasás(&ata0s, partition.Mbr.Primarypartition[0], fájlnév, data)
	ata0s.Flush()
}

func getcr3() uint32
