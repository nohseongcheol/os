// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Restricted JVM running at ARM64 EL0. Checks file, stack, reference and branch bounds during execution. */
public final class JavaMachine {
    static int[] file = new int[16 * 16384], temporaryFile = new int[16384], fileNameText = new int[512];
    static int[] constantTag = new int[8192], constantFirstValue = new int[8192], constantSecondValue = new int[8192], stringReference = new int[8192];
    static int[] methodNameText = new int[512], methodType = new int[512], methodAccess = new int[512], methodOwner = new int[512];
    static int[] methodStart = new int[512], methodEnd = new int[512], methodStack = new int[512], methodLocals = new int[512];
    static int[] methodArgumentCount = new int[512], methodArgumentType = new int[8192], methodReturn = new int[512];
    static int[] boundaryValue = new int[16 * 16384];
    static int[] localValue = new int[16384], localType = new int[16384], operandStackValue = new int[16384], operandStackType = new int[16384];
    static int[] frameMethod = new int[128], framePosition = new int[128], frameStack = new int[128], frameInstruction = new int[128], initializeFrame = new int[128];
    static int[] classDefinitionName = new int[16], classDefinitionSize = new int[16], classDefinitionParent = new int[16], classDefinitionState = new int[16], classSlotCount = new int[16], initializeClassDefinition = new int[16];
    static int[] classInterface = new int[16 * 16], classInterfaceCount = new int[16];
    static int[] slotName = new int[512], slotType = new int[512], slotOwner = new int[512], slotPermissions = new int[512], slotPosition = new int[512], slotData = new int[512];
    static int[] catchStart = new int[1024], catchEnd = new int[1024], catchPosition = new int[1024], catchClass = new int[1024], catchMethod = new int[1024];
    static int[] heapValue = new int[32768], heapWidth = new int[32768], heapMark = new int[32768], heapReference = new int[32768], waitForDisplay = new int[32768];
    static int[] temporaryReference = new int[256], arrayElement = new int[32768], storeInteger = new int[256];
    static int size, readPosition, methodCount, className, frameIndex = -1, heapEndPosition = 1, returnType;
    static int classDefinitionCount, slotCount, catchCount, currentParsedClass, thrownObject, temporaryCount, displayCount, collectionCount;
    static int currentThread, threadCount = 1, entryClassDefinition;
    static int[] threadFrame = new int[4], threadState = new int[4], threadObject = new int[4], threadTarget = new int[4], waitForThread = new int[4];
    static boolean error, changeRequest;
    static int[] lockOwner = new int[32768], lockDepth = new int[32768], frameLock = new int[128], classLock = new int[16], classThread = new int[16];

    static void failureValue(String wordText) {
        if (error) return;
        int categoryCode = 0;
        if (JavaTools.equalText(wordText, "ArithmeticException: / by zero")) categoryCode = 4;
        if (JavaTools.equalText(wordText, "NullPointerException") || JavaTools.equalText(wordText, "null or invalid array")) categoryCode = 5;
        if (JavaTools.equalText(wordText, "ArrayIndexOutOfBoundsException")) categoryCode = 7;
        if (JavaTools.equalText(wordText, "StringIndexOutOfBoundsException")) categoryCode = 8;
        if (JavaTools.equalText(wordText, "NumberFormatException")) categoryCode = 10;
        if (JavaTools.equalText(wordText, "FileNotFoundException: file open failed")) categoryCode = 12;
        if (JavaTools.equalText(wordText, "IOException: stream closed") || JavaTools.equalText(wordText, "IOException: read failed") || JavaTools.equalText(wordText, "IOException: write failed")) categoryCode = 11;
        if (JavaTools.equalText(wordText, "ClassCastException")) categoryCode = 14;
        if (JavaTools.equalText(wordText, "NegativeArraySizeException")) categoryCode = 15;
        if (categoryCode != 0 && frameIndex >= 0) { throwException(categoryCode, wordText); return; }
        User.write("JVM error: "); User.write(wordText); User.writeCharacterValue(10); error = true;
    }
    static boolean clip(int run, int lengthValue) {
        if (run < 0 || run >= file.length || lengthValue < 0) return false;
        int classDefinition = run / 16384;
        return run % 16384 <= classDefinitionSize[classDefinition] && lengthValue <= classDefinitionSize[classDefinition] - run % 16384;
    }
    static int byteValue() {
        if (!clip(readPosition, 1)) { failureValue("truncated class file"); return 0; }
        return file[readPosition++];
    }
    static int shortValue() { return byteValue() << 8 | byteValue(); }
    static int Integer() { return shortValue() << 16 | shortValue(); }
    static void skipBytes(int lengthValue) { if (!clip(readPosition, lengthValue)) failureValue("invalid attribute size"); else readPosition += lengthValue; }
    static boolean checkConstant(int number, int kindValue) {
        if (number <= 0 || number >= constantTag.length || constantTag[number] != kindValue) { failureValue("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean textRange(int run, int lengthValue, String wordText) {
        if (!clip(run, lengthValue)) return false;
        int readCursor = run, ending = run + lengthValue;
        for (int loopIndex = 0; loopIndex < wordText.length(); loopIndex++) {
            int characterCode = wordText.charAt(loopIndex);
            if (characterCode > 0 && characterCode < 128) { if (readCursor >= ending || file[readCursor++] != characterCode) return false; }
            else if (characterCode < 2048) {
                if (readCursor + 2 > ending || file[readCursor++] != (192 | (characterCode >> 6)) || file[readCursor++] != (128 | (characterCode & 63))) return false;
            } else if (readCursor + 3 > ending || file[readCursor++] != (224 | (characterCode >> 12)) || file[readCursor++] != (128 | ((characterCode >> 6) & 63)) || file[readCursor++] != (128 | (characterCode & 63))) return false;
        }
        return readCursor == ending;
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
    static int readConstantIndex() { int value = shortValue(); return value == 0 ? 0 : currentParsedClass * 512 + value; }
    static int readOpcodeConstant() { return methodOwner[frameMethod[frameIndex]] * 512 + readOpcodeShort(); }
    static void skipAttribute() {
        int itemCount = shortValue();
        for (int number = 0; number < itemCount && !error; number++) { checkConstant(readConstantIndex(), 1); skipBytes(Integer()); }
    }
    static int commandLength(int value) {
        if (value == 16 || value == 18 || value == 21 || value == 25 || value == 54 || value == 58 || value == 188) return 2;
        if (value == 17 || value == 19 || value == 132 || value >= 153 && value <= 167
            || value >= 178 && value <= 184 || value == 187 || value == 189 || value == 192 || value == 193 || value == 198 || value == 199) return 3;
        if (value == 185 || value == 200) return 5;
        if (value >= 0 && value <= 8 || value >= 26 && value <= 29 || value >= 42 && value <= 46 || value >= 50 && value <= 53
            || value >= 59 && value <= 62 || value >= 75 && value <= 79 || value >= 83 && value <= 95
            || value == 96 || value == 100 || value == 104 || value == 108 || value == 112 || value == 116
            || value == 120 || value == 122 || value == 124 || value == 126 || value == 128 || value == 130
            || value >= 145 && value <= 147 || value == 172 || value == 176 || value == 177 || value == 190 || value == 191
            || value == 194 || value == 195) return 1;
        return 0;
    }
    static int positionInteger(int readCursor) {
        if (!clip(readCursor, 4)) { failureValue("truncated bytecode operand"); return 0; }
        return file[readCursor] << 24 | file[readCursor + 1] << 16 | file[readCursor + 2] << 8 | file[readCursor + 3];
    }
    static int readLength(int readCursor, int run, int ending) {
        int value = file[readCursor], lengthValue = commandLength(value);
        if (value == 170 || value == 171) {
            int basePosition = readCursor + 1;
            while ((basePosition - run) % 4 != 0) basePosition++;
            if (ending - basePosition < (value == 170 ? 12 : 8)) return 0;
            int entryCount = value == 170 ? positionInteger(basePosition + 8) - positionInteger(basePosition + 4) + 1 : positionInteger(basePosition + 4);
            if (entryCount < 0 || entryCount > 2048) return 0;
            lengthValue = basePosition - readCursor + (value == 170 ? 12 + 4 * entryCount : 8 + 8 * entryCount);
        }
        if (value == 196 && readCursor + 1 < ending) {
            int wordData = file[readCursor + 1]; lengthValue = wordData == 132 ? 6 : (wordData == 21 || wordData == 25 || wordData == 54 || wordData == 58) ? 4 : 0;
        }
        return lengthValue > 0 && lengthValue <= ending - readCursor ? lengthValue : 0;
    }
    static void checkDestinationValue(int destinationValue, int functionValue) {
        if (destinationValue < methodStart[functionValue] || destinationValue >= methodEnd[functionValue] || boundaryValue[destinationValue] != functionValue + 1) failureValue("invalid branch target");
    }
    static void readClass(int classDefinition) {
        currentParsedClass = classDefinition; readPosition = classDefinition * 16384; size = readPosition + classDefinitionSize[classDefinition];
        if (Integer() != 0xcafebabe) { failureValue("not a class file"); return; }
        int minorRevision = shortValue(), versionValue = shortValue();
        if (versionValue < 45 || versionValue > 52 || minorRevision != 0) { failureValue("supported class versions: 45..52, minor 0"); return; }
        int constantCount = shortValue(), basePosition = classDefinition * 512;
        if (constantCount < 1 || constantCount > 512) { failureValue("constant pool limit (511)"); return; }
        for (int entryCount = 1; entryCount < constantCount && !error; entryCount++) {
            int number = basePosition + entryCount, kindValue = byteValue(); constantTag[number] = kindValue;
            if (kindValue == 1) { constantSecondValue[number] = shortValue(); constantFirstValue[number] = readPosition; skipBytes(constantSecondValue[number]); }
            else if (kindValue == 3) constantFirstValue[number] = Integer();
            else if (kindValue == 7 || kindValue == 8) constantFirstValue[number] = readConstantIndex();
            else if (kindValue == 9 || kindValue == 10 || kindValue == 11 || kindValue == 12) { constantFirstValue[number] = readConstantIndex(); constantSecondValue[number] = readConstantIndex(); }
            else failureValue("unsupported constant type");
        }
        int permissionValue = shortValue();
        if ((permissionValue & (0x2000 | 0x4000)) != 0) failureValue("annotation/enum class unsupported");
        classDefinitionName[classDefinition] = classNameText(readConstantIndex());
        classDefinitionParent[classDefinition] = classNameText(readConstantIndex());
        int interfaceCount = shortValue(); if (interfaceCount > 16) { failureValue("interface count limit"); return; }
        classInterfaceCount[classDefinition] = interfaceCount;
        for (int loopIndex = 0; loopIndex < interfaceCount; loopIndex++) classInterface[classDefinition * 16 + loopIndex] = classNameText(readConstantIndex());
        int fieldCount = shortValue();
        if (fieldCount > 512 - slotCount) { failureValue("field count limit (512)"); return; }
        for (int loopIndex = 0; loopIndex < fieldCount && !error; loopIndex++) {
            int fileIndex = slotCount++; slotOwner[fileIndex] = classDefinition; slotPermissions[fileIndex] = shortValue(); slotName[fileIndex] = readConstantIndex(); slotType[fileIndex] = readConstantIndex();
            checkConstant(slotName[fileIndex], 1); checkConstant(slotType[fileIndex], 1);
            int preservedValue = readPosition; readPosition = constantFirstValue[slotType[fileIndex]]; int categoryCode = descriptorType(readPosition + constantSecondValue[slotType[fileIndex]], false); readPosition = preservedValue;
            if ((slotPermissions[fileIndex] & 8) == 0) slotPosition[fileIndex] = classSlotCount[classDefinition]++;
            int attributeData = shortValue();
            for (int innerPosition = 0; innerPosition < attributeData && !error; innerPosition++) {
                int nameConstant = readConstantIndex(), validLength = Integer();
                if (wordText(nameConstant, "ConstantValue") && validLength == 2) {
                    int dataValue = readConstantIndex();
                    if (categoryCode == 1 && checkConstant(dataValue, 3)) slotData[fileIndex] = constantFirstValue[dataValue];
                    else if (categoryCode == 2 && checkConstant(dataValue, 8)) slotData[fileIndex] = constantText(constantFirstValue[dataValue]);
                } else skipBytes(validLength);
            }
        }
        int itemCount = shortValue();
        if (itemCount > 512 - methodCount) { failureValue("method count limit (512)"); return; }
        for (int loopIndex = 0; loopIndex < itemCount && !error; loopIndex++) {
            int number = methodCount++; methodOwner[number] = classDefinition;
            methodAccess[number] = shortValue(); methodNameText[number] = readConstantIndex(); methodType[number] = readConstantIndex();
            checkConstant(methodNameText[number], 1); readDescriptor(number);
            if ((methodAccess[number] & 8) == 0) {
                if (methodArgumentCount[number] == 16) { failureValue("too many instance method arguments"); return; }
                for (int comparisonPosition = methodArgumentCount[number]; comparisonPosition > 0; comparisonPosition--) methodArgumentType[number * 16 + comparisonPosition] = methodArgumentType[number * 16 + comparisonPosition - 1];
                methodArgumentType[number * 16] = 2; methodArgumentCount[number]++;
            }
            if ((methodAccess[number] & 0x100) != 0) failureValue("user native method unsupported");
            if (wordText(methodNameText[number], "<clinit>")) initializeClassDefinition[classDefinition] = number + 1;
            for (int frontValue = 0; frontValue < number; frontValue++) if (methodOwner[frontValue] == classDefinition && matchingWord(methodNameText[frontValue], methodNameText[number]) && matchingWord(methodType[frontValue], methodType[number])) failureValue("duplicate method");
            int attributeCount = shortValue();
            for (int attributeValue = 0; attributeValue < attributeCount && !error; attributeValue++) {
                int name = readConstantIndex(), lengthValue = Integer(), run = readPosition;
                if (!clip(run, lengthValue)) { failureValue("truncated method attribute"); break; }
                if (wordText(name, "Code")) {
                    if (methodStart[number] != 0) failureValue("duplicate Code attribute");
                    methodStack[number] = shortValue(); methodLocals[number] = shortValue(); int codeLength = Integer();
                    if (methodStack[number] > 128 || methodLocals[number] > 128 || methodLocals[number] < methodArgumentCount[number]
                        || codeLength < 1 || codeLength > 8192) failureValue("method memory limits exceeded");
                    methodStart[number] = readPosition; skipBytes(codeLength); methodEnd[number] = readPosition;
                    int catchingCount = shortValue();
                    if (catchingCount > 1024 - catchCount) { failureValue("exception table limit"); return; }
                    for (int innerPosition = 0; innerPosition < catchingCount; innerPosition++) {
                        int errorReference = catchCount++; catchMethod[errorReference] = number;
                        catchStart[errorReference] = methodStart[number] + shortValue(); catchEnd[errorReference] = methodStart[number] + shortValue();
                        catchPosition[errorReference] = methodStart[number] + shortValue(); int encodedValue = readConstantIndex(); catchClass[errorReference] = encodedValue == 0 ? 0 : classNameText(encodedValue);
                    }
                    skipAttribute();
                    if (readPosition != run + lengthValue) failureValue("Code attribute size mismatch");
                } else skipBytes(lengthValue);
            }
            if ((methodAccess[number] & 0x400) != 0) continue;
            if (methodStart[number] == 0) failureValue("missing Code attribute");
            int slotEntry = methodStart[number];
            while (slotEntry < methodEnd[number] && !error) {
                int lengthValue = readLength(slotEntry, methodStart[number], methodEnd[number]);
                if (lengthValue == 0) { failureValue("unsupported or truncated bytecode"); break; }
                boundaryValue[slotEntry] = number + 1; slotEntry += lengthValue;
            }
            slotEntry = methodStart[number];
            while (slotEntry < methodEnd[number] && !error) {
                int value = file[slotEntry];
                if (value >= 153 && value <= 167 || value == 198 || value == 199) checkDestinationValue(slotEntry + (short)(file[slotEntry + 1] << 8 | file[slotEntry + 2]), number);
                if (value == 200) checkDestinationValue(slotEntry + positionInteger(slotEntry + 1), number);
                if (value == 170 || value == 171) {
                    int readCursor = slotEntry + 1; while ((readCursor - methodStart[number]) % 4 != 0) readCursor++;
                    checkDestinationValue(slotEntry + positionInteger(readCursor), number);
                    int entryCount = value == 170 ? positionInteger(readCursor + 8) - positionInteger(readCursor + 4) + 1 : positionInteger(readCursor + 4);
                    readCursor += value == 170 ? 12 : 8;
                    for (int innerPosition = 0; innerPosition < entryCount; innerPosition++) checkDestinationValue(slotEntry + positionInteger(readCursor + innerPosition * (value == 170 ? 4 : 8) + (value == 170 ? 0 : 4)), number);
                }
                slotEntry += readLength(slotEntry, methodStart[number], methodEnd[number]);
            }
            for (int innerPosition = 0; innerPosition < catchCount; innerPosition++) if (catchMethod[innerPosition] == number) {
                checkDestinationValue(catchStart[innerPosition], number); checkDestinationValue(catchPosition[innerPosition], number);
                if (catchEnd[innerPosition] != methodEnd[number]) checkDestinationValue(catchEnd[innerPosition], number);
                if (catchStart[innerPosition] >= catchEnd[innerPosition]) failureValue("invalid exception range");
            }
        }
        if (!error) skipAttribute();
        if (readPosition != size) failureValue("extra class file data");
    }
    static int allocateStorage(int kindValue, int lengthValue) { return newMemory(kindValue, lengthValue); }
    static boolean objectValue(int reference, int kindValue) {
        if (!isValidObject(reference)) return false;
        if (heapValue[reference] != kindValue) { failureValue("object type mismatch"); return false; }
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
        if (returnType == 2) protectValue(operandStackValue[slotEntry]);
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
        if (frameIndex % 32 == 31) { failureValue("call stack limit (32)"); return; }
        int nextItem = frameIndex + 1;
        for (int number = 0; number < 128; number++) localType[nextItem * 128 + number] = 0;
        for (int number = methodArgumentCount[functionValue] - 1; number >= 0; number--) {
            localValue[nextItem * 128 + number] = subtractValues(methodArgumentType[functionValue * 16 + number]); localType[nextItem * 128 + number] = methodArgumentType[functionValue * 16 + number];
        }
        if (error) return;
        frameIndex = nextItem; initializeFrame[frameIndex] = 0; frameMethod[frameIndex] = functionValue; framePosition[frameIndex] = methodStart[functionValue]; frameStack[frameIndex] = 0;
    }
    static void returnResult(int typeValue) {
        if (typeValue != methodReturn[frameMethod[frameIndex]]) { failureValue("return type mismatch"); return; }
        int value = typeValue == 0 ? 0 : subtractValues(typeValue);
        if (initializeFrame[frameIndex] != 0) classDefinitionState[initializeFrame[frameIndex] - 1] = 2;
        if (frameLock[frameIndex] != 0) { releaseLock(frameLock[frameIndex]); frameLock[frameIndex] = 0; }
        frameIndex--; if (frameIndex >= currentThread * 32 && typeValue != 0) putValue(value, typeValue);
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
                if (value < 1) { failureValue("invalid file stream path"); return; }
                streamFileName[slotEntry] = value;
            }
            streamFileName[lengthValue] = 0;
            int descriptorEntry = User.openFileDescriptor(streamFileName, Output ? (continuationValue ? 1089 : 577) : 0);
            if (descriptorEntry < 0) { failureValue("FileNotFoundException: file open failed"); return; }
            heapValue[streamValue + 2] = descriptorEntry; heapValue[streamValue + 3] = 1;
            return;
        }
        if (command != 182) { failureValue("invalid file stream invocation"); return; }
        if ((Output && wordText(name, "write") || !Output && wordText(name, "read"))
            && (wordText(formatValue, Output ? "([B)V" : "([B)I") || wordText(formatValue, Output ? "([BII)V" : "([BII)I"))) {
            boolean clipValue = wordText(formatValue, Output ? "([BII)V" : "([BII)I");
            int entryCount = clipValue ? subtractValues(1) : 0, startingPoint = clipValue ? subtractValues(1) : 0, dataArray = subtractValues(2), objectReference = subtractValues(2);
            if (!objectValue(dataArray, 20) || !objectValue(objectReference, kindValue)) return;
            if (!clipValue) entryCount = heapValue[dataArray + 1];
            if (startingPoint < 0 || entryCount < 0 || startingPoint > heapValue[dataArray + 1] - entryCount) { throwException(6, "file buffer bounds"); return; }
            if (heapValue[objectReference + 3] == 0 || heapValue[objectReference + 2] < 0) { failureValue("IOException: stream closed"); return; }
            int completedCount = 0;
            while (completedCount < entryCount && !error) {
                int returnedValue = Output ? User.writeOneFileByte(heapValue[objectReference + 2], heapValue[dataArray + 2 + startingPoint + completedCount]) : User.readOneFileByte(heapValue[objectReference + 2]);
                if (returnedValue < 0) { failureValue(Output ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Output && returnedValue == 256) break;
                if (!Output) heapValue[dataArray + 2 + startingPoint + completedCount] = (byte)returnedValue;
                completedCount++;
            }
            if (!Output) putValue(entryCount != 0 && completedCount == 0 ? -1 : completedCount, 1);
            return;
        }
        if (Output && wordText(name, "flush") && wordText(formatValue, "()V")) { int objectReference = subtractValues(2); if (objectValue(objectReference, kindValue) && heapValue[objectReference + 2] < 0) failureValue("IOException: stream closed"); return; }
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
            if (result < -1) failureValue("IOException: read failed"); else putValue(result == 256 ? -1 : result, 1);
        } else if (User.writeOneFileByte(descriptorEntry, value) != 1) failureValue("IOException: write failed");
    }
    static void callMethod(int index, int command) {
        if (index <= 0 || index >= constantTag.length || (constantTag[index] != 10 && constantTag[index] != 11)) { failureValue("invalid method reference"); return; }
        int ownerValue = classNameText(constantFirstValue[index]), name = referenceName(constantSecondValue[index]), formatValue = referenceType(constantSecondValue[index]);
        if (error) return;
        if (invokeDefault(ownerValue, name, formatValue, command)) return;
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
        int classDefinition = findClassDefinition(ownerValue); if (classDefinition < 0 || error) return;
        int fileIndex = findMethod(classDefinition, name, formatValue);
        if (fileIndex < 0) {
            for (int characterCode = classDefinition, entryCount = 0; characterCode >= 0 && entryCount < 16; entryCount++, characterCode = parentClass(characterCode))
                if (wordText(classDefinitionParent[characterCode], "java/lang/Thread")) { invokeThread(name, formatValue, command); return; }
            failureValue("NoSuchMethodError"); return;
        }
        if (((methodAccess[fileIndex] & 8) != 0) != (command == 184)) { failureValue("method static/instance mismatch"); return; }
        if (command == 184) { if (!initialize(methodOwner[fileIndex], frameInstruction[frameIndex])) return; }
        else {
            int readCursor = frameStack[frameIndex] - methodArgumentCount[fileIndex];
            if (readCursor < 0 || operandStackType[frameIndex * 128 + readCursor] != 2) { failureValue("invalid method receiver"); return; }
            int objectReference = operandStackValue[frameIndex * 128 + readCursor];
            if (!isValidObject(objectReference)) return;
            if (heapValue[objectReference] < 32 || !containsClass(heapValue[objectReference] - 32, ownerValue)) { failureValue("method receiver type mismatch"); return; }
            if (command != 183) fileIndex = findMethod(heapValue[objectReference] - 32, name, formatValue);
        }
        if (fileIndex < 0 || (methodAccess[fileIndex] & 0x400) != 0) { failureValue("AbstractMethodError"); return; }
        int lockReference = 0;
        if ((methodAccess[fileIndex] & 32) != 0) {
            if (command == 184) { int characterCode = methodOwner[fileIndex]; if (classLock[characterCode] == 0) classLock[characterCode] = allocateStorage(8, 0); lockReference = classLock[characterCode]; }
            else lockReference = operandStackValue[frameIndex * 128 + frameStack[frameIndex] - methodArgumentCount[fileIndex]];
            if (!acquireLock(lockReference)) { if (!error) framePosition[frameIndex] = frameInstruction[frameIndex]; return; }
        }
        invoke(fileIndex); if (!error) frameLock[frameIndex] = lockReference;
    }
    static boolean canStoreArray(int arrayReference, int dataValue) {
        if (dataValue == 0 || arrayElement[arrayReference] == 0) return true;
        boolean isSuccessful = arrayElement[arrayReference] == -1 ? (dataValue > 0 && dataValue < heapEndPosition && heapValue[dataValue] == 1) : matchingObject(dataValue, arrayElement[arrayReference]);
        if (!isSuccessful && !error) throwException(17, "array element type mismatch");
        return isSuccessful;
    }
    static int arraySlot(int reference, int subscriptValue, int typeValue) {
        if (!objectValue(reference, typeValue)) return 0;
        if (subscriptValue < 0 || subscriptValue >= heapValue[reference + 1]) { failureValue("ArrayIndexOutOfBoundsException"); return 0; }
        return reference + 2 + subscriptValue;
    }
    static void executeCommand() {
        int remainderData = 500000, fragmentValue = 100;
        while (true) {
            if (error) { if (thrownObject != 0) handleException(); if (error || frameIndex < currentThread * 32) break; }
            if (frameIndex < currentThread * 32 || changeRequest || --fragmentValue == 0) { if (!switchThread()) break; fragmentValue = 100; }
            if (frameIndex == 0 && classDefinitionState[entryClassDefinition] != 2 && !initialize(entryClassDefinition, framePosition[frameIndex])) continue;
            if (frameIndex == currentThread * 32 && currentThread != 0 && (methodAccess[frameMethod[frameIndex]] & 32) != 0 && frameLock[frameIndex] == 0) {
                int objectReference = threadTarget[currentThread]; if (!acquireLock(objectReference)) { if (error) break; continue; } frameLock[frameIndex] = objectReference;
            }
            temporaryCount = 0;
            if (--remainderData == 0) { failureValue("instruction limit (500000)"); break; }
            int run = framePosition[frameIndex]; frameInstruction[frameIndex] = run; int value = readOpcodeByte();
            if (error) break;
            if (value == 0) continue;
            if (value == 1) { putValue(0, 2); continue; }
            if (value >= 2 && value <= 8) { putValue(value - 3, 1); continue; }
            if (value == 16) { putValue((byte)readOpcodeByte(), 1); continue; }
            if (value == 17) { putValue((short)readOpcodeShort(), 1); continue; }
            if (value == 18 || value == 19) {
                int number = methodOwner[frameMethod[frameIndex]] * 512 + (value == 18 ? readOpcodeByte() : readOpcodeShort());
                if (number <= 0 || number >= constantTag.length) failureValue("invalid ldc constant");
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
            if (value == 46 || value >= 50 && value <= 53) {
                int entryPosition = subtractValues(1), objectReference = subtractValues(2), categoryCode = value == 46 ? 2 : value == 50 ? 3 : value == 51 ? 20 : value == 52 ? 22 : 23;
                if (value == 51 && objectReference > 0 && objectReference < heapEndPosition && heapValue[objectReference] == 21) categoryCode = 21;
                int readCursor = arraySlot(objectReference, entryPosition, categoryCode); if (!error) putValue(heapValue[readCursor], value == 50 ? 2 : 1); continue;
            }
            if (value == 79 || value >= 83 && value <= 86) {
                int entryReference = subtractValues(value == 83 ? 2 : 1), entryPosition = subtractValues(1), objectReference = subtractValues(2), categoryCode = value == 79 ? 2 : value == 83 ? 3 : value == 84 ? 20 : value == 85 ? 22 : 23;
                if (value == 84 && objectReference > 0 && objectReference < heapEndPosition && heapValue[objectReference] == 21) categoryCode = 21;
                int readCursor = arraySlot(objectReference, entryPosition, categoryCode);
                if (!error && categoryCode == 3 && !canStoreArray(objectReference, entryReference)) continue;
                if (!error) heapValue[readCursor] = categoryCode == 20 ? (byte)entryReference : categoryCode == 21 ? entryReference & 1 : categoryCode == 22 ? (char)entryReference : categoryCode == 23 ? (short)entryReference : entryReference;
                continue;
            }
            if (value >= 87 && value <= 95) { stackInstruction(value); continue; }
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
            if (value >= 178 && value <= 181) { invokeField(readOpcodeConstant(), value, run); continue; }
            if (value >= 182 && value <= 185) {
                int encodedValue = readOpcodeConstant();
                if (value == 185) { int totalCount = readOpcodeByte(); if (totalCount == 0 || readOpcodeByte() != 0) { failureValue("invalid invokeinterface operands"); continue; } }
                callMethod(encodedValue, value); continue;
            }
            if (value == 187) { newObject(classNameText(readOpcodeConstant()), run); continue; }
            if (value == 188 || value == 189) {
                int categoryCode = 3, component = 0;
                if (value == 188) { int temporaryData = readOpcodeByte(); categoryCode = temporaryData == 10 ? 2 : temporaryData == 8 ? 20 : temporaryData == 4 ? 21 : temporaryData == 5 ? 22 : temporaryData == 9 ? 23 : 0; }
                else component = classNameText(readOpcodeConstant());
                if (categoryCode == 0) { failureValue("unsupported primitive array type"); continue; }
                int validLength = subtractValues(1), objectReference = allocateStorage(categoryCode, validLength); if (!error) arrayElement[objectReference] = component; putValue(objectReference, 2); continue;
            }
            if (value == 190) {
                int objectReference = subtractValues(2);
                if (isValidObject(objectReference)) { int comparisonPosition = heapValue[objectReference]; if (comparisonPosition != 2 && comparisonPosition != 3 && (comparisonPosition < 20 || comparisonPosition > 23)) failureValue("not an array"); else putValue(heapValue[objectReference + 1], 1); }
                continue;
            }
            if (value == 191) {
                int objectReference = subtractValues(2); if (isValidObject(objectReference)) { if (heapValue[objectReference] != 9) failureValue("athrow requires supported Throwable"); else { thrownObject = objectReference; error = true; } }
                continue;
            }
            if (value == 192 || value == 193) {
                int nameConstant = classNameText(readOpcodeConstant()), objectReference = subtractValues(2); boolean match = matchingObject(objectReference, nameConstant);
                if (value == 193) putValue(objectReference != 0 && match ? 1 : 0, 1);
                else { if (!match && !error) failureValue("ClassCastException"); putValue(objectReference, 2); }
                continue;
            }
            if (value == 170 || value == 171) {
                int readCursor = run + 1, fileIndex = frameMethod[frameIndex], keyReference = subtractValues(1);
                while ((readCursor - methodStart[fileIndex]) % 4 != 0) readCursor++;
                int targetAddress = positionInteger(readCursor);
                if (value == 170) { int lowValue = positionInteger(readCursor + 4), highValue = positionInteger(readCursor + 8); if (keyReference >= lowValue && keyReference <= highValue) targetAddress = positionInteger(readCursor + 12 + (keyReference - lowValue) * 4); }
                else { int totalCount = positionInteger(readCursor + 4); for (int loopIndex = 0; loopIndex < totalCount; loopIndex++) if (positionInteger(readCursor + 8 + loopIndex * 8) == keyReference) targetAddress = positionInteger(readCursor + 12 + loopIndex * 8); }
                moveValue(run + targetAddress); continue;
            }
            if (value == 200) { moveValue(run + positionInteger(run + 1)); continue; }
            if (value == 194 || value == 195) {
                int objectReference = subtractValues(2);
                if (value == 195) releaseLock(objectReference);
                else if (!acquireLock(objectReference) && !error) { putValue(objectReference, 2); framePosition[frameIndex] = run; }
                continue;
            }
            if (value == 196) {
                int commandCode = readOpcodeByte(), entryPosition = readOpcodeShort();
                if (commandCode == 21 || commandCode == 25) readLocal(entryPosition, commandCode == 21 ? 1 : 2);
                else if (commandCode == 54 || commandCode == 58) writeLocal(entryPosition, commandCode == 54 ? 1 : 2);
                else if (commandCode == 132) { int deltaValue = (short)readOpcodeShort(); readLocal(entryPosition, 1); putValue(subtractValues(1) + deltaValue, 1); writeLocal(entryPosition, 1); }
                else failureValue("unsupported wide opcode");
                continue;
            }
            failureValue("unsupported bytecode");
        }
    }
    static int findClassDefinition(int name) {
        for (int loopIndex = 0; loopIndex < classDefinitionCount; loopIndex++) if (classDefinitionName[loopIndex] != 0 && matchingWord(classDefinitionName[loopIndex], name)) return loopIndex;
        return loadClassDefinition(constantText(name));
    }
    static int loadClassDefinition(int nameString) {
        if (!objectValue(nameString, 1)) return -1;
        int lengthValue = heapValue[nameString + 1];
        if (lengthValue < 1 || lengthValue > 505 || classDefinitionCount == 16) { failureValue("class name/count limit"); return -1; }
        for (int loopIndex = 0; loopIndex < lengthValue; loopIndex++) { int characterCode = heapValue[nameString + 2 + loopIndex]; fileNameText[loopIndex] = characterCode == '/' ? '.' : characterCode; }
        fileNameText[lengthValue] = '.'; fileNameText[lengthValue + 1] = 'c'; fileNameText[lengthValue + 2] = 'l'; fileNameText[lengthValue + 3] = 'a'; fileNameText[lengthValue + 4] = 's'; fileNameText[lengthValue + 5] = 's'; fileNameText[lengthValue + 6] = 0;
        int size = User.readFile(fileNameText, temporaryFile);
        if (size < 0) { failureValue("ClassNotFoundException"); return -1; }
        int classDefinition = classDefinitionCount++; classDefinitionSize[classDefinition] = size;
        for (int loopIndex = 0; loopIndex < size; loopIndex++) file[classDefinition * 16384 + loopIndex] = temporaryFile[loopIndex];
        readClass(classDefinition); if (error) return -1;
        int actualData = constantText(classDefinitionName[classDefinition]);
        if (!textsEqual(actualData, nameString, true)) { failureValue("class name does not match file"); return -1; }
        int parentValue = classDefinitionParent[classDefinition];
        if (parentValue != 0 && !wordText(parentValue, "java/lang/Object") && !wordText(parentValue, "java/lang/Thread")) {
            // A registered class is not loaded again; inheritance cycles are explicitly rejected.
            int topValue = findClassDefinition(parentValue);
            if (error || topValue < 0) return -1;
            int readCursor = topValue, stageCount = 0;
            while (readCursor >= 0 && stageCount++ < 16) {
                if (readCursor == classDefinition) { failureValue("cyclic inheritance"); return -1; }
                readCursor = parentClass(readCursor);
            }
            int startDisplacement = classSlotCount[topValue];
            for (int fileIndex = 0; fileIndex < slotCount; fileIndex++) if (slotOwner[fileIndex] == classDefinition && (slotPermissions[fileIndex] & 8) == 0) slotPosition[fileIndex] += startDisplacement;
            classSlotCount[classDefinition] += startDisplacement;
        }
        return classDefinition;
    }
    static int parentClass(int classDefinition) {
        int name = classDefinitionParent[classDefinition];
        for (int loopIndex = 0; loopIndex < classDefinitionCount; loopIndex++) if (name != 0 && classDefinitionName[loopIndex] != 0 && matchingWord(classDefinitionName[loopIndex], name)) return loopIndex;
        return -1;
    }
    static int findMethod(int classDefinition, int name, int formatValue) {
        for (int depthValue = 0; classDefinition >= 0 && depthValue < 16; depthValue++, classDefinition = parentClass(classDefinition)) {
            for (int loopIndex = 0; loopIndex < methodCount; loopIndex++) if (methodOwner[loopIndex] == classDefinition && matchingWord(methodNameText[loopIndex], name) && matchingWord(methodType[loopIndex], formatValue)) return loopIndex;
        }
        return -1;
    }
    static int nameMethod(int classDefinition, String name, String formatValue) {
        for (int depthValue = 0; classDefinition >= 0 && depthValue < 16; depthValue++, classDefinition = parentClass(classDefinition))
            for (int loopIndex = 0; loopIndex < methodCount; loopIndex++) if (methodOwner[loopIndex] == classDefinition && wordText(methodNameText[loopIndex], name) && wordText(methodType[loopIndex], formatValue)) return loopIndex;
        return -1;
    }
    static int typeKind(int name) { return file[constantFirstValue[name]] == 'L' || file[constantFirstValue[name]] == '[' ? 2 : 1; }
    static boolean initialize(int classDefinition, int commandStart) {
        if (classDefinition < 0 || error) return false;
        if (classDefinitionState[classDefinition] == 3) { failureValue("NoClassDefFoundError: initialization failed"); return false; }
        if (classDefinitionState[classDefinition] == 1 && classThread[classDefinition] != currentThread) { framePosition[frameIndex] = commandStart; changeRequest = true; return false; }
        if (classDefinitionState[classDefinition] != 0) return true;
        int topValue = parentClass(classDefinition);
        if (topValue >= 0 && !initialize(topValue, commandStart)) return false;
        classDefinitionState[classDefinition] = 1; classThread[classDefinition] = currentThread;
        if (initializeClassDefinition[classDefinition] != 0) {
            framePosition[frameIndex] = commandStart;
            invoke(initializeClassDefinition[classDefinition] - 1); if (!error) initializeFrame[frameIndex] = classDefinition + 1;
            return false;
        }
        classDefinitionState[classDefinition] = 2; return true;
    }
    static void invokeField(int index, int command, int run) {
        if (!checkConstant(index, 9)) return;
        int ownerValue = classNameText(constantFirstValue[index]), name = referenceName(constantSecondValue[index]), formatValue = referenceType(constantSecondValue[index]);
        if (wordText(ownerValue, "java/lang/System") && (wordText(name, "out") || wordText(name, "err")) && wordText(formatValue, "Ljava/io/PrintStream;") && command == 178) { putValue(-1, 2); return; }
        int classDefinition = findClassDefinition(ownerValue); if (classDefinition < 0 || error) return;
        int foundValue = -1;
        for (int readCursor = classDefinition, depthValue = 0; readCursor >= 0 && depthValue < 16 && foundValue < 0; depthValue++, readCursor = parentClass(readCursor))
            for (int fileIndex = 0; fileIndex < slotCount; fileIndex++) if (slotOwner[fileIndex] == readCursor && matchingWord(slotName[fileIndex], name) && matchingWord(slotType[fileIndex], formatValue)) foundValue = fileIndex;
        if (foundValue < 0) { failureValue("NoSuchFieldError"); return; }
        boolean staticValue = command == 178 || command == 179;
        if (staticValue != ((slotPermissions[foundValue] & 8) != 0)) { failureValue("field static/instance mismatch"); return; }
        if (staticValue && !initialize(slotOwner[foundValue], run)) return;
        int typeValue = typeKind(formatValue), value = 0;
        if (command == 179 || command == 181) value = subtractValues(typeValue);
        if (staticValue) { if (command == 178) putValue(slotData[foundValue], typeValue); else if (!error) slotData[foundValue] = value; return; }
        int objectReference = subtractValues(2);
        if (!isValidObject(objectReference)) return;
        if (heapValue[objectReference] < 32 || !containsClass(heapValue[objectReference] - 32, ownerValue)) { failureValue("field receiver type mismatch"); return; }
        int preservedSlot = objectReference + 2 + slotPosition[foundValue];
        if (command == 180) putValue(heapValue[preservedSlot], typeValue);
        else if (!error) { heapValue[preservedSlot] = value; heapReference[preservedSlot] = typeValue == 2 ? 1 : 0; }
    }
    static boolean containsClass(int classDefinition, int name) {
        for (int depth = 0; classDefinition >= 0 && depth < 16; depth++, classDefinition = parentClass(classDefinition)) {
            if (matchingWord(classDefinitionName[classDefinition], name) || (classDefinitionParent[classDefinition] != 0 && matchingWord(classDefinitionParent[classDefinition], name))) return true;
            for (int innerPosition = 0; innerPosition < classInterfaceCount[classDefinition]; innerPosition++) if (matchingWord(classInterface[classDefinition * 16 + innerPosition], name)) return true;
        }
        return false;
    }
    static boolean textsEqual(int firstData, int byteData, boolean path) {
        if (firstData == byteData) return true;
        if (firstData <= 0 || byteData <= 0 || heapValue[firstData] != 1 || heapValue[byteData] != 1 || heapValue[firstData + 1] != heapValue[byteData + 1]) return false;
        for (int loopIndex = 0; loopIndex < heapValue[firstData + 1]; loopIndex++) {
            int xCoordinate = heapValue[firstData + 2 + loopIndex], yCoordinate = heapValue[byteData + 2 + loopIndex];
            if (path) { if (xCoordinate == '.') xCoordinate = '/'; if (yCoordinate == '.') yCoordinate = '/'; }
            if (xCoordinate != yCoordinate) return false;
        }
        return true;
    }
    static boolean isValidObject(int objectReference) {
        if (objectReference == 0) { failureValue("NullPointerException"); return false; }
        if (objectReference < 1 || objectReference >= heapEndPosition || heapWidth[objectReference] < 2 || heapValue[objectReference] == 0) { failureValue("invalid object reference"); return false; }
        return true;
    }
    static void protectValue(int objectReference) {
        if (objectReference > 0 && objectReference < heapEndPosition && heapWidth[objectReference] >= 2 && temporaryCount < temporaryReference.length) temporaryReference[temporaryCount++] = objectReference;
    }
    static void showValue(int objectReference) {
        if (objectReference > 0 && objectReference < heapEndPosition && heapWidth[objectReference] >= 2 && heapValue[objectReference] != 0 && heapMark[objectReference] == 0) {
            heapMark[objectReference] = 1; waitForDisplay[displayCount++] = objectReference;
        }
    }
    static void collectGarbage() {
        displayCount = 0; collectionCount++;
        for (int checkPosition = 1; checkPosition < heapEndPosition; checkPosition += heapWidth[checkPosition]) heapMark[checkPosition] = 0;
        for (int loopIndex = 0; loopIndex < stringReference.length; loopIndex++) showValue(stringReference[loopIndex]);
        for (int loopIndex = 0; loopIndex < slotCount; loopIndex++) if ((slotPermissions[loopIndex] & 8) != 0 && typeKind(slotType[loopIndex]) == 2) showValue(slotData[loopIndex]);
        for (int temporaryData = 0; temporaryData < threadCount; temporaryData++) {
            showValue(threadObject[temporaryData]); showValue(threadTarget[temporaryData]);
            int topPosition = temporaryData == currentThread ? frameIndex : threadFrame[temporaryData];
            for (int fileIndex = temporaryData * 32; fileIndex <= topPosition; fileIndex++) {
                for (int innerPosition = 0; innerPosition < methodLocals[frameMethod[fileIndex]]; innerPosition++) if (localType[fileIndex * 128 + innerPosition] == 2) showValue(localValue[fileIndex * 128 + innerPosition]);
                for (int innerPosition = 0; innerPosition < frameStack[fileIndex]; innerPosition++) if (operandStackType[fileIndex * 128 + innerPosition] == 2) showValue(operandStackValue[fileIndex * 128 + innerPosition]);
            }
        }
        for (int loopIndex = 0; loopIndex < screenReference.length; loopIndex++) showValue(screenReference[loopIndex]);
        for (int loopIndex = 0; loopIndex < laterCount; loopIndex++) showValue(scheduleLater[loopIndex]);
        for (int loopIndex = 0; loopIndex < storeInteger.length; loopIndex++) showValue(storeInteger[loopIndex]);
        for (int loopIndex = 0; loopIndex < classDefinitionCount; loopIndex++) showValue(classLock[loopIndex]);
        for (int checkPosition = 1; checkPosition < heapEndPosition; checkPosition += heapWidth[checkPosition]) if (lockDepth[checkPosition] > 0) showValue(checkPosition);
        showValue(thrownObject);
        for (int loopIndex = 0; loopIndex < temporaryCount; loopIndex++) showValue(temporaryReference[loopIndex]);
        while (displayCount > 0) {
            int objectReference = waitForDisplay[--displayCount], categoryCode = heapValue[objectReference];
            for (int loopIndex = objectReference + 2; loopIndex < objectReference + heapWidth[objectReference]; loopIndex++) if (categoryCode == 3 || categoryCode == 4 || heapReference[loopIndex] != 0) showValue(heapValue[loopIndex]);
        }
        for (int checkPosition = 1; checkPosition < heapEndPosition; checkPosition += heapWidth[checkPosition]) if (heapMark[checkPosition] == 0) heapValue[checkPosition] = 0;
        for (int checkPosition = 1; checkPosition < heapEndPosition; checkPosition += heapWidth[checkPosition]) if (heapValue[checkPosition] == 0) {
            while (checkPosition + heapWidth[checkPosition] < heapEndPosition && heapValue[checkPosition + heapWidth[checkPosition]] == 0) { int nextPosition = checkPosition + heapWidth[checkPosition]; heapWidth[checkPosition] += heapWidth[nextPosition]; heapWidth[nextPosition] = 0; }
            if (checkPosition + heapWidth[checkPosition] == heapEndPosition) { heapEndPosition = checkPosition; break; }
        }
    }
    static int newMemory(int kindValue, int lengthValue) {
        if (lengthValue < 0) { failureValue("NegativeArraySizeException"); return 0; }
        if (lengthValue > heapValue.length - 3) { failureValue("object heap exhausted"); return 0; }
        int requiredCount = lengthValue + 2, objectReference = 0;
        if (requiredCount <= heapValue.length - heapEndPosition) { objectReference = heapEndPosition; heapEndPosition += requiredCount; }
        else {
            collectGarbage();
            for (int readCursor = 1; readCursor < heapEndPosition; readCursor += heapWidth[readCursor]) if (heapValue[readCursor] == 0 && heapWidth[readCursor] >= requiredCount) { objectReference = readCursor; break; }
            if (objectReference != 0) {
                int remainingLength = heapWidth[objectReference] - requiredCount;
                if (remainingLength >= 2) { heapWidth[objectReference + requiredCount] = remainingLength; heapValue[objectReference + requiredCount] = 0; }
                else requiredCount += remainingLength;
            } else if (requiredCount <= heapValue.length - heapEndPosition) { objectReference = heapEndPosition; heapEndPosition += requiredCount; }
        }
        if (objectReference == 0) { failureValue("object heap exhausted"); return 0; }
        for (int loopIndex = 0; loopIndex < requiredCount; loopIndex++) { heapValue[objectReference + loopIndex] = 0; heapReference[objectReference + loopIndex] = 0; heapWidth[objectReference + loopIndex] = 0; }
        arrayElement[objectReference] = 0;
        heapWidth[objectReference] = requiredCount; heapValue[objectReference] = kindValue; heapValue[objectReference + 1] = lengthValue; protectValue(objectReference); return objectReference;
    }
    static int exceptionClass(String nameConstant) {
        if (JavaTools.equalText(nameConstant, "java/lang/Throwable")) return 1;
        if (JavaTools.equalText(nameConstant, "java/lang/Exception")) return 2;
        if (JavaTools.equalText(nameConstant, "java/lang/RuntimeException")) return 3;
        if (JavaTools.equalText(nameConstant, "java/lang/ArithmeticException")) return 4;
        if (JavaTools.equalText(nameConstant, "java/lang/NullPointerException")) return 5;
        if (JavaTools.equalText(nameConstant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (JavaTools.equalText(nameConstant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (JavaTools.equalText(nameConstant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (JavaTools.equalText(nameConstant, "java/lang/IllegalArgumentException")) return 9;
        if (JavaTools.equalText(nameConstant, "java/lang/NumberFormatException")) return 10;
        if (JavaTools.equalText(nameConstant, "java/io/IOException")) return 11;
        if (JavaTools.equalText(nameConstant, "java/io/FileNotFoundException")) return 12;
        if (JavaTools.equalText(nameConstant, "java/lang/IllegalStateException")) return 13;
        if (JavaTools.equalText(nameConstant, "java/lang/ClassCastException")) return 14;
        if (JavaTools.equalText(nameConstant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int exceptionConstant(int name) {
        for (int loopIndex = 1; loopIndex <= 41; loopIndex++) if (wordText(name, exceptionName(loopIndex))) return loopIndex;
        return 0;
    }
    static String exceptionName(int identityValue) {
        if (identityValue == 40) return "java/lang/InterruptedException";
        if (identityValue == 41) return "English/Native/WaitInterruptedException";
        if (identityValue == 39) return "java/net/SocketException";
        if (identityValue == 20) return "English/Native/exception";
        if (identityValue == 21) return "English/Native/ExecutionException";
        if (identityValue == 22) return "English/Native/InputOutputException";
        if (identityValue == 23) return "English/Native/WaitTimeoutException";
        if (identityValue == 24) return "English/Native/AddressLookupException";
        if (identityValue == 25) return "English/Native/MissingFileException";
        if (identityValue == 26) return "English/Native/CommunicationException";
        if (identityValue == 27) return "English/Native/InvalidArgumentException";
        if (identityValue == 28) return "English/Native/NumberFormatFailure";
        if (identityValue == 29) return "English/Native/BoundsException";
        if (identityValue == 30) return "English/Native/ArrayBoundsException";
        if (identityValue == 31) return "English/Native/StringBoundsException";
        if (identityValue == 32) return "English/Native/NullReferenceException";
        if (identityValue == 33) return "English/Native/ArithmeticFailure";
        if (identityValue == 34) return "English/Native/StateException";
        if (identityValue == 35) return "English/Native/TypeCastException";
        if (identityValue == 36) return "English/Native/NegativeArraySizeFailure";
        if (identityValue == 37) return "English/Native/ArrayStoreFailure";
        if (identityValue == 38) return "English/Native/ThreadStateException";
        if (identityValue == 1) return "java/lang/Throwable"; if (identityValue == 2) return "java/lang/Exception";
        if (identityValue == 3) return "java/lang/RuntimeException"; if (identityValue == 4) return "java/lang/ArithmeticException";
        if (identityValue == 5) return "java/lang/NullPointerException"; if (identityValue == 6) return "java/lang/IndexOutOfBoundsException";
        if (identityValue == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (identityValue == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (identityValue == 9) return "java/lang/IllegalArgumentException"; if (identityValue == 10) return "java/lang/NumberFormatException";
        if (identityValue == 11) return "java/io/IOException"; if (identityValue == 12) return "java/io/FileNotFoundException";
        if (identityValue == 17) return "java/lang/ArrayStoreException";
        if (identityValue == 18) return "java/net/UnknownHostException";
        if (identityValue == 19) return "java/net/SocketTimeoutException";
        if (identityValue == 16) return "java/lang/IllegalThreadStateException";
        if (identityValue == 13) return "java/lang/IllegalStateException"; if (identityValue == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int exceptionParent(int identityValue) {
        if (identityValue == 40) return 2;
        if (identityValue == 41) return 40;
        if (identityValue == 39) return 11;
        if (identityValue == 1) return 0;
        if (identityValue == 2) return 1;
        if (identityValue == 3) return 2;
        if (identityValue == 4) return 3;
        if (identityValue == 5) return 3;
        if (identityValue == 6) return 3;
        if (identityValue == 7) return 6;
        if (identityValue == 8) return 6;
        if (identityValue == 9) return 3;
        if (identityValue == 10) return 9;
        if (identityValue == 11) return 2;
        if (identityValue == 12) return 11;
        if (identityValue == 13) return 3;
        if (identityValue == 14) return 3;
        if (identityValue == 15) return 3;
        if (identityValue == 16) return 9;
        if (identityValue == 17) return 3;
        if (identityValue == 18) return 11;
        if (identityValue == 19) return 11;
        if (identityValue == 20) return 2;
        if (identityValue == 21) return 3;
        if (identityValue == 22) return 11;
        if (identityValue == 23) return 22;
        if (identityValue == 24) return 22;
        if (identityValue == 25) return 22;
        if (identityValue == 26) return 22;
        if (identityValue == 27) return 9;
        if (identityValue == 28) return 27;
        if (identityValue == 29) return 6;
        if (identityValue == 30) return 29;
        if (identityValue == 31) return 29;
        if (identityValue == 32) return 5;
        if (identityValue == 33) return 4;
        if (identityValue == 34) return 13;
        if (identityValue == 35) return 14;
        if (identityValue == 36) return 15;
        if (identityValue == 37) return 17;
        if (identityValue == 38) return 16;
        return 0;
    }
    static boolean containsException(int actualValue, int wanted) {
        for (int depthValue = 0; actualValue != 0 && depthValue < 16; depthValue++, actualValue = exceptionParent(actualValue))
            if (actualValue == wanted) return true;
        return false;
    }
    static void throwException(int identityValue, String readmeReference) {
        int objectReference = newMemory(9, 2); if (error) return;
        heapValue[objectReference + 2] = identityValue; heapValue[objectReference + 3] = hostCharacter(readmeReference); heapReference[objectReference + 3] = 1;
        thrownObject = objectReference; error = true;
    }
    static boolean matchingObject(int objectReference, int name) {
        if (objectReference == 0) return true;
        if (!isValidObject(objectReference)) return false;
        int categoryCode = heapValue[objectReference];
        if (wordText(name, "java/lang/Object")) return true;
        if (categoryCode >= 32) return containsClass(categoryCode - 32, name);
        if (categoryCode == 9) { int targetAddress = exceptionConstant(name); return targetAddress != 0 && containsException(heapValue[objectReference + 2], targetAddress); }
        if (categoryCode == 1) return wordText(name, "java/lang/String") || wordText(name, "java/lang/CharSequence");
        if (categoryCode == 4) return wordText(name, "java/lang/StringBuilder") || wordText(name, "java/lang/CharSequence");
        if (categoryCode == 10) return wordText(name, "java/util/ArrayList") || wordText(name, "java/util/List");
        if (categoryCode == 11) return wordText(name, "java/util/HashMap") || wordText(name, "java/util/Map");
        if (categoryCode == 12) return wordText(name, "java/lang/Integer") || wordText(name, "java/lang/Number");
        if (categoryCode >= 24 && categoryCode <= 28 && heapValue[objectReference + 13] != 0) return koreanScreenClass(name) == categoryCode || wordText(name, "English/Native/ScreenElement");
        if (categoryCode >= 24 && categoryCode <= 28) return (koreanScreenClass(name) == 0 && screenClass(name) == categoryCode) || wordText(name, "java/awt/Component") || wordText(name, "java/awt/Container") || wordText(name, "javax/swing/JComponent");
        if (categoryCode == 29) return wordText(name, heapValue[objectReference + 3] != 0 ? "English/Native/ActionNotice" : "java/awt/event/ActionEvent");
        if (categoryCode == 30) return wordText(name, "java/awt/FlowLayout") || wordText(name, "java/awt/LayoutManager");
        if (categoryCode == 17) return wordText(name, "java/net/Socket");
        if (categoryCode == 18) return wordText(name, "java/net/ServerSocket");
        if (categoryCode == 19) return wordText(name, heapValue[objectReference + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (categoryCode == 14) return wordText(name, "java/net/InetAddress");
        if (categoryCode == 15) return wordText(name, "java/net/DatagramSocket");
        if (categoryCode == 16) return wordText(name, "java/net/DatagramPacket");
        if (categoryCode == 13) return wordText(name, heapValue[objectReference + 3] != 0 ? "English/Native/worker" : "java/lang/Thread");
        if (categoryCode == 2) return wordText(name, "[I"); if (categoryCode == 20) return wordText(name, "[B"); if (categoryCode == 21) return wordText(name, "[Z");
        if (categoryCode == 22) return wordText(name, "[C"); if (categoryCode == 23) return wordText(name, "[S");
        if (categoryCode != 3) return false;
        if (wordText(name, "[Ljava/lang/Object;")) return true;
        int component = arrayElement[objectReference];
        if (component == -1) return wordText(name, "[Ljava/lang/String;") || wordText(name, "[Ljava/lang/CharSequence;");
        if (component == 0) return false;
        if (compareArrayClasses(component, name)) return true;
        if ((wordText(component, "java/lang/String") || wordText(component, "java/lang/StringBuilder")) && wordText(name, "[Ljava/lang/CharSequence;")) return true;
        for (int loopIndex = 0; loopIndex < classDefinitionCount; loopIndex++) if (matchingWord(classDefinitionName[loopIndex], component)) {
            for (int characterCode = loopIndex, depth = 0; characterCode >= 0 && depth < 16; depth++, characterCode = parentClass(characterCode)) {
                if (compareArrayClasses(classDefinitionParent[characterCode], name)) return true;
                for (int innerPosition = 0; innerPosition < classInterfaceCount[characterCode]; innerPosition++) if (compareArrayClasses(classInterface[characterCode * 16 + innerPosition], name)) return true;
            }
        }
        return false;
    }
    static boolean compareArrayClasses(int nameConstant, int descriptor) {
        int checkPosition = constantFirstValue[descriptor], entryCount = constantSecondValue[descriptor];
        if (nameConstant == 0 || entryCount < 4 || file[checkPosition] != '[' || file[checkPosition + 1] != 'L' || file[checkPosition + entryCount - 1] != ';' || constantSecondValue[nameConstant] != entryCount - 3) return false;
        for (int loopIndex = 0; loopIndex < entryCount - 3; loopIndex++) if (file[constantFirstValue[nameConstant] + loopIndex] != file[checkPosition + 2 + loopIndex]) return false;
        return true;
    }
    static void handleException() {
        if (thrownObject == 0) return;
        error = false;
        while (frameIndex >= currentThread * 32) {
            int fileIndex = frameMethod[frameIndex], readCursor = frameInstruction[frameIndex];
            for (int loopIndex = 0; loopIndex < catchCount; loopIndex++) if (catchMethod[loopIndex] == fileIndex && readCursor >= catchStart[loopIndex] && readCursor < catchEnd[loopIndex]
                && (catchClass[loopIndex] == 0 || matchingObject(thrownObject, catchClass[loopIndex]))) {
                framePosition[frameIndex] = catchPosition[loopIndex]; frameStack[frameIndex] = 0; putValue(thrownObject, 2); thrownObject = 0; return;
            }
            if (initializeFrame[frameIndex] != 0) classDefinitionState[initializeFrame[frameIndex] - 1] = 3;
            if (frameLock[frameIndex] != 0) { releaseLock(frameLock[frameIndex]); frameLock[frameIndex] = 0; }
            frameIndex--;
        }
        User.write("Uncaught ");
        if (heapValue[thrownObject] == 9) { User.write(exceptionName(heapValue[thrownObject + 2])); User.write(": "); writeText(heapValue[thrownObject + 3]); }
        else User.write("user exception");
        User.writeCharacterValue(10); thrownObject = 0; error = true;
    }
    // This JVM currently permits only category-1 stack entries (int/reference).
    static void stackInstruction(int commandCode) {
        int firstData = subtractValues(0), firstFormat = returnType;
        if (commandCode == 87) return;
        if (commandCode == 89) { putValue(firstData, firstFormat); putValue(firstData, firstFormat); return; }
        int byteData = subtractValues(0), secondFormat = returnType;
        if (commandCode == 88) return;
        if (commandCode == 90) { putValue(firstData, firstFormat); putValue(byteData, secondFormat); putValue(firstData, firstFormat); return; }
        if (commandCode == 92) { putValue(byteData, secondFormat); putValue(firstData, firstFormat); putValue(byteData, secondFormat); putValue(firstData, firstFormat); return; }
        if (commandCode == 95) { putValue(firstData, firstFormat); putValue(byteData, secondFormat); return; }
        int characterCode = subtractValues(0), thirdFormat = returnType;
        if (commandCode == 91) { putValue(firstData, firstFormat); putValue(characterCode, thirdFormat); putValue(byteData, secondFormat); putValue(firstData, firstFormat); return; }
        if (commandCode == 93) { putValue(byteData, secondFormat); putValue(firstData, firstFormat); putValue(characterCode, thirdFormat); putValue(byteData, secondFormat); putValue(firstData, firstFormat); return; }
        int trailingValue = subtractValues(0), fourthFormat = returnType;
        putValue(byteData, secondFormat); putValue(firstData, firstFormat); putValue(trailingValue, fourthFormat); putValue(characterCode, thirdFormat); putValue(byteData, secondFormat); putValue(firstData, firstFormat);
    }
    static void newObject(int nameConstant, int startingPoint) {
        int categoryCode = 0, validLength = 0, exceptionReference = exceptionConstant(nameConstant);
        if (wordText(nameConstant, "java/lang/StringBuilder")) { categoryCode = 4; validLength = 1; }
        if (wordText(nameConstant, "java/io/FileInputStream")) { categoryCode = 5; validLength = 2; }
        if (wordText(nameConstant, "java/io/FileOutputStream")) { categoryCode = 6; validLength = 2; }
        if (exceptionReference != 0) { categoryCode = 9; validLength = 2; }
        if (wordText(nameConstant, "java/util/ArrayList")) { categoryCode = 10; validLength = 2; }
        if (wordText(nameConstant, "java/util/HashMap")) { categoryCode = 11; validLength = 2; }
        if (wordText(nameConstant, "java/lang/Integer")) { categoryCode = 12; validLength = 1; }
        if (wordText(nameConstant, "java/net/Socket")) { categoryCode = 17; validLength = 5; }
        if (wordText(nameConstant, "java/net/ServerSocket")) { categoryCode = 18; validLength = 5; }
        if (wordText(nameConstant, "java/net/DatagramSocket")) { categoryCode = 15; validLength = 3; }
        if (wordText(nameConstant, "java/net/DatagramPacket")) { categoryCode = 16; validLength = 4; }
        if (wordText(nameConstant, "java/lang/Thread") || wordText(nameConstant, "English/Native/worker")) { categoryCode = 13; validLength = 2; }
        if (wordText(nameConstant, "java/lang/Object")) { categoryCode = 8; }
        if (categoryCode == 0 && screenClass(nameConstant) != 0) { categoryCode = screenClass(nameConstant); validLength = 12; }
        if (categoryCode == 0) {
            int characterCode = findClassDefinition(nameConstant); if (characterCode < 0 || error || !initialize(characterCode, startingPoint)) return;
            categoryCode = 32 + characterCode; validLength = classSlotCount[characterCode];
        }
        int objectReference = allocateStorage(categoryCode, validLength); if (error) return;
        if (categoryCode == 13 && wordText(nameConstant, "English/Native/worker")) heapValue[objectReference + 3] = 1;
        if (categoryCode >= 24 && categoryCode <= 28 && koreanScreenClass(nameConstant) != 0) heapValue[objectReference + 13] = 1;
        if (categoryCode == 5 || categoryCode == 6 || categoryCode == 15 || categoryCode == 17 || categoryCode == 18) heapValue[objectReference + 2] = -1;
        if (categoryCode == 9) heapValue[objectReference + 2] = exceptionReference;
        putValue(objectReference, 2);
    }
    static boolean valuesEqual(int firstData, int byteData) {
        if (firstData == byteData) return true;
        if (firstData == 0 || byteData == 0 || firstData < 0 || byteData < 0 || firstData >= heapEndPosition || byteData >= heapEndPosition) return false;
        if (heapValue[firstData] == 1 && heapValue[byteData] == 1) return textsEqual(firstData, byteData, false);
        return heapValue[firstData] == 12 && heapValue[byteData] == 12 && heapValue[firstData + 2] == heapValue[byteData + 2];
    }
    static int textFragment(int objectReference, int startPosition, int endPosition) {
        if (!objectValue(objectReference, 1)) return 0;
        if (startPosition < 0 || endPosition < startPosition || endPosition > heapValue[objectReference + 1]) { failureValue("StringIndexOutOfBoundsException"); return 0; }
        int returnedValue = allocateStorage(1, endPosition - startPosition); if (error) return 0;
        for (int loopIndex = startPosition; loopIndex < endPosition; loopIndex++) heapValue[returnedValue + 2 + loopIndex - startPosition] = heapValue[objectReference + 2 + loopIndex];
        return returnedValue;
    }
    static int joinText(int firstData, int byteData) {
        if (!objectValue(firstData, 1) || !objectValue(byteData, 1)) return 0;
        int entryCount = heapValue[firstData + 1], methodIndex = heapValue[byteData + 1], returnedValue = allocateStorage(1, entryCount + methodIndex); if (error) return 0;
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) heapValue[returnedValue + 2 + loopIndex] = heapValue[firstData + 2 + loopIndex];
        for (int loopIndex = 0; loopIndex < methodIndex; loopIndex++) heapValue[returnedValue + 2 + entryCount + loopIndex] = heapValue[byteData + 2 + loopIndex];
        return returnedValue;
    }
    static boolean invokeDefault(int owner, int nameConstant, int descriptorConstant, int commandCode) {
        if (wordText(owner, "English/Native/Arguments") && commandCode == 184) {
            if (wordText(nameConstant, "itemCount") && wordText(descriptorConstant, "()I")) { putValue(User.argumentsCount() - 1, 1); return true; }
            if (wordText(nameConstant, "text") && wordText(descriptorConstant, "(I)Ljava/lang/String;")) {
                int ordinalIndex = subtractValues(1);
                if (ordinalIndex < 0 || ordinalIndex >= User.argumentsCount() - 1) throwException(29, "executeCommand arguments 범위를 벗어났습니다");
                else putValue(hostCharacter(User.arguments(ordinalIndex + 1)), 2);
                return true;
            }
            failureValue("지원하지 않는 English executeCommand arguments invoke"); return true;
        }
        if (wordText(owner, "English/Native/worker")) { processThread(nameConstant, descriptorConstant, commandCode, true); return true; }
        if (koreanScreenOwner(owner)) { invokeKoreanScreen(owner, nameConstant, descriptorConstant, commandCode); return true; }
        if (screenOwner(owner)) { invokeScreen(owner, nameConstant, descriptorConstant, commandCode); return true; }
        if (wordText(owner, "java/net/Socket") || wordText(owner, "java/net/ServerSocket") || wordText(owner, "java/io/InputStream") || wordText(owner, "java/io/OutputStream")) { invokeStream(owner, nameConstant, descriptorConstant, commandCode); return true; }
        if (wordText(owner, "English/Native/kernelValue") && commandCode == 184) {
            if (wordText(nameConstant, "screenWidth") && wordText(descriptorConstant, "()I")) { putValue(User.screenWidth(), 1); return true; }
            if (wordText(nameConstant, "screenHeight") && wordText(descriptorConstant, "()I")) { putValue(User.screenHeight(), 1); return true; }
            if (wordText(nameConstant, "milliseconds") && wordText(descriptorConstant, "()I")) { putValue(User.milliseconds(), 1); return true; }
            if (wordText(nameConstant, "waitForImage") && wordText(descriptorConstant, "()I")) { putValue(User.waitForImage(), 1); return true; }
            if (wordText(nameConstant, "rectangle") && wordText(descriptorConstant, "(IIIII)I")) { int pixelColour = subtractValues(1), heightValue = subtractValues(1), widthValue = subtractValues(1), yCoordinate = subtractValues(1), xCoordinate = subtractValues(1); putValue(User.rectangle(xCoordinate, yCoordinate, widthValue, heightValue, pixelColour), 1); return true; }
        }
        if (wordText(owner, "java/net/InetAddress") || wordText(owner, "java/net/DatagramPacket") || wordText(owner, "java/net/DatagramSocket")) { networkInvoke(owner, nameConstant, descriptorConstant, commandCode); return true; }
        if (wordText(owner, "java/lang/Thread")) { invokeThread(nameConstant, descriptorConstant, commandCode); return true; }
        if (wordText(owner, "java/lang/Object")) {
            if (wordText(nameConstant, "<init>") && wordText(descriptorConstant, "()V") && commandCode == 183) { isValidObject(subtractValues(2)); return true; }
            if (wordText(nameConstant, "equals") && wordText(descriptorConstant, "(Ljava/lang/Object;)Z")) { int byteData = subtractValues(2), firstData = subtractValues(2); if (isValidObject(firstData)) putValue(firstData == byteData ? 1 : 0, 1); return true; }
        }
        if (exceptionConstant(owner) != 0) {
            if (wordText(nameConstant, "<init>") && commandCode == 183 && (wordText(descriptorConstant, "()V") || wordText(descriptorConstant, "(Ljava/lang/String;)V"))) {
                int prompt = wordText(descriptorConstant, "()V") ? 0 : subtractValues(2), objectReference = subtractValues(2);
                if (objectValue(objectReference, 9)) { heapValue[objectReference + 3] = prompt; heapReference[objectReference + 3] = 1; } return true;
            }
            if ((wordText(nameConstant, "getMessage") || wordText(nameConstant, "description")) && wordText(descriptorConstant, "()Ljava/lang/String;")) { int objectReference = subtractValues(2); if (objectValue(objectReference, 9)) putValue(heapValue[objectReference + 3], 2); return true; }
        }
        if (wordText(owner, "java/lang/String")) {
            if (commandCode == 182 && wordText(nameConstant, "getBytes") && (wordText(descriptorConstant, "()[B") || wordText(descriptorConstant, "(Ljava/lang/String;)[B"))) {
                int encodingName = wordText(descriptorConstant, "()[B") ? 0 : subtractValues(2), objectReference = subtractValues(2);
                if (!objectValue(objectReference, 1)) return true;
                if (encodingName != 0 && !textsEqual(encodingName, hostCharacter("UTF-8"), false) && !textsEqual(encodingName, hostCharacter("UTF8"), false) && !textsEqual(encodingName, hostCharacter("utf-8"), false)) { throwException(11, "only UTF-8 encoding is supported"); return true; }
                int entryCount = heapValue[objectReference + 1], returnedValue = allocateStorage(20, entryCount * 3), usedCount = 0; if (error) return true;
                for (int innerPosition = 0; innerPosition < entryCount; innerPosition++) {
                    int characterCode = heapValue[objectReference + 2 + innerPosition];
                    if (characterCode >= 0xd800 && characterCode <= 0xdbff && innerPosition + 1 < entryCount && heapValue[objectReference + 3 + innerPosition] >= 0xdc00 && heapValue[objectReference + 3 + innerPosition] <= 0xdfff) characterCode = 0x10000 + ((characterCode - 0xd800) << 10) + heapValue[objectReference + 2 + ++innerPosition] - 0xdc00;
                    else if (characterCode >= 0xd800 && characterCode <= 0xdfff) characterCode = '?';
                    if (characterCode < 128) heapValue[returnedValue + 2 + usedCount++] = characterCode;
                    else { int byteCount = characterCode < 2048 ? 2 : characterCode < 65536 ? 3 : 4; heapValue[returnedValue + 2 + usedCount++] = (byte)((byteCount == 2 ? 192 : byteCount == 3 ? 224 : 240) | characterCode >> (6 * (byteCount - 1))); for (int comparisonPosition = byteCount - 1; comparisonPosition > 0; comparisonPosition--) heapValue[returnedValue + 2 + usedCount++] = (byte)(128 | characterCode >> (6 * (comparisonPosition - 1)) & 63); }
                }
                heapValue[returnedValue + 1] = usedCount; putValue(returnedValue, 2); return true;
            }
            if (commandCode == 184 && wordText(nameConstant, "valueOf") && wordText(descriptorConstant, "(I)Ljava/lang/String;")) { putValue(digitCharacter(subtractValues(1)), 2); return true; }
            if (commandCode != 182) return false;
            if (wordText(nameConstant, "equals") && wordText(descriptorConstant, "(Ljava/lang/Object;)Z")) { int byteData = subtractValues(2), firstData = subtractValues(2); if (objectValue(firstData, 1)) putValue(textsEqual(firstData, byteData, false) ? 1 : 0, 1); return true; }
            if (wordText(nameConstant, "isEmpty") && wordText(descriptorConstant, "()Z")) { int firstData = subtractValues(2); if (objectValue(firstData, 1)) putValue(heapValue[firstData + 1] == 0 ? 1 : 0, 1); return true; }
            if (wordText(nameConstant, "substring") && (wordText(descriptorConstant, "(I)Ljava/lang/String;") || wordText(descriptorConstant, "(II)Ljava/lang/String;"))) {
                boolean secondValue = wordText(descriptorConstant, "(II)Ljava/lang/String;"); int endPosition = secondValue ? subtractValues(1) : 0, startingPoint = subtractValues(1), firstData = subtractValues(2);
                if (objectValue(firstData, 1)) putValue(textFragment(firstData, startingPoint, secondValue ? endPosition : heapValue[firstData + 1]), 2); return true;
            }
            if (wordText(nameConstant, "concat") && wordText(descriptorConstant, "(Ljava/lang/String;)Ljava/lang/String;")) { int byteData = subtractValues(2), firstData = subtractValues(2); putValue(joinText(firstData, byteData), 2); return true; }
            if (wordText(nameConstant, "hashCode") && wordText(descriptorConstant, "()I")) { int firstData = subtractValues(2), hashValue = 0; if (objectValue(firstData, 1)) { for (int loopIndex = 0; loopIndex < heapValue[firstData + 1]; loopIndex++) hashValue = hashValue * 31 + heapValue[firstData + 2 + loopIndex]; putValue(hashValue, 1); } return true; }
            if (wordText(nameConstant, "toString") && wordText(descriptorConstant, "()Ljava/lang/String;")) { int firstData = subtractValues(2); if (objectValue(firstData, 1)) putValue(firstData, 2); return true; }
        }
        if (wordText(owner, "java/lang/Integer")) {
            if (commandCode == 184 && wordText(nameConstant, "valueOf") && wordText(descriptorConstant, "(I)Ljava/lang/Integer;")) { int dataValue = subtractValues(1), objectReference = dataValue >= -128 && dataValue <= 127 ? storeInteger[dataValue + 128] : 0; if (objectReference == 0) { objectReference = allocateStorage(12, 1); if (!error) { heapValue[objectReference + 2] = dataValue; if (dataValue >= -128 && dataValue <= 127) storeInteger[dataValue + 128] = objectReference; } } putValue(objectReference, 2); return true; }
            if (commandCode == 183 && wordText(nameConstant, "<init>") && wordText(descriptorConstant, "(I)V")) { int dataValue = subtractValues(1), objectReference = subtractValues(2); if (objectValue(objectReference, 12)) heapValue[objectReference + 2] = dataValue; return true; }
            if (commandCode == 182 && wordText(nameConstant, "intValue") && wordText(descriptorConstant, "()I")) { int objectReference = subtractValues(2); if (objectValue(objectReference, 12)) putValue(heapValue[objectReference + 2], 1); return true; }
            if (commandCode == 184 && wordText(nameConstant, "toString") && wordText(descriptorConstant, "(I)Ljava/lang/String;")) { putValue(digitCharacter(subtractValues(1)), 2); return true; }
        }
        if (wordText(owner, "java/lang/Math") && commandCode == 184) {
            if (wordText(nameConstant, "abs") && wordText(descriptorConstant, "(I)I")) { int readValue = subtractValues(1); putValue(readValue < 0 ? -readValue : readValue, 1); return true; }
            if ((wordText(nameConstant, "min") || wordText(nameConstant, "max")) && wordText(descriptorConstant, "(II)I")) { int byteData = subtractValues(1), firstData = subtractValues(1); putValue(wordText(nameConstant, "min") ? (firstData < byteData ? firstData : byteData) : (firstData > byteData ? firstData : byteData), 1); return true; }
        }
        if (wordText(owner, "java/lang/System") && commandCode == 184) {
            if (wordText(nameConstant, "gc") && wordText(descriptorConstant, "()V")) { collectGarbage(); return true; }
            if (wordText(nameConstant, "arraycopy") && wordText(descriptorConstant, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int entryCount = subtractValues(1), destinationValueIndex = subtractValues(1), byteData = subtractValues(2), startPosition = subtractValues(1), firstData = subtractValues(2);
                if (isValidObject(firstData) && isValidObject(byteData)) {
                    int categoryCode = heapValue[firstData];
                    if (heapValue[byteData] != categoryCode || (categoryCode != 2 && categoryCode != 3 && (categoryCode < 20 || categoryCode > 23))) failureValue("arraycopy type mismatch");
                    else if (entryCount < 0 || startPosition < 0 || destinationValueIndex < 0 || startPosition > heapValue[firstData + 1] - entryCount || destinationValueIndex > heapValue[byteData + 1] - entryCount) failureValue("ArrayIndexOutOfBoundsException");
                    else if (firstData == byteData && destinationValueIndex > startPosition) { for (int loopIndex = entryCount - 1; loopIndex >= 0; loopIndex--) heapValue[byteData + 2 + destinationValueIndex + loopIndex] = heapValue[firstData + 2 + startPosition + loopIndex]; }
                    else { for (int loopIndex = 0; loopIndex < entryCount && !error; loopIndex++) { int dataValue = heapValue[firstData + 2 + startPosition + loopIndex]; if (categoryCode != 3 || canStoreArray(byteData, dataValue)) heapValue[byteData + 2 + destinationValueIndex + loopIndex] = dataValue; } }
                }
                return true;
            }
        }
        if (wordText(owner, "java/util/ArrayList") || wordText(owner, "java/util/List") || wordText(owner, "java/util/HashMap") || wordText(owner, "java/util/Map")) {
            invokeCollection(owner, nameConstant, descriptorConstant, commandCode); return true;
        }
        return false;
    }
    static void extendCollection(int objectReference, int requiredCount) {
        int previousValue = heapValue[objectReference + 2], capacityData = previousValue == 0 ? 0 : heapValue[previousValue + 1];
        if (capacityData >= requiredCount) return;
        int nextPosition = capacityData < 8 ? 8 : capacityData * 2; if (nextPosition < requiredCount) nextPosition = requiredCount;
        int dataArray = allocateStorage(3, nextPosition); if (error) return;
        for (int loopIndex = 0; loopIndex < capacityData; loopIndex++) heapValue[dataArray + 2 + loopIndex] = heapValue[previousValue + 2 + loopIndex];
        heapValue[objectReference + 2] = dataArray; heapReference[objectReference + 2] = 1;
    }
    static void invokeCollection(int owner, int nameConstant, int descriptorConstant, int commandCode) {
        boolean mappedReference = wordText(owner, "java/util/HashMap") || wordText(owner, "java/util/Map"); int categoryCode = mappedReference ? 11 : 10;
        if (wordText(nameConstant, "<init>") && commandCode == 183 && wordText(descriptorConstant, "()V")) { int objectReference = subtractValues(2); if (objectValue(objectReference, categoryCode)) extendCollection(objectReference, 8); return; }
        if (commandCode != 182 && commandCode != 185) { failureValue("invalid collection invocation"); return; }
        if (wordText(nameConstant, "size") && wordText(descriptorConstant, "()I") || wordText(nameConstant, "isEmpty") && wordText(descriptorConstant, "()Z")) {
            int objectReference = subtractValues(2); if (objectValue(objectReference, categoryCode)) putValue(wordText(nameConstant, "size") ? heapValue[objectReference + 3] : heapValue[objectReference + 3] == 0 ? 1 : 0, 1); return;
        }
        if (wordText(nameConstant, "clear") && wordText(descriptorConstant, "()V")) { int objectReference = subtractValues(2); if (objectValue(objectReference, categoryCode)) { int dataArray = heapValue[objectReference + 2]; for (int loopIndex = 0; loopIndex < heapValue[dataArray + 1]; loopIndex++) heapValue[dataArray + 2 + loopIndex] = 0; heapValue[objectReference + 3] = 0; } return; }
        if (!mappedReference && wordText(nameConstant, "add") && wordText(descriptorConstant, "(Ljava/lang/Object;)Z")) {
            int dataValue = subtractValues(2), objectReference = subtractValues(2); if (!objectValue(objectReference, 10)) return;
            int entryCount = heapValue[objectReference + 3]; extendCollection(objectReference, entryCount + 1); if (!error) { heapValue[heapValue[objectReference + 2] + 2 + entryCount] = dataValue; heapValue[objectReference + 3] = entryCount + 1; putValue(1, 1); } return;
        }
        if (!mappedReference && (wordText(nameConstant, "get") || wordText(nameConstant, "remove")) && wordText(descriptorConstant, "(I)Ljava/lang/Object;") || !mappedReference && wordText(nameConstant, "set") && wordText(descriptorConstant, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean isAssigned = wordText(nameConstant, "set"); int dataValue = isAssigned ? subtractValues(2) : 0, entryPosition = subtractValues(1), objectReference = subtractValues(2);
            if (!objectValue(objectReference, 10)) return;
            int entryCount = heapValue[objectReference + 3], dataArray = heapValue[objectReference + 2];
            if (entryPosition < 0 || entryPosition >= entryCount) { throwException(6, "list index"); return; }
            int previousValue = heapValue[dataArray + 2 + entryPosition];
            if (isAssigned) heapValue[dataArray + 2 + entryPosition] = dataValue;
            if (wordText(nameConstant, "remove")) { for (int loopIndex = entryPosition + 1; loopIndex < entryCount; loopIndex++) heapValue[dataArray + 1 + loopIndex] = heapValue[dataArray + 2 + loopIndex]; heapValue[dataArray + 1 + entryCount] = 0; heapValue[objectReference + 3] = entryCount - 1; }
            putValue(previousValue, 2); return;
        }
        if (mappedReference && (wordText(nameConstant, "get") || wordText(nameConstant, "remove")) && wordText(descriptorConstant, "(Ljava/lang/Object;)Ljava/lang/Object;") || mappedReference && wordText(nameConstant, "put") && wordText(descriptorConstant, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || mappedReference && wordText(nameConstant, "containsKey") && wordText(descriptorConstant, "(Ljava/lang/Object;)Z")) {
            boolean isInsertion = wordText(nameConstant, "put"), remove = wordText(nameConstant, "remove");
            int dataValue = isInsertion ? subtractValues(2) : 0, keyReference = subtractValues(2), objectReference = subtractValues(2); if (!objectValue(objectReference, 11)) return;
            int entryCount = heapValue[objectReference + 3], dataArray = heapValue[objectReference + 2], wasFound = -1;
            for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) if (valuesEqual(keyReference, heapValue[dataArray + 2 + 2 * loopIndex])) { wasFound = loopIndex; break; }
            int previousValue = wasFound < 0 ? 0 : heapValue[dataArray + 3 + 2 * wasFound];
            if (isInsertion) {
                if (wasFound < 0) { extendCollection(objectReference, (entryCount + 1) * 2); dataArray = heapValue[objectReference + 2]; wasFound = entryCount; if (!error) heapValue[objectReference + 3] = entryCount + 1; }
                if (!error) { heapValue[dataArray + 2 + 2 * wasFound] = keyReference; heapValue[dataArray + 3 + 2 * wasFound] = dataValue; }
            }
            if (remove && wasFound >= 0) { for (int loopIndex = wasFound + 1; loopIndex < entryCount; loopIndex++) { heapValue[dataArray + 2 * loopIndex] = heapValue[dataArray + 2 + 2 * loopIndex]; heapValue[dataArray + 1 + 2 * loopIndex] = heapValue[dataArray + 3 + 2 * loopIndex]; } heapValue[dataArray + 2 * entryCount] = 0; heapValue[dataArray + 1 + 2 * entryCount] = 0; heapValue[objectReference + 3] = entryCount - 1; }
            if (wordText(nameConstant, "containsKey")) putValue(wasFound >= 0 ? 1 : 0, 1); else putValue(previousValue, 2);
            return;
        }
        failureValue("unsupported collection method");
    }
    static boolean acquireLock(int objectReference) {
        if (!isValidObject(objectReference)) return false;
        if (lockDepth[objectReference] != 0 && lockOwner[objectReference] != currentThread + 1) { changeRequest = true; return false; }
        lockOwner[objectReference] = currentThread + 1; lockDepth[objectReference]++; return true;
    }
    static void releaseLock(int objectReference) {
        if (!isValidObject(objectReference)) return;
        if (lockDepth[objectReference] == 0 || lockOwner[objectReference] != currentThread + 1) { throwException(13, "monitor not owned"); return; }
        if (--lockDepth[objectReference] == 0) lockOwner[objectReference] = 0;
    }
    static boolean switchThread() {
        threadFrame[currentThread] = frameIndex;
        if (frameIndex < currentThread * 32) threadState[currentThread] = 3;
        for (int loopIndex = 0; loopIndex < threadCount; loopIndex++) if (threadState[loopIndex] == 2 && threadState[waitForThread[loopIndex]] == 3) threadState[loopIndex] = 1;
        for (int loopIndex = 1; loopIndex <= threadCount; loopIndex++) {
            int nextPosition = (currentThread + loopIndex) % threadCount;
            if (threadState[nextPosition] == 1) { currentThread = nextPosition; frameIndex = threadFrame[nextPosition]; changeRequest = false; return true; }
        }
        for (int loopIndex = 0; loopIndex < threadCount; loopIndex++) if (threadState[loopIndex] != 3) { failureValue("thread deadlock"); return false; }
        return false;
    }
    static void invokeThread(int nameConstant, int descriptorConstant, int commandCode) { processThread(nameConstant, descriptorConstant, commandCode, false); }
    static void processThread(int nameConstant, int descriptorConstant, int commandCode, boolean English) {
        if (commandCode == 184 && wordText(nameConstant, English ? "yieldTask" : "yield") && wordText(descriptorConstant, "()V")) { changeRequest = true; return; }
        if (commandCode == 184 && wordText(nameConstant, "currentThread") && wordText(descriptorConstant, "()Ljava/lang/Thread;")) { putValue(threadObject[currentThread], 2); return; }
        if (commandCode == 183 && wordText(nameConstant, "<init>") && (wordText(descriptorConstant, "()V") || wordText(descriptorConstant, English ? "(LEnglish/Native/RunnableTask;)V" : "(Ljava/lang/Runnable;)V"))) {
            int targetAddress = wordText(descriptorConstant, "()V") ? 0 : subtractValues(2), objectReference = subtractValues(2);
            if (!isValidObject(objectReference)) return;
            if (heapValue[objectReference] == 13) { heapValue[objectReference + 2] = targetAddress; heapReference[objectReference + 2] = 1; }
            else if (targetAddress != 0) failureValue("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (commandCode == 182 && (wordText(nameConstant, English ? "startTask" : "start") || wordText(nameConstant, English ? "await" : "join")) && wordText(descriptorConstant, "()V") || commandCode == 182 && wordText(nameConstant, English ? "isAlive" : "isAlive") && wordText(descriptorConstant, "()Z")) {
            int objectReference = subtractValues(2); if (!isValidObject(objectReference)) return;
            int identityValue = -1; for (int loopIndex = 0; loopIndex < threadCount; loopIndex++) if (threadObject[loopIndex] == objectReference) identityValue = loopIndex;
            if (wordText(nameConstant, English ? "isAlive" : "isAlive")) { putValue(identityValue >= 0 && threadState[identityValue] != 3 ? 1 : 0, 1); return; }
            if (wordText(nameConstant, English ? "await" : "join")) { if (identityValue >= 0 && threadState[identityValue] != 3) { waitForThread[currentThread] = identityValue; threadState[currentThread] = 2; changeRequest = true; } return; }
            if (identityValue >= 0) { throwException(English ? 38 : 16, "thread already started"); return; }
            if (threadCount == 4) { failureValue("thread limit (4 including main)"); return; }
            int targetAddress = heapValue[objectReference] == 13 ? heapValue[objectReference + 2] : objectReference;
            int fileIndex = targetAddress > 0 && heapValue[targetAddress] >= 32 ? nameMethod(heapValue[targetAddress] - 32, English ? "executeTask" : "run", "()V") : -1;
            if (targetAddress != 0 && fileIndex < 0) { failureValue("Runnable.run required"); return; }
            identityValue = threadCount++; threadObject[identityValue] = objectReference; threadTarget[identityValue] = targetAddress;
            int frame = identityValue * 32; threadFrame[identityValue] = fileIndex < 0 ? frame - 1 : frame; threadState[identityValue] = fileIndex < 0 ? 3 : 1;
            if (fileIndex >= 0) { frameMethod[frame] = fileIndex; framePosition[frame] = methodStart[fileIndex]; localValue[frame * 128] = targetAddress; localType[frame * 128] = 2; }
            return;
        }
        failureValue("unsupported Thread method");
    }
    static int[] networkTemporaryValue = new int[514], addressText = new int[16];
    static int localAddress() { return addressObject(0x7f000001); }
    static int addressObject(int value) { int objectReference = allocateStorage(14, 1); if (!error) heapValue[objectReference + 2] = value; return objectReference; }
    static int decodeAddress(int objectReference) {
        if (objectReference == 0 || textsEqual(objectReference, hostCharacter("localhost"), false)) return 0x7f000001;
        if (!objectValue(objectReference, 1)) return 0;
        int dataValue = 0, totalCount = 0, addressByte = 0, digits = 0, entryCount = heapValue[objectReference + 1];
        for (int loopIndex = 0; loopIndex <= entryCount; loopIndex++) {
            int characterCode = loopIndex == entryCount ? '.' : heapValue[objectReference + 2 + loopIndex];
            if (characterCode == '.') { if (digits == 0 || totalCount == 4) { throwException(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dataValue = dataValue << 8 | addressByte; totalCount++; addressByte = digits = 0; }
            else { if (characterCode < '0' || characterCode > '9' || ++digits > 3 || (addressByte = addressByte * 10 + characterCode - '0') > 255) { throwException(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (totalCount != 4) { throwException(18, "invalid IPv4 address"); return 0; } return dataValue;
    }
    static int addressCharacter(int dataValue) {
        int entryCount = 0;
        for (int shift = 24; shift >= 0; shift -= 8) {
            int addressByte = dataValue >>> shift & 255;
            if (addressByte >= 100) addressText[entryCount++] = '0' + addressByte / 100;
            if (addressByte >= 10) addressText[entryCount++] = '0' + addressByte / 10 % 10;
            addressText[entryCount++] = '0' + addressByte % 10; if (shift != 0) addressText[entryCount++] = '.';
        }
        int objectReference = allocateStorage(1, entryCount); if (!error) for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) heapValue[objectReference + 2 + loopIndex] = addressText[loopIndex]; return objectReference;
    }
    static void networkInvoke(int owner, int nameConstant, int descriptorConstant, int commandCode) {
        if (wordText(owner, "java/net/InetAddress")) {
            if (commandCode == 184 && wordText(nameConstant, "getLoopbackAddress") && wordText(descriptorConstant, "()Ljava/net/InetAddress;")) { putValue(localAddress(), 2); return; }
            if (commandCode == 184 && wordText(nameConstant, "getByName") && wordText(descriptorConstant, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dataValue = decodeAddress(subtractValues(2)); if (thrownObject == 0 && !error) putValue(addressObject(dataValue), 2); return;
            }
            if (commandCode == 182 && wordText(nameConstant, "getHostAddress") && wordText(descriptorConstant, "()Ljava/lang/String;")) { int objectReference = subtractValues(2); if (objectValue(objectReference, 14)) putValue(addressCharacter(heapValue[objectReference + 2]), 2); return; }
        }
        if (wordText(owner, "java/net/DatagramPacket")) {
            if (commandCode == 183 && wordText(nameConstant, "<init>") && (wordText(descriptorConstant, "([BI)V") || wordText(descriptorConstant, "([BILjava/net/InetAddress;I)V"))) {
                boolean destinationValueReference = wordText(descriptorConstant, "([BILjava/net/InetAddress;I)V"); int portNumber = destinationValueReference ? subtractValues(1) : 0, addressReference = destinationValueReference ? subtractValues(2) : 0;
                int entryCount = subtractValues(1), dataArray = subtractValues(2), objectReference = subtractValues(2);
                if (!objectValue(objectReference, 16) || !objectValue(dataArray, 20)) return;
                if (entryCount < 0 || entryCount > heapValue[dataArray + 1] || portNumber < 0 || portNumber > 65535) { throwException(9, "invalid datagram length/port"); return; }
                if (addressReference != 0 && !objectValue(addressReference, 14)) return;
                heapValue[objectReference + 2] = dataArray; heapReference[objectReference + 2] = 1; heapValue[objectReference + 3] = entryCount;
                heapValue[objectReference + 4] = addressReference; heapReference[objectReference + 4] = 1; heapValue[objectReference + 5] = portNumber; return;
            }
            if (commandCode == 182 && wordText(nameConstant, "setLength") && wordText(descriptorConstant, "(I)V")) {
                int entryCount = subtractValues(1), objectReference = subtractValues(2); if (!objectValue(objectReference, 16)) return;
                if (entryCount < 0 || entryCount > heapValue[heapValue[objectReference + 2] + 1]) throwException(9, "invalid datagram length"); else heapValue[objectReference + 3] = entryCount; return;
            }
            if (commandCode == 182 && (wordText(nameConstant, "getData") && wordText(descriptorConstant, "()[B") || wordText(nameConstant, "getLength") && wordText(descriptorConstant, "()I") || wordText(nameConstant, "getAddress") && wordText(descriptorConstant, "()Ljava/net/InetAddress;") || wordText(nameConstant, "getPort") && wordText(descriptorConstant, "()I"))) {
                int objectReference = subtractValues(2); if (!objectValue(objectReference, 16)) return;
                int entryPosition = wordText(nameConstant, "getData") ? 2 : wordText(nameConstant, "getLength") ? 3 : wordText(nameConstant, "getAddress") ? 4 : 5;
                putValue(heapValue[objectReference + entryPosition], entryPosition == 2 || entryPosition == 4 ? 2 : 1); return;
            }
        }
        if (wordText(owner, "java/net/DatagramSocket")) {
            if (commandCode == 183 && wordText(nameConstant, "<init>") && (wordText(descriptorConstant, "()V") || wordText(descriptorConstant, "(I)V"))) {
                int portNumber = wordText(descriptorConstant, "()V") ? 0 : subtractValues(1), objectReference = subtractValues(2); if (!objectValue(objectReference, 15)) return;
                if (portNumber < 0 || portNumber > 65535) { throwException(9, "invalid port"); return; }
                int openedFileNumber = User.openNetwork(portNumber); if (openedFileNumber < 0) throwException(39, "UDP socket/bind failed"); else heapValue[objectReference + 2] = openedFileNumber; return;
            }
            if (commandCode == 182 && wordText(nameConstant, "setSoTimeout") && wordText(descriptorConstant, "(I)V")) {
                int millisecondsValue = subtractValues(1), objectReference = subtractValues(2); if (!objectValue(objectReference, 15)) return;
                if (millisecondsValue < 0) throwException(9, "negative timeout"); else heapValue[objectReference + 3] = millisecondsValue; return;
            }
            if (commandCode == 182 && wordText(nameConstant, "getLocalPort") && wordText(descriptorConstant, "()I")) { int objectReference = subtractValues(2); if (objectValue(objectReference, 15)) putValue(heapValue[objectReference + 2] < 0 ? -1 : User.networkPort(heapValue[objectReference + 2]), 1); return; }
            if (commandCode == 182 && wordText(nameConstant, "isClosed") && wordText(descriptorConstant, "()Z")) { int objectReference = subtractValues(2); if (objectValue(objectReference, 15)) putValue(heapValue[objectReference + 2] < 0 ? 1 : 0, 1); return; }
            if (commandCode == 182 && wordText(nameConstant, "close") && wordText(descriptorConstant, "()V")) { int objectReference = subtractValues(2); if (objectValue(objectReference, 15) && heapValue[objectReference + 2] >= 0) { User.closeFileDescriptor(heapValue[objectReference + 2]); heapValue[objectReference + 2] = -1; } return; }
            if (commandCode == 182 && (wordText(nameConstant, "send") || wordText(nameConstant, "receive")) && wordText(descriptorConstant, "(Ljava/net/DatagramPacket;)V")) {
                int packet = subtractValues(2), objectReference = subtractValues(2); if (!objectValue(packet, 16) || !objectValue(objectReference, 15)) return;
                int dataArray = heapValue[packet + 2], validLength = heapValue[packet + 3], openedFileNumber = heapValue[objectReference + 2];
                if (openedFileNumber < 0) { throwException(39, "socket closed"); return; }
                if (wordText(nameConstant, "send")) {
                    if (!objectValue(heapValue[packet + 4], 14)) return;
                    if (validLength > 512) { throwException(11, "datagram limit (512 bytes)"); return; }
                    for (int loopIndex = 0; loopIndex < validLength; loopIndex++) networkTemporaryValue[loopIndex] = heapValue[dataArray + 2 + loopIndex];
                    if (User.sendNetwork(openedFileNumber, heapValue[heapValue[packet + 4] + 2], heapValue[packet + 5], networkTemporaryValue, validLength) < 0) throwException(11, "UDP send failed");
                } else {
                    int entryCount = User.receiveNetwork(openedFileNumber, networkTemporaryValue, validLength > 512 ? 512 : validLength);
                    if (entryCount == -11) {
                        int currentTime = User.milliseconds();
                        if (heapValue[objectReference + 4] == 0) heapValue[objectReference + 4] = currentTime + 1;
                        if (heapValue[objectReference + 3] > 0 && currentTime - (heapValue[objectReference + 4] - 1) >= heapValue[objectReference + 3]) { heapValue[objectReference + 4] = 0; throwException(19, "receive timed out"); return; }
                        putValue(objectReference, 2); putValue(packet, 2); framePosition[frameIndex] = frameInstruction[frameIndex]; changeRequest = true; return;
                    }
                    heapValue[objectReference + 4] = 0;
                    if (entryCount < 0) { throwException(11, "UDP receive failed"); return; }
                    for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) heapValue[dataArray + 2 + loopIndex] = (byte)networkTemporaryValue[loopIndex];
                    heapValue[packet + 3] = entryCount; heapValue[packet + 4] = addressObject(networkTemporaryValue[513]); heapReference[packet + 4] = 1; heapValue[packet + 5] = networkTemporaryValue[512];
                }
                return;
            }
        }
        failureValue("unsupported java.net method");
    }
    static boolean waitForStream(int objectReference) {
        int currentTime = User.milliseconds();
        if (heapValue[objectReference + 5] == 0) heapValue[objectReference + 5] = currentTime + 1;
        if (heapValue[objectReference + 3] > 0 && currentTime - (heapValue[objectReference + 5] - 1) >= heapValue[objectReference + 3]) { heapValue[objectReference + 5] = 0; throwException(19, "stream wait timed out"); return false; }
        framePosition[frameIndex] = frameInstruction[frameIndex]; changeRequest = true; return true;
    }
    static void invokeStream(int owner, int nameConstant, int descriptorConstant, int commandCode) {
        boolean receivePage = wordText(owner, "java/net/ServerSocket"), stream = wordText(owner, "java/io/InputStream") || wordText(owner, "java/io/OutputStream");
        if (!stream && commandCode == 183 && wordText(nameConstant, "<init>")) {
            boolean isEmptyState = wordText(descriptorConstant, "()V"), named = wordText(descriptorConstant, "(Ljava/lang/String;I)V"), addressed = wordText(descriptorConstant, "(Ljava/net/InetAddress;I)V");
            if (!(isEmptyState || receivePage && wordText(descriptorConstant, "(I)V") || !receivePage && (named || addressed))) { failureValue("unsupported socket constructor"); return; }
            int portNumber = isEmptyState ? 0 : subtractValues(1), addressReference = named || addressed ? subtractValues(2) : 0, objectReference = subtractValues(2);
            if (!objectValue(objectReference, receivePage ? 18 : 17)) return;
            if (portNumber < 0 || portNumber > 65535) { throwException(9, "invalid port"); return; }
            if (addressed && !objectValue(addressReference, 14)) return;
            int networkAddress = named ? decodeAddress(addressReference) : addressed ? heapValue[addressReference + 2] : 0x7f000001;
            if (error || thrownObject != 0) return;
            int openedFileNumber = User.streamControl(0, 0, 0); if (openedFileNumber < 0) { throwException(39, "socket slots exhausted"); return; }
            int processedValue = isEmptyState ? 0 : receivePage ? User.streamControl(1, openedFileNumber, portNumber) : User.connectStream(openedFileNumber, networkAddress, portNumber);
            if (processedValue < 0) { User.closeFileDescriptor(openedFileNumber); throwException(39, "socket bind/connect failed"); return; }
            heapValue[objectReference + 2] = openedFileNumber; heapValue[objectReference + 4] = portNumber; heapValue[objectReference + 6] = isEmptyState ? 0 : 1; return;
        }
        if (!stream && wordText(nameConstant, "setSoTimeout") && wordText(descriptorConstant, "(I)V")) { int millisecondsValue = subtractValues(1), objectReference = subtractValues(2); if (!objectValue(objectReference, receivePage ? 18 : 17)) return; if (millisecondsValue < 0) throwException(9, "negative timeout"); else heapValue[objectReference + 3] = millisecondsValue; return; }
        if (!stream && wordText(nameConstant, "close") && wordText(descriptorConstant, "()V")) { int objectReference = subtractValues(2); if (objectValue(objectReference, receivePage ? 18 : 17) && heapValue[objectReference + 2] >= 0) { User.closeFileDescriptor(heapValue[objectReference + 2]); heapValue[objectReference + 2] = -1; } return; }
        if (!stream && (wordText(nameConstant, "getLocalPort") || wordText(nameConstant, "getPort") || wordText(nameConstant, "isClosed") || wordText(nameConstant, "isConnected"))) {
            int objectReference = subtractValues(2); if (!objectValue(objectReference, receivePage ? 18 : 17)) return;
            putValue(wordText(nameConstant, "isClosed") ? heapValue[objectReference + 2] < 0 ? 1 : 0 : wordText(nameConstant, "isConnected") ? heapValue[objectReference + 6] : wordText(nameConstant, "getPort") ? heapValue[objectReference + 4] : heapValue[objectReference + 2] < 0 ? -1 : User.streamControl(4, heapValue[objectReference + 2], 0), 1); return;
        }
        if (receivePage && wordText(nameConstant, "accept") && wordText(descriptorConstant, "()Ljava/net/Socket;")) {
            int objectReference = subtractValues(2); if (!objectValue(objectReference, 18)) return; int openedFileNumber = User.streamControl(3, heapValue[objectReference + 2], 0);
            if (openedFileNumber == -11) { if (waitForStream(objectReference)) putValue(objectReference, 2); return; }
            heapValue[objectReference + 5] = 0; if (openedFileNumber < 0) { throwException(11, "accept failed"); return; }
            int returnedValue = allocateStorage(17, 5); if (error) { User.closeFileDescriptor(openedFileNumber); return; } heapValue[returnedValue + 2] = openedFileNumber; heapValue[returnedValue + 4] = User.streamControl(5, openedFileNumber, 0); heapValue[returnedValue + 6] = 1; putValue(returnedValue, 2); return;
        }
        if (!receivePage && !stream && ((wordText(nameConstant, "getInputStream") && wordText(descriptorConstant, "()Ljava/io/InputStream;")) || (wordText(nameConstant, "getOutputStream") && wordText(descriptorConstant, "()Ljava/io/OutputStream;")))) {
            int objectReference = subtractValues(2); if (!objectValue(objectReference, 17)) return; if (heapValue[objectReference + 2] < 0 || heapValue[objectReference + 6] == 0) { throwException(39, "socket is not connected"); return; }
            int returnedValue = allocateStorage(19, 4); if (error) return; heapValue[returnedValue + 2] = objectReference; heapReference[returnedValue + 2] = 1; heapValue[returnedValue + 3] = wordText(nameConstant, "getInputStream") ? 0 : 1; putValue(returnedValue, 2); return;
        }
        if (stream) {
            boolean hasRead = wordText(nameConstant, "read"), isWriteOperation = wordText(nameConstant, "write"), block = wordText(descriptorConstant, "([B)I") || wordText(descriptorConstant, "([B)V"), isSubarray = wordText(descriptorConstant, "([BII)I") || wordText(descriptorConstant, "([BII)V");
            int entryCount = isSubarray ? subtractValues(1) : 0, startDisplacement = isSubarray ? subtractValues(1) : 0, dataArray = block || isSubarray ? subtractValues(2) : 0;
            int dataValue = isWriteOperation && wordText(descriptorConstant, "(I)V") ? subtractValues(1) : 0, objectReference = subtractValues(2);
            if (!objectValue(objectReference, 19)) return; int parentReference = heapValue[objectReference + 2], openedFileNumber = heapValue[parentReference + 2];
            if (openedFileNumber < 0) { throwException(11, "stream closed"); return; }
            if (wordText(nameConstant, "close") && wordText(descriptorConstant, "()V")) { User.closeFileDescriptor(openedFileNumber); heapValue[parentReference + 2] = -1; return; }
            if (wordText(nameConstant, "flush") && wordText(descriptorConstant, "()V")) return;
            if ((!hasRead && !isWriteOperation) || hasRead != (heapValue[objectReference + 3] == 0)) { failureValue("unsupported stream operation"); return; }
            if (block || isSubarray) { if (!objectValue(dataArray, 20)) return; if (block) entryCount = heapValue[dataArray + 1]; if (startDisplacement < 0 || entryCount < 0 || startDisplacement > heapValue[dataArray + 1] - entryCount) { throwException(6, "stream array bounds"); return; } }
            else entryCount = 1;
            if (entryCount == 0) { if (hasRead) putValue(0, 1); return; }
            int completedCount = isWriteOperation ? heapValue[objectReference + 4] : 0, processedValue = 0;
            while (completedCount < entryCount) {
                processedValue = hasRead ? User.readOneFileByte(openedFileNumber) : User.writeOneFileByte(openedFileNumber, block || isSubarray ? heapValue[dataArray + 2 + startDisplacement + completedCount] : dataValue);
                if (processedValue < 0 || hasRead && processedValue == 256) break;
                if (hasRead && (block || isSubarray)) heapValue[dataArray + 2 + startDisplacement + completedCount] = (byte)processedValue;
                completedCount++; if (hasRead && !(block || isSubarray)) break;
            }
            if (processedValue == -11 && (isWriteOperation || completedCount == 0)) {
                heapValue[objectReference + 4] = completedCount;
                if (waitForStream(parentReference)) { putValue(objectReference, 2); if (block || isSubarray) putValue(dataArray, 2); if (isSubarray) { putValue(startDisplacement, 1); putValue(entryCount, 1); } if (isWriteOperation && !(block || isSubarray)) putValue(dataValue, 1); } return;
            }
            heapValue[objectReference + 4] = 0; heapValue[parentReference + 5] = 0;
            if (processedValue < 0 && processedValue != -11) { throwException(11, "stream I/O failed"); return; }
            if (hasRead) putValue(completedCount == 0 && processedValue == 256 ? -1 : block || isSubarray ? completedCount : processedValue, 1); return;
        }
        failureValue("unsupported Socket/ServerSocket method");
    }
    static int[] screenReference = new int[32], temporaryScreenText = new int[256], scheduleLater = new int[8];
    static int laterCount;
    static int[] laterKoreanValue = new int[8];
    static boolean isHandlingEvent;
    static int koreanScreenClass(int nameConstant) {
        if (wordText(nameConstant, "English/Native/window")) return 24;
        if (wordText(nameConstant, "English/Native/label")) return 26;
        if (wordText(nameConstant, "English/Native/button")) return 27;
        if (wordText(nameConstant, "English/Native/TextField")) return 28;
        if (wordText(nameConstant, "English/Native/ActionNotice")) return 29;
        return 0;
    }
    static boolean koreanScreenOwner(int nameConstant) {
        return koreanScreenClass(nameConstant) != 0 || wordText(nameConstant, "English/Native/ScreenElement") || wordText(nameConstant, "English/Native/EventQueue");
    }
    static int screenClass(int nameConstant) {
        int KoreanClass = koreanScreenClass(nameConstant); if (KoreanClass != 0) return KoreanClass;
        if (wordText(nameConstant, "javax/swing/JFrame")) return 24;
        if (wordText(nameConstant, "javax/swing/JPanel")) return 25;
        if (wordText(nameConstant, "javax/swing/JLabel")) return 26;
        if (wordText(nameConstant, "javax/swing/JButton")) return 27;
        if (wordText(nameConstant, "javax/swing/JTextField")) return 28;
        if (wordText(nameConstant, "java/awt/event/ActionEvent")) return 29;
        if (wordText(nameConstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean screenOwner(int nameConstant) {
        return screenClass(nameConstant) != 0 || wordText(nameConstant, "java/awt/Component") || wordText(nameConstant, "java/awt/Container") || wordText(nameConstant, "javax/swing/JComponent") || wordText(nameConstant, "javax/swing/AbstractButton") || wordText(nameConstant, "javax/swing/text/JTextComponent") || wordText(nameConstant, "javax/swing/SwingUtilities");
    }
    static boolean screenObject(int objectReference) { if (!isValidObject(objectReference)) return false; if (heapValue[objectReference] < 24 || heapValue[objectReference] > 28) { failureValue("unsupported Swing receiver"); return false; } return true; }
    static void setScreenCharacter(int objectReference, int textReference) {
        if (textReference != 0 && !objectValue(textReference, 1)) return;
        int entryCount = textReference == 0 ? 0 : heapValue[textReference + 1]; if (entryCount > 254) { throwException(9, "GUI text limit"); return; }
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) temporaryScreenText[loopIndex] = heapValue[textReference + 2 + loopIndex];
        if (User.screenText(heapValue[objectReference + 2], temporaryScreenText, entryCount) < 0) { throwException(9, "GUI text too long/invalid"); return; }
        heapValue[objectReference + 3] = textReference; heapReference[objectReference + 3] = 1;
    }
    static int readScreenCharacter(int objectReference) {
        int identityValue = heapValue[objectReference + 2], entryCount = User.screenConnection(8, identityValue, 0, 0, 0, 0), usedCount = 0;
        if (entryCount < 0) { failureValue("GUI text read failed"); return 0; }
        for (int loopIndex = 0; loopIndex < entryCount; loopIndex++) { int encodedValue = User.screenConnection(9, identityValue, loopIndex, 0, 0, 0); if (encodedValue >= 65536) { encodedValue -= 65536; temporaryScreenText[usedCount++] = 0xd800 | encodedValue >> 10; temporaryScreenText[usedCount++] = 0xdc00 | encodedValue & 1023; } else temporaryScreenText[usedCount++] = encodedValue; }
        int returnedValue = allocateStorage(1, usedCount); if (!error) for (int loopIndex = 0; loopIndex < usedCount; loopIndex++) heapValue[returnedValue + 2 + loopIndex] = temporaryScreenText[loopIndex]; return returnedValue;
    }
    /* Creates objects from the local API directly and connects them to kernel graphics, without Swing objects or adapters. */
    static void invokeKoreanScreen(int owner, int nameConstant, int descriptorConstant, int commandCode) {
        if (wordText(owner, "English/Native/EventQueue")) {
            if (commandCode == 184 && wordText(nameConstant, "invokeLater") && wordText(descriptorConstant, "(LEnglish/Native/RunnableTask;)V")) {
                int TaskAction = subtractValues(2); if (!isValidObject(TaskAction)) return;
                if (laterCount == 8) { failureValue("Screen performTask 대기열이 가득 찼습니다"); return; }
                laterKoreanValue[laterCount] = 1; scheduleLater[laterCount++] = TaskAction; return;
            }
            if (commandCode == 184 && wordText(nameConstant, "isEventDispatching") && wordText(descriptorConstant, "()Z")) { putValue(isHandlingEvent ? 1 : 0, 1); return; }
            failureValue("지원하지 않는 English Screen 일정 invoke"); return;
        }
        if (wordText(owner, "English/Native/ActionNotice")) {
            int notice = subtractValues(2); if (!objectValue(notice, 29) || heapValue[notice + 3] == 0) return;
            if (wordText(nameConstant, "eventSource") && wordText(descriptorConstant, "()LEnglish/Native/ScreenElement;")) putValue(heapValue[notice + 2], 2);
            else if (wordText(nameConstant, "commandText") && wordText(descriptorConstant, "()Ljava/lang/String;")) putValue(readScreenCharacter(heapValue[notice + 2]), 2);
            else if (wordText(nameConstant, "index") && wordText(descriptorConstant, "()I")) putValue(1001, 1);
            else failureValue("지원하지 않는 English action notice invoke"); return;
        }
        if (commandCode == 183 && wordText(nameConstant, "<init>")) {
            int kindValue = koreanScreenClass(owner), receiverValue = 0, horizontalPosition = 0, verticalPosition = 0, widthSpan = 0, heightValue = 0;
            if (kindValue == 24 && wordText(descriptorConstant, "(Ljava/lang/String;II)V")) {
                heightValue = subtractValues(1); widthSpan = subtractValues(1); horizontalPosition = (User.screenWidth() - widthSpan) / 2; verticalPosition = (User.screenHeight() - heightValue) / 2;
            } else if ((kindValue == 26 || kindValue == 28) && wordText(descriptorConstant, "(Ljava/lang/String;IIII)V") || kindValue == 27 && wordText(descriptorConstant, "(Ljava/lang/String;IIIILEnglish/Native/ActionReceiver;)V")) {
                if (kindValue == 27) receiverValue = subtractValues(2);
                heightValue = subtractValues(1); widthSpan = subtractValues(1); verticalPosition = subtractValues(1); horizontalPosition = subtractValues(1);
            } else { failureValue("지원하지 않는 English Screen 생성자"); return; }
            int text = subtractValues(2), elementValue = subtractValues(2); if (!screenObject(elementValue)) return;
            if (widthSpan < 1 || heightValue < 1 || horizontalPosition < 0 || verticalPosition < 0 || widthSpan > User.screenWidth() - horizontalPosition || heightValue > User.screenHeight() - verticalPosition) { throwException(27, "Screen 영역을 벗어난 크기입니다"); return; }
            int index = User.screenConnection(0, kindValue - 23, 0, 0, 0, 0);
            if (index < 1 || index > 32) { failureValue("Screen elementValue 자리가 가득 찼습니다"); return; }
            heapValue[elementValue + 2] = index; screenReference[index - 1] = elementValue;
            heapValue[elementValue + 5] = horizontalPosition; heapValue[elementValue + 6] = verticalPosition; heapValue[elementValue + 7] = widthSpan; heapValue[elementValue + 8] = heightValue; heapValue[elementValue + 10] = 2;
            heapValue[elementValue + 4] = receiverValue; heapReference[elementValue + 4] = 1; heapValue[elementValue + 12] = 1;
            User.screenConnection(1, index, horizontalPosition, verticalPosition, widthSpan, heightValue);
            if (kindValue == 24) User.screenConnection(7, index, 2, 0, 0, 0);
            setScreenCharacter(elementValue, text); return;
        }
        if (commandCode != 182) { failureValue("잘못된 English Screen invoke command"); return; }
        if (wordText(nameConstant, "writeText") && wordText(descriptorConstant, "(Ljava/lang/String;)V")) {
            int text = subtractValues(2), elementValue = subtractValues(2); if (screenObject(elementValue)) setScreenCharacter(elementValue, text); return;
        }
        if (wordText(nameConstant, "readText") && wordText(descriptorConstant, "()Ljava/lang/String;")) {
            int elementValue = subtractValues(2); if (screenObject(elementValue)) putValue(readScreenCharacter(elementValue), 2); return;
        }
        if (wordText(nameConstant, "setActionReceiver") && wordText(descriptorConstant, "(LEnglish/Native/ActionReceiver;)V")) {
            int receiverValue = subtractValues(2), elementValue = subtractValues(2);
            if (screenObject(elementValue)) { heapValue[elementValue + 4] = receiverValue; heapReference[elementValue + 4] = 1; heapValue[elementValue + 12] = 1; } return;
        }
        if (wordText(nameConstant, "addElement") && wordText(descriptorConstant, "(LEnglish/Native/ScreenElement;)V")) {
            int childValue = subtractValues(2), parentValue = subtractValues(2); if (!screenObject(childValue) || !screenObject(parentValue)) return;
            if (User.screenConnection(2, heapValue[parentValue + 2], heapValue[childValue + 2], 0, 0, 0) < 0) { throwException(27, "잘못된 Screen 부모입니다"); return; }
            heapValue[childValue + 11] = parentValue; heapReference[childValue + 11] = 1; return;
        }
        if (wordText(nameConstant, "setBounds") && wordText(descriptorConstant, "(IIII)V")) {
            int heightValue = subtractValues(1), widthSpan = subtractValues(1), verticalPosition = subtractValues(1), horizontalPosition = subtractValues(1), elementValue = subtractValues(2); if (!screenObject(elementValue)) return;
            if (User.screenConnection(1, heapValue[elementValue + 2], horizontalPosition, verticalPosition, widthSpan, heightValue) < 0) { throwException(27, "Screen 영역을 벗어난 자리입니다"); return; }
            heapValue[elementValue + 5] = horizontalPosition; heapValue[elementValue + 6] = verticalPosition; heapValue[elementValue + 7] = widthSpan; heapValue[elementValue + 8] = heightValue; return;
        }
        if ((wordText(nameConstant, "showWindow") || wordText(nameConstant, "close")) && wordText(descriptorConstant, "()V")) {
            boolean visibilityValue = wordText(nameConstant, "showWindow"); int elementValue = subtractValues(2); if (!screenObject(elementValue)) return;
            if (User.screenConnection(visibilityValue ? 3 : 4, heapValue[elementValue + 2], visibilityValue ? 1 : 0, 0, 0, 0) < 0) { failureValue("화면은 interactive 명령에서 실행해야 합니다"); return; }
            heapValue[elementValue + 9] = visibilityValue ? 1 : 0; return;
        }
        if (wordText(nameConstant, "isVisible") && wordText(descriptorConstant, "()Z")) { int elementValue = subtractValues(2); if (screenObject(elementValue)) putValue(heapValue[elementValue + 9], 1); return; }
        failureValue("지원하지 않는 English Screen methodValue");
    }
    static void invokeScreen(int owner, int nameConstant, int descriptorConstant, int commandCode) {
        if (wordText(owner, "javax/swing/SwingUtilities")) {
            if (commandCode == 184 && wordText(nameConstant, "invokeLater") && wordText(descriptorConstant, "(Ljava/lang/Runnable;)V")) { int objectReference = subtractValues(2); if (!isValidObject(objectReference)) return; if (laterCount == 8) { failureValue("invokeLater queue full"); return; } scheduleLater[laterCount++] = objectReference; return; }
            if (commandCode == 184 && wordText(nameConstant, "isEventDispatchThread") && wordText(descriptorConstant, "()Z")) { putValue(isHandlingEvent ? 1 : 0, 1); return; }
            failureValue("unsupported SwingUtilities method"); return;
        }
        if (wordText(owner, "java/awt/event/ActionEvent")) {
            int objectReference = subtractValues(2); if (!objectValue(objectReference, 29)) return;
            if (wordText(nameConstant, "getSource") && wordText(descriptorConstant, "()Ljava/lang/Object;")) putValue(heapValue[objectReference + 2], 2);
            else if (wordText(nameConstant, "getActionCommand") && wordText(descriptorConstant, "()Ljava/lang/String;")) putValue(readScreenCharacter(heapValue[objectReference + 2]), 2);
            else if (wordText(nameConstant, "getID") && wordText(descriptorConstant, "()I")) putValue(1001, 1);
            else failureValue("unsupported ActionEvent method"); return;
        }
        if (commandCode == 183 && wordText(nameConstant, "<init>")) {
            int columns = 0, textReference = 0;
            if (wordText(descriptorConstant, "(I)V")) columns = subtractValues(1);
            else if (wordText(descriptorConstant, "(Ljava/lang/String;I)V")) { columns = subtractValues(1); textReference = subtractValues(2); }
            else if (wordText(descriptorConstant, "(Ljava/lang/String;)V")) textReference = subtractValues(2);
            else if (wordText(descriptorConstant, "(Ljava/awt/LayoutManager;)V")) subtractValues(2);
            else if (!wordText(descriptorConstant, "()V")) { failureValue("unsupported Swing constructor"); return; }
            int objectReference = subtractValues(2); if (!isValidObject(objectReference)) return;
            if (heapValue[objectReference] == 30) { failureValue("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!screenObject(objectReference) || columns < 0) return;
            int identityValue = User.screenConnection(0, heapValue[objectReference] - 23, 0, 0, 0, 0);
            if (identityValue < 1 || identityValue > 32) { failureValue("GUI widget slots exhausted"); return; }
            heapValue[objectReference + 2] = identityValue; screenReference[identityValue - 1] = objectReference; heapValue[objectReference + 5] = heapValue[objectReference] == 24 ? 130 : 16; heapValue[objectReference + 6] = heapValue[objectReference] == 24 ? 110 : 16;
            heapValue[objectReference + 7] = heapValue[objectReference] == 24 ? 380 : 220; heapValue[objectReference + 8] = heapValue[objectReference] == 24 ? 240 : 28; heapValue[objectReference + 10] = 1;
            setScreenCharacter(objectReference, textReference); return;
        }
        if (wordText(nameConstant, "setText") || wordText(nameConstant, "setTitle")) { int textReference = subtractValues(2), objectReference = subtractValues(2); if (screenObject(objectReference) && wordText(descriptorConstant, "(Ljava/lang/String;)V")) setScreenCharacter(objectReference, textReference); return; }
        if (wordText(nameConstant, "getText") || wordText(nameConstant, "getTitle")) { int objectReference = subtractValues(2); if (screenObject(objectReference) && wordText(descriptorConstant, "()Ljava/lang/String;")) putValue(readScreenCharacter(objectReference), 2); return; }
        if (wordText(nameConstant, "addActionListener") && wordText(descriptorConstant, "(Ljava/awt/event/ActionListener;)V")) { int receiveReference = subtractValues(2), objectReference = subtractValues(2); if (screenObject(objectReference)) { heapValue[objectReference + 4] = receiveReference; heapReference[objectReference + 4] = 1; } return; }
        if (wordText(nameConstant, "getContentPane") && wordText(descriptorConstant, "()Ljava/awt/Container;")) { int objectReference = subtractValues(2); if (screenObject(objectReference)) putValue(objectReference, 2); return; }
        if (wordText(nameConstant, "setLayout") && wordText(descriptorConstant, "(Ljava/awt/LayoutManager;)V")) { int layoutReference = subtractValues(2), objectReference = subtractValues(2); if (screenObject(objectReference) && layoutReference != 0) failureValue("only absolute layout (null) is supported"); return; }
        if (wordText(nameConstant, "add") && (wordText(descriptorConstant, "(Ljava/awt/Component;)Ljava/awt/Component;") || wordText(descriptorConstant, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean layoutCondition = wordText(descriptorConstant, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (layoutCondition) subtractValues(2);
            int childReference = subtractValues(2), objectReference = subtractValues(2); if (!screenObject(childReference) || !screenObject(objectReference)) return;
            if (User.screenConnection(2, heapValue[objectReference + 2], heapValue[childReference + 2], 0, 0, 0) < 0) { throwException(9, "invalid GUI parent"); return; }
            heapValue[childReference + 11] = objectReference; heapReference[childReference + 11] = 1; if (!layoutCondition) putValue(childReference, 2); return;
        }
        if (wordText(nameConstant, "setBounds") && wordText(descriptorConstant, "(IIII)V")) {
            int heightValue = subtractValues(1), widthValue = subtractValues(1), yCoordinate = subtractValues(1), xCoordinate = subtractValues(1), objectReference = subtractValues(2); if (!screenObject(objectReference)) return;
            if (User.screenConnection(1, heapValue[objectReference + 2], xCoordinate, yCoordinate, widthValue, heightValue) < 0) { throwException(9, "GUI bounds"); return; }
            heapValue[objectReference + 5] = xCoordinate; heapValue[objectReference + 6] = yCoordinate; heapValue[objectReference + 7] = widthValue; heapValue[objectReference + 8] = heightValue; return;
        }
        if (wordText(nameConstant, "setSize") && wordText(descriptorConstant, "(II)V")) {
            int heightValue = subtractValues(1), widthValue = subtractValues(1), objectReference = subtractValues(2); if (!screenObject(objectReference)) return;
            if (User.screenConnection(1, heapValue[objectReference + 2], heapValue[objectReference + 5], heapValue[objectReference + 6], widthValue, heightValue) < 0) throwException(9, "GUI size"); else { heapValue[objectReference + 7] = widthValue; heapValue[objectReference + 8] = heightValue; } return;
        }
        if (wordText(nameConstant, "setLocationRelativeTo") && wordText(descriptorConstant, "(Ljava/awt/Component;)V")) { int relative = subtractValues(2), objectReference = subtractValues(2); if (!screenObject(objectReference)) return; if (relative != 0) { failureValue("only screen centering supported"); return; } heapValue[objectReference + 5] = (User.screenWidth() - heapValue[objectReference + 7]) / 2; heapValue[objectReference + 6] = (User.screenHeight() - heapValue[objectReference + 8]) / 2; User.screenConnection(1, heapValue[objectReference + 2], heapValue[objectReference + 5], heapValue[objectReference + 6], heapValue[objectReference + 7], heapValue[objectReference + 8]); return; }
        if (wordText(nameConstant, "setDefaultCloseOperation") && wordText(descriptorConstant, "(I)V")) { int policy = subtractValues(1), objectReference = subtractValues(2); if (screenObject(objectReference)) { if (policy < 0 || policy > 3) throwException(9, "close policy"); else { heapValue[objectReference + 10] = policy; User.screenConnection(7, heapValue[objectReference + 2], policy, 0, 0, 0); } } return; }
        if (wordText(nameConstant, "setVisible") && wordText(descriptorConstant, "(Z)V")) { int dataValue = subtractValues(1), objectReference = subtractValues(2); if (screenObject(objectReference)) { int processedValue = User.screenConnection(3, heapValue[objectReference + 2], dataValue, 0, 0, 0); if (processedValue < 0) failureValue("Swing requires a standalone interactive command"); else heapValue[objectReference + 9] = dataValue; } return; }
        if (wordText(nameConstant, "dispose") && wordText(descriptorConstant, "()V")) { int objectReference = subtractValues(2); if (screenObject(objectReference)) { User.screenConnection(4, heapValue[objectReference + 2], 0, 0, 0, 0); heapValue[objectReference + 9] = 0; } return; }
        if (wordText(nameConstant, "repaint") || wordText(nameConstant, "validate")) { int objectReference = subtractValues(2); if (!screenObject(objectReference) || !wordText(descriptorConstant, "()V")) return; User.screenConnection(1, heapValue[objectReference + 2], heapValue[objectReference + 5], heapValue[objectReference + 6], heapValue[objectReference + 7], heapValue[objectReference + 8]); return; }
        if (wordText(nameConstant, "isVisible") && wordText(descriptorConstant, "()Z")) { int objectReference = subtractValues(2); if (screenObject(objectReference)) putValue(heapValue[objectReference + 9], 1); return; }
        failureValue("unsupported Swing method (native subset)");
    }
    static void dispatchEvent(int targetAddress, int eventNumber, boolean English) {
        if (targetAddress < 1 || heapValue[targetAddress] < 32) { failureValue("Java event listener required"); return; }
        int fileIndex = nameMethod(heapValue[targetAddress] - 32, eventNumber == 0 ? (English ? "executeTask" : "run") : (English ? "receiveAction" : "actionPerformed"), eventNumber == 0 ? "()V" : (English ? "(LEnglish/Native/ActionNotice;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fileIndex < 0) { failureValue("event callback missing"); return; }
        currentThread = 0; threadCount = 1; frameIndex = 0; threadState[0] = 1; frameStack[0] = 0; frameLock[0] = initializeFrame[0] = 0; changeRequest = false;
        for (int loopIndex = 0; loopIndex < 128; loopIndex++) { localValue[loopIndex] = localType[loopIndex] = 0; }
        frameMethod[0] = fileIndex; framePosition[0] = methodStart[fileIndex]; localValue[0] = targetAddress; localType[0] = 2;
        if (eventNumber != 0) { localValue[1] = eventNumber; localType[1] = 2; }
        isHandlingEvent = true; executeCommand(); isHandlingEvent = false;
    }
    static void screenEvents() {
        while (!error) {
            if (laterCount > 0) { int targetAddress = scheduleLater[0], English = laterKoreanValue[0]; for (int loopIndex = 1; loopIndex < laterCount; loopIndex++) { scheduleLater[loopIndex - 1] = scheduleLater[loopIndex]; laterKoreanValue[loopIndex - 1] = laterKoreanValue[loopIndex]; } scheduleLater[--laterCount] = 0; laterKoreanValue[laterCount] = 0; dispatchEvent(targetAddress, 0, English != 0); continue; }
            if (User.screenConnection(6, 0, 0, 0, 0, 0) == 0) return;
            int eventNumber = User.screenConnection(5, 0, 0, 0, 0, 0); if (eventNumber == 0) continue;
            if (eventNumber < 0) { failureValue("GUI event I/O failed"); return; }
            int identityValue = eventNumber & 65535; if (identityValue < 1 || identityValue > 32) continue; int objectReference = screenReference[identityValue - 1]; if (objectReference == 0) continue;
            if ((eventNumber & 65536) != 0) {
                if (heapValue[objectReference + 10] != 0) heapValue[objectReference + 9] = 0;
                if (heapValue[objectReference + 10] == 3) for (int loopIndex = 0; loopIndex < 32; loopIndex++) if (screenReference[loopIndex] != 0 && heapValue[screenReference[loopIndex]] == 24) User.screenConnection(4, loopIndex + 1, 0, 0, 0, 0);
            } else if (heapValue[objectReference + 4] != 0) {
                int readmeReference = allocateStorage(29, 2); if (error) return; heapValue[readmeReference + 2] = objectReference; heapValue[readmeReference + 3] = heapValue[objectReference + 12]; heapReference[readmeReference + 2] = 1; dispatchEvent(heapValue[objectReference + 4], readmeReference, heapValue[objectReference + 12] != 0);
            }
        }
    }
    public static int run() {
        if (User.argumentsCount() == 1 && JavaTools.equalText(User.arguments(0), "-version")) {
            User.write("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (User.argumentsCount() < 1) { User.write("Usage: java CLASS [ARGS]\n"); return 2; }
        entryClassDefinition = loadClassDefinition(hostCharacter(User.arguments(0))); if (error || entryClassDefinition < 0) return 1;
        int entryPointValue = nameMethod(entryClassDefinition, "run", "()V");
        boolean koreanEntry = entryPointValue >= 0 && (methodAccess[entryPointValue] & 9) == 9;
        if (!koreanEntry) entryPointValue = nameMethod(entryClassDefinition, "main", "([Ljava/lang/String;)V");
        if (entryPointValue < 0 || (methodAccess[entryPointValue] & 9) != 9) failureValue("public static void run() or main(String[] args) required");
        if (error) return 1;
        int arguments = allocateStorage(3, User.argumentsCount() - 1); arrayElement[arguments] = -1;
        for (int number = 1; number < User.argumentsCount() && !error; number++) heapValue[arguments + 1 + number] = hostCharacter(User.arguments(number));
        frameIndex = 0; frameMethod[0] = entryPointValue; framePosition[0] = methodStart[entryPointValue]; localValue[0] = koreanEntry ? 0 : arguments; localType[0] = koreanEntry ? 0 : 2;
        threadState[0] = 1; threadObject[0] = allocateStorage(13, 2);
        executeCommand(); if (!error) screenEvents(); return error ? 1 : 0;
    }
}
