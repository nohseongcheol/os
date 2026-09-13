# VirtualBox crash logging

The kernel mirrors every VGA console message to COM1. VirtualBox captures COM1
as the host-side text file `build/virtualbox-current.log`, so a crash remains available
after the guest display freezes.

## Run and collect

The VM must be powered off when its UART configuration is changed.

```sh
make vbox
make vbox-log
```

`make vbox` rebuilds the ISO, configures COM1 (`0x3f8`, IRQ 4), clears the old
capture and starts the registered VM named `worldos ETH`. Override the
name when necessary:

```sh
make vbox VM_NAME='another VM name'
```

After a fault, generate a symbolized report with:

```sh
make diagnose
```

The raw exception record includes the vector, error code, EIP, CS, EFLAGS,
CR0, CR3, and (for page faults) CR2 plus decoded access flags. Exceptions from
user mode also include the previous ESP and SS. `make diagnose` resolves each
recorded EIP against `build/kernel.bin`, which is the first place Codex should
look when investigating the crash. If no exception exists, it reports that fact
and shows only the most recent guest output instead of dumping the entire log.
