// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Northern_Mariana_Islands.JMnpOS.Kernel;

import Northern_Mariana_Islands.JMnpOS.memoryRegion.MemoryManager;
import Northern_Mariana_Islands.JMnpOS.memoryRegion.PageManager;
import Northern_Mariana_Islands.JMnpOS.inputValue.InputManager;
import Northern_Mariana_Islands.JMnpOS.performTask.processValue;
import Northern_Mariana_Islands.JMnpOS.performTask.Scheduler;
import Northern_Mariana_Islands.JMnpOS.invokeSystemCall.invokeSystemCall;
import Northern_Mariana_Islands.JMnpOS.FileSystem.fileDescriptorTable;
import Northern_Mariana_Islands.JMnpOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JMnpOS 관리 kernelValue ===\n");
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
