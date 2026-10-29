// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Initial Pi4 port of the standalone Java kernel, running directly rather than on Linux or a host JVM. */
public final class Kernel {
    static int[] taskIterations = new int[3];
    static int[] taskSum = new int[3];
    static int taskOrder;
    static int taskError;
    static int randomSeed = 17;

    static void verify(boolean condition, int index) {
        if (!condition) { TerminalIO.write("FAIL "); TerminalIO.number(index); Board.stop(index); }
    }
    static int branch(int value) {
        switch (value) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int denseSwitch(int value) {
        switch (value) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] returnArray(int[] arrayValue) { return arrayValue; }
    static void testArithmetic() {
        int value = randomSeed;
        verify(value * 7 - value == 102 && value / 3 == 5 && value % 3 == 2, 1);
        int minimumInteger = 0x80000000, negativeOne = -1;
        verify(minimumInteger / negativeOne == minimumInteger && minimumInteger % negativeOne == 0, 2);
        verify(minimumInteger + minimumInteger == 0 && -minimumInteger == minimumInteger, 3);
        verify((-value >> 2) == -5 && (-value >>> 2) == 1073741819 && (value << 33) == 34, 4);
        verify((byte)(value * 16) == 16 && (short)65535 == -1 && (char)negativeOne == 65535, 5);
        int[] arrayValue = new int[5];
        for (int loopIndex = 0; loopIndex < arrayValue.length; loopIndex++) arrayValue[loopIndex] = loopIndex * value;
        arrayValue[2]++;
        verify(returnArray(arrayValue) == arrayValue && arrayValue[2] == 35 && arrayValue[4] == 68, 6);
        verify(branch(value - 117) == 7 && branch(value - 15) == 9 && branch(value) == 3 && denseSwitch(value - 15) == 17, 7);
        String text = "한글 😀";
        verify(text.length() == 5 && text.charAt(0) == '한' && text.charAt(3) == 0xd83d, 8);
        verify(Board.cpuPrivilegeLevel() == 1, 9);
        TerminalIO.write("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void performTask(int index) {
        // Check that local variables survive a yield: each task has an independent machine stack.
        int localValue = index * 100;
        for (int loopIndex = 0; loopIndex < 10; loopIndex++) {
            if (taskOrder % 2 + 1 != index) taskError++;
            taskOrder++;
            localValue += loopIndex + index;
            taskSum[index] = localValue;
            taskIterations[index]++;
            Board.yieldProcessor();
            if (localValue != taskSum[index]) taskError++;
        }
    }
    static void testTasks() {
        taskOrder = 0; taskError = 0;
        taskIterations[1] = 0; taskIterations[2] = 0;
        verify(Board.createTask(1) == 0 && Board.createTask(2) == 0, 20);
        int rotationCount = 0;
        while (Board.taskState(1) != 0 || Board.taskState(2) != 0) {
            Board.yieldProcessor();
            verify(++rotationCount < 100, 21);
        }
        verify(taskIterations[1] == 10 && taskIterations[2] == 10 && taskOrder == 20 && taskError == 0, 22);
        verify(taskSum[1] == 155 && taskSum[2] == 265, 23);
        TerminalIO.write("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rectangle(int horizontalPosition, int verticalPosition, int widthValue, int heightValue, int colourValue) {
        for (int yCoordinate = verticalPosition; yCoordinate < verticalPosition + heightValue; yCoordinate++)
            for (int xCoordinate = horizontalPosition; xCoordinate < horizontalPosition + widthValue; xCoordinate++) Board.putScreenPixel(xCoordinate, yCoordinate, colourValue);
    }
    static void Screen() {
        if (Board.prepareScreen() == 0) { TerminalIO.write("FRAMEBUFFER unavailable\n"); return; }
        rectangle(0, 0, Board.screenWidth(), Board.screenHeight(), 0x302018);
        rectangle(40, 40, 560, 400, 0xefe8e2);
        rectangle(40, 40, 560, 40, 0x905020);
        rectangle(60, 110, 240, 140, 0x90b050);
        rectangle(320, 110, 260, 140, 0xd0a040);
        rectangle(60, 290, 520, 120, 0xd8d0c8);
        TerminalIO.write("FRAMEBUFFER PASS "); TerminalIO.number(Board.screenWidth()); TerminalIO.Characters('x');
        TerminalIO.number(Board.screenHeight()); TerminalIO.write(" RGB32 (drawing only)\n");
    }
    static void testC() {
        int result = Board.testCpp();
        verify(result == 0, 100 + result);
        TerminalIO.write("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void testUserPrograms() {
        verify(Board.checkUserProgram() == 0, 200);
        TerminalIO.write("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int initialResult = Board.runUserProgram(0);
        if (initialResult != 0) { TerminalIO.write("USER DEMO RESULT "); TerminalIO.number(initialResult); TerminalIO.Characters(10); }
        verify(initialResult == 0, 201);
        TerminalIO.write("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] expectedValues = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int index = 0; index < expectedValues.length; index++) {
            TerminalIO.write("USER CHECK "); TerminalIO.number(index); TerminalIO.Characters(10);
            int result = Board.runUserProgram(index + 1);
            if (result != expectedValues[index]) { TerminalIO.write("USER RESULT "); TerminalIO.number(result); TerminalIO.Characters(10); }
            verify(result == expectedValues[index], 210 + index);
        }
        verify(Board.runUserProgram(0) == 0, 220);
        TerminalIO.write("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void testNetworking() {
        int result = Board.runUserProgram(9);
        if (result != 0) { TerminalIO.write("UDP RESULT "); TerminalIO.number(result); TerminalIO.Characters(10); }
        verify(result == 0, 230);
    }
    static void systemInformation() {
        TerminalIO.write("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        TerminalIO.write("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        TerminalIO.write("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        TerminalIO.write("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        TerminalIO.write("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void run() {
        TerminalIO.write("WorldOS en · Hello · 😀\n");
        testArithmetic();
        testC();
        testTasks();
        Screen();
        testUserPrograms();
        testNetworking();
        TerminalIO.write("NATIVE READY\n");
        CommandInterpreter.executeCommand();
    }
}
