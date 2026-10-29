// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Insertion, deletion, arrow keys, command history and Tab completion preserve UTF-8 byte boundaries. */
public final class LineEditor {
    static boolean commandLine;
    static int[] logRecord = new int[16 * 1024], logLength = new int[16], storeValue = new int[4096], candidate = new int[64];
    static int logCount, logRecordEnd, searchValue, storedLength, size, cursorValue, candidateCount, candidateLength, startWindow;
    static boolean showHorizontalPosition;
    static String commandsList = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd secureShell RemoteDisplay run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] commandCandidate = new int[128];
    static void addCommandCandidate(String entryList, int startPosition, int endPosition, int inputLength) {
        int byteCount=0;
        for(int positionIndex=startPosition;positionIndex<endPosition;positionIndex++) {
            int characterCode=entryList.charAt(positionIndex);
            if(characterCode>=0xd800 && characterCode<=0xdbff && positionIndex+1<endPosition)characterCode=0x10000+((characterCode-0xd800)<<10)+entryList.charAt(++positionIndex)-0xdc00;
            int number=characterCode<128?1:characterCode<2048?2:characterCode<65536?3:4;
            if(byteCount+number>62)return;
            for(int sequenceValue=number-1;sequenceValue>=0;sequenceValue--)commandCandidate[byteCount++]=number==1?characterCode:sequenceValue==number-1?(number==2?0xc0:number==3?0xe0:0xf0)|(characterCode>>(6*sequenceValue)):0x80|((characterCode>>(6*sequenceValue))&63);
        }
        if(byteCount<inputLength)return;
        for(int positionIndex=0;positionIndex<inputLength;positionIndex++)if(commandCandidate[positionIndex]!=CommandInterpreter.line[positionIndex])return;
        candidateCount++;candidateLength=byteCount+1;
        for(int positionIndex=0;positionIndex<byteCount;positionIndex++)candidate[positionIndex]=commandCandidate[positionIndex];candidate[byteCount]=' ';
    }
    static int frontValue(int readCursor) { if (readCursor > 0) { readCursor--; while (readCursor > 0 && (CommandInterpreter.line[readCursor] & 192) == 128) readCursor--; } return readCursor; }
    static int backValue(int readCursor) { if (readCursor < size) { readCursor++; while (readCursor < size && (CommandInterpreter.line[readCursor] & 192) == 128) readCursor++; } return readCursor; }
    static int widthSpan(int startPosition, int destinationValueIndex) {
        int cells = 0;
        for (int loopIndex = startPosition; loopIndex < destinationValueIndex; loopIndex++) { int byteData = CommandInterpreter.line[loopIndex]; if ((byteData & 192) == 128) continue; cells += byteData >= 196 ? 2 : 1; }
        return cells;
    }
    static void retryValue() {
        TerminalIO.write("\r\u001b[2K");
        TerminalIO.write(commandLine ? "jkoros-native> " : "edit> ");
        visibleLines();
    }
    // Move left and right within one physical line. Redisplaying a long command must not erase output above it.
    static int visibleWidth() { int columns = Board.terminal(13) & 65535; return columns - (commandLine ? 18 : 9); }
    static void visibleLines() {
        if (cursorValue < startWindow) startWindow = cursorValue;
        while (widthSpan(startWindow, cursorValue) > visibleWidth()) startWindow = backValue(startWindow);
        int endPosition = startWindow;
        while (endPosition < size && widthSpan(startWindow, backValue(endPosition)) <= visibleWidth()) endPosition = backValue(endPosition);
        TerminalIO.write("\r\u001b["); TerminalIO.number(commandLine ? 16 : 7); TerminalIO.write("G\u001b[K");
        if (startWindow > 0) TerminalIO.Characters('<');
        for (int loopIndex = startWindow; loopIndex < endPosition; loopIndex++) Board.writeSerial(CommandInterpreter.line[loopIndex]);
        TerminalIO.Characters(endPosition < size ? '>' : ' ');
        TerminalIO.write("\u001b["); TerminalIO.number(widthSpan(cursorValue, endPosition) + 1); TerminalIO.Characters('D');
        showHorizontalPosition = startWindow > 0 || endPosition < size || widthSpan(0, size) > visibleWidth();
    }
    static void appendLog() {
        if (!commandLine || size == 0 || size > 1024) return;
        if (logCount > 0) {
            int lastPosition = (logRecordEnd + 15) % 16; boolean isSame = logLength[lastPosition] == size;
            for (int loopIndex = 0; isSame && loopIndex < size; loopIndex++) if (logRecord[lastPosition * 1024 + loopIndex] != CommandInterpreter.line[loopIndex]) isSame = false;
            if (isSame) return;
        }
        logLength[logRecordEnd] = size; for (int loopIndex = 0; loopIndex < size; loopIndex++) logRecord[logRecordEnd * 1024 + loopIndex] = CommandInterpreter.line[loopIndex];
        logRecordEnd = (logRecordEnd + 1) % 16; if (logCount < 16) logCount++;
    }
    static void logMovement(int deltaValue) {
        if (!commandLine) return;
        if (searchValue == 0 && deltaValue > 0) { storedLength = size; for (int loopIndex = 0; loopIndex < size; loopIndex++) storeValue[loopIndex] = CommandInterpreter.line[loopIndex]; }
        int nextPosition = searchValue + deltaValue; if (nextPosition < 0 || nextPosition > logCount) return; searchValue = nextPosition;
        if (searchValue == 0) { size = storedLength; for (int loopIndex = 0; loopIndex < size; loopIndex++) CommandInterpreter.line[loopIndex] = storeValue[loopIndex]; }
        else { int preservedSlot = (logRecordEnd + 16 - searchValue) % 16; size = logLength[preservedSlot]; for (int loopIndex = 0; loopIndex < size; loopIndex++) CommandInterpreter.line[loopIndex] = logRecord[preservedSlot * 1024 + loopIndex]; }
        cursorValue = size; retryValue();
    }
    static void showLog() {
        for (int entryCount = 0; entryCount < logCount; entryCount++) {
            int preservedSlot = (logRecordEnd + 16 - logCount + entryCount) % 16; TerminalIO.number(entryCount + 1); TerminalIO.write("  ");
            for (int loopIndex = 0; loopIndex < logLength[preservedSlot]; loopIndex++) Board.writeSerial(logRecord[preservedSlot * 1024 + loopIndex]); TerminalIO.Characters(10);
        }
    }
    static void addCandidate(int[] dataArray, int startPosition, int entryCount, int prefix, int totalCount, boolean directoryNumber) {
        if (entryCount < totalCount || entryCount > 62) return;
        for (int loopIndex = 0; loopIndex < totalCount; loopIndex++) if (dataArray[startPosition + loopIndex] != CommandInterpreter.line[prefix + loopIndex]) return;
        candidateCount++; candidateLength = entryCount + 1;
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) candidate[loopIndex] = dataArray[startPosition + loopIndex]; candidate[entryCount] = directoryNumber ? '/' : ' ';
    }
    static void completedValue() {
        if (!commandLine || cursorValue != size) return;
        int startingPoint = size; while (startingPoint > 0 && CommandInterpreter.line[startingPoint - 1] != ' ') startingPoint--;
        for (int loopIndex = startingPoint; loopIndex < size; loopIndex++) if (CommandInterpreter.line[loopIndex] == '/' || CommandInterpreter.line[loopIndex] == '"' || CommandInterpreter.line[loopIndex] == 39 || CommandInterpreter.line[loopIndex] == '\\') return;
        candidateCount = 0; int entryCount = size - startingPoint;
        if (startingPoint == 0) {
            for(int listIndex=0;listIndex<2;listIndex++) {
                String entryList=listIndex==0?commandsList:SystemCommands.completedWord();
                int readCursor=0;
                while(readCursor<entryList.length()) {
                    int endPosition=readCursor;while(endPosition<entryList.length() && entryList.charAt(endPosition)!=' ')endPosition++;
                    addCommandCandidate(entryList,readCursor,endPosition,entryCount);readCursor=endPosition+1;
                }
            }
        } else {
            MemoryFiles.pathStart(1); MemoryFiles.pathByte(0, '.'); MemoryFiles.normalizeValue();
            for (int loopIndex = 0; loopIndex < MemoryFiles.fileCount; loopIndex++) {
                int startPosition = MemoryFiles.entryStart(MemoryFiles.name, loopIndex * 64, MemoryFiles.namelen[loopIndex]);
                if (startPosition >= 0) addCandidate(MemoryFiles.name, loopIndex * 64 + startPosition, MemoryFiles.namelen[loopIndex] - startPosition, startingPoint, entryCount, false);
            }
            for (int loopIndex = 0; loopIndex < 16; loopIndex++) {
                int startPosition = MemoryFiles.entryStart(MemoryFiles.directoryName, loopIndex * 64, MemoryFiles.directoryLength[loopIndex]);
                if (startPosition >= 0) addCandidate(MemoryFiles.directoryName, loopIndex * 64 + startPosition, MemoryFiles.directoryLength[loopIndex] - startPosition, startingPoint, entryCount, true);
            }
        }
        if (candidateCount != 1) { Board.writeSerial(7); return; }
        for (int loopIndex = entryCount; loopIndex < candidateLength && size < CommandInterpreter.line.length - 1; loopIndex++) {
            if (candidate[loopIndex] == ' ' && loopIndex != candidateLength - 1) CommandInterpreter.line[size++] = '\\';
            CommandInterpreter.line[size++] = candidate[loopIndex];
        }
        cursorValue = size; retryValue();
    }
    static int readEscape() {
        int startingPoint = Board.milliseconds();
        while (Board.milliseconds() - startingPoint < 80) { int byteData = Board.readSerial(); if (byteData >= 0) return byteData; Board.yieldProcessor(); }
        return -1;
    }
    static void escapeValue() {
        int first = readEscape(); if (first != '[' && first != 'O') return;
        int entryCount = 0, endPosition = -1;
        for (int loopIndex = 0; loopIndex < 12; loopIndex++) { int byteData = readEscape(); if (byteData < 0) return; if (byteData >= '0' && byteData <= '9') entryCount = entryCount * 10 + byteData - '0'; else { endPosition = byteData; break; } }
        if (endPosition == 'A') logMovement(1);
        else if (endPosition == 'B') logMovement(-1);
        else if (endPosition == 'C') { cursorValue = backValue(cursorValue); retryValue(); }
        else if (endPosition == 'D') { cursorValue = frontValue(cursorValue); retryValue(); }
        else if (endPosition == 'H' || endPosition == '~' && (entryCount == 1 || entryCount == 7)) { cursorValue = 0; retryValue(); }
        else if (endPosition == 'F' || endPosition == '~' && (entryCount == 4 || entryCount == 8)) { cursorValue = size; retryValue(); }
        else if (endPosition == '~' && entryCount == 3 && cursorValue < size) {
            int nextPosition = backValue(cursorValue); for (int loopIndex = nextPosition; loopIndex < size; loopIndex++) CommandInterpreter.line[loopIndex - nextPosition + cursorValue] = CommandInterpreter.line[loopIndex]; size -= nextPosition - cursorValue; retryValue();
        }
        else if (endPosition == '~' && (entryCount == 5 || entryCount == 6)) Board.terminal(entryCount == 5 ? 5 : 6);
        else if (endPosition == '~' && entryCount == 24 && commandLine) { CommandInterpreter.terminal(true); }
    }
    static int read() {
        if (!windowSession.readContinuation) { size = cursorValue = searchValue = startWindow = 0; showHorizontalPosition = false; }
        else { windowSession.readContinuation = false; retryValue(); } boolean overflow = false;
        while (true) {
            int byteData = Board.readSerial(); if (byteData == -4096) return -3;
            if (Board.terminal(14) != 0) retryValue(); if (byteData < 0) { Board.yieldProcessor(); continue; }
            if (byteData == 10 && CommandInterpreter.previousLine) { CommandInterpreter.previousLine = false; continue; } CommandInterpreter.previousLine = byteData == 13;
            if (byteData == 27) { escapeValue(); continue; }
            if (byteData == 3) { TerminalIO.write("^C\n"); return -1; }
            if (byteData == 4 && size == 0 && commandLine) { if (Board.terminal(2) != 0) CommandInterpreter.terminal(true); return -1; }
            if (byteData == 13 || byteData == 10) { TerminalIO.Characters(10); if (!overflow) appendLog(); return overflow ? -2 : size; }
            if (byteData == 9 && commandLine) { completedValue(); continue; }
            if (byteData == 1 || byteData == 5) { cursorValue = byteData == 1 ? 0 : size; retryValue(); continue; }
            if (byteData == 8 || byteData == 127 || byteData == 21) {
                if (byteData == 21) { for (int loopIndex = cursorValue; loopIndex < size; loopIndex++) CommandInterpreter.line[loopIndex - cursorValue] = CommandInterpreter.line[loopIndex]; size -= cursorValue; cursorValue = 0; }
                else if (cursorValue > 0) { int beforeChange = frontValue(cursorValue); for (int loopIndex = cursorValue; loopIndex < size; loopIndex++) CommandInterpreter.line[loopIndex - cursorValue + beforeChange] = CommandInterpreter.line[loopIndex]; size -= cursorValue - beforeChange; cursorValue = beforeChange; }
                retryValue(); continue;
            }
            if (byteData == 11) { size = cursorValue; retryValue(); continue; }
            if (byteData < 32 && byteData != 9) continue;
            if (size == CommandInterpreter.line.length) { overflow = true; continue; }
            for (int loopIndex = size; loopIndex > cursorValue; loopIndex--) CommandInterpreter.line[loopIndex] = CommandInterpreter.line[loopIndex - 1];
            CommandInterpreter.line[cursorValue++] = byteData; size++;
            if (cursorValue == size && !showHorizontalPosition && widthSpan(0, size) <= visibleWidth()) Board.writeSerial(byteData);
            else if (cursorValue == size) visibleLines(); else retryValue();
        }
    }
}
