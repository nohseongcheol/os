package sistēmacall

import . "unsafe"

import . "pārtraukums"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "failsSistēma/msdospartition"
import . "failsSistēma/fat"
import . "failsSistēma/elf"
import mem "atmiņamanager"
import . "paging"
import . "ports"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuālaAtmiņa"

var console_2 = TConsole{}

type TSyscall struct {
	TPārtraukumshandler
}

const (
	SysIziet	uint32	= 1
	Sysfork		uint32	= 2
	SysLasīt	uint32	= 3
	SysRakstīt	uint32	= 4
	SysAtvērt	uint32	= 5
	SysAizvērt	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syspiekļūt	uint32	= 33
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
	SysrtIziet	uint32	= 252

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
	maksfd			= 32
	maksAtvērtFAILI		= 128
)

type fdieraksts struct {
	izmantots	bool
	apraksts	int32
	fdKarogi	uint32
}

type atvērtFailsApraksts struct {
	izmantots	bool
	refs		uint32
	kind		uint32
	karogi		uint32
	novietojums	uint32
	izmērs		uint32
	nosaukums	[12]byte
	nosaukumslen	uint32
	aux		uint32
}

const (
	fdkindNav	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindconsole	uint32	= 3
	fdkindSakneMape	uint32	= 4
	fdkindLigzda	uint32	= 5

	oLasītonly	uint32	= 0
	oRakstītonly	uint32	= 1
	oLasītRakstīt	uint32	= 2
	ocreate		uint32	= 0x40
	oApraut		uint32	= 0x200
	oappend		uint32	= 0x400
	oMape		uint32	= 0x10000

	seekkopa		uint32	= 0
	seekPašreizējais	uint32	= 1
	seekBeigas		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fkopafd		uint32	= 2
	fgetfl		uint32	= 3
	fkopafl		uint32	= 4
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
	maksLigzdapackets	= 8
	maksdatagramIzmērs	= 512
)

type ligzdaaddressipv4 struct {
	Family	uint16
	Ports	uint16
	Address	uint32
	Zero	[8]byte
}

type ligzdapacket struct {
	izmantots	bool
	izmērs		uint32
	avots		ligzdaaddressipv4
	data		[maksdatagramIzmērs]byte
}

type vietējaisdatagramLigzda struct {
	izmantots	bool
	bound		bool
	connected	bool
	vietējais	ligzdaaddressipv4
	remote		ligzdaaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maksLigzdapackets]ligzdapacket
}

type posixstat struct {
	Ierīce		uint32
	Ino		uint32
	Režīms		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Izmērs_2	int32
	Blksize		int32
	Bloks		int32
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
	Versija		[65]byte
	Machine		[65]byte
}

const (
	maksIzpildītvectorieraksts	= 16
	maksIzpildītvirkneGarums	= 63
)

type izpildītvector struct {
	count	uint32
	lengths	[maksIzpildītvectorieraksts]uint32
	values	[maksIzpildītvectorieraksts][maksIzpildītvirkneGarums + 1]byte
}

type processieraksts struct {
	izmantots	bool
	pid		uint32
	vecāks		uint32
	exited		bool
	statuss		uint32
	programmabreak	uint32
	fds		[maksfd]fdieraksts
}

type virkneheader struct {
	Data	uintptr
	Len	int
}

func syscallKļūda(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var atvērtFailsTabula [maksAtvērtFAILI]atvērtFailsApraksts
var processTabula [32]processieraksts
var vietējaissockets [makssockets]vietējaisdatagramLigzda
var nākamaisephemeralPorts uint16 = 49152

const (
	lietotājsheapbase	uint32	= 0x06000000
	lietotājsheapIerobežot	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLasīt uint32
var stdinRakstīt uint32

func Pārtraukums(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIziet_2(saturs uint32) {
	Syscall(SysIziet, saturs)
}

func SysLasīt_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLasīt, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysDrukātstr(buffer string) {
	h := (*virkneheader)(Pointer(&buffer))
	Syscall(SysRakstīt, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysDrukātunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysRakstīt, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysAtvērt_2(cEĻŠ uintptr, karogi uint32, režīms uint32) int32 {
	return int32(Syscall(SysAtvērt, uint32(cEĻŠ), karogi, režīms))
}

func SysAizvērt_2(fd uint32) int32 {
	return int32(Syscall(SysAizvērt, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametri_3 ...uint32) uint32 {

	l := len(parametri_3)
	switch l {
	case 1:
		return Pārtraukums(parametri_3[0], 0, 0, 0, 0, 0)
	case 2:
		return Pārtraukums(parametri_3[0], parametri_3[1], 0, 0, 0, 0)
	case 3:
		return Pārtraukums(parametri_3[0], parametri_3[1], parametri_3[2], 0, 0, 0)
	case 4:
		return Pārtraukums(parametri_3[0], parametri_3[1], parametri_3[2], parametri_3[3], 0, 0)
	case 5:
		return Pārtraukums(parametri_3[0], parametri_3[1], parametri_3[2], parametri_3[3], parametri_3[4], 0)
	case 6:
		return Pārtraukums(parametri_3[0], parametri_3[1], parametri_3[2], parametri_3[3], parametri_3[4], parametri_3[5])
	default:
		return syscallKļūda(Enosys)
	}
}

func (pats *TSyscall) Init(manager *TPārtraukumsmanager) {
	initFailsdescriptor()

	pārtraukumshandler = handlePārtraukums

	var address uintptr
	address = uintptr(Pointer(&pārtraukumshandler))

	pats.TPārtraukumshandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var pārtraukumshandler func(uint32) uint32

func handlePārtraukums(esp uint32) uint32 {
	var cpu = (*TcpuStāvoklis)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysIziet:
		sysIziet(cpu.Ebx)
		return uint32(uintptr(Pointer(ApturētPašreizējaisthread(cpu))))
	case SysrtIziet:
		sysIziet(cpu.Ebx)
		return uint32(uintptr(Pointer(ApturētPašreizējaisthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLasīt:
		cpu.Eax = uint32(sysLasīt(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysRakstīt:
		cpu.Eax = uint32(sysRakstīt(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysAtvērt:
		cpu.Eax = uint32(sysAtvērt(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysAtvērt(cpu.Ebx, ocreate|oRakstītonly|oApraut, cpu.Ecx))
		return esp
	case SysAizvērt:
		cpu.Eax = uint32(sysAizvērt(int32(cpu.Ebx)))
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
		cpu.Eax = Pašreizējaispid()
		return esp
	case Sysgetppid:
		cpu.Eax = Pašreizējaisvecākspid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Syspiekļūt:
		cpu.Eax = uint32(syspiekļūt(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysLigzdacall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Drukāt(cpu.Ebx)
		return esp

	default:
		console_2.MDrukātxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Drukāt(esp)
		console_2.MDrukāt(([]byte)(":"))
		console_2.MUnsignedinteger32Drukāt(cpu.Eax)
		console_2.MDrukāt(([]byte)(":"))
		console_2.MUnsignedinteger32Drukāt(cpu.Ebx)
		console_2.MDrukāt(([]byte)(":"))
		console_2.MUnsignedinteger32Drukāt(cpu.Ecx)
		console_2.MDrukāt(([]byte)(":"))
		console_2.MUnsignedinteger32Drukāt(cpu.Edx)
		console_2.MDrukāt(([]byte)("]"))
		cpu.Eax = syscallKļūda(Enosys)
		return esp
	}

	return esp
}

func initFailsdescriptor() {
	for i := 0; i < maksAtvērtFAILI; i++ {
		atvērtFailsTabula[i] = atvērtFailsApraksts{}
	}
	for i := 0; i < len(processTabula); i++ {
		processTabula[i] = processieraksts{}
	}
	for i := 0; i < len(vietējaissockets); i++ {
		vietējaissockets[i] = vietējaisdatagramLigzda{}
	}
	nākamaisephemeralPorts = 49152
	atvērtFailsTabula[0] = atvērtFailsApraksts{izmantots: true, kind: fdkindstdin, karogi: oLasītonly}
	atvērtFailsTabula[1] = atvērtFailsApraksts{izmantots: true, kind: fdkindconsole, karogi: oRakstītonly}
	atvērtFailsTabula[2] = atvērtFailsApraksts{izmantots: true, kind: fdkindconsole, karogi: oRakstītonly}
}

func meklētprocess(pid uint32) *processieraksts {
	for i := 0; i < len(processTabula); i++ {
		if processTabula[i].izmantots && processTabula[i].pid == pid {
			return &processTabula[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processieraksts) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdieraksts{izmantots: true, apraksts: fd}
		atvērtFailsTabula[fd].refs++
	}
}

func ensurePašreizējaisprocess() *processieraksts {
	pid := Pašreizējaispid()
	if process := meklētprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processTabula); i++ {
		if !processTabula[i].izmantots {
			processTabula[i] = processieraksts{
				izmantots:	true,
				pid:		pid,
				vecāks:		Pašreizējaisvecākspid(),
				programmabreak:	lietotājsheapbase,
			}
			initializeprocessfds(&processTabula[i])
			return &processTabula[i]
		}
	}
	return nil
}

func getAtvērtFailsfor(process *processieraksts, fd int32) *atvērtFailsApraksts {
	if process == nil || fd < 0 || fd >= maksfd || !process.fds[fd].izmantots {
		return nil
	}
	apraksts := process.fds[fd].apraksts
	if apraksts < 0 || apraksts >= maksAtvērtFAILI || !atvērtFailsTabula[apraksts].izmantots {
		return nil
	}
	return &atvērtFailsTabula[apraksts]
}

func getAtvērtFails(fd int32) *atvērtFailsApraksts {
	return getAtvērtFailsfor(ensurePašreizējaisprocess(), fd)
}

func allocateAtvērtFails() int32 {
	for i := int32(3); i < maksAtvērtFAILI; i++ {
		if !atvērtFailsTabula[i].izmantots {
			atvērtFailsTabula[i] = atvērtFailsApraksts{izmantots: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processieraksts, apraksts int32, minimums int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimums < 0 || minimums >= maksfd {
		return Einval
	}
	for fd := minimums; fd < maksfd; fd++ {
		if !process.fds[fd].izmantots {
			process.fds[fd] = fdieraksts{izmantots: true, apraksts: apraksts}
			return fd
		}
	}
	return Emfile
}

func releaseAtvērtFails(apraksts int32) {
	if apraksts < 0 || apraksts >= maksAtvērtFAILI {
		return
	}
	ieraksts := &atvērtFailsTabula[apraksts]
	if ieraksts.refs > 0 {
		ieraksts.refs--
	}

	if ieraksts.refs == 0 && apraksts > stderrfd {
		if ieraksts.kind == fdkindLigzda && ieraksts.aux < makssockets {
			vietējaissockets[ieraksts.aux] = vietējaisdatagramLigzda{}
		}
		*ieraksts = atvērtFailsApraksts{}
	}
}

func aizvērtprocessfd(process *processieraksts, fd int32) int32 {
	if process == nil || getAtvērtFailsfor(process, fd) == nil {
		return Ebadf
	}
	apraksts := process.fds[fd].apraksts
	process.fds[fd] = fdieraksts{}
	releaseAtvērtFails(apraksts)
	return 0
}

func sysRakstīt(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	ieraksts := getAtvērtFails(fd)
	if ieraksts == nil {
		return Ebadf
	}
	if ieraksts.kind != fdkindconsole {
		if ieraksts.kind == fdkindLigzda {
			return ligzdaSūtītto(fd, address, count, 0, 0)
		}
		if ieraksts.kind == fdkindfat || ieraksts.kind == fdkindSakneMape {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBaitifromKursors(uintptr(address), int(count), int(count))
	console_2.MDrukāt(buffer)
	return int32(count)
}

func sysLasīt(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	ieraksts := getAtvērtFails(fd)
	if ieraksts == nil {
		return Ebadf
	}
	if ieraksts.kind == fdkindstdin {
		return lasītstdin(address, count)
	}
	if ieraksts.kind == fdkindSakneMape {
		return Eisdir
	}
	if ieraksts.kind == fdkindLigzda {
		return ligzdareceivefrom(fd, address, count, 0, 0)
	}
	if ieraksts.kind != fdkindfat {
		return Ebadf
	}
	if ieraksts.novietojums >= ieraksts.izmērs {
		return 0
	}
	remaining := ieraksts.izmērs - ieraksts.novietojums
	if count > remaining {
		count = remaining
	}
	buffer := GetBaitifromKursors(uintptr(address), int(count), int(count))
	return lasītvfsFails(ieraksts, buffer, count)
}

func sysAtvērt(cEĻŠaddress uint32, karogi uint32, režīms uint32) int32 {
	_ = režīms
	if cEĻŠaddress == 0 {
		return Efault
	}
	piekļūtRežīms := karogi & 3
	if piekļūtRežīms == oRakstītonly || piekļūtRežīms == oLasītRakstīt || (karogi&(ocreate|oApraut|oappend)) != 0 {
		return Erofs
	}

	process := ensurePašreizējaisprocess()
	if process == nil {
		return Enfile
	}
	apraksts := allocateAtvērtFails()
	if apraksts < 0 {
		return apraksts
	}
	ieraksts := &atvērtFailsTabula[apraksts]
	ieraksts.karogi = karogi
	if isSakneCEĻŠ(cEĻŠaddress) {
		ieraksts.kind = fdkindSakneMape
		ieraksts.izmērs = 0
	} else {
		nosaukumslen, nosaukums := kopētCEĻŠ(cEĻŠaddress)
		if nosaukumslen == 0 {
			*ieraksts = atvērtFailsApraksts{}
			return Enoent
		}
		izmērs := failsIzmērs(nosaukums[:nosaukumslen])
		if izmērs == 0 {
			*ieraksts = atvērtFailsApraksts{}
			return Enoent
		}
		if (karogi & oMape) != 0 {
			*ieraksts = atvērtFailsApraksts{}
			return Enotdir
		}
		ieraksts.kind = fdkindfat
		ieraksts.izmērs = izmērs
		ieraksts.nosaukumslen = nosaukumslen
		ieraksts.nosaukums = nosaukums
	}

	fd := allocatefd(process, apraksts, 3)
	if fd < 0 {
		*ieraksts = atvērtFailsApraksts{}
		return fd
	}
	return fd
}

func sysAizvērt(fd int32) int32 {
	return aizvērtprocessfd(ensurePašreizējaisprocess(), fd)
}

func sysdup(fd int32, minimums int32) int32 {
	process := ensurePašreizējaisprocess()
	ieraksts := getAtvērtFailsfor(process, fd)
	if ieraksts == nil {
		return Ebadf
	}
	jaunsfd := allocatefd(process, process.fds[fd].apraksts, minimums)
	if jaunsfd >= 0 {
		ieraksts.refs++
	}
	return jaunsfd
}

func sysdup2(oldfd int32, jaunsfd int32) int32 {
	process := ensurePašreizējaisprocess()
	ieraksts := getAtvērtFailsfor(process, oldfd)
	if ieraksts == nil {
		return Ebadf
	}
	if jaunsfd < 0 || jaunsfd >= maksfd {
		return Ebadf
	}
	if oldfd == jaunsfd {
		return jaunsfd
	}
	if process.fds[jaunsfd].izmantots {
		aizvērtprocessfd(process, jaunsfd)
	}
	process.fds[jaunsfd] = fdieraksts{izmantots: true, apraksts: process.fds[oldfd].apraksts}
	ieraksts.refs++
	return jaunsfd
}

func sysfcntl(fd int32, komanda uint32, argument uint32) int32 {
	process := ensurePašreizējaisprocess()
	ieraksts := getAtvērtFailsfor(process, fd)
	if ieraksts == nil {
		return Ebadf
	}
	switch komanda {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(process.fds[fd].fdKarogi)
	case fkopafd:
		process.fds[fd].fdKarogi = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(ieraksts.karogi)
	case fkopafl:
		ieraksts.karogi = (ieraksts.karogi & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	ieraksts := getAtvērtFails(fd)
	if ieraksts == nil {
		return Ebadf
	}
	if ieraksts.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekkopa:
		base = 0
	case seekPašreizējais:
		base = int64(ieraksts.novietojums)
	case seekBeigas:
		base = int64(ieraksts.izmērs)
	default:
		return Einval
	}
	novietojums_2 := base + int64(offset)
	if novietojums_2 < 0 || novietojums_2 > 0x7FFFFFFF {
		return Einval
	}
	ieraksts.novietojums = uint32(novietojums_2)
	return int32(ieraksts.novietojums)
}

func lasītvfsFails(ieraksts *atvērtFailsApraksts, mērķis_2 []byte, count uint32) int32 {
	atmiņamanager := &mem.TAtmiņamanager{}
	tmpKursors := atmiņamanager.Malloc(ieraksts.izmērs)
	if tmpKursors == nil {
		return Einval
	}
	tmp := GetBaitifromKursors(uintptr(tmpKursors), int(ieraksts.izmērs), int(ieraksts.izmērs))
	lasītFails(ieraksts.nosaukums[:ieraksts.nosaukumslen], tmp)
	copy(mērķis_2[:count], tmp[ieraksts.novietojums:ieraksts.novietojums+count])
	ieraksts.novietojums += count
	atmiņamanager.Brīvs(tmpKursors)
	return int32(count)
}

func isSakneCEĻŠ(cEĻŠaddress uint32) bool {
	if cEĻŠaddress == 0 {
		return false
	}
	cEĻŠ := GetBaitifromKursors(uintptr(cEĻŠaddress), 4, 4)
	if cEĻŠ[0] == '/' && cEĻŠ[1] == 0 {
		return true
	}
	if cEĻŠ[0] == '.' && cEĻŠ[1] == 0 {
		return true
	}
	if cEĻŠ[0] == '/' && cEĻŠ[1] == '.' && cEĻŠ[2] == 0 {
		return true
	}
	return false
}

func syspiekļūt(cEĻŠaddress uint32, režīms uint32) int32 {
	if cEĻŠaddress == 0 {
		return Efault
	}
	if (režīms & ^uint32(7)) != 0 {
		return Einval
	}
	isSakne := isSakneCEĻŠ(cEĻŠaddress)
	exists := isSakne
	if !exists {
		nosaukumslen, nosaukums := kopētCEĻŠ(cEĻŠaddress)
		exists = nosaukumslen != 0 && failsIzmērs(nosaukums[:nosaukumslen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (režīms & 2) != 0 {
		return Eacces
	}

	if (režīms&1) != 0 && !isSakne {
		return Eacces
	}
	return 0
}

func syschdir(cEĻŠaddress uint32) int32 {
	if cEĻŠaddress == 0 {
		return Efault
	}
	if !isSakneCEĻŠ(cEĻŠaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, izmērs uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if izmērs < 2 {
		return Erange
	}
	buffer_2 := GetBaitifromKursors(uintptr(bufferaddress), int(izmērs), int(izmērs))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, režīms uint32, izmērs uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Ierīce = 1
	stat.Ino = inode
	stat.Režīms = režīms
	stat.Nlink = 1
	stat.Izmērs_2 = int32(izmērs)
	stat.Blksize = 512
	stat.Bloks = int32((izmērs + 511) / 512)
	return 0
}

func sysstat(cEĻŠaddress uint32, stataddress uint32) int32 {
	if cEĻŠaddress == 0 {
		return Efault
	}
	if isSakneCEĻŠ(cEĻŠaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nosaukumslen, nosaukums := kopētCEĻŠ(cEĻŠaddress)
	if nosaukumslen == 0 {
		return Enoent
	}
	izmērs := failsIzmērs(nosaukums[:nosaukumslen])
	if izmērs == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nosaukumslen; i++ {
		inode = inode*33 + uint32(nosaukums[i])
	}
	return fillposixstat(stataddress, sifreg|0444, izmērs, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	ieraksts := getAtvērtFails(fd)
	if ieraksts == nil {
		return Ebadf
	}
	switch ieraksts.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindSakneMape:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, ieraksts.izmērs, uint32(fd+2))
	case fdkindLigzda:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getAtvērtFails(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	process := ensurePašreizējaisprocess()
	if process == nil {
		return 0
	}
	if process.programmabreak == 0 {
		process.programmabreak = lietotājsheapbase
	}
	if address_2 == 0 {
		return process.programmabreak
	}
	if address_2 < lietotājsheapbase || address_2 > lietotājsheapIerobežot {
		return process.programmabreak
	}
	process.programmabreak = address_2
	return process.programmabreak
}

func kopētutslauks(mērķis *[65]byte, vērtība string) {
	ierobežot := len(vērtība)
	if ierobežot > 64 {
		ierobežot = 64
	}
	for i := 0; i < ierobežot; i++ {
		mērķis[i] = vērtība[i]
	}
	mērķis[ierobežot] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nosaukums := (*posixutsname)(Pointer(uintptr(address_2)))
	*nosaukums = posixutsname{}
	kopētutslauks(&nosaukums.Sysname, "EngOS")
	kopētutslauks(&nosaukums.Nodename, "engos")
	kopētutslauks(&nosaukums.Release, "0.1-posix")
	kopētutslauks(&nosaukums.Versija, "POSIX.1-2017 phase 1")
	kopētutslauks(&nosaukums.Machine, "i386")
	return 0
}

func maiņvietaunsignedinteger16(vērtība uint16) uint16 {
	return (vērtība << 8) | (vērtība >> 8)
}

func ligzdacallargument(parametri_2 uint32, saturs uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(parametri_2 + saturs*4)))
}

func ligzdaforfd(fd int32) (*vietējaisdatagramLigzda, int32) {
	ieraksts := getAtvērtFails(fd)
	if ieraksts == nil || ieraksts.kind != fdkindLigzda || ieraksts.aux >= makssockets {
		return nil, Ebadf
	}
	ligzda := &vietējaissockets[ieraksts.aux]
	if !ligzda.izmantots {
		return nil, Ebadf
	}
	return ligzda, 0
}

func allocateLigzda(domēns uint32, ligzdaTips uint32, protocol uint32) int32 {
	if domēns != afinet {
		return Eafnosupport
	}
	if ligzdaTips != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensurePašreizējaisprocess()
	if process == nil {
		return Enfile
	}
	ligzdaSaturs := -1
	for i := 0; i < makssockets; i++ {
		if !vietējaissockets[i].izmantots {
			ligzdaSaturs = i
			break
		}
	}
	if ligzdaSaturs < 0 {
		return Enfile
	}
	apraksts := allocateAtvērtFails()
	if apraksts < 0 {
		return apraksts
	}
	vietējaissockets[ligzdaSaturs] = vietējaisdatagramLigzda{izmantots: true}
	ieraksts := &atvērtFailsTabula[apraksts]
	ieraksts.kind = fdkindLigzda
	ieraksts.karogi = oLasītRakstīt
	ieraksts.aux = uint32(ligzdaSaturs)
	fd := allocatefd(process, apraksts, 3)
	if fd < 0 {
		vietējaissockets[ligzdaSaturs] = vietējaisdatagramLigzda{}
		*ieraksts = atvērtFailsApraksts{}
		return fd
	}
	return fd
}

func ligzdaaddress(address_2 uint32, garums uint32) (*ligzdaaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if garums < 16 {
		return nil, Einval
	}
	result := (*ligzdaaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portsIenākošāIzmantot(ports uint16, except *vietējaisdatagramLigzda) bool {
	for i := 0; i < makssockets; i++ {
		ligzda := &vietējaissockets[i]
		if ligzda != except && ligzda.izmantots && ligzda.bound && ligzda.vietējais.Ports == ports {
			return true
		}
	}
	return false
}

func bindephemeral(ligzda *vietējaisdatagramLigzda) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		ports := maiņvietaunsignedinteger16(nākamaisephemeralPorts)
		nākamaisephemeralPorts++
		if nākamaisephemeralPorts < 49152 {
			nākamaisephemeralPorts = 49152
		}
		if !portsIenākošāIzmantot(ports, ligzda) {
			ligzda.vietējais = ligzdaaddressipv4{Family: afinet, Ports: ports, Address: 0x0100007F}
			ligzda.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func ligzdabind(fd int32, address_2 uint32, garums uint32) int32 {
	ligzda, err := ligzdaforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := ligzdaaddress(address_2, garums)
	if err != 0 {
		return err
	}
	if ligzda.bound {
		return Einval
	}
	if requested.Ports == 0 {
		return bindephemeral(ligzda)
	}
	if portsIenākošāIzmantot(requested.Ports, ligzda) {
		return Eaddrinuse
	}
	ligzda.vietējais = *requested
	ligzda.bound = true
	return 0
}

func ligzdaSavienoties(fd int32, address_2 uint32, garums uint32) int32 {
	ligzda, err := ligzdaforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := ligzdaaddress(address_2, garums)
	if err != 0 {
		return err
	}
	if !ligzda.bound {
		if err := bindephemeral(ligzda); err != 0 {
			return err
		}
	}
	ligzda.remote = *remote
	ligzda.connected = true
	return 0
}

func ligzdaSūtītto(fd int32, bufferaddress_2 uint32, garums uint32, mērķisaddress uint32, mērķisGarums uint32) int32 {
	ligzda, err := ligzdaforfd(fd)
	if err != 0 {
		return err
	}
	if garums > maksdatagramIzmērs {
		return Emsgsize
	}
	if garums != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var mērķis ligzdaaddressipv4
	if mērķisaddress != 0 {
		address_2, addressKļūda := ligzdaaddress(mērķisaddress, mērķisGarums)
		if addressKļūda != 0 {
			return addressKļūda
		}
		mērķis = *address_2
	} else {
		if !ligzda.connected {
			return Enotconn
		}
		mērķis = ligzda.remote
	}
	if !ligzda.bound {
		if bindKļūda := bindephemeral(ligzda); bindKļūda != 0 {
			return bindKļūda
		}
	}
	var receiver *vietējaisdatagramLigzda
	for i := 0; i < makssockets; i++ {
		candidate := &vietējaissockets[i]
		if candidate.izmantots && candidate.bound && candidate.vietējais.Ports == mērķis.Ports &&
			(candidate.vietējais.Address == 0 || candidate.vietējais.Address == mērķis.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksLigzdapackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = ligzdapacket{izmantots: true, izmērs: garums, avots: ligzda.vietējais}
	if garums != 0 {
		avots := GetBaitifromKursors(uintptr(bufferaddress_2), int(garums), int(garums))
		copy(packet.data[:garums], avots)
	}
	receiver.tail = (receiver.tail + 1) % maksLigzdapackets
	receiver.count++
	return int32(garums)
}

func ligzdareceivefrom(fd int32, bufferaddress_2 uint32, garums uint32, avotsaddress uint32, avotsGarumsaddress uint32) int32 {
	ligzda, err := ligzdaforfd(fd)
	if err != 0 {
		return err
	}
	if garums != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if ligzda.count == 0 {
		return Eagain
	}
	packet := &ligzda.packets[ligzda.head]
	kopētGarums := packet.izmērs
	if kopētGarums > garums {
		kopētGarums = garums
	}
	if kopētGarums != 0 {
		mērķis := GetBaitifromKursors(uintptr(bufferaddress_2), int(kopētGarums), int(kopētGarums))
		copy(mērķis, packet.data[:kopētGarums])
	}
	if avotsaddress != 0 {
		if avotsGarumsaddress == 0 {
			return Efault
		}
		providedGarums := (*uint32)(Pointer(uintptr(avotsGarumsaddress)))
		if *providedGarums >= 16 {
			*(*ligzdaaddressipv4)(Pointer(uintptr(avotsaddress))) = packet.avots
		}
		*providedGarums = 16
	}
	*packet = ligzdapacket{}
	ligzda.head = (ligzda.head + 1) % maksLigzdapackets
	ligzda.count--
	return int32(kopētGarums)
}

func kopētLigzdaNosaukums(fd int32, address_2 uint32, garumsaddress uint32, peer bool) int32 {
	ligzda, err := ligzdaforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || garumsaddress == 0 {
		return Efault
	}
	garums := (*uint32)(Pointer(uintptr(garumsaddress)))
	if *garums < 16 {
		*garums = 16
		return Einval
	}
	if peer {
		if !ligzda.connected {
			return Enotconn
		}
		*(*ligzdaaddressipv4)(Pointer(uintptr(address_2))) = ligzda.remote
	} else {
		if !ligzda.bound {
			if bindKļūda := bindephemeral(ligzda); bindKļūda != 0 {
				return bindKļūda
			}
		}
		*(*ligzdaaddressipv4)(Pointer(uintptr(address_2))) = ligzda.vietējais
	}
	*garums = 16
	return 0
}

func sysLigzdacall(call uint32, parametri_2 uint32) int32 {
	if parametri_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateLigzda(ligzdacallargument(parametri_2, 0), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2))
	case 2:
		return ligzdabind(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2))
	case 3:
		return ligzdaSavienoties(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopētLigzdaNosaukums(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2), false)
	case 7:
		return kopētLigzdaNosaukums(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2), true)
	case 9:
		return ligzdaSūtītto(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2), 0, 0)
	case 10:
		return ligzdareceivefrom(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2), 0, 0)
	case 11:
		return ligzdaSūtītto(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2), ligzdacallargument(parametri_2, 4), ligzdacallargument(parametri_2, 5))
	case 12:
		return ligzdareceivefrom(int32(ligzdacallargument(parametri_2, 0)), ligzdacallargument(parametri_2, 1), ligzdacallargument(parametri_2, 2), ligzdacallargument(parametri_2, 4), ligzdacallargument(parametri_2, 5))
	case 13:
		if _, err := ligzdaforfd(int32(ligzdacallargument(parametri_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := ligzdaforfd(int32(ligzdacallargument(parametri_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func lasītstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBaitifromKursors(uintptr(address), int(count), int(count))
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
	nākamais := (stdinRakstīt + 1) % uint32(len(stdinbuffer))
	if nākamais == stdinLasīt {
		return
	}
	stdinbuffer[stdinRakstīt] = c
	stdinRakstīt = nākamais
}

func stdingetblocking() byte {
	for stdinLasīt == stdinRakstīt {
		sc := pollKlaviatūrascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLasīt]
	stdinLasīt = (stdinLasīt + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlaviatūrascancode() byte {
	for (PortsLasītbyte(0x64) & 0x01) == 0 {
	}
	sc := PortsLasītbyte(0x60)
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

func kopētIzpildītvector(address_2 uint32, result *izpildītvector) int32 {
	*result = izpildītvector{}
	if address_2 == 0 {
		return 0
	}
	for saturs := uint32(0); saturs < maksIzpildītvectorieraksts; saturs++ {
		virkneaddress := *(*uint32)(Pointer(uintptr(address_2 + saturs*4)))
		if virkneaddress == 0 {
			result.count = saturs
			return 0
		}
		terminated := false
		for garums := uint32(0); garums <= maksIzpildītvirkneGarums; garums++ {
			vērtība := *(*byte)(Pointer(uintptr(virkneaddress + garums)))
			result.values[saturs][garums] = vērtība
			if vērtība == 0 {
				result.lengths[saturs] = garums
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

func pushIzpildītunsignedinteger32(stack *uint32, vērtība uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = vērtība
}

func setupIzpildītstack(cpu *TcpuStāvoklis, parametri_2 *izpildītvector, environment *izpildītvector) int32 {
	const stackBaiti uint32 = 4096
	if !MakeApgabalsPrivātswritable(getcr3(), LietotājsstackAugšā-stackBaiti, stackBaiti) {
		return Enomem
	}
	stack := LietotājsstackAugšā
	var argumentpointers [maksIzpildītvectorieraksts]uint32
	var environmentpointers [maksIzpildītvectorieraksts]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		garums := environment.lengths[i] + 1
		stack -= garums
		mērķis := GetBaitifromKursors(uintptr(stack), int(garums), int(garums))
		copy(mērķis, environment.values[i][:garums])
		environmentpointers[i] = stack
	}
	for i := int(parametri_2.count) - 1; i >= 0; i-- {
		garums := parametri_2.lengths[i] + 1
		stack -= garums
		mērķis := GetBaitifromKursors(uintptr(stack), int(garums), int(garums))
		copy(mērķis, parametri_2.values[i][:garums])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushIzpildītunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushIzpildītunsignedinteger32(&stack, environmentpointers[i])
	}
	pushIzpildītunsignedinteger32(&stack, 0)
	for i := int(parametri_2.count) - 1; i >= 0; i-- {
		pushIzpildītunsignedinteger32(&stack, argumentpointers[i])
	}
	pushIzpildītunsignedinteger32(&stack, parametri_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func aizvērtIeslēgtsIzpildīt(process *processieraksts) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if process.fds[fd].izmantots && (process.fds[fd].fdKarogi&fdcloexec) != 0 {
			aizvērtprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *TcpuStāvoklis, cEĻŠaddress uint32) int32 {
	if cEĻŠaddress == 0 {
		return Efault
	}
	var parametri_2 izpildītvector
	var environment izpildītvector
	if result := kopētIzpildītvector(cpu.Ecx, &parametri_2); result < 0 {
		return result
	}
	if result := kopētIzpildītvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	nosaukumslen, nosaukums := kopētCEĻŠ(cEĻŠaddress)
	if nosaukumslen == 0 {
		return Enoent
	}
	izmērs := failsIzmērs(nosaukums[:nosaukumslen])
	if izmērs == 0 {
		return Enoent
	}
	atmiņamanager := &mem.TAtmiņamanager{}
	failsKursors := atmiņamanager.Malloc(izmērs)
	if failsKursors == nil {
		return Einval
	}
	data := GetBaitifromKursors(uintptr(failsKursors), int(izmērs), int(izmērs))
	lasītFails(nosaukums[:nosaukumslen], data)
	if izmērs < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		atmiņamanager.Brīvs(failsKursors)
		return Enoexec
	}
	loader := Elf{}
	ieraksts := loader.Getieraksts(data)
	loader.Parse(data, getcr3())
	atmiņamanager.Brīvs(failsKursors)
	if result := setupIzpildītstack(cpu, &parametri_2, &environment); result < 0 {
		return result
	}
	aizvērtIeslēgtsIzpildīt(ensurePašreizējaisprocess())
	cpu.Eip = ieraksts
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStāvoklis) int32 {
	vecākspid := Pašreizējaispid()
	if ensurePašreizējaisprocess() == nil {
		return Enfile
	}
	pid := allocateprocess(vecākspid)
	if pid == 0 {
		return Einval
	}
	atmiņamanager := &mem.TAtmiņamanager{}
	threadKursors := atmiņamanager.Malloc(uint32(Sizeof(TThread{})))
	stackKursors := atmiņamanager.Malloc(ThreadstackIzmērs)
	bērnsLapaMape := Cloneaddressspacecow(getcr3())
	if threadKursors == nil || stackKursors == nil || bērnsLapaMape == 0 {
		izmestprocess(pid)
		return Einval
	}
	bērns := (*TThread)(threadKursors)
	bērns.Stack = uint32(uintptr(stackKursors))
	bērns.CpuStāvoklis = (*TcpuStāvoklis)(Pointer(uintptr(stackKursors) + ThreadstackIzmērs - Sizeof(TcpuStāvoklis{})))
	*bērns.CpuStāvoklis = *cpu
	bērns.CpuStāvoklis.Eax = 0
	bērns.Lietotājsstack_2 = cpu.Esp
	bērns.LietotājsstackIzmērs_2 = 0
	bērns.Pid = pid
	bērns.Vecākspid = vecākspid
	bērns.LapaMapeieraksts = bērnsLapaMape
	bērns.ThreadStāvoklis = Gatavs
	bērns.Fpuoffset = 0xffffffff
	bērns.Iskernel = false
	Pievienotrunnablethread(bērns)
	return int32(pid)
}

func sysIziet(statuss uint32) {
	pid := Pašreizējaispid()
	for i := 0; i < len(processTabula); i++ {
		if processTabula[i].izmantots && processTabula[i].pid == pid {
			aizvērtVisiprocessfds(&processTabula[i])
			processTabula[i].exited = true
			processTabula[i].statuss = (statuss & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statussaddress uint32, opcijas uint32) int32 {
	if (opcijas & ^uint32(1)) != 0 {
		return Einval
	}
	vecākspid := Pašreizējaispid()
	foundbērns := false
	for i := 0; i < len(processTabula); i++ {
		p := &processTabula[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.izmantots && matches && p.vecāks == vecākspid {
			foundbērns = true
			if p.exited {
				if statussaddress != 0 {
					*(*uint32)(Pointer(uintptr(statussaddress))) = p.statuss
				}
				bērnspid := p.pid
				*p = processieraksts{}
				return int32(bērnspid)
			}
		}
	}
	if !foundbērns {
		return Echild
	}

	if (opcijas & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocess(vecāks uint32) uint32 {
	vecāksprocess := meklētprocess(vecāks)
	pid := Allocatepid()
	for i := 0; i < len(processTabula); i++ {
		if !processTabula[i].izmantots {
			processTabula[i] = processieraksts{
				izmantots:	true,
				pid:		pid,
				vecāks:		vecāks,
				programmabreak:	lietotājsheapbase,
			}
			if vecāksprocess != nil {
				processTabula[i].programmabreak = vecāksprocess.programmabreak
				for fd := 0; fd < maksfd; fd++ {
					if vecāksprocess.fds[fd].izmantots {
						processTabula[i].fds[fd] = vecāksprocess.fds[fd]
						apraksts := vecāksprocess.fds[fd].apraksts
						if apraksts >= 0 && apraksts < maksAtvērtFAILI {
							atvērtFailsTabula[apraksts].refs++
						}
					}
				}
			} else {
				initializeprocessfds(&processTabula[i])
			}
			return pid
		}
	}
	return 0
}

func aizvērtVisiprocessfds(process *processieraksts) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if process.fds[fd].izmantots {
			aizvērtprocessfd(process, fd)
		}
	}
}

func izmestprocess(pid uint32) {
	process := meklētprocess(pid)
	if process == nil {
		return
	}
	aizvērtVisiprocessfds(process)
	*process = processieraksts{}
}

func kopētCEĻŠ(cEĻŠaddress uint32) (uint32, [12]byte) {
	var nosaukums [12]byte
	if cEĻŠaddress == 0 {
		return 0, nosaukums
	}
	raw := GetBaitifromKursors(uintptr(cEĻŠaddress), 64, 64)
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
		nosaukums[n] = c
		n++
	}
	return n, nosaukums
}

func failsIzmērs(failanosaukums []byte) uint32 {
	var ata0s = TPaplašinātiTehnoloģijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabula{}
	partition.Lasītpartition(&ata0s)

	bios := TBiosparameterBloks32{}
	izmērs := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failanosaukums)
	ata0s.Flush()
	return izmērs
}

func lasītFails(failanosaukums []byte, data []byte) {
	var ata0s = TPaplašinātiTehnoloģijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabula{}
	partition.Lasītpartition(&ata0s)

	bios := TBiosparameterBloks32{}
	bios.Lasīt(&ata0s, partition.Mbr.Primarypartition[0], failanosaukums, data)
	ata0s.Flush()
}

func getcr3() uint32
