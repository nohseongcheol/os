/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemacall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "fileSistema/msdospartition"
import . "fileSistema/fat"
import . "fileSistema/formato_eseguibile_e_collegabile"
import mem "memoriamanager"
import . "paging"
import . "porta"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualeMemoria"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysEsci		uint32	= 1
	Sysfork		uint32	= 2
	SysLettura	uint32	= 3
	SysScrittura	uint32	= 4
	SysApri		uint32	= 5
	SysChiudi	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysaccesso	uint32	= 33
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
	SysrtEsci	uint32	= 252

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
	massimafd		= 32
	massimaApriFile		= 128
)

type fdvoce struct {
	usato		bool
	descrizione	int32
	fdFlag		uint32
}

type aprifileDescrizione struct {
	usato		bool
	refs		uint32
	tipo		uint32
	flag		uint32
	posizione	uint32
	dimensione	uint32
	nome		[12]byte
	nomelen		uint32
	aux		uint32
}

const (
	fdTipoNessuno		uint32	= 0
	fdTipofat		uint32	= 1
	fdTipostdin		uint32	= 2
	fdTipoconsole		uint32	= 3
	fdTipoRadiceCartella	uint32	= 4
	fdTiposocket		uint32	= 5

	oLetturaonly		uint32	= 0
	oScritturaonly		uint32	= 1
	oLetturaScrittura	uint32	= 2
	ocreate			uint32	= 0x40
	oTroncailvalore		uint32	= 0x200
	oappend			uint32	= 0x400
	oCartella		uint32	= 0x10000

	seekImposta	uint32	= 0
	seekCorrente	uint32	= 1
	seekFine	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fImpostafd	uint32	= 2
	fgetfl		uint32	= 3
	fImpostafl	uint32	= 4
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
	massimasockets			= 32
	massimasocketpacchetti		= 8
	massimadatagramDimensione	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Porta	uint16
	Address	uint32
	Zero	[8]byte
}

type socketPACCHETTO struct {
	usato		bool
	dimensione	uint32
	origine		socketaddressipv4
	data		[massimadatagramDimensione]byte
}

type localedatagramsocket struct {
	usato		bool
	bound		bool
	connected	bool
	locale		socketaddressipv4
	remoto		socketaddressipv4
	head		uint32
	tail		uint32
	conteggio	uint32
	pacchetti	[massimasocketpacchetti]socketPACCHETTO
}

type posixstat struct {
	Dispositivo	uint32
	Ino		uint32
	MODO		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Dimensione_2	int32
	Blksize		int32
	Blocco		int32
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
	Versione	[65]byte
	Machine		[65]byte
}

const (
	massimaEsecuzionevectorvoce	= 16
	massimaEsecuzioneStringaDurata	= 63
)

type esecuzionevector struct {
	conteggio	uint32
	lengths		[massimaEsecuzionevectorvoce]uint32
	valori		[massimaEsecuzionevectorvoce][massimaEsecuzioneStringaDurata + 1]byte
}

type processivoce struct {
	usato		bool
	pid		uint32
	genitore	uint32
	uscito		bool
	stato		uint32
	programmabreak	uint32
	fds		[massimafd]fdvoce
}

type stringaheader struct {
	Data	uintptr
	Len	int
}

func syscallErrore(errori int32) uint32 {
	return *(*uint32)(Pointer(&errori))
}

var aprifileTabella [massimaApriFile]aprifileDescrizione
var processiTabella [32]processivoce
var localesockets [massimasockets]localedatagramsocket
var successivoephemeralPorta uint16 = 49152

const (
	utenteheapbase		uint32	= 0x06000000
	utenteheapLimite	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLettura uint32
var stdinScrittura uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysEsci_2(indice uint32) {
	Syscall(SysEsci, indice)
}

func SysLettura_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLettura, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysStampastr(buffer string) {
	h := (*stringaheader)(Pointer(&buffer))
	Syscall(SysScrittura, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysStampaunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysScrittura, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysApri_2(pERCORSO uintptr, flag uint32, mODO uint32) int32 {
	return int32(Syscall(SysApri, uint32(pERCORSO), flag, mODO))
}

func SysChiudi_2(fd uint32) int32 {
	return int32(Syscall(SysChiudi, fd))
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
		return Interrupt(parametri[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupt(parametri[0], parametri[1], 0, 0, 0, 0)
	case 3:
		return Interrupt(parametri[0], parametri[1], parametri[2], 0, 0, 0)
	case 4:
		return Interrupt(parametri[0], parametri[1], parametri[2], parametri[3], 0, 0)
	case 5:
		return Interrupt(parametri[0], parametri[1], parametri[2], parametri[3], parametri[4], 0)
	case 6:
		return Interrupt(parametri[0], parametri[1], parametri[2], parametri[3], parametri[4], parametri[5])
	default:
		return syscallErrore(Enosys)
	}
}

func (séstesso *TSyscall) Init(manager *TInterruptmanager) {
	initfiledescriptor()

	interrupthandler = manigliainterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	séstesso.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func manigliainterrupt(esp uint32) uint32 {
	var cpu = (*TcpuStato)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysEsci:
		sysEsci(cpu.Ebx)
		return uint32(uintptr(Pointer(FermaCorrentethread(cpu))))
	case SysrtEsci:
		sysEsci(cpu.Ebx)
		return uint32(uintptr(Pointer(FermaCorrentethread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLettura:
		cpu.Eax = uint32(sysLettura(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysScrittura:
		cpu.Eax = uint32(sysScrittura(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysApri:
		cpu.Eax = uint32(sysApri(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysApri(cpu.Ebx, ocreate|oScritturaonly|oTroncailvalore, cpu.Ecx))
		return esp
	case SysChiudi:
		cpu.Eax = uint32(sysChiudi(int32(cpu.Ebx)))
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
		cpu.Eax = Correntepid()
		return esp
	case Sysgetppid:
		cpu.Eax = Correntegenitorepid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysaccesso:
		cpu.Eax = uint32(sysaccesso(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Stampa(cpu.Ebx)
		return esp

	default:
		console_2.MStampaxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Stampa(esp)
		console_2.MStampa(([]byte)(":"))
		console_2.MUnsignedinteger32Stampa(cpu.Eax)
		console_2.MStampa(([]byte)(":"))
		console_2.MUnsignedinteger32Stampa(cpu.Ebx)
		console_2.MStampa(([]byte)(":"))
		console_2.MUnsignedinteger32Stampa(cpu.Ecx)
		console_2.MStampa(([]byte)(":"))
		console_2.MUnsignedinteger32Stampa(cpu.Edx)
		console_2.MStampa(([]byte)("]"))
		cpu.Eax = syscallErrore(Enosys)
		return esp
	}

	return esp
}

func initfiledescriptor() {
	for i := 0; i < massimaApriFile; i++ {
		aprifileTabella[i] = aprifileDescrizione{}
	}
	for i := 0; i < len(processiTabella); i++ {
		processiTabella[i] = processivoce{}
	}
	for i := 0; i < len(localesockets); i++ {
		localesockets[i] = localedatagramsocket{}
	}
	successivoephemeralPorta = 49152
	aprifileTabella[0] = aprifileDescrizione{usato: true, tipo: fdTipostdin, flag: oLetturaonly}
	aprifileTabella[1] = aprifileDescrizione{usato: true, tipo: fdTipoconsole, flag: oScritturaonly}
	aprifileTabella[2] = aprifileDescrizione{usato: true, tipo: fdTipoconsole, flag: oScritturaonly}
}

func trovaProcessi(pid uint32) *processivoce {
	for i := 0; i < len(processiTabella); i++ {
		if processiTabella[i].usato && processiTabella[i].pid == pid {
			return &processiTabella[i]
		}
	}
	return nil
}

func initializeProcessifds(processi *processivoce) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		processi.fds[fd] = fdvoce{usato: true, descrizione: fd}
		aprifileTabella[fd].refs++
	}
}

func ensureCorrenteProcessi() *processivoce {
	pid := Correntepid()
	if processi := trovaProcessi(pid); processi != nil {
		return processi
	}
	for i := 0; i < len(processiTabella); i++ {
		if !processiTabella[i].usato {
			processiTabella[i] = processivoce{
				usato:		true,
				pid:		pid,
				genitore:	Correntegenitorepid(),
				programmabreak:	utenteheapbase,
			}
			initializeProcessifds(&processiTabella[i])
			return &processiTabella[i]
		}
	}
	return nil
}

func getAprifilefor(processi *processivoce, fd int32) *aprifileDescrizione {
	if processi == nil || fd < 0 || fd >= massimafd || !processi.fds[fd].usato {
		return nil
	}
	descrizione := processi.fds[fd].descrizione
	if descrizione < 0 || descrizione >= massimaApriFile || !aprifileTabella[descrizione].usato {
		return nil
	}
	return &aprifileTabella[descrizione]
}

func getAprifile(fd int32) *aprifileDescrizione {
	return getAprifilefor(ensureCorrenteProcessi(), fd)
}

func allocateAprifile() int32 {
	for i := int32(3); i < massimaApriFile; i++ {
		if !aprifileTabella[i].usato {
			aprifileTabella[i] = aprifileDescrizione{usato: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(processi *processivoce, descrizione int32, minimo int32) int32 {
	if processi == nil {
		return Enfile
	}
	if minimo < 0 || minimo >= massimafd {
		return Einval
	}
	for fd := minimo; fd < massimafd; fd++ {
		if !processi.fds[fd].usato {
			processi.fds[fd] = fdvoce{usato: true, descrizione: descrizione}
			return fd
		}
	}
	return Emfile
}

func releaseAprifile(descrizione int32) {
	if descrizione < 0 || descrizione >= massimaApriFile {
		return
	}
	voce := &aprifileTabella[descrizione]
	if voce.refs > 0 {
		voce.refs--
	}

	if voce.refs == 0 && descrizione > stderrfd {
		if voce.tipo == fdTiposocket && voce.aux < massimasockets {
			localesockets[voce.aux] = localedatagramsocket{}
		}
		*voce = aprifileDescrizione{}
	}
}

func chiudiProcessifd(processi *processivoce, fd int32) int32 {
	if processi == nil || getAprifilefor(processi, fd) == nil {
		return Ebadf
	}
	descrizione := processi.fds[fd].descrizione
	processi.fds[fd] = fdvoce{}
	releaseAprifile(descrizione)
	return 0
}

func sysScrittura(fd int32, address uint32, conteggio uint32) int32 {
	if conteggio == 0 {
		return 0
	}
	if address == 0 || address+conteggio < address {
		return Efault
	}
	if conteggio > 4096 {
		return Einval
	}
	voce := getAprifile(fd)
	if voce == nil {
		return Ebadf
	}
	if voce.tipo != fdTipoconsole {
		if voce.tipo == fdTiposocket {
			return socketSpediscito(fd, address, conteggio, 0, 0)
		}
		if voce.tipo == fdTipofat || voce.tipo == fdTipoRadiceCartella {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytefromPuntatore(uintptr(address), int(conteggio), int(conteggio))
	console_2.MStampa(buffer)
	return int32(conteggio)
}

func sysLettura(fd int32, address uint32, conteggio uint32) int32 {
	if conteggio == 0 {
		return 0
	}
	if address == 0 || address+conteggio < address {
		return Efault
	}
	voce := getAprifile(fd)
	if voce == nil {
		return Ebadf
	}
	if voce.tipo == fdTipostdin {
		return letturastdin(address, conteggio)
	}
	if voce.tipo == fdTipoRadiceCartella {
		return Eisdir
	}
	if voce.tipo == fdTiposocket {
		return socketreceivefrom(fd, address, conteggio, 0, 0)
	}
	if voce.tipo != fdTipofat {
		return Ebadf
	}
	if voce.posizione >= voce.dimensione {
		return 0
	}
	remaining := voce.dimensione - voce.posizione
	if conteggio > remaining {
		conteggio = remaining
	}
	buffer := GetBytefromPuntatore(uintptr(address), int(conteggio), int(conteggio))
	return letturavfsfile(voce, buffer, conteggio)
}

func sysApri(pERCORSOaddress uint32, flag uint32, mODO uint32) int32 {
	_ = mODO
	if pERCORSOaddress == 0 {
		return Efault
	}
	accessoMODO := flag & 3
	if accessoMODO == oScritturaonly || accessoMODO == oLetturaScrittura || (flag&(ocreate|oTroncailvalore|oappend)) != 0 {
		return Erofs
	}

	processi := ensureCorrenteProcessi()
	if processi == nil {
		return Enfile
	}
	descrizione := allocateAprifile()
	if descrizione < 0 {
		return descrizione
	}
	voce := &aprifileTabella[descrizione]
	voce.flag = flag
	if isRadicePERCORSO(pERCORSOaddress) {
		voce.tipo = fdTipoRadiceCartella
		voce.dimensione = 0
	} else {
		nomelen, nome := copiaPERCORSO(pERCORSOaddress)
		if nomelen == 0 {
			*voce = aprifileDescrizione{}
			return Enoent
		}
		dimensione := fileDimensione(nome[:nomelen])
		if dimensione == 0 {
			*voce = aprifileDescrizione{}
			return Enoent
		}
		if (flag & oCartella) != 0 {
			*voce = aprifileDescrizione{}
			return Enotdir
		}
		voce.tipo = fdTipofat
		voce.dimensione = dimensione
		voce.nomelen = nomelen
		voce.nome = nome
	}

	fd := allocatefd(processi, descrizione, 3)
	if fd < 0 {
		*voce = aprifileDescrizione{}
		return fd
	}
	return fd
}

func sysChiudi(fd int32) int32 {
	return chiudiProcessifd(ensureCorrenteProcessi(), fd)
}

func sysdup(fd int32, minimo int32) int32 {
	processi := ensureCorrenteProcessi()
	voce := getAprifilefor(processi, fd)
	if voce == nil {
		return Ebadf
	}
	nuovofd := allocatefd(processi, processi.fds[fd].descrizione, minimo)
	if nuovofd >= 0 {
		voce.refs++
	}
	return nuovofd
}

func sysdup2(oldfd int32, nuovofd int32) int32 {
	processi := ensureCorrenteProcessi()
	voce := getAprifilefor(processi, oldfd)
	if voce == nil {
		return Ebadf
	}
	if nuovofd < 0 || nuovofd >= massimafd {
		return Ebadf
	}
	if oldfd == nuovofd {
		return nuovofd
	}
	if processi.fds[nuovofd].usato {
		chiudiProcessifd(processi, nuovofd)
	}
	processi.fds[nuovofd] = fdvoce{usato: true, descrizione: processi.fds[oldfd].descrizione}
	voce.refs++
	return nuovofd
}

func sysfcntl(fd int32, comando uint32, argument uint32) int32 {
	processi := ensureCorrenteProcessi()
	voce := getAprifilefor(processi, fd)
	if voce == nil {
		return Ebadf
	}
	switch comando {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(processi.fds[fd].fdFlag)
	case fImpostafd:
		processi.fds[fd].fdFlag = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(voce.flag)
	case fImpostafl:
		voce.flag = (voce.flag & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	voce := getAprifile(fd)
	if voce == nil {
		return Ebadf
	}
	if voce.tipo != fdTipofat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekImposta:
		base = 0
	case seekCorrente:
		base = int64(voce.posizione)
	case seekFine:
		base = int64(voce.dimensione)
	default:
		return Einval
	}
	posizione_2 := base + int64(offset)
	if posizione_2 < 0 || posizione_2 > 0x7FFFFFFF {
		return Einval
	}
	voce.posizione = uint32(posizione_2)
	return int32(voce.posizione)
}

func letturavfsfile(voce *aprifileDescrizione, destinazione_2 []byte, conteggio uint32) int32 {
	memoriamanager := &mem.TMemoriamanager{}
	tmpPuntatore := memoriamanager.Alloca_memoria(voce.dimensione)
	if tmpPuntatore == nil {
		return Einval
	}
	tmp := GetBytefromPuntatore(uintptr(tmpPuntatore), int(voce.dimensione), int(voce.dimensione))
	letturafile(voce.nome[:voce.nomelen], tmp)
	copy(destinazione_2[:conteggio], tmp[voce.posizione:voce.posizione+conteggio])
	voce.posizione += conteggio
	memoriamanager.Libero(tmpPuntatore)
	return int32(conteggio)
}

func isRadicePERCORSO(pERCORSOaddress uint32) bool {
	if pERCORSOaddress == 0 {
		return false
	}
	pERCORSO := GetBytefromPuntatore(uintptr(pERCORSOaddress), 4, 4)
	if pERCORSO[0] == '/' && pERCORSO[1] == 0 {
		return true
	}
	if pERCORSO[0] == '.' && pERCORSO[1] == 0 {
		return true
	}
	if pERCORSO[0] == '/' && pERCORSO[1] == '.' && pERCORSO[2] == 0 {
		return true
	}
	return false
}

func sysaccesso(pERCORSOaddress uint32, mODO uint32) int32 {
	if pERCORSOaddress == 0 {
		return Efault
	}
	if (mODO & ^uint32(7)) != 0 {
		return Einval
	}
	isRadice := isRadicePERCORSO(pERCORSOaddress)
	exists := isRadice
	if !exists {
		nomelen, nome := copiaPERCORSO(pERCORSOaddress)
		exists = nomelen != 0 && fileDimensione(nome[:nomelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mODO & 2) != 0 {
		return Eacces
	}

	if (mODO&1) != 0 && !isRadice {
		return Eacces
	}
	return 0
}

func syschdir(pERCORSOaddress uint32) int32 {
	if pERCORSOaddress == 0 {
		return Efault
	}
	if !isRadicePERCORSO(pERCORSOaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, dimensione uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if dimensione < 2 {
		return Erange
	}
	buffer_2 := GetBytefromPuntatore(uintptr(bufferaddress), int(dimensione), int(dimensione))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mODO uint32, dimensione uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dispositivo = 1
	stat.Ino = inode
	stat.MODO = mODO
	stat.Nlink = 1
	stat.Dimensione_2 = int32(dimensione)
	stat.Blksize = 512
	stat.Blocco = int32((dimensione + 511) / 512)
	return 0
}

func sysstat(pERCORSOaddress uint32, stataddress uint32) int32 {
	if pERCORSOaddress == 0 {
		return Efault
	}
	if isRadicePERCORSO(pERCORSOaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nomelen, nome := copiaPERCORSO(pERCORSOaddress)
	if nomelen == 0 {
		return Enoent
	}
	dimensione := fileDimensione(nome[:nomelen])
	if dimensione == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nomelen; i++ {
		inode = inode*33 + uint32(nome[i])
	}
	return fillposixstat(stataddress, sifreg|0444, dimensione, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	voce := getAprifile(fd)
	if voce == nil {
		return Ebadf
	}
	switch voce.tipo {
	case fdTipostdin, fdTipoconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdTipoRadiceCartella:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdTipofat:
		return fillposixstat(stataddress, sifreg|0444, voce.dimensione, uint32(fd+2))
	case fdTiposocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getAprifile(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	processi := ensureCorrenteProcessi()
	if processi == nil {
		return 0
	}
	if processi.programmabreak == 0 {
		processi.programmabreak = utenteheapbase
	}
	if address_2 == 0 {
		return processi.programmabreak
	}
	if address_2 < utenteheapbase || address_2 > utenteheapLimite {
		return processi.programmabreak
	}
	processi.programmabreak = address_2
	return processi.programmabreak
}

func copiautscampo(destinazione *[65]byte, valore string) {
	limite := len(valore)
	if limite > 64 {
		limite = 64
	}
	for i := 0; i < limite; i++ {
		destinazione[i] = valore[i]
	}
	destinazione[limite] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nome := (*posixutsname)(Pointer(uintptr(address_2)))
	*nome = posixutsname{}
	copiautscampo(&nome.Sysname, "EngOS")
	copiautscampo(&nome.Nodename, "engos")
	copiautscampo(&nome.Release, "0.1-posix")
	copiautscampo(&nome.Versione, "POSIX.1-2017 phase 1")
	copiautscampo(&nome.Machine, "i386")
	return 0
}

func swapunsignedinteger16(valore uint16) uint16 {
	return (valore << 8) | (valore >> 8)
}

func socketcallargument(argomenti_2 uint32, indice uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argomenti_2 + indice*4)))
}

func socketforfd(fd int32) (*localedatagramsocket, int32) {
	voce := getAprifile(fd)
	if voce == nil || voce.tipo != fdTiposocket || voce.aux >= massimasockets {
		return nil, Ebadf
	}
	socket := &localesockets[voce.aux]
	if !socket.usato {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(dominio uint32, socketTipo uint32, protocol uint32) int32 {
	if dominio != afinet {
		return Eafnosupport
	}
	if socketTipo != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	processi := ensureCorrenteProcessi()
	if processi == nil {
		return Enfile
	}
	socketIndice := -1
	for i := 0; i < massimasockets; i++ {
		if !localesockets[i].usato {
			socketIndice = i
			break
		}
	}
	if socketIndice < 0 {
		return Enfile
	}
	descrizione := allocateAprifile()
	if descrizione < 0 {
		return descrizione
	}
	localesockets[socketIndice] = localedatagramsocket{usato: true}
	voce := &aprifileTabella[descrizione]
	voce.tipo = fdTiposocket
	voce.flag = oLetturaScrittura
	voce.aux = uint32(socketIndice)
	fd := allocatefd(processi, descrizione, 3)
	if fd < 0 {
		localesockets[socketIndice] = localedatagramsocket{}
		*voce = aprifileDescrizione{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, durata uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if durata < 16 {
		return nil, Einval
	}
	rISULTATO := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if rISULTATO.Family != afinet {
		return nil, Eafnosupport
	}
	return rISULTATO, 0
}

func portaIngressoUtilizza(porta uint16, except *localedatagramsocket) bool {
	for i := 0; i < massimasockets; i++ {
		socket := &localesockets[i]
		if socket != except && socket.usato && socket.bound && socket.locale.Porta == porta {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localedatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		porta := swapunsignedinteger16(successivoephemeralPorta)
		successivoephemeralPorta++
		if successivoephemeralPorta < 49152 {
			successivoephemeralPorta = 49152
		}
		if !portaIngressoUtilizza(porta, socket) {
			socket.locale = socketaddressipv4{Family: afinet, Porta: porta, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, durata uint32) int32 {
	socket, errori := socketforfd(fd)
	if errori != 0 {
		return errori
	}
	requested, errori := socketaddress(address_2, durata)
	if errori != 0 {
		return errori
	}
	if socket.bound {
		return Einval
	}
	if requested.Porta == 0 {
		return bindephemeral(socket)
	}
	if portaIngressoUtilizza(requested.Porta, socket) {
		return Eaddrinuse
	}
	socket.locale = *requested
	socket.bound = true
	return 0
}

func socketConnetti(fd int32, address_2 uint32, durata uint32) int32 {
	socket, errori := socketforfd(fd)
	if errori != 0 {
		return errori
	}
	remoto, errori := socketaddress(address_2, durata)
	if errori != 0 {
		return errori
	}
	if !socket.bound {
		if errori := bindephemeral(socket); errori != 0 {
			return errori
		}
	}
	socket.remoto = *remoto
	socket.connected = true
	return 0
}

func socketSpediscito(fd int32, bufferaddress_2 uint32, durata uint32, destinazioneaddress uint32, destinazioneDurata uint32) int32 {
	socket, errori := socketforfd(fd)
	if errori != 0 {
		return errori
	}
	if durata > massimadatagramDimensione {
		return Emsgsize
	}
	if durata != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destinazione socketaddressipv4
	if destinazioneaddress != 0 {
		address_2, addressErrore := socketaddress(destinazioneaddress, destinazioneDurata)
		if addressErrore != 0 {
			return addressErrore
		}
		destinazione = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destinazione = socket.remoto
	}
	if !socket.bound {
		if bindErrore := bindephemeral(socket); bindErrore != 0 {
			return bindErrore
		}
	}
	var receiver *localedatagramsocket
	for i := 0; i < massimasockets; i++ {
		candidate := &localesockets[i]
		if candidate.usato && candidate.bound && candidate.locale.Porta == destinazione.Porta &&
			(candidate.locale.Address == 0 || candidate.locale.Address == destinazione.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.conteggio >= massimasocketpacchetti {
		return Eagain
	}
	pACCHETTO := &receiver.pacchetti[receiver.tail]
	*pACCHETTO = socketPACCHETTO{usato: true, dimensione: durata, origine: socket.locale}
	if durata != 0 {
		origine := GetBytefromPuntatore(uintptr(bufferaddress_2), int(durata), int(durata))
		copy(pACCHETTO.data[:durata], origine)
	}
	receiver.tail = (receiver.tail + 1) % massimasocketpacchetti
	receiver.conteggio++
	return int32(durata)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, durata uint32, origineaddress uint32, origineDurataaddress uint32) int32 {
	socket, errori := socketforfd(fd)
	if errori != 0 {
		return errori
	}
	if durata != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.conteggio == 0 {
		return Eagain
	}
	pACCHETTO := &socket.pacchetti[socket.head]
	copiaDurata := pACCHETTO.dimensione
	if copiaDurata > durata {
		copiaDurata = durata
	}
	if copiaDurata != 0 {
		destinazione := GetBytefromPuntatore(uintptr(bufferaddress_2), int(copiaDurata), int(copiaDurata))
		copy(destinazione, pACCHETTO.data[:copiaDurata])
	}
	if origineaddress != 0 {
		if origineDurataaddress == 0 {
			return Efault
		}
		providedDurata := (*uint32)(Pointer(uintptr(origineDurataaddress)))
		if *providedDurata >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(origineaddress))) = pACCHETTO.origine
		}
		*providedDurata = 16
	}
	*pACCHETTO = socketPACCHETTO{}
	socket.head = (socket.head + 1) % massimasocketpacchetti
	socket.conteggio--
	return int32(copiaDurata)
}

func copiasocketNome(fd int32, address_2 uint32, durataaddress uint32, peer bool) int32 {
	socket, errori := socketforfd(fd)
	if errori != 0 {
		return errori
	}
	if address_2 == 0 || durataaddress == 0 {
		return Efault
	}
	durata := (*uint32)(Pointer(uintptr(durataaddress)))
	if *durata < 16 {
		*durata = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remoto
	} else {
		if !socket.bound {
			if bindErrore := bindephemeral(socket); bindErrore != 0 {
				return bindErrore
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.locale
	}
	*durata = 16
	return 0
}

func syssocketcall(call uint32, argomenti_2 uint32) int32 {
	if argomenti_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(argomenti_2, 0), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2))
	case 3:
		return socketConnetti(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copiasocketNome(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2), false)
	case 7:
		return copiasocketNome(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2), true)
	case 9:
		return socketSpediscito(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2), 0, 0)
	case 11:
		return socketSpediscito(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2), socketcallargument(argomenti_2, 4), socketcallargument(argomenti_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(argomenti_2, 0)), socketcallargument(argomenti_2, 1), socketcallargument(argomenti_2, 2), socketcallargument(argomenti_2, 4), socketcallargument(argomenti_2, 5))
	case 13:
		if _, errori := socketforfd(int32(socketcallargument(argomenti_2, 0))); errori != 0 {
			return errori
		}
		return 0
	case 14:
		if _, errori := socketforfd(int32(socketcallargument(argomenti_2, 0))); errori != 0 {
			return errori
		}
		return 0
	}
	return Eopnotsupp
}

func letturastdin(address uint32, conteggio uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBytefromPuntatore(uintptr(address), int(conteggio), int(conteggio))
	var n uint32
	for n < conteggio {
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
	successivo := (stdinScrittura + 1) % uint32(len(stdinbuffer))
	if successivo == stdinLettura {
		return
	}
	stdinbuffer[stdinScrittura] = c
	stdinScrittura = successivo
}

func stdingetblocking() byte {
	for stdinLettura == stdinScrittura {
		sc := pollTastierascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLettura]
	stdinLettura = (stdinLettura + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastierascancode() byte {
	for (PortaLetturabyte(0x64) & 0x01) == 0 {
	}
	sc := PortaLetturabyte(0x60)
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

func copiaEsecuzionevector(address_2 uint32, rISULTATO *esecuzionevector) int32 {
	*rISULTATO = esecuzionevector{}
	if address_2 == 0 {
		return 0
	}
	for indice := uint32(0); indice < massimaEsecuzionevectorvoce; indice++ {
		stringaaddress := *(*uint32)(Pointer(uintptr(address_2 + indice*4)))
		if stringaaddress == 0 {
			rISULTATO.conteggio = indice
			return 0
		}
		terminated := false
		for durata := uint32(0); durata <= massimaEsecuzioneStringaDurata; durata++ {
			valore := *(*byte)(Pointer(uintptr(stringaaddress + durata)))
			rISULTATO.valori[indice][durata] = valore
			if valore == 0 {
				rISULTATO.lengths[indice] = durata
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

func pushEsecuzioneunsignedinteger32(memoria_a_pila *uint32, valore uint32) {
	*memoria_a_pila -= 4
	*(*uint32)(Pointer(uintptr(*memoria_a_pila))) = valore
}

func setupEsecuzionestack(cpu *TcpuStato, argomenti_2 *esecuzionevector, environment *esecuzionevector) int32 {
	const stackByte uint32 = 4096
	if !MakeIntervalloPrivatowritable(getcr3(), UtentestackSopra-stackByte, stackByte) {
		return Enomem
	}
	memoria_a_pila := UtentestackSopra
	var argumentpointers [massimaEsecuzionevectorvoce]uint32
	var environmentpointers [massimaEsecuzionevectorvoce]uint32

	for i := int(environment.conteggio) - 1; i >= 0; i-- {
		durata := environment.lengths[i] + 1
		memoria_a_pila -= durata
		destinazione := GetBytefromPuntatore(uintptr(memoria_a_pila), int(durata), int(durata))
		copy(destinazione, environment.valori[i][:durata])
		environmentpointers[i] = memoria_a_pila
	}
	for i := int(argomenti_2.conteggio) - 1; i >= 0; i-- {
		durata := argomenti_2.lengths[i] + 1
		memoria_a_pila -= durata
		destinazione := GetBytefromPuntatore(uintptr(memoria_a_pila), int(durata), int(durata))
		copy(destinazione, argomenti_2.valori[i][:durata])
		argumentpointers[i] = memoria_a_pila
	}
	memoria_a_pila &= ^uint32(3)
	pushEsecuzioneunsignedinteger32(&memoria_a_pila, 0)
	for i := int(environment.conteggio) - 1; i >= 0; i-- {
		pushEsecuzioneunsignedinteger32(&memoria_a_pila, environmentpointers[i])
	}
	pushEsecuzioneunsignedinteger32(&memoria_a_pila, 0)
	for i := int(argomenti_2.conteggio) - 1; i >= 0; i-- {
		pushEsecuzioneunsignedinteger32(&memoria_a_pila, argumentpointers[i])
	}
	pushEsecuzioneunsignedinteger32(&memoria_a_pila, argomenti_2.conteggio)
	cpu.Esp = memoria_a_pila
	cpu.Ebp = 0
	return 0
}

func chiudiAccesoEsecuzione(processi *processivoce) {
	if processi == nil {
		return
	}
	for fd := int32(0); fd < massimafd; fd++ {
		if processi.fds[fd].usato && (processi.fds[fd].fdFlag&fdcloexec) != 0 {
			chiudiProcessifd(processi, fd)
		}
	}
}

func sysexecve(cpu *TcpuStato, pERCORSOaddress uint32) int32 {
	if pERCORSOaddress == 0 {
		return Efault
	}
	var argomenti_2 esecuzionevector
	var environment esecuzionevector
	if rISULTATO := copiaEsecuzionevector(cpu.Ecx, &argomenti_2); rISULTATO < 0 {
		return rISULTATO
	}
	if rISULTATO := copiaEsecuzionevector(cpu.Edx, &environment); rISULTATO < 0 {
		return rISULTATO
	}
	nomelen, nome := copiaPERCORSO(pERCORSOaddress)
	if nomelen == 0 {
		return Enoent
	}
	dimensione := fileDimensione(nome[:nomelen])
	if dimensione == 0 {
		return Enoent
	}
	memoriamanager := &mem.TMemoriamanager{}
	filePuntatore := memoriamanager.Alloca_memoria(dimensione)
	if filePuntatore == nil {
		return Einval
	}
	data := GetBytefromPuntatore(uintptr(filePuntatore), int(dimensione), int(dimensione))
	letturafile(nome[:nomelen], data)
	if dimensione < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memoriamanager.Libero(filePuntatore)
		return Enoexec
	}
	loader := Elf{}
	voce := loader.Getvoce(data)
	loader.Parse(data, getcr3())
	memoriamanager.Libero(filePuntatore)
	if rISULTATO := setupEsecuzionestack(cpu, &argomenti_2, &environment); rISULTATO < 0 {
		return rISULTATO
	}
	chiudiAccesoEsecuzione(ensureCorrenteProcessi())
	cpu.Eip = voce
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStato) int32 {
	genitorepid := Correntepid()
	if ensureCorrenteProcessi() == nil {
		return Enfile
	}
	pid := allocateProcessi(genitorepid)
	if pid == 0 {
		return Einval
	}
	memoriamanager := &mem.TMemoriamanager{}
	threadPuntatore := memoriamanager.Alloca_memoria(uint32(Sizeof(TThread{})))
	stackPuntatore := memoriamanager.Alloca_memoria(ThreadstackDimensione)
	figlioPAGINACartella := CloneaddressSpaziocow(getcr3())
	if threadPuntatore == nil || stackPuntatore == nil || figlioPAGINACartella == 0 {
		scartaProcessi(pid)
		return Einval
	}
	figlio := (*TThread)(threadPuntatore)
	figlio.Stack = uint32(uintptr(stackPuntatore))
	figlio.CpuStato = (*TcpuStato)(Pointer(uintptr(stackPuntatore) + ThreadstackDimensione - Sizeof(TcpuStato{})))
	*figlio.CpuStato = *cpu
	figlio.CpuStato.Eax = 0
	figlio.Utentestack_2 = cpu.Esp
	figlio.UtentestackDimensione_2 = 0
	figlio.Pid = pid
	figlio.Genitorepid = genitorepid
	figlio.PAGINACartellavoce = figlioPAGINACartella
	figlio.ThreadStato = Pronto
	figlio.Fpuoffset = 0xffffffff
	figlio.Iskernel = false
	Aggiungirunnablethread(figlio)
	return int32(pid)
}

func sysEsci(stato uint32) {
	pid := Correntepid()
	for i := 0; i < len(processiTabella); i++ {
		if processiTabella[i].usato && processiTabella[i].pid == pid {
			chiudiTuttoProcessifds(&processiTabella[i])
			processiTabella[i].uscito = true
			processiTabella[i].stato = (stato & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statoaddress uint32, opzioni uint32) int32 {
	if (opzioni & ^uint32(1)) != 0 {
		return Einval
	}
	genitorepid := Correntepid()
	foundfiglio := false
	for i := 0; i < len(processiTabella); i++ {
		p := &processiTabella[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.usato && matches && p.genitore == genitorepid {
			foundfiglio = true
			if p.uscito {
				if statoaddress != 0 {
					*(*uint32)(Pointer(uintptr(statoaddress))) = p.stato
				}
				figliopid := p.pid
				*p = processivoce{}
				return int32(figliopid)
			}
		}
	}
	if !foundfiglio {
		return Echild
	}

	if (opzioni & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProcessi(genitore uint32) uint32 {
	genitoreProcessi := trovaProcessi(genitore)
	pid := Allocatepid()
	for i := 0; i < len(processiTabella); i++ {
		if !processiTabella[i].usato {
			processiTabella[i] = processivoce{
				usato:		true,
				pid:		pid,
				genitore:	genitore,
				programmabreak:	utenteheapbase,
			}
			if genitoreProcessi != nil {
				processiTabella[i].programmabreak = genitoreProcessi.programmabreak
				for fd := 0; fd < massimafd; fd++ {
					if genitoreProcessi.fds[fd].usato {
						processiTabella[i].fds[fd] = genitoreProcessi.fds[fd]
						descrizione := genitoreProcessi.fds[fd].descrizione
						if descrizione >= 0 && descrizione < massimaApriFile {
							aprifileTabella[descrizione].refs++
						}
					}
				}
			} else {
				initializeProcessifds(&processiTabella[i])
			}
			return pid
		}
	}
	return 0
}

func chiudiTuttoProcessifds(processi *processivoce) {
	if processi == nil {
		return
	}
	for fd := int32(0); fd < massimafd; fd++ {
		if processi.fds[fd].usato {
			chiudiProcessifd(processi, fd)
		}
	}
}

func scartaProcessi(pid uint32) {
	processi := trovaProcessi(pid)
	if processi == nil {
		return
	}
	chiudiTuttoProcessifds(processi)
	*processi = processivoce{}
}

func copiaPERCORSO(pERCORSOaddress uint32) (uint32, [12]byte) {
	var nome [12]byte
	if pERCORSOaddress == 0 {
		return 0, nome
	}
	raw := GetBytefromPuntatore(uintptr(pERCORSOaddress), 64, 64)
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
		nome[n] = c
		n++
	}
	return n, nome
}

func fileDimensione(nomedelfile []byte) uint32 {
	var ata0s = TAvanzateTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabella{}
	partition.Letturapartition(&ata0s)

	bios := TParametri_del_file_system32{}
	dimensione := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomedelfile)
	ata0s.Flush()
	return dimensione
}

func letturafile(nomedelfile []byte, data []byte) {
	var ata0s = TAvanzateTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabella{}
	partition.Letturapartition(&ata0s)

	bios := TParametri_del_file_system32{}
	bios.Lettura(&ata0s, partition.Mbr.Primarypartition[0], nomedelfile, data)
	ata0s.Flush()
}

func getcr3() uint32
