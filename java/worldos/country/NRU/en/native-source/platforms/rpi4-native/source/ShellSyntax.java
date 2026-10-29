// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Restricted interactive shell grammar. Pipes run sequentially; the environment is shared within one shell. */
public final class ShellSyntax {
    static int[] source = new int[4 * 4096], kindValue = new int[4 * 128], run = new int[4 * 128], ending = new int[4 * 128];
    static int[] variableName = new int[16 * 32], variableData = new int[16 * 256], namelen = new int[16], valueLength = new int[16];
    static int[] scriptValue = new int[4 * 16384];
    static int stateValue, depthValue, written;
    static boolean isConnecting, scriptEnd, extensionError;
    static boolean nameCharacter(int characterCode) { return characterCode >= 'a' && characterCode <= 'z' || characterCode >= 'A' && characterCode <= 'Z' || characterCode == '_' || characterCode >= 128; }
    static boolean nameSuffix(int characterCode) { return nameCharacter(characterCode) || characterCode >= '0' && characterCode <= '9'; }
    static void error(String text) { Board.switchIo(0); TerminalIO.write("command parseValue: "); TerminalIO.write(text); TerminalIO.Characters(10); stateValue = 2; }
    static int read(int entryCount, int depth) {
        int currentIndex = 0, totalCount = 0, basePosition = depth * 4096, specialCharacter = depth * 128;
        while (currentIndex < entryCount) {
            while (currentIndex < entryCount && (source[basePosition + currentIndex] == 32 || source[basePosition + currentIndex] == 9)) currentIndex++;
            if (currentIndex == entryCount || source[basePosition + currentIndex] == '#') break;
            if (totalCount == 128) { error("낱말이 너무 많습니다"); return -1; }
            int startPosition = currentIndex, characterCode = source[basePosition + currentIndex], dataKind = 0;
            if (characterCode == ';') { dataKind = 1; currentIndex++; }
            else if (characterCode == '&') { if (currentIndex + 1 >= entryCount || source[basePosition + currentIndex + 1] != '&') { error("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } dataKind = 2; currentIndex += 2; }
            else if (characterCode == '|') { currentIndex++; dataKind = currentIndex < entryCount && source[basePosition + currentIndex] == '|' ? 3 : 4; if (dataKind == 3) currentIndex++; }
            else if (characterCode == '>') { currentIndex++; dataKind = currentIndex < entryCount && source[basePosition + currentIndex] == '>' ? 6 : 5; if (dataKind == 6) currentIndex++; }
            else if (characterCode == '<') { dataKind = 7; currentIndex++; }
            else {
                int quote = 0;
                while (currentIndex < entryCount) {
                    characterCode = source[basePosition + currentIndex];
                    if (characterCode == '`' && quote != 39 || characterCode == '$' && quote != 39 && currentIndex + 1 < entryCount && source[basePosition + currentIndex + 1] == '(') { error("command result 치환은 지원하지 않습니다"); return -1; }
                    if (characterCode == '\\' && quote != 39) { if (++currentIndex == entryCount) { error("line 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } currentIndex++; continue; }
                    if (characterCode == quote) { quote = 0; currentIndex++; continue; }
                    if (quote == 0 && (characterCode == 39 || characterCode == 34)) { quote = characterCode; currentIndex++; continue; }
                    if (quote == 0 && (characterCode == 32 || characterCode == 9 || characterCode == ';' || characterCode == '&' || characterCode == '|' || characterCode == '<' || characterCode == '>')) break;
                    currentIndex++;
                }
                if (quote != 0) { error("따옴표가 닫히지 않았습니다"); return -1; }
                if (currentIndex < entryCount && (source[basePosition + currentIndex] == '>' || source[basePosition + currentIndex] == '<')) {
                    boolean numericValue = currentIndex > startPosition;
                    for (int loopIndex = startPosition; loopIndex < currentIndex; loopIndex++) if (source[basePosition + loopIndex] < '0' || source[basePosition + loopIndex] > '9') numericValue = false;
                    if (numericValue) { error("번호를 지정한 file descriptorEntry inputOutput 전환은 지원하지 않습니다"); return -1; }
                }
            }
            kindValue[specialCharacter + totalCount] = dataKind; run[specialCharacter + totalCount] = startPosition; ending[specialCharacter + totalCount] = currentIndex; totalCount++;
        }
        boolean lexicalWord = false;
        for (int loopIndex = 0; loopIndex < totalCount; loopIndex++) {
            int temporaryData = kindValue[specialCharacter + loopIndex];
            if (temporaryData == 0) lexicalWord = true;
            else if (temporaryData >= 5) { if (++loopIndex == totalCount || kindValue[specialCharacter + loopIndex] != 0) { error("inputOutput 전환에 file 이름이 필요합니다"); return -1; } }
            else { if (!lexicalWord || loopIndex == totalCount - 1 && temporaryData != 1) { error("명령이 빠졌습니다"); return -1; } lexicalWord = false; }
        }
        if (totalCount > 0 && !lexicalWord && kindValue[specialCharacter + totalCount - 1] != 1) { error("명령이 빠졌습니다"); return -1; }
        return totalCount;
    }
    static boolean rangeText(int[] dataArray, int localStart, int entryCount, String characterPosition) {
        if (entryCount != characterPosition.length()) return false; for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) if (dataArray[localStart + loopIndex] != characterPosition.charAt(loopIndex)) return false; return true;
    }
    static void putValue(int byteData) {
        if (written >= CommandInterpreter.tokenValue.length) { if (!extensionError) error("변수를 펼친 명령이 너무 깁니다"); extensionError = true; return; }
        CommandInterpreter.tokenValue[written++] = byteData;
    }
    static void variableValue(int[] dataArray, int startPosition, int entryCount) {
        if (rangeText(dataArray, startPosition, entryCount, "PWD")) { putValue('/'); for (int loopIndex = 0; loopIndex < MemoryFiles.currentLength; loopIndex++) putValue(MemoryFiles.currentItem[loopIndex]); return; }
        if (rangeText(dataArray, startPosition, entryCount, "HOME")) { putValue('/'); return; }
        if (rangeText(dataArray, startPosition, entryCount, "?")) {
            int dataValue = stateValue, digit = 100; boolean hasStarted = false;
            while (digit > 0) { int trailingValue = dataValue / digit; if (trailingValue != 0 || hasStarted || digit == 1) { putValue('0' + trailingValue); hasStarted = true; } dataValue %= digit; digit /= 10; } return;
        }
        for (int loopIndex = 0; loopIndex < 16; loopIndex++) if (namelen[loopIndex] == entryCount) {
            boolean match = true; for (int innerPosition = 0; innerPosition < entryCount; innerPosition++) if (variableName[loopIndex * 32 + innerPosition] != dataArray[startPosition + innerPosition]) match = false;
            if (match) { for (int innerPosition = 0; innerPosition < valueLength[loopIndex]; innerPosition++) putValue(variableData[loopIndex * 256 + innerPosition]); return; }
        }
    }
    static boolean wordValue(int lexicalWordIndex, int depth) {
        int readCursor = run[depth * 128 + lexicalWordIndex], endPosition = ending[depth * 128 + lexicalWordIndex], basePosition = depth * 4096, quote = 0;
        if (readCursor < endPosition && source[basePosition + readCursor] == '~' && (readCursor + 1 == endPosition || source[basePosition + readCursor + 1] == '/')) { putValue('/'); readCursor++; }
        while (readCursor < endPosition) {
            int characterCode = source[basePosition + readCursor++];
            if (characterCode == quote) { quote = 0; continue; }
            if (quote == 0 && (characterCode == 39 || characterCode == 34)) { quote = characterCode; continue; }
            if (characterCode == '\\' && quote != 39) { int nextPosition = source[basePosition + readCursor++]; if (quote == 34 && nextPosition != '$' && nextPosition != '"' && nextPosition != '\\') putValue('\\'); putValue(nextPosition); continue; }
            if (characterCode == '$' && quote != 39 && readCursor < endPosition) {
                boolean brace = source[basePosition + readCursor] == '{'; if (brace) readCursor++;
                int begin = readCursor;
                if (readCursor < endPosition && source[basePosition + readCursor] == '?') readCursor++;
                else while (readCursor < endPosition && nameSuffix(source[basePosition + readCursor])) readCursor++;
                if (brace && (readCursor == endPosition || source[basePosition + readCursor] != '}')) { error("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (readCursor == begin && !brace) { putValue('$'); continue; }
                variableValue(source, basePosition + begin, readCursor - begin); if (brace) readCursor++; continue;
            }
            putValue(characterCode);
        }
        return !extensionError;
    }
    static int environmentSettings(int argumentIndex, boolean remove) {
        int localStart = CommandInterpreter.startingPoint[argumentIndex], endPosition = localStart + CommandInterpreter.lengthValue[argumentIndex], equalityPosition = localStart;
        while (equalityPosition < endPosition && CommandInterpreter.tokenValue[equalityPosition] != '=') equalityPosition++;
        int entryCount = equalityPosition - localStart;
        if (entryCount < 1 || entryCount > 31 || !nameCharacter(CommandInterpreter.tokenValue[localStart]) || !remove && equalityPosition == endPosition || endPosition - equalityPosition - 1 > 255) return 2;
        for (int loopIndex = localStart; loopIndex < equalityPosition; loopIndex++) if (!nameSuffix(CommandInterpreter.tokenValue[loopIndex])) return 2;
        if (rangeText(CommandInterpreter.tokenValue, localStart, entryCount, "PWD") || rangeText(CommandInterpreter.tokenValue, localStart, entryCount, "HOME")) return 2;
        int wasFound = -1, isEmptyState = -1;
        for (int loopIndex = 0; loopIndex < 16; loopIndex++) {
            if (namelen[loopIndex] == 0) isEmptyState = loopIndex;
            if (namelen[loopIndex] != entryCount) continue;
            boolean match = true; for (int innerPosition = 0; innerPosition < entryCount; innerPosition++) if (variableName[loopIndex * 32 + innerPosition] != CommandInterpreter.tokenValue[localStart + innerPosition]) match = false;
            if (match) wasFound = loopIndex;
        }
        if (remove) { if (wasFound >= 0) namelen[wasFound] = 0; return 0; }
        if (wasFound < 0) wasFound = isEmptyState; if (wasFound < 0) return 1;
        namelen[wasFound] = entryCount; valueLength[wasFound] = endPosition - equalityPosition - 1;
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) variableName[wasFound * 32 + loopIndex] = CommandInterpreter.tokenValue[localStart + loopIndex];
        for (int loopIndex = equalityPosition + 1; loopIndex < endPosition; loopIndex++) variableData[wasFound * 256 + loopIndex - equalityPosition - 1] = CommandInterpreter.tokenValue[loopIndex];
        return 0;
    }
    static void showEnvironment() {
        TerminalIO.write("HOME=/\nPWD="); MemoryFiles.currentWrite(); TerminalIO.Characters(10);
        for (int loopIndex = 0; loopIndex < 16; loopIndex++) if (namelen[loopIndex] > 0) {
            for (int innerPosition = 0; innerPosition < namelen[loopIndex]; innerPosition++) Board.writeSerial(variableName[loopIndex * 32 + innerPosition]); TerminalIO.Characters('=');
            for (int innerPosition = 0; innerPosition < valueLength[loopIndex]; innerPosition++) Board.writeSerial(variableData[loopIndex * 256 + innerPosition]); TerminalIO.Characters(10);
        }
    }
    static void executeCommand(int[] dataArray, int startDisplacement, int entryCount, int depth) {
        if (depth >= 4 || entryCount > 4096) { error("command 파일의 nestingValue 또는 line lengthValue 제한을 넘었습니다"); return; }
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) source[depth * 4096 + loopIndex] = dataArray[startDisplacement + loopIndex];
        int totalCount = read(entryCount, depth); if (totalCount < 0) return;
        int readCursor = 0, conditionMet = 1;
        while (readCursor < totalCount) {
            int groupEnd = readCursor;
            while (groupEnd < totalCount && (kindValue[depth * 128 + groupEnd] == 0 || kindValue[depth * 128 + groupEnd] >= 4)) groupEnd++;
            boolean execute = conditionMet == 1 || conditionMet == 2 && stateValue == 0 || conditionMet == 3 && stateValue != 0;
            if (execute) {
                boolean previousItemIndex = false;
                while (readCursor < groupEnd) {
                    int nextPosition = readCursor; while (nextPosition < groupEnd && kindValue[depth * 128 + nextPosition] != 4) nextPosition++;
                    boolean connectStream = nextPosition < groupEnd; int inputPage = -1, outputPage = -1, outMode = 0;
                    CommandInterpreter.tokenCount = 0; written = 0; extensionError = false;
                    for (int loopIndex = readCursor; loopIndex < nextPosition; loopIndex++) {
                        int dataKind = kindValue[depth * 128 + loopIndex];
                        if (dataKind >= 5) { if (dataKind == 7) { if (inputPage >= 0) { error("inputValue 전환이 겹쳤습니다"); return; } inputPage = ++loopIndex; } else { if (outputPage >= 0) { error("Output 전환이 겹쳤습니다"); return; } outputPage = ++loopIndex; outMode = dataKind; } continue; }
                        if (CommandInterpreter.tokenCount == 32) { error("인수가 너무 많습니다"); return; }
                        int argumentIndex = CommandInterpreter.tokenCount++; CommandInterpreter.startingPoint[argumentIndex] = written;
                        if (!wordValue(loopIndex, depth)) return;
                        CommandInterpreter.lengthValue[argumentIndex] = written - CommandInterpreter.startingPoint[argumentIndex];
                    }
                    isConnecting = previousItemIndex || connectStream || inputPage >= 0 || outputPage >= 0;
                    if (isConnecting && (CommandInterpreter.equalText(0, "vi") || CommandInterpreter.equalText(0, "edit") || CommandInterpreter.equalText(0, "load") || CommandInterpreter.equalText(0, "gui") || CommandInterpreter.equalText(0, "terminal") || CommandInterpreter.equalText(0, "sh") || CommandInterpreter.equalText(0, "source"))) { error("interactive 명령과 command 파일은 inputOutput 전환이나 streamValue 연결에 쓸 number 없습니다"); return; }
                    ShellIO.run(previousItemIndex, connectStream);
                    for (int redir = 0; redir < 2; redir++) {
                        int entryPosition = redir == 0 ? inputPage : outputPage; if (entryPosition < 0) continue;
                        int startPosition = written; if (!wordValue(entryPosition, depth)) { ShellIO.ending(); return; }
                        int processedValue = MemoryFiles.pathStart(written - startPosition);
                        for (int innerPosition = startPosition; processedValue >= 0 && innerPosition < written; innerPosition++) processedValue = MemoryFiles.pathByte(innerPosition - startPosition, CommandInterpreter.tokenValue[innerPosition]);
                        if (processedValue >= 0) processedValue = MemoryFiles.open(redir == 0 ? 0 : outMode == 6 ? 1089 : 577);
                        if (processedValue < 0) { ShellIO.ending(); CommandInterpreter.error(processedValue); stateValue = 1; return; }
                        if (redir == 0) ShellIO.inputFile = processedValue; else ShellIO.outputFile = processedValue;
                    }
                    ShellIO.allowInteractive = depth == 0 && readCursor == 0 && nextPosition == totalCount;
                    depthValue = depth; CommandInterpreter.result = 0; Board.switchIo(1);
                    CommandInterpreter.command();
                    Board.terminal(3);
                    int returnedValue = CommandInterpreter.result, streamError = ShellIO.failureValue;
                    ShellIO.ending(); isConnecting = false;
                    stateValue = streamError < 0 ? 1 : returnedValue;
                    if (streamError < 0) { CommandInterpreter.error(streamError); return; }
                    if (scriptEnd || returnedValue == -1005) return;
                    previousItemIndex = true; readCursor = nextPosition + 1;
                }
            }
            if (groupEnd < totalCount) conditionMet = kindValue[depth * 128 + groupEnd];
            readCursor = groupEnd + 1;
        }
    }
    static void executeFile() {
        if (CommandInterpreter.tokenCount != 2 || depthValue >= 3) { CommandInterpreter.result = 2; TerminalIO.write("사용법: sh file (nestingValue depthValue <= 3)\n"); return; }
        int depth = depthValue + 1, processedValue = CommandInterpreter.path(1); if (processedValue >= 0) processedValue = MemoryFiles.open(0);
        if (processedValue < 0) { CommandInterpreter.error(processedValue); return; }
        int entryCount = 0, byteData;
        while ((byteData = MemoryFiles.read(processedValue)) != 256 && byteData >= 0 && entryCount < 16384) scriptValue[depth * 16384 + entryCount++] = byteData;
        MemoryFiles.close(processedValue); Board.switchIo(0);
        for (int readCursor = 0; readCursor < entryCount && !scriptEnd;) {
            int endPosition = readCursor; while (endPosition < entryCount && scriptValue[depth * 16384 + endPosition] != 10) endPosition++;
            int validLength = endPosition - readCursor; if (validLength > 0 && scriptValue[depth * 16384 + endPosition - 1] == 13) validLength--;
            executeCommand(scriptValue, depth * 16384 + readCursor, validLength, depth); readCursor = endPosition + 1;
        }
        CommandInterpreter.result = stateValue; scriptEnd = false; depthValue = depth - 1;
    }
}
