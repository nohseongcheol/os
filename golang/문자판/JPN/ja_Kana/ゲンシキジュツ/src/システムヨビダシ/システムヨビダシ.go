/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package システムヨビダシ

import . "unsafe"

import . "ワリコミ"
import . "コンソール"
import . "ハンヨウ"
import . "フクスウタスクカンリ"
import . "ドライバー/ata"
import . "ファイルシステム/msdosクブン"
import . "ファイルシステム/fat"
import . "ファイルシステム/ジッコウレンケツケイシキ"
import mem "メモリカンリシャ"
import . "ページカンリ"
import . "ポート"
import . "タスクカンリ/スケジューラ"
import . "タスクカンリ/スレッド"
import . "カソウメモリ"

var コンソール_2 = Tコンソール{}

type TSyscall struct {
	Tワリコミhandler
}

const (
	Sysシュウリョウ		uint32	= 1
	Sysfork		uint32	= 2
	Sysヨミコミ		uint32	= 3
	Sysカキコミ		uint32	= 4
	Sysヒラク		uint32	= 5
	Sysトジル		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysアクセス		uint32	= 33
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
	Sysrtシュウリョウ		uint32	= 252

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
	サイダイfd			= 32
	サイダイヒラクファイル		= 128
)

type fdentry struct {
	シヨウチュウ	bool
	セツメイ	int32
	fdフラグ	uint32
}

type ヒラクファイルセツメイ struct {
	シヨウチュウ	bool
	refs	uint32
	kind	uint32
	フラグ	uint32
	ハイチ	uint32
	サイズ	uint32
	ナマエ	[12]byte
	ナマエlen	uint32
	aux	uint32
}

const (
	fdkindナシ	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindコンソール	uint32	= 3
	fdkindルートディレクトリ	uint32	= 4
	fdkindソケット	uint32	= 5

	oヨミコミセンヨウ	uint32	= 0
	oカキコミセンヨウ	uint32	= 1
	oヨミコミカキコミ	uint32	= 2
	oサクセイ	uint32	= 0x40
	oキリステ	uint32	= 0x200
	oappend	uint32	= 0x400
	oディレクトリ	uint32	= 0x10000

	seekアリ		uint32	= 0
	seekゲンザイノニチジ	uint32	= 1
	seekブンマツ		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fアリfd		uint32	= 2
	fgetfl		uint32	= 3
	fアリfl		uint32	= 4
	fdcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet		= 2
	sockdatagram	= 2
	ipprotocoludp	= 17
	サイダイsockets	= 32
	サイダイソケットパケット	= 8
	サイダイdatagramサイズ	= 512
)

type ソケットaddressipv4 struct {
	Family	uint16
	Pポート	uint16
	Address	uint32
	Zスウチノ0	[8]byte
}

type ソケットpacket struct {
	シヨウチュウ	bool
	サイズ	uint32
	テンソウモト	ソケットaddressipv4
	データ	[サイダイdatagramサイズ]byte
}

type ローカルdatagramソケット struct {
	シヨウチュウ		bool
	bound		bool
	connected	bool
	ローカル		ソケットaddressipv4
	リモート		ソケットaddressipv4
	head		uint32
	tail		uint32
	カウント		uint32
	パケット		[サイダイソケットパケット]ソケットpacket
}

type posixstat struct {
	Dデバイス		uint32
	Ino		uint32
	Mモード		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sサイズ_2		int32
	Blksize		int32
	Bブロック		int32
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
	Vバージョン		[65]byte
	Machine		[65]byte
}

const (
	サイダイジッコウvectorentry	= 16
	サイダイジッコウブンジレツナガサ	= 63
)

type ジッコウvector struct {
	カウント	uint32
	lengths	[サイダイジッコウvectorentry]uint32
	スウチ	[サイダイジッコウvectorentry][サイダイジッコウブンジレツナガサ + 1]byte
}

type プロセスentry struct {
	シヨウチュウ		bool
	pid		uint32
	parent		uint32
	シュウリョウ		bool
	ジョウタイ		uint32
	プログラムbreak	uint32
	fds		[サイダイfd]fdentry
}

type モジレツヘッダ struct {
	Data	uintptr
	Len	int
}

func syscallエラー(エラー int32) uint32 {
	return *(*uint32)(Pointer(&エラー))
}

var ヒラクファイルtable [サイダイヒラクファイル]ヒラクファイルセツメイ
var プロセスtable [32]プロセスentry
var ローカルsockets [サイダイsockets]ローカルdatagramソケット
var ツギephemeralポート uint16 = 49152

const (
	リヨウシャheapbase	uint32	= 0x06000000
	リヨウシャheapセイゲン	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinヨミコミ uint32
var stdinカキコミ uint32

func Iワリコミ(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysシュウリョウ_2(モクジ uint32) {
	Syscall(Sysシュウリョウ, モクジ)
}

func Sysヨミコミ_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysヨミコミ, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysインサツstr(buffer string) {
	h := (*モジレツヘッダ)(Pointer(&buffer))
	Syscall(Sysカキコミ, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysインサツunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysカキコミ, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysヒラク_2(パス uintptr, フラグ uint32, モード uint32) int32 {
	return int32(Syscall(Sysヒラク, uint32(パス), フラグ, モード))
}

func Sysトジル_2(fd uint32) int32 {
	return int32(Syscall(Sysトジル, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(パラメータ ...uint32) uint32 {

	l := len(パラメータ)
	switch l {
	case 1:
		return Iワリコミ(パラメータ[0], 0, 0, 0, 0, 0)
	case 2:
		return Iワリコミ(パラメータ[0], パラメータ[1], 0, 0, 0, 0)
	case 3:
		return Iワリコミ(パラメータ[0], パラメータ[1], パラメータ[2], 0, 0, 0)
	case 4:
		return Iワリコミ(パラメータ[0], パラメータ[1], パラメータ[2], パラメータ[3], 0, 0)
	case 5:
		return Iワリコミ(パラメータ[0], パラメータ[1], パラメータ[2], パラメータ[3], パラメータ[4], 0)
	case 6:
		return Iワリコミ(パラメータ[0], パラメータ[1], パラメータ[2], パラメータ[3], パラメータ[4], パラメータ[5])
	default:
		return syscallエラー(Enosys)
	}
}

func (self *TSyscall) Init(カンリシャ *Tワリコミカンリシャ) {
	initファイルdescriptor()

	ワリコミhandler = トッテワリコミ

	var address uintptr
	address = uintptr(Pointer(&ワリコミhandler))

	self.Tワリコミhandler.Init(0x80, uintptr(Pointer(カンリシャ)), address)
}

var ワリコミhandler func(uint32) uint32

func トッテワリコミ(esp uint32) uint32 {
	var cpu = (*Tcpuジョウタイ)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysシュウリョウ:
		sysシュウリョウ(cpu.Ebx)
		return uint32(uintptr(Pointer(Sテイシゲンザイノニチジスレッド(cpu))))
	case Sysrtシュウリョウ:
		sysシュウリョウ(cpu.Ebx)
		return uint32(uintptr(Pointer(Sテイシゲンザイノニチジスレッド(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysヨミコミ:
		cpu.Eax = uint32(sysヨミコミ(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysカキコミ:
		cpu.Eax = uint32(sysカキコミ(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysヒラク:
		cpu.Eax = uint32(sysヒラク(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysヒラク(cpu.Ebx, oサクセイ|oカキコミセンヨウ|oキリステ, cpu.Ecx))
		return esp
	case Sysトジル:
		cpu.Eax = uint32(sysトジル(int32(cpu.Ebx)))
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
		cpu.Eax = Cゲンザイノニチジpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Cゲンザイノニチジparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysアクセス:
		cpu.Eax = uint32(sysアクセス(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysソケットヨビダシ(cpu.Ebx, cpu.Ecx))
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
		コンソール_2.MUnsignedinteger32インサツ(cpu.Ebx)
		return esp

	default:
		コンソール_2.Mインサツxy(([]byte)("sys["), 1, 23)
		コンソール_2.MUnsignedinteger32インサツ(esp)
		コンソール_2.Mインサツ(([]byte)(":"))
		コンソール_2.MUnsignedinteger32インサツ(cpu.Eax)
		コンソール_2.Mインサツ(([]byte)(":"))
		コンソール_2.MUnsignedinteger32インサツ(cpu.Ebx)
		コンソール_2.Mインサツ(([]byte)(":"))
		コンソール_2.MUnsignedinteger32インサツ(cpu.Ecx)
		コンソール_2.Mインサツ(([]byte)(":"))
		コンソール_2.MUnsignedinteger32インサツ(cpu.Edx)
		コンソール_2.Mインサツ(([]byte)("]"))
		cpu.Eax = syscallエラー(Enosys)
		return esp
	}

	return esp
}

func initファイルdescriptor() {
	for i := 0; i < サイダイヒラクファイル; i++ {
		ヒラクファイルtable[i] = ヒラクファイルセツメイ{}
	}
	for i := 0; i < len(プロセスtable); i++ {
		プロセスtable[i] = プロセスentry{}
	}
	for i := 0; i < len(ローカルsockets); i++ {
		ローカルsockets[i] = ローカルdatagramソケット{}
	}
	ツギephemeralポート = 49152
	ヒラクファイルtable[0] = ヒラクファイルセツメイ{シヨウチュウ: true, kind: fdkindstdin, フラグ: oヨミコミセンヨウ}
	ヒラクファイルtable[1] = ヒラクファイルセツメイ{シヨウチュウ: true, kind: fdkindコンソール, フラグ: oカキコミセンヨウ}
	ヒラクファイルtable[2] = ヒラクファイルセツメイ{シヨウチュウ: true, kind: fdkindコンソール, フラグ: oカキコミセンヨウ}
}

func ケンサクプロセス(pid uint32) *プロセスentry {
	for i := 0; i < len(プロセスtable); i++ {
		if プロセスtable[i].シヨウチュウ && プロセスtable[i].pid == pid {
			return &プロセスtable[i]
		}
	}
	return nil
}

func initializeプロセスfds(プロセス *プロセスentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		プロセス.fds[fd] = fdentry{シヨウチュウ: true, セツメイ: fd}
		ヒラクファイルtable[fd].refs++
	}
}

func ensureゲンザイノニチジプロセス() *プロセスentry {
	pid := Cゲンザイノニチジpid()
	if プロセス := ケンサクプロセス(pid); プロセス != nil {
		return プロセス
	}
	for i := 0; i < len(プロセスtable); i++ {
		if !プロセスtable[i].シヨウチュウ {
			プロセスtable[i] = プロセスentry{
				シヨウチュウ:		true,
				pid:		pid,
				parent:		Cゲンザイノニチジparentpid(),
				プログラムbreak:	リヨウシャheapbase,
			}
			initializeプロセスfds(&プロセスtable[i])
			return &プロセスtable[i]
		}
	}
	return nil
}

func getヒラクファイルfor(プロセス *プロセスentry, fd int32) *ヒラクファイルセツメイ {
	if プロセス == nil || fd < 0 || fd >= サイダイfd || !プロセス.fds[fd].シヨウチュウ {
		return nil
	}
	セツメイ := プロセス.fds[fd].セツメイ
	if セツメイ < 0 || セツメイ >= サイダイヒラクファイル || !ヒラクファイルtable[セツメイ].シヨウチュウ {
		return nil
	}
	return &ヒラクファイルtable[セツメイ]
}

func getヒラクファイル(fd int32) *ヒラクファイルセツメイ {
	return getヒラクファイルfor(ensureゲンザイノニチジプロセス(), fd)
}

func allocateヒラクファイル() int32 {
	for i := int32(3); i < サイダイヒラクファイル; i++ {
		if !ヒラクファイルtable[i].シヨウチュウ {
			ヒラクファイルtable[i] = ヒラクファイルセツメイ{シヨウチュウ: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(プロセス *プロセスentry, セツメイ int32, サイショウ int32) int32 {
	if プロセス == nil {
		return Enfile
	}
	if サイショウ < 0 || サイショウ >= サイダイfd {
		return Einval
	}
	for fd := サイショウ; fd < サイダイfd; fd++ {
		if !プロセス.fds[fd].シヨウチュウ {
			プロセス.fds[fd] = fdentry{シヨウチュウ: true, セツメイ: セツメイ}
			return fd
		}
	}
	return Emfile
}

func releaseヒラクファイル(セツメイ int32) {
	if セツメイ < 0 || セツメイ >= サイダイヒラクファイル {
		return
	}
	entry := &ヒラクファイルtable[セツメイ]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && セツメイ > stderrfd {
		if entry.kind == fdkindソケット && entry.aux < サイダイsockets {
			ローカルsockets[entry.aux] = ローカルdatagramソケット{}
		}
		*entry = ヒラクファイルセツメイ{}
	}
}

func トジルプロセスfd(プロセス *プロセスentry, fd int32) int32 {
	if プロセス == nil || getヒラクファイルfor(プロセス, fd) == nil {
		return Ebadf
	}
	セツメイ := プロセス.fds[fd].セツメイ
	プロセス.fds[fd] = fdentry{}
	releaseヒラクファイル(セツメイ)
	return 0
}

func sysカキコミ(fd int32, address uint32, カウント uint32) int32 {
	if カウント == 0 {
		return 0
	}
	if address == 0 || address+カウント < address {
		return Efault
	}
	if カウント > 4096 {
		return Einval
	}
	entry := getヒラクファイル(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindコンソール {
		if entry.kind == fdkindソケット {
			return ソケットソウシンto(fd, address, カウント, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindルートディレクトリ {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getバイトカラポインタ(uintptr(address), int(カウント), int(カウント))
	コンソール_2.Mインサツ(buffer)
	return int32(カウント)
}

func sysヨミコミ(fd int32, address uint32, カウント uint32) int32 {
	if カウント == 0 {
		return 0
	}
	if address == 0 || address+カウント < address {
		return Efault
	}
	entry := getヒラクファイル(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return ヨミコミstdin(address, カウント)
	}
	if entry.kind == fdkindルートディレクトリ {
		return Eisdir
	}
	if entry.kind == fdkindソケット {
		return ソケットreceiveカラ(fd, address, カウント, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.ハイチ >= entry.サイズ {
		return 0
	}
	remaining := entry.サイズ - entry.ハイチ
	if カウント > remaining {
		カウント = remaining
	}
	buffer := Getバイトカラポインタ(uintptr(address), int(カウント), int(カウント))
	return ヨミコミvfsファイル(entry, buffer, カウント)
}

func sysヒラク(パスaddress uint32, フラグ uint32, モード uint32) int32 {
	_ = モード
	if パスaddress == 0 {
		return Efault
	}
	アクセスモード := フラグ & 3
	if アクセスモード == oカキコミセンヨウ || アクセスモード == oヨミコミカキコミ || (フラグ&(oサクセイ|oキリステ|oappend)) != 0 {
		return Erofs
	}

	プロセス := ensureゲンザイノニチジプロセス()
	if プロセス == nil {
		return Enfile
	}
	セツメイ := allocateヒラクファイル()
	if セツメイ < 0 {
		return セツメイ
	}
	entry := &ヒラクファイルtable[セツメイ]
	entry.フラグ = フラグ
	if isルートパス(パスaddress) {
		entry.kind = fdkindルートディレクトリ
		entry.サイズ = 0
	} else {
		ナマエlen, ナマエ := フクセイパス(パスaddress)
		if ナマエlen == 0 {
			*entry = ヒラクファイルセツメイ{}
			return Enoent
		}
		サイズ := ファイルサイズ(ナマエ[:ナマエlen])
		if サイズ == 0 {
			*entry = ヒラクファイルセツメイ{}
			return Enoent
		}
		if (フラグ & oディレクトリ) != 0 {
			*entry = ヒラクファイルセツメイ{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.サイズ = サイズ
		entry.ナマエlen = ナマエlen
		entry.ナマエ = ナマエ
	}

	fd := allocatefd(プロセス, セツメイ, 3)
	if fd < 0 {
		*entry = ヒラクファイルセツメイ{}
		return fd
	}
	return fd
}

func sysトジル(fd int32) int32 {
	return トジルプロセスfd(ensureゲンザイノニチジプロセス(), fd)
}

func sysdup(fd int32, サイショウ int32) int32 {
	プロセス := ensureゲンザイノニチジプロセス()
	entry := getヒラクファイルfor(プロセス, fd)
	if entry == nil {
		return Ebadf
	}
	シンキfd := allocatefd(プロセス, プロセス.fds[fd].セツメイ, サイショウ)
	if シンキfd >= 0 {
		entry.refs++
	}
	return シンキfd
}

func sysdup2(oldfd int32, シンキfd int32) int32 {
	プロセス := ensureゲンザイノニチジプロセス()
	entry := getヒラクファイルfor(プロセス, oldfd)
	if entry == nil {
		return Ebadf
	}
	if シンキfd < 0 || シンキfd >= サイダイfd {
		return Ebadf
	}
	if oldfd == シンキfd {
		return シンキfd
	}
	if プロセス.fds[シンキfd].シヨウチュウ {
		トジルプロセスfd(プロセス, シンキfd)
	}
	プロセス.fds[シンキfd] = fdentry{シヨウチュウ: true, セツメイ: プロセス.fds[oldfd].セツメイ}
	entry.refs++
	return シンキfd
}

func sysfcntl(fd int32, コマンド uint32, argument uint32) int32 {
	プロセス := ensureゲンザイノニチジプロセス()
	entry := getヒラクファイルfor(プロセス, fd)
	if entry == nil {
		return Ebadf
	}
	switch コマンド {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(プロセス.fds[fd].fdフラグ)
	case fアリfd:
		プロセス.fds[fd].fdフラグ = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.フラグ)
	case fアリfl:
		entry.フラグ = (entry.フラグ & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getヒラクファイル(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekアリ:
		base = 0
	case seekゲンザイノニチジ:
		base = int64(entry.ハイチ)
	case seekブンマツ:
		base = int64(entry.サイズ)
	default:
		return Einval
	}
	ハイチ_2 := base + int64(offset)
	if ハイチ_2 < 0 || ハイチ_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.ハイチ = uint32(ハイチ_2)
	return int32(entry.ハイチ)
}

func ヨミコミvfsファイル(entry *ヒラクファイルセツメイ, テンソウサキ_2 []byte, カウント uint32) int32 {
	メモリカンリシャ := &mem.Tメモリカンリシャ{}
	tmpポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(entry.サイズ)
	if tmpポインタ == nil {
		return Einval
	}
	tmp := Getバイトカラポインタ(uintptr(tmpポインタ), int(entry.サイズ), int(entry.サイズ))
	ヨミコミファイル(entry.ナマエ[:entry.ナマエlen], tmp)
	copy(テンソウサキ_2[:カウント], tmp[entry.ハイチ:entry.ハイチ+カウント])
	entry.ハイチ += カウント
	メモリカンリシャ.Fアキ(tmpポインタ)
	return int32(カウント)
}

func isルートパス(パスaddress uint32) bool {
	if パスaddress == 0 {
		return false
	}
	パス := Getバイトカラポインタ(uintptr(パスaddress), 4, 4)
	if パス[0] == '/' && パス[1] == 0 {
		return true
	}
	if パス[0] == '.' && パス[1] == 0 {
		return true
	}
	if パス[0] == '/' && パス[1] == '.' && パス[2] == 0 {
		return true
	}
	return false
}

func sysアクセス(パスaddress uint32, モード uint32) int32 {
	if パスaddress == 0 {
		return Efault
	}
	if (モード & ^uint32(7)) != 0 {
		return Einval
	}
	isルート := isルートパス(パスaddress)
	exists := isルート
	if !exists {
		ナマエlen, ナマエ := フクセイパス(パスaddress)
		exists = ナマエlen != 0 && ファイルサイズ(ナマエ[:ナマエlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (モード & 2) != 0 {
		return Eacces
	}

	if (モード&1) != 0 && !isルート {
		return Eacces
	}
	return 0
}

func syschdir(パスaddress uint32) int32 {
	if パスaddress == 0 {
		return Efault
	}
	if !isルートパス(パスaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, サイズ uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if サイズ < 2 {
		return Erange
	}
	buffer_2 := Getバイトカラポインタ(uintptr(bufferaddress), int(サイズ), int(サイズ))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, モード uint32, サイズ uint32, iノード uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dデバイス = 1
	stat.Ino = iノード
	stat.Mモード = モード
	stat.Nlink = 1
	stat.Sサイズ_2 = int32(サイズ)
	stat.Blksize = 512
	stat.Bブロック = int32((サイズ + 511) / 512)
	return 0
}

func sysstat(パスaddress uint32, stataddress uint32) int32 {
	if パスaddress == 0 {
		return Efault
	}
	if isルートパス(パスaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	ナマエlen, ナマエ := フクセイパス(パスaddress)
	if ナマエlen == 0 {
		return Enoent
	}
	サイズ := ファイルサイズ(ナマエ[:ナマエlen])
	if サイズ == 0 {
		return Enoent
	}
	iノード := uint32(2)
	for i := uint32(0); i < ナマエlen; i++ {
		iノード = iノード*33 + uint32(ナマエ[i])
	}
	return fillposixstat(stataddress, sifreg|0444, サイズ, iノード)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getヒラクファイル(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindコンソール:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindルートディレクトリ:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.サイズ, uint32(fd+2))
	case fdkindソケット:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getヒラクファイル(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	プロセス := ensureゲンザイノニチジプロセス()
	if プロセス == nil {
		return 0
	}
	if プロセス.プログラムbreak == 0 {
		プロセス.プログラムbreak = リヨウシャheapbase
	}
	if address_2 == 0 {
		return プロセス.プログラムbreak
	}
	if address_2 < リヨウシャheapbase || address_2 > リヨウシャheapセイゲン {
		return プロセス.プログラムbreak
	}
	プロセス.プログラムbreak = address_2
	return プロセス.プログラムbreak
}

func フクセイutsfield(テンソウサキ *[65]byte, アタイ string) {
	セイゲン := len(アタイ)
	if セイゲン > 64 {
		セイゲン = 64
	}
	for i := 0; i < セイゲン; i++ {
		テンソウサキ[i] = アタイ[i]
	}
	テンソウサキ[セイゲン] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	ナマエ := (*posixutsname)(Pointer(uintptr(address_2)))
	*ナマエ = posixutsname{}
	フクセイutsfield(&ナマエ.Sysname, "EngOS")
	フクセイutsfield(&ナマエ.Nodename, "engos")
	フクセイutsfield(&ナマエ.Release, "0.1-posix")
	フクセイutsfield(&ナマエ.Vバージョン, "POSIX.1-2017 phase 1")
	フクセイutsfield(&ナマエ.Machine, "i386")
	return 0
}

func スワップunsignedinteger16(アタイ uint16) uint16 {
	return (アタイ << 8) | (アタイ >> 8)
}

func ソケットヨビダシargument(ヒキスウ_2 uint32, モクジ uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ヒキスウ_2 + モクジ*4)))
}

func ソケットforfd(fd int32) (*ローカルdatagramソケット, int32) {
	entry := getヒラクファイル(fd)
	if entry == nil || entry.kind != fdkindソケット || entry.aux >= サイダイsockets {
		return nil, Ebadf
	}
	ソケット := &ローカルsockets[entry.aux]
	if !ソケット.シヨウチュウ {
		return nil, Ebadf
	}
	return ソケット, 0
}

func allocateソケット(ドメイン uint32, ソケットカタ uint32, protocol uint32) int32 {
	if ドメイン != afinet {
		return Eafnosupport
	}
	if ソケットカタ != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	プロセス := ensureゲンザイノニチジプロセス()
	if プロセス == nil {
		return Enfile
	}
	ソケットモクジ := -1
	for i := 0; i < サイダイsockets; i++ {
		if !ローカルsockets[i].シヨウチュウ {
			ソケットモクジ = i
			break
		}
	}
	if ソケットモクジ < 0 {
		return Enfile
	}
	セツメイ := allocateヒラクファイル()
	if セツメイ < 0 {
		return セツメイ
	}
	ローカルsockets[ソケットモクジ] = ローカルdatagramソケット{シヨウチュウ: true}
	entry := &ヒラクファイルtable[セツメイ]
	entry.kind = fdkindソケット
	entry.フラグ = oヨミコミカキコミ
	entry.aux = uint32(ソケットモクジ)
	fd := allocatefd(プロセス, セツメイ, 3)
	if fd < 0 {
		ローカルsockets[ソケットモクジ] = ローカルdatagramソケット{}
		*entry = ヒラクファイルセツメイ{}
		return fd
	}
	return fd
}

func ソケットaddress(address_2 uint32, ナガサ uint32) (*ソケットaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if ナガサ < 16 {
		return nil, Einval
	}
	セイセイサキ := (*ソケットaddressipv4)(Pointer(uintptr(address_2)))
	if セイセイサキ.Family != afinet {
		return nil, Eafnosupport
	}
	return セイセイサキ, 0
}

func ポートジュシンON(ポート uint16, except *ローカルdatagramソケット) bool {
	for i := 0; i < サイダイsockets; i++ {
		ソケット := &ローカルsockets[i]
		if ソケット != except && ソケット.シヨウチュウ && ソケット.bound && ソケット.ローカル.Pポート == ポート {
			return true
		}
	}
	return false
}

func バインドephemeral(ソケット *ローカルdatagramソケット) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		ポート := スワップunsignedinteger16(ツギephemeralポート)
		ツギephemeralポート++
		if ツギephemeralポート < 49152 {
			ツギephemeralポート = 49152
		}
		if !ポートジュシンON(ポート, ソケット) {
			ソケット.ローカル = ソケットaddressipv4{Family: afinet, Pポート: ポート, Address: 0x0100007F}
			ソケット.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func ソケットバインド(fd int32, address_2 uint32, ナガサ uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	requested, エラー := ソケットaddress(address_2, ナガサ)
	if エラー != 0 {
		return エラー
	}
	if ソケット.bound {
		return Einval
	}
	if requested.Pポート == 0 {
		return バインドephemeral(ソケット)
	}
	if ポートジュシンON(requested.Pポート, ソケット) {
		return Eaddrinuse
	}
	ソケット.ローカル = *requested
	ソケット.bound = true
	return 0
}

func ソケットセツゾク(fd int32, address_2 uint32, ナガサ uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	リモート, エラー := ソケットaddress(address_2, ナガサ)
	if エラー != 0 {
		return エラー
	}
	if !ソケット.bound {
		if エラー := バインドephemeral(ソケット); エラー != 0 {
			return エラー
		}
	}
	ソケット.リモート = *リモート
	ソケット.connected = true
	return 0
}

func ソケットソウシンto(fd int32, bufferaddress_2 uint32, ナガサ uint32, テンソウサキaddress uint32, テンソウサキナガサ uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	if ナガサ > サイダイdatagramサイズ {
		return Emsgsize
	}
	if ナガサ != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var テンソウサキ ソケットaddressipv4
	if テンソウサキaddress != 0 {
		address_2, addressエラー := ソケットaddress(テンソウサキaddress, テンソウサキナガサ)
		if addressエラー != 0 {
			return addressエラー
		}
		テンソウサキ = *address_2
	} else {
		if !ソケット.connected {
			return Enotconn
		}
		テンソウサキ = ソケット.リモート
	}
	if !ソケット.bound {
		if バインドエラー := バインドephemeral(ソケット); バインドエラー != 0 {
			return バインドエラー
		}
	}
	var receiver *ローカルdatagramソケット
	for i := 0; i < サイダイsockets; i++ {
		candidate := &ローカルsockets[i]
		if candidate.シヨウチュウ && candidate.bound && candidate.ローカル.Pポート == テンソウサキ.Pポート &&
			(candidate.ローカル.Address == 0 || candidate.ローカル.Address == テンソウサキ.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.カウント >= サイダイソケットパケット {
		return Eagain
	}
	packet := &receiver.パケット[receiver.tail]
	*packet = ソケットpacket{シヨウチュウ: true, サイズ: ナガサ, テンソウモト: ソケット.ローカル}
	if ナガサ != 0 {
		テンソウモト := Getバイトカラポインタ(uintptr(bufferaddress_2), int(ナガサ), int(ナガサ))
		copy(packet.データ[:ナガサ], テンソウモト)
	}
	receiver.tail = (receiver.tail + 1) % サイダイソケットパケット
	receiver.カウント++
	return int32(ナガサ)
}

func ソケットreceiveカラ(fd int32, bufferaddress_2 uint32, ナガサ uint32, テンソウモトaddress uint32, テンソウモトナガサaddress uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	if ナガサ != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if ソケット.カウント == 0 {
		return Eagain
	}
	packet := &ソケット.パケット[ソケット.head]
	フクセイナガサ := packet.サイズ
	if フクセイナガサ > ナガサ {
		フクセイナガサ = ナガサ
	}
	if フクセイナガサ != 0 {
		テンソウサキ := Getバイトカラポインタ(uintptr(bufferaddress_2), int(フクセイナガサ), int(フクセイナガサ))
		copy(テンソウサキ, packet.データ[:フクセイナガサ])
	}
	if テンソウモトaddress != 0 {
		if テンソウモトナガサaddress == 0 {
			return Efault
		}
		providedナガサ := (*uint32)(Pointer(uintptr(テンソウモトナガサaddress)))
		if *providedナガサ >= 16 {
			*(*ソケットaddressipv4)(Pointer(uintptr(テンソウモトaddress))) = packet.テンソウモト
		}
		*providedナガサ = 16
	}
	*packet = ソケットpacket{}
	ソケット.head = (ソケット.head + 1) % サイダイソケットパケット
	ソケット.カウント--
	return int32(フクセイナガサ)
}

func フクセイソケットナマエ(fd int32, address_2 uint32, ナガサaddress uint32, peer bool) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	if address_2 == 0 || ナガサaddress == 0 {
		return Efault
	}
	ナガサ := (*uint32)(Pointer(uintptr(ナガサaddress)))
	if *ナガサ < 16 {
		*ナガサ = 16
		return Einval
	}
	if peer {
		if !ソケット.connected {
			return Enotconn
		}
		*(*ソケットaddressipv4)(Pointer(uintptr(address_2))) = ソケット.リモート
	} else {
		if !ソケット.bound {
			if バインドエラー := バインドephemeral(ソケット); バインドエラー != 0 {
				return バインドエラー
			}
		}
		*(*ソケットaddressipv4)(Pointer(uintptr(address_2))) = ソケット.ローカル
	}
	*ナガサ = 16
	return 0
}

func sysソケットヨビダシ(ヨビダシ uint32, ヒキスウ_2 uint32) int32 {
	if ヒキスウ_2 == 0 {
		return Efault
	}
	switch ヨビダシ {
	case 1:
		return allocateソケット(ソケットヨビダシargument(ヒキスウ_2, 0), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2))
	case 2:
		return ソケットバインド(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2))
	case 3:
		return ソケットセツゾク(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return フクセイソケットナマエ(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2), false)
	case 7:
		return フクセイソケットナマエ(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2), true)
	case 9:
		return ソケットソウシンto(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2), 0, 0)
	case 10:
		return ソケットreceiveカラ(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2), 0, 0)
	case 11:
		return ソケットソウシンto(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2), ソケットヨビダシargument(ヒキスウ_2, 4), ソケットヨビダシargument(ヒキスウ_2, 5))
	case 12:
		return ソケットreceiveカラ(int32(ソケットヨビダシargument(ヒキスウ_2, 0)), ソケットヨビダシargument(ヒキスウ_2, 1), ソケットヨビダシargument(ヒキスウ_2, 2), ソケットヨビダシargument(ヒキスウ_2, 4), ソケットヨビダシargument(ヒキスウ_2, 5))
	case 13:
		if _, エラー := ソケットforfd(int32(ソケットヨビダシargument(ヒキスウ_2, 0))); エラー != 0 {
			return エラー
		}
		return 0
	case 14:
		if _, エラー := ソケットforfd(int32(ソケットヨビダシargument(ヒキスウ_2, 0))); エラー != 0 {
			return エラー
		}
		return 0
	}
	return Eopnotsupp
}

func ヨミコミstdin(address uint32, カウント uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getバイトカラポインタ(uintptr(address), int(カウント), int(カウント))
	var n uint32
	for n < カウント {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputバイト(c byte) {
	ツギ := (stdinカキコミ + 1) % uint32(len(stdinbuffer))
	if ツギ == stdinヨミコミ {
		return
	}
	stdinbuffer[stdinカキコミ] = c
	stdinカキコミ = ツギ
}

func stdingetblocking() byte {
	for stdinヨミコミ == stdinカキコミ {
		sc := pollキーボードscancode()
		if sc != 0 {
			Stdinputバイト(sc)
		}
	}
	c := stdinbuffer[stdinヨミコミ]
	stdinヨミコミ = (stdinヨミコミ + 1) % uint32(len(stdinbuffer))
	return c
}

func pollキーボードscancode() byte {
	for (Pポートヨミコミバイト(0x64) & 0x01) == 0 {
	}
	sc := Pポートヨミコミバイト(0x60)
	return scancodetoバイト(sc)
}

func scancodetoバイト(sc uint8) byte {
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

func フクセイジッコウvector(address_2 uint32, セイセイサキ *ジッコウvector) int32 {
	*セイセイサキ = ジッコウvector{}
	if address_2 == 0 {
		return 0
	}
	for モクジ := uint32(0); モクジ < サイダイジッコウvectorentry; モクジ++ {
		モジレツaddress := *(*uint32)(Pointer(uintptr(address_2 + モクジ*4)))
		if モジレツaddress == 0 {
			セイセイサキ.カウント = モクジ
			return 0
		}
		terminated := false
		for ナガサ := uint32(0); ナガサ <= サイダイジッコウブンジレツナガサ; ナガサ++ {
			アタイ := *(*byte)(Pointer(uintptr(モジレツaddress + ナガサ)))
			セイセイサキ.スウチ[モクジ][ナガサ] = アタイ
			if アタイ == 0 {
				セイセイサキ.lengths[モクジ] = ナガサ
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

func pushジッコウunsignedinteger32(ツミカサネキオクリョウイキ *uint32, アタイ uint32) {
	*ツミカサネキオクリョウイキ -= 4
	*(*uint32)(Pointer(uintptr(*ツミカサネキオクリョウイキ))) = アタイ
}

func setupジッコウstack(cpu *Tcpuジョウタイ, ヒキスウ_2 *ジッコウvector, environment *ジッコウvector) int32 {
	const stackバイト uint32 = 4096
	if !Makerangeプライベートwritable(getcr3(), Uリヨウシャstackウエ-stackバイト, stackバイト) {
		return Enomem
	}
	ツミカサネキオクリョウイキ := Uリヨウシャstackウエ
	var argumentpointers [サイダイジッコウvectorentry]uint32
	var environmentpointers [サイダイジッコウvectorentry]uint32

	for i := int(environment.カウント) - 1; i >= 0; i-- {
		ナガサ := environment.lengths[i] + 1
		ツミカサネキオクリョウイキ -= ナガサ
		テンソウサキ := Getバイトカラポインタ(uintptr(ツミカサネキオクリョウイキ), int(ナガサ), int(ナガサ))
		copy(テンソウサキ, environment.スウチ[i][:ナガサ])
		environmentpointers[i] = ツミカサネキオクリョウイキ
	}
	for i := int(ヒキスウ_2.カウント) - 1; i >= 0; i-- {
		ナガサ := ヒキスウ_2.lengths[i] + 1
		ツミカサネキオクリョウイキ -= ナガサ
		テンソウサキ := Getバイトカラポインタ(uintptr(ツミカサネキオクリョウイキ), int(ナガサ), int(ナガサ))
		copy(テンソウサキ, ヒキスウ_2.スウチ[i][:ナガサ])
		argumentpointers[i] = ツミカサネキオクリョウイキ
	}
	ツミカサネキオクリョウイキ &= ^uint32(3)
	pushジッコウunsignedinteger32(&ツミカサネキオクリョウイキ, 0)
	for i := int(environment.カウント) - 1; i >= 0; i-- {
		pushジッコウunsignedinteger32(&ツミカサネキオクリョウイキ, environmentpointers[i])
	}
	pushジッコウunsignedinteger32(&ツミカサネキオクリョウイキ, 0)
	for i := int(ヒキスウ_2.カウント) - 1; i >= 0; i-- {
		pushジッコウunsignedinteger32(&ツミカサネキオクリョウイキ, argumentpointers[i])
	}
	pushジッコウunsignedinteger32(&ツミカサネキオクリョウイキ, ヒキスウ_2.カウント)
	cpu.Esp = ツミカサネキオクリョウイキ
	cpu.Ebp = 0
	return 0
}

func トジルトキジッコウ(プロセス *プロセスentry) {
	if プロセス == nil {
		return
	}
	for fd := int32(0); fd < サイダイfd; fd++ {
		if プロセス.fds[fd].シヨウチュウ && (プロセス.fds[fd].fdフラグ&fdcloexec) != 0 {
			トジルプロセスfd(プロセス, fd)
		}
	}
}

func sysexecve(cpu *Tcpuジョウタイ, パスaddress uint32) int32 {
	if パスaddress == 0 {
		return Efault
	}
	var ヒキスウ_2 ジッコウvector
	var environment ジッコウvector
	if セイセイサキ := フクセイジッコウvector(cpu.Ecx, &ヒキスウ_2); セイセイサキ < 0 {
		return セイセイサキ
	}
	if セイセイサキ := フクセイジッコウvector(cpu.Edx, &environment); セイセイサキ < 0 {
		return セイセイサキ
	}
	ナマエlen, ナマエ := フクセイパス(パスaddress)
	if ナマエlen == 0 {
		return Enoent
	}
	サイズ := ファイルサイズ(ナマエ[:ナマエlen])
	if サイズ == 0 {
		return Enoent
	}
	メモリカンリシャ := &mem.Tメモリカンリシャ{}
	ファイルポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	if ファイルポインタ == nil {
		return Einval
	}
	データ := Getバイトカラポインタ(uintptr(ファイルポインタ), int(サイズ), int(サイズ))
	ヨミコミファイル(ナマエ[:ナマエlen], データ)
	if サイズ < 52 || データ[0] != 0x7F || データ[1] != 'E' || データ[2] != 'L' || データ[3] != 'F' {
		メモリカンリシャ.Fアキ(ファイルポインタ)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(データ)
	loader.Parse(データ, getcr3())
	メモリカンリシャ.Fアキ(ファイルポインタ)
	if セイセイサキ := setupジッコウstack(cpu, &ヒキスウ_2, &environment); セイセイサキ < 0 {
		return セイセイサキ
	}
	トジルトキジッコウ(ensureゲンザイノニチジプロセス())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpuジョウタイ) int32 {
	parentpid := Cゲンザイノニチジpid()
	if ensureゲンザイノニチジプロセス() == nil {
		return Enfile
	}
	pid := allocateプロセス(parentpid)
	if pid == 0 {
		return Einval
	}
	メモリカンリシャ := &mem.Tメモリカンリシャ{}
	スレッドポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(uint32(Sizeof(Tスレッド{})))
	stackポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(Tスレッドstackサイズ)
	childページディレクトリ := Cloneaddressスペースcow(getcr3())
	if スレッドポインタ == nil || stackポインタ == nil || childページディレクトリ == 0 {
		ハキプロセス(pid)
		return Einval
	}
	child := (*Tスレッド)(スレッドポインタ)
	child.Stack = uint32(uintptr(stackポインタ))
	child.Cpuジョウタイ = (*Tcpuジョウタイ)(Pointer(uintptr(stackポインタ) + Tスレッドstackサイズ - Sizeof(Tcpuジョウタイ{})))
	*child.Cpuジョウタイ = *cpu
	child.Cpuジョウタイ.Eax = 0
	child.Uリヨウシャstack_2 = cpu.Esp
	child.Uリヨウシャstackサイズ_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pページディレクトリentry = childページディレクトリ
	child.Tスレッドジョウタイ = RジュンビOK
	child.Fpuoffset = 0xffffffff
	child.Isチュウカク = false
	Aツイカrunnableスレッド(child)
	return int32(pid)
}

func sysシュウリョウ(ジョウタイ uint32) {
	pid := Cゲンザイノニチジpid()
	for i := 0; i < len(プロセスtable); i++ {
		if プロセスtable[i].シヨウチュウ && プロセスtable[i].pid == pid {
			トジルスベテプロセスfds(&プロセスtable[i])
			プロセスtable[i].シュウリョウ = true
			プロセスtable[i].ジョウタイ = (ジョウタイ & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, ジョウタイaddress uint32, オプション uint32) int32 {
	if (オプション & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Cゲンザイノニチジpid()
	foundchild := false
	for i := 0; i < len(プロセスtable); i++ {
		p := &プロセスtable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.シヨウチュウ && matches && p.parent == parentpid {
			foundchild = true
			if p.シュウリョウ {
				if ジョウタイaddress != 0 {
					*(*uint32)(Pointer(uintptr(ジョウタイaddress))) = p.ジョウタイ
				}
				childpid := p.pid
				*p = プロセスentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (オプション & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateプロセス(parent uint32) uint32 {
	parentプロセス := ケンサクプロセス(parent)
	pid := Allocatepid()
	for i := 0; i < len(プロセスtable); i++ {
		if !プロセスtable[i].シヨウチュウ {
			プロセスtable[i] = プロセスentry{
				シヨウチュウ:		true,
				pid:		pid,
				parent:		parent,
				プログラムbreak:	リヨウシャheapbase,
			}
			if parentプロセス != nil {
				プロセスtable[i].プログラムbreak = parentプロセス.プログラムbreak
				for fd := 0; fd < サイダイfd; fd++ {
					if parentプロセス.fds[fd].シヨウチュウ {
						プロセスtable[i].fds[fd] = parentプロセス.fds[fd]
						セツメイ := parentプロセス.fds[fd].セツメイ
						if セツメイ >= 0 && セツメイ < サイダイヒラクファイル {
							ヒラクファイルtable[セツメイ].refs++
						}
					}
				}
			} else {
				initializeプロセスfds(&プロセスtable[i])
			}
			return pid
		}
	}
	return 0
}

func トジルスベテプロセスfds(プロセス *プロセスentry) {
	if プロセス == nil {
		return
	}
	for fd := int32(0); fd < サイダイfd; fd++ {
		if プロセス.fds[fd].シヨウチュウ {
			トジルプロセスfd(プロセス, fd)
		}
	}
}

func ハキプロセス(pid uint32) {
	プロセス := ケンサクプロセス(pid)
	if プロセス == nil {
		return
	}
	トジルスベテプロセスfds(プロセス)
	*プロセス = プロセスentry{}
}

func フクセイパス(パスaddress uint32) (uint32, [12]byte) {
	var ナマエ [12]byte
	if パスaddress == 0 {
		return 0, ナマエ
	}
	raw := Getバイトカラポインタ(uintptr(パスaddress), 64, 64)
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
		ナマエ[n] = c
		n++
	}
	return n, ナマエ
}

func ファイルサイズ(ファイルメイ []byte) uint32 {
	var ata0s = Tショウサイシヨウギジュツattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	クブン := Tmsdosクブンtable{}
	クブン.Rヨミコミクブン(&ata0s)

	bios := Tファイルタイケイセッテイチ32{}
	サイズ := bios.Len(&ata0s, クブン.Mbr.Primaryクブン[0], ファイルメイ)
	ata0s.Flush()
	return サイズ
}

func ヨミコミファイル(ファイルメイ []byte, データ []byte) {
	var ata0s = Tショウサイシヨウギジュツattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	クブン := Tmsdosクブンtable{}
	クブン.Rヨミコミクブン(&ata0s)

	bios := Tファイルタイケイセッテイチ32{}
	bios.Rヨミコミ(&ata0s, クブン.Mbr.Primaryクブン[0], ファイルメイ, データ)
	ata0s.Flush()
}

func getcr3() uint32
