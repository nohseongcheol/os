// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Small serial/PS2 command interpreter that performs no disk writes. */
public final class CommandInterpreter {
    static int[] inputValue = new int[128];
    static int lengthValue = 0;
    static boolean returnToPreviousLine = false;
    static boolean lineOverflow = false;

    static boolean command(String name) {
        if (lengthValue < name.length()) return false;
        for (int index = 0; index < name.length(); index++)
            if (inputValue[index] != name.charAt(index)) return false;
        return lengthValue == name.length() || inputValue[name.length()] == ' ';
    }

    static void showHelp() {
        TextTerminal.write("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        TextTerminal.write("apps | run NAME [ARGS] | net\n");
        TextTerminal.write("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        TextTerminal.write("sync (연결된 JKSTORE1 storeValue 장치에 file 보존)\n");
    }

    static void processValueEntry() {
        if (lengthValue == 0) return;
        if (command("help")) showHelp();
        else if (command("sync")) {
            int result = preserveFile.synchronize();
            TextTerminal.write("Sync: "); TextTerminal.writeNumber(result); TextTerminal.Characters(10);
        }
        else if (command("ls")) MemoryFileSystem.entryList();
        else if (command("edit")) MemoryFileSystem.command(inputValue, 4, lengthValue, 0);
        else if (command("cat")) MemoryFileSystem.command(inputValue, 3, lengthValue, 1);
        else if (command("rm")) MemoryFileSystem.command(inputValue, 2, lengthValue, 2);
        else if (command("java") || command("javac")) {
            int result = ExecutionManager.executeCommand(inputValue, 0, lengthValue);
            TextTerminal.write("Exit: "); TextTerminal.writeNumber(result); TextTerminal.Characters(10);
        }
        else if (command("apps")) ExecutionManager.entryList();
        else if (command("net")) networkStack.stateValue();
        else if (command("run")) {
            int result = ExecutionManager.executeCommand(inputValue, 3, lengthValue);
            TextTerminal.write("Exit: "); TextTerminal.writeNumber(result); TextTerminal.write("\n");
        } else if (command("info")) {
            TextTerminal.write("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (command("mem")) {
            TextTerminal.write("upperSide memoryValue addressRegion(KiB): "); TextTerminal.writeNumber(memoryRegion.upperMemorySize());
            TextTerminal.write("\n배열 동적 memoryValue addressRegion(byteValue): "); TextTerminal.writeNumber(deviceValue.arrayUsage());
            TextTerminal.write(" / 262144\n작업 addressRegion sectionValue: "); TextTerminal.writeNumber(memoryRegion.usedEntryCount());
            TextTerminal.write(" / 8 (각 4096바이트)\n");
        } else if (command("alloc")) {
            int index = memoryRegion.allocateStorage();
            TextTerminal.write("sectionValue index: "); TextTerminal.writeNumber(index); TextTerminal.write("\n");
        } else if (command("free")) {
            if (lengthValue == 6 && inputValue[4] == ' ' && inputValue[5] >= '0' && inputValue[5] <= '7') {
                TextTerminal.write(memoryRegion.returnResult(inputValue[5] - '0') ? "반환됨\n" : "할당되지 않은 sectionValue\n");
            } else TextTerminal.write("사용법: free 0..7\n");
        } else if (command("echo")) {
            for (int index = 5; index < lengthValue; index++) TextTerminal.Characters(inputValue[index]);
            TextTerminal.Characters(10);
        } else if (command("clear")) TextTerminal.eraseEntry();
        else if (command("test")) Kernel.tests();
        else if (command("halt")) {
            TextTerminal.write("HALTED\n");
            deviceValue.haltExecution();
        } else TextTerminal.write("알 number 없는 명령입니다. help를 입력하세요.\n");
    }

    static void acceptAndWrite(int value) {
        if (value == 10 && returnToPreviousLine) { returnToPreviousLine = false; return; }
        returnToPreviousLine = value == 13;
        if (value == 10 || value == 13) {
            TextTerminal.Characters(10);
            if (MemoryFileSystem.isEditing) MemoryFileSystem.editedLine(inputValue, lengthValue, lineOverflow);
            else processValueEntry();
            lengthValue = 0;
            lineOverflow = false;
            TextTerminal.write(MemoryFileSystem.isEditing ? "...> " : "jkoros> ");
        } else if (value == 8 || value == 127) {
            if (lengthValue > 0) {
                lengthValue--;
                TextTerminal.serialByte(8); TextTerminal.serialByte(32); TextTerminal.serialByte(8);
                TextTerminal.screenCharacter(8);
            }
        } else if (value >= 32 && value < 127 && lengthValue < inputValue.length) {
            inputValue[lengthValue++] = value;
            TextTerminal.Characters(value);
        } else if (value >= 32 && value < 127) lineOverflow = true;
    }

    static void run() {
        showHelp();
        TextTerminal.write("READY\njkoros> ");
        while (true) {
            int value = TextTerminal.readSerial();
            if (value < 0) value = Keyboard.read();
            if (value >= 0) acceptAndWrite(value);
            else { networkStack.verify(); deviceValue.yieldBriefly(); }
        }
    }
}
