// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Shell state for four terminals. File storage is shared; paths, variables, history and input are separate. */
public final class windowSession {
    static int[] preserveValue = new int[4 * 30000], prepare = new int[4];
    static int currentItem, position;
    static boolean readContinuation;
    static void arrayValue(int[] data, boolean storeValue) {
        for (int loopIndex = 0; loopIndex < data.length; loopIndex++) { if (storeValue) preserveValue[position++] = data[loopIndex]; else data[loopIndex] = preserveValue[position++]; }
    }
    static int value(int dataValue, boolean wasStored) { if (wasStored) { preserveValue[position++] = dataValue; return dataValue; } return preserveValue[position++]; }
    static void seekPosition(int preservedSlot, boolean wasStored) {
        position = preservedSlot * 30000;
        arrayValue(MemoryFiles.currentItem, wasStored); MemoryFiles.currentLength = value(MemoryFiles.currentLength, wasStored);
        arrayValue(ShellSyntax.variableName, wasStored); arrayValue(ShellSyntax.variableData, wasStored); arrayValue(ShellSyntax.namelen, wasStored); arrayValue(ShellSyntax.valueLength, wasStored);
        ShellSyntax.stateValue = value(ShellSyntax.stateValue, wasStored);
        arrayValue(LineEditor.logRecord, wasStored); arrayValue(LineEditor.logLength, wasStored); arrayValue(LineEditor.storeValue, wasStored); arrayValue(CommandInterpreter.line, wasStored);
        LineEditor.logCount = value(LineEditor.logCount, wasStored); LineEditor.logRecordEnd = value(LineEditor.logRecordEnd, wasStored);
        LineEditor.searchValue = value(LineEditor.searchValue, wasStored); LineEditor.storedLength = value(LineEditor.storedLength, wasStored);
        LineEditor.size = value(LineEditor.size, wasStored); LineEditor.cursorValue = value(LineEditor.cursorValue, wasStored); LineEditor.startWindow = value(LineEditor.startWindow, wasStored);
        prepare[preservedSlot] = 1;
    }
    static void processValueEntry() {
        int eventNumber = Board.terminal(12); if (eventNumber == 0) return;
        seekPosition(currentItem, true);
        for (int loopIndex = 0; loopIndex < 4; loopIndex++) {
            if ((eventNumber & (1 << (8 + loopIndex))) != 0) { Board.controlUserProgram(32 + loopIndex); prepare[loopIndex] = 0; }
            if ((eventNumber & (1 << (4 + loopIndex))) != 0 && loopIndex != currentItem) prepare[loopIndex] = 0;
        }
        int nextPosition = (eventNumber & 15) - 1; if (nextPosition < 0) nextPosition = 0;
        if (prepare[nextPosition] == 0) for (int loopIndex = 0; loopIndex < 30000; loopIndex++) preserveValue[nextPosition * 30000 + loopIndex] = 0;
        currentItem = nextPosition; seekPosition(currentItem, false); Board.terminal(100 + currentItem); readContinuation = true;
        TerminalIO.write("\nTERMINAL FOCUS "); TerminalIO.number(currentItem + 1); TerminalIO.Characters(10);
    }
    static boolean resumeExecution() {
        if (Board.controlUserProgram(16 + currentItem) == 0) return false;
        ShellIO.allowInteractive = true; ShellIO.run(false, false); Board.switchIo(1);
        int processedValue = Board.controlUserProgram(currentItem); ShellIO.ending();
        if (processedValue != -1005) { readContinuation = false; ShellSyntax.stateValue = processedValue < 0 ? 126 : processedValue; TerminalIO.write("exit "); TerminalIO.number(processedValue); TerminalIO.Characters(10); Board.terminal(3); }
        return true;
    }
}
