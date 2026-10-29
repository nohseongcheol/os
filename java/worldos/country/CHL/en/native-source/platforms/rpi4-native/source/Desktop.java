// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Small launcher on the framebuffer, controlled by UART TAB/ENTER/Q. Its limited UI uses a project-defined 5x7 Latin font, with no Swing, USB HID or full input method. */
public final class Desktop {
    static String characterValues = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // Seven rows per glyph, each expressed by two hexadecimal digits. A project-defined 5x7 font.
    static String shapesList =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int digitValue(int characterValue) { return characterValue <= '9' ? characterValue - '0' : characterValue - 'A' + 10; }
    static void text(int horizontalPosition, int verticalPosition, String contentValue, int colourValue) {
        for (int characterValue = 0; characterValue < contentValue.length(); characterValue++) {
            int foundValue = -1;
            for (int candidate = 0; candidate < characterValues.length(); candidate++) if (characterValues.charAt(candidate) == contentValue.charAt(characterValue)) foundValue = candidate;
            if (foundValue < 0) continue;
            for (int rowValue = 0; rowValue < 7; rowValue++) {
                int position = foundValue * 14 + rowValue * 2;
                int bitValue = digitValue(shapesList.charAt(position)) * 16 + digitValue(shapesList.charAt(position + 1));
                for (int columnValue = 0; columnValue < 5; columnValue++) if ((bitValue & (16 >> columnValue)) != 0)
                    Kernel.rectangle(horizontalPosition + characterValue * 12 + columnValue * 2, verticalPosition + rowValue * 2, 2, 2, colourValue);
            }
        }
    }
    static void paintScreen(int selectionValue, String stateValue) {
        Kernel.rectangle(0, 0, Board.screenWidth(), Board.screenHeight(), 0x302018);
        Kernel.rectangle(32, 24, 576, 432, 0xefe8e2);
        Kernel.rectangle(32, 24, 576, 48, 0x905020);
        text(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int index = 0; index < 5; index++) {
            Kernel.rectangle(64, 112 + index * 52, 512, 40, index == selectionValue ? 0xd0a040 : 0xd8d0c8);
            text(84, 128 + index * 52, index == 0 ? "RUN C++ FILE PROGRAM" : index == 1 ? "RUN UDP LOOPBACK" : index == 2 ? "COMPILE AND RUN JAVA" : index == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        text(68, 384, stateValue, 0x205020);
        text(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void executeCommand() {
        if (Board.prepareScreen() == 0) { TerminalIO.write("GUI unavailable\n"); return; }
        int selectionValue = 0;
        String stateValue = "READY";
        boolean previousLine = CommandInterpreter.previousLine;
        paintScreen(selectionValue, stateValue);
        TerminalIO.write("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int inputValue = Board.readSerial();
            if (inputValue < 0) { Board.yieldProcessor(); continue; }
            if (inputValue == 10 && previousLine) { previousLine = false; continue; }
            previousLine = inputValue == 13;
            if (inputValue >= '1' && inputValue <= '5') { selectionValue = inputValue - '1'; inputValue = 13; }
            if (inputValue == 't' || inputValue == 'T') { CommandInterpreter.terminal(false); return; }
            if (inputValue == 'q' || inputValue == 'Q' || inputValue == 27) break;
            if (inputValue == 9 || inputValue == 'j') {
                selectionValue = (selectionValue + 1) % 5; paintScreen(selectionValue, stateValue); TerminalIO.write("GUI FOCUS "); TerminalIO.number(selectionValue); TerminalIO.Characters(10);
            } else if (inputValue == 13 || inputValue == 10) {
                if (selectionValue == 4) { CommandInterpreter.terminal(false); return; }
                int result;
                if (selectionValue < 2) result = Board.runUserProgram(selectionValue == 0 ? 0 : 9);
                else if (selectionValue == 2) {
                    result = CommandInterpreter.runExample(10, "Hello.java");
                    if (result == 0) result = CommandInterpreter.runExample(11, "Hello");
                } else result = CommandInterpreter.runExample(12, "hello.py");
                stateValue = result != 0 ? "PROGRAM FAILED" : selectionValue == 0 ? "C++ FILE OK" : selectionValue == 1 ? "UDP LOOPBACK OK" : selectionValue == 2 ? "JAVA OK" : "MICROPYTHON OK";
                paintScreen(selectionValue, stateValue);
                TerminalIO.write("GUI ACTION "); TerminalIO.number(selectionValue); TerminalIO.write(" RESULT "); TerminalIO.number(result); TerminalIO.Characters(10);
            }
        }
        Kernel.Screen();
        TerminalIO.write("GUI EXIT\n");
    }
}
