package järjestelmäcall

import . "unsafe"

import . "keskeytys"
import . "konsoli"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "tiedostoJärjestelmä/msdospartition"
import . "tiedostoJärjestelmä/fat"
import . "tiedostoJärjestelmä/suoritettava_ja_linkitettävä_muoto"
import mem "muistimanager"
import . "paging"
import . "portti"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuaalinenMuisti"

var konsoli_2 = TKonsoli{}

type TSyscall struct {
	TKeskeytyshandler
}

const (
	SysSulje_2	uint32	= 1
	Sysfork		uint32	= 2
	SysLuku		uint32	= 3
	SysKirjoitus	uint32	= 4
	SysAvaa		uint32	= 5
	SysSulje	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syspääsy	uint32	= 33
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
	SysrtSulje	uint32	= 252

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
	maksimifd			= 32
	maksimiAvaaTiedostot		= 128
)

type fdhakusana struct {
	käyttö	bool
	kuvaus	int32
	fdLiput	uint32
}

type avaaTiedostoKuvaus struct {
	käyttö		bool
	refs		uint32
	laji		uint32
	liput		uint32
	sijainti	uint32
	koko		uint32
	nimi		[12]byte
	nimilen		uint32
	aux		uint32
}

const (
	fdLajiEimitään		uint32	= 0
	fdLajifat		uint32	= 1
	fdLajistdin		uint32	= 2
	fdLajiKonsoli		uint32	= 3
	fdLajiJuuriKansio	uint32	= 4
	fdLajiPistoke		uint32	= 5

	oLukuonly	uint32	= 0
	oKirjoitusonly	uint32	= 1
	oLukuKirjoitus	uint32	= 2
	oLuo		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oKansio		uint32	= 0x10000

	seekaseta		uint32	= 0
	seekNykyinen		uint32	= 1
	seekLoppuajankohta	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fasetafd	uint32	= 2
	fgetfl		uint32	= 3
	fasetafl	uint32	= 4
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
	maksimisockets		= 32
	maksimiPistokepakettia	= 8
	maksimidatagramKoko	= 512
)

type pistokeaddressipv4 struct {
	Family	uint16
	Portti	uint16
	Address	uint32
	Zero	[8]byte
}

type pistokepacket struct {
	käyttö	bool
	koko	uint32
	lähde	pistokeaddressipv4
	data	[maksimidatagramKoko]byte
}

type paikallinendatagramPistoke struct {
	käyttö		bool
	bound		bool
	connected	bool
	paikallinen	pistokeaddressipv4
	etä		pistokeaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	pakettia	[maksimiPistokepakettia]pistokepacket
}

type posixstat struct {
	Laite		uint32
	Ino		uint32
	TILA		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Koko_2		int32
	Blksize		int32
	Lohko		int32
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
	Versio		[65]byte
	Machine		[65]byte
}

const (
	maksimiSuoritusvectorhakusana	= 16
	maksimiSuoritusMerkkijonoKesto	= 63
)

type suoritusvector struct {
	count	uint32
	lengths	[maksimiSuoritusvectorhakusana]uint32
	arvot	[maksimiSuoritusvectorhakusana][maksimiSuoritusMerkkijonoKesto + 1]byte
}

type prosessihakusana struct {
	käyttö		bool
	pid		uint32
	vanhempi	uint32
	exited		bool
	tila		uint32
	ohjelmabreak	uint32
	fds		[maksimifd]fdhakusana
}

type merkkijonoheader struct {
	Data	uintptr
	Len	int
}

func syscallVirhe(virhe int32) uint32 {
	return *(*uint32)(Pointer(&virhe))
}

var avaaTiedostoTaulukko [maksimiAvaaTiedostot]avaaTiedostoKuvaus
var prosessiTaulukko [32]prosessihakusana
var paikallinensockets [maksimisockets]paikallinendatagramPistoke
var seuraavaephemeralPortti uint16 = 49152

const (
	käyttäjäheapbase	uint32	= 0x06000000
	käyttäjäheapRajoitus	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLuku uint32
var stdinKirjoitus uint32

func Keskeytys(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysSulje_4(hakemisto uint32) {
	Syscall(SysSulje_2, hakemisto)
}

func SysLuku_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLuku, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysTulostastr(buffer string) {
	h := (*merkkijonoheader)(Pointer(&buffer))
	Syscall(SysKirjoitus, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysTulostaunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysKirjoitus, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysAvaa_2(polku uintptr, liput uint32, tILA uint32) int32 {
	return int32(Syscall(SysAvaa, uint32(polku), liput, tILA))
}

func SysSulje_3(fd uint32) int32 {
	return int32(Syscall(SysSulje, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametrit_3 ...uint32) uint32 {

	l := len(parametrit_3)
	switch l {
	case 1:
		return Keskeytys(parametrit_3[0], 0, 0, 0, 0, 0)
	case 2:
		return Keskeytys(parametrit_3[0], parametrit_3[1], 0, 0, 0, 0)
	case 3:
		return Keskeytys(parametrit_3[0], parametrit_3[1], parametrit_3[2], 0, 0, 0)
	case 4:
		return Keskeytys(parametrit_3[0], parametrit_3[1], parametrit_3[2], parametrit_3[3], 0, 0)
	case 5:
		return Keskeytys(parametrit_3[0], parametrit_3[1], parametrit_3[2], parametrit_3[3], parametrit_3[4], 0)
	case 6:
		return Keskeytys(parametrit_3[0], parametrit_3[1], parametrit_3[2], parametrit_3[3], parametrit_3[4], parametrit_3[5])
	default:
		return syscallVirhe(Enosys)
	}
}

func (itse *TSyscall) Init(manager *TKeskeytysmanager) {
	initTiedostodescriptor()

	keskeytyshandler = kahvaKeskeytys

	var address uintptr
	address = uintptr(Pointer(&keskeytyshandler))

	itse.TKeskeytyshandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var keskeytyshandler func(uint32) uint32

func kahvaKeskeytys(esp uint32) uint32 {
	var cpu = (*TcpuTila)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysSulje_2:
		sysSulje_2(cpu.Ebx)
		return uint32(uintptr(Pointer(PysäytäNykyinenthread(cpu))))
	case SysrtSulje:
		sysSulje_2(cpu.Ebx)
		return uint32(uintptr(Pointer(PysäytäNykyinenthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLuku:
		cpu.Eax = uint32(sysLuku(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysKirjoitus:
		cpu.Eax = uint32(sysKirjoitus(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysAvaa:
		cpu.Eax = uint32(sysAvaa(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysAvaa(cpu.Ebx, oLuo|oKirjoitusonly|otruncate, cpu.Ecx))
		return esp
	case SysSulje:
		cpu.Eax = uint32(sysSulje(int32(cpu.Ebx)))
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
		cpu.Eax = Nykyinenpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Nykyinenvanhempipid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Syspääsy:
		cpu.Eax = uint32(syspääsy(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysPistokecall(cpu.Ebx, cpu.Ecx))
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
		konsoli_2.MUnsignedinteger32Tulosta(cpu.Ebx)
		return esp

	default:
		konsoli_2.MTulostaxy(([]byte)("sys["), 1, 23)
		konsoli_2.MUnsignedinteger32Tulosta(esp)
		konsoli_2.MTulosta(([]byte)(":"))
		konsoli_2.MUnsignedinteger32Tulosta(cpu.Eax)
		konsoli_2.MTulosta(([]byte)(":"))
		konsoli_2.MUnsignedinteger32Tulosta(cpu.Ebx)
		konsoli_2.MTulosta(([]byte)(":"))
		konsoli_2.MUnsignedinteger32Tulosta(cpu.Ecx)
		konsoli_2.MTulosta(([]byte)(":"))
		konsoli_2.MUnsignedinteger32Tulosta(cpu.Edx)
		konsoli_2.MTulosta(([]byte)("]"))
		cpu.Eax = syscallVirhe(Enosys)
		return esp
	}

	return esp
}

func initTiedostodescriptor() {
	for i := 0; i < maksimiAvaaTiedostot; i++ {
		avaaTiedostoTaulukko[i] = avaaTiedostoKuvaus{}
	}
	for i := 0; i < len(prosessiTaulukko); i++ {
		prosessiTaulukko[i] = prosessihakusana{}
	}
	for i := 0; i < len(paikallinensockets); i++ {
		paikallinensockets[i] = paikallinendatagramPistoke{}
	}
	seuraavaephemeralPortti = 49152
	avaaTiedostoTaulukko[0] = avaaTiedostoKuvaus{käyttö: true, laji: fdLajistdin, liput: oLukuonly}
	avaaTiedostoTaulukko[1] = avaaTiedostoKuvaus{käyttö: true, laji: fdLajiKonsoli, liput: oKirjoitusonly}
	avaaTiedostoTaulukko[2] = avaaTiedostoKuvaus{käyttö: true, laji: fdLajiKonsoli, liput: oKirjoitusonly}
}

func etsiProsessi(pid uint32) *prosessihakusana {
	for i := 0; i < len(prosessiTaulukko); i++ {
		if prosessiTaulukko[i].käyttö && prosessiTaulukko[i].pid == pid {
			return &prosessiTaulukko[i]
		}
	}
	return nil
}

func initializeProsessifds(prosessi *prosessihakusana) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		prosessi.fds[fd] = fdhakusana{käyttö: true, kuvaus: fd}
		avaaTiedostoTaulukko[fd].refs++
	}
}

func ensureNykyinenProsessi() *prosessihakusana {
	pid := Nykyinenpid()
	if prosessi := etsiProsessi(pid); prosessi != nil {
		return prosessi
	}
	for i := 0; i < len(prosessiTaulukko); i++ {
		if !prosessiTaulukko[i].käyttö {
			prosessiTaulukko[i] = prosessihakusana{
				käyttö:		true,
				pid:		pid,
				vanhempi:	Nykyinenvanhempipid(),
				ohjelmabreak:	käyttäjäheapbase,
			}
			initializeProsessifds(&prosessiTaulukko[i])
			return &prosessiTaulukko[i]
		}
	}
	return nil
}

func getAvaaTiedostofor(prosessi *prosessihakusana, fd int32) *avaaTiedostoKuvaus {
	if prosessi == nil || fd < 0 || fd >= maksimifd || !prosessi.fds[fd].käyttö {
		return nil
	}
	kuvaus := prosessi.fds[fd].kuvaus
	if kuvaus < 0 || kuvaus >= maksimiAvaaTiedostot || !avaaTiedostoTaulukko[kuvaus].käyttö {
		return nil
	}
	return &avaaTiedostoTaulukko[kuvaus]
}

func getAvaaTiedosto(fd int32) *avaaTiedostoKuvaus {
	return getAvaaTiedostofor(ensureNykyinenProsessi(), fd)
}

func allocateAvaaTiedosto() int32 {
	for i := int32(3); i < maksimiAvaaTiedostot; i++ {
		if !avaaTiedostoTaulukko[i].käyttö {
			avaaTiedostoTaulukko[i] = avaaTiedostoKuvaus{käyttö: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(prosessi *prosessihakusana, kuvaus int32, minimi int32) int32 {
	if prosessi == nil {
		return Enfile
	}
	if minimi < 0 || minimi >= maksimifd {
		return Einval
	}
	for fd := minimi; fd < maksimifd; fd++ {
		if !prosessi.fds[fd].käyttö {
			prosessi.fds[fd] = fdhakusana{käyttö: true, kuvaus: kuvaus}
			return fd
		}
	}
	return Emfile
}

func releaseAvaaTiedosto(kuvaus int32) {
	if kuvaus < 0 || kuvaus >= maksimiAvaaTiedostot {
		return
	}
	hakusana := &avaaTiedostoTaulukko[kuvaus]
	if hakusana.refs > 0 {
		hakusana.refs--
	}

	if hakusana.refs == 0 && kuvaus > stderrfd {
		if hakusana.laji == fdLajiPistoke && hakusana.aux < maksimisockets {
			paikallinensockets[hakusana.aux] = paikallinendatagramPistoke{}
		}
		*hakusana = avaaTiedostoKuvaus{}
	}
}

func suljeProsessifd(prosessi *prosessihakusana, fd int32) int32 {
	if prosessi == nil || getAvaaTiedostofor(prosessi, fd) == nil {
		return Ebadf
	}
	kuvaus := prosessi.fds[fd].kuvaus
	prosessi.fds[fd] = fdhakusana{}
	releaseAvaaTiedosto(kuvaus)
	return 0
}

func sysKirjoitus(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	hakusana := getAvaaTiedosto(fd)
	if hakusana == nil {
		return Ebadf
	}
	if hakusana.laji != fdLajiKonsoli {
		if hakusana.laji == fdLajiPistoke {
			return pistokeLähetäto(fd, address, count, 0, 0)
		}
		if hakusana.laji == fdLajifat || hakusana.laji == fdLajiJuuriKansio {
			return Erofs
		}
		return Ebadf
	}
	buffer := GettavualähteestäOsoitin(uintptr(address), int(count), int(count))
	konsoli_2.MTulosta(buffer)
	return int32(count)
}

func sysLuku(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	hakusana := getAvaaTiedosto(fd)
	if hakusana == nil {
		return Ebadf
	}
	if hakusana.laji == fdLajistdin {
		return lukustdin(address, count)
	}
	if hakusana.laji == fdLajiJuuriKansio {
		return Eisdir
	}
	if hakusana.laji == fdLajiPistoke {
		return pistokereceivelähteestä(fd, address, count, 0, 0)
	}
	if hakusana.laji != fdLajifat {
		return Ebadf
	}
	if hakusana.sijainti >= hakusana.koko {
		return 0
	}
	remaining := hakusana.koko - hakusana.sijainti
	if count > remaining {
		count = remaining
	}
	buffer := GettavualähteestäOsoitin(uintptr(address), int(count), int(count))
	return lukuvfsTiedosto(hakusana, buffer, count)
}

func sysAvaa(polkuaddress uint32, liput uint32, tILA uint32) int32 {
	_ = tILA
	if polkuaddress == 0 {
		return Efault
	}
	pääsyTILA := liput & 3
	if pääsyTILA == oKirjoitusonly || pääsyTILA == oLukuKirjoitus || (liput&(oLuo|otruncate|oappend)) != 0 {
		return Erofs
	}

	prosessi := ensureNykyinenProsessi()
	if prosessi == nil {
		return Enfile
	}
	kuvaus := allocateAvaaTiedosto()
	if kuvaus < 0 {
		return kuvaus
	}
	hakusana := &avaaTiedostoTaulukko[kuvaus]
	hakusana.liput = liput
	if isJuuriPolku(polkuaddress) {
		hakusana.laji = fdLajiJuuriKansio
		hakusana.koko = 0
	} else {
		nimilen, nimi := kopioiPolku(polkuaddress)
		if nimilen == 0 {
			*hakusana = avaaTiedostoKuvaus{}
			return Enoent
		}
		koko := tiedostoKoko(nimi[:nimilen])
		if koko == 0 {
			*hakusana = avaaTiedostoKuvaus{}
			return Enoent
		}
		if (liput & oKansio) != 0 {
			*hakusana = avaaTiedostoKuvaus{}
			return Enotdir
		}
		hakusana.laji = fdLajifat
		hakusana.koko = koko
		hakusana.nimilen = nimilen
		hakusana.nimi = nimi
	}

	fd := allocatefd(prosessi, kuvaus, 3)
	if fd < 0 {
		*hakusana = avaaTiedostoKuvaus{}
		return fd
	}
	return fd
}

func sysSulje(fd int32) int32 {
	return suljeProsessifd(ensureNykyinenProsessi(), fd)
}

func sysdup(fd int32, minimi int32) int32 {
	prosessi := ensureNykyinenProsessi()
	hakusana := getAvaaTiedostofor(prosessi, fd)
	if hakusana == nil {
		return Ebadf
	}
	uusifd := allocatefd(prosessi, prosessi.fds[fd].kuvaus, minimi)
	if uusifd >= 0 {
		hakusana.refs++
	}
	return uusifd
}

func sysdup2(oldfd int32, uusifd int32) int32 {
	prosessi := ensureNykyinenProsessi()
	hakusana := getAvaaTiedostofor(prosessi, oldfd)
	if hakusana == nil {
		return Ebadf
	}
	if uusifd < 0 || uusifd >= maksimifd {
		return Ebadf
	}
	if oldfd == uusifd {
		return uusifd
	}
	if prosessi.fds[uusifd].käyttö {
		suljeProsessifd(prosessi, uusifd)
	}
	prosessi.fds[uusifd] = fdhakusana{käyttö: true, kuvaus: prosessi.fds[oldfd].kuvaus}
	hakusana.refs++
	return uusifd
}

func sysfcntl(fd int32, komento uint32, argument uint32) int32 {
	prosessi := ensureNykyinenProsessi()
	hakusana := getAvaaTiedostofor(prosessi, fd)
	if hakusana == nil {
		return Ebadf
	}
	switch komento {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(prosessi.fds[fd].fdLiput)
	case fasetafd:
		prosessi.fds[fd].fdLiput = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(hakusana.liput)
	case fasetafl:
		hakusana.liput = (hakusana.liput & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	hakusana := getAvaaTiedosto(fd)
	if hakusana == nil {
		return Ebadf
	}
	if hakusana.laji != fdLajifat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekaseta:
		base = 0
	case seekNykyinen:
		base = int64(hakusana.sijainti)
	case seekLoppuajankohta:
		base = int64(hakusana.koko)
	default:
		return Einval
	}
	sijainti_2 := base + int64(offset)
	if sijainti_2 < 0 || sijainti_2 > 0x7FFFFFFF {
		return Einval
	}
	hakusana.sijainti = uint32(sijainti_2)
	return int32(hakusana.sijainti)
}

func lukuvfsTiedosto(hakusana *avaaTiedostoKuvaus, kohde_2 []byte, count uint32) int32 {
	muistimanager := &mem.TMuistimanager{}
	tmpOsoitin := muistimanager.Varaa_muistia(hakusana.koko)
	if tmpOsoitin == nil {
		return Einval
	}
	tmp := GettavualähteestäOsoitin(uintptr(tmpOsoitin), int(hakusana.koko), int(hakusana.koko))
	lukuTiedosto(hakusana.nimi[:hakusana.nimilen], tmp)
	copy(kohde_2[:count], tmp[hakusana.sijainti:hakusana.sijainti+count])
	hakusana.sijainti += count
	muistimanager.Vapaana(tmpOsoitin)
	return int32(count)
}

func isJuuriPolku(polkuaddress uint32) bool {
	if polkuaddress == 0 {
		return false
	}
	polku := GettavualähteestäOsoitin(uintptr(polkuaddress), 4, 4)
	if polku[0] == '/' && polku[1] == 0 {
		return true
	}
	if polku[0] == '.' && polku[1] == 0 {
		return true
	}
	if polku[0] == '/' && polku[1] == '.' && polku[2] == 0 {
		return true
	}
	return false
}

func syspääsy(polkuaddress uint32, tILA uint32) int32 {
	if polkuaddress == 0 {
		return Efault
	}
	if (tILA & ^uint32(7)) != 0 {
		return Einval
	}
	isJuuri := isJuuriPolku(polkuaddress)
	exists := isJuuri
	if !exists {
		nimilen, nimi := kopioiPolku(polkuaddress)
		exists = nimilen != 0 && tiedostoKoko(nimi[:nimilen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (tILA & 2) != 0 {
		return Eacces
	}

	if (tILA&1) != 0 && !isJuuri {
		return Eacces
	}
	return 0
}

func syschdir(polkuaddress uint32) int32 {
	if polkuaddress == 0 {
		return Efault
	}
	if !isJuuriPolku(polkuaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, koko uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if koko < 2 {
		return Erange
	}
	buffer_2 := GettavualähteestäOsoitin(uintptr(bufferaddress), int(koko), int(koko))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, tILA uint32, koko uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Laite = 1
	stat.Ino = inode
	stat.TILA = tILA
	stat.Nlink = 1
	stat.Koko_2 = int32(koko)
	stat.Blksize = 512
	stat.Lohko = int32((koko + 511) / 512)
	return 0
}

func sysstat(polkuaddress uint32, stataddress uint32) int32 {
	if polkuaddress == 0 {
		return Efault
	}
	if isJuuriPolku(polkuaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nimilen, nimi := kopioiPolku(polkuaddress)
	if nimilen == 0 {
		return Enoent
	}
	koko := tiedostoKoko(nimi[:nimilen])
	if koko == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nimilen; i++ {
		inode = inode*33 + uint32(nimi[i])
	}
	return fillposixstat(stataddress, sifreg|0444, koko, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	hakusana := getAvaaTiedosto(fd)
	if hakusana == nil {
		return Ebadf
	}
	switch hakusana.laji {
	case fdLajistdin, fdLajiKonsoli:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdLajiJuuriKansio:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdLajifat:
		return fillposixstat(stataddress, sifreg|0444, hakusana.koko, uint32(fd+2))
	case fdLajiPistoke:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getAvaaTiedosto(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	prosessi := ensureNykyinenProsessi()
	if prosessi == nil {
		return 0
	}
	if prosessi.ohjelmabreak == 0 {
		prosessi.ohjelmabreak = käyttäjäheapbase
	}
	if address_2 == 0 {
		return prosessi.ohjelmabreak
	}
	if address_2 < käyttäjäheapbase || address_2 > käyttäjäheapRajoitus {
		return prosessi.ohjelmabreak
	}
	prosessi.ohjelmabreak = address_2
	return prosessi.ohjelmabreak
}

func kopioiutskenttä(kohde *[65]byte, arvo string) {
	rajoitus := len(arvo)
	if rajoitus > 64 {
		rajoitus = 64
	}
	for i := 0; i < rajoitus; i++ {
		kohde[i] = arvo[i]
	}
	kohde[rajoitus] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nimi := (*posixutsname)(Pointer(uintptr(address_2)))
	*nimi = posixutsname{}
	kopioiutskenttä(&nimi.Sysname, "EngOS")
	kopioiutskenttä(&nimi.Nodename, "engos")
	kopioiutskenttä(&nimi.Release, "0.1-posix")
	kopioiutskenttä(&nimi.Versio, "POSIX.1-2017 phase 1")
	kopioiutskenttä(&nimi.Machine, "i386")
	return 0
}

func swapunsignedinteger16(arvo uint16) uint16 {
	return (arvo << 8) | (arvo >> 8)
}

func pistokecallargument(parametrit_2 uint32, hakemisto uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(parametrit_2 + hakemisto*4)))
}

func pistokeforfd(fd int32) (*paikallinendatagramPistoke, int32) {
	hakusana := getAvaaTiedosto(fd)
	if hakusana == nil || hakusana.laji != fdLajiPistoke || hakusana.aux >= maksimisockets {
		return nil, Ebadf
	}
	pistoke := &paikallinensockets[hakusana.aux]
	if !pistoke.käyttö {
		return nil, Ebadf
	}
	return pistoke, 0
}

func allocatePistoke(verkkoalue uint32, pistokeTyyppi uint32, protocol uint32) int32 {
	if verkkoalue != afinet {
		return Eafnosupport
	}
	if pistokeTyyppi != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	prosessi := ensureNykyinenProsessi()
	if prosessi == nil {
		return Enfile
	}
	pistokeHakemisto := -1
	for i := 0; i < maksimisockets; i++ {
		if !paikallinensockets[i].käyttö {
			pistokeHakemisto = i
			break
		}
	}
	if pistokeHakemisto < 0 {
		return Enfile
	}
	kuvaus := allocateAvaaTiedosto()
	if kuvaus < 0 {
		return kuvaus
	}
	paikallinensockets[pistokeHakemisto] = paikallinendatagramPistoke{käyttö: true}
	hakusana := &avaaTiedostoTaulukko[kuvaus]
	hakusana.laji = fdLajiPistoke
	hakusana.liput = oLukuKirjoitus
	hakusana.aux = uint32(pistokeHakemisto)
	fd := allocatefd(prosessi, kuvaus, 3)
	if fd < 0 {
		paikallinensockets[pistokeHakemisto] = paikallinendatagramPistoke{}
		*hakusana = avaaTiedostoKuvaus{}
		return fd
	}
	return fd
}

func pistokeaddress(address_2 uint32, kesto uint32) (*pistokeaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if kesto < 16 {
		return nil, Einval
	}
	tULOS := (*pistokeaddressipv4)(Pointer(uintptr(address_2)))
	if tULOS.Family != afinet {
		return nil, Eafnosupport
	}
	return tULOS, 0
}

func porttiSaapuvaKäytä(portti uint16, except *paikallinendatagramPistoke) bool {
	for i := 0; i < maksimisockets; i++ {
		pistoke := &paikallinensockets[i]
		if pistoke != except && pistoke.käyttö && pistoke.bound && pistoke.paikallinen.Portti == portti {
			return true
		}
	}
	return false
}

func bindephemeral(pistoke *paikallinendatagramPistoke) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		portti := swapunsignedinteger16(seuraavaephemeralPortti)
		seuraavaephemeralPortti++
		if seuraavaephemeralPortti < 49152 {
			seuraavaephemeralPortti = 49152
		}
		if !porttiSaapuvaKäytä(portti, pistoke) {
			pistoke.paikallinen = pistokeaddressipv4{Family: afinet, Portti: portti, Address: 0x0100007F}
			pistoke.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func pistokebind(fd int32, address_2 uint32, kesto uint32) int32 {
	pistoke, virhe := pistokeforfd(fd)
	if virhe != 0 {
		return virhe
	}
	requested, virhe := pistokeaddress(address_2, kesto)
	if virhe != 0 {
		return virhe
	}
	if pistoke.bound {
		return Einval
	}
	if requested.Portti == 0 {
		return bindephemeral(pistoke)
	}
	if porttiSaapuvaKäytä(requested.Portti, pistoke) {
		return Eaddrinuse
	}
	pistoke.paikallinen = *requested
	pistoke.bound = true
	return 0
}

func pistokeYhdistä(fd int32, address_2 uint32, kesto uint32) int32 {
	pistoke, virhe := pistokeforfd(fd)
	if virhe != 0 {
		return virhe
	}
	etä, virhe := pistokeaddress(address_2, kesto)
	if virhe != 0 {
		return virhe
	}
	if !pistoke.bound {
		if virhe := bindephemeral(pistoke); virhe != 0 {
			return virhe
		}
	}
	pistoke.etä = *etä
	pistoke.connected = true
	return 0
}

func pistokeLähetäto(fd int32, bufferaddress_2 uint32, kesto uint32, kohdeaddress uint32, kohdeKesto uint32) int32 {
	pistoke, virhe := pistokeforfd(fd)
	if virhe != 0 {
		return virhe
	}
	if kesto > maksimidatagramKoko {
		return Emsgsize
	}
	if kesto != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var kohde pistokeaddressipv4
	if kohdeaddress != 0 {
		address_2, addressVirhe := pistokeaddress(kohdeaddress, kohdeKesto)
		if addressVirhe != 0 {
			return addressVirhe
		}
		kohde = *address_2
	} else {
		if !pistoke.connected {
			return Enotconn
		}
		kohde = pistoke.etä
	}
	if !pistoke.bound {
		if bindVirhe := bindephemeral(pistoke); bindVirhe != 0 {
			return bindVirhe
		}
	}
	var receiver *paikallinendatagramPistoke
	for i := 0; i < maksimisockets; i++ {
		candidate := &paikallinensockets[i]
		if candidate.käyttö && candidate.bound && candidate.paikallinen.Portti == kohde.Portti &&
			(candidate.paikallinen.Address == 0 || candidate.paikallinen.Address == kohde.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksimiPistokepakettia {
		return Eagain
	}
	packet := &receiver.pakettia[receiver.tail]
	*packet = pistokepacket{käyttö: true, koko: kesto, lähde: pistoke.paikallinen}
	if kesto != 0 {
		lähde := GettavualähteestäOsoitin(uintptr(bufferaddress_2), int(kesto), int(kesto))
		copy(packet.data[:kesto], lähde)
	}
	receiver.tail = (receiver.tail + 1) % maksimiPistokepakettia
	receiver.count++
	return int32(kesto)
}

func pistokereceivelähteestä(fd int32, bufferaddress_2 uint32, kesto uint32, lähdeaddress uint32, lähdeKestoaddress uint32) int32 {
	pistoke, virhe := pistokeforfd(fd)
	if virhe != 0 {
		return virhe
	}
	if kesto != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if pistoke.count == 0 {
		return Eagain
	}
	packet := &pistoke.pakettia[pistoke.head]
	kopioiKesto := packet.koko
	if kopioiKesto > kesto {
		kopioiKesto = kesto
	}
	if kopioiKesto != 0 {
		kohde := GettavualähteestäOsoitin(uintptr(bufferaddress_2), int(kopioiKesto), int(kopioiKesto))
		copy(kohde, packet.data[:kopioiKesto])
	}
	if lähdeaddress != 0 {
		if lähdeKestoaddress == 0 {
			return Efault
		}
		providedKesto := (*uint32)(Pointer(uintptr(lähdeKestoaddress)))
		if *providedKesto >= 16 {
			*(*pistokeaddressipv4)(Pointer(uintptr(lähdeaddress))) = packet.lähde
		}
		*providedKesto = 16
	}
	*packet = pistokepacket{}
	pistoke.head = (pistoke.head + 1) % maksimiPistokepakettia
	pistoke.count--
	return int32(kopioiKesto)
}

func kopioiPistokeNimi(fd int32, address_2 uint32, kestoaddress uint32, peer bool) int32 {
	pistoke, virhe := pistokeforfd(fd)
	if virhe != 0 {
		return virhe
	}
	if address_2 == 0 || kestoaddress == 0 {
		return Efault
	}
	kesto := (*uint32)(Pointer(uintptr(kestoaddress)))
	if *kesto < 16 {
		*kesto = 16
		return Einval
	}
	if peer {
		if !pistoke.connected {
			return Enotconn
		}
		*(*pistokeaddressipv4)(Pointer(uintptr(address_2))) = pistoke.etä
	} else {
		if !pistoke.bound {
			if bindVirhe := bindephemeral(pistoke); bindVirhe != 0 {
				return bindVirhe
			}
		}
		*(*pistokeaddressipv4)(Pointer(uintptr(address_2))) = pistoke.paikallinen
	}
	*kesto = 16
	return 0
}

func sysPistokecall(call uint32, parametrit_2 uint32) int32 {
	if parametrit_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatePistoke(pistokecallargument(parametrit_2, 0), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2))
	case 2:
		return pistokebind(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2))
	case 3:
		return pistokeYhdistä(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopioiPistokeNimi(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2), false)
	case 7:
		return kopioiPistokeNimi(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2), true)
	case 9:
		return pistokeLähetäto(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2), 0, 0)
	case 10:
		return pistokereceivelähteestä(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2), 0, 0)
	case 11:
		return pistokeLähetäto(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2), pistokecallargument(parametrit_2, 4), pistokecallargument(parametrit_2, 5))
	case 12:
		return pistokereceivelähteestä(int32(pistokecallargument(parametrit_2, 0)), pistokecallargument(parametrit_2, 1), pistokecallargument(parametrit_2, 2), pistokecallargument(parametrit_2, 4), pistokecallargument(parametrit_2, 5))
	case 13:
		if _, virhe := pistokeforfd(int32(pistokecallargument(parametrit_2, 0))); virhe != 0 {
			return virhe
		}
		return 0
	case 14:
		if _, virhe := pistokeforfd(int32(pistokecallargument(parametrit_2, 0))); virhe != 0 {
			return virhe
		}
		return 0
	}
	return Eopnotsupp
}

func lukustdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GettavualähteestäOsoitin(uintptr(address), int(count), int(count))
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
	seuraava := (stdinKirjoitus + 1) % uint32(len(stdinbuffer))
	if seuraava == stdinLuku {
		return
	}
	stdinbuffer[stdinKirjoitus] = c
	stdinKirjoitus = seuraava
}

func stdingetblocking() byte {
	for stdinLuku == stdinKirjoitus {
		sc := pollNäppäimistöscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLuku]
	stdinLuku = (stdinLuku + 1) % uint32(len(stdinbuffer))
	return c
}

func pollNäppäimistöscancode() byte {
	for (PorttiLukubyte(0x64) & 0x01) == 0 {
	}
	sc := PorttiLukubyte(0x60)
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

func kopioiSuoritusvector(address_2 uint32, tULOS *suoritusvector) int32 {
	*tULOS = suoritusvector{}
	if address_2 == 0 {
		return 0
	}
	for hakemisto := uint32(0); hakemisto < maksimiSuoritusvectorhakusana; hakemisto++ {
		merkkijonoaddress := *(*uint32)(Pointer(uintptr(address_2 + hakemisto*4)))
		if merkkijonoaddress == 0 {
			tULOS.count = hakemisto
			return 0
		}
		terminated := false
		for kesto := uint32(0); kesto <= maksimiSuoritusMerkkijonoKesto; kesto++ {
			arvo := *(*byte)(Pointer(uintptr(merkkijonoaddress + kesto)))
			tULOS.arvot[hakemisto][kesto] = arvo
			if arvo == 0 {
				tULOS.lengths[hakemisto] = kesto
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

func pushSuoritusunsignedinteger32(pinomuisti *uint32, arvo uint32) {
	*pinomuisti -= 4
	*(*uint32)(Pointer(uintptr(*pinomuisti))) = arvo
}

func setupSuoritusstack(cpu *TcpuTila, parametrit_2 *suoritusvector, environment *suoritusvector) int32 {
	const stacktavua uint32 = 4096
	if !MakeAlueYksityinenwritable(getcr3(), KäyttäjästackYlhäällä-stacktavua, stacktavua) {
		return Enomem
	}
	pinomuisti := KäyttäjästackYlhäällä
	var argumentpointers [maksimiSuoritusvectorhakusana]uint32
	var environmentpointers [maksimiSuoritusvectorhakusana]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		kesto := environment.lengths[i] + 1
		pinomuisti -= kesto
		kohde := GettavualähteestäOsoitin(uintptr(pinomuisti), int(kesto), int(kesto))
		copy(kohde, environment.arvot[i][:kesto])
		environmentpointers[i] = pinomuisti
	}
	for i := int(parametrit_2.count) - 1; i >= 0; i-- {
		kesto := parametrit_2.lengths[i] + 1
		pinomuisti -= kesto
		kohde := GettavualähteestäOsoitin(uintptr(pinomuisti), int(kesto), int(kesto))
		copy(kohde, parametrit_2.arvot[i][:kesto])
		argumentpointers[i] = pinomuisti
	}
	pinomuisti &= ^uint32(3)
	pushSuoritusunsignedinteger32(&pinomuisti, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushSuoritusunsignedinteger32(&pinomuisti, environmentpointers[i])
	}
	pushSuoritusunsignedinteger32(&pinomuisti, 0)
	for i := int(parametrit_2.count) - 1; i >= 0; i-- {
		pushSuoritusunsignedinteger32(&pinomuisti, argumentpointers[i])
	}
	pushSuoritusunsignedinteger32(&pinomuisti, parametrit_2.count)
	cpu.Esp = pinomuisti
	cpu.Ebp = 0
	return 0
}

func suljePäälläSuoritus(prosessi *prosessihakusana) {
	if prosessi == nil {
		return
	}
	for fd := int32(0); fd < maksimifd; fd++ {
		if prosessi.fds[fd].käyttö && (prosessi.fds[fd].fdLiput&fdcloexec) != 0 {
			suljeProsessifd(prosessi, fd)
		}
	}
}

func sysexecve(cpu *TcpuTila, polkuaddress uint32) int32 {
	if polkuaddress == 0 {
		return Efault
	}
	var parametrit_2 suoritusvector
	var environment suoritusvector
	if tULOS := kopioiSuoritusvector(cpu.Ecx, &parametrit_2); tULOS < 0 {
		return tULOS
	}
	if tULOS := kopioiSuoritusvector(cpu.Edx, &environment); tULOS < 0 {
		return tULOS
	}
	nimilen, nimi := kopioiPolku(polkuaddress)
	if nimilen == 0 {
		return Enoent
	}
	koko := tiedostoKoko(nimi[:nimilen])
	if koko == 0 {
		return Enoent
	}
	muistimanager := &mem.TMuistimanager{}
	tiedostoOsoitin := muistimanager.Varaa_muistia(koko)
	if tiedostoOsoitin == nil {
		return Einval
	}
	data := GettavualähteestäOsoitin(uintptr(tiedostoOsoitin), int(koko), int(koko))
	lukuTiedosto(nimi[:nimilen], data)
	if koko < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		muistimanager.Vapaana(tiedostoOsoitin)
		return Enoexec
	}
	loader := Elf{}
	hakusana := loader.Gethakusana(data)
	loader.Parse(data, getcr3())
	muistimanager.Vapaana(tiedostoOsoitin)
	if tULOS := setupSuoritusstack(cpu, &parametrit_2, &environment); tULOS < 0 {
		return tULOS
	}
	suljePäälläSuoritus(ensureNykyinenProsessi())
	cpu.Eip = hakusana
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuTila) int32 {
	vanhempipid := Nykyinenpid()
	if ensureNykyinenProsessi() == nil {
		return Enfile
	}
	pid := allocateProsessi(vanhempipid)
	if pid == 0 {
		return Einval
	}
	muistimanager := &mem.TMuistimanager{}
	threadOsoitin := muistimanager.Varaa_muistia(uint32(Sizeof(TThread{})))
	stackOsoitin := muistimanager.Varaa_muistia(ThreadstackKoko)
	lapsiSivuKansio := CloneaddressVälicow(getcr3())
	if threadOsoitin == nil || stackOsoitin == nil || lapsiSivuKansio == 0 {
		hylkääProsessi(pid)
		return Einval
	}
	lapsi := (*TThread)(threadOsoitin)
	lapsi.Stack = uint32(uintptr(stackOsoitin))
	lapsi.CpuTila = (*TcpuTila)(Pointer(uintptr(stackOsoitin) + ThreadstackKoko - Sizeof(TcpuTila{})))
	*lapsi.CpuTila = *cpu
	lapsi.CpuTila.Eax = 0
	lapsi.Käyttäjästack_2 = cpu.Esp
	lapsi.KäyttäjästackKoko_2 = 0
	lapsi.Pid = pid
	lapsi.Vanhempipid = vanhempipid
	lapsi.SivuKansiohakusana = lapsiSivuKansio
	lapsi.ThreadTila = Valmis
	lapsi.Fpuoffset = 0xffffffff
	lapsi.Iskernel = false
	Lisäärunnablethread(lapsi)
	return int32(pid)
}

func sysSulje_2(tila uint32) {
	pid := Nykyinenpid()
	for i := 0; i < len(prosessiTaulukko); i++ {
		if prosessiTaulukko[i].käyttö && prosessiTaulukko[i].pid == pid {
			suljeKaikkiProsessifds(&prosessiTaulukko[i])
			prosessiTaulukko[i].exited = true
			prosessiTaulukko[i].tila = (tila & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, tilaaddress uint32, valinnat uint32) int32 {
	if (valinnat & ^uint32(1)) != 0 {
		return Einval
	}
	vanhempipid := Nykyinenpid()
	foundlapsi := false
	for i := 0; i < len(prosessiTaulukko); i++ {
		p := &prosessiTaulukko[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.käyttö && matches && p.vanhempi == vanhempipid {
			foundlapsi = true
			if p.exited {
				if tilaaddress != 0 {
					*(*uint32)(Pointer(uintptr(tilaaddress))) = p.tila
				}
				lapsipid := p.pid
				*p = prosessihakusana{}
				return int32(lapsipid)
			}
		}
	}
	if !foundlapsi {
		return Echild
	}

	if (valinnat & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProsessi(vanhempi uint32) uint32 {
	vanhempiProsessi := etsiProsessi(vanhempi)
	pid := Allocatepid()
	for i := 0; i < len(prosessiTaulukko); i++ {
		if !prosessiTaulukko[i].käyttö {
			prosessiTaulukko[i] = prosessihakusana{
				käyttö:		true,
				pid:		pid,
				vanhempi:	vanhempi,
				ohjelmabreak:	käyttäjäheapbase,
			}
			if vanhempiProsessi != nil {
				prosessiTaulukko[i].ohjelmabreak = vanhempiProsessi.ohjelmabreak
				for fd := 0; fd < maksimifd; fd++ {
					if vanhempiProsessi.fds[fd].käyttö {
						prosessiTaulukko[i].fds[fd] = vanhempiProsessi.fds[fd]
						kuvaus := vanhempiProsessi.fds[fd].kuvaus
						if kuvaus >= 0 && kuvaus < maksimiAvaaTiedostot {
							avaaTiedostoTaulukko[kuvaus].refs++
						}
					}
				}
			} else {
				initializeProsessifds(&prosessiTaulukko[i])
			}
			return pid
		}
	}
	return 0
}

func suljeKaikkiProsessifds(prosessi *prosessihakusana) {
	if prosessi == nil {
		return
	}
	for fd := int32(0); fd < maksimifd; fd++ {
		if prosessi.fds[fd].käyttö {
			suljeProsessifd(prosessi, fd)
		}
	}
}

func hylkääProsessi(pid uint32) {
	prosessi := etsiProsessi(pid)
	if prosessi == nil {
		return
	}
	suljeKaikkiProsessifds(prosessi)
	*prosessi = prosessihakusana{}
}

func kopioiPolku(polkuaddress uint32) (uint32, [12]byte) {
	var nimi [12]byte
	if polkuaddress == 0 {
		return 0, nimi
	}
	raw := GettavualähteestäOsoitin(uintptr(polkuaddress), 64, 64)
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

func tiedostoKoko(tiedostonimi []byte) uint32 {
	var ata0s = TLisäasetuksetTekniikkaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaulukko{}
	partition.Lukupartition(&ata0s)

	bios := TTiedostojärjestelmän_parametrit32{}
	koko := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], tiedostonimi)
	ata0s.Flush()
	return koko
}

func lukuTiedosto(tiedostonimi []byte, data []byte) {
	var ata0s = TLisäasetuksetTekniikkaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaulukko{}
	partition.Lukupartition(&ata0s)

	bios := TTiedostojärjestelmän_parametrit32{}
	bios.Luku(&ata0s, partition.Mbr.Primarypartition[0], tiedostonimi, data)
	ata0s.Flush()
}

func getcr3() uint32
