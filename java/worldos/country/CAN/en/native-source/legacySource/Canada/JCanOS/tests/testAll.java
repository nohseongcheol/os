// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.tests;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Canada.JCanOS.memoryRegion.MemoryManager;
import Canada.JCanOS.memoryRegion.PageManager;
import Canada.JCanOS.inputValue.inputEvent;
import Canada.JCanOS.performTask.processValue;
import Canada.JCanOS.invokeSystemCall.invokeSystemCall;
import Canada.JCanOS.FileSystem.ExecutableLoader;
import Canada.JCanOS.Kernel.Kernel;
import Canada.JCanOS.Host.HostHardware;
import Canada.JCanOS.interrupt.InterruptManager;
import Canada.JCanOS.descriptorEntry.GlobalDescriptorTable;
import Canada.JCanOS.storageDevice.AdvancedTechnologyAttachment;
import Canada.JCanOS.deviceValue.PeripheralBusManager;
import Canada.JCanOS.networkStack.NetworkTools;
import Canada.JCanOS.networkStack.NetworkLayer;
import Canada.JCanOS.deviceValue.Clock;
import Canada.JCanOS.descriptorEntry.TaskStateSegment;
import Canada.JCanOS.Screen.characterDisplay;
import Canada.JCanOS.FileSystem.primaryPartitionTable;

public final class testAll {
    private static int passCount;

    private testAll() {
    }

    public static void main(String[] parameterArgument) {
        HostHardware deviceValue = new HostHardware();
        Kernel kernelValue = new Kernel(deviceValue);
        kernelValue.run();

        testMemory(kernelValue);
        testPageManagement(kernelValue);
        testFilesAndProcesses(kernelValue);
        testElf(kernelValue);
        testInput(kernelValue);
        testHardware(deviceValue);
        testInterruptsAndDescriptors();
        testStorageAndNetworking();
        testScreenAndClock();

        System.out.println("JCanOS tests passValue: " + passCount);
    }

    private static void testMemory(Kernel kernelValue) {
        MemoryManager managerValue = kernelValue.memoryRegion();
        int firstAddress = managerValue.allocateAligned(100, 64);
        verify((firstAddress & 63) == 0, "alignValue allocateStorage");
        managerValue.writeByteValue(firstAddress, (byte) 0x5a);
        verify(managerValue.readByteValue(firstAddress) == (byte) 0x5a, "물리 memoryRegion 읽고 write");
        int beforeUse = managerValue.usedSize();
        managerValue.releaseStorage(firstAddress);
        verify(managerValue.usedSize() < beforeUse, "memoryRegion releaseStorage");
    }

    private static void testPageManagement(Kernel kernelValue) {
        PageManager managerValue = kernelValue.pageManagement();
        PageManager.AddressSpace parentSpace = managerValue.newAddressSpace();
        managerValue.mapPage(parentSpace, 0x1000, true);
        managerValue.writeByteValue(parentSpace, 0x1010, (byte) 7);
        PageManager.AddressSpace childSpace = managerValue.cloneCopyOnWrite(parentSpace);
        managerValue.writeByteValue(childSpace, 0x1010, (byte) 9);
        verify(managerValue.readByteValue(parentSpace, 0x1010) == 7, "write 시 copyValue parentValue 격리");
        verify(managerValue.readByteValue(childSpace, 0x1010) == 9, "write 시 copyValue childValue write");
    }

    private static void testFilesAndProcesses(Kernel kernelValue) {
        byte[] contentValue = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernelValue.FileSystem().appendFile("tests", contentValue);
        processValue parentValue = kernelValue.firstProcess();
        invokeSystemCall invoke = kernelValue.invokeSystemCall();
        int descriptorEntry = invoke.open(parentValue, "/tests", invokeSystemCall.readOnlyFlag);
        verify(descriptorEntry >= 3, "file open");

        byte[] receiveDestination = new byte[contentValue.length];
        verify(invoke.read(parentValue, descriptorEntry, receiveDestination, receiveDestination.length) == contentValue.length, "file read");
        verify(Arrays.equals(contentValue, receiveDestination), "file contentValue");
        verify(invoke.movePosition(parentValue, descriptorEntry, 0, invokeSystemCall.searchStart) == 0, "file position moveValue");

        int clonedDescriptor = invoke.duplicateDescriptor(parentValue, descriptorEntry);
        verify(clonedDescriptor >= 0, "descriptorEntry cloneValue");
        processValue childValue = invoke.cloneProcess(parentValue);
        verify(childValue.identifierValue() != parentValue.identifierValue(), "processValue identifierValue 분리");
        verify(childValue.parentIdentifier() == parentValue.identifierValue(), "parentValue processValue identifierValue");
        verify(invoke.close(childValue, descriptorEntry) == 0 && parentValue.fileDescriptor().isOpen(descriptorEntry), "childValue close 격리");

        int previousEnd = invoke.increaseProgramBreak(parentValue, 8192);
        verify(previousEnd == 0x06000000, "Program ending 늘리기");
        verify(parentValue.programBreak() == 0x06002000, "Program ending 반영");
        verify(childValue.programBreak() == 0x06000000, "과정별 Program ending 격리");

        childValue.exitProgram(7);
        verify(invoke.waitForChild(parentValue, childValue.identifierValue(), false) == (7 << 8), "childValue exitProgram await");
        verify(invoke.isAccessible("tests", 1) == -13, "executeCommand permissionValue rejectValue");
        verify(invoke.userIdentifier() == 0 && invoke.groupIdentifier() == 0, "사용자와 무리 identifierValue");
        verify("/".equals(invoke.currentTaskList(2)) && invoke.switchTaskList("/") == 0, "currentItem performTask entryList");
        verify(invoke.isTerminal(parentValue, 1), "표준 Output TerminalIO");
        verify("JCanOS".equals(invoke.systemDetails().systemName()), "operatingSystemValue systemInformation");
    }

    private static void testElf(Kernel kernelValue) {
        byte[] data = new byte[92];
        data[0] = 0x7f;
        data[1] = 'E';
        data[2] = 'L';
        data[3] = 'F';
        data[4] = 1;
        data[5] = 1;
        writeIntegerValue(data, 24, 0x04001000);
        writeIntegerValue(data, 32, 52);
        writeShortInteger(data, 46, 40);
        writeShortInteger(data, 48, 1);
        writeIntegerValue(data, 56, 8);
        writeIntegerValue(data, 60, 2);
        writeIntegerValue(data, 64, 0x04002000);
        writeIntegerValue(data, 72, 64);

        ExecutableLoader.image imageValue = new ExecutableLoader().Checks(data);
        verify(imageValue.startAddress() == 0x04001000, "ELF run address");
        verify(imageValue.sectionsList().size() == 1 && imageValue.sectionsList().get(0).kindValue() == 8, "ELF 빈 data sectionValue");
        int descriptorEntry = kernelValue.invokeSystemCall().open(kernelValue.firstProcess(), "tests", invokeSystemCall.readOnlyFlag);
        verify(kernelValue.invokeSystemCall().file_control(kernelValue.firstProcess(), descriptorEntry, 2, 1) == 0, "executeCommand 시 close settings");
        verify(kernelValue.invokeSystemCall().executeCommand(kernelValue.firstProcess(), data, new String[] {"tests", "value"}, new String[] {"language=English"}) == 0, "ELF executeCommand imageValue 적재");
        verify(kernelValue.firstProcess().executionStartAddress() == 0x04001000, "executeCommand run address 반영");
        verify(kernelValue.firstProcess().executionArgument().length == 2 && kernelValue.firstProcess().environmentValue().length == 1, "executeCommand 인자와 environment");
        verify(!kernelValue.firstProcess().fileDescriptor().isOpen(descriptorEntry), "executeCommand 시 descriptorEntry close");
        verify(kernelValue.pageManagement().readByteValue(kernelValue.firstProcess().AddressSpace(), 0x04002000) == 0, "빈 data sectionValue zeroOperand initialize");
    }

    private static void testInput(Kernel kernelValue) {
        kernelValue.InputManagement().keyDown('가');
        kernelValue.InputManagement().mouseMovement(3, -2);
        inputEvent firstEvent = kernelValue.InputManagement().nextEvent();
        inputEvent secondEvent = kernelValue.InputManagement().nextEvent();
        verify(firstEvent.eventKind() == inputEvent.kindValue.keyDown, "자판 event");
        verify(secondEvent.firstValue() == 3 && secondEvent.secondValue() == -2, "쥐 moveValue event");
    }

    private static void testHardware(HostHardware deviceValue) {
        deviceValue.writePortByte(0x3f8, 0xab);
        verify(deviceValue.readPortByte(0x3f8) == 0xab, "hardwarePort inputOutput boundaryValue");
        verify(deviceValue.serialLog().contains("JCanOS"), "serialValue logRecord");
    }

    private static void testInterruptsAndDescriptors() {
        InterruptManager managerValue = new InterruptManager();
        managerValue.registerEntry(0x21, storageAddress -> storageAddress + 4);
        managerValue.enable();
        verify(managerValue.distributeValue(0x21, 100) == 104, "interrupt distributeValue");
        managerValue.deactivate();
        verify(managerValue.distributeValue(0x21, 100) == 100, "interrupt deactivate");

        GlobalDescriptorTable descriptorTable = new GlobalDescriptorTable();
        descriptorTable.setDefaultValue();
        verify(descriptorTable.fragmentsList().size() == 5, "전역 descriptorTable");
        TaskStateSegment taskState = new TaskStateSegment();
        taskState.setPrivilegedStack(0x10, 0x800000);
        verify(taskState.stackZeroBlock() == 0x10 && taskState.stackZeroAddress() == 0x800000, "performTask stateValue sectionValue");
    }

    private static void testStorageAndNetworking() {
        AdvancedTechnologyAttachment storageDevice = new AdvancedTechnologyAttachment(4, false);
        byte[] dataToWrite = new byte[AdvancedTechnologyAttachment.sectionSize];
        byte[] readDataValue = new byte[AdvancedTechnologyAttachment.sectionSize];
        dataToWrite[17] = 42;
        storageDevice.write(2, dataToWrite);
        storageDevice.read(2, readDataValue);
        verify(readDataValue[17] == 42, "ATA sectionValue 읽고 write");

        PeripheralBusManager peripheral = new PeripheralBusManager();
        peripheral.discoveredValue(new PeripheralBusManager.deviceValue(0x1022, 0x2000, 0xc000, 11));
        verify(peripheral.findEntry(0x1022, 0x2000) != null, "주변 deviceValue findEntry");

        byte[] ethernetFrame = new byte[34];
        ethernetFrame[12] = 0x08;
        ethernetFrame[13] = 0x00;
        ethernetFrame[14] = 0x45;
        verify(NetworkTools.ethernetUpperProtocol(ethernetFrame) == 0x0800, "이더넷 상위 contractValue");
        verify(NetworkTools.isIpv4Protocol(ethernetFrame, 14), "상호통신망규약 4판");
        verify(NetworkTools.internetChecksum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 checksum");

        byte[] firstSection = new byte[512];
        firstSection[510] = 0x55;
        firstSection[511] = (byte) 0xaa;
        firstSection[450] = 0x0b;
        writeIntegerValue(firstSection, 454, 63);
        writeIntegerValue(firstSection, 458, 1024);
        verify(new primaryPartitionTable().read(firstSection).size() == 1, "defaultValue 분할 영역표");

        NetworkLayer layerValue = new NetworkLayer();
        int[] receivedCount = new int[1];
        layerValue.registerUserDataUnit(7, (data, run, lengthValue) -> receivedCount[0]++);
        byte[] frameIndex = new byte[14 + 20 + 8];
        frameIndex[12] = 0x08;
        frameIndex[13] = 0x00;
        frameIndex[14] = 0x45;
        frameIndex[16] = 0;
        frameIndex[17] = 28;
        frameIndex[23] = 17;
        frameIndex[36] = 0;
        frameIndex[37] = 7;
        verify(layerValue.receiveEthernet(frameIndex) && receivedCount[0] == 1, "User data unitValue distributeValue");
    }

    private static void testScreenAndClock() {
        characterDisplay Screen = new characterDisplay();
        Screen.Output("가나\n다");
        verify(Screen.Characters(0, 0) == '가' && Screen.Characters(0, 1) == '다', "Characters Screen Output");
        Clock Clock = new Clock(100);
        for (int index = 0; index < 10; index++) {
            Clock.tickValue();
        }
        verify(Clock.elapsedMilliseconds() == 100, "Clock tickValue convertValue");
    }

    private static void writeIntegerValue(byte[] data, int position, int value) {
        data[position] = (byte) value;
        data[position + 1] = (byte) (value >>> 8);
        data[position + 2] = (byte) (value >>> 16);
        data[position + 3] = (byte) (value >>> 24);
    }

    private static void writeShortInteger(byte[] data, int position, int value) {
        data[position] = (byte) value;
        data[position + 1] = (byte) (value >>> 8);
    }

    private static void verify(boolean condition, String name) {
        if (!condition) {
            throw new AssertionError("failureValue: " + name);
        }
        passCount++;
        System.out.println("passValue: " + name);
    }
}
