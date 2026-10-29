// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hong_Kong_SAR_China.JHkgOS.Kernel;

import Hong_Kong_SAR_China.JHkgOS.memoryRegion.MemoryManager;
import Hong_Kong_SAR_China.JHkgOS.memoryRegion.PageManager;
import Hong_Kong_SAR_China.JHkgOS.inputValue.InputManager;
import Hong_Kong_SAR_China.JHkgOS.performTask.processValue;
import Hong_Kong_SAR_China.JHkgOS.performTask.Scheduler;
import Hong_Kong_SAR_China.JHkgOS.invokeSystemCall.invokeSystemCall;
import Hong_Kong_SAR_China.JHkgOS.FileSystem.fileDescriptorTable;
import Hong_Kong_SAR_China.JHkgOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JHkgOS 관리 kernelValue ===\n");
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
