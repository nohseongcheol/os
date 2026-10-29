// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ethiopia.JEthOS.Kernel;

import Ethiopia.JEthOS.memoryRegion.MemoryManager;
import Ethiopia.JEthOS.memoryRegion.PageManager;
import Ethiopia.JEthOS.inputValue.InputManager;
import Ethiopia.JEthOS.performTask.processValue;
import Ethiopia.JEthOS.performTask.Scheduler;
import Ethiopia.JEthOS.invokeSystemCall.invokeSystemCall;
import Ethiopia.JEthOS.FileSystem.fileDescriptorTable;
import Ethiopia.JEthOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JEthOS 관리 kernelValue ===\n");
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
