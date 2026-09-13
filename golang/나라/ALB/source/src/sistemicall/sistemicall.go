package sistemicall

import . "unsafe"

import . "interrupt"
import . "konsolë"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "kartelëSistemi/msdospartition"
import . "kartelëSistemi/fat"
import . "kartelëSistemi/elf"
import mem "memoriaManazhuesi"
import . "paging"
import . "porta"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualMemoria"

var konsolë_2 = TKonsolë{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysDalja	uint32	= 1
	Sysfork		uint32	= 2
	SysLeximi	uint32	= 3
	SysShkrimi	uint32	= 4
	SysHap		uint32	= 5
	SysMbyll	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysfutja	uint32	= 33
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
	SysrtDalja	uint32	= 252

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
	stdinPF		int32	= 0
	stdoutPF	int32	= 1
	stderrPF	int32	= 2
	maxPF			= 32
	maxHapKartela		= 128
)

type pFentry struct {
	përdorur	bool
	përshkrimi	int32
	pFFlamurka	uint32
}

type hapKartelëPërshkrimi struct {
	përdorur	bool
	refs		uint32
	kind		uint32
	flamurka	uint32
	pozicion	uint32
	madhësia	uint32
	emri		[12]byte
	emrilen		uint32
	aux		uint32
}

const (
	pFkindAsnjë		uint32	= 0
	pFkindfat		uint32	= 1
	pFkindstdin		uint32	= 2
	pFkindKonsolë		uint32	= 3
	pFkindRrënjëDosje	uint32	= 4
	pFkindsocket		uint32	= 5

	oLeximionly	uint32	= 0
	oShkrimionly	uint32	= 1
	oLeximiShkrimi	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oDosje		uint32	= 0x10000

	seekCaktoni	uint32	= 0
	seekEtanishme	uint32	= 1
	seekFund	uint32	= 2

	fdupPF		uint32	= 0
	fgetPF		uint32	= 1
	fCaktoniPF	uint32	= 2
	fgetfl		uint32	= 3
	fCaktonifl	uint32	= 4
	pFcloexec	uint32	= 1

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
	maxsocketpackets	= 8
	maxdatagramMadhësia	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Porta	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	përdorur	bool
	madhësia	uint32
	burimi		socketaddressipv4
	data		[maxdatagramMadhësia]byte
}

type localdatagramsocket struct {
	përdorur	bool
	bound		bool
	connected	bool
	local		socketaddressipv4
	remote		socketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Dispozitivi	uint32
	Ino		uint32
	Mënyrë		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Madhësia_2	int32
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
	maxexecvectorentry	= 16
	maxexecvargGjatësi	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecvargGjatësi + 1]byte
}

type proçesentry struct {
	përdorur	bool
	pid		uint32
	prind		uint32
	exited		bool
	gjendja		uint32
	programibreak	uint32
	fds		[maxPF]pFentry
}

type vargheader struct {
	Data	uintptr
	Len	int
}

func syscallGabim(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var hapKartelëTabela [maxHapKartela]hapKartelëPërshkrimi
var proçesTabela [32]proçesentry
var localsockets [maxsockets]localdatagramsocket
var pasuesenephemeralPorta uint16 = 49152

const (
	përdoruesiheapbase	uint32	= 0x06000000
	përdoruesiheapKufi	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLeximi uint32
var stdinShkrimi uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysDalja_2(treguesi uint32) {
	Syscall(SysDalja, treguesi)
}

func SysLeximi_2(pF uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLeximi, pF, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysPrintostr(buffer string) {
	h := (*vargheader)(Pointer(&buffer))
	Syscall(SysShkrimi, uint32(stdoutPF), uint32(h.Data), uint32(h.Len))
}

func SysPrintounsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysShkrimi, uint32(stdoutPF), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysHap_2(pOZICIONI uintptr, flamurka uint32, mënyrë uint32) int32 {
	return int32(Syscall(SysHap, uint32(pOZICIONI), flamurka, mënyrë))
}

func SysMbyll_2(pF uint32) int32 {
	return int32(Syscall(SysMbyll, pF))
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
		return syscallGabim(Enosys)
	}
}

func (vetvetja *TSyscall) Init(manazhuesi *TInterruptManazhuesi) {
	initKartelëdescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	vetvetja.TInterrupthandler.Init(0x80, uintptr(Pointer(manazhuesi)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*TcpuGjendje)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysDalja:
		sysDalja(cpu.Ebx)
		return uint32(uintptr(Pointer(NdaloEtanishmethread(cpu))))
	case SysrtDalja:
		sysDalja(cpu.Ebx)
		return uint32(uintptr(Pointer(NdaloEtanishmethread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLeximi:
		cpu.Eax = uint32(sysLeximi(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysShkrimi:
		cpu.Eax = uint32(sysShkrimi(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysHap:
		cpu.Eax = uint32(sysHap(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysHap(cpu.Ebx, ocreate|oShkrimionly|otruncate, cpu.Ecx))
		return esp
	case SysMbyll:
		cpu.Eax = uint32(sysMbyll(int32(cpu.Ebx)))
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
		cpu.Eax = Etanishmepid()
		return esp
	case Sysgetppid:
		cpu.Eax = Etanishmeprindpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysfutja:
		cpu.Eax = uint32(sysfutja(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(syssocketcall(cpu.Ebx, cpu.Ecx))
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
		konsolë_2.MUnsignedinteger32Printo(cpu.Ebx)
		return esp

	default:
		konsolë_2.MPrintoxy(([]byte)("sys["), 1, 23)
		konsolë_2.MUnsignedinteger32Printo(esp)
		konsolë_2.MPrinto(([]byte)(":"))
		konsolë_2.MUnsignedinteger32Printo(cpu.Eax)
		konsolë_2.MPrinto(([]byte)(":"))
		konsolë_2.MUnsignedinteger32Printo(cpu.Ebx)
		konsolë_2.MPrinto(([]byte)(":"))
		konsolë_2.MUnsignedinteger32Printo(cpu.Ecx)
		konsolë_2.MPrinto(([]byte)(":"))
		konsolë_2.MUnsignedinteger32Printo(cpu.Edx)
		konsolë_2.MPrinto(([]byte)("]"))
		cpu.Eax = syscallGabim(Enosys)
		return esp
	}

	return esp
}

func initKartelëdescriptor() {
	for i := 0; i < maxHapKartela; i++ {
		hapKartelëTabela[i] = hapKartelëPërshkrimi{}
	}
	for i := 0; i < len(proçesTabela); i++ {
		proçesTabela[i] = proçesentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	pasuesenephemeralPorta = 49152
	hapKartelëTabela[0] = hapKartelëPërshkrimi{përdorur: true, kind: pFkindstdin, flamurka: oLeximionly}
	hapKartelëTabela[1] = hapKartelëPërshkrimi{përdorur: true, kind: pFkindKonsolë, flamurka: oShkrimionly}
	hapKartelëTabela[2] = hapKartelëPërshkrimi{përdorur: true, kind: pFkindKonsolë, flamurka: oShkrimionly}
}

func gjejProçes(pid uint32) *proçesentry {
	for i := 0; i < len(proçesTabela); i++ {
		if proçesTabela[i].përdorur && proçesTabela[i].pid == pid {
			return &proçesTabela[i]
		}
	}
	return nil
}

func initializeProçesfds(proçes *proçesentry) {
	for pF := int32(0); pF <= stderrPF; pF++ {
		proçes.fds[pF] = pFentry{përdorur: true, përshkrimi: pF}
		hapKartelëTabela[pF].refs++
	}
}

func ensureEtanishmeProçes() *proçesentry {
	pid := Etanishmepid()
	if proçes := gjejProçes(pid); proçes != nil {
		return proçes
	}
	for i := 0; i < len(proçesTabela); i++ {
		if !proçesTabela[i].përdorur {
			proçesTabela[i] = proçesentry{
				përdorur:	true,
				pid:		pid,
				prind:		Etanishmeprindpid(),
				programibreak:	përdoruesiheapbase,
			}
			initializeProçesfds(&proçesTabela[i])
			return &proçesTabela[i]
		}
	}
	return nil
}

func getHapKartelëfor(proçes *proçesentry, pF int32) *hapKartelëPërshkrimi {
	if proçes == nil || pF < 0 || pF >= maxPF || !proçes.fds[pF].përdorur {
		return nil
	}
	përshkrimi := proçes.fds[pF].përshkrimi
	if përshkrimi < 0 || përshkrimi >= maxHapKartela || !hapKartelëTabela[përshkrimi].përdorur {
		return nil
	}
	return &hapKartelëTabela[përshkrimi]
}

func getHapKartelë(pF int32) *hapKartelëPërshkrimi {
	return getHapKartelëfor(ensureEtanishmeProçes(), pF)
}

func allocateHapKartelë() int32 {
	for i := int32(3); i < maxHapKartela; i++ {
		if !hapKartelëTabela[i].përdorur {
			hapKartelëTabela[i] = hapKartelëPërshkrimi{përdorur: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatePF(proçes *proçesentry, përshkrimi int32, minimum int32) int32 {
	if proçes == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxPF {
		return Einval
	}
	for pF := minimum; pF < maxPF; pF++ {
		if !proçes.fds[pF].përdorur {
			proçes.fds[pF] = pFentry{përdorur: true, përshkrimi: përshkrimi}
			return pF
		}
	}
	return Emfile
}

func releaseHapKartelë(përshkrimi int32) {
	if përshkrimi < 0 || përshkrimi >= maxHapKartela {
		return
	}
	entry := &hapKartelëTabela[përshkrimi]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && përshkrimi > stderrPF {
		if entry.kind == pFkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = hapKartelëPërshkrimi{}
	}
}

func mbyllProçesPF(proçes *proçesentry, pF int32) int32 {
	if proçes == nil || getHapKartelëfor(proçes, pF) == nil {
		return Ebadf
	}
	përshkrimi := proçes.fds[pF].përshkrimi
	proçes.fds[pF] = pFentry{}
	releaseHapKartelë(përshkrimi)
	return 0
}

func sysShkrimi(pF int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getHapKartelë(pF)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != pFkindKonsolë {
		if entry.kind == pFkindsocket {
			return socketDërgoto(pF, address, count, 0, 0)
		}
		if entry.kind == pFkindfat || entry.kind == pFkindRrënjëDosje {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbytesfromKursori(uintptr(address), int(count), int(count))
	konsolë_2.MPrinto(buffer)
	return int32(count)
}

func sysLeximi(pF int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getHapKartelë(pF)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == pFkindstdin {
		return leximistdin(address, count)
	}
	if entry.kind == pFkindRrënjëDosje {
		return Eisdir
	}
	if entry.kind == pFkindsocket {
		return socketreceivefrom(pF, address, count, 0, 0)
	}
	if entry.kind != pFkindfat {
		return Ebadf
	}
	if entry.pozicion >= entry.madhësia {
		return 0
	}
	remaining := entry.madhësia - entry.pozicion
	if count > remaining {
		count = remaining
	}
	buffer := GetbytesfromKursori(uintptr(address), int(count), int(count))
	return leximivfsKartelë(entry, buffer, count)
}

func sysHap(pOZICIONIaddress uint32, flamurka uint32, mënyrë uint32) int32 {
	_ = mënyrë
	if pOZICIONIaddress == 0 {
		return Efault
	}
	futjamënyrë := flamurka & 3
	if futjamënyrë == oShkrimionly || futjamënyrë == oLeximiShkrimi || (flamurka&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	proçes := ensureEtanishmeProçes()
	if proçes == nil {
		return Enfile
	}
	përshkrimi := allocateHapKartelë()
	if përshkrimi < 0 {
		return përshkrimi
	}
	entry := &hapKartelëTabela[përshkrimi]
	entry.flamurka = flamurka
	if isRrënjëPOZICIONI(pOZICIONIaddress) {
		entry.kind = pFkindRrënjëDosje
		entry.madhësia = 0
	} else {
		emrilen, emri := kopjoPOZICIONI(pOZICIONIaddress)
		if emrilen == 0 {
			*entry = hapKartelëPërshkrimi{}
			return Enoent
		}
		madhësia := kartelëMadhësia(emri[:emrilen])
		if madhësia == 0 {
			*entry = hapKartelëPërshkrimi{}
			return Enoent
		}
		if (flamurka & oDosje) != 0 {
			*entry = hapKartelëPërshkrimi{}
			return Enotdir
		}
		entry.kind = pFkindfat
		entry.madhësia = madhësia
		entry.emrilen = emrilen
		entry.emri = emri
	}

	pF := allocatePF(proçes, përshkrimi, 3)
	if pF < 0 {
		*entry = hapKartelëPërshkrimi{}
		return pF
	}
	return pF
}

func sysMbyll(pF int32) int32 {
	return mbyllProçesPF(ensureEtanishmeProçes(), pF)
}

func sysdup(pF int32, minimum int32) int32 {
	proçes := ensureEtanishmeProçes()
	entry := getHapKartelëfor(proçes, pF)
	if entry == nil {
		return Ebadf
	}
	iRiPF := allocatePF(proçes, proçes.fds[pF].përshkrimi, minimum)
	if iRiPF >= 0 {
		entry.refs++
	}
	return iRiPF
}

func sysdup2(oldPF int32, iRiPF int32) int32 {
	proçes := ensureEtanishmeProçes()
	entry := getHapKartelëfor(proçes, oldPF)
	if entry == nil {
		return Ebadf
	}
	if iRiPF < 0 || iRiPF >= maxPF {
		return Ebadf
	}
	if oldPF == iRiPF {
		return iRiPF
	}
	if proçes.fds[iRiPF].përdorur {
		mbyllProçesPF(proçes, iRiPF)
	}
	proçes.fds[iRiPF] = pFentry{përdorur: true, përshkrimi: proçes.fds[oldPF].përshkrimi}
	entry.refs++
	return iRiPF
}

func sysfcntl(pF int32, urdhër uint32, argument uint32) int32 {
	proçes := ensureEtanishmeProçes()
	entry := getHapKartelëfor(proçes, pF)
	if entry == nil {
		return Ebadf
	}
	switch urdhër {
	case fdupPF:
		return sysdup(pF, int32(argument))
	case fgetPF:
		return int32(proçes.fds[pF].pFFlamurka)
	case fCaktoniPF:
		proçes.fds[pF].pFFlamurka = argument & pFcloexec
		return 0
	case fgetfl:
		return int32(entry.flamurka)
	case fCaktonifl:
		entry.flamurka = (entry.flamurka & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(pF int32, offset int32, whence uint32) int32 {
	entry := getHapKartelë(pF)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != pFkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekCaktoni:
		base = 0
	case seekEtanishme:
		base = int64(entry.pozicion)
	case seekFund:
		base = int64(entry.madhësia)
	default:
		return Einval
	}
	pozicion_2 := base + int64(offset)
	if pozicion_2 < 0 || pozicion_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.pozicion = uint32(pozicion_2)
	return int32(entry.pozicion)
}

func leximivfsKartelë(entry *hapKartelëPërshkrimi, destinacioni_2 []byte, count uint32) int32 {
	memoriaManazhuesi := &mem.TMemoriaManazhuesi{}
	tmpKursori := memoriaManazhuesi.Malloc(entry.madhësia)
	if tmpKursori == nil {
		return Einval
	}
	tmp := GetbytesfromKursori(uintptr(tmpKursori), int(entry.madhësia), int(entry.madhësia))
	leximiKartelë(entry.emri[:entry.emrilen], tmp)
	copy(destinacioni_2[:count], tmp[entry.pozicion:entry.pozicion+count])
	entry.pozicion += count
	memoriaManazhuesi.Elirë(tmpKursori)
	return int32(count)
}

func isRrënjëPOZICIONI(pOZICIONIaddress uint32) bool {
	if pOZICIONIaddress == 0 {
		return false
	}
	pOZICIONI := GetbytesfromKursori(uintptr(pOZICIONIaddress), 4, 4)
	if pOZICIONI[0] == '/' && pOZICIONI[1] == 0 {
		return true
	}
	if pOZICIONI[0] == '.' && pOZICIONI[1] == 0 {
		return true
	}
	if pOZICIONI[0] == '/' && pOZICIONI[1] == '.' && pOZICIONI[2] == 0 {
		return true
	}
	return false
}

func sysfutja(pOZICIONIaddress uint32, mënyrë uint32) int32 {
	if pOZICIONIaddress == 0 {
		return Efault
	}
	if (mënyrë & ^uint32(7)) != 0 {
		return Einval
	}
	isRrënjë := isRrënjëPOZICIONI(pOZICIONIaddress)
	exists := isRrënjë
	if !exists {
		emrilen, emri := kopjoPOZICIONI(pOZICIONIaddress)
		exists = emrilen != 0 && kartelëMadhësia(emri[:emrilen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mënyrë & 2) != 0 {
		return Eacces
	}

	if (mënyrë&1) != 0 && !isRrënjë {
		return Eacces
	}
	return 0
}

func syschdir(pOZICIONIaddress uint32) int32 {
	if pOZICIONIaddress == 0 {
		return Efault
	}
	if !isRrënjëPOZICIONI(pOZICIONIaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, madhësia uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if madhësia < 2 {
		return Erange
	}
	buffer_2 := GetbytesfromKursori(uintptr(bufferaddress), int(madhësia), int(madhësia))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mënyrë uint32, madhësia uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dispozitivi = 1
	stat.Ino = inode
	stat.Mënyrë = mënyrë
	stat.Nlink = 1
	stat.Madhësia_2 = int32(madhësia)
	stat.Blksize = 512
	stat.Block = int32((madhësia + 511) / 512)
	return 0
}

func sysstat(pOZICIONIaddress uint32, stataddress uint32) int32 {
	if pOZICIONIaddress == 0 {
		return Efault
	}
	if isRrënjëPOZICIONI(pOZICIONIaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	emrilen, emri := kopjoPOZICIONI(pOZICIONIaddress)
	if emrilen == 0 {
		return Enoent
	}
	madhësia := kartelëMadhësia(emri[:emrilen])
	if madhësia == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < emrilen; i++ {
		inode = inode*33 + uint32(emri[i])
	}
	return fillposixstat(stataddress, sifreg|0444, madhësia, inode)
}

func sysfstat(pF int32, stataddress uint32) int32 {
	entry := getHapKartelë(pF)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case pFkindstdin, pFkindKonsolë:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(pF+1))
	case pFkindRrënjëDosje:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case pFkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.madhësia, uint32(pF+2))
	case pFkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(pF+2))
	}
	return Ebadf
}

func sysfsync(pF int32) int32 {
	if getHapKartelë(pF) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proçes := ensureEtanishmeProçes()
	if proçes == nil {
		return 0
	}
	if proçes.programibreak == 0 {
		proçes.programibreak = përdoruesiheapbase
	}
	if address_2 == 0 {
		return proçes.programibreak
	}
	if address_2 < përdoruesiheapbase || address_2 > përdoruesiheapKufi {
		return proçes.programibreak
	}
	proçes.programibreak = address_2
	return proçes.programibreak
}

func kopjoutsfield(destinacioni *[65]byte, vlera string) {
	kufi := len(vlera)
	if kufi > 64 {
		kufi = 64
	}
	for i := 0; i < kufi; i++ {
		destinacioni[i] = vlera[i]
	}
	destinacioni[kufi] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	emri := (*posixutsname)(Pointer(uintptr(address_2)))
	*emri = posixutsname{}
	kopjoutsfield(&emri.Sysname, "EngOS")
	kopjoutsfield(&emri.Nodename, "engos")
	kopjoutsfield(&emri.Release, "0.1-posix")
	kopjoutsfield(&emri.Version, "POSIX.1-2017 phase 1")
	kopjoutsfield(&emri.Machine, "i386")
	return 0
}

func swapunsignedinteger16(vlera uint16) uint16 {
	return (vlera << 8) | (vlera >> 8)
}

func socketcallargument(argumente_2 uint32, treguesi uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumente_2 + treguesi*4)))
}

func socketforPF(pF int32) (*localdatagramsocket, int32) {
	entry := getHapKartelë(pF)
	if entry == nil || entry.kind != pFkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.përdorur {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domeini uint32, socketLloji uint32, protocol uint32) int32 {
	if domeini != afinet {
		return Eafnosupport
	}
	if socketLloji != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proçes := ensureEtanishmeProçes()
	if proçes == nil {
		return Enfile
	}
	socketTreguesi := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].përdorur {
			socketTreguesi = i
			break
		}
	}
	if socketTreguesi < 0 {
		return Enfile
	}
	përshkrimi := allocateHapKartelë()
	if përshkrimi < 0 {
		return përshkrimi
	}
	localsockets[socketTreguesi] = localdatagramsocket{përdorur: true}
	entry := &hapKartelëTabela[përshkrimi]
	entry.kind = pFkindsocket
	entry.flamurka = oLeximiShkrimi
	entry.aux = uint32(socketTreguesi)
	pF := allocatePF(proçes, përshkrimi, 3)
	if pF < 0 {
		localsockets[socketTreguesi] = localdatagramsocket{}
		*entry = hapKartelëPërshkrimi{}
		return pF
	}
	return pF
}

func socketaddress(address_2 uint32, gjatësi uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if gjatësi < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portaZmadhoPërdor(porta uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.përdorur && socket.bound && socket.local.Porta == porta {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		porta := swapunsignedinteger16(pasuesenephemeralPorta)
		pasuesenephemeralPorta++
		if pasuesenephemeralPorta < 49152 {
			pasuesenephemeralPorta = 49152
		}
		if !portaZmadhoPërdor(porta, socket) {
			socket.local = socketaddressipv4{Family: afinet, Porta: porta, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(pF int32, address_2 uint32, gjatësi uint32) int32 {
	socket, err := socketforPF(pF)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, gjatësi)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Porta == 0 {
		return bindephemeral(socket)
	}
	if portaZmadhoPërdor(requested.Porta, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketLidhu(pF int32, address_2 uint32, gjatësi uint32) int32 {
	socket, err := socketforPF(pF)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, gjatësi)
	if err != 0 {
		return err
	}
	if !socket.bound {
		if err := bindephemeral(socket); err != 0 {
			return err
		}
	}
	socket.remote = *remote
	socket.connected = true
	return 0
}

func socketDërgoto(pF int32, bufferaddress_2 uint32, gjatësi uint32, destinacioniaddress uint32, destinacioniGjatësi uint32) int32 {
	socket, err := socketforPF(pF)
	if err != 0 {
		return err
	}
	if gjatësi > maxdatagramMadhësia {
		return Emsgsize
	}
	if gjatësi != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destinacioni socketaddressipv4
	if destinacioniaddress != 0 {
		address_2, addressGabim := socketaddress(destinacioniaddress, destinacioniGjatësi)
		if addressGabim != 0 {
			return addressGabim
		}
		destinacioni = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destinacioni = socket.remote
	}
	if !socket.bound {
		if bindGabim := bindephemeral(socket); bindGabim != 0 {
			return bindGabim
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.përdorur && candidate.bound && candidate.local.Porta == destinacioni.Porta &&
			(candidate.local.Address == 0 || candidate.local.Address == destinacioni.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxsocketpackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = socketpacket{përdorur: true, madhësia: gjatësi, burimi: socket.local}
	if gjatësi != 0 {
		burimi := GetbytesfromKursori(uintptr(bufferaddress_2), int(gjatësi), int(gjatësi))
		copy(packet.data[:gjatësi], burimi)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(gjatësi)
}

func socketreceivefrom(pF int32, bufferaddress_2 uint32, gjatësi uint32, burimiaddress uint32, burimiGjatësiaddress uint32) int32 {
	socket, err := socketforPF(pF)
	if err != 0 {
		return err
	}
	if gjatësi != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	kopjoGjatësi := packet.madhësia
	if kopjoGjatësi > gjatësi {
		kopjoGjatësi = gjatësi
	}
	if kopjoGjatësi != 0 {
		destinacioni := GetbytesfromKursori(uintptr(bufferaddress_2), int(kopjoGjatësi), int(kopjoGjatësi))
		copy(destinacioni, packet.data[:kopjoGjatësi])
	}
	if burimiaddress != 0 {
		if burimiGjatësiaddress == 0 {
			return Efault
		}
		providedGjatësi := (*uint32)(Pointer(uintptr(burimiGjatësiaddress)))
		if *providedGjatësi >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(burimiaddress))) = packet.burimi
		}
		*providedGjatësi = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(kopjoGjatësi)
}

func kopjosocketEmri(pF int32, address_2 uint32, gjatësiaddress uint32, peer bool) int32 {
	socket, err := socketforPF(pF)
	if err != 0 {
		return err
	}
	if address_2 == 0 || gjatësiaddress == 0 {
		return Efault
	}
	gjatësi := (*uint32)(Pointer(uintptr(gjatësiaddress)))
	if *gjatësi < 16 {
		*gjatësi = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindGabim := bindephemeral(socket); bindGabim != 0 {
				return bindGabim
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.local
	}
	*gjatësi = 16
	return 0
}

func syssocketcall(call uint32, argumente_2 uint32) int32 {
	if argumente_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(argumente_2, 0), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2))
	case 3:
		return socketLidhu(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopjosocketEmri(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), false)
	case 7:
		return kopjosocketEmri(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), true)
	case 9:
		return socketDërgoto(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), 0, 0)
	case 11:
		return socketDërgoto(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), socketcallargument(argumente_2, 4), socketcallargument(argumente_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), socketcallargument(argumente_2, 4), socketcallargument(argumente_2, 5))
	case 13:
		if _, err := socketforPF(int32(socketcallargument(argumente_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := socketforPF(int32(socketcallargument(argumente_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func leximistdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetbytesfromKursori(uintptr(address), int(count), int(count))
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
	pasuesen := (stdinShkrimi + 1) % uint32(len(stdinbuffer))
	if pasuesen == stdinLeximi {
		return
	}
	stdinbuffer[stdinShkrimi] = c
	stdinShkrimi = pasuesen
}

func stdingetblocking() byte {
	for stdinLeximi == stdinShkrimi {
		sc := pollTastierascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLeximi]
	stdinLeximi = (stdinLeximi + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastierascancode() byte {
	for (PortaLeximibyte(0x64) & 0x01) == 0 {
	}
	sc := PortaLeximibyte(0x60)
	return scancodetobyte_2(sc)
}

func scancodetobyte_2(sc uint8) byte {
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

func kopjoexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for treguesi := uint32(0); treguesi < maxexecvectorentry; treguesi++ {
		vargaddress := *(*uint32)(Pointer(uintptr(address_2 + treguesi*4)))
		if vargaddress == 0 {
			result.count = treguesi
			return 0
		}
		terminated := false
		for gjatësi := uint32(0); gjatësi <= maxexecvargGjatësi; gjatësi++ {
			vlera := *(*byte)(Pointer(uintptr(vargaddress + gjatësi)))
			result.values[treguesi][gjatësi] = vlera
			if vlera == 0 {
				result.lengths[treguesi] = gjatësi
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

func pushexecunsignedinteger32(stack *uint32, vlera uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = vlera
}

func setupexecstack(cpu *TcpuGjendje, argumente_2 *execvector, environment *execvector) int32 {
	const stackbytes uint32 = 4096
	if !MakeIntervalPrivatwritable(getcr3(), Përdoruesistacksipër-stackbytes, stackbytes) {
		return Enomem
	}
	stack := Përdoruesistacksipër
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		gjatësi := environment.lengths[i] + 1
		stack -= gjatësi
		destinacioni := GetbytesfromKursori(uintptr(stack), int(gjatësi), int(gjatësi))
		copy(destinacioni, environment.values[i][:gjatësi])
		environmentpointers[i] = stack
	}
	for i := int(argumente_2.count) - 1; i >= 0; i-- {
		gjatësi := argumente_2.lengths[i] + 1
		stack -= gjatësi
		destinacioni := GetbytesfromKursori(uintptr(stack), int(gjatësi), int(gjatësi))
		copy(destinacioni, argumente_2.values[i][:gjatësi])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushexecunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, environmentpointers[i])
	}
	pushexecunsignedinteger32(&stack, 0)
	for i := int(argumente_2.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, argumentpointers[i])
	}
	pushexecunsignedinteger32(&stack, argumente_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func mbyllonexec(proçes *proçesentry) {
	if proçes == nil {
		return
	}
	for pF := int32(0); pF < maxPF; pF++ {
		if proçes.fds[pF].përdorur && (proçes.fds[pF].pFFlamurka&pFcloexec) != 0 {
			mbyllProçesPF(proçes, pF)
		}
	}
}

func sysexecve(cpu *TcpuGjendje, pOZICIONIaddress uint32) int32 {
	if pOZICIONIaddress == 0 {
		return Efault
	}
	var argumente_2 execvector
	var environment execvector
	if result := kopjoexecvector(cpu.Ecx, &argumente_2); result < 0 {
		return result
	}
	if result := kopjoexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	emrilen, emri := kopjoPOZICIONI(pOZICIONIaddress)
	if emrilen == 0 {
		return Enoent
	}
	madhësia := kartelëMadhësia(emri[:emrilen])
	if madhësia == 0 {
		return Enoent
	}
	memoriaManazhuesi := &mem.TMemoriaManazhuesi{}
	kartelëKursori := memoriaManazhuesi.Malloc(madhësia)
	if kartelëKursori == nil {
		return Einval
	}
	data := GetbytesfromKursori(uintptr(kartelëKursori), int(madhësia), int(madhësia))
	leximiKartelë(emri[:emrilen], data)
	if madhësia < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memoriaManazhuesi.Elirë(kartelëKursori)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	memoriaManazhuesi.Elirë(kartelëKursori)
	if result := setupexecstack(cpu, &argumente_2, &environment); result < 0 {
		return result
	}
	mbyllonexec(ensureEtanishmeProçes())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuGjendje) int32 {
	prindpid := Etanishmepid()
	if ensureEtanishmeProçes() == nil {
		return Enfile
	}
	pid := allocateProçes(prindpid)
	if pid == 0 {
		return Einval
	}
	memoriaManazhuesi := &mem.TMemoriaManazhuesi{}
	threadKursori := memoriaManazhuesi.Malloc(uint32(Sizeof(TThread{})))
	stackKursori := memoriaManazhuesi.Malloc(ThreadstackMadhësia)
	birfaqeDosje := CloneaddressHapësiracow(getcr3())
	if threadKursori == nil || stackKursori == nil || birfaqeDosje == 0 {
		discardProçes(pid)
		return Einval
	}
	bir := (*TThread)(threadKursori)
	bir.Stack = uint32(uintptr(stackKursori))
	bir.CpuGjendje = (*TcpuGjendje)(Pointer(uintptr(stackKursori) + ThreadstackMadhësia - Sizeof(TcpuGjendje{})))
	*bir.CpuGjendje = *cpu
	bir.CpuGjendje.Eax = 0
	bir.Përdoruesistack_2 = cpu.Esp
	bir.PërdoruesistackMadhësia_2 = 0
	bir.Pid = pid
	bir.Prindpid = prindpid
	bir.FaqeDosjeentry = birfaqeDosje
	bir.ThreadGjendje = Gati
	bir.Fpuoffset = 0xffffffff
	bir.Iskernel = false
	Shtorunnablethread(bir)
	return int32(pid)
}

func sysDalja(gjendja uint32) {
	pid := Etanishmepid()
	for i := 0; i < len(proçesTabela); i++ {
		if proçesTabela[i].përdorur && proçesTabela[i].pid == pid {
			mbyllkrejtProçesfds(&proçesTabela[i])
			proçesTabela[i].exited = true
			proçesTabela[i].gjendja = (gjendja & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, gjendjaaddress uint32, mundësitë uint32) int32 {
	if (mundësitë & ^uint32(1)) != 0 {
		return Einval
	}
	prindpid := Etanishmepid()
	foundbir := false
	for i := 0; i < len(proçesTabela); i++ {
		p := &proçesTabela[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.përdorur && matches && p.prind == prindpid {
			foundbir = true
			if p.exited {
				if gjendjaaddress != 0 {
					*(*uint32)(Pointer(uintptr(gjendjaaddress))) = p.gjendja
				}
				birpid := p.pid
				*p = proçesentry{}
				return int32(birpid)
			}
		}
	}
	if !foundbir {
		return Echild
	}

	if (mundësitë & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProçes(prind uint32) uint32 {
	prindProçes := gjejProçes(prind)
	pid := Allocatepid()
	for i := 0; i < len(proçesTabela); i++ {
		if !proçesTabela[i].përdorur {
			proçesTabela[i] = proçesentry{
				përdorur:	true,
				pid:		pid,
				prind:		prind,
				programibreak:	përdoruesiheapbase,
			}
			if prindProçes != nil {
				proçesTabela[i].programibreak = prindProçes.programibreak
				for pF := 0; pF < maxPF; pF++ {
					if prindProçes.fds[pF].përdorur {
						proçesTabela[i].fds[pF] = prindProçes.fds[pF]
						përshkrimi := prindProçes.fds[pF].përshkrimi
						if përshkrimi >= 0 && përshkrimi < maxHapKartela {
							hapKartelëTabela[përshkrimi].refs++
						}
					}
				}
			} else {
				initializeProçesfds(&proçesTabela[i])
			}
			return pid
		}
	}
	return 0
}

func mbyllkrejtProçesfds(proçes *proçesentry) {
	if proçes == nil {
		return
	}
	for pF := int32(0); pF < maxPF; pF++ {
		if proçes.fds[pF].përdorur {
			mbyllProçesPF(proçes, pF)
		}
	}
}

func discardProçes(pid uint32) {
	proçes := gjejProçes(pid)
	if proçes == nil {
		return
	}
	mbyllkrejtProçesfds(proçes)
	*proçes = proçesentry{}
}

func kopjoPOZICIONI(pOZICIONIaddress uint32) (uint32, [12]byte) {
	var emri [12]byte
	if pOZICIONIaddress == 0 {
		return 0, emri
	}
	raw := GetbytesfromKursori(uintptr(pOZICIONIaddress), 64, 64)
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
		emri[n] = c
		n++
	}
	return n, emri
}

func kartelëMadhësia(emriifile []byte) uint32 {
	var ata0s = TTëmëtejshmetechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Leximipartition(&ata0s)

	bios := TBiosparameterblock32{}
	madhësia := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], emriifile)
	ata0s.Flush()
	return madhësia
}

func leximiKartelë(emriifile []byte, data []byte) {
	var ata0s = TTëmëtejshmetechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Leximipartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Leximi(&ata0s, partition.Mbr.Primarypartition[0], emriifile, data)
	ata0s.Flush()
}

func getcr3() uint32
