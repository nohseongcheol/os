// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Restricted JVM running in ring 3. Checks file, stack, reference and branch bounds during execution. */
public final class JavaMachine {
    static int[] file = new int[16384], fileNameText = new int[64];
    static int[] constantTag = new int[512], constantFirstValue = new int[512], constantSecondValue = new int[512], stringReference = new int[512];
    static int[] methodNameText = new int[32], methodType = new int[32], methodAccess = new int[32];
    static int[] methodStart = new int[32], methodEnd = new int[32], methodStack = new int[32], methodLocals = new int[32];
    static int[] methodArgumentCount = new int[32], methodArgumentType = new int[512], methodReturn = new int[32];
    static int[] boundaryValue = new int[16384];
    static int[] localValue = new int[4096], localType = new int[4096], operandStackValue = new int[4096], operandStackType = new int[4096];
    static int[] frameMethod = new int[32], framePosition = new int[32], frameStack = new int[32];
    static int[] heapValue = new int[8192];
    static int size, readPosition, constantCount, methodCount, className, frameIndex = -1, heapEndPosition = 1, returnType;
    static boolean error;

    static void failureValue(String wordText) {
        if (!error) { User.write("JVM error: "); User.write(wordText); User.writeCharacterValue(10); }
        error = true;
    }
    static boolean clip(int run, int lengthValue) { return run >= 0 && lengthValue >= 0 && run <= size - lengthValue; }
    static int byteValue() {
        if (!clip(readPosition, 1)) { failureValue("truncated class file"); return 0; }
        return file[readPosition++];
    }
    static int shortValue() { return byteValue() << 8 | byteValue(); }
    static int Integer() { return shortValue() << 16 | shortValue(); }
    static void skipBytes(int lengthValue) { if (!clip(readPosition, lengthValue)) failureValue("invalid attribute size"); else readPosition += lengthValue; }
    static boolean checkConstant(int number, int kindValue) {
        if (number <= 0 || number >= constantCount || constantTag[number] != kindValue) { failureValue("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean textRange(int run, int lengthValue, String wordText) {
        if (!clip(run, lengthValue) || lengthValue != wordText.length()) return false;
        for (int number = 0; number < lengthValue; number++) if (file[run + number] != wordText.charAt(number)) return false;
        return true;
    }
    static boolean wordText(int constantValue, String wordText) { return checkConstant(constantValue, 1) && textRange(constantFirstValue[constantValue], constantSecondValue[constantValue], wordText); }
    static boolean matchingWord(int firstOperand, int secondOperand) {
        if (!checkConstant(firstOperand, 1) || !checkConstant(secondOperand, 1) || constantSecondValue[firstOperand] != constantSecondValue[secondOperand]) return false;
        for (int number = 0; number < constantSecondValue[firstOperand]; number++) if (file[constantFirstValue[firstOperand] + number] != file[constantFirstValue[secondOperand] + number]) return false;
        return true;
    }
    static int classNameText(int number) { return checkConstant(number, 7) && checkConstant(constantFirstValue[number], 1) ? constantFirstValue[number] : 0; }
    static int referenceName(int number) { return checkConstant(number, 12) && checkConstant(constantFirstValue[number], 1) ? constantFirstValue[number] : 0; }
    static int referenceType(int number) { return checkConstant(number, 12) && checkConstant(constantSecondValue[number], 1) ? constantSecondValue[number] : 0; }
    static int descriptorType(int ending, boolean emptyType) {
        if (readPosition >= ending) { failureValue("invalid descriptor"); return 0; }
        int value = byteValue();
        if (value == 'V' && emptyType) return 0;
        if (value == 'I' || value == 'B' || value == 'C' || value == 'S' || value == 'Z') return 1;
        if (value == '[') { descriptorType(ending, false); return 2; }
        if (value == 'L') {
            int run = readPosition;
            while (readPosition < ending && file[readPosition] != ';') readPosition++;
            if (readPosition == ending || readPosition == run) failureValue("invalid reference descriptor");
            else readPosition++;
            return 2;
        }
        failureValue("unsupported descriptor type"); return 0;
    }
    static void readDescriptor(int functionValue) {
        int previousItem = readPosition, number = methodType[functionValue];
        if (!checkConstant(number, 1)) return;
        readPosition = constantFirstValue[number]; int ending = readPosition + constantSecondValue[number];
        if (byteValue() != '(') failureValue("invalid method descriptor");
        int itemCount = 0;
        while (!error && readPosition < ending && file[readPosition] != ')') {
            if (itemCount == 16) { failureValue("too many method arguments"); break; }
            methodArgumentType[functionValue * 16 + itemCount++] = descriptorType(ending, false);
        }
        if (readPosition >= ending || byteValue() != ')') failureValue("invalid method descriptor");
        methodReturn[functionValue] = descriptorType(ending, true); methodArgumentCount[functionValue] = itemCount;
        if (readPosition != ending) failureValue("invalid method descriptor");
        readPosition = previousItem;
    }
    static void skipAttribute() {
        int itemCount = shortValue();
        for (int number = 0; number < itemCount && !error; number++) { checkConstant(shortValue(), 1); skipBytes(Integer()); }
    }
    static int commandLength(int value) {
        if (value == 16 || value == 18 || value == 21 || value == 25 || value == 54 || value == 58 || value == 188) return 2;
        if (value == 17 || value == 19 || value == 132 || value >= 153 && value <= 167
            || value >= 178 && value <= 184 || value == 187 || value == 189 || value == 192 || value == 198 || value == 199) return 3;
        if (value >= 0 && value <= 8 || value >= 26 && value <= 29 || value >= 42 && value <= 46 || value == 50
            || value >= 59 && value <= 62 || value >= 75 && value <= 79 || value == 83 || value == 87 || value == 89 || value == 95
            || value == 96 || value == 100 || value == 104 || value == 108 || value == 112 || value == 116
            || value == 120 || value == 122 || value == 124 || value == 126 || value == 128 || value == 130
            || value >= 145 && value <= 147 || value == 172 || value == 176 || value == 177 || value == 190) return 1;
        return 0;
    }
    static void readClass() {
        if (Integer() != 0xcafebabe) failureValue("not a class file");
        int minorRevision = shortValue(), versionValue = shortValue();
        if (versionValue < 45 || versionValue > 52 || minorRevision != 0) failureValue("supported class versions: 45..52, minor 0");
        constantCount = shortValue();
        if (constantCount < 1 || constantCount > 512) { failureValue("constant pool limit (511)"); return; }
        for (int number = 1; number < constantCount && !error; number++) {
            int kindValue = byteValue(); constantTag[number] = kindValue;
            if (kindValue == 1) { constantSecondValue[number] = shortValue(); constantFirstValue[number] = readPosition; skipBytes(constantSecondValue[number]); }
            else if (kindValue == 3) constantFirstValue[number] = Integer();
            else if (kindValue == 7 || kindValue == 8) constantFirstValue[number] = shortValue();
            else if (kindValue == 9 || kindValue == 10 || kindValue == 12) { constantFirstValue[number] = shortValue(); constantSecondValue[number] = shortValue(); }
            else failureValue("unsupported constant type");
        }
        int permissionValue = shortValue();
        if ((permissionValue & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) failureValue("unsupported class flags");
        className = classNameText(shortValue());
        if (!wordText(classNameText(shortValue()), "java/lang/Object")) failureValue("inheritance unsupported");
        if (shortValue() != 0) failureValue("interfaces unsupported");
        if (shortValue() != 0) failureValue("fields unsupported");
        methodCount = shortValue();
        if (methodCount < 1 || methodCount > 32) { failureValue("method count limit (32)"); return; }
        for (int number = 0; number < methodCount && !error; number++) {
            methodAccess[number] = shortValue(); methodNameText[number] = shortValue(); methodType[number] = shortValue();
            checkConstant(methodNameText[number], 1); readDescriptor(number);
            if ((methodAccess[number] & (0x100 | 0x400 | 0x20)) != 0) failureValue("native, abstract and synchronized methods unsupported");
            if ((methodAccess[number] & 8) == 0 && !wordText(methodNameText[number], "<init>")) failureValue("instance methods unsupported");
            if (wordText(methodNameText[number], "<clinit>")) failureValue("class initializers unsupported");
            for (int frontValue = 0; frontValue < number; frontValue++) if (matchingWord(methodNameText[frontValue], methodNameText[number]) && matchingWord(methodType[frontValue], methodType[number])) failureValue("duplicate method");
            int itemCount = shortValue();
            for (int attributeValue = 0; attributeValue < itemCount && !error; attributeValue++) {
                int name = shortValue(), lengthValue = Integer(), run = readPosition;
                if (!clip(run, lengthValue)) { failureValue("truncated method attribute"); break; }
                if (wordText(name, "Code")) {
                    if (methodStart[number] != 0) failureValue("duplicate Code attribute");
                    methodStack[number] = shortValue(); methodLocals[number] = shortValue(); int codeLength = Integer();
                    if (methodStack[number] > 128 || methodLocals[number] > 128 || methodLocals[number] < methodArgumentCount[number]
                        || codeLength < 1 || codeLength > 8192) failureValue("method memory limits exceeded");
                    methodStart[number] = readPosition; skipBytes(codeLength); methodEnd[number] = readPosition;
                    if (shortValue() != 0) failureValue("exception handlers unsupported");
                    skipAttribute();
                    if (readPosition != run + lengthValue) failureValue("Code attribute size mismatch");
                } else skipBytes(lengthValue);
            }
            if (methodStart[number] == 0) failureValue("missing Code attribute");
            int slotEntry = methodStart[number];
            while (slotEntry < methodEnd[number] && !error) {
                int lengthValue = commandLength(file[slotEntry]);
                if (lengthValue == 0 || lengthValue > methodEnd[number] - slotEntry) { failureValue("unsupported or truncated bytecode"); break; }
                boundaryValue[slotEntry] = number + 1; slotEntry += lengthValue;
            }
            // Reject invalid branch targets even in paths that are never executed.
            slotEntry = methodStart[number];
            while (slotEntry < methodEnd[number] && !error) {
                int value = file[slotEntry];
                if (value >= 153 && value <= 167 || value == 198 || value == 199) {
                    int destinationValue = slotEntry + (short)(file[slotEntry + 1] << 8 | file[slotEntry + 2]);
                    if (destinationValue < methodStart[number] || destinationValue >= methodEnd[number] || boundaryValue[destinationValue] != number + 1) failureValue("invalid branch target");
                }
                slotEntry += commandLength(value);
            }
        }
        if (!error) skipAttribute();
        if (readPosition != size) failureValue("extra class file data");
    }
    static int allocateStorage(int kindValue, int lengthValue) {
        if (lengthValue < 0 || lengthValue > heapValue.length - heapEndPosition - 2) { failureValue("object heap exhausted or negative array size"); return 0; }
        int reference = heapEndPosition; heapEndPosition += lengthValue + 2; heapValue[reference] = kindValue; heapValue[reference + 1] = lengthValue;
        return reference;
    }
    static boolean objectValue(int reference, int kindValue) {
        if (reference < 1 || reference >= heapEndPosition - 1 || heapValue[reference] != kindValue) { failureValue("null or invalid object reference"); return false; }
        return true;
    }
    static int constantText(int index) {
        if (!checkConstant(index, 1)) return 0;
        if (stringReference[index] != 0) return stringReference[index];
        int reference = allocateStorage(1, constantSecondValue[index]); if (error) return 0;
        int ending = constantFirstValue[index] + constantSecondValue[index], number = constantFirstValue[index], lengthValue = 0;
        while (number < ending && !error) {
            int value = file[number++];
            if (value == 0) failureValue("invalid modified UTF-8");
            else if (value >= 192 && value <= 223 && number < ending) {
                int nextItem = file[number++];
                if ((nextItem & 192) != 128) failureValue("invalid modified UTF-8");
                value = (value & 31) << 6 | nextItem & 63;
                if (value != 0 && value < 128) failureValue("overlong modified UTF-8");
            } else if (value >= 224 && value <= 239 && number + 1 < ending) {
                int firstOperand = file[number++], secondOperand = file[number++];
                if ((firstOperand & 192) != 128 || (secondOperand & 192) != 128) failureValue("invalid modified UTF-8");
                value = (value & 15) << 12 | (firstOperand & 63) << 6 | secondOperand & 63;
                if (value < 2048) failureValue("overlong modified UTF-8");
            } else if (value >= 128) failureValue("invalid modified UTF-8");
            heapValue[reference + 2 + lengthValue++] = value;
        }
        heapValue[reference + 1] = lengthValue; stringReference[index] = reference; return reference;
    }
    static int hostCharacter(String value) {
        int reference = allocateStorage(1, value.length()); if (error) return 0;
        for (int number = 0; number < value.length(); number++) heapValue[reference + 2 + number] = value.charAt(number);
        return reference;
    }
    static void writeText(int reference) {
        if (reference == 0) { User.write("null"); return; }
        if (!objectValue(reference, 1)) return;
        for (int number = 0; number < heapValue[reference + 1]; number++) User.writeCharacterValue(heapValue[reference + 2 + number]);
    }
    static int digitCharacter(int value) {
        int reference = allocateStorage(1, 11); if (error) return 0;
        int lengthValue = 0;
        if (value < 0) heapValue[reference + 2 + lengthValue++] = '-'; else value = -value;
        int positionIndex = 1000000000; boolean run = false;
        while (positionIndex != 0) {
            int number = -(value / positionIndex);
            if (number != 0 || run || positionIndex == 1) { heapValue[reference + 2 + lengthValue++] = '0' + number; run = true; }
            value %= positionIndex; positionIndex /= 10;
        }
        heapValue[reference + 1] = lengthValue; return reference;
    }
    static int decodeInteger(int reference) {
        if (!objectValue(reference, 1)) return 0;
        int lengthValue = heapValue[reference + 1], number = 0, value = 0; boolean negativeValue = false;
        if (lengthValue > 0 && (heapValue[reference + 2] == '-' || heapValue[reference + 2] == '+')) { negativeValue = heapValue[reference + 2] == '-'; number++; }
        if (number == lengthValue) failureValue("NumberFormatException");
        for (; number < lengthValue && !error; number++) {
            int digitValue = heapValue[reference + 2 + number] - '0';
            if (digitValue < 0 || digitValue > 9 || value < -214748364 || value == -214748364 && digitValue > (negativeValue ? 8 : 7)) failureValue("NumberFormatException");
            value = value * 10 - digitValue;
        }
        return negativeValue ? value : -value;
    }
    static void putValue(int value, int typeValue) {
        if (error) return;
        if (frameIndex < 0 || frameStack[frameIndex] >= methodStack[frameMethod[frameIndex]]) { failureValue("operand stack overflow"); return; }
        int slotEntry = frameIndex * 128 + frameStack[frameIndex]++; operandStackValue[slotEntry] = value; operandStackType[slotEntry] = typeValue;
    }
    static int subtractValues(int typeValue) {
        if (error) return 0;
        if (frameIndex < 0 || frameStack[frameIndex] < 1) { failureValue("operand stack underflow"); return 0; }
        int slotEntry = frameIndex * 128 + --frameStack[frameIndex]; returnType = operandStackType[slotEntry];
        if (typeValue != 0 && returnType != typeValue) failureValue("operand type mismatch");
        return operandStackValue[slotEntry];
    }
    static void readLocal(int index, int typeValue) {
        if (index >= methodLocals[frameMethod[frameIndex]] || index < 0 || localType[frameIndex * 128 + index] != typeValue) { failureValue("invalid or uninitialized local"); return; }
        putValue(localValue[frameIndex * 128 + index], typeValue);
    }
    static void writeLocal(int index, int typeValue) {
        if (index >= methodLocals[frameMethod[frameIndex]] || index < 0) { failureValue("local index out of range"); return; }
        int value = subtractValues(typeValue); localValue[frameIndex * 128 + index] = value; localType[frameIndex * 128 + index] = typeValue;
    }
    static int readOpcodeByte() {
        int position = framePosition[frameIndex];
        if (position < methodStart[frameMethod[frameIndex]] || position >= methodEnd[frameMethod[frameIndex]]) { failureValue("instruction pointer out of range"); return 0; }
        framePosition[frameIndex]++; return file[position];
    }
    static int readOpcodeShort() { return readOpcodeByte() << 8 | readOpcodeByte(); }
    static void moveValue(int position) {
        int functionValue = frameMethod[frameIndex];
        if (position < methodStart[functionValue] || position >= methodEnd[functionValue] || boundaryValue[position] != functionValue + 1) failureValue("invalid branch target");
        else framePosition[frameIndex] = position;
    }
    static void invoke(int functionValue) {
        if (frameIndex == 31) { failureValue("call stack limit (32)"); return; }
        int nextItem = frameIndex + 1;
        for (int number = 0; number < 128; number++) localType[nextItem * 128 + number] = 0;
        for (int number = methodArgumentCount[functionValue] - 1; number >= 0; number--) {
            localValue[nextItem * 128 + number] = subtractValues(methodArgumentType[functionValue * 16 + number]); localType[nextItem * 128 + number] = methodArgumentType[functionValue * 16 + number];
        }
        frameIndex = nextItem; frameMethod[frameIndex] = functionValue; framePosition[frameIndex] = methodStart[functionValue]; frameStack[frameIndex] = 0;
    }
    static void returnResult(int typeValue) {
        if (typeValue != methodReturn[frameMethod[frameIndex]]) { failureValue("return type mismatch"); return; }
        int value = typeValue == 0 ? 0 : subtractValues(typeValue);
        frameIndex--; if (frameIndex >= 0 && typeValue != 0) putValue(value, typeValue);
    }
    static int[] streamFileName = new int[64];
    static void fileStreamCall(int ownerValue, int name, int formatValue, int command) {
        boolean Output = wordText(ownerValue, "java/io/FileOutputStream");
        int kindValue = Output ? 6 : 5;
        if (command == 183 && wordText(name, "<init>")) {
            boolean continuationValue = false;
            if (Output && wordText(formatValue, "(Ljava/lang/String;Z)V")) continuationValue = subtractValues(1) != 0;
            else if (!wordText(formatValue, "(Ljava/lang/String;)V")) { failureValue("unsupported file stream constructor"); return; }
            int fileEntryName = subtractValues(2), streamValue = subtractValues(2);
            if (!objectValue(fileEntryName, 1) || !objectValue(streamValue, kindValue) || error) return;
            if (heapValue[streamValue + 3] != 0) { failureValue("file stream already initialized"); return; }
            int lengthValue = heapValue[fileEntryName + 1];
            if (lengthValue < 1 || lengthValue > 63) { failureValue("invalid file name length"); return; }
            for (int slotEntry = 0; slotEntry < lengthValue; slotEntry++) {
                int value = heapValue[fileEntryName + 2 + slotEntry];
                if (value < 1 || value > 127) { failureValue("file stream paths currently require ASCII"); return; }
                streamFileName[slotEntry] = value;
            }
            streamFileName[lengthValue] = 0;
            int descriptorEntry = User.openFileDescriptor(streamFileName, Output ? (continuationValue ? 1089 : 577) : 0);
            if (descriptorEntry < 0) { failureValue("FileNotFoundException: file open failed"); return; }
            heapValue[streamValue + 2] = descriptorEntry; heapValue[streamValue + 3] = 1;
            return;
        }
        if (command != 182) { failureValue("invalid file stream invocation"); return; }
        int action = -1, value = 0;
        if (wordText(name, "close") && wordText(formatValue, "()V")) action = 0;
        if (!Output && wordText(name, "read") && wordText(formatValue, "()I")) action = 1;
        if (Output && wordText(name, "write") && wordText(formatValue, "(I)V")) { action = 2; value = subtractValues(1); }
        if (action < 0) { failureValue("unsupported file stream method"); return; }
        int streamValue = subtractValues(2);
        if (!objectValue(streamValue, kindValue) || error) return;
        if (heapValue[streamValue + 3] == 0) { failureValue("uninitialized file stream"); return; }
        int descriptorEntry = heapValue[streamValue + 2];
        if (action == 0) {
            if (descriptorEntry >= 0 && User.closeFileDescriptor(descriptorEntry) < 0) failureValue("IOException: close failed");
            heapValue[streamValue + 2] = -1; return;
        }
        if (descriptorEntry < 0) { failureValue("IOException: stream closed"); return; }
        if (action == 1) {
            int result = User.readOneFileByte(descriptorEntry);
            if (result < -1) failureValue("IOException: read failed"); else putValue(result, 1);
        } else if (User.writeOneFileByte(descriptorEntry, value) != 1) failureValue("IOException: write failed");
    }
    static void callMethod(int index, int command) {
        if (!checkConstant(index, 10)) return;
        int ownerValue = classNameText(constantFirstValue[index]), name = referenceName(constantSecondValue[index]), formatValue = referenceType(constantSecondValue[index]);
        if (error) return;
        if (matchingWord(ownerValue, className)) {
            if (command != 184) { failureValue("only static user methods are supported"); return; }
            for (int number = 0; number < methodCount; number++) if (matchingWord(name, methodNameText[number]) && matchingWord(formatValue, methodType[number])) {
                if ((methodAccess[number] & 8) == 0) failureValue("method is not static"); else invoke(number);
                return;
            }
            failureValue("NoSuchMethodError"); return;
        }
        if (wordText(ownerValue, "java/io/FileInputStream") || wordText(ownerValue, "java/io/FileOutputStream")) {
            fileStreamCall(ownerValue, name, formatValue, command); return;
        }
        if (command == 184 && wordText(ownerValue, "java/lang/Integer") && wordText(name, "parseInt") && wordText(formatValue, "(Ljava/lang/String;)I")) {
            putValue(decodeInteger(subtractValues(2)), 1); return;
        }
        if (command == 182 && wordText(ownerValue, "java/io/PrintStream") && (wordText(name, "println") || wordText(name, "print"))) {
            int typeValue = 0, value = 0;
            if (wordText(formatValue, "(I)V")) { typeValue = 1; value = subtractValues(1); }
            else if (wordText(formatValue, "(Z)V")) { typeValue = 2; value = subtractValues(1); }
            else if (wordText(formatValue, "(C)V")) { typeValue = 3; value = subtractValues(1); }
            else if (wordText(formatValue, "(Ljava/lang/String;)V")) { typeValue = 4; value = subtractValues(2); }
            else if (!wordText(formatValue, "()V") || !wordText(name, "println")) failureValue("unsupported print descriptor");
            if (subtractValues(2) != -1) failureValue("invalid PrintStream receiver");
            if (error) return;
            if (typeValue == 1) JavaTools.writeNumber(value);
            if (typeValue == 2) User.write(value == 0 ? "false" : "true");
            if (typeValue == 3) User.writeCharacterValue(value & 65535);
            if (typeValue == 4) writeText(value);
            if (wordText(name, "println")) User.writeCharacterValue(10);
            return;
        }
        if (command == 182 && wordText(ownerValue, "java/lang/String")) {
            if (wordText(name, "length") && wordText(formatValue, "()I")) {
                int reference = subtractValues(2); if (objectValue(reference, 1)) putValue(heapValue[reference + 1], 1); return;
            }
            if (wordText(name, "charAt") && wordText(formatValue, "(I)C")) {
                int subscriptValue = subtractValues(1), reference = subtractValues(2);
                if (objectValue(reference, 1)) {
                    if (subscriptValue < 0 || subscriptValue >= heapValue[reference + 1]) failureValue("StringIndexOutOfBoundsException"); else putValue(heapValue[reference + 2 + subscriptValue], 1);
                }
                return;
            }
        }
        if (wordText(ownerValue, "java/lang/StringBuilder")) {
            if (command == 183 && wordText(name, "<init>") && wordText(formatValue, "()V")) { objectValue(subtractValues(2), 4); return; }
            if (command == 182 && wordText(name, "toString") && wordText(formatValue, "()Ljava/lang/String;")) {
                int reference = subtractValues(2); if (objectValue(reference, 4)) putValue(heapValue[reference + 2] == 0 ? hostCharacter("") : heapValue[reference + 2], 2); return;
            }
            if (command == 182 && wordText(name, "append")) {
                int text = 0;
                if (wordText(formatValue, "(I)Ljava/lang/StringBuilder;")) text = digitCharacter(subtractValues(1));
                else if (wordText(formatValue, "(Z)Ljava/lang/StringBuilder;")) text = hostCharacter(subtractValues(1) == 0 ? "false" : "true");
                else if (wordText(formatValue, "(C)Ljava/lang/StringBuilder;")) {
                    int value = subtractValues(1); text = allocateStorage(1, 1); if (!error) heapValue[text + 2] = value & 65535;
                }
                else if (wordText(formatValue, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { text = subtractValues(2); if (text == 0) text = hostCharacter("null"); }
                else { failureValue("unsupported StringBuilder append"); return; }
                int reference = subtractValues(2); if (!objectValue(reference, 4) || !objectValue(text, 1)) return;
                int frontValue = heapValue[reference + 2], frontValueLength = frontValue == 0 ? 0 : heapValue[frontValue + 1], backValueLength = heapValue[text + 1];
                int newText = allocateStorage(1, frontValueLength + backValueLength); if (error) return;
                for (int number = 0; number < frontValueLength; number++) heapValue[newText + 2 + number] = heapValue[frontValue + 2 + number];
                for (int number = 0; number < backValueLength; number++) heapValue[newText + 2 + frontValueLength + number] = heapValue[text + 2 + number];
                heapValue[reference + 2] = newText; putValue(reference, 2); return;
            }
        }
        failureValue("unsupported library method");
    }
    static int arraySlot(int reference, int subscriptValue, int typeValue) {
        if (!objectValue(reference, typeValue)) return 0;
        if (subscriptValue < 0 || subscriptValue >= heapValue[reference + 1]) { failureValue("ArrayIndexOutOfBoundsException"); return 0; }
        return reference + 2 + subscriptValue;
    }
    static void executeCommand() {
        int remainderData = 500000;
        while (frameIndex >= 0 && !error) {
            if (--remainderData == 0) { failureValue("instruction limit (500000)"); break; }
            int run = framePosition[frameIndex], value = readOpcodeByte();
            if (error) break;
            if (value == 0) continue;
            if (value == 1) { putValue(0, 2); continue; }
            if (value >= 2 && value <= 8) { putValue(value - 3, 1); continue; }
            if (value == 16) { putValue((byte)readOpcodeByte(), 1); continue; }
            if (value == 17) { putValue((short)readOpcodeShort(), 1); continue; }
            if (value == 18 || value == 19) {
                int number = value == 18 ? readOpcodeByte() : readOpcodeShort();
                if (number <= 0 || number >= constantCount) failureValue("invalid ldc constant");
                else if (constantTag[number] == 3) putValue(constantFirstValue[number], 1);
                else if (constantTag[number] == 8) putValue(constantText(constantFirstValue[number]), 2);
                else failureValue("unsupported ldc constant");
                continue;
            }
            if (value == 21 || value == 25) { readLocal(readOpcodeByte(), value == 21 ? 1 : 2); continue; }
            if (value >= 26 && value <= 29) { readLocal(value - 26, 1); continue; }
            if (value >= 42 && value <= 45) { readLocal(value - 42, 2); continue; }
            if (value == 54 || value == 58) { writeLocal(readOpcodeByte(), value == 54 ? 1 : 2); continue; }
            if (value >= 59 && value <= 62) { writeLocal(value - 59, 1); continue; }
            if (value >= 75 && value <= 78) { writeLocal(value - 75, 2); continue; }
            if (value == 46 || value == 50) {
                int subscriptValue = subtractValues(1), reference = subtractValues(2), slotEntry = arraySlot(reference, subscriptValue, value == 46 ? 2 : 3);
                if (!error) putValue(heapValue[slotEntry], value == 46 ? 1 : 2); continue;
            }
            if (value == 79 || value == 83) {
                int itemElement = subtractValues(value == 79 ? 1 : 2), subscriptValue = subtractValues(1), reference = subtractValues(2), slotEntry = arraySlot(reference, subscriptValue, value == 79 ? 2 : 3);
                if (value == 83 && itemElement != 0) objectValue(itemElement, 1);
                if (!error) heapValue[slotEntry] = itemElement; continue;
            }
            if (value == 87) { subtractValues(0); continue; }
            if (value == 89) { int firstOperand = subtractValues(0), typeValue = returnType; putValue(firstOperand, typeValue); putValue(firstOperand, typeValue); continue; }
            if (value == 95) { int firstOperand = subtractValues(0), firstOperandType = returnType, secondOperand = subtractValues(0), secondOperandType = returnType; putValue(firstOperand, firstOperandType); putValue(secondOperand, secondOperandType); continue; }
            if (value == 96 || value == 100 || value == 104 || value == 108 || value == 112 || value == 120
                || value == 122 || value == 124 || value == 126 || value == 128 || value == 130) {
                int secondOperand = subtractValues(1), firstOperand = subtractValues(1), result = 0;
                if ((value == 108 || value == 112) && secondOperand == 0) { failureValue("ArithmeticException: / by zero"); continue; }
                if (value == 96) result = firstOperand + secondOperand;
                if (value == 100) result = firstOperand - secondOperand;
                if (value == 104) result = firstOperand * secondOperand;
                if (value == 108) result = firstOperand / secondOperand;
                if (value == 112) result = firstOperand % secondOperand;
                if (value == 120) result = firstOperand << secondOperand;
                if (value == 122) result = firstOperand >> secondOperand;
                if (value == 124) result = firstOperand >>> secondOperand;
                if (value == 126) result = firstOperand & secondOperand;
                if (value == 128) result = firstOperand | secondOperand;
                if (value == 130) result = firstOperand ^ secondOperand;
                putValue(result, 1); continue;
            }
            if (value == 116) { putValue(-subtractValues(1), 1); continue; }
            if (value == 132) {
                int localScope = readOpcodeByte(), incrementStep = (byte)readOpcodeByte(); readLocal(localScope, 1); putValue(subtractValues(1) + incrementStep, 1); writeLocal(localScope, 1); continue;
            }
            if (value >= 145 && value <= 147) {
                int number = subtractValues(1); putValue(value == 145 ? (byte)number : value == 146 ? (char)number : (short)number, 1); continue;
            }
            if (value >= 153 && value <= 167 || value == 198 || value == 199) {
                int destinationValue = run + (short)readOpcodeShort(); boolean shouldProceed = value == 167;
                if (value >= 153 && value <= 158) {
                    int number = subtractValues(1); shouldProceed = value == 153 ? number == 0 : value == 154 ? number != 0 : value == 155 ? number < 0 : value == 156 ? number >= 0 : value == 157 ? number > 0 : number <= 0;
                } else if (value >= 159 && value <= 166) {
                    int secondOperand = subtractValues(value >= 165 ? 2 : 1), firstOperand = subtractValues(value >= 165 ? 2 : 1);
                    shouldProceed = value == 159 || value == 165 ? firstOperand == secondOperand : value == 160 || value == 166 ? firstOperand != secondOperand : value == 161 ? firstOperand < secondOperand : value == 162 ? firstOperand >= secondOperand : value == 163 ? firstOperand > secondOperand : firstOperand <= secondOperand;
                } else if (value == 198 || value == 199) { int number = subtractValues(2); shouldProceed = value == 198 ? number == 0 : number != 0; }
                if (shouldProceed) moveValue(destinationValue); continue;
            }
            if (value == 172 || value == 176 || value == 177) { returnResult(value == 172 ? 1 : value == 176 ? 2 : 0); continue; }
            if (value == 178) {
                int number = readOpcodeShort(); if (!checkConstant(number, 9)) continue;
                if (!wordText(classNameText(constantFirstValue[number]), "java/lang/System") || !wordText(referenceName(constantSecondValue[number]), "out")
                    || !wordText(referenceType(constantSecondValue[number]), "Ljava/io/PrintStream;")) failureValue("unsupported static field");
                else putValue(-1, 2); continue;
            }
            if (value == 182 || value == 183 || value == 184) { callMethod(readOpcodeShort(), value); continue; }
            if (value == 187) {
                int name = classNameText(readOpcodeShort());
                if (wordText(name, "java/lang/StringBuilder")) putValue(allocateStorage(4, 1), 2);
                else if (wordText(name, "java/io/FileInputStream") || wordText(name, "java/io/FileOutputStream")) {
                    int reference = allocateStorage(wordText(name, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!error) { heapValue[reference + 2] = -1; putValue(reference, 2); }
                } else failureValue("unsupported object construction");
                continue;
            }
            if (value == 188 || value == 189) {
                if (value == 188) { if (readOpcodeByte() != 10) failureValue("only int[] newarray is supported"); }
                else if (!wordText(classNameText(readOpcodeShort()), "java/lang/String")) failureValue("only String[] anewarray is supported");
                int lengthValue = subtractValues(1); putValue(allocateStorage(value == 188 ? 2 : 3, lengthValue), 2); continue;
            }
            if (value == 190) {
                int reference = subtractValues(2);
                if (reference < 1 || reference >= heapEndPosition - 1 || (heapValue[reference] != 2 && heapValue[reference] != 3)) failureValue("null or invalid array");
                else putValue(heapValue[reference + 1], 1); continue;
            }
            if (value == 192) {
                int name = classNameText(readOpcodeShort()), reference = subtractValues(2);
                if (!wordText(name, "java/lang/String")) failureValue("unsupported checkcast");
                else if (reference != 0) objectValue(reference, 1);
                putValue(reference, 2); continue;
            }
            failureValue("unsupported bytecode");
        }
    }
    public static int run() {
        if (User.argumentsCount() == 1 && JavaTools.equalText(User.arguments(0), "-version")) {
            User.write("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (User.argumentsCount() < 1) { User.write("Usage: java CLASS [ARGS]\n"); return 2; }
        int lengthValue = JavaTools.name(fileNameText, User.arguments(0));
        if (lengthValue < 1 || lengthValue > 57) { User.write("java: invalid class name\n"); return 2; }
        fileNameText[lengthValue] = '.'; fileNameText[lengthValue + 1] = 'c'; fileNameText[lengthValue + 2] = 'l'; fileNameText[lengthValue + 3] = 'a'; fileNameText[lengthValue + 4] = 's'; fileNameText[lengthValue + 5] = 's';
        size = User.readFile(fileNameText, file);
        if (size < 0) { User.write("java: cannot read class: "); JavaTools.writeNumber(size); User.writeCharacterValue(10); return 1; }
        readClass(); if (error) return 1;
        int characterName = constantText(className);
        if (!error && heapValue[characterName + 1] != lengthValue) failureValue("class name does not match file");
        for (int number = 0; number < lengthValue && !error; number++) if (heapValue[characterName + 2 + number] != fileNameText[number]) failureValue("class name does not match file");
        int entryPointValue = -1;
        for (int number = 0; number < methodCount; number++) if (wordText(methodNameText[number], "main") && wordText(methodType[number], "([Ljava/lang/String;)V") && (methodAccess[number] & 9) == 9) entryPointValue = number;
        if (entryPointValue < 0) failureValue("public static void main(String[] args) required");
        if (error) return 1;
        int arguments = allocateStorage(3, User.argumentsCount() - 1);
        for (int number = 1; number < User.argumentsCount() && !error; number++) heapValue[arguments + 1 + number] = hostCharacter(User.arguments(number));
        frameIndex = 0; frameMethod[0] = entryPointValue; framePosition[0] = methodStart[entryPointValue]; localValue[0] = arguments; localType[0] = 2;
        executeCommand(); return error ? 1 : 0;
    }
}
