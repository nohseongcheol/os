# EngOS POSIX.1-2017 implementation

EngOS implements POSIX incrementally.  The user ABI uses the Linux i386
register convention (`int 0x80`, system-call number in EAX, arguments in
EBX/ECX/EDX/ESI/EDI/EBP), while the public C API is provided by the
freestanding library in `./uživatelský_prostor/posix`.

This document is a conformance roadmap, not a claim that EngOS is currently a
POSIX-certified system.  Unsupported calls return `-1` with `errno=ENOSYS`, or
a more specific error such as `EROFS` when the limitation is intentional.

## Phase 1: base ABI and read-only files (implemented)

- `errno` translation for negative kernel error results
- `_exit`, `read`, `write`, `close`, `lseek`
- `open`, `creat`, `fcntl`
- `stat`, `lstat`, `fstat`
- `access`, `chdir`, `getcwd`
- `dup`, `dup2`, shared open-file offsets and descriptor flags
- `fork`, `execve`, `wait`, `waitpid` foundations
- `getpid`, `getppid`, UID/GID query functions
- `brk`, `sbrk`, `fsync`, `sync`, `isatty`, `uname`
- POSIX-facing headers for types, file flags, status, process waiting and
  system identity

File descriptors and the program break are maintained per process. `fork`
uses copy-on-write address spaces and inherits open-file descriptions;
`execve` constructs `argc`/`argv`/`envp`, initializes libc `environ`, and
honors `FD_CLOEXEC`. Blocking `wait` is provided by libc retrying the kernel
wait operation; a scheduler-native wait queue remains a performance follow-up.

Current filesystem restrictions: FAT access is root-directory, read-only and
8.3-name based. `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_TRUNC` and `O_APPEND`
therefore return `EROFS`.

## IPv4 UDP local sockets (implemented)

The i386 `socketcall` ABI is wired into the same per-process file-descriptor
table. The C library provides `socket`, `bind`, `connect`, `send`, `sendto`,
`recv`, `recvfrom`, address queries, `shutdown`, and byte-order helpers. The
current transport is an in-kernel IPv4 UDP datagram path between guest
processes. Empty receive queues return `EAGAIN`.

This is not external networking yet: the legacy PCnet/ARP/IPv4/ICMP/UDP
driver packages compile but are not connected to the default boot path. TCP,
host routing, DNS, readiness polling, and blocking socket waits remain future
work.

## Phase 2: writable VFS and directories

- VFS vnode/mount layers and writable open-file operations
- FAT create, truncate, append, allocation, unlink, rename and metadata update
- `mkdir`, `rmdir`, `unlink`, `rename`, `link`, `chmod`, `umask`
- directory streams and `getdents` backing for `opendir/readdir/closedir`
- pipes and atomic `PIPE_BUF` writes

## Phase 3: process control, signals and time

- scheduler wait queues and fully blocking `waitpid`, pipe and terminal I/O
- process groups, sessions and controlling terminals
- signal masks, actions, delivery frames and `kill`
- monotonic/realtime clocks, `nanosleep`, interval timers and `times`

## Phase 4: memory, terminal and networking (partially implemented)

- `mmap`, `munmap`, `mprotect`, shared mappings and POSIX shared memory
- termios, canonical/non-canonical TTY input and job control
- connect the implemented IPv4/UDP socket descriptors to PCnet; then add TCP
- `select`, `poll` and descriptor readiness

## Phase 5: pthread and remaining POSIX libraries

- pthread lifecycle, TLS, mutexes, condition variables and cancellation
- semaphores, message queues and synchronization objects
- locale, regex, glob, word expansion and remaining POSIX utility APIs
- automated conformance tests and documented deviations

## Build and test

```sh
cd ./uživatelský_prostor/posix
make clean all check
make runtime
```

The resulting library is `build/libengos_posix.a`. Include headers with
`-I./uživatelský_prostor/posix/deklarace` and link the archive into an EngOS i386 user
program. `tests/runtime.c` is the kernel/libc integration smoke test and
`tests/socket_runtime.c` verifies UDP socket calls from a user ELF.

The full phase-1 verification report, including known failing cases, is
`./uživatelský_prostor/posix/TEST_RESULTS.md`. Build all runtime test executables
with `make test-programs`.
