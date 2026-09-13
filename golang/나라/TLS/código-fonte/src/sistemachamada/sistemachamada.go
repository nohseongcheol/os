package sistemachamada

import . "unsafe"

import . "interrupção"
import . "console"
import . "utilitário"
import . "múltiplogestãoTarefas"
import . "controlador/ata"
import . "ficheirosistema/msdospartição"
import . "ficheirosistema/fat"
import . "ficheirosistema/formato_executável_e_ligável"
import mem "memóriagestor"
import . "paginação"
import . "porto"
import . "gestãoTarefas/escalonador"
import . "gestãoTarefas/fluxoExecução"
import . "virtualmemória"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupçãohandler
}

const (
	SysSair		uint32	= 1
	Sysfork		uint32	= 2
	Sysler		uint32	= 3
	Sysescrever	uint32	= 4
	Sysabrir	uint32	= 5
	Sysfechar	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysacesso	uint32	= 33
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
	SysrtSair	uint32	= 252

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
	maxabrirFICHEIROS		= 128
)

type fdpontodeentrada struct {
	utilizado	bool
	descrição	int32
	fdParâmetros	uint32
}

type abrirficheiroDescrição struct {
	utilizado	bool
	refs		uint32
	tipo		uint32
	parâmetros	uint32
	posição		uint32
	tamanho		uint32
	nome		[12]byte
	nomelen		uint32
	aux		uint32
}

const (
	fdTipoNenhum		uint32	= 0
	fdTipofat		uint32	= 1
	fdTipostdin		uint32	= 2
	fdTipoconsole		uint32	= 3
	fdTipoRaizdiretório	uint32	= 4
	fdTipoconectorRede	uint32	= 5

	olersomente		uint32	= 0
	oescreversomente	uint32	= 1
	olerescrever		uint32	= 2
	ocriar			uint32	= 0x40
	oTruncar		uint32	= 0x200
	oappend			uint32	= 0x400
	odiretório		uint32	= 0x10000

	seekconjunto	uint32	= 0
	seekAtual	uint32	= 1
	seekFim		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fconjuntofd	uint32	= 2
	fgetfl		uint32	= 3
	fconjuntofl	uint32	= 4
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
	maxconectorRedepacotes	= 8
	maxdatagramTamanho	= 512
)

type conectorRedeEndereçoiVa4 struct {
	Family		uint16
	Porto		uint16
	Endereço	uint32
	Zero		[8]byte
}

type conectorRedepacket struct {
	utilizado	bool
	tamanho		uint32
	origem		conectorRedeEndereçoiVa4
	dados		[maxdatagramTamanho]byte
}

type localdatagramconectorRede struct {
	utilizado	bool
	bound		bool
	connected	bool
	local		conectorRedeEndereçoiVa4
	remotos		conectorRedeEndereçoiVa4
	head		uint32
	tail		uint32
	contar		uint32
	pacotes		[maxconectorRedepacotes]conectorRedepacket
}

type posixstat struct {
	Dispositivo	uint32
	Ino		uint32
	Modo		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Tamanho_2	int32
	Blksize		int32
	Bloco		int32
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
	Versão		[65]byte
	Machine		[65]byte
}

const (
	maxexecvectorpontodeentrada	= 16
	maxexeclinhaDuração		= 63
)

type execvector struct {
	contar	uint32
	lengths	[maxexecvectorpontodeentrada]uint32
	valores	[maxexecvectorpontodeentrada][maxexeclinhaDuração + 1]byte
}

type processopontodeentrada struct {
	utilizado	bool
	pid		uint32
	superior	uint32
	saiu		bool
	estado		uint32
	programabreak	uint32
	fds		[maxfd]fdpontodeentrada
}

type linhacabeçalho struct {
	Data	uintptr
	Len	int
}

func syscallErro(erro int32) uint32 {
	return *(*uint32)(Pointer(&erro))
}

var abrirficheiroTabela [maxabrirFICHEIROS]abrirficheiroDescrição
var processoTabela [32]processopontodeentrada
var localsockets [maxsockets]localdatagramconectorRede
var seguinteephemeralporto uint16 = 49152

const (
	utilizadorheapbase	uint32	= 0x06000000
	utilizadorheapLimite	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinler uint32
var stdinescrever uint32

func Interrupção(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysSair_2(índice uint32) {
	Syscall(SysSair, índice)
}

func Sysler_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysler, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysImprimirstr(buffer string) {
	h := (*linhacabeçalho)(Pointer(&buffer))
	Syscall(Sysescrever, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysImprimirunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysescrever, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysabrir_2(cAMINHO uintptr, parâmetros uint32, modo uint32) int32 {
	return int32(Syscall(Sysabrir, uint32(cAMINHO), parâmetros, modo))
}

func Sysfechar_2(fd uint32) int32 {
	return int32(Syscall(Sysfechar, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(endereço uint32) uint32 {
	return Syscall(Sysbrk, endereço)
}

func Syscall(parâmetros_2 ...uint32) uint32 {

	l := len(parâmetros_2)
	switch l {
	case 1:
		return Interrupção(parâmetros_2[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupção(parâmetros_2[0], parâmetros_2[1], 0, 0, 0, 0)
	case 3:
		return Interrupção(parâmetros_2[0], parâmetros_2[1], parâmetros_2[2], 0, 0, 0)
	case 4:
		return Interrupção(parâmetros_2[0], parâmetros_2[1], parâmetros_2[2], parâmetros_2[3], 0, 0)
	case 5:
		return Interrupção(parâmetros_2[0], parâmetros_2[1], parâmetros_2[2], parâmetros_2[3], parâmetros_2[4], 0)
	case 6:
		return Interrupção(parâmetros_2[0], parâmetros_2[1], parâmetros_2[2], parâmetros_2[3], parâmetros_2[4], parâmetros_2[5])
	default:
		return syscallErro(Enosys)
	}
}

func (próprio *TSyscall) Init(gestor *TInterrupçãogestor) {
	initficheirodescriptor()

	interrupçãohandler = manípulointerrupção

	var endereço uintptr
	endereço = uintptr(Pointer(&interrupçãohandler))

	próprio.TInterrupçãohandler.Init(0x80, uintptr(Pointer(gestor)), endereço)
}

var interrupçãohandler func(uint32) uint32

func manípulointerrupção(esp uint32) uint32 {
	var cpu = (*TcpuEstado)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysSair:
		sysSair(cpu.Ebx)
		return uint32(uintptr(Pointer(PararAtualfluxoExecução(cpu))))
	case SysrtSair:
		sysSair(cpu.Ebx)
		return uint32(uintptr(Pointer(PararAtualfluxoExecução(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysler:
		cpu.Eax = uint32(sysler(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysescrever:
		cpu.Eax = uint32(sysescrever(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysabrir:
		cpu.Eax = uint32(sysabrir(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysabrir(cpu.Ebx, ocriar|oescreversomente|oTruncar, cpu.Ecx))
		return esp
	case Sysfechar:
		cpu.Eax = uint32(sysfechar(int32(cpu.Ebx)))
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
		cpu.Eax = Atualpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Atualsuperiorpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysacesso:
		cpu.Eax = uint32(sysacesso(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysconectorRedechamada(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Imprimir(cpu.Ebx)
		return esp

	default:
		console_2.MImprimirxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Imprimir(esp)
		console_2.MImprimir(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimir(cpu.Eax)
		console_2.MImprimir(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimir(cpu.Ebx)
		console_2.MImprimir(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimir(cpu.Ecx)
		console_2.MImprimir(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimir(cpu.Edx)
		console_2.MImprimir(([]byte)("]"))
		cpu.Eax = syscallErro(Enosys)
		return esp
	}

	return esp
}

func initficheirodescriptor() {
	for i := 0; i < maxabrirFICHEIROS; i++ {
		abrirficheiroTabela[i] = abrirficheiroDescrição{}
	}
	for i := 0; i < len(processoTabela); i++ {
		processoTabela[i] = processopontodeentrada{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramconectorRede{}
	}
	seguinteephemeralporto = 49152
	abrirficheiroTabela[0] = abrirficheiroDescrição{utilizado: true, tipo: fdTipostdin, parâmetros: olersomente}
	abrirficheiroTabela[1] = abrirficheiroDescrição{utilizado: true, tipo: fdTipoconsole, parâmetros: oescreversomente}
	abrirficheiroTabela[2] = abrirficheiroDescrição{utilizado: true, tipo: fdTipoconsole, parâmetros: oescreversomente}
}

func procurarprocesso(pid uint32) *processopontodeentrada {
	for i := 0; i < len(processoTabela); i++ {
		if processoTabela[i].utilizado && processoTabela[i].pid == pid {
			return &processoTabela[i]
		}
	}
	return nil
}

func initializeprocessofds(processo *processopontodeentrada) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		processo.fds[fd] = fdpontodeentrada{utilizado: true, descrição: fd}
		abrirficheiroTabela[fd].refs++
	}
}

func ensureAtualprocesso() *processopontodeentrada {
	pid := Atualpid()
	if processo := procurarprocesso(pid); processo != nil {
		return processo
	}
	for i := 0; i < len(processoTabela); i++ {
		if !processoTabela[i].utilizado {
			processoTabela[i] = processopontodeentrada{
				utilizado:	true,
				pid:		pid,
				superior:	Atualsuperiorpid(),
				programabreak:	utilizadorheapbase,
			}
			initializeprocessofds(&processoTabela[i])
			return &processoTabela[i]
		}
	}
	return nil
}

func getabrirficheirofor(processo *processopontodeentrada, fd int32) *abrirficheiroDescrição {
	if processo == nil || fd < 0 || fd >= maxfd || !processo.fds[fd].utilizado {
		return nil
	}
	descrição := processo.fds[fd].descrição
	if descrição < 0 || descrição >= maxabrirFICHEIROS || !abrirficheiroTabela[descrição].utilizado {
		return nil
	}
	return &abrirficheiroTabela[descrição]
}

func getabrirficheiro(fd int32) *abrirficheiroDescrição {
	return getabrirficheirofor(ensureAtualprocesso(), fd)
}

func allocateabrirficheiro() int32 {
	for i := int32(3); i < maxabrirFICHEIROS; i++ {
		if !abrirficheiroTabela[i].utilizado {
			abrirficheiroTabela[i] = abrirficheiroDescrição{utilizado: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(processo *processopontodeentrada, descrição int32, mínimo int32) int32 {
	if processo == nil {
		return Enfile
	}
	if mínimo < 0 || mínimo >= maxfd {
		return Einval
	}
	for fd := mínimo; fd < maxfd; fd++ {
		if !processo.fds[fd].utilizado {
			processo.fds[fd] = fdpontodeentrada{utilizado: true, descrição: descrição}
			return fd
		}
	}
	return Emfile
}

func releaseabrirficheiro(descrição int32) {
	if descrição < 0 || descrição >= maxabrirFICHEIROS {
		return
	}
	pontodeentrada := &abrirficheiroTabela[descrição]
	if pontodeentrada.refs > 0 {
		pontodeentrada.refs--
	}

	if pontodeentrada.refs == 0 && descrição > stderrfd {
		if pontodeentrada.tipo == fdTipoconectorRede && pontodeentrada.aux < maxsockets {
			localsockets[pontodeentrada.aux] = localdatagramconectorRede{}
		}
		*pontodeentrada = abrirficheiroDescrição{}
	}
}

func fecharprocessofd(processo *processopontodeentrada, fd int32) int32 {
	if processo == nil || getabrirficheirofor(processo, fd) == nil {
		return Ebadf
	}
	descrição := processo.fds[fd].descrição
	processo.fds[fd] = fdpontodeentrada{}
	releaseabrirficheiro(descrição)
	return 0
}

func sysescrever(fd int32, endereço uint32, contar uint32) int32 {
	if contar == 0 {
		return 0
	}
	if endereço == 0 || endereço+contar < endereço {
		return Efault
	}
	if contar > 4096 {
		return Einval
	}
	pontodeentrada := getabrirficheiro(fd)
	if pontodeentrada == nil {
		return Ebadf
	}
	if pontodeentrada.tipo != fdTipoconsole {
		if pontodeentrada.tipo == fdTipoconectorRede {
			return conectorRedeEnviarpara(fd, endereço, contar, 0, 0)
		}
		if pontodeentrada.tipo == fdTipofat || pontodeentrada.tipo == fdTipoRaizdiretório {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbytesdePonteiro(uintptr(endereço), int(contar), int(contar))
	console_2.MImprimir(buffer)
	return int32(contar)
}

func sysler(fd int32, endereço uint32, contar uint32) int32 {
	if contar == 0 {
		return 0
	}
	if endereço == 0 || endereço+contar < endereço {
		return Efault
	}
	pontodeentrada := getabrirficheiro(fd)
	if pontodeentrada == nil {
		return Ebadf
	}
	if pontodeentrada.tipo == fdTipostdin {
		return lerstdin(endereço, contar)
	}
	if pontodeentrada.tipo == fdTipoRaizdiretório {
		return Eisdir
	}
	if pontodeentrada.tipo == fdTipoconectorRede {
		return conectorRedereceivede(fd, endereço, contar, 0, 0)
	}
	if pontodeentrada.tipo != fdTipofat {
		return Ebadf
	}
	if pontodeentrada.posição >= pontodeentrada.tamanho {
		return 0
	}
	remaining := pontodeentrada.tamanho - pontodeentrada.posição
	if contar > remaining {
		contar = remaining
	}
	buffer := GetbytesdePonteiro(uintptr(endereço), int(contar), int(contar))
	return lervfsficheiro(pontodeentrada, buffer, contar)
}

func sysabrir(cAMINHOEndereço uint32, parâmetros uint32, modo uint32) int32 {
	_ = modo
	if cAMINHOEndereço == 0 {
		return Efault
	}
	acessomodo := parâmetros & 3
	if acessomodo == oescreversomente || acessomodo == olerescrever || (parâmetros&(ocriar|oTruncar|oappend)) != 0 {
		return Erofs
	}

	processo := ensureAtualprocesso()
	if processo == nil {
		return Enfile
	}
	descrição := allocateabrirficheiro()
	if descrição < 0 {
		return descrição
	}
	pontodeentrada := &abrirficheiroTabela[descrição]
	pontodeentrada.parâmetros = parâmetros
	if isRaizCAMINHO(cAMINHOEndereço) {
		pontodeentrada.tipo = fdTipoRaizdiretório
		pontodeentrada.tamanho = 0
	} else {
		nomelen, nome := copiarCAMINHO(cAMINHOEndereço)
		if nomelen == 0 {
			*pontodeentrada = abrirficheiroDescrição{}
			return Enoent
		}
		tamanho := ficheiroTamanho(nome[:nomelen])
		if tamanho == 0 {
			*pontodeentrada = abrirficheiroDescrição{}
			return Enoent
		}
		if (parâmetros & odiretório) != 0 {
			*pontodeentrada = abrirficheiroDescrição{}
			return Enotdir
		}
		pontodeentrada.tipo = fdTipofat
		pontodeentrada.tamanho = tamanho
		pontodeentrada.nomelen = nomelen
		pontodeentrada.nome = nome
	}

	fd := allocatefd(processo, descrição, 3)
	if fd < 0 {
		*pontodeentrada = abrirficheiroDescrição{}
		return fd
	}
	return fd
}

func sysfechar(fd int32) int32 {
	return fecharprocessofd(ensureAtualprocesso(), fd)
}

func sysdup(fd int32, mínimo int32) int32 {
	processo := ensureAtualprocesso()
	pontodeentrada := getabrirficheirofor(processo, fd)
	if pontodeentrada == nil {
		return Ebadf
	}
	novofd := allocatefd(processo, processo.fds[fd].descrição, mínimo)
	if novofd >= 0 {
		pontodeentrada.refs++
	}
	return novofd
}

func sysdup2(oldfd int32, novofd int32) int32 {
	processo := ensureAtualprocesso()
	pontodeentrada := getabrirficheirofor(processo, oldfd)
	if pontodeentrada == nil {
		return Ebadf
	}
	if novofd < 0 || novofd >= maxfd {
		return Ebadf
	}
	if oldfd == novofd {
		return novofd
	}
	if processo.fds[novofd].utilizado {
		fecharprocessofd(processo, novofd)
	}
	processo.fds[novofd] = fdpontodeentrada{utilizado: true, descrição: processo.fds[oldfd].descrição}
	pontodeentrada.refs++
	return novofd
}

func sysfcntl(fd int32, comando uint32, argument uint32) int32 {
	processo := ensureAtualprocesso()
	pontodeentrada := getabrirficheirofor(processo, fd)
	if pontodeentrada == nil {
		return Ebadf
	}
	switch comando {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(processo.fds[fd].fdParâmetros)
	case fconjuntofd:
		processo.fds[fd].fdParâmetros = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(pontodeentrada.parâmetros)
	case fconjuntofl:
		pontodeentrada.parâmetros = (pontodeentrada.parâmetros & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, deslocamento int32, whence uint32) int32 {
	pontodeentrada := getabrirficheiro(fd)
	if pontodeentrada == nil {
		return Ebadf
	}
	if pontodeentrada.tipo != fdTipofat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekconjunto:
		base = 0
	case seekAtual:
		base = int64(pontodeentrada.posição)
	case seekFim:
		base = int64(pontodeentrada.tamanho)
	default:
		return Einval
	}
	posição_2 := base + int64(deslocamento)
	if posição_2 < 0 || posição_2 > 0x7FFFFFFF {
		return Einval
	}
	pontodeentrada.posição = uint32(posição_2)
	return int32(pontodeentrada.posição)
}

func lervfsficheiro(pontodeentrada *abrirficheiroDescrição, destino_2 []byte, contar uint32) int32 {
	memóriagestor := &mem.TMemóriagestor{}
	tmpPonteiro := memóriagestor.Alocar_memória(pontodeentrada.tamanho)
	if tmpPonteiro == nil {
		return Einval
	}
	tmp := GetbytesdePonteiro(uintptr(tmpPonteiro), int(pontodeentrada.tamanho), int(pontodeentrada.tamanho))
	lerficheiro(pontodeentrada.nome[:pontodeentrada.nomelen], tmp)
	copy(destino_2[:contar], tmp[pontodeentrada.posição:pontodeentrada.posição+contar])
	pontodeentrada.posição += contar
	memóriagestor.Livre(tmpPonteiro)
	return int32(contar)
}

func isRaizCAMINHO(cAMINHOEndereço uint32) bool {
	if cAMINHOEndereço == 0 {
		return false
	}
	cAMINHO := GetbytesdePonteiro(uintptr(cAMINHOEndereço), 4, 4)
	if cAMINHO[0] == '/' && cAMINHO[1] == 0 {
		return true
	}
	if cAMINHO[0] == '.' && cAMINHO[1] == 0 {
		return true
	}
	if cAMINHO[0] == '/' && cAMINHO[1] == '.' && cAMINHO[2] == 0 {
		return true
	}
	return false
}

func sysacesso(cAMINHOEndereço uint32, modo uint32) int32 {
	if cAMINHOEndereço == 0 {
		return Efault
	}
	if (modo & ^uint32(7)) != 0 {
		return Einval
	}
	isRaiz := isRaizCAMINHO(cAMINHOEndereço)
	exists := isRaiz
	if !exists {
		nomelen, nome := copiarCAMINHO(cAMINHOEndereço)
		exists = nomelen != 0 && ficheiroTamanho(nome[:nomelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (modo & 2) != 0 {
		return Eacces
	}

	if (modo&1) != 0 && !isRaiz {
		return Eacces
	}
	return 0
}

func syschdir(cAMINHOEndereço uint32) int32 {
	if cAMINHOEndereço == 0 {
		return Efault
	}
	if !isRaizCAMINHO(cAMINHOEndereço) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferEndereço uint32, tamanho uint32) int32 {
	if bufferEndereço == 0 {
		return Efault
	}
	if tamanho < 2 {
		return Erange
	}
	buffer_2 := GetbytesdePonteiro(uintptr(bufferEndereço), int(tamanho), int(tamanho))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statEndereço uint32, modo uint32, tamanho uint32, inode uint32) int32 {
	if statEndereço == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statEndereço)))
	*stat = posixstat{}
	stat.Dispositivo = 1
	stat.Ino = inode
	stat.Modo = modo
	stat.Nlink = 1
	stat.Tamanho_2 = int32(tamanho)
	stat.Blksize = 512
	stat.Bloco = int32((tamanho + 511) / 512)
	return 0
}

func sysstat(cAMINHOEndereço uint32, statEndereço uint32) int32 {
	if cAMINHOEndereço == 0 {
		return Efault
	}
	if isRaizCAMINHO(cAMINHOEndereço) {
		return fillposixstat(statEndereço, sifdir|0555, 0, 1)
	}
	nomelen, nome := copiarCAMINHO(cAMINHOEndereço)
	if nomelen == 0 {
		return Enoent
	}
	tamanho := ficheiroTamanho(nome[:nomelen])
	if tamanho == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nomelen; i++ {
		inode = inode*33 + uint32(nome[i])
	}
	return fillposixstat(statEndereço, sifreg|0444, tamanho, inode)
}

func sysfstat(fd int32, statEndereço uint32) int32 {
	pontodeentrada := getabrirficheiro(fd)
	if pontodeentrada == nil {
		return Ebadf
	}
	switch pontodeentrada.tipo {
	case fdTipostdin, fdTipoconsole:
		return fillposixstat(statEndereço, sifchr|0666, 0, uint32(fd+1))
	case fdTipoRaizdiretório:
		return fillposixstat(statEndereço, sifdir|0555, 0, 1)
	case fdTipofat:
		return fillposixstat(statEndereço, sifreg|0444, pontodeentrada.tamanho, uint32(fd+2))
	case fdTipoconectorRede:
		return fillposixstat(statEndereço, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getabrirficheiro(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(endereço_2 uint32) uint32 {
	processo := ensureAtualprocesso()
	if processo == nil {
		return 0
	}
	if processo.programabreak == 0 {
		processo.programabreak = utilizadorheapbase
	}
	if endereço_2 == 0 {
		return processo.programabreak
	}
	if endereço_2 < utilizadorheapbase || endereço_2 > utilizadorheapLimite {
		return processo.programabreak
	}
	processo.programabreak = endereço_2
	return processo.programabreak
}

func copiarutscampo(destino *[65]byte, valor string) {
	limite := len(valor)
	if limite > 64 {
		limite = 64
	}
	for i := 0; i < limite; i++ {
		destino[i] = valor[i]
	}
	destino[limite] = 0
}

func sysuname(endereço_2 uint32) int32 {
	if endereço_2 == 0 {
		return Efault
	}
	nome := (*posixutsname)(Pointer(uintptr(endereço_2)))
	*nome = posixutsname{}
	copiarutscampo(&nome.Sysname, "EngOS")
	copiarutscampo(&nome.Nodename, "engos")
	copiarutscampo(&nome.Release, "0.1-posix")
	copiarutscampo(&nome.Versão, "POSIX.1-2017 phase 1")
	copiarutscampo(&nome.Machine, "i386")
	return 0
}

func swapunsignedinteger16(valor uint16) uint16 {
	return (valor << 8) | (valor >> 8)
}

func conectorRedechamadaargument(argumentos_2 uint32, índice uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumentos_2 + índice*4)))
}

func conectorRedeforfd(fd int32) (*localdatagramconectorRede, int32) {
	pontodeentrada := getabrirficheiro(fd)
	if pontodeentrada == nil || pontodeentrada.tipo != fdTipoconectorRede || pontodeentrada.aux >= maxsockets {
		return nil, Ebadf
	}
	conectorRede := &localsockets[pontodeentrada.aux]
	if !conectorRede.utilizado {
		return nil, Ebadf
	}
	return conectorRede, 0
}

func allocateconectorRede(domínio uint32, conectorRedetipo uint32, protocol uint32) int32 {
	if domínio != afinet {
		return Eafnosupport
	}
	if conectorRedetipo != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	processo := ensureAtualprocesso()
	if processo == nil {
		return Enfile
	}
	conectorRedeÍndice := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].utilizado {
			conectorRedeÍndice = i
			break
		}
	}
	if conectorRedeÍndice < 0 {
		return Enfile
	}
	descrição := allocateabrirficheiro()
	if descrição < 0 {
		return descrição
	}
	localsockets[conectorRedeÍndice] = localdatagramconectorRede{utilizado: true}
	pontodeentrada := &abrirficheiroTabela[descrição]
	pontodeentrada.tipo = fdTipoconectorRede
	pontodeentrada.parâmetros = olerescrever
	pontodeentrada.aux = uint32(conectorRedeÍndice)
	fd := allocatefd(processo, descrição, 3)
	if fd < 0 {
		localsockets[conectorRedeÍndice] = localdatagramconectorRede{}
		*pontodeentrada = abrirficheiroDescrição{}
		return fd
	}
	return fd
}

func conectorRedeEndereço(endereço_2 uint32, duração uint32) (*conectorRedeEndereçoiVa4, int32) {
	if endereço_2 == 0 {
		return nil, Efault
	}
	if duração < 16 {
		return nil, Einval
	}
	destino_3 := (*conectorRedeEndereçoiVa4)(Pointer(uintptr(endereço_2)))
	if destino_3.Family != afinet {
		return nil, Eafnosupport
	}
	return destino_3, 0
}

func portoEntradaUtilizar(porto uint16, except *localdatagramconectorRede) bool {
	for i := 0; i < maxsockets; i++ {
		conectorRede := &localsockets[i]
		if conectorRede != except && conectorRede.utilizado && conectorRede.bound && conectorRede.local.Porto == porto {
			return true
		}
	}
	return false
}

func vincularephemeral(conectorRede *localdatagramconectorRede) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		porto := swapunsignedinteger16(seguinteephemeralporto)
		seguinteephemeralporto++
		if seguinteephemeralporto < 49152 {
			seguinteephemeralporto = 49152
		}
		if !portoEntradaUtilizar(porto, conectorRede) {
			conectorRede.local = conectorRedeEndereçoiVa4{Family: afinet, Porto: porto, Endereço: 0x0100007F}
			conectorRede.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func conectorRedeVincular(fd int32, endereço_2 uint32, duração uint32) int32 {
	conectorRede, erro := conectorRedeforfd(fd)
	if erro != 0 {
		return erro
	}
	requested, erro := conectorRedeEndereço(endereço_2, duração)
	if erro != 0 {
		return erro
	}
	if conectorRede.bound {
		return Einval
	}
	if requested.Porto == 0 {
		return vincularephemeral(conectorRede)
	}
	if portoEntradaUtilizar(requested.Porto, conectorRede) {
		return Eaddrinuse
	}
	conectorRede.local = *requested
	conectorRede.bound = true
	return 0
}

func conectorRedeLigar(fd int32, endereço_2 uint32, duração uint32) int32 {
	conectorRede, erro := conectorRedeforfd(fd)
	if erro != 0 {
		return erro
	}
	remotos, erro := conectorRedeEndereço(endereço_2, duração)
	if erro != 0 {
		return erro
	}
	if !conectorRede.bound {
		if erro := vincularephemeral(conectorRede); erro != 0 {
			return erro
		}
	}
	conectorRede.remotos = *remotos
	conectorRede.connected = true
	return 0
}

func conectorRedeEnviarpara(fd int32, bufferEndereço_2 uint32, duração uint32, destinoEndereço uint32, destinoDuração uint32) int32 {
	conectorRede, erro := conectorRedeforfd(fd)
	if erro != 0 {
		return erro
	}
	if duração > maxdatagramTamanho {
		return Emsgsize
	}
	if duração != 0 && bufferEndereço_2 == 0 {
		return Efault
	}
	var destino conectorRedeEndereçoiVa4
	if destinoEndereço != 0 {
		endereço_2, endereçoErro := conectorRedeEndereço(destinoEndereço, destinoDuração)
		if endereçoErro != 0 {
			return endereçoErro
		}
		destino = *endereço_2
	} else {
		if !conectorRede.connected {
			return Enotconn
		}
		destino = conectorRede.remotos
	}
	if !conectorRede.bound {
		if vincularErro := vincularephemeral(conectorRede); vincularErro != 0 {
			return vincularErro
		}
	}
	var receiver *localdatagramconectorRede
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.utilizado && candidate.bound && candidate.local.Porto == destino.Porto &&
			(candidate.local.Endereço == 0 || candidate.local.Endereço == destino.Endereço) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.contar >= maxconectorRedepacotes {
		return Eagain
	}
	packet := &receiver.pacotes[receiver.tail]
	*packet = conectorRedepacket{utilizado: true, tamanho: duração, origem: conectorRede.local}
	if duração != 0 {
		origem := GetbytesdePonteiro(uintptr(bufferEndereço_2), int(duração), int(duração))
		copy(packet.dados[:duração], origem)
	}
	receiver.tail = (receiver.tail + 1) % maxconectorRedepacotes
	receiver.contar++
	return int32(duração)
}

func conectorRedereceivede(fd int32, bufferEndereço_2 uint32, duração uint32, origemEndereço uint32, origemDuraçãoEndereço uint32) int32 {
	conectorRede, erro := conectorRedeforfd(fd)
	if erro != 0 {
		return erro
	}
	if duração != 0 && bufferEndereço_2 == 0 {
		return Efault
	}
	if conectorRede.contar == 0 {
		return Eagain
	}
	packet := &conectorRede.pacotes[conectorRede.head]
	copiarDuração := packet.tamanho
	if copiarDuração > duração {
		copiarDuração = duração
	}
	if copiarDuração != 0 {
		destino := GetbytesdePonteiro(uintptr(bufferEndereço_2), int(copiarDuração), int(copiarDuração))
		copy(destino, packet.dados[:copiarDuração])
	}
	if origemEndereço != 0 {
		if origemDuraçãoEndereço == 0 {
			return Efault
		}
		providedDuração := (*uint32)(Pointer(uintptr(origemDuraçãoEndereço)))
		if *providedDuração >= 16 {
			*(*conectorRedeEndereçoiVa4)(Pointer(uintptr(origemEndereço))) = packet.origem
		}
		*providedDuração = 16
	}
	*packet = conectorRedepacket{}
	conectorRede.head = (conectorRede.head + 1) % maxconectorRedepacotes
	conectorRede.contar--
	return int32(copiarDuração)
}

func copiarconectorRedeNome(fd int32, endereço_2 uint32, duraçãoEndereço uint32, peer bool) int32 {
	conectorRede, erro := conectorRedeforfd(fd)
	if erro != 0 {
		return erro
	}
	if endereço_2 == 0 || duraçãoEndereço == 0 {
		return Efault
	}
	duração := (*uint32)(Pointer(uintptr(duraçãoEndereço)))
	if *duração < 16 {
		*duração = 16
		return Einval
	}
	if peer {
		if !conectorRede.connected {
			return Enotconn
		}
		*(*conectorRedeEndereçoiVa4)(Pointer(uintptr(endereço_2))) = conectorRede.remotos
	} else {
		if !conectorRede.bound {
			if vincularErro := vincularephemeral(conectorRede); vincularErro != 0 {
				return vincularErro
			}
		}
		*(*conectorRedeEndereçoiVa4)(Pointer(uintptr(endereço_2))) = conectorRede.local
	}
	*duração = 16
	return 0
}

func sysconectorRedechamada(chamada uint32, argumentos_2 uint32) int32 {
	if argumentos_2 == 0 {
		return Efault
	}
	switch chamada {
	case 1:
		return allocateconectorRede(conectorRedechamadaargument(argumentos_2, 0), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2))
	case 2:
		return conectorRedeVincular(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2))
	case 3:
		return conectorRedeLigar(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copiarconectorRedeNome(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2), false)
	case 7:
		return copiarconectorRedeNome(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2), true)
	case 9:
		return conectorRedeEnviarpara(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2), 0, 0)
	case 10:
		return conectorRedereceivede(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2), 0, 0)
	case 11:
		return conectorRedeEnviarpara(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2), conectorRedechamadaargument(argumentos_2, 4), conectorRedechamadaargument(argumentos_2, 5))
	case 12:
		return conectorRedereceivede(int32(conectorRedechamadaargument(argumentos_2, 0)), conectorRedechamadaargument(argumentos_2, 1), conectorRedechamadaargument(argumentos_2, 2), conectorRedechamadaargument(argumentos_2, 4), conectorRedechamadaargument(argumentos_2, 5))
	case 13:
		if _, erro := conectorRedeforfd(int32(conectorRedechamadaargument(argumentos_2, 0))); erro != 0 {
			return erro
		}
		return 0
	case 14:
		if _, erro := conectorRedeforfd(int32(conectorRedechamadaargument(argumentos_2, 0))); erro != 0 {
			return erro
		}
		return 0
	}
	return Eopnotsupp
}

func lerstdin(endereço uint32, contar uint32) int32 {
	if endereço == 0 {
		return Einval
	}
	buffer := GetbytesdePonteiro(uintptr(endereço), int(contar), int(contar))
	var n uint32
	for n < contar {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputocteto(c byte) {
	seguinte := (stdinescrever + 1) % uint32(len(stdinbuffer))
	if seguinte == stdinler {
		return
	}
	stdinbuffer[stdinescrever] = c
	stdinescrever = seguinte
}

func stdingetblocking() byte {
	for stdinler == stdinescrever {
		sc := polltecladoscancode()
		if sc != 0 {
			Stdinputocteto(sc)
		}
	}
	c := stdinbuffer[stdinler]
	stdinler = (stdinler + 1) % uint32(len(stdinbuffer))
	return c
}

func polltecladoscancode() byte {
	for (Portolerocteto(0x64) & 0x01) == 0 {
	}
	sc := Portolerocteto(0x60)
	return scancodeparaocteto(sc)
}

func scancodeparaocteto(sc uint8) byte {
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

func copiarexecvector(endereço_2 uint32, destino_3 *execvector) int32 {
	*destino_3 = execvector{}
	if endereço_2 == 0 {
		return 0
	}
	for índice := uint32(0); índice < maxexecvectorpontodeentrada; índice++ {
		linhaEndereço := *(*uint32)(Pointer(uintptr(endereço_2 + índice*4)))
		if linhaEndereço == 0 {
			destino_3.contar = índice
			return 0
		}
		terminated := false
		for duração := uint32(0); duração <= maxexeclinhaDuração; duração++ {
			valor := *(*byte)(Pointer(uintptr(linhaEndereço + duração)))
			destino_3.valores[índice][duração] = valor
			if valor == 0 {
				destino_3.lengths[índice] = duração
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

func pushexecunsignedinteger32(memória_de_pilha *uint32, valor uint32) {
	*memória_de_pilha -= 4
	*(*uint32)(Pointer(uintptr(*memória_de_pilha))) = valor
}

func setupexecstack(cpu *TcpuEstado, argumentos_2 *execvector, environment *execvector) int32 {
	const stackbytes uint32 = 4096
	if !MakeIntervaloPrivadowritable(getcr3(), UtilizadorstackSuperior-stackbytes, stackbytes) {
		return Enomem
	}
	memória_de_pilha := UtilizadorstackSuperior
	var argumentpointers [maxexecvectorpontodeentrada]uint32
	var environmentpointers [maxexecvectorpontodeentrada]uint32

	for i := int(environment.contar) - 1; i >= 0; i-- {
		duração := environment.lengths[i] + 1
		memória_de_pilha -= duração
		destino := GetbytesdePonteiro(uintptr(memória_de_pilha), int(duração), int(duração))
		copy(destino, environment.valores[i][:duração])
		environmentpointers[i] = memória_de_pilha
	}
	for i := int(argumentos_2.contar) - 1; i >= 0; i-- {
		duração := argumentos_2.lengths[i] + 1
		memória_de_pilha -= duração
		destino := GetbytesdePonteiro(uintptr(memória_de_pilha), int(duração), int(duração))
		copy(destino, argumentos_2.valores[i][:duração])
		argumentpointers[i] = memória_de_pilha
	}
	memória_de_pilha &= ^uint32(3)
	pushexecunsignedinteger32(&memória_de_pilha, 0)
	for i := int(environment.contar) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&memória_de_pilha, environmentpointers[i])
	}
	pushexecunsignedinteger32(&memória_de_pilha, 0)
	for i := int(argumentos_2.contar) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&memória_de_pilha, argumentpointers[i])
	}
	pushexecunsignedinteger32(&memória_de_pilha, argumentos_2.contar)
	cpu.Esp = memória_de_pilha
	cpu.Ebp = 0
	return 0
}

func fecharaoexec(processo *processopontodeentrada) {
	if processo == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if processo.fds[fd].utilizado && (processo.fds[fd].fdParâmetros&fdcloexec) != 0 {
			fecharprocessofd(processo, fd)
		}
	}
}

func sysexecve(cpu *TcpuEstado, cAMINHOEndereço uint32) int32 {
	if cAMINHOEndereço == 0 {
		return Efault
	}
	var argumentos_2 execvector
	var environment execvector
	if destino_3 := copiarexecvector(cpu.Ecx, &argumentos_2); destino_3 < 0 {
		return destino_3
	}
	if destino_3 := copiarexecvector(cpu.Edx, &environment); destino_3 < 0 {
		return destino_3
	}
	nomelen, nome := copiarCAMINHO(cAMINHOEndereço)
	if nomelen == 0 {
		return Enoent
	}
	tamanho := ficheiroTamanho(nome[:nomelen])
	if tamanho == 0 {
		return Enoent
	}
	memóriagestor := &mem.TMemóriagestor{}
	ficheiroPonteiro := memóriagestor.Alocar_memória(tamanho)
	if ficheiroPonteiro == nil {
		return Einval
	}
	dados := GetbytesdePonteiro(uintptr(ficheiroPonteiro), int(tamanho), int(tamanho))
	lerficheiro(nome[:nomelen], dados)
	if tamanho < 52 || dados[0] != 0x7F || dados[1] != 'E' || dados[2] != 'L' || dados[3] != 'F' {
		memóriagestor.Livre(ficheiroPonteiro)
		return Enoexec
	}
	loader := Elf{}
	pontodeentrada := loader.Getpontodeentrada(dados)
	loader.Parse(dados, getcr3())
	memóriagestor.Livre(ficheiroPonteiro)
	if destino_3 := setupexecstack(cpu, &argumentos_2, &environment); destino_3 < 0 {
		return destino_3
	}
	fecharaoexec(ensureAtualprocesso())
	cpu.Eip = pontodeentrada
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuEstado) int32 {
	superiorpid := Atualpid()
	if ensureAtualprocesso() == nil {
		return Enfile
	}
	pid := allocateprocesso(superiorpid)
	if pid == 0 {
		return Einval
	}
	memóriagestor := &mem.TMemóriagestor{}
	fluxoExecuçãoPonteiro := memóriagestor.Alocar_memória(uint32(Sizeof(TFluxoExecução{})))
	stackPonteiro := memóriagestor.Alocar_memória(FluxoExecuçãostackTamanho)
	dependentepáginadiretório := CloneEndereçoEspaçocow(getcr3())
	if fluxoExecuçãoPonteiro == nil || stackPonteiro == nil || dependentepáginadiretório == 0 {
		apagarprocesso(pid)
		return Einval
	}
	dependente := (*TFluxoExecução)(fluxoExecuçãoPonteiro)
	dependente.Stack = uint32(uintptr(stackPonteiro))
	dependente.CpuEstado = (*TcpuEstado)(Pointer(uintptr(stackPonteiro) + FluxoExecuçãostackTamanho - Sizeof(TcpuEstado{})))
	*dependente.CpuEstado = *cpu
	dependente.CpuEstado.Eax = 0
	dependente.Utilizadorstack_2 = cpu.Esp
	dependente.UtilizadorstackTamanho_2 = 0
	dependente.Pid = pid
	dependente.Superiorpid = superiorpid
	dependente.Páginadiretóriopontodeentrada = dependentepáginadiretório
	dependente.FluxoExecuçãoEstado = Pronto
	dependente.FpuDeslocamento = 0xffffffff
	dependente.Isnúcleo = false
	AdicionarrunnablefluxoExecução(dependente)
	return int32(pid)
}

func sysSair(estado uint32) {
	pid := Atualpid()
	for i := 0; i < len(processoTabela); i++ {
		if processoTabela[i].utilizado && processoTabela[i].pid == pid {
			fecharTudoprocessofds(&processoTabela[i])
			processoTabela[i].saiu = true
			processoTabela[i].estado = (estado & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, estadoEndereço uint32, opções uint32) int32 {
	if (opções & ^uint32(1)) != 0 {
		return Einval
	}
	superiorpid := Atualpid()
	founddependente := false
	for i := 0; i < len(processoTabela); i++ {
		p := &processoTabela[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.utilizado && matches && p.superior == superiorpid {
			founddependente = true
			if p.saiu {
				if estadoEndereço != 0 {
					*(*uint32)(Pointer(uintptr(estadoEndereço))) = p.estado
				}
				dependentepid := p.pid
				*p = processopontodeentrada{}
				return int32(dependentepid)
			}
		}
	}
	if !founddependente {
		return Echild
	}

	if (opções & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocesso(superior uint32) uint32 {
	superiorprocesso := procurarprocesso(superior)
	pid := Allocatepid()
	for i := 0; i < len(processoTabela); i++ {
		if !processoTabela[i].utilizado {
			processoTabela[i] = processopontodeentrada{
				utilizado:	true,
				pid:		pid,
				superior:	superior,
				programabreak:	utilizadorheapbase,
			}
			if superiorprocesso != nil {
				processoTabela[i].programabreak = superiorprocesso.programabreak
				for fd := 0; fd < maxfd; fd++ {
					if superiorprocesso.fds[fd].utilizado {
						processoTabela[i].fds[fd] = superiorprocesso.fds[fd]
						descrição := superiorprocesso.fds[fd].descrição
						if descrição >= 0 && descrição < maxabrirFICHEIROS {
							abrirficheiroTabela[descrição].refs++
						}
					}
				}
			} else {
				initializeprocessofds(&processoTabela[i])
			}
			return pid
		}
	}
	return 0
}

func fecharTudoprocessofds(processo *processopontodeentrada) {
	if processo == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if processo.fds[fd].utilizado {
			fecharprocessofd(processo, fd)
		}
	}
}

func apagarprocesso(pid uint32) {
	processo := procurarprocesso(pid)
	if processo == nil {
		return
	}
	fecharTudoprocessofds(processo)
	*processo = processopontodeentrada{}
}

func copiarCAMINHO(cAMINHOEndereço uint32) (uint32, [12]byte) {
	var nome [12]byte
	if cAMINHOEndereço == 0 {
		return 0, nome
	}
	raw := GetbytesdePonteiro(uintptr(cAMINHOEndereço), 64, 64)
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

func ficheiroTamanho(nomedoficheiro []byte) uint32 {
	var ata0s = TAvançadoTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partição := TmsdospartiçãoTabela{}
	partição.Lerpartição(&ata0s)

	bios := TParâmetros_do_sistema_de_ficheiros32{}
	tamanho := bios.Len(&ata0s, partição.Mbr.Primarypartição[0], nomedoficheiro)
	ata0s.Flush()
	return tamanho
}

func lerficheiro(nomedoficheiro []byte, dados []byte) {
	var ata0s = TAvançadoTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partição := TmsdospartiçãoTabela{}
	partição.Lerpartição(&ata0s)

	bios := TParâmetros_do_sistema_de_ficheiros32{}
	bios.Ler(&ata0s, partição.Mbr.Primarypartição[0], nomedoficheiro, dados)
	ata0s.Flush()
}

func getcr3() uint32
