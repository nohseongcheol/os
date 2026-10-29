// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Java entry point called after actual boot, independent of a JVM or host operating system. */
public final class Kernel {
    static int totalValue(int ending) {
        int sumValue = 0;
        for (int index = 1; index <= ending; index++) sumValue += index;
        return sumValue;
    }

    static boolean tests() {
        int[] values = new int[4];
        values[2] = totalValue(10);
        int negativeValue = -7;
        int minimumValue = 0x80000000;
        int divisionResult = -1;
        int index = memoryRegion.allocateStorage();
        boolean passValue = values[0] == 0 && values[2] == 55 && values.length == 4
            && negativeValue / 3 == -2 && negativeValue % 3 == -1 && minimumValue / divisionResult == minimumValue
            && minimumValue % divisionResult == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && index >= 0 && memoryRegion.returnResult(index) && !memoryRegion.returnResult(index);
        TextTerminal.write(passValue ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return passValue;
    }

    public static void run() {
        TextTerminal.prepare();
        TextTerminal.write("JKOROS NATIVE JAVA\n");
        TextTerminal.write("Java 기계어 kernelValue run\n");
        if (deviceValue.bootMarker() != 0x2badb002) {
            TextTerminal.write("BAD MULTIBOOT MAGIC\n");
            deviceValue.haltExecution();
        }
        if (!tests()) deviceValue.haltExecution();
        if (memoryRegion.upperMemorySize() < 15360) {
            TextTerminal.write("At least 16 MiB RAM required\n");
            deviceValue.haltExecution();
        }
        deviceValue.prepareUserProgram();
        TextTerminal.write("USER ELF: ring 3 / paging / int 0x80\n");
        NetworkDeviceDriver.prepare();
        networkStack.cleanProcess();
        MemoryFileSystem.prepare();
        preserveFile.prepare();
        CommandInterpreter.run();
    }
}
