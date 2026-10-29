// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_S_Outlying_Islands.JUmiOS.Kernel;

import U_S_Outlying_Islands.JUmiOS.memoryRegion.MemoryManager;
import U_S_Outlying_Islands.JUmiOS.memoryRegion.PageManager;
import U_S_Outlying_Islands.JUmiOS.inputValue.InputManager;
import U_S_Outlying_Islands.JUmiOS.performTask.processValue;
import U_S_Outlying_Islands.JUmiOS.performTask.Scheduler;
import U_S_Outlying_Islands.JUmiOS.invokeSystemCall.invokeSystemCall;
import U_S_Outlying_Islands.JUmiOS.FileSystem.fileDescriptorTable;
import U_S_Outlying_Islands.JUmiOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JUmiOS 관리 kernelValue ===\n");
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
