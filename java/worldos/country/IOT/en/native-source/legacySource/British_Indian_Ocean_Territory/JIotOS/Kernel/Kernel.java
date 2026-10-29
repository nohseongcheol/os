// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package British_Indian_Ocean_Territory.JIotOS.Kernel;

import British_Indian_Ocean_Territory.JIotOS.memoryRegion.MemoryManager;
import British_Indian_Ocean_Territory.JIotOS.memoryRegion.PageManager;
import British_Indian_Ocean_Territory.JIotOS.inputValue.InputManager;
import British_Indian_Ocean_Territory.JIotOS.performTask.processValue;
import British_Indian_Ocean_Territory.JIotOS.performTask.Scheduler;
import British_Indian_Ocean_Territory.JIotOS.invokeSystemCall.invokeSystemCall;
import British_Indian_Ocean_Territory.JIotOS.FileSystem.fileDescriptorTable;
import British_Indian_Ocean_Territory.JIotOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JIotOS 관리 kernelValue ===\n");
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
