// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Shell built-in tools sharing the RAM VFS and standard input/output. */
public final class ShellTools {
    static int[] data = new int[16384];
    static int inputFile = -1;
    static int openFile(int argumentIndex, int processMode) {
        int processedValue = CommandInterpreter.path(argumentIndex); return processedValue < 0 ? processedValue : MemoryFiles.open(processMode);
    }
    static boolean prepareInput(int argumentIndex) {
        inputFile = -1;
        if (argumentIndex < CommandInterpreter.tokenCount) {
            inputFile = openFile(argumentIndex, 0);
            if (inputFile < 0) { CommandInterpreter.error(inputFile); return false; }
        }
        return true;
    }
    static int read() {
        if (inputFile >= 3) return MemoryFiles.read(inputFile);
        while (true) {
            int byteData = Board.readSerial(); if (byteData == -2 || byteData == 4) return 256;
            if (byteData == 3) { CommandInterpreter.result = 130; return 256; }
            if (byteData >= 0) return byteData; Board.yieldProcessor();
        }
    }
    static void close() { if (inputFile >= 3) MemoryFiles.close(inputFile); inputFile = -1; }
    static void viewValue() {
        int lastPosition = CommandInterpreter.tokenCount == 1 ? 2 : CommandInterpreter.tokenCount;
        for (int argumentIndex = 1; argumentIndex < lastPosition; argumentIndex++) {
            if (!prepareInput(argumentIndex)) continue;
            int byteData; while ((byteData = read()) != 256 && byteData >= 0) Board.writeSerial(byteData);
            if (byteData < 0) CommandInterpreter.error(byteData); close();
        }
    }
    static void fileJob(String actionNumber) {
        if (CommandInterpreter.tokenCount != 2) { CommandInterpreter.result = 2; TerminalIO.write("사용법: mkdir/rmdir/touch file\n"); return; }
        int processedValue = CommandInterpreter.path(1);
        if (processedValue >= 0) {
            if (actionNumber.charAt(0) == 'm') processedValue = MemoryFiles.createDirectory();
            else if (actionNumber.charAt(0) == 'r') processedValue = MemoryFiles.removeDirectory();
            else { processedValue = MemoryFiles.open(65); if (processedValue >= 3) processedValue = MemoryFiles.close(processedValue); }
        }
        if (processedValue < 0) CommandInterpreter.error(processedValue);
    }
    static void copyValue(boolean hasMoved) {
        if (CommandInterpreter.tokenCount != 3) { CommandInterpreter.result = 2; TerminalIO.write("사용법: cp/mv original destinationEndpoint (file)\n"); return; }
        int processedValue = CommandInterpreter.path(1); if (processedValue >= 0) processedValue = MemoryFiles.normalizeValue();
        if (processedValue < 0) { CommandInterpreter.error(processedValue); return; }
        int originalNumber = MemoryFiles.findEntry(); if (originalNumber < 0) { CommandInterpreter.error(-2); return; }
        int entryCount = MemoryFiles.lengthValue[originalNumber]; for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) data[loopIndex] = MemoryFiles.readData(originalNumber, loopIndex);
        processedValue = CommandInterpreter.path(2); if (processedValue >= 0) processedValue = MemoryFiles.normalizeValue();
        if (processedValue < 0) { CommandInterpreter.error(processedValue); return; }
        if (MemoryFiles.findEntry() == originalNumber) { if (!hasMoved) CommandInterpreter.error(-22); return; }
        if (hasMoved) { processedValue = MemoryFiles.renameEntry(originalNumber); if (processedValue < 0) CommandInterpreter.error(processedValue); return; }
        int openedFileNumber = MemoryFiles.open(577); if (openedFileNumber < 0) { CommandInterpreter.error(openedFileNumber); return; }
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) { processedValue = MemoryFiles.write(openedFileNumber, data[loopIndex]); if (processedValue < 0) { CommandInterpreter.error(processedValue); break; } }
        MemoryFiles.close(openedFileNumber);
    }
    static int digitValue(int argumentIndex) {
        if (argumentIndex >= CommandInterpreter.tokenCount) return -1;
        int entryCount = 0; for (int loopIndex = 0; loopIndex < CommandInterpreter.lengthValue[argumentIndex]; loopIndex++) { int characterCode = CommandInterpreter.tokenValue[CommandInterpreter.startingPoint[argumentIndex] + loopIndex]; if (characterCode < '0' || characterCode > '9' || entryCount > 10000) return -1; entryCount = entryCount * 10 + characterCode - '0'; } return entryCount;
    }
    static void countingValue() {
        int argumentIndex = 1, option = 0;
        if (CommandInterpreter.equalText(1, "-c") || CommandInterpreter.equalText(1, "-l") || CommandInterpreter.equalText(1, "-w")) { option = CommandInterpreter.equalText(1, "-c") ? 1 : CommandInterpreter.equalText(1, "-l") ? 2 : 3; argumentIndex++; }
        if (CommandInterpreter.tokenCount > argumentIndex + 1) { CommandInterpreter.result = 2; TerminalIO.write("사용법: wc [-c|-l|-w] [file]\n"); return; }
        if (!prepareInput(argumentIndex)) return;
        int byteCount = 0, lines = 0, lexicalWordCount = 0, byteData; boolean lexicalWord = false;
        while ((byteData = read()) >= 0 && byteData != 256) { byteCount++; if (byteData == 10) lines++; boolean space = byteData == 32 || byteData >= 9 && byteData <= 13; if (!space && !lexicalWord) lexicalWordCount++; lexicalWord = !space; }
        close(); if (byteData < 0) { CommandInterpreter.error(byteData); return; }
        if (option != 0) TerminalIO.number(option == 1 ? byteCount : option == 2 ? lines : lexicalWordCount);
        else { TerminalIO.number(lines); TerminalIO.Characters(' '); TerminalIO.number(lexicalWordCount); TerminalIO.Characters(' '); TerminalIO.number(byteCount); } TerminalIO.Characters(10);
    }
    static void findEntry() {
        if (CommandInterpreter.tokenCount < 2 || CommandInterpreter.tokenCount > 3) { CommandInterpreter.result = 2; TerminalIO.write("사용법: grep 찾을문구 [file]\n"); return; }
        if (!prepareInput(2)) return;
        int entryCount = 0, byteData, matches = 0;
        while (true) {
            byteData = read();
            if (byteData == 10 || byteData == 256 || byteData < 0) {
                boolean wasFound = false;
                for (int loopIndex = 0; loopIndex <= entryCount - CommandInterpreter.lengthValue[1]; loopIndex++) {
                    boolean isSame = true; for (int innerPosition = 0; innerPosition < CommandInterpreter.lengthValue[1]; innerPosition++) if (data[loopIndex + innerPosition] != CommandInterpreter.tokenValue[CommandInterpreter.startingPoint[1] + innerPosition]) isSame = false;
                    if (isSame) wasFound = true;
                }
                if (wasFound && (entryCount > 0 || byteData == 10)) { for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) Board.writeSerial(data[loopIndex]); TerminalIO.Characters(10); matches++; }
                entryCount = 0; if (byteData != 10) break;
            } else if (entryCount < data.length) data[entryCount++] = byteData;
            else { CommandInterpreter.error(-28); close(); return; }
        }
        close(); if (byteData < 0) CommandInterpreter.error(byteData); else if (CommandInterpreter.result == 0) CommandInterpreter.result = matches == 0 ? 1 : 0;
    }
    static void headValue(boolean rearPosition) {
        int argumentIndex = 1, lines = 10;
        if (CommandInterpreter.equalText(1, "-n")) { lines = digitValue(2); argumentIndex = 3; }
        if (lines < 0 || CommandInterpreter.tokenCount > argumentIndex + 1) { CommandInterpreter.result = 2; TerminalIO.write("사용법: head/tail [-n lines] [file]\n"); return; }
        if (!prepareInput(argumentIndex)) return;
        int entryCount = 0, byteData;
        while ((byteData = read()) != 256 && byteData >= 0) { if (entryCount == data.length) { CommandInterpreter.error(-28); close(); return; } data[entryCount++] = byteData; }
        close(); if (byteData < 0) { CommandInterpreter.error(byteData); return; }
        int localStart = 0, endPosition = entryCount;
        if (lines == 0) return;
        if (rearPosition) { int totalCount = 0; for (int loopIndex = entryCount - 2; loopIndex >= 0; loopIndex--) if (data[loopIndex] == 10 && ++totalCount == lines) { localStart = loopIndex + 1; break; } }
        else { int totalCount = 0; for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) if (data[loopIndex] == 10 && ++totalCount == lines) { endPosition = loopIndex + 1; break; } }
        for (int loopIndex = localStart; loopIndex < endPosition; loopIndex++) Board.writeSerial(data[loopIndex]);
    }
    static void writeTogether() {
        boolean append = CommandInterpreter.equalText(1, "-a"); int argumentIndex = append ? 2 : 1;
        if (CommandInterpreter.tokenCount != argumentIndex + 1) { CommandInterpreter.result = 2; TerminalIO.write("사용법: tee [-a] file\n"); return; }
        int openedFileNumber = openFile(argumentIndex, append ? 1089 : 577); if (openedFileNumber < 0) { CommandInterpreter.error(openedFileNumber); return; }
        inputFile = -1; int byteData;
        while ((byteData = read()) != 256 && byteData >= 0) { int processedValue = MemoryFiles.write(openedFileNumber, byteData); if (processedValue < 0) { CommandInterpreter.error(processedValue); break; } Board.writeSerial(byteData); }
        MemoryFiles.close(openedFileNumber);
    }
}
