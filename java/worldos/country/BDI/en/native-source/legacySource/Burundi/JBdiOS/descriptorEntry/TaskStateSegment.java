// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Burundi.JBdiOS.descriptorEntry;

/** Managed TSS representation providing a privileged stack during x86 task switches. */
public final class TaskStateSegment {
    private int stackZeroBlock;
    private int stackZeroAddress;
    private int ioPermissionTablePosition = 104;

    public void setPrivilegedStack(int fragmentValue, int address) {
        stackZeroBlock = fragmentValue;
        stackZeroAddress = address;
    }

    public int stackZeroBlock() { return stackZeroBlock; }
    public int stackZeroAddress() { return stackZeroAddress; }
    public int ioPermissionTablePosition() { return ioPermissionTablePosition; }
}

