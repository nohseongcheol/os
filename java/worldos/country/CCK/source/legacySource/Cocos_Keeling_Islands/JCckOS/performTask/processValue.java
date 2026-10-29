// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cocos_Keeling_Islands.JCckOS.performTask;

import Cocos_Keeling_Islands.JCckOS.memoryRegion.PageManager;
import Cocos_Keeling_Islands.JCckOS.FileSystem.fileDescriptorTable;

public final class processValue {
    private final int identifierValue;
    private final int parentIdentifier;
    private final PageManager.AddressSpace AddressSpace;
    private final fileDescriptorTable fileDescriptor;
    private processState stateValue = processState.prepare;
    private int exitCode;
    private int programBreak = 0x06000000;
    private int executionStartAddress;
    private String[] executionArgument = new String[0];
    private String[] environmentValue = new String[0];

    processValue(int identifierValue, int parentIdentifier, PageManager.AddressSpace AddressSpace, fileDescriptorTable fileDescriptor) {
        this.identifierValue = identifierValue;
        this.parentIdentifier = parentIdentifier;
        this.AddressSpace = AddressSpace;
        this.fileDescriptor = fileDescriptor;
    }

    public int identifierValue() {
        return identifierValue;
    }

    public int parentIdentifier() {
        return parentIdentifier;
    }

    public PageManager.AddressSpace AddressSpace() {
        return AddressSpace;
    }

    public fileDescriptorTable fileDescriptor() {
        return fileDescriptor;
    }

    public processState stateValue() {
        return stateValue;
    }

    public void setState(processState newState) {
        stateValue = newState;
    }

    public int exitCode() {
        return exitCode;
    }

    public void exitProgram(int value) {
        exitCode = value & 0xff;
        stateValue = processState.exitProgram;
    }

    public int programBreak() {
        return programBreak;
    }

    public void setProgramBreak(int newEnd) {
        if (newEnd < 0x06000000 || newEnd > 0x07000000) {
            throw new IllegalArgumentException("Program ending 범위를 벗어났습니다.");
        }
        programBreak = newEnd;
    }

    public void setExecutionContext(int startAddress, String[] parameterArgument, String[] environment) {
        executionStartAddress = startAddress;
        executionArgument = parameterArgument.clone();
        environmentValue = environment.clone();
    }

    public int executionStartAddress() { return executionStartAddress; }
    public String[] executionArgument() { return executionArgument.clone(); }
    public String[] environmentValue() { return environmentValue.clone(); }
}
