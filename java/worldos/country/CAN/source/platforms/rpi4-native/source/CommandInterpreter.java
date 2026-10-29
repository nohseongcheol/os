// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 command line with quotes, Backspace, Ctrl-U, Ctrl-C and a RAM editor. */
public final class CommandInterpreter {
    static int[] line = new int[4096], tokenValue = new int[4096], startingPoint = new int[32], lengthValue = new int[32];
    static int[] editedContents = new int[16384], editName = new int[63];
    static int tokenCount, editNameLength, result;
    static boolean previousLine;
    static void originalByte(int value) { Board.writeSerial(value); }
    static int read_input_line() { return LineEditor.read(); }
    static boolean divideValues(int size) {
        int position = 0, ending = 0; tokenCount = 0;
        while (position < size) {
            while (position < size && (line[position] == 32 || line[position] == 9)) position++;
            if (position == size) break;
            if (tokenCount == 16) { TerminalIO.write("command parseValue: 인수가 너무 많습니다\n"); return false; }
            startingPoint[tokenCount] = ending; int quoteValue = 0;
            while (position < size) {
                int value = line[position++];
                if (quoteValue == 0 && (value == 32 || value == 9)) break;
                if (value == quoteValue) { quoteValue = 0; continue; }
                if (quoteValue == 0 && (value == 39 || value == 34)) { quoteValue = value; continue; }
                tokenValue[ending++] = value;
            }
            if (quoteValue != 0) { TerminalIO.write("command parseValue: 따옴표가 닫히지 않았습니다\n"); return false; }
            lengthValue[tokenCount] = ending - startingPoint[tokenCount]; tokenCount++;
        }
        return true;
    }
    static boolean equalText(int index, String wordText) {
        if (index >= tokenCount) return false;
        int positionIndex=0;
        for (int ordinalIndex=0; ordinalIndex<wordText.length(); ordinalIndex++) {
            int characterCode=wordText.charAt(ordinalIndex);
            if (characterCode>=0xd800 && characterCode<=0xdbff && ordinalIndex+1<wordText.length()) characterCode=0x10000+((characterCode-0xd800)<<10)+wordText.charAt(++ordinalIndex)-0xdc00;
            int byteCount=characterCode<128?1:characterCode<2048?2:characterCode<65536?3:4;
            for (int sequenceValue=byteCount-1; sequenceValue>=0; sequenceValue--) {
                int value=byteCount==1?characterCode:sequenceValue==byteCount-1?(byteCount==2?0xc0:byteCount==3?0xe0:0xf0)|(characterCode>>(6*sequenceValue)):0x80|((characterCode>>(6*sequenceValue))&63);
                if (positionIndex>=lengthValue[index] || tokenValue[startingPoint[index]+positionIndex++]!=value) return false;
            }
        }
        return positionIndex==lengthValue[index];
    }
    static int path(int index) {
        if (index >= tokenCount) return -22;
        int result = MemoryFiles.pathStart(lengthValue[index]); if (result < 0) return result;
        for (int loopIndex = 0; loopIndex < lengthValue[index]; loopIndex++) {
            result = MemoryFiles.pathByte(loopIndex, tokenValue[startingPoint[index] + loopIndex]); if (result < 0) return result;
        }
        return 0;
    }
    static void error(int index) { result = 1; TerminalIO.write("error "); TerminalIO.number(index); TerminalIO.Characters(10); }
    static void viewValue() {
        if (tokenCount != 2) { TerminalIO.write("사용법: cat file\n"); return; }
        int result = path(1); if (result < 0) { error(result); return; }
        int file = MemoryFiles.open(0); if (file < 0) { error(file); return; }
        while (true) { int value = MemoryFiles.read(file); if (value == 256) break; if (value < 0) { error(value); break; } originalByte(value); }
        MemoryFiles.close(file); TerminalIO.Characters(10);
    }
    static void editValue() {
        if (tokenCount != 2) { TerminalIO.write("사용법: edit file\n"); return; }
        int result = path(1); if (result < 0) { error(result); return; }
        editNameLength = lengthValue[1];
        for (int loopIndex = 0; loopIndex < editNameLength; loopIndex++) editName[loopIndex] = tokenValue[startingPoint[1] + loopIndex];
        TerminalIO.write("EDIT: file 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(maximumValue 16384바이트)\n");
        int size = 0;
        while (true) {
            TerminalIO.write("edit> "); int inputValue = read_input_line();
            if (inputValue < 0) { TerminalIO.write("EDIT CANCELLED\n"); return; }
            if (inputValue == 1 && line[0] == '.') break;
            if (inputValue + 1 > editedContents.length - size) { TerminalIO.write("EDIT CANCELLED: file too large\n"); return; }
            for (int loopIndex = 0; loopIndex < inputValue; loopIndex++) editedContents[size++] = line[loopIndex];
            editedContents[size++] = 10;
        }
        MemoryFiles.pathStart(editNameLength);
        for (int loopIndex = 0; loopIndex < editNameLength; loopIndex++) MemoryFiles.pathByte(loopIndex, editName[loopIndex]);
        int file = MemoryFiles.open(577); if (file < 0) { error(file); return; }
        for (int loopIndex = 0; loopIndex < size; loopIndex++) MemoryFiles.write(file, editedContents[loopIndex]);
        MemoryFiles.close(file); TerminalIO.write("SAVED "); TerminalIO.number(size); TerminalIO.write("byteValue(주기억 file)\n");
    }
    static int hexadecimalValue(int value) {
        if (value >= '0' && value <= '9') return value - '0';
        if (value >= 'a' && value <= 'f') return value - 'a' + 10;
        if (value >= 'A' && value <= 'F') return value - 'A' + 10;
        return -1;
    }
    static void binaryIo(boolean putValue) {
        if (tokenCount != 2) { TerminalIO.write("사용법: load file | hex file\n"); return; }
        int result = path(1); if (result < 0) { error(result); return; }
        if (!putValue) {
            int file = MemoryFiles.open(0); if (file < 0) { error(file); return; }
            TerminalIO.write("HEX BEGIN "); TerminalIO.number(MemoryFiles.size(file)); TerminalIO.Characters(10);
            int entryCount = 0;
            while (true) {
                int value = MemoryFiles.read(file); if (value < 0 || value == 256) break;
                TerminalIO.Characters("0123456789abcdef".charAt(value >> 4)); TerminalIO.Characters("0123456789abcdef".charAt(value & 15));
                if (++entryCount % 32 == 0) TerminalIO.Characters(10);
            }
            if (entryCount % 32 != 0) TerminalIO.Characters(10);
            MemoryFiles.close(file); TerminalIO.write("HEX END\n"); return;
        }
        editNameLength = lengthValue[1];
        for (int loopIndex = 0; loopIndex < editNameLength; loopIndex++) editName[loopIndex] = tokenValue[startingPoint[1] + loopIndex];
        TerminalIO.write("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int size = 0;
        while (true) {
            TerminalIO.write("hex> "); int inputValue = read_input_line();
            if (inputValue < 0) { TerminalIO.write("LOAD CANCELLED\n"); return; }
            if (inputValue == 1 && line[0] == '.') break;
            int frontValue = -1;
            for (int loopIndex = 0; loopIndex < inputValue; loopIndex++) {
                if (line[loopIndex] == 32 || line[loopIndex] == 9) continue;
                int value = hexadecimalValue(line[loopIndex]);
                if (value < 0 || size >= editedContents.length) { TerminalIO.write("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontValue < 0) frontValue = value; else { editedContents[size++] = frontValue * 16 + value; frontValue = -1; }
            }
            if (frontValue >= 0) { TerminalIO.write("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        MemoryFiles.pathStart(editNameLength);
        for (int loopIndex = 0; loopIndex < editNameLength; loopIndex++) MemoryFiles.pathByte(loopIndex, editName[loopIndex]);
        int file = MemoryFiles.open(577); if (file < 0) { error(file); return; }
        for (int loopIndex = 0; loopIndex < size; loopIndex++) MemoryFiles.write(file, editedContents[loopIndex]);
        MemoryFiles.close(file); TerminalIO.write("LOADED "); TerminalIO.number(size); TerminalIO.write("byteValue(주기억 file)\n");
    }
    static int tools(int index) {
        return ToolEntry(index, 1);
    }
    static int ToolEntry(int index, int run) {
        if (tokenCount - run > 8) return -22;
        Board.prepareArguments(tokenCount - run);
        for (int firstData = run; firstData < tokenCount; firstData++) {
            if (lengthValue[firstData] > 255) return -36;
            for (int loopIndex = 0; loopIndex < lengthValue[firstData]; loopIndex++) Board.argumentByte(firstData - run, loopIndex, tokenValue[startingPoint[firstData] + loopIndex]);
        }
        return index == -2 ? Board.executeLinuxFile() : index < 0 ? Board.executeUserFile() : Board.runUserProgram(index);
    }
    static int PythonBundle() {
        if (tokenCount > 8) return -22;
        Board.prepareArguments(tokenCount);
        String path = "/lib/Bundle.py";
        // Write a Java string to the shell's UTF-8 argument buffer.
        int positionIndex = 0;
        for (int ordinalIndex = 0; ordinalIndex < path.length(); ordinalIndex++) {
            int characterValue = path.charAt(ordinalIndex);
            if (characterValue < 128) Board.argumentByte(0, positionIndex++, characterValue);
            else { Board.argumentByte(0, positionIndex++, 0xe0 | (characterValue >> 12)); Board.argumentByte(0, positionIndex++, 0x80 | ((characterValue >> 6) & 63)); Board.argumentByte(0, positionIndex++, 0x80 | (characterValue & 63)); }
        }
        for (int ordinalIndex = 1; ordinalIndex < tokenCount; ordinalIndex++) {
            if (lengthValue[ordinalIndex] > 255) return -36;
            for (int characterValue = 0; characterValue < lengthValue[ordinalIndex]; characterValue++) Board.argumentByte(ordinalIndex, characterValue, tokenValue[startingPoint[ordinalIndex] + characterValue]);
        }
        return Board.runUserProgram(12);
    }
    static int executionFormat() {
        int processedValue = path(0); if (processedValue < 0) return processedValue;
        int file = MemoryFiles.open(0); if (file < 0) return file;
        int firstData = MemoryFiles.read(file), byteData = MemoryFiles.read(file), characterCode = MemoryFiles.read(file), trailingValue = MemoryFiles.read(file);
        MemoryFiles.close(file);
        if (firstData == 127 && byteData == 'E' && characterCode == 'L' && trailingValue == 'F') return 1;
        if (firstData == 'P' && byteData == 'K' && characterCode == 3 && trailingValue == 4) return 2;
        return 0;
    }
    static int runExample(int index, String arguments) {
        Board.prepareArguments(1);
        for (int loopIndex = 0; loopIndex < arguments.length(); loopIndex++) Board.argumentByte(0, loopIndex, arguments.charAt(loopIndex));
        return Board.runUserProgram(index);
    }
    static void textByte(int file, int value) { MemoryFiles.write(file, value); }
    static void staticFile(String name, String contentValue) {
        // Bundle filenames use ASCII; file contents are stored as UTF-8.
        MemoryFiles.pathStart(name.length());
        for (int loopIndex = 0; loopIndex < name.length(); loopIndex++) MemoryFiles.pathByte(loopIndex, name.charAt(loopIndex));
        int file = MemoryFiles.open(193); if (file < 0) return;
        for (int loopIndex = 0; loopIndex < contentValue.length(); loopIndex++) {
            int characterCode = contentValue.charAt(loopIndex);
            if (characterCode >= 0xd800 && characterCode <= 0xdbff && loopIndex + 1 < contentValue.length()) characterCode = 0x10000 + ((characterCode - 0xd800) << 10) + contentValue.charAt(++loopIndex) - 0xdc00;
            if (characterCode < 128) textByte(file, characterCode);
            else {
                int number = characterCode < 2048 ? 2 : characterCode < 65536 ? 3 : 4;
                textByte(file, (number == 2 ? 0xc0 : number == 3 ? 0xe0 : 0xf0) | (characterCode >> (6 * (number - 1))));
                for (int entryCount = number - 1; entryCount > 0; entryCount--) textByte(file, 0x80 | ((characterCode >> (6 * (entryCount - 1))) & 63));
            }
        }
        MemoryFiles.close(file);
    }
    static void hangulHelp() {
        TerminalIO.write("Press F9 or Shift+Space to switch to the English keyboard.\n");
        TerminalIO.write("  [EN] keyboard; [EN] ASCII\n");
        TerminalIO.write("  a → a\n");
        TerminalIO.write("  F9: EN ↔ English | Ctrl+Shift+V: UTF-8\n");
        TerminalIO.write("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        TerminalIO.write("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int examplePath(String name) {
        int byteCount = 0;
        for (int loopIndex = 0; loopIndex < name.length(); loopIndex++) { int characterCode = name.charAt(loopIndex); if (characterCode >= 0xd800 && characterCode <= 0xdfff) return -22; byteCount += characterCode < 128 ? 1 : characterCode < 2048 ? 2 : 3; }
        int processedValue = MemoryFiles.pathStart(byteCount); if (processedValue < 0) return processedValue;
        int positionIndex = 0;
        for (int loopIndex = 0; loopIndex < name.length(); loopIndex++) {
            int characterCode = name.charAt(loopIndex);
            if (characterCode < 128) MemoryFiles.pathByte(positionIndex++, characterCode);
            else if (characterCode < 2048) { MemoryFiles.pathByte(positionIndex++, 0xc0 | (characterCode >> 6)); MemoryFiles.pathByte(positionIndex++, 0x80 | (characterCode & 63)); }
            else { MemoryFiles.pathByte(positionIndex++, 0xe0 | (characterCode >> 12)); MemoryFiles.pathByte(positionIndex++, 0x80 | ((characterCode >> 6) & 63)); MemoryFiles.pathByte(positionIndex++, 0x80 | (characterCode & 63)); }
        }
        return 0;
    }
    static int exampleDirectory(String name) {
        int processedValue = examplePath(name); if (processedValue < 0) return processedValue;
        processedValue = MemoryFiles.createDirectory(); return processedValue == -17 ? 0 : processedValue;
    }
    static int exampleFile(String name, String data) {
        int processedValue = examplePath(name); if (processedValue < 0) return processedValue;
        int file = MemoryFiles.open(193); if (file == -17) return 0; if (file < 0) return file;
        for (int loopIndex = 0; loopIndex < data.length(); loopIndex += 2) {
            processedValue = MemoryFiles.write(file, hexadecimalValue(data.charAt(loopIndex)) * 16 + hexadecimalValue(data.charAt(loopIndex + 1)));
            if (processedValue < 0) { MemoryFiles.close(file); return processedValue; }
        }
        return MemoryFiles.close(file);
    }
    static void showHelp() {
        systemTool.showHelp();
        TerminalIO.write("sshd / secureShell start|stop|status: SSH :22 (user, 장치별 passwordValue)\n");
        TerminalIO.write("vncd / RemoteDisplay start|stop|status: VNC :5900 (장치별 passwordValue)\n");
        TerminalIO.write("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        TerminalIO.write("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        TerminalIO.write("wc grep head tail tee env export unset history sh source true false exit\n");
        TerminalIO.write("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        TerminalIO.write("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        TerminalIO.write("cornerValue + leftSide 버튼 dragValue: terminal size changeValue; terminal size: columnValue/rowValue\n");
        TerminalIO.write("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        TerminalIO.write("vi FILE: i to insert; Esc then :wq to save and quit\n");
        TerminalIO.write("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        TerminalIO.write("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        TerminalIO.write("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        TerminalIO.write("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        TerminalIO.write("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        TerminalIO.write("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        TerminalIO.write("python FILE.py | python -c 'CODE' (MicroPython)\n");
        TerminalIO.write("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        TerminalIO.write("pip: MicroPython sourceTree installValue; Host --network --pip neededValue; /lib는 RAM\n");
        TerminalIO.write("gui | run cpp | net test | tasks | selftest | samples\n");
        TerminalIO.write("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        TerminalIO.write("/example/java /example/c /example/python: examples ready at boot\n");
        TerminalIO.write("example java|c|python: restore missing examples (keeps existing files)\n");
        hangulHelp();
    }
    static void terminal(boolean wasSwitched) {
        if (wasSwitched && Board.terminal(2) != 0) { Board.terminal(0); TerminalIO.write("TERMINAL CLOSED\n"); }
        else if (Board.terminal(1) < 0) error(-19);
        else TerminalIO.write("TERMINAL READY — English terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void command() {
        if (tokenCount == 0) return;
        if (systemTool.executeCommand()) return;
        if (equalText(0,"sshd") || equalText(0,"secureShell") || equalText(0,"vncd") || equalText(0,"RemoteDisplay")) {
            int kindValue=equalText(0,"vncd")||equalText(0,"RemoteDisplay")?1:0;
            int action=equalText(1,"start")||equalText(1,"run")?1:equalText(1,"stop")||equalText(1,"stop")?0:2;
            int stateValue=Board.remoteControl(kindValue,action);
            if(stateValue<0)error(stateValue);else TerminalIO.write(Board.remoteControl(kindValue,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (equalText(0, "help") || equalText(0, "h")) { if (equalText(1, "ko") || equalText(1, "input")) hangulHelp(); else showHelp(); }
        else if (equalText(0, "info") || equalText(0, "i")) Kernel.systemInformation();
        else if (equalText(0, "pwd")) { MemoryFiles.currentWrite(); TerminalIO.Characters(10); }
        else if (equalText(0, "cd")) {
            int processedValue;
            if (tokenCount == 1) { MemoryFiles.pathStart(1); processedValue = MemoryFiles.pathByte(0, '/'); } else processedValue = tokenCount == 2 ? path(1) : -22;
            if (processedValue >= 0) processedValue = MemoryFiles.changeDirectory(); if (processedValue < 0) error(processedValue);
        }
        else if (equalText(0, "ls") || equalText(0, "f")) {
            int argumentIndex = equalText(1, "-l") ? 2 : 1, processedValue;
            if (tokenCount == argumentIndex) { MemoryFiles.pathStart(1); processedValue = MemoryFiles.pathByte(0, '.'); } else processedValue = tokenCount == argumentIndex + 1 ? path(argumentIndex) : -22;
            if (processedValue >= 0) processedValue = MemoryFiles.pathEntries(); if (processedValue < 0) error(processedValue);
        }
        else if (equalText(0, "mkdir") || equalText(0, "rmdir") || equalText(0, "touch")) ShellTools.fileJob(equalText(0, "mkdir") ? "mkdir" : equalText(0, "rmdir") ? "rmdir" : "touch");
        else if (equalText(0, "cp") || equalText(0, "mv")) ShellTools.copyValue(equalText(0, "mv"));
        else if (equalText(0, "cat")) ShellTools.viewValue();
        else if (equalText(0, "wc")) ShellTools.countingValue();
        else if (equalText(0, "grep")) ShellTools.findEntry();
        else if (equalText(0, "head") || equalText(0, "tail")) ShellTools.headValue(equalText(0, "tail"));
        else if (equalText(0, "tee")) ShellTools.writeTogether();
        else if (equalText(0, "env")) ShellSyntax.showEnvironment();
        else if (equalText(0, "export") || equalText(0, "unset")) {
            if (tokenCount == 1) ShellSyntax.showEnvironment();
            for (int loopIndex = 1; loopIndex < tokenCount; loopIndex++) { int processedValue = ShellSyntax.environmentSettings(loopIndex, equalText(0, "unset")); if (processedValue != 0) { result = processedValue; TerminalIO.write("command parseValue: variableValue 이름이 잘못되었거나 예약된 이름이거나 environment 공간이 가득 찼습니다\n"); } }
        }
        else if (equalText(0, "sh") || equalText(0, "source")) ShellSyntax.executeFile();
        else if (equalText(0, "true")) result = 0;
        else if (equalText(0, "false")) result = 1;
        else if (equalText(0, "history")) LineEditor.showLog();
        else if (equalText(0, "exit")) {
            if (ShellSyntax.depthValue > 0) { result = tokenCount == 1 ? ShellSyntax.stateValue : ShellTools.digitValue(1); if (result < 0 || result > 255) result = 2; ShellSyntax.scriptEnd = true; }
            else if (Board.terminal(2) != 0) terminal(true);
            else TerminalIO.write("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (equalText(0, "edit")) editValue();
        else if (equalText(0, "load") || equalText(0, "hex")) binaryIo(equalText(0, "load"));
        else if (equalText(0, "rm")) {
            if (tokenCount < 2) { result = 2; TerminalIO.write("사용법: rm file...\n"); }
            for (int loopIndex = 1; loopIndex < tokenCount; loopIndex++) { int processedValue = path(loopIndex); if (processedValue == 0) processedValue = MemoryFiles.eraseEntry(); if (processedValue < 0) error(processedValue); }
        }
        else if (equalText(0, "echo")) {
            int startPosition = equalText(1, "-n") ? 2 : 1;
            for (int firstData = startPosition; firstData < tokenCount; firstData++) { if (firstData > startPosition) TerminalIO.Characters(32); for (int loopIndex = 0; loopIndex < lengthValue[firstData]; loopIndex++) Board.writeSerial(tokenValue[startingPoint[firstData] + loopIndex]); }
            if (startPosition == 1) TerminalIO.Characters(10);
        }
        else if (equalText(0, "clear")) TerminalIO.write("\u001b[2J\u001b[H");
        else if (equalText(0, "javac") || equalText(0, "java") || equalText(0, "python") || equalText(0, "pip")) {
            int processedValue = equalText(0, "pip") ? PythonBundle() : tools(equalText(0, "javac") ? 10 : equalText(0, "java") ? 11 : 12); result = processedValue == -1005 ? -1005 : processedValue < 0 ? 126 : processedValue;
            if (processedValue != -1005 && !ShellSyntax.isConnecting) { TerminalIO.write("exit "); TerminalIO.number(processedValue); TerminalIO.Characters(10); }
        }
        else if (equalText(0, "vi")) { int processedValue = tools(13); result = processedValue == -1005 ? -1005 : processedValue < 0 ? 126 : processedValue; }
        else if (equalText(0, "cc") || equalText(0, "tcc")) { int processedValue = tools(15); result = processedValue < 0 ? 126 : processedValue; if (!ShellSyntax.isConnecting) { TerminalIO.write("exit "); TerminalIO.number(processedValue); TerminalIO.Characters(10); } }
        else if (equalText(0, "jaot")) { int processedValue = tools(16); result = processedValue < 0 ? 126 : processedValue; if (!ShellSyntax.isConnecting) { TerminalIO.write("exit "); TerminalIO.number(processedValue); TerminalIO.Characters(10); } }
        else if (equalText(0, "terminal")) {
            if (equalText(1, "size")) { int size = Board.terminal(13); TerminalIO.write("TERMINAL SIZE "); TerminalIO.number(size & 65535); TerminalIO.Characters('x'); TerminalIO.number(size >>> 16); TerminalIO.Characters(10); }
            else terminal(false);
        }
        else if (equalText(0, "gui") || equalText(0, "v")) { Board.terminal(9); Desktop.executeCommand(); }
        else if (equalText(0, "c")) Kernel.testC();
        else if (equalText(0, "tasks") || equalText(0, "t")) Kernel.testTasks();
        else if (equalText(0, "g")) Kernel.Screen();
        else if (equalText(0, "selftest") || equalText(0, "u")) Kernel.testUserPrograms();
        else if (equalText(0, "e") || (equalText(0, "run") && equalText(1, "cpp"))) {
            int processedValue = Board.runUserProgram(0); if (processedValue == 0) TerminalIO.write("ELF DEMO PASS\n"); else error(processedValue);
        }
        else if (equalText(0, "run")) { int processedValue = equalText(1, "--linux") ? ToolEntry(-2, 2) : tools(-1); result = processedValue == -1005 ? -1005 : processedValue < 0 ? 126 : processedValue; if (processedValue != -1005 && !ShellSyntax.isConnecting) { TerminalIO.write("exit "); TerminalIO.number(processedValue); TerminalIO.Characters(10); } }
        else if (equalText(0, "n") || (equalText(0, "net") && equalText(1, "test"))) Kernel.testNetworking();
        else if (equalText(0, "ftpd")) {
            if (equalText(1, "start")) { int processedValue = Board.fileTransferService(1); if (processedValue < 0) error(processedValue); else { TerminalIO.write("FTP listening "); systemTool.writeAddress(Board.networkStatus(0,0)); TerminalIO.write(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (equalText(1, "stop")) { Board.fileTransferService(0); TerminalIO.write("FTP stopped\n"); }
            else TerminalIO.write(Board.fileTransferService(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (equalText(0, "samples")) { Bundle.prepare(); TerminalIO.write("SAMPLES READY (existing files kept)\n"); }
        else if (equalText(0, "example")) {
            int language = equalText(1, "java") ? 0 : equalText(1, "c") ? 1 : equalText(1, "python") ? 2 : -1;
            if (tokenCount != 2 || language < 0) TerminalIO.write("example java|c|python: Output, file, 네트워크, 그래픽, Java Swing window examples\n");
            else { int processedValue = ExampleBundle.installValue(language); if (processedValue < 0) { error(processedValue); if (processedValue == -28) TerminalIO.write("RAM full: remove unused files, then retry example\n"); } else TerminalIO.write("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formatValue = executionFormat();
            if (formatValue == 1 || formatValue == 2) {
                int processedValue = ToolEntry(formatValue == 1 ? -1 : 14, 0); result = processedValue == -1005 ? -1005 : processedValue < 0 ? 126 : processedValue;
                if (processedValue != -1005 && !ShellSyntax.isConnecting) { TerminalIO.write("exit "); TerminalIO.number(processedValue); TerminalIO.Characters(10); }
            } else if (formatValue == 0) { result = 126; TerminalIO.write("실행할 number 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { result = 127; TerminalIO.write("Unknown command. help: commands\n"); }
        }
    }
    public static void executeCommand() {
        Bundle.prepare();
        for (int language = 0; language < 3; language++) { int processedValue = ExampleBundle.installValue(language); if (processedValue < 0) error(processedValue); }
        showHelp();
        while (true) {
            windowSession.processValueEntry(); if (windowSession.resumeExecution()) continue;
            if (!windowSession.readContinuation) TerminalIO.write("jkoros-native> "); LineEditor.commandLine = true; Board.remoteWait(1); int size = read_input_line(); Board.remoteWait(0); LineEditor.commandLine = false;
            if (size == -3) continue;
            if (size == -2) TerminalIO.write("command parseValue: 명령줄이 너무 깁니다\n");
            if (size >= 0) { ShellSyntax.scriptEnd = false; ShellSyntax.executeCommand(line, 0, size, 0); } else ShellSyntax.stateValue = 130;
            Board.endRemoteCommand(ShellSyntax.stateValue);
            LineEditor.size = LineEditor.cursorValue = LineEditor.startWindow = 0;
        }
    }
}
