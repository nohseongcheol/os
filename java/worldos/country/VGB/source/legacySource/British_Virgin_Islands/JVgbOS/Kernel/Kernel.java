// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package British_Virgin_Islands.JVgbOS.Kernel;

import British_Virgin_Islands.JVgbOS.memoryRegion.MemoryManager;
import British_Virgin_Islands.JVgbOS.memoryRegion.PageManager;
import British_Virgin_Islands.JVgbOS.inputValue.InputManager;
import British_Virgin_Islands.JVgbOS.performTask.processValue;
import British_Virgin_Islands.JVgbOS.performTask.Scheduler;
import British_Virgin_Islands.JVgbOS.invokeSystemCall.invokeSystemCall;
import British_Virgin_Islands.JVgbOS.FileSystem.fileDescriptorTable;
import British_Virgin_Islands.JVgbOS.FileSystem.FileSystem;

/** Assembles and starts the Java-managed kernel. */
public final class Kernel {
    private final hardwareValue deviceValue;
    private final MemoryManager memoryRegion = new MemoryManager(32 * 1024 * 1024);
    private final PageManager pageManagement = new PageManager();
    private final FileSystem FileSystem = new FileSystem();
    private final Scheduler Scheduler = new Scheduler(pageManagement);
    private final InputManager InputManagement = new InputManager(256);
    private final processValue firstProcess;
    private final invokeSystemCall invokeSystemCall;

    public Kernel(hardwareValue deviceValue) {
        this.deviceValue = deviceValue;
        firstProcess = Scheduler.firstProcess(new fileDescriptorTable(FileSystem));
        invokeSystemCall = new invokeSystemCall(FileSystem, pageManagement, Scheduler, deviceValue, InputManagement);
    }

    public void run() {
        deviceValue.serialOutput("=== JVgbOS 관리 kernelValue ===\n");
    }

    public void executeStep() {
        deviceValue.haltCpu();
    }

    public MemoryManager memoryRegion() {
        return memoryRegion;
    }

    public PageManager pageManagement() {
        return pageManagement;
    }

    public FileSystem FileSystem() {
        return FileSystem;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public InputManager InputManagement() {
        return InputManagement;
    }

    public processValue firstProcess() {
        return firstProcess;
    }

    public invokeSystemCall invokeSystemCall() {
        return invokeSystemCall;
    }
}
