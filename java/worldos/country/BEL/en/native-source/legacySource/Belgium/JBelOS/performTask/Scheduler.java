// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belgium.JBelOS.performTask;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Belgium.JBelOS.memoryRegion.PageManager;
import Belgium.JBelOS.FileSystem.fileDescriptorTable;

/** Manages process identifiers and a round-robin ready queue. */
public final class Scheduler {
    private final PageManager pageManagement;
    private final Map<Integer, processValue> processList = new HashMap<Integer, processValue>();
    private final Queue<processValue> readyQueue = new ArrayDeque<processValue>();
    private int nextIdentifier = 1;

    public Scheduler(PageManager pageManagement) {
        this.pageManagement = pageManagement;
    }

    public processValue firstProcess(fileDescriptorTable fileDescriptor) {
        processValue newProcess = new processValue(allocateIdentifier(), 0, pageManagement.newAddressSpace(), fileDescriptor);
        processList.put(Integer.valueOf(newProcess.identifierValue()), newProcess);
        readyQueue.offer(newProcess);
        return newProcess;
    }

    public processValue cloneValue(processValue parentValue) {
        processValue childValue = new processValue(
                allocateIdentifier(),
                parentValue.identifierValue(),
                pageManagement.cloneCopyOnWrite(parentValue.AddressSpace()),
                parentValue.fileDescriptor().cloneValue());
        childValue.setProgramBreak(parentValue.programBreak());
        processList.put(Integer.valueOf(childValue.identifierValue()), childValue);
        readyQueue.offer(childValue);
        return childValue;
    }

    public processValue nextProcess() {
        int checkCount = readyQueue.size();
        for (int index = 0; index < checkCount; index++) {
            processValue nextItem = readyQueue.poll();
            if (nextItem != null && (nextItem.stateValue() == processState.prepare || nextItem.stateValue() == processState.executeCommand)) {
                nextItem.setState(processState.executeCommand);
                readyQueue.offer(nextItem);
                return nextItem;
            }
        }
        return null;
    }

    public int waitForChild(processValue parentValue, int childIdentifier, boolean nonBlocking) {
        for (processValue candidate : processList.values()) {
            if (candidate.parentIdentifier() != parentValue.identifierValue()) {
                continue;
            }
            if (childIdentifier > 0 && candidate.identifierValue() != childIdentifier) {
                continue;
            }
            if (candidate.stateValue() == processState.exitProgram) {
                int result = (candidate.exitCode() & 0xff) << 8;
                processList.remove(Integer.valueOf(candidate.identifierValue()));
                return result;
            }
            return nonBlocking ? 0 : -11;
        }
        return -10;
    }

    public processValue findProcess(int identifierValue) {
        return processList.get(Integer.valueOf(identifierValue));
    }

    private int allocateIdentifier() {
        return nextIdentifier++;
    }
}
