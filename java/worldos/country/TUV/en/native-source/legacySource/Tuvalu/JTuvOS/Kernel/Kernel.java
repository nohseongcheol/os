// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tuvalu.JTuvOS.Kernel;

import Tuvalu.JTuvOS.memoryRegion.MemoryManager;
import Tuvalu.JTuvOS.memoryRegion.PageManager;
import Tuvalu.JTuvOS.inputValue.InputManager;
import Tuvalu.JTuvOS.performTask.processValue;
import Tuvalu.JTuvOS.performTask.Scheduler;
import Tuvalu.JTuvOS.invokeSystemCall.invokeSystemCall;
import Tuvalu.JTuvOS.FileSystem.fileDescriptorTable;
import Tuvalu.JTuvOS.FileSystem.FileSystem;

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
        deviceValue.serialOutput("=== JTuvOS 관리 kernelValue ===\n");
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
