// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package South_Georgia_South_Sandwich_Islands.JSgsOS.Kernel;

import South_Georgia_South_Sandwich_Islands.JSgsOS.memoryRegion.MemoryManager;
import South_Georgia_South_Sandwich_Islands.JSgsOS.memoryRegion.PageManager;
import South_Georgia_South_Sandwich_Islands.JSgsOS.inputValue.InputManager;
import South_Georgia_South_Sandwich_Islands.JSgsOS.performTask.processValue;
import South_Georgia_South_Sandwich_Islands.JSgsOS.performTask.Scheduler;
import South_Georgia_South_Sandwich_Islands.JSgsOS.invokeSystemCall.invokeSystemCall;
import South_Georgia_South_Sandwich_Islands.JSgsOS.FileSystem.fileDescriptorTable;
import South_Georgia_South_Sandwich_Islands.JSgsOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JSgsOS 관리 kernelValue ===\n");
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
