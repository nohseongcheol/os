# EngOS POSIX phase-1 verification

Date: 2026-09-08

## Scope

This verifies all 49 C functions currently declared by the phase-1 and local
UDP socket headers in `include/`. It does not claim coverage of every interface in POSIX.1-2017;
EngOS has not implemented the remaining standard interfaces yet.

The tests use the current EngOS kernel ISO and copies of the FAT test disk.
The VirtualBox VDI is not modified.

## Build and ABI results

- The library and every test compile with `-Wall -Wextra -Werror -nostdinc`.
- All 32 public declarations have definitions in `libengos_posix.a`.
- The test executables link as static i386 ELF files with the EngOS `crt0`.

```sh
cd .
make clean all check test-programs
```

## Runtime results after fixes

| Test | Result | Coverage |
| --- | --- | --- |
| Core API | PASS (84 checks) | files, paths, descriptors, identity, errors, permissions, `.bss` |
| Standard input | PASS | blocking `read()` with injected `a` and Enter |
| Process control | PASS | COW, child PID/PPID, `_exit`, blocking `wait`/`waitpid`, status |
| Descriptor inheritance | PASS | child close isolation and shared open description |
| Repeated fork | PASS | five sequential fork/wait cycles in one boot |
| Heap | PASS | grow, write, shrink, and per-process break isolation |
| Exec | PASS | image replacement, `argc/argv`, `envp/environ`, `FD_CLOEXEC` |
| IPv4 UDP local sockets | PASS (11 checks) | descriptors, bind/connect, datagrams, addresses, errors, close |

No test log contains `PTEST:FAIL`, `EXCEPTION`, `HALTED`, `panic`, or `fatal`.

## Resolved defects

1. Page fault vector 0x0E now enters the recoverable paging handler, allowing
   copy-on-write faults to resume with `IRET`.
2. COW tracks the complete 512 MiB physical range, handles already-COW pages,
   and copies high physical frames through their mapped virtual address.
3. The kernel allocator's complete 0-48 MiB range is shared by every address
   space, preventing corruption after repeated forks.
4. PID allocation is shared by initial processes and fork-created children.
5. File descriptor tables and program breaks are per-process. Fork inherits
   descriptors and open descriptions correctly; closing in a child does not
   close the parent's descriptor.
6. `wait()` and `waitpid()` expose blocking behavior through the libc wrapper,
   while `WNOHANG` and `ECHILD` retain their non-blocking/error behavior.
7. `execve()` validates ELF input, copies arguments before replacing the
   image, creates the initial user stack, initializes `environ`, and applies
   close-on-exec descriptor flags.
8. `brk()`/`sbrk()` use a mapped 16 MiB per-process heap window and enforce its
   bounds.
9. ELF `SHT_NOBITS` sections such as `.bss` are now explicitly zero-filled.
10. `access(X_OK)` now honors the exposed mode bits.

## Test programs

- `tests/runtime.c`: core API, permissions, errno, and `.bss`
- `tests/stdin_runtime.c`: blocking stdin
- `tests/exec_runtime.c`, `tests/exec_target.c`: exec stack and close-on-exec
- `tests/heap_runtime.c`: usable and process-isolated heap
- `tests/fork_runtime.c`: COW, waits, descriptors, repeated fork
- `tests/socket_runtime.c`: IPv4 UDP guest-local socket calls

Final logs:

- `/tmp/engos-posix-core-final-fixed.log`
- `/tmp/engos-posix-fork-stress-final3.log`
- `/tmp/engos-posix-heap-final-fixed.log`
- `/tmp/engos-posix-exec-final-fixed.log`
- `/tmp/engos-posix-stdin-final-fixed3.log`
- `/tmp/engos-posix-net.log`

## Remaining scope

All phase-1 wrappers now pass their available runtime suite. This is not full
POSIX.1-2017 conformance: writable filesystem operations, signals, clocks,
pipes, process groups, terminals, external networking/TCP, pthreads, and the other roadmap
phases remain to be implemented. Blocking waits currently retry the kernel
wait operation from libc; scheduler wait queues remain a performance follow-up.
