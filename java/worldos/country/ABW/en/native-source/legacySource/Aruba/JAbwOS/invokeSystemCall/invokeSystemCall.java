// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aruba.JAbwOS.invokeSystemCall;

import Aruba.JAbwOS.memoryRegion.PageManager;
import Aruba.JAbwOS.performTask.processValue;
import Aruba.JAbwOS.performTask.Scheduler;
import Aruba.JAbwOS.FileSystem.ExecutableLoader;
import Aruba.JAbwOS.FileSystem.FileSystem;
import Aruba.JAbwOS.FileSystem.fileInformation;
import Aruba.JAbwOS.Kernel.hardwareValue;
import Aruba.JAbwOS.inputValue.InputManager;
import Aruba.JAbwOS.inputValue.inputEvent;

/** Java management layer for the first stage of engos POSIX calls. */
public final class invokeSystemCall {
    public static final int readOnlyFlag = 0;
    public static final int searchStart = 0;
    public static final int searchCurrent = 1;
    public static final int findEntryEnd = 2;

    private final FileSystem FileSystem;
    private final PageManager pageManagement;
    private final Scheduler Scheduler;
    private final ExecutableLoader loader = new ExecutableLoader();
    private final hardwareValue deviceValue;
    private final InputManager InputManagement;

    public invokeSystemCall(FileSystem FileSystem, PageManager pageManagement, Scheduler Scheduler, hardwareValue deviceValue, InputManager InputManagement) {
        this.FileSystem = FileSystem;
        this.pageManagement = pageManagement;
        this.Scheduler = Scheduler;
        this.deviceValue = deviceValue;
        this.InputManagement = InputManagement;
    }

    public int processIdentifier(processValue currentProcess) {
        return currentProcess.identifierValue();
    }

    public int parentProcessIdentifier(processValue currentProcess) {
        return currentProcess.parentIdentifier();
    }

    public int open(processValue currentProcess, String name, int flagValue) {
        if (flagValue != readOnlyFlag) {
            return -30;
        }
        return currentProcess.fileDescriptor().open(name);
    }

    public int read(processValue currentProcess, int descriptorEntry, byte[] receiveDestination, int size) {
        if (descriptorEntry == 0) {
            if (size <= 0 || receiveDestination.length == 0) {
                return 0;
            }
            inputEvent event = InputManagement.nextEvent();
            if (event == null || event.eventKind() != inputEvent.kindValue.keyDown) {
                return -11;
            }
            receiveDestination[0] = (byte) event.firstValue();
            return 1;
        }
        return currentProcess.fileDescriptor().read(descriptorEntry, receiveDestination, size);
    }

    public int write(processValue currentProcess, int descriptorEntry, byte[] data, int size) {
        if (descriptorEntry != 1 && descriptorEntry != 2) {
            return currentProcess.fileDescriptor().isOpen(descriptorEntry) ? -30 : -9;
        }
        if (size < 0 || size > data.length) {
            return -22;
        }
        deviceValue.serialOutput(new String(data, 0, size, java.nio.charset.StandardCharsets.UTF_8));
        return size;
    }

    public int close(processValue currentProcess, int descriptorEntry) {
        return currentProcess.fileDescriptor().close(descriptorEntry);
    }

    public int movePosition(processValue currentProcess, int descriptorEntry, int distanceValue, int projectRoot) {
        return currentProcess.fileDescriptor().movePosition(descriptorEntry, distanceValue, projectRoot);
    }

    public int duplicateDescriptor(processValue currentProcess, int descriptorEntry) {
        return currentProcess.fileDescriptor().clonedDescriptor(descriptorEntry, 0);
    }

    public int duplicateDescriptorAt(processValue currentProcess, int descriptorEntry, int newDescriptor) {
        return currentProcess.fileDescriptor().duplicateAt(descriptorEntry, newDescriptor);
    }

    public int isAccessible(String name, int methodMode) {
        fileInformation systemInformation = FileSystem.systemInformation(name);
        if (systemInformation == null) {
            return -2;
        }
        if ((methodMode & 1) != 0 && (systemInformation.shapeKind() & 0111) == 0) {
            return -13;
        }
        if ((methodMode & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int switchTaskList(String name) {
        return "/".equals(name) ? 0 : -20;
    }

    public String currentTaskList(int receiveSize) {
        return receiveSize >= 2 ? "/" : null;
    }

    public int userIdentifier() { return 0; }
    public int effectiveUserIdentifier() { return 0; }
    public int groupIdentifier() { return 0; }
    public int effectiveGroupIdentifier() { return 0; }

    public int synchronizeFile(processValue currentProcess, int descriptorEntry) {
        return currentProcess.fileDescriptor().systemInformation(descriptorEntry) == null ? -9 : 0;
    }

    public void synchronizeAll() {
        // The current filesystem is read-only, so there is no data to flush.
    }

    public boolean isTerminal(processValue currentProcess, int descriptorEntry) {
        fileInformation systemInformation = currentProcess.fileDescriptor().systemInformation(descriptorEntry);
        return systemInformation != null && (systemInformation.shapeKind() & 0170000) == 0020000;
    }

    public int file_control(processValue currentProcess, int descriptorEntry, int command, int parameterArgument) {
        if (command == 0) {
            return currentProcess.fileDescriptor().clonedDescriptor(descriptorEntry, parameterArgument);
        }
        if (command == 1) {
            return currentProcess.fileDescriptor().closeOnExecValue(descriptorEntry);
        }
        if (command == 2) {
            return currentProcess.fileDescriptor().setCloseOnExec(descriptorEntry, (parameterArgument & 1) != 0);
        }
        if (command == 3) {
            return currentProcess.fileDescriptor().systemInformation(descriptorEntry) == null ? -9 : readOnlyFlag;
        }
        if (command == 4) {
            return parameterArgument == readOnlyFlag ? 0 : -30;
        }
        return -22;
    }

    public int createEntry(String name, int permissionValue) {
        return -30;
    }

    public fileInformation descriptorInformation(processValue currentProcess, int descriptorEntry) {
        return currentProcess.fileDescriptor().systemInformation(descriptorEntry);
    }

    public systemDetails systemDetails() {
        return new systemDetails("JAbwOS", "JAbwOS", "0.1", "Java managed kernel", "i386");
    }

    public fileInformation fileInformation(String name) {
        return FileSystem.systemInformation(name);
    }

    public processValue cloneProcess(processValue parentValue) {
        return Scheduler.cloneValue(parentValue);
    }

    public int waitForChild(processValue parentValue, int childIdentifier, boolean nonBlocking) {
        return Scheduler.waitForChild(parentValue, childIdentifier, nonBlocking);
    }

    public int programBreak(processValue currentProcess, int newEnd) {
        int previousEnd = currentProcess.programBreak();
        if (newEnd == 0) {
            return previousEnd;
        }
        if (newEnd < 0x06000000 || newEnd > 0x07000000) {
            return -12;
        }
        int firstPage = previousEnd / PageManager.pageSize;
        int lastPage = (newEnd + PageManager.pageSize - 1) / PageManager.pageSize;
        if (newEnd > previousEnd) {
            for (int index = firstPage; index < lastPage; index++) {
                int address = index * PageManager.pageSize;
                try {
                    pageManagement.readByteValue(currentProcess.AddressSpace(), address);
                } catch (IllegalStateException error) {
                    pageManagement.mapPage(currentProcess.AddressSpace(), address, true);
                }
            }
        }
        currentProcess.setProgramBreak(newEnd);
        return newEnd;
    }

    public int increaseProgramBreak(processValue currentProcess, int incrementAmount) {
        int previousEnd = currentProcess.programBreak();
        int result = programBreak(currentProcess, previousEnd + incrementAmount);
        return result < 0 ? result : previousEnd;
    }

    public int executeCommand(processValue currentProcess, byte[] executableFile) {
        return executeCommand(currentProcess, executableFile, new String[0], new String[0]);
    }

    public int executeCommand(processValue currentProcess, byte[] executableFile, String[] parameterArgument, String[] environment) {
        ExecutableLoader.image imageValue;
        try {
            imageValue = loader.Checks(executableFile);
        } catch (IllegalArgumentException error) {
            return -8;
        }
        if (parameterArgument == null || environment == null || parameterArgument.length > 16 || environment.length > 16) {
            return -7;
        }
        for (ExecutableLoader.sectionValue sectionValue : imageValue.sectionsList()) {
            if ((sectionValue.flagValue() & 2) == 0 || sectionValue.size() == 0) {
                continue;
            }
            int firstPage = sectionValue.address() / PageManager.pageSize;
            int lastPage = (sectionValue.address() + sectionValue.size() + PageManager.pageSize - 1) / PageManager.pageSize;
            for (int index = firstPage; index < lastPage; index++) {
                int address = index * PageManager.pageSize;
                try {
                    pageManagement.readByteValue(currentProcess.AddressSpace(), address);
                    pageManagement.privateRangeWrite(currentProcess.AddressSpace(), address, PageManager.pageSize);
                } catch (IllegalStateException error) {
                    pageManagement.mapPage(currentProcess.AddressSpace(), address, true);
                }
            }
            for (int index = 0; index < sectionValue.size(); index++) {
                byte value = sectionValue.kindValue() == 8 ? 0 : executableFile[sectionValue.filePosition() + index];
                pageManagement.writeByteValue(currentProcess.AddressSpace(), sectionValue.address() + index, value);
            }
        }
        currentProcess.setExecutionContext(imageValue.startAddress(), parameterArgument, environment);
        currentProcess.fileDescriptor().closeOnExec();
        return 0;
    }

    public void quitProgram(processValue currentProcess, int stateValue) {
        currentProcess.exitProgram(stateValue);
    }
}
