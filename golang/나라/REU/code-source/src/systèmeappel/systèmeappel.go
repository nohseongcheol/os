package systèmeappel

import . "unsafe"

import . "interruption"
import . "console"
import . "utilitaire"
import . "multiplegestionTâches"
import . "pilote/ata"
import . "fichiersystème/msdospartition"
import . "fichiersystème/fat"
import . "fichiersystème/format_exécutable_et_liable"
import mem "mémoiregestionnaire"
import . "pagination"
import . "port"
import . "gestionTâches/ordonnanceur"
import . "gestionTâches/filExécution"
import . "virtuelmémoire"

var console_2 = TConsole{}

type TSyscall struct {
	TInterruptionhandler
}

const (
	SysQuitter	uint32	= 1
	Sysfork		uint32	= 2
	Syslire		uint32	= 3
	Sysécrire	uint32	= 4
	Sysouvrir	uint32	= 5
	Sysfermer	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysaccès	uint32	= 33
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
	SysrtQuitter	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2Élevé		int32	= -7
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
	maxouvrirFICHIERS		= 128
)

type fdélément struct {
	utilisé		bool
	description	int32
	fdAttributs	uint32
}

type ouvrirfichierdescription struct {
	utilisé		bool
	refs		uint32
	typeValeur	uint32
	attributs_2	uint32
	position	uint32
	taille		uint32
	nom		[12]byte
	nomlen		uint32
	aux		uint32
}

const (
	fdTypeAucun		uint32	= 0
	fdTypefat		uint32	= 1
	fdTypestdin		uint32	= 2
	fdTypeconsole		uint32	= 3
	fdTypeRacinerépertoire	uint32	= 4
	fdTypepriseRéseau	uint32	= 5

	olireseulement		uint32	= 0
	oécrireseulement	uint32	= 1
	olireécrire		uint32	= 2
	ocréer			uint32	= 0x40
	oTronquelavaleur	uint32	= 0x200
	oappend			uint32	= 0x400
	orépertoire		uint32	= 0x10000

	seekensemble	uint32	= 0
	seekCourante	uint32	= 1
	seekFin		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fensemblefd	uint32	= 2
	fgetfl		uint32	= 3
	fensemblefl	uint32	= 4
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
	maxpriseRéseaupaquets	= 8
	maxdatagramTaille	= 512
)

type priseRéseauaddressiValeur4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zéro	[8]byte
}

type priseRéseaupacket struct {
	utilisé	bool
	taille	uint32
	source	priseRéseauaddressiValeur4
	données	[maxdatagramTaille]byte
}

type localedatagrampriseRéseau struct {
	utilisé		bool
	bound		bool
	connected	bool
	locale		priseRéseauaddressiValeur4
	distant		priseRéseauaddressiValeur4
	head		uint32
	tail		uint32
	nombre		uint32
	paquets		[maxpriseRéseaupaquets]priseRéseaupacket
}

type posixstat struct {
	Périphérique	uint32
	Ino		uint32
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Taille_2	int32
	Blksize		int32
	Bloc		int32
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
	maxExécutionvectorélément	= 16
	maxExécutionChaîneDurée		= 63
)

type exécutionvector struct {
	nombre	uint32
	lengths	[maxExécutionvectorélément]uint32
	valeurs	[maxExécutionvectorélément][maxExécutionChaîneDurée + 1]byte
}

type processusélément struct {
	utilisé		bool
	pid		uint32
	parent		uint32
	fermé		bool
	état		uint32
	programmebreak	uint32
	fds		[maxfd]fdélément
}

type chaîneenTête struct {
	Data	uintptr
	Len	int
}

func syscallErreur(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var ouvrirfichierTableau [maxouvrirFICHIERS]ouvrirfichierdescription
var processusTableau [32]processusélément
var localesockets [maxsockets]localedatagrampriseRéseau
var suivantephemeralport uint16 = 49152

const (
	utilisateurheapbase	uint32	= 0x06000000
	utilisateurheapLimite	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinlire uint32
var stdinécrire uint32

func Interruption(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysQuitter_2(index uint32) {
	Syscall(SysQuitter, index)
}

func Syslire_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Syslire, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysImprimerstr(buffer string) {
	h := (*chaîneenTête)(Pointer(&buffer))
	Syscall(Sysécrire, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysImprimerunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysécrire, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysouvrir_2(cHEMIN uintptr, attributs_2 uint32, mode uint32) int32 {
	return int32(Syscall(Sysouvrir, uint32(cHEMIN), attributs_2, mode))
}

func Sysfermer_2(fd uint32) int32 {
	return int32(Syscall(Sysfermer, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(paramètres ...uint32) uint32 {

	l := len(paramètres)
	switch l {
	case 1:
		return Interruption(paramètres[0], 0, 0, 0, 0, 0)
	case 2:
		return Interruption(paramètres[0], paramètres[1], 0, 0, 0, 0)
	case 3:
		return Interruption(paramètres[0], paramètres[1], paramètres[2], 0, 0, 0)
	case 4:
		return Interruption(paramètres[0], paramètres[1], paramètres[2], paramètres[3], 0, 0)
	case 5:
		return Interruption(paramètres[0], paramètres[1], paramètres[2], paramètres[3], paramètres[4], 0)
	case 6:
		return Interruption(paramètres[0], paramètres[1], paramètres[2], paramètres[3], paramètres[4], paramètres[5])
	default:
		return syscallErreur(Enosys)
	}
}

func (self *TSyscall) Init(gestionnaire *TInterruptiongestionnaire) {
	initfichierdescriptor()

	interruptionhandler = poignéeinterruption

	var address uintptr
	address = uintptr(Pointer(&interruptionhandler))

	self.TInterruptionhandler.Init(0x80, uintptr(Pointer(gestionnaire)), address)
}

var interruptionhandler func(uint32) uint32

func poignéeinterruption(esp uint32) uint32 {
	var processeur = (*TcpuÉtat)(Pointer(uintptr(esp)))

	switch processeur.Eax {
	case SysQuitter:
		sysQuitter(processeur.Ebx)
		return uint32(uintptr(Pointer(ArrêterCourantefilExécution(processeur))))
	case SysrtQuitter:
		sysQuitter(processeur.Ebx)
		return uint32(uintptr(Pointer(ArrêterCourantefilExécution(processeur))))
	case Sysfork:
		processeur.Eax = uint32(sysfork(processeur))
		return esp
	case Syslire:
		processeur.Eax = uint32(syslire(int32(processeur.Ebx), processeur.Ecx, processeur.Edx))
		return esp
	case Sysécrire:
		processeur.Eax = uint32(sysécrire(int32(processeur.Ebx), processeur.Ecx, processeur.Edx))
		return esp
	case Sysouvrir:
		processeur.Eax = uint32(sysouvrir(processeur.Ebx, processeur.Ecx, processeur.Edx))
		return esp
	case Syscreat:
		processeur.Eax = uint32(sysouvrir(processeur.Ebx, ocréer|oécrireseulement|oTronquelavaleur, processeur.Ecx))
		return esp
	case Sysfermer:
		processeur.Eax = uint32(sysfermer(int32(processeur.Ebx)))
		return esp
	case Syswaitpid:
		processeur.Eax = uint32(syswaitpid(int32(processeur.Ebx), processeur.Ecx, processeur.Edx))
		return esp
	case Syslseek:
		processeur.Eax = uint32(syslseek(int32(processeur.Ebx), int32(processeur.Ecx), processeur.Edx))
		return esp
	case Sysexecve:
		processeur.Eax = uint32(sysexecve(processeur, processeur.Ebx))
		return esp
	case Sysgetpid:
		processeur.Eax = Courantepid()
		return esp
	case Sysgetppid:
		processeur.Eax = Couranteparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		processeur.Eax = 0
		return esp
	case Sysaccès:
		processeur.Eax = uint32(sysaccès(processeur.Ebx, processeur.Ecx))
		return esp
	case Syschdir:
		processeur.Eax = uint32(syschdir(processeur.Ebx))
		return esp
	case Sysgetcwd:
		processeur.Eax = uint32(sysgetcwd(processeur.Ebx, processeur.Ecx))
		return esp
	case Sysdup:
		processeur.Eax = uint32(sysdup(int32(processeur.Ebx), 0))
		return esp
	case Sysdup2:
		processeur.Eax = uint32(sysdup2(int32(processeur.Ebx), int32(processeur.Ecx)))
		return esp
	case Syssocketcall:
		processeur.Eax = uint32(syspriseRéseauappel(processeur.Ebx, processeur.Ecx))
		return esp
	case Sysfcntl:
		processeur.Eax = uint32(sysfcntl(int32(processeur.Ebx), processeur.Ecx, processeur.Edx))
		return esp
	case Sysstat, Syslstat:
		processeur.Eax = uint32(sysstat(processeur.Ebx, processeur.Ecx))
		return esp
	case Sysfstat:
		processeur.Eax = uint32(sysfstat(int32(processeur.Ebx), processeur.Ecx))
		return esp
	case Sysfsync:
		processeur.Eax = uint32(sysfsync(int32(processeur.Ebx)))
		return esp
	case Syssync:
		processeur.Eax = 0
		return esp
	case Sysuname:
		processeur.Eax = uint32(sysuname(processeur.Ebx))
		return esp
	case Sysbrk:
		processeur.Eax = sysbrk(processeur.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Imprimer(processeur.Ebx)
		return esp

	default:
		console_2.MImprimerxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Imprimer(esp)
		console_2.MImprimer(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimer(processeur.Eax)
		console_2.MImprimer(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimer(processeur.Ebx)
		console_2.MImprimer(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimer(processeur.Ecx)
		console_2.MImprimer(([]byte)(":"))
		console_2.MUnsignedinteger32Imprimer(processeur.Edx)
		console_2.MImprimer(([]byte)("]"))
		processeur.Eax = syscallErreur(Enosys)
		return esp
	}

	return esp
}

func initfichierdescriptor() {
	for i := 0; i < maxouvrirFICHIERS; i++ {
		ouvrirfichierTableau[i] = ouvrirfichierdescription{}
	}
	for i := 0; i < len(processusTableau); i++ {
		processusTableau[i] = processusélément{}
	}
	for i := 0; i < len(localesockets); i++ {
		localesockets[i] = localedatagrampriseRéseau{}
	}
	suivantephemeralport = 49152
	ouvrirfichierTableau[0] = ouvrirfichierdescription{utilisé: true, typeValeur: fdTypestdin, attributs_2: olireseulement}
	ouvrirfichierTableau[1] = ouvrirfichierdescription{utilisé: true, typeValeur: fdTypeconsole, attributs_2: oécrireseulement}
	ouvrirfichierTableau[2] = ouvrirfichierdescription{utilisé: true, typeValeur: fdTypeconsole, attributs_2: oécrireseulement}
}

func rechercherprocessus(pid uint32) *processusélément {
	for i := 0; i < len(processusTableau); i++ {
		if processusTableau[i].utilisé && processusTableau[i].pid == pid {
			return &processusTableau[i]
		}
	}
	return nil
}

func initializeprocessusfds(processus *processusélément) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		processus.fds[fd] = fdélément{utilisé: true, description: fd}
		ouvrirfichierTableau[fd].refs++
	}
}

func ensureCouranteprocessus() *processusélément {
	pid := Courantepid()
	if processus := rechercherprocessus(pid); processus != nil {
		return processus
	}
	for i := 0; i < len(processusTableau); i++ {
		if !processusTableau[i].utilisé {
			processusTableau[i] = processusélément{
				utilisé:	true,
				pid:		pid,
				parent:		Couranteparentpid(),
				programmebreak:	utilisateurheapbase,
			}
			initializeprocessusfds(&processusTableau[i])
			return &processusTableau[i]
		}
	}
	return nil
}

func getouvrirfichierfor(processus *processusélément, fd int32) *ouvrirfichierdescription {
	if processus == nil || fd < 0 || fd >= maxfd || !processus.fds[fd].utilisé {
		return nil
	}
	description := processus.fds[fd].description
	if description < 0 || description >= maxouvrirFICHIERS || !ouvrirfichierTableau[description].utilisé {
		return nil
	}
	return &ouvrirfichierTableau[description]
}

func getouvrirfichier(fd int32) *ouvrirfichierdescription {
	return getouvrirfichierfor(ensureCouranteprocessus(), fd)
}

func allocateouvrirfichier() int32 {
	for i := int32(3); i < maxouvrirFICHIERS; i++ {
		if !ouvrirfichierTableau[i].utilisé {
			ouvrirfichierTableau[i] = ouvrirfichierdescription{utilisé: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(processus *processusélément, description int32, minimum int32) int32 {
	if processus == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !processus.fds[fd].utilisé {
			processus.fds[fd] = fdélément{utilisé: true, description: description}
			return fd
		}
	}
	return Emfile
}

func releaseouvrirfichier(description int32) {
	if description < 0 || description >= maxouvrirFICHIERS {
		return
	}
	élément := &ouvrirfichierTableau[description]
	if élément.refs > 0 {
		élément.refs--
	}

	if élément.refs == 0 && description > stderrfd {
		if élément.typeValeur == fdTypepriseRéseau && élément.aux < maxsockets {
			localesockets[élément.aux] = localedatagrampriseRéseau{}
		}
		*élément = ouvrirfichierdescription{}
	}
}

func fermerprocessusfd(processus *processusélément, fd int32) int32 {
	if processus == nil || getouvrirfichierfor(processus, fd) == nil {
		return Ebadf
	}
	description := processus.fds[fd].description
	processus.fds[fd] = fdélément{}
	releaseouvrirfichier(description)
	return 0
}

func sysécrire(fd int32, address uint32, nombre uint32) int32 {
	if nombre == 0 {
		return 0
	}
	if address == 0 || address+nombre < address {
		return Efault
	}
	if nombre > 4096 {
		return Einval
	}
	élément := getouvrirfichier(fd)
	if élément == nil {
		return Ebadf
	}
	if élément.typeValeur != fdTypeconsole {
		if élément.typeValeur == fdTypepriseRéseau {
			return priseRéseauEnvoyerto(fd, address, nombre, 0, 0)
		}
		if élément.typeValeur == fdTypefat || élément.typeValeur == fdTypeRacinerépertoire {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetOctetsdePointeur(uintptr(address), int(nombre), int(nombre))
	console_2.MImprimer(buffer)
	return int32(nombre)
}

func syslire(fd int32, address uint32, nombre uint32) int32 {
	if nombre == 0 {
		return 0
	}
	if address == 0 || address+nombre < address {
		return Efault
	}
	élément := getouvrirfichier(fd)
	if élément == nil {
		return Ebadf
	}
	if élément.typeValeur == fdTypestdin {
		return lirestdin(address, nombre)
	}
	if élément.typeValeur == fdTypeRacinerépertoire {
		return Eisdir
	}
	if élément.typeValeur == fdTypepriseRéseau {
		return priseRéseaureceivede(fd, address, nombre, 0, 0)
	}
	if élément.typeValeur != fdTypefat {
		return Ebadf
	}
	if élément.position >= élément.taille {
		return 0
	}
	remaining := élément.taille - élément.position
	if nombre > remaining {
		nombre = remaining
	}
	buffer := GetOctetsdePointeur(uintptr(address), int(nombre), int(nombre))
	return lirevfsfichier(élément, buffer, nombre)
}

func sysouvrir(cHEMINaddress uint32, attributs_2 uint32, mode uint32) int32 {
	_ = mode
	if cHEMINaddress == 0 {
		return Efault
	}
	accèsmode := attributs_2 & 3
	if accèsmode == oécrireseulement || accèsmode == olireécrire || (attributs_2&(ocréer|oTronquelavaleur|oappend)) != 0 {
		return Erofs
	}

	processus := ensureCouranteprocessus()
	if processus == nil {
		return Enfile
	}
	description := allocateouvrirfichier()
	if description < 0 {
		return description
	}
	élément := &ouvrirfichierTableau[description]
	élément.attributs_2 = attributs_2
	if isRacineCHEMIN(cHEMINaddress) {
		élément.typeValeur = fdTypeRacinerépertoire
		élément.taille = 0
	} else {
		nomlen, nom := copierCHEMIN(cHEMINaddress)
		if nomlen == 0 {
			*élément = ouvrirfichierdescription{}
			return Enoent
		}
		taille := fichierTaille(nom[:nomlen])
		if taille == 0 {
			*élément = ouvrirfichierdescription{}
			return Enoent
		}
		if (attributs_2 & orépertoire) != 0 {
			*élément = ouvrirfichierdescription{}
			return Enotdir
		}
		élément.typeValeur = fdTypefat
		élément.taille = taille
		élément.nomlen = nomlen
		élément.nom = nom
	}

	fd := allocatefd(processus, description, 3)
	if fd < 0 {
		*élément = ouvrirfichierdescription{}
		return fd
	}
	return fd
}

func sysfermer(fd int32) int32 {
	return fermerprocessusfd(ensureCouranteprocessus(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	processus := ensureCouranteprocessus()
	élément := getouvrirfichierfor(processus, fd)
	if élément == nil {
		return Ebadf
	}
	nouveaufd := allocatefd(processus, processus.fds[fd].description, minimum)
	if nouveaufd >= 0 {
		élément.refs++
	}
	return nouveaufd
}

func sysdup2(vieuxfd int32, nouveaufd int32) int32 {
	processus := ensureCouranteprocessus()
	élément := getouvrirfichierfor(processus, vieuxfd)
	if élément == nil {
		return Ebadf
	}
	if nouveaufd < 0 || nouveaufd >= maxfd {
		return Ebadf
	}
	if vieuxfd == nouveaufd {
		return nouveaufd
	}
	if processus.fds[nouveaufd].utilisé {
		fermerprocessusfd(processus, nouveaufd)
	}
	processus.fds[nouveaufd] = fdélément{utilisé: true, description: processus.fds[vieuxfd].description}
	élément.refs++
	return nouveaufd
}

func sysfcntl(fd int32, commande uint32, argument uint32) int32 {
	processus := ensureCouranteprocessus()
	élément := getouvrirfichierfor(processus, fd)
	if élément == nil {
		return Ebadf
	}
	switch commande {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(processus.fds[fd].fdAttributs)
	case fensemblefd:
		processus.fds[fd].fdAttributs = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(élément.attributs_2)
	case fensemblefl:
		élément.attributs_2 = (élément.attributs_2 & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, décalage int32, whence uint32) int32 {
	élément := getouvrirfichier(fd)
	if élément == nil {
		return Ebadf
	}
	if élément.typeValeur != fdTypefat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekensemble:
		base = 0
	case seekCourante:
		base = int64(élément.position)
	case seekFin:
		base = int64(élément.taille)
	default:
		return Einval
	}
	position_2 := base + int64(décalage)
	if position_2 < 0 || position_2 > 0x7FFFFFFF {
		return Einval
	}
	élément.position = uint32(position_2)
	return int32(élément.position)
}

func lirevfsfichier(élément *ouvrirfichierdescription, destination_2 []byte, nombre uint32) int32 {
	mémoiregestionnaire := &mem.TMémoiregestionnaire{}
	tmpPointeur := mémoiregestionnaire.Allouer_la_mémoire(élément.taille)
	if tmpPointeur == nil {
		return Einval
	}
	tmp := GetOctetsdePointeur(uintptr(tmpPointeur), int(élément.taille), int(élément.taille))
	lirefichier(élément.nom[:élément.nomlen], tmp)
	copy(destination_2[:nombre], tmp[élément.position:élément.position+nombre])
	élément.position += nombre
	mémoiregestionnaire.Libre(tmpPointeur)
	return int32(nombre)
}

func isRacineCHEMIN(cHEMINaddress uint32) bool {
	if cHEMINaddress == 0 {
		return false
	}
	cHEMIN := GetOctetsdePointeur(uintptr(cHEMINaddress), 4, 4)
	if cHEMIN[0] == '/' && cHEMIN[1] == 0 {
		return true
	}
	if cHEMIN[0] == '.' && cHEMIN[1] == 0 {
		return true
	}
	if cHEMIN[0] == '/' && cHEMIN[1] == '.' && cHEMIN[2] == 0 {
		return true
	}
	return false
}

func sysaccès(cHEMINaddress uint32, mode uint32) int32 {
	if cHEMINaddress == 0 {
		return Efault
	}
	if (mode & ^uint32(7)) != 0 {
		return Einval
	}
	isRacine := isRacineCHEMIN(cHEMINaddress)
	exists := isRacine
	if !exists {
		nomlen, nom := copierCHEMIN(cHEMINaddress)
		exists = nomlen != 0 && fichierTaille(nom[:nomlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mode & 2) != 0 {
		return Eacces
	}

	if (mode&1) != 0 && !isRacine {
		return Eacces
	}
	return 0
}

func syschdir(cHEMINaddress uint32) int32 {
	if cHEMINaddress == 0 {
		return Efault
	}
	if !isRacineCHEMIN(cHEMINaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, taille uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if taille < 2 {
		return Erange
	}
	buffer_2 := GetOctetsdePointeur(uintptr(bufferaddress), int(taille), int(taille))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mode uint32, taille uint32, inœud uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Périphérique = 1
	stat.Ino = inœud
	stat.Mode = mode
	stat.Nlink = 1
	stat.Taille_2 = int32(taille)
	stat.Blksize = 512
	stat.Bloc = int32((taille + 511) / 512)
	return 0
}

func sysstat(cHEMINaddress uint32, stataddress uint32) int32 {
	if cHEMINaddress == 0 {
		return Efault
	}
	if isRacineCHEMIN(cHEMINaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nomlen, nom := copierCHEMIN(cHEMINaddress)
	if nomlen == 0 {
		return Enoent
	}
	taille := fichierTaille(nom[:nomlen])
	if taille == 0 {
		return Enoent
	}
	inœud := uint32(2)
	for i := uint32(0); i < nomlen; i++ {
		inœud = inœud*33 + uint32(nom[i])
	}
	return fillposixstat(stataddress, sifreg|0444, taille, inœud)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	élément := getouvrirfichier(fd)
	if élément == nil {
		return Ebadf
	}
	switch élément.typeValeur {
	case fdTypestdin, fdTypeconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdTypeRacinerépertoire:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdTypefat:
		return fillposixstat(stataddress, sifreg|0444, élément.taille, uint32(fd+2))
	case fdTypepriseRéseau:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getouvrirfichier(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	processus := ensureCouranteprocessus()
	if processus == nil {
		return 0
	}
	if processus.programmebreak == 0 {
		processus.programmebreak = utilisateurheapbase
	}
	if address_2 == 0 {
		return processus.programmebreak
	}
	if address_2 < utilisateurheapbase || address_2 > utilisateurheapLimite {
		return processus.programmebreak
	}
	processus.programmebreak = address_2
	return processus.programmebreak
}

func copierutschamp(destination *[65]byte, valeur string) {
	limite := len(valeur)
	if limite > 64 {
		limite = 64
	}
	for i := 0; i < limite; i++ {
		destination[i] = valeur[i]
	}
	destination[limite] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nom := (*posixutsname)(Pointer(uintptr(address_2)))
	*nom = posixutsname{}
	copierutschamp(&nom.Sysname, "EngOS")
	copierutschamp(&nom.Nodename, "engos")
	copierutschamp(&nom.Release, "0.1-posix")
	copierutschamp(&nom.Version, "POSIX.1-2017 phase 1")
	copierutschamp(&nom.Machine, "i386")
	return 0
}

func swapunsignedinteger16(valeur uint16) uint16 {
	return (valeur << 8) | (valeur >> 8)
}

func priseRéseauappelargument(arguments_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + index*4)))
}

func priseRéseauforfd(fd int32) (*localedatagrampriseRéseau, int32) {
	élément := getouvrirfichier(fd)
	if élément == nil || élément.typeValeur != fdTypepriseRéseau || élément.aux >= maxsockets {
		return nil, Ebadf
	}
	priseRéseau := &localesockets[élément.aux]
	if !priseRéseau.utilisé {
		return nil, Ebadf
	}
	return priseRéseau, 0
}

func allocatepriseRéseau(domaine uint32, priseRéseautype uint32, protocol uint32) int32 {
	if domaine != afinet {
		return Eafnosupport
	}
	if priseRéseautype != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	processus := ensureCouranteprocessus()
	if processus == nil {
		return Enfile
	}
	priseRéseauindex := -1
	for i := 0; i < maxsockets; i++ {
		if !localesockets[i].utilisé {
			priseRéseauindex = i
			break
		}
	}
	if priseRéseauindex < 0 {
		return Enfile
	}
	description := allocateouvrirfichier()
	if description < 0 {
		return description
	}
	localesockets[priseRéseauindex] = localedatagrampriseRéseau{utilisé: true}
	élément := &ouvrirfichierTableau[description]
	élément.typeValeur = fdTypepriseRéseau
	élément.attributs_2 = olireécrire
	élément.aux = uint32(priseRéseauindex)
	fd := allocatefd(processus, description, 3)
	if fd < 0 {
		localesockets[priseRéseauindex] = localedatagrampriseRéseau{}
		*élément = ouvrirfichierdescription{}
		return fd
	}
	return fd
}

func priseRéseauaddress(address_2 uint32, durée uint32) (*priseRéseauaddressiValeur4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if durée < 16 {
		return nil, Einval
	}
	rÉSULTAT := (*priseRéseauaddressiValeur4)(Pointer(uintptr(address_2)))
	if rÉSULTAT.Family != afinet {
		return nil, Eafnosupport
	}
	return rÉSULTAT, 0
}

func portEntranteUtiliser(port uint16, except *localedatagrampriseRéseau) bool {
	for i := 0; i < maxsockets; i++ {
		priseRéseau := &localesockets[i]
		if priseRéseau != except && priseRéseau.utilisé && priseRéseau.bound && priseRéseau.locale.Port == port {
			return true
		}
	}
	return false
}

func relierephemeral(priseRéseau *localedatagrampriseRéseau) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(suivantephemeralport)
		suivantephemeralport++
		if suivantephemeralport < 49152 {
			suivantephemeralport = 49152
		}
		if !portEntranteUtiliser(port, priseRéseau) {
			priseRéseau.locale = priseRéseauaddressiValeur4{Family: afinet, Port: port, Address: 0x0100007F}
			priseRéseau.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func priseRéseauRelier(fd int32, address_2 uint32, durée uint32) int32 {
	priseRéseau, err := priseRéseauforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := priseRéseauaddress(address_2, durée)
	if err != 0 {
		return err
	}
	if priseRéseau.bound {
		return Einval
	}
	if requested.Port == 0 {
		return relierephemeral(priseRéseau)
	}
	if portEntranteUtiliser(requested.Port, priseRéseau) {
		return Eaddrinuse
	}
	priseRéseau.locale = *requested
	priseRéseau.bound = true
	return 0
}

func priseRéseauConnecter(fd int32, address_2 uint32, durée uint32) int32 {
	priseRéseau, err := priseRéseauforfd(fd)
	if err != 0 {
		return err
	}
	distant, err := priseRéseauaddress(address_2, durée)
	if err != 0 {
		return err
	}
	if !priseRéseau.bound {
		if err := relierephemeral(priseRéseau); err != 0 {
			return err
		}
	}
	priseRéseau.distant = *distant
	priseRéseau.connected = true
	return 0
}

func priseRéseauEnvoyerto(fd int32, bufferaddress_2 uint32, durée uint32, destinationaddress uint32, destinationDurée uint32) int32 {
	priseRéseau, err := priseRéseauforfd(fd)
	if err != 0 {
		return err
	}
	if durée > maxdatagramTaille {
		return Emsgsize
	}
	if durée != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination priseRéseauaddressiValeur4
	if destinationaddress != 0 {
		address_2, addressErreur := priseRéseauaddress(destinationaddress, destinationDurée)
		if addressErreur != 0 {
			return addressErreur
		}
		destination = *address_2
	} else {
		if !priseRéseau.connected {
			return Enotconn
		}
		destination = priseRéseau.distant
	}
	if !priseRéseau.bound {
		if relierErreur := relierephemeral(priseRéseau); relierErreur != 0 {
			return relierErreur
		}
	}
	var receiver *localedatagrampriseRéseau
	for i := 0; i < maxsockets; i++ {
		candidate := &localesockets[i]
		if candidate.utilisé && candidate.bound && candidate.locale.Port == destination.Port &&
			(candidate.locale.Address == 0 || candidate.locale.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.nombre >= maxpriseRéseaupaquets {
		return Eagain
	}
	packet := &receiver.paquets[receiver.tail]
	*packet = priseRéseaupacket{utilisé: true, taille: durée, source: priseRéseau.locale}
	if durée != 0 {
		source := GetOctetsdePointeur(uintptr(bufferaddress_2), int(durée), int(durée))
		copy(packet.données[:durée], source)
	}
	receiver.tail = (receiver.tail + 1) % maxpriseRéseaupaquets
	receiver.nombre++
	return int32(durée)
}

func priseRéseaureceivede(fd int32, bufferaddress_2 uint32, durée uint32, sourceaddress uint32, sourceDuréeaddress uint32) int32 {
	priseRéseau, err := priseRéseauforfd(fd)
	if err != 0 {
		return err
	}
	if durée != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if priseRéseau.nombre == 0 {
		return Eagain
	}
	packet := &priseRéseau.paquets[priseRéseau.head]
	copierDurée := packet.taille
	if copierDurée > durée {
		copierDurée = durée
	}
	if copierDurée != 0 {
		destination := GetOctetsdePointeur(uintptr(bufferaddress_2), int(copierDurée), int(copierDurée))
		copy(destination, packet.données[:copierDurée])
	}
	if sourceaddress != 0 {
		if sourceDuréeaddress == 0 {
			return Efault
		}
		providedDurée := (*uint32)(Pointer(uintptr(sourceDuréeaddress)))
		if *providedDurée >= 16 {
			*(*priseRéseauaddressiValeur4)(Pointer(uintptr(sourceaddress))) = packet.source
		}
		*providedDurée = 16
	}
	*packet = priseRéseaupacket{}
	priseRéseau.head = (priseRéseau.head + 1) % maxpriseRéseaupaquets
	priseRéseau.nombre--
	return int32(copierDurée)
}

func copierpriseRéseauNom(fd int32, address_2 uint32, duréeaddress uint32, peer bool) int32 {
	priseRéseau, err := priseRéseauforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || duréeaddress == 0 {
		return Efault
	}
	durée := (*uint32)(Pointer(uintptr(duréeaddress)))
	if *durée < 16 {
		*durée = 16
		return Einval
	}
	if peer {
		if !priseRéseau.connected {
			return Enotconn
		}
		*(*priseRéseauaddressiValeur4)(Pointer(uintptr(address_2))) = priseRéseau.distant
	} else {
		if !priseRéseau.bound {
			if relierErreur := relierephemeral(priseRéseau); relierErreur != 0 {
				return relierErreur
			}
		}
		*(*priseRéseauaddressiValeur4)(Pointer(uintptr(address_2))) = priseRéseau.locale
	}
	*durée = 16
	return 0
}

func syspriseRéseauappel(appel uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch appel {
	case 1:
		return allocatepriseRéseau(priseRéseauappelargument(arguments_2, 0), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2))
	case 2:
		return priseRéseauRelier(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2))
	case 3:
		return priseRéseauConnecter(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copierpriseRéseauNom(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2), false)
	case 7:
		return copierpriseRéseauNom(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2), true)
	case 9:
		return priseRéseauEnvoyerto(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2), 0, 0)
	case 10:
		return priseRéseaureceivede(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2), 0, 0)
	case 11:
		return priseRéseauEnvoyerto(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2), priseRéseauappelargument(arguments_2, 4), priseRéseauappelargument(arguments_2, 5))
	case 12:
		return priseRéseaureceivede(int32(priseRéseauappelargument(arguments_2, 0)), priseRéseauappelargument(arguments_2, 1), priseRéseauappelargument(arguments_2, 2), priseRéseauappelargument(arguments_2, 4), priseRéseauappelargument(arguments_2, 5))
	case 13:
		if _, err := priseRéseauforfd(int32(priseRéseauappelargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := priseRéseauforfd(int32(priseRéseauappelargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func lirestdin(address uint32, nombre uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetOctetsdePointeur(uintptr(address), int(nombre), int(nombre))
	var n uint32
	for n < nombre {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputoctet(c byte) {
	suivant := (stdinécrire + 1) % uint32(len(stdinbuffer))
	if suivant == stdinlire {
		return
	}
	stdinbuffer[stdinécrire] = c
	stdinécrire = suivant
}

func stdingetblocking() byte {
	for stdinlire == stdinécrire {
		sc := pollclavierscancode()
		if sc != 0 {
			Stdinputoctet(sc)
		}
	}
	c := stdinbuffer[stdinlire]
	stdinlire = (stdinlire + 1) % uint32(len(stdinbuffer))
	return c
}

func pollclavierscancode() byte {
	for (Portlireoctet(0x64) & 0x01) == 0 {
	}
	sc := Portlireoctet(0x60)
	return scancodetooctet(sc)
}

func scancodetooctet(sc uint8) byte {
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

func copierExécutionvector(address_2 uint32, rÉSULTAT *exécutionvector) int32 {
	*rÉSULTAT = exécutionvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxExécutionvectorélément; index++ {
		chaîneaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if chaîneaddress == 0 {
			rÉSULTAT.nombre = index
			return 0
		}
		terminated := false
		for durée := uint32(0); durée <= maxExécutionChaîneDurée; durée++ {
			valeur := *(*byte)(Pointer(uintptr(chaîneaddress + durée)))
			rÉSULTAT.valeurs[index][durée] = valeur
			if valeur == 0 {
				rÉSULTAT.lengths[index] = durée
				terminated = true
				break
			}
		}
		if !terminated {
			return E2Élevé
		}
	}
	return E2Élevé
}

func pushExécutionunsignedinteger32(mémoire_de_pile *uint32, valeur uint32) {
	*mémoire_de_pile -= 4
	*(*uint32)(Pointer(uintptr(*mémoire_de_pile))) = valeur
}

func setupExécutionstack(processeur *TcpuÉtat, arguments_2 *exécutionvector, environment *exécutionvector) int32 {
	const stackOctets uint32 = 4096
	if !MakeIntervallePrivéwritable(getcr3(), UtilisateurstackHaut-stackOctets, stackOctets) {
		return Enomem
	}
	mémoire_de_pile := UtilisateurstackHaut
	var argumentpointers [maxExécutionvectorélément]uint32
	var environmentpointers [maxExécutionvectorélément]uint32

	for i := int(environment.nombre) - 1; i >= 0; i-- {
		durée := environment.lengths[i] + 1
		mémoire_de_pile -= durée
		destination := GetOctetsdePointeur(uintptr(mémoire_de_pile), int(durée), int(durée))
		copy(destination, environment.valeurs[i][:durée])
		environmentpointers[i] = mémoire_de_pile
	}
	for i := int(arguments_2.nombre) - 1; i >= 0; i-- {
		durée := arguments_2.lengths[i] + 1
		mémoire_de_pile -= durée
		destination := GetOctetsdePointeur(uintptr(mémoire_de_pile), int(durée), int(durée))
		copy(destination, arguments_2.valeurs[i][:durée])
		argumentpointers[i] = mémoire_de_pile
	}
	mémoire_de_pile &= ^uint32(3)
	pushExécutionunsignedinteger32(&mémoire_de_pile, 0)
	for i := int(environment.nombre) - 1; i >= 0; i-- {
		pushExécutionunsignedinteger32(&mémoire_de_pile, environmentpointers[i])
	}
	pushExécutionunsignedinteger32(&mémoire_de_pile, 0)
	for i := int(arguments_2.nombre) - 1; i >= 0; i-- {
		pushExécutionunsignedinteger32(&mémoire_de_pile, argumentpointers[i])
	}
	pushExécutionunsignedinteger32(&mémoire_de_pile, arguments_2.nombre)
	processeur.Esp = mémoire_de_pile
	processeur.Ebp = 0
	return 0
}

func fermersurExécution(processus *processusélément) {
	if processus == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if processus.fds[fd].utilisé && (processus.fds[fd].fdAttributs&fdcloexec) != 0 {
			fermerprocessusfd(processus, fd)
		}
	}
}

func sysexecve(processeur *TcpuÉtat, cHEMINaddress uint32) int32 {
	if cHEMINaddress == 0 {
		return Efault
	}
	var arguments_2 exécutionvector
	var environment exécutionvector
	if rÉSULTAT := copierExécutionvector(processeur.Ecx, &arguments_2); rÉSULTAT < 0 {
		return rÉSULTAT
	}
	if rÉSULTAT := copierExécutionvector(processeur.Edx, &environment); rÉSULTAT < 0 {
		return rÉSULTAT
	}
	nomlen, nom := copierCHEMIN(cHEMINaddress)
	if nomlen == 0 {
		return Enoent
	}
	taille := fichierTaille(nom[:nomlen])
	if taille == 0 {
		return Enoent
	}
	mémoiregestionnaire := &mem.TMémoiregestionnaire{}
	fichierPointeur := mémoiregestionnaire.Allouer_la_mémoire(taille)
	if fichierPointeur == nil {
		return Einval
	}
	données := GetOctetsdePointeur(uintptr(fichierPointeur), int(taille), int(taille))
	lirefichier(nom[:nomlen], données)
	if taille < 52 || données[0] != 0x7F || données[1] != 'E' || données[2] != 'L' || données[3] != 'F' {
		mémoiregestionnaire.Libre(fichierPointeur)
		return Enoexec
	}
	loader := Elf{}
	élément := loader.Getélément(données)
	loader.Parse(données, getcr3())
	mémoiregestionnaire.Libre(fichierPointeur)
	if rÉSULTAT := setupExécutionstack(processeur, &arguments_2, &environment); rÉSULTAT < 0 {
		return rÉSULTAT
	}
	fermersurExécution(ensureCouranteprocessus())
	processeur.Eip = élément
	processeur.Eax = 0
	return 0
}

func sysfork(processeur *TcpuÉtat) int32 {
	parentpid := Courantepid()
	if ensureCouranteprocessus() == nil {
		return Enfile
	}
	pid := allocateprocessus(parentpid)
	if pid == 0 {
		return Einval
	}
	mémoiregestionnaire := &mem.TMémoiregestionnaire{}
	filExécutionPointeur := mémoiregestionnaire.Allouer_la_mémoire(uint32(Sizeof(TFilExécution{})))
	stackPointeur := mémoiregestionnaire.Allouer_la_mémoire(FilExécutionstackTaille)
	enfantpagerépertoire := CloneaddressEspacecow(getcr3())
	if filExécutionPointeur == nil || stackPointeur == nil || enfantpagerépertoire == 0 {
		abandonnerprocessus(pid)
		return Einval
	}
	enfant := (*TFilExécution)(filExécutionPointeur)
	enfant.Stack = uint32(uintptr(stackPointeur))
	enfant.ProcesseurÉtat = (*TcpuÉtat)(Pointer(uintptr(stackPointeur) + FilExécutionstackTaille - Sizeof(TcpuÉtat{})))
	*enfant.ProcesseurÉtat = *processeur
	enfant.ProcesseurÉtat.Eax = 0
	enfant.Utilisateurstack_2 = processeur.Esp
	enfant.UtilisateurstackTaille_2 = 0
	enfant.Pid = pid
	enfant.Parentpid = parentpid
	enfant.Pagerépertoireélément = enfantpagerépertoire
	enfant.FilExécutionÉtat = Prêt
	enfant.FpuDécalage = 0xffffffff
	enfant.Isnoyau = false
	AjouterrunnablefilExécution(enfant)
	return int32(pid)
}

func sysQuitter(état uint32) {
	pid := Courantepid()
	for i := 0; i < len(processusTableau); i++ {
		if processusTableau[i].utilisé && processusTableau[i].pid == pid {
			fermerToutprocessusfds(&processusTableau[i])
			processusTableau[i].fermé = true
			processusTableau[i].état = (état & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, étataddress uint32, options uint32) int32 {
	if (options & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Courantepid()
	foundenfant := false
	for i := 0; i < len(processusTableau); i++ {
		p := &processusTableau[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.utilisé && matches && p.parent == parentpid {
			foundenfant = true
			if p.fermé {
				if étataddress != 0 {
					*(*uint32)(Pointer(uintptr(étataddress))) = p.état
				}
				enfantpid := p.pid
				*p = processusélément{}
				return int32(enfantpid)
			}
		}
	}
	if !foundenfant {
		return Echild
	}

	if (options & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocessus(parent uint32) uint32 {
	parentprocessus := rechercherprocessus(parent)
	pid := Allocatepid()
	for i := 0; i < len(processusTableau); i++ {
		if !processusTableau[i].utilisé {
			processusTableau[i] = processusélément{
				utilisé:	true,
				pid:		pid,
				parent:		parent,
				programmebreak:	utilisateurheapbase,
			}
			if parentprocessus != nil {
				processusTableau[i].programmebreak = parentprocessus.programmebreak
				for fd := 0; fd < maxfd; fd++ {
					if parentprocessus.fds[fd].utilisé {
						processusTableau[i].fds[fd] = parentprocessus.fds[fd]
						description := parentprocessus.fds[fd].description
						if description >= 0 && description < maxouvrirFICHIERS {
							ouvrirfichierTableau[description].refs++
						}
					}
				}
			} else {
				initializeprocessusfds(&processusTableau[i])
			}
			return pid
		}
	}
	return 0
}

func fermerToutprocessusfds(processus *processusélément) {
	if processus == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if processus.fds[fd].utilisé {
			fermerprocessusfd(processus, fd)
		}
	}
}

func abandonnerprocessus(pid uint32) {
	processus := rechercherprocessus(pid)
	if processus == nil {
		return
	}
	fermerToutprocessusfds(processus)
	*processus = processusélément{}
}

func copierCHEMIN(cHEMINaddress uint32) (uint32, [12]byte) {
	var nom [12]byte
	if cHEMINaddress == 0 {
		return 0, nom
	}
	raw := GetOctetsdePointeur(uintptr(cHEMINaddress), 64, 64)
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
		nom[n] = c
		n++
	}
	return n, nom
}

func fichierTaille(nomdefichier []byte) uint32 {
	var ata0s = TAvancéTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTableau{}
	partition.Lirepartition(&ata0s)

	bios := TParamètres_du_système_de_fichiers32{}
	taille := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomdefichier)
	ata0s.Flush()
	return taille
}

func lirefichier(nomdefichier []byte, données []byte) {
	var ata0s = TAvancéTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTableau{}
	partition.Lirepartition(&ata0s)

	bios := TParamètres_du_système_de_fichiers32{}
	bios.Lire(&ata0s, partition.Mbr.Primarypartition[0], nomdefichier, données)
	ata0s.Flush()
}

func getcr3() uint32
