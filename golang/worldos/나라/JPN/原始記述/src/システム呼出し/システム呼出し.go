/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package システム呼出し

import . "unsafe"

import . "割込み"
import . "コンソール"
import . "汎用"
import . "複数タスク管理"
import . "ドライバー/ata"
import . "ファイルシステム/msdos区分"
import . "ファイルシステム/fat"
import . "ファイルシステム/実行連結形式"
import mem "メモリ管理者"
import . "ページ管理"
import . "ポート"
import . "タスク管理/スケジューラ"
import . "タスク管理/スレッド"
import . "仮想メモリ"

var コンソール_2 = Tコンソール{}

type TSyscall struct {
	T割込みhandler
}

const (
	Sys終了		uint32	= 1
	Sysfork		uint32	= 2
	Sys読込み		uint32	= 3
	Sys書込み		uint32	= 4
	Sys開く		uint32	= 5
	Sys閉じる		uint32	= 6
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
	Sysrt終了		uint32	= 252

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
	最大fd			= 32
	最大開くファイル		= 128
)

type fdentry struct {
	使用中	bool
	説明	int32
	fdフラグ	uint32
}

type 開くファイル説明 struct {
	使用中	bool
	refs	uint32
	kind	uint32
	フラグ	uint32
	配置	uint32
	サイズ	uint32
	名前	[12]byte
	名前len	uint32
	aux	uint32
}

const (
	fdkindなし	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindコンソール	uint32	= 3
	fdkindルートディレクトリ	uint32	= 4
	fdkindソケット	uint32	= 5

	o読込み専用	uint32	= 0
	o書込み専用	uint32	= 1
	o読込み書込み	uint32	= 2
	o作成	uint32	= 0x40
	o切り捨て	uint32	= 0x200
	oappend	uint32	= 0x400
	oディレクトリ	uint32	= 0x10000

	seekあり		uint32	= 0
	seek現在の日時	uint32	= 1
	seek文末		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fありfd		uint32	= 2
	fgetfl		uint32	= 3
	fありfl		uint32	= 4
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
	最大sockets	= 32
	最大ソケットパケット	= 8
	最大datagramサイズ	= 512
)

type ソケットaddressipv4 struct {
	Family	uint16
	Pポート	uint16
	Address	uint32
	Z数値の0	[8]byte
}

type ソケットpacket struct {
	使用中	bool
	サイズ	uint32
	転送元	ソケットaddressipv4
	データ	[最大datagramサイズ]byte
}

type ローカルdatagramソケット struct {
	使用中		bool
	bound		bool
	connected	bool
	ローカル		ソケットaddressipv4
	リモート		ソケットaddressipv4
	head		uint32
	tail		uint32
	カウント		uint32
	パケット		[最大ソケットパケット]ソケットpacket
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
	最大実行vectorentry	= 16
	最大実行文字列長さ	= 63
)

type 実行vector struct {
	カウント	uint32
	lengths	[最大実行vectorentry]uint32
	数値	[最大実行vectorentry][最大実行文字列長さ + 1]byte
}

type プロセスentry struct {
	使用中		bool
	pid		uint32
	parent		uint32
	終了		bool
	状態		uint32
	プログラムbreak	uint32
	fds		[最大fd]fdentry
}

type 文字列ヘッダ struct {
	Data	uintptr
	Len	int
}

func syscallエラー(エラー int32) uint32 {
	return *(*uint32)(Pointer(&エラー))
}

var 開くファイルtable [最大開くファイル]開くファイル説明
var プロセスtable [32]プロセスentry
var ローカルsockets [最大sockets]ローカルdatagramソケット
var 次ephemeralポート uint16 = 49152

const (
	利用者heapbase	uint32	= 0x06000000
	利用者heap制限	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdin読込み uint32
var stdin書込み uint32

func I割込み(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sys終了_2(目次 uint32) {
	Syscall(Sys終了, 目次)
}

func Sys読込み_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sys読込み, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sys印刷str(buffer string) {
	h := (*文字列ヘッダ)(Pointer(&buffer))
	Syscall(Sys書込み, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sys印刷unsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sys書込み, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sys開く_2(パス uintptr, フラグ uint32, モード uint32) int32 {
	return int32(Syscall(Sys開く, uint32(パス), フラグ, モード))
}

func Sys閉じる_2(fd uint32) int32 {
	return int32(Syscall(Sys閉じる, fd))
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
		return I割込み(パラメータ[0], 0, 0, 0, 0, 0)
	case 2:
		return I割込み(パラメータ[0], パラメータ[1], 0, 0, 0, 0)
	case 3:
		return I割込み(パラメータ[0], パラメータ[1], パラメータ[2], 0, 0, 0)
	case 4:
		return I割込み(パラメータ[0], パラメータ[1], パラメータ[2], パラメータ[3], 0, 0)
	case 5:
		return I割込み(パラメータ[0], パラメータ[1], パラメータ[2], パラメータ[3], パラメータ[4], 0)
	case 6:
		return I割込み(パラメータ[0], パラメータ[1], パラメータ[2], パラメータ[3], パラメータ[4], パラメータ[5])
	default:
		return syscallエラー(Enosys)
	}
}

func (self *TSyscall) Init(管理者 *T割込み管理者) {
	initファイルdescriptor()

	割込みhandler = 取っ手割込み

	var address uintptr
	address = uintptr(Pointer(&割込みhandler))

	self.T割込みhandler.Init(0x80, uintptr(Pointer(管理者)), address)
}

var 割込みhandler func(uint32) uint32

func 取っ手割込み(esp uint32) uint32 {
	var cpu = (*Tcpu状態)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sys終了:
		sys終了(cpu.Ebx)
		return uint32(uintptr(Pointer(S停止現在の日時スレッド(cpu))))
	case Sysrt終了:
		sys終了(cpu.Ebx)
		return uint32(uintptr(Pointer(S停止現在の日時スレッド(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sys読込み:
		cpu.Eax = uint32(sys読込み(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sys書込み:
		cpu.Eax = uint32(sys書込み(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sys開く:
		cpu.Eax = uint32(sys開く(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sys開く(cpu.Ebx, o作成|o書込み専用|o切り捨て, cpu.Ecx))
		return esp
	case Sys閉じる:
		cpu.Eax = uint32(sys閉じる(int32(cpu.Ebx)))
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
		cpu.Eax = C現在の日時pid()
		return esp
	case Sysgetppid:
		cpu.Eax = C現在の日時parentpid()
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
		cpu.Eax = uint32(sysソケット呼出し(cpu.Ebx, cpu.Ecx))
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
		コンソール_2.MUnsignedinteger32印刷(cpu.Ebx)
		return esp

	default:
		コンソール_2.M印刷xy(([]byte)("sys["), 1, 23)
		コンソール_2.MUnsignedinteger32印刷(esp)
		コンソール_2.M印刷(([]byte)(":"))
		コンソール_2.MUnsignedinteger32印刷(cpu.Eax)
		コンソール_2.M印刷(([]byte)(":"))
		コンソール_2.MUnsignedinteger32印刷(cpu.Ebx)
		コンソール_2.M印刷(([]byte)(":"))
		コンソール_2.MUnsignedinteger32印刷(cpu.Ecx)
		コンソール_2.M印刷(([]byte)(":"))
		コンソール_2.MUnsignedinteger32印刷(cpu.Edx)
		コンソール_2.M印刷(([]byte)("]"))
		cpu.Eax = syscallエラー(Enosys)
		return esp
	}

	return esp
}

func initファイルdescriptor() {
	for i := 0; i < 最大開くファイル; i++ {
		開くファイルtable[i] = 開くファイル説明{}
	}
	for i := 0; i < len(プロセスtable); i++ {
		プロセスtable[i] = プロセスentry{}
	}
	for i := 0; i < len(ローカルsockets); i++ {
		ローカルsockets[i] = ローカルdatagramソケット{}
	}
	次ephemeralポート = 49152
	開くファイルtable[0] = 開くファイル説明{使用中: true, kind: fdkindstdin, フラグ: o読込み専用}
	開くファイルtable[1] = 開くファイル説明{使用中: true, kind: fdkindコンソール, フラグ: o書込み専用}
	開くファイルtable[2] = 開くファイル説明{使用中: true, kind: fdkindコンソール, フラグ: o書込み専用}
}

func 検索プロセス(pid uint32) *プロセスentry {
	for i := 0; i < len(プロセスtable); i++ {
		if プロセスtable[i].使用中 && プロセスtable[i].pid == pid {
			return &プロセスtable[i]
		}
	}
	return nil
}

func initializeプロセスfds(プロセス *プロセスentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		プロセス.fds[fd] = fdentry{使用中: true, 説明: fd}
		開くファイルtable[fd].refs++
	}
}

func ensure現在の日時プロセス() *プロセスentry {
	pid := C現在の日時pid()
	if プロセス := 検索プロセス(pid); プロセス != nil {
		return プロセス
	}
	for i := 0; i < len(プロセスtable); i++ {
		if !プロセスtable[i].使用中 {
			プロセスtable[i] = プロセスentry{
				使用中:		true,
				pid:		pid,
				parent:		C現在の日時parentpid(),
				プログラムbreak:	利用者heapbase,
			}
			initializeプロセスfds(&プロセスtable[i])
			return &プロセスtable[i]
		}
	}
	return nil
}

func get開くファイルfor(プロセス *プロセスentry, fd int32) *開くファイル説明 {
	if プロセス == nil || fd < 0 || fd >= 最大fd || !プロセス.fds[fd].使用中 {
		return nil
	}
	説明 := プロセス.fds[fd].説明
	if 説明 < 0 || 説明 >= 最大開くファイル || !開くファイルtable[説明].使用中 {
		return nil
	}
	return &開くファイルtable[説明]
}

func get開くファイル(fd int32) *開くファイル説明 {
	return get開くファイルfor(ensure現在の日時プロセス(), fd)
}

func allocate開くファイル() int32 {
	for i := int32(3); i < 最大開くファイル; i++ {
		if !開くファイルtable[i].使用中 {
			開くファイルtable[i] = 開くファイル説明{使用中: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(プロセス *プロセスentry, 説明 int32, 最小 int32) int32 {
	if プロセス == nil {
		return Enfile
	}
	if 最小 < 0 || 最小 >= 最大fd {
		return Einval
	}
	for fd := 最小; fd < 最大fd; fd++ {
		if !プロセス.fds[fd].使用中 {
			プロセス.fds[fd] = fdentry{使用中: true, 説明: 説明}
			return fd
		}
	}
	return Emfile
}

func release開くファイル(説明 int32) {
	if 説明 < 0 || 説明 >= 最大開くファイル {
		return
	}
	entry := &開くファイルtable[説明]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && 説明 > stderrfd {
		if entry.kind == fdkindソケット && entry.aux < 最大sockets {
			ローカルsockets[entry.aux] = ローカルdatagramソケット{}
		}
		*entry = 開くファイル説明{}
	}
}

func 閉じるプロセスfd(プロセス *プロセスentry, fd int32) int32 {
	if プロセス == nil || get開くファイルfor(プロセス, fd) == nil {
		return Ebadf
	}
	説明 := プロセス.fds[fd].説明
	プロセス.fds[fd] = fdentry{}
	release開くファイル(説明)
	return 0
}

func sys書込み(fd int32, address uint32, カウント uint32) int32 {
	if カウント == 0 {
		return 0
	}
	if address == 0 || address+カウント < address {
		return Efault
	}
	if カウント > 4096 {
		return Einval
	}
	entry := get開くファイル(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindコンソール {
		if entry.kind == fdkindソケット {
			return ソケット送信to(fd, address, カウント, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindルートディレクトリ {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getバイトからポインタ(uintptr(address), int(カウント), int(カウント))
	コンソール_2.M印刷(buffer)
	return int32(カウント)
}

func sys読込み(fd int32, address uint32, カウント uint32) int32 {
	if カウント == 0 {
		return 0
	}
	if address == 0 || address+カウント < address {
		return Efault
	}
	entry := get開くファイル(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return 読込みstdin(address, カウント)
	}
	if entry.kind == fdkindルートディレクトリ {
		return Eisdir
	}
	if entry.kind == fdkindソケット {
		return ソケットreceiveから(fd, address, カウント, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.配置 >= entry.サイズ {
		return 0
	}
	remaining := entry.サイズ - entry.配置
	if カウント > remaining {
		カウント = remaining
	}
	buffer := Getバイトからポインタ(uintptr(address), int(カウント), int(カウント))
	return 読込みvfsファイル(entry, buffer, カウント)
}

func sys開く(パスaddress uint32, フラグ uint32, モード uint32) int32 {
	_ = モード
	if パスaddress == 0 {
		return Efault
	}
	アクセスモード := フラグ & 3
	if アクセスモード == o書込み専用 || アクセスモード == o読込み書込み || (フラグ&(o作成|o切り捨て|oappend)) != 0 {
		return Erofs
	}

	プロセス := ensure現在の日時プロセス()
	if プロセス == nil {
		return Enfile
	}
	説明 := allocate開くファイル()
	if 説明 < 0 {
		return 説明
	}
	entry := &開くファイルtable[説明]
	entry.フラグ = フラグ
	if isルートパス(パスaddress) {
		entry.kind = fdkindルートディレクトリ
		entry.サイズ = 0
	} else {
		名前len, 名前 := 複製パス(パスaddress)
		if 名前len == 0 {
			*entry = 開くファイル説明{}
			return Enoent
		}
		サイズ := ファイルサイズ(名前[:名前len])
		if サイズ == 0 {
			*entry = 開くファイル説明{}
			return Enoent
		}
		if (フラグ & oディレクトリ) != 0 {
			*entry = 開くファイル説明{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.サイズ = サイズ
		entry.名前len = 名前len
		entry.名前 = 名前
	}

	fd := allocatefd(プロセス, 説明, 3)
	if fd < 0 {
		*entry = 開くファイル説明{}
		return fd
	}
	return fd
}

func sys閉じる(fd int32) int32 {
	return 閉じるプロセスfd(ensure現在の日時プロセス(), fd)
}

func sysdup(fd int32, 最小 int32) int32 {
	プロセス := ensure現在の日時プロセス()
	entry := get開くファイルfor(プロセス, fd)
	if entry == nil {
		return Ebadf
	}
	新規fd := allocatefd(プロセス, プロセス.fds[fd].説明, 最小)
	if 新規fd >= 0 {
		entry.refs++
	}
	return 新規fd
}

func sysdup2(oldfd int32, 新規fd int32) int32 {
	プロセス := ensure現在の日時プロセス()
	entry := get開くファイルfor(プロセス, oldfd)
	if entry == nil {
		return Ebadf
	}
	if 新規fd < 0 || 新規fd >= 最大fd {
		return Ebadf
	}
	if oldfd == 新規fd {
		return 新規fd
	}
	if プロセス.fds[新規fd].使用中 {
		閉じるプロセスfd(プロセス, 新規fd)
	}
	プロセス.fds[新規fd] = fdentry{使用中: true, 説明: プロセス.fds[oldfd].説明}
	entry.refs++
	return 新規fd
}

func sysfcntl(fd int32, コマンド uint32, argument uint32) int32 {
	プロセス := ensure現在の日時プロセス()
	entry := get開くファイルfor(プロセス, fd)
	if entry == nil {
		return Ebadf
	}
	switch コマンド {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(プロセス.fds[fd].fdフラグ)
	case fありfd:
		プロセス.fds[fd].fdフラグ = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.フラグ)
	case fありfl:
		entry.フラグ = (entry.フラグ & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := get開くファイル(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekあり:
		base = 0
	case seek現在の日時:
		base = int64(entry.配置)
	case seek文末:
		base = int64(entry.サイズ)
	default:
		return Einval
	}
	配置_2 := base + int64(offset)
	if 配置_2 < 0 || 配置_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.配置 = uint32(配置_2)
	return int32(entry.配置)
}

func 読込みvfsファイル(entry *開くファイル説明, 転送先_2 []byte, カウント uint32) int32 {
	メモリ管理者 := &mem.Tメモリ管理者{}
	tmpポインタ := メモリ管理者.M記憶領域を確保(entry.サイズ)
	if tmpポインタ == nil {
		return Einval
	}
	tmp := Getバイトからポインタ(uintptr(tmpポインタ), int(entry.サイズ), int(entry.サイズ))
	読込みファイル(entry.名前[:entry.名前len], tmp)
	copy(転送先_2[:カウント], tmp[entry.配置:entry.配置+カウント])
	entry.配置 += カウント
	メモリ管理者.F空き(tmpポインタ)
	return int32(カウント)
}

func isルートパス(パスaddress uint32) bool {
	if パスaddress == 0 {
		return false
	}
	パス := Getバイトからポインタ(uintptr(パスaddress), 4, 4)
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
		名前len, 名前 := 複製パス(パスaddress)
		exists = 名前len != 0 && ファイルサイズ(名前[:名前len]) != 0
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
	buffer_2 := Getバイトからポインタ(uintptr(bufferaddress), int(サイズ), int(サイズ))
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
	名前len, 名前 := 複製パス(パスaddress)
	if 名前len == 0 {
		return Enoent
	}
	サイズ := ファイルサイズ(名前[:名前len])
	if サイズ == 0 {
		return Enoent
	}
	iノード := uint32(2)
	for i := uint32(0); i < 名前len; i++ {
		iノード = iノード*33 + uint32(名前[i])
	}
	return fillposixstat(stataddress, sifreg|0444, サイズ, iノード)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := get開くファイル(fd)
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
	if get開くファイル(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	プロセス := ensure現在の日時プロセス()
	if プロセス == nil {
		return 0
	}
	if プロセス.プログラムbreak == 0 {
		プロセス.プログラムbreak = 利用者heapbase
	}
	if address_2 == 0 {
		return プロセス.プログラムbreak
	}
	if address_2 < 利用者heapbase || address_2 > 利用者heap制限 {
		return プロセス.プログラムbreak
	}
	プロセス.プログラムbreak = address_2
	return プロセス.プログラムbreak
}

func 複製utsfield(転送先 *[65]byte, 値 string) {
	制限 := len(値)
	if 制限 > 64 {
		制限 = 64
	}
	for i := 0; i < 制限; i++ {
		転送先[i] = 値[i]
	}
	転送先[制限] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	名前 := (*posixutsname)(Pointer(uintptr(address_2)))
	*名前 = posixutsname{}
	複製utsfield(&名前.Sysname, "EngOS")
	複製utsfield(&名前.Nodename, "engos")
	複製utsfield(&名前.Release, "0.1-posix")
	複製utsfield(&名前.Vバージョン, "POSIX.1-2017 phase 1")
	複製utsfield(&名前.Machine, "i386")
	return 0
}

func スワップunsignedinteger16(値 uint16) uint16 {
	return (値 << 8) | (値 >> 8)
}

func ソケット呼出しargument(引数_2 uint32, 目次 uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(引数_2 + 目次*4)))
}

func ソケットforfd(fd int32) (*ローカルdatagramソケット, int32) {
	entry := get開くファイル(fd)
	if entry == nil || entry.kind != fdkindソケット || entry.aux >= 最大sockets {
		return nil, Ebadf
	}
	ソケット := &ローカルsockets[entry.aux]
	if !ソケット.使用中 {
		return nil, Ebadf
	}
	return ソケット, 0
}

func allocateソケット(ドメイン uint32, ソケット型 uint32, protocol uint32) int32 {
	if ドメイン != afinet {
		return Eafnosupport
	}
	if ソケット型 != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	プロセス := ensure現在の日時プロセス()
	if プロセス == nil {
		return Enfile
	}
	ソケット目次 := -1
	for i := 0; i < 最大sockets; i++ {
		if !ローカルsockets[i].使用中 {
			ソケット目次 = i
			break
		}
	}
	if ソケット目次 < 0 {
		return Enfile
	}
	説明 := allocate開くファイル()
	if 説明 < 0 {
		return 説明
	}
	ローカルsockets[ソケット目次] = ローカルdatagramソケット{使用中: true}
	entry := &開くファイルtable[説明]
	entry.kind = fdkindソケット
	entry.フラグ = o読込み書込み
	entry.aux = uint32(ソケット目次)
	fd := allocatefd(プロセス, 説明, 3)
	if fd < 0 {
		ローカルsockets[ソケット目次] = ローカルdatagramソケット{}
		*entry = 開くファイル説明{}
		return fd
	}
	return fd
}

func ソケットaddress(address_2 uint32, 長さ uint32) (*ソケットaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if 長さ < 16 {
		return nil, Einval
	}
	生成先 := (*ソケットaddressipv4)(Pointer(uintptr(address_2)))
	if 生成先.Family != afinet {
		return nil, Eafnosupport
	}
	return 生成先, 0
}

func ポート受信ON(ポート uint16, except *ローカルdatagramソケット) bool {
	for i := 0; i < 最大sockets; i++ {
		ソケット := &ローカルsockets[i]
		if ソケット != except && ソケット.使用中 && ソケット.bound && ソケット.ローカル.Pポート == ポート {
			return true
		}
	}
	return false
}

func バインドephemeral(ソケット *ローカルdatagramソケット) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		ポート := スワップunsignedinteger16(次ephemeralポート)
		次ephemeralポート++
		if 次ephemeralポート < 49152 {
			次ephemeralポート = 49152
		}
		if !ポート受信ON(ポート, ソケット) {
			ソケット.ローカル = ソケットaddressipv4{Family: afinet, Pポート: ポート, Address: 0x0100007F}
			ソケット.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func ソケットバインド(fd int32, address_2 uint32, 長さ uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	requested, エラー := ソケットaddress(address_2, 長さ)
	if エラー != 0 {
		return エラー
	}
	if ソケット.bound {
		return Einval
	}
	if requested.Pポート == 0 {
		return バインドephemeral(ソケット)
	}
	if ポート受信ON(requested.Pポート, ソケット) {
		return Eaddrinuse
	}
	ソケット.ローカル = *requested
	ソケット.bound = true
	return 0
}

func ソケット接続(fd int32, address_2 uint32, 長さ uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	リモート, エラー := ソケットaddress(address_2, 長さ)
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

func ソケット送信to(fd int32, bufferaddress_2 uint32, 長さ uint32, 転送先address uint32, 転送先長さ uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	if 長さ > 最大datagramサイズ {
		return Emsgsize
	}
	if 長さ != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var 転送先 ソケットaddressipv4
	if 転送先address != 0 {
		address_2, addressエラー := ソケットaddress(転送先address, 転送先長さ)
		if addressエラー != 0 {
			return addressエラー
		}
		転送先 = *address_2
	} else {
		if !ソケット.connected {
			return Enotconn
		}
		転送先 = ソケット.リモート
	}
	if !ソケット.bound {
		if バインドエラー := バインドephemeral(ソケット); バインドエラー != 0 {
			return バインドエラー
		}
	}
	var receiver *ローカルdatagramソケット
	for i := 0; i < 最大sockets; i++ {
		candidate := &ローカルsockets[i]
		if candidate.使用中 && candidate.bound && candidate.ローカル.Pポート == 転送先.Pポート &&
			(candidate.ローカル.Address == 0 || candidate.ローカル.Address == 転送先.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.カウント >= 最大ソケットパケット {
		return Eagain
	}
	packet := &receiver.パケット[receiver.tail]
	*packet = ソケットpacket{使用中: true, サイズ: 長さ, 転送元: ソケット.ローカル}
	if 長さ != 0 {
		転送元 := Getバイトからポインタ(uintptr(bufferaddress_2), int(長さ), int(長さ))
		copy(packet.データ[:長さ], 転送元)
	}
	receiver.tail = (receiver.tail + 1) % 最大ソケットパケット
	receiver.カウント++
	return int32(長さ)
}

func ソケットreceiveから(fd int32, bufferaddress_2 uint32, 長さ uint32, 転送元address uint32, 転送元長さaddress uint32) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	if 長さ != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if ソケット.カウント == 0 {
		return Eagain
	}
	packet := &ソケット.パケット[ソケット.head]
	複製長さ := packet.サイズ
	if 複製長さ > 長さ {
		複製長さ = 長さ
	}
	if 複製長さ != 0 {
		転送先 := Getバイトからポインタ(uintptr(bufferaddress_2), int(複製長さ), int(複製長さ))
		copy(転送先, packet.データ[:複製長さ])
	}
	if 転送元address != 0 {
		if 転送元長さaddress == 0 {
			return Efault
		}
		provided長さ := (*uint32)(Pointer(uintptr(転送元長さaddress)))
		if *provided長さ >= 16 {
			*(*ソケットaddressipv4)(Pointer(uintptr(転送元address))) = packet.転送元
		}
		*provided長さ = 16
	}
	*packet = ソケットpacket{}
	ソケット.head = (ソケット.head + 1) % 最大ソケットパケット
	ソケット.カウント--
	return int32(複製長さ)
}

func 複製ソケット名前(fd int32, address_2 uint32, 長さaddress uint32, peer bool) int32 {
	ソケット, エラー := ソケットforfd(fd)
	if エラー != 0 {
		return エラー
	}
	if address_2 == 0 || 長さaddress == 0 {
		return Efault
	}
	長さ := (*uint32)(Pointer(uintptr(長さaddress)))
	if *長さ < 16 {
		*長さ = 16
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
	*長さ = 16
	return 0
}

func sysソケット呼出し(呼出し uint32, 引数_2 uint32) int32 {
	if 引数_2 == 0 {
		return Efault
	}
	switch 呼出し {
	case 1:
		return allocateソケット(ソケット呼出しargument(引数_2, 0), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2))
	case 2:
		return ソケットバインド(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2))
	case 3:
		return ソケット接続(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return 複製ソケット名前(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2), false)
	case 7:
		return 複製ソケット名前(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2), true)
	case 9:
		return ソケット送信to(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2), 0, 0)
	case 10:
		return ソケットreceiveから(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2), 0, 0)
	case 11:
		return ソケット送信to(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2), ソケット呼出しargument(引数_2, 4), ソケット呼出しargument(引数_2, 5))
	case 12:
		return ソケットreceiveから(int32(ソケット呼出しargument(引数_2, 0)), ソケット呼出しargument(引数_2, 1), ソケット呼出しargument(引数_2, 2), ソケット呼出しargument(引数_2, 4), ソケット呼出しargument(引数_2, 5))
	case 13:
		if _, エラー := ソケットforfd(int32(ソケット呼出しargument(引数_2, 0))); エラー != 0 {
			return エラー
		}
		return 0
	case 14:
		if _, エラー := ソケットforfd(int32(ソケット呼出しargument(引数_2, 0))); エラー != 0 {
			return エラー
		}
		return 0
	}
	return Eopnotsupp
}

func 読込みstdin(address uint32, カウント uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getバイトからポインタ(uintptr(address), int(カウント), int(カウント))
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
	次 := (stdin書込み + 1) % uint32(len(stdinbuffer))
	if 次 == stdin読込み {
		return
	}
	stdinbuffer[stdin書込み] = c
	stdin書込み = 次
}

func stdingetblocking() byte {
	for stdin読込み == stdin書込み {
		sc := pollキーボードscancode()
		if sc != 0 {
			Stdinputバイト(sc)
		}
	}
	c := stdinbuffer[stdin読込み]
	stdin読込み = (stdin読込み + 1) % uint32(len(stdinbuffer))
	return c
}

func pollキーボードscancode() byte {
	for (Pポート読込みバイト(0x64) & 0x01) == 0 {
	}
	sc := Pポート読込みバイト(0x60)
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

func 複製実行vector(address_2 uint32, 生成先 *実行vector) int32 {
	*生成先 = 実行vector{}
	if address_2 == 0 {
		return 0
	}
	for 目次 := uint32(0); 目次 < 最大実行vectorentry; 目次++ {
		文字列address := *(*uint32)(Pointer(uintptr(address_2 + 目次*4)))
		if 文字列address == 0 {
			生成先.カウント = 目次
			return 0
		}
		terminated := false
		for 長さ := uint32(0); 長さ <= 最大実行文字列長さ; 長さ++ {
			値 := *(*byte)(Pointer(uintptr(文字列address + 長さ)))
			生成先.数値[目次][長さ] = 値
			if 値 == 0 {
				生成先.lengths[目次] = 長さ
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

func push実行unsignedinteger32(積重ね記憶領域 *uint32, 値 uint32) {
	*積重ね記憶領域 -= 4
	*(*uint32)(Pointer(uintptr(*積重ね記憶領域))) = 値
}

func setup実行stack(cpu *Tcpu状態, 引数_2 *実行vector, environment *実行vector) int32 {
	const stackバイト uint32 = 4096
	if !Makerangeプライベートwritable(getcr3(), U利用者stack上-stackバイト, stackバイト) {
		return Enomem
	}
	積重ね記憶領域 := U利用者stack上
	var argumentpointers [最大実行vectorentry]uint32
	var environmentpointers [最大実行vectorentry]uint32

	for i := int(environment.カウント) - 1; i >= 0; i-- {
		長さ := environment.lengths[i] + 1
		積重ね記憶領域 -= 長さ
		転送先 := Getバイトからポインタ(uintptr(積重ね記憶領域), int(長さ), int(長さ))
		copy(転送先, environment.数値[i][:長さ])
		environmentpointers[i] = 積重ね記憶領域
	}
	for i := int(引数_2.カウント) - 1; i >= 0; i-- {
		長さ := 引数_2.lengths[i] + 1
		積重ね記憶領域 -= 長さ
		転送先 := Getバイトからポインタ(uintptr(積重ね記憶領域), int(長さ), int(長さ))
		copy(転送先, 引数_2.数値[i][:長さ])
		argumentpointers[i] = 積重ね記憶領域
	}
	積重ね記憶領域 &= ^uint32(3)
	push実行unsignedinteger32(&積重ね記憶領域, 0)
	for i := int(environment.カウント) - 1; i >= 0; i-- {
		push実行unsignedinteger32(&積重ね記憶領域, environmentpointers[i])
	}
	push実行unsignedinteger32(&積重ね記憶領域, 0)
	for i := int(引数_2.カウント) - 1; i >= 0; i-- {
		push実行unsignedinteger32(&積重ね記憶領域, argumentpointers[i])
	}
	push実行unsignedinteger32(&積重ね記憶領域, 引数_2.カウント)
	cpu.Esp = 積重ね記憶領域
	cpu.Ebp = 0
	return 0
}

func 閉じる時実行(プロセス *プロセスentry) {
	if プロセス == nil {
		return
	}
	for fd := int32(0); fd < 最大fd; fd++ {
		if プロセス.fds[fd].使用中 && (プロセス.fds[fd].fdフラグ&fdcloexec) != 0 {
			閉じるプロセスfd(プロセス, fd)
		}
	}
}

func sysexecve(cpu *Tcpu状態, パスaddress uint32) int32 {
	if パスaddress == 0 {
		return Efault
	}
	var 引数_2 実行vector
	var environment 実行vector
	if 生成先 := 複製実行vector(cpu.Ecx, &引数_2); 生成先 < 0 {
		return 生成先
	}
	if 生成先 := 複製実行vector(cpu.Edx, &environment); 生成先 < 0 {
		return 生成先
	}
	名前len, 名前 := 複製パス(パスaddress)
	if 名前len == 0 {
		return Enoent
	}
	サイズ := ファイルサイズ(名前[:名前len])
	if サイズ == 0 {
		return Enoent
	}
	メモリ管理者 := &mem.Tメモリ管理者{}
	ファイルポインタ := メモリ管理者.M記憶領域を確保(サイズ)
	if ファイルポインタ == nil {
		return Einval
	}
	データ := Getバイトからポインタ(uintptr(ファイルポインタ), int(サイズ), int(サイズ))
	読込みファイル(名前[:名前len], データ)
	if サイズ < 52 || データ[0] != 0x7F || データ[1] != 'E' || データ[2] != 'L' || データ[3] != 'F' {
		メモリ管理者.F空き(ファイルポインタ)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(データ)
	loader.Parse(データ, getcr3())
	メモリ管理者.F空き(ファイルポインタ)
	if 生成先 := setup実行stack(cpu, &引数_2, &environment); 生成先 < 0 {
		return 生成先
	}
	閉じる時実行(ensure現在の日時プロセス())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpu状態) int32 {
	parentpid := C現在の日時pid()
	if ensure現在の日時プロセス() == nil {
		return Enfile
	}
	pid := allocateプロセス(parentpid)
	if pid == 0 {
		return Einval
	}
	メモリ管理者 := &mem.Tメモリ管理者{}
	スレッドポインタ := メモリ管理者.M記憶領域を確保(uint32(Sizeof(Tスレッド{})))
	stackポインタ := メモリ管理者.M記憶領域を確保(Tスレッドstackサイズ)
	childページディレクトリ := Cloneaddressスペースcow(getcr3())
	if スレッドポインタ == nil || stackポインタ == nil || childページディレクトリ == 0 {
		破棄プロセス(pid)
		return Einval
	}
	child := (*Tスレッド)(スレッドポインタ)
	child.Stack = uint32(uintptr(stackポインタ))
	child.Cpu状態 = (*Tcpu状態)(Pointer(uintptr(stackポインタ) + Tスレッドstackサイズ - Sizeof(Tcpu状態{})))
	*child.Cpu状態 = *cpu
	child.Cpu状態.Eax = 0
	child.U利用者stack_2 = cpu.Esp
	child.U利用者stackサイズ_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pページディレクトリentry = childページディレクトリ
	child.Tスレッド状態 = R準備OK
	child.Fpuoffset = 0xffffffff
	child.Is中核 = false
	A追加runnableスレッド(child)
	return int32(pid)
}

func sys終了(状態 uint32) {
	pid := C現在の日時pid()
	for i := 0; i < len(プロセスtable); i++ {
		if プロセスtable[i].使用中 && プロセスtable[i].pid == pid {
			閉じるすべてプロセスfds(&プロセスtable[i])
			プロセスtable[i].終了 = true
			プロセスtable[i].状態 = (状態 & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, 状態address uint32, オプション uint32) int32 {
	if (オプション & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := C現在の日時pid()
	foundchild := false
	for i := 0; i < len(プロセスtable); i++ {
		p := &プロセスtable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.使用中 && matches && p.parent == parentpid {
			foundchild = true
			if p.終了 {
				if 状態address != 0 {
					*(*uint32)(Pointer(uintptr(状態address))) = p.状態
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
	parentプロセス := 検索プロセス(parent)
	pid := Allocatepid()
	for i := 0; i < len(プロセスtable); i++ {
		if !プロセスtable[i].使用中 {
			プロセスtable[i] = プロセスentry{
				使用中:		true,
				pid:		pid,
				parent:		parent,
				プログラムbreak:	利用者heapbase,
			}
			if parentプロセス != nil {
				プロセスtable[i].プログラムbreak = parentプロセス.プログラムbreak
				for fd := 0; fd < 最大fd; fd++ {
					if parentプロセス.fds[fd].使用中 {
						プロセスtable[i].fds[fd] = parentプロセス.fds[fd]
						説明 := parentプロセス.fds[fd].説明
						if 説明 >= 0 && 説明 < 最大開くファイル {
							開くファイルtable[説明].refs++
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

func 閉じるすべてプロセスfds(プロセス *プロセスentry) {
	if プロセス == nil {
		return
	}
	for fd := int32(0); fd < 最大fd; fd++ {
		if プロセス.fds[fd].使用中 {
			閉じるプロセスfd(プロセス, fd)
		}
	}
}

func 破棄プロセス(pid uint32) {
	プロセス := 検索プロセス(pid)
	if プロセス == nil {
		return
	}
	閉じるすべてプロセスfds(プロセス)
	*プロセス = プロセスentry{}
}

func 複製パス(パスaddress uint32) (uint32, [12]byte) {
	var 名前 [12]byte
	if パスaddress == 0 {
		return 0, 名前
	}
	raw := Getバイトからポインタ(uintptr(パスaddress), 64, 64)
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
		名前[n] = c
		n++
	}
	return n, 名前
}

func ファイルサイズ(ファイル名 []byte) uint32 {
	var ata0s = T詳細使用技術attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	区分 := Tmsdos区分table{}
	区分.R読込み区分(&ata0s)

	bios := Tファイル体系設定値32{}
	サイズ := bios.Len(&ata0s, 区分.Mbr.Primary区分[0], ファイル名)
	ata0s.Flush()
	return サイズ
}

func 読込みファイル(ファイル名 []byte, データ []byte) {
	var ata0s = T詳細使用技術attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	区分 := Tmsdos区分table{}
	区分.R読込み区分(&ata0s)

	bios := Tファイル体系設定値32{}
	bios.R読込み(&ata0s, 区分.Mbr.Primary区分[0], ファイル名, データ)
	ata0s.Flush()
}

func getcr3() uint32
