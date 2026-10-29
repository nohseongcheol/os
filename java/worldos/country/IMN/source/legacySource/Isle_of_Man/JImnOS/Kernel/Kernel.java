// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isle_of_Man.JImnOS.Kernel;

import Isle_of_Man.JImnOS.memoryRegion.MemoryManager;
import Isle_of_Man.JImnOS.memoryRegion.PageManager;
import Isle_of_Man.JImnOS.inputValue.InputManager;
import Isle_of_Man.JImnOS.performTask.processValue;
import Isle_of_Man.JImnOS.performTask.Scheduler;
import Isle_of_Man.JImnOS.invokeSystemCall.invokeSystemCall;
import Isle_of_Man.JImnOS.FileSystem.fileDescriptorTable;
import Isle_of_Man.JImnOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JImnOS 관리 kernelValue ===\n");
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
