// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eight files retained for the session. Failed source editing or compilation preserves existing files. */
public final class MemoryFileSystem {
    static final int maximumSize = 16384;
    static int[] namesList = new int[8 * 64];
    static int[] sizeList = new int[8];
    static int[] openCount = new int[8], permissionGrants = new int[8];
    static int[] name = new int[64];
    static int[] editValue = new int[maximumSize];
    static boolean isEditing = false;
    static boolean overflowValue = false;
    static int editSize = 0;

    static boolean checkName(int[] characterValue, int lengthValue) {
        if (lengthValue < 1 || lengthValue > 63) return false;
        for (int number = 0; number < lengthValue; number++) {
            int value = characterValue[number];
            if (!(value >= 'a' && value <= 'z') && !(value >= 'A' && value <= 'Z')
                && !(value >= '0' && value <= '9') && value != '_' && value != '-' && value != '.') return false;
        }
        return characterValue[0] != '.';
    }

    static int findEntry(int[] characterValue, int lengthValue) {
        if (!checkName(characterValue, lengthValue)) return -22;
        for (int number = 0; number < 8; number++) {
            boolean equalText = namesList[number * 64 + lengthValue] == 0;
            for (int slotEntry = 0; slotEntry < lengthValue; slotEntry++) if (namesList[number * 64 + slotEntry] != characterValue[slotEntry]) equalText = false;
            if (equalText) return number;
        }
        return -2;
    }

    static int storeValue(int[] characterValue, int lengthValue, int[] data, int size) {
        if (!checkName(characterValue, lengthValue) || size < 0 || size > data.length) return -22;
        if (size > maximumSize) return -90;
        int index = findEntry(characterValue, lengthValue);
        if (index == -2) {
            for (int number = 0; number < 8 && index < 0; number++) if (namesList[number * 64] == 0 && openCount[number] == 0) index = number;
            if (index >= 0) permissionGrants[index] = 438;
        }
        if (index < 0) return -28;
        int address = deviceValue.fileMemory() + index * maximumSize;
        for (int number = 0; number < size; number++) deviceValue.writeMemory(address + number, data[number]);
        for (int number = 0; number < 64; number++) namesList[index * 64 + number] = number < lengthValue ? characterValue[number] : 0;
        sizeList[index] = size;
        return size;
    }

    static void entryList() {
        for (int number = 0; number < 8; number++) if (namesList[number * 64] != 0) {
            for (int slotEntry = 0; slotEntry < 64 && namesList[number * 64 + slotEntry] != 0; slotEntry++) TextTerminal.Characters(namesList[number * 64 + slotEntry]);
            TextTerminal.write("  "); TextTerminal.writeNumber(sizeList[number]); TextTerminal.write("byteValue\n");
        }
        TextTerminal.write(StorageDeviceConnection.isAvailable ? "file 8칸, 파일당 16384바이트; sync로 storeValue 장치에 보존\n"
            : "temporaryValue file 8칸, 파일당 16384바이트; retryValue 시작하면 사라짐\n");
    }

    static void command(int[] inputValue, int run, int lengthValue, int action) {
        while (run < lengthValue && inputValue[run] == ' ') run++;
        int ending = lengthValue;
        while (ending > run && inputValue[ending - 1] == ' ') ending--;
        int number = ending - run;
        if (number < 1 || number > 63) { TextTerminal.write("올바르지 않은 file name\n"); return; }
        for (int slotEntry = 0; slotEntry < 64; slotEntry++) name[slotEntry] = slotEntry < number ? inputValue[run + slotEntry] : 0;
        int index = findEntry(name, number);
        if (index == -22) { TextTerminal.write("올바르지 않은 file name\n"); return; }
        if (action == 0) {
            isEditing = true; editSize = 0; overflowValue = false;
            TextTerminal.write("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (index < 0) TextTerminal.write("파일을 찾을 number 없습니다\n");
        else if (action == 1) {
            int address = deviceValue.fileMemory() + index * maximumSize;
            for (int slotEntry = 0; slotEntry < sizeList[index]; slotEntry++) TextTerminal.Characters(deviceValue.readMemory(address + slotEntry));
            TextTerminal.Characters(10);
        } else { namesList[index * 64] = 0; sizeList[index] = 0; TextTerminal.write("파일을 지웠습니다\n"); }
    }

    static boolean isExact(int[] inputValue, int lengthValue, String phraseValue) {
        if (lengthValue != phraseValue.length()) return false;
        for (int slotEntry = 0; slotEntry < lengthValue; slotEntry++) if (inputValue[slotEntry] != phraseValue.charAt(slotEntry)) return false;
        return true;
    }

    static void editedLine(int[] inputValue, int lengthValue, boolean lineOverflow) {
        if (isExact(inputValue, lengthValue, ".cancel")) {
            isEditing = false; TextTerminal.write("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (isExact(inputValue, lengthValue, ".save")) {
            isEditing = false;
            if (overflowValue) { TextTerminal.write("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int number = 0;
            while (number < 64 && name[number] != 0) number++;
            int result = storeValue(name, number, editValue, editSize);
            TextTerminal.write(result >= 0 ? "보존한 byteValue number: " : "보존 failureValue: ");
            TextTerminal.writeNumber(result); TextTerminal.Characters(10);
        } else if (lineOverflow || lengthValue + 1 > maximumSize - editSize) overflowValue = true;
        else {
            for (int number = 0; number < lengthValue; number++) editValue[editSize++] = inputValue[number];
            editValue[editSize++] = 10;
        }
    }

    static void examples(String file, String contentValue) {
        for (int number = 0; number < 64; number++) name[number] = number < file.length() ? file.charAt(number) : 0;
        for (int number = 0; number < contentValue.length(); number++) editValue[number] = contentValue.charAt(number);
        storeValue(name, file.length(), editValue, contentValue.length());
    }

    static void prepare() {
        examples("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int groupValue = deviceValue.javaFileBundle(), size = deviceValue.javaFileBundleSize();
        if (size < 8 || ExecutionManager.number(groupValue) != 0x464a4b4a) { TextTerminal.write("올바르지 않은 Java file groupValue\n"); return; }
        int itemCount = ExecutionManager.number(groupValue + 4);
        if (itemCount < 0 || itemCount > 8 || itemCount > (size - 8) / 72) { TextTerminal.write("올바르지 않은 Java file entryList\n"); return; }
        for (int number = 0; number < itemCount; number++) {
            int entryValue = groupValue + 8 + number * 72, lengthValue = 0;
            for (int slotEntry = 0; slotEntry < 64; slotEntry++) name[slotEntry] = deviceValue.readMemory(entryValue + slotEntry);
            while (lengthValue < 64 && name[lengthValue] != 0) lengthValue++;
            int position = ExecutionManager.number(entryValue + 64), fileSize = ExecutionManager.number(entryValue + 68);
            if (!checkName(name, lengthValue) || fileSize < 0 || fileSize > maximumSize || position < 8 + itemCount * 72 || position > size - fileSize) {
                TextTerminal.write("올바르지 않은 Java file entryValue\n"); return;
            }
            for (int slotEntry = 0; slotEntry < fileSize; slotEntry++) editValue[slotEntry] = deviceValue.readMemory(groupValue + position + slotEntry);
            if (storeValue(name, lengthValue, editValue, fileSize) < 0) { TextTerminal.write("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
