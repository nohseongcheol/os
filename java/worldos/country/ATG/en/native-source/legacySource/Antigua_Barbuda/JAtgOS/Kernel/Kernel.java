// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Antigua_Barbuda.JAtgOS.Kernel;

import Antigua_Barbuda.JAtgOS.memoryRegion.MemoryManager;
import Antigua_Barbuda.JAtgOS.memoryRegion.PageManager;
import Antigua_Barbuda.JAtgOS.inputValue.InputManager;
import Antigua_Barbuda.JAtgOS.performTask.processValue;
import Antigua_Barbuda.JAtgOS.performTask.Scheduler;
import Antigua_Barbuda.JAtgOS.invokeSystemCall.invokeSystemCall;
import Antigua_Barbuda.JAtgOS.FileSystem.fileDescriptorTable;
import Antigua_Barbuda.JAtgOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JAtgOS 관리 kernelValue ===\n");
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
