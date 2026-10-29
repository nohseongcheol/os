// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Restricted Java source compiler running in the guest and producing standard version 49 class files. */
public final class JavaCompiler {
    static int[] source = new int[16384], Output = new int[16384], codeValue = new int[4096];
    static int[] tokenKind = new int[2048], tokenPosition = new int[2048], tokenLength = new int[2048];
    static int[] constantValue = new int[4096], constantOffset = new int[512];
    static int[] Characters = new int[512], fileNameText = new int[64];
    static int[] insertedCode = new int[16];
    static int sourceSize, tokenCount, position, codeSize, constantSize, constantCount = 1, outputSize, characterLength;
    static boolean error;
    static int classToken, classConstant, parentConstant, codeConstant;
    static int[] methodEntryName = new int[32], methodReturn = new int[32], methodArgumentCount = new int[32];
    static int[] methodArgumentName = new int[512], methodArgumentType = new int[512];
    static int[] methodBody = new int[32], methodEnd = new int[32], methodCode = new int[32];
    static int[] methodLength = new int[32], methodLocals = new int[32], methodNameConstant = new int[32], methodDescriptorConstant = new int[32];
    static int[] methodAccess = new int[32];
    static int methodCount, currentMethod, localCount, depthValue, expressionDepth;
    static int[] localName = new int[128], localType = new int[128], localDepth = new int[128];

    static void failureValue(String reasonValue) {
        if (!error) {
            User.write("javac error: "); User.write(reasonValue);
            User.write(" at line ");
            int line = 1, ending = position < tokenCount ? tokenPosition[position] : sourceSize;
            for (int number = 0; number < ending; number++) if (source[number] == 10) line++;
            JavaTools.writeNumber(line); User.writeCharacterValue(10);
        }
        error = true;
    }
    static boolean characterValue(int value) { return IdentifierRules.firstCharacter(value); }
    static boolean digitValue(int value) { return value >= '0' && value <= '9'; }
    static boolean namesEqual(int firstOperand, int secondOperand) {
        if (firstOperand < 0 || secondOperand < 0 || firstOperand >= tokenCount || secondOperand >= tokenCount || tokenLength[firstOperand] != tokenLength[secondOperand]) return false;
        for (int number = 0; number < tokenLength[firstOperand]; number++) if (source[tokenPosition[firstOperand] + number] != source[tokenPosition[secondOperand] + number]) return false;
        return true;
    }
    static boolean wordValue(int tokenValue, String wordText) {
        if (tokenValue < 0 || tokenValue >= tokenCount || tokenLength[tokenValue] != wordText.length()) return false;
        for (int number = 0; number < wordText.length(); number++) if (source[tokenPosition[tokenValue] + number] != wordText.charAt(number)) return false;
        return true;
    }
    static int kindValue() { return position < tokenCount ? tokenKind[position] : 0; }
    static boolean receive(int value) { if (kindValue() != value) return false; position++; return true; }
    static void requirementValue(int value) { if (!receive(value)) failureValue("unexpected token"); }
    static boolean takeWord(String wordText) { if (!wordValue(position, wordText)) return false; position++; return true; }
    static void requireWord(String wordText) { if (!takeWord(wordText)) failureValue(wordText); }
    static int identifierValue() {
        int result = position;
        if (kindValue() != 256) failureValue("identifier required"); else position++;
        String reservedWords = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int run = 0;
        for (int number = 0; number <= reservedWords.length(); number++) {
            if (number == reservedWords.length() || reservedWords.charAt(number) == ' ') {
                boolean equalText = number - run == tokenLength[result];
                for (int slotEntry = run; equalText && slotEntry < number; slotEntry++) if (reservedWords.charAt(slotEntry) != source[tokenPosition[result] + slotEntry - run]) equalText = false;
                if (equalText) failureValue("reserved word cannot be an identifier");
                run = number + 1;
            }
        }
        return result;
    }
    static void cutValue() {
        int number = 0;
        while (number < sourceSize && !error) {
            int value = source[number], run = number, kindValue = value;
            if (value == 32 || value == 9 || value == 10 || value == 13) { number++; continue; }
            if (value == '/' && number + 1 < sourceSize && source[number + 1] == '/') {
                while (number < sourceSize && source[number] != 10) number++;
                continue;
            }
            if (value == '/' && number + 1 < sourceSize && source[number + 1] == '*') {
                number += 2;
                while (number + 1 < sourceSize && !(source[number] == '*' && source[number + 1] == '/')) number++;
                if (number + 1 >= sourceSize) { failureValue("unterminated comment"); break; }
                number += 2; continue;
            }
            if (characterValue(value)) { kindValue = 256; while (number < sourceSize && IdentifierRules.continuationCharacter(source[number])) number++; }
            else if (digitValue(value)) { kindValue = 257; while (number < sourceSize && digitValue(source[number])) number++; }
            else if (value == '"' || value == '\'') {
                kindValue = value == '"' ? 258 : 259; number++;
                while (number < sourceSize && source[number] != value && source[number] != 10 && source[number] != 13) {
                    if (source[number] == '\\') number++;
                    number++;
                }
                if (number >= sourceSize || source[number] != value) { failureValue("unterminated literal"); break; }
                number++;
            } else {
                number++;
                if (number < sourceSize) {
                    int nextItem = source[number];
                    if (value == '=' && nextItem == '=') kindValue = 300;
                    if (value == '!' && nextItem == '=') kindValue = 301;
                    if (value == '<' && nextItem == '=') kindValue = 302;
                    if (value == '>' && nextItem == '=') kindValue = 303;
                    if (value == '&' && nextItem == '&') kindValue = 304;
                    if (value == '|' && nextItem == '|') kindValue = 305;
                    if (value == '+' && nextItem == '+') kindValue = 306;
                    if (value == '-' && nextItem == '-') kindValue = 307;
                    if (value == '+' && nextItem == '=') kindValue = 308;
                    if (value == '-' && nextItem == '=') kindValue = 309;
                    if (value == '*' && nextItem == '=') kindValue = 310;
                    if (value == '/' && nextItem == '=') kindValue = 311;
                    if (value == '%' && nextItem == '=') kindValue = 312;
                    if (kindValue >= 300) number++;
                }
            }
            if (tokenCount == tokenKind.length - 1) { failureValue("too many tokens (2047 maximum)"); break; }
            tokenKind[tokenCount] = kindValue; tokenPosition[tokenCount] = run; tokenLength[tokenCount++] = number - run;
        }
    }
    static void writeConstantByte(int value) {
        if (constantSize == constantValue.length) { failureValue("constant pool too large"); return; }
        constantValue[constantSize++] = value & 255;
    }
    static void writeConstantShort(int value) { writeConstantByte(value >> 8); writeConstantByte(value); }
    static int registerConstant(int run) {
        for (int number = 1; number < constantCount; number++) {
            int frontValue = constantOffset[number], lengthValue = (number + 1 < constantCount ? constantOffset[number + 1] : run) - frontValue;
            if (lengthValue != constantSize - run) continue;
            boolean equalText = true;
            for (int slotEntry = 0; slotEntry < lengthValue; slotEntry++) if (constantValue[frontValue + slotEntry] != constantValue[run + slotEntry]) equalText = false;
            if (equalText) { constantSize = run; return number; }
        }
        if (constantCount == constantOffset.length) { failureValue("too many constants"); return 0; }
        constantOffset[constantCount] = run;
        return constantCount++;
    }
    static void appendText(int value) {
        if (characterLength == Characters.length) { failureValue("text too long"); return; }
        Characters[characterLength++] = value;
    }
    static void appendWord(String wordText) { for (int number = 0; number < wordText.length(); number++) appendText(wordText.charAt(number)); }
    static int characterConstant() {
        int run = constantSize; writeConstantByte(1); writeConstantShort(0);
        for (int number = 0; number < characterLength; number++) {
            int value = Characters[number];
            if (value > 0 && value < 128) writeConstantByte(value);
            else if (value < 2048) { writeConstantByte(192 | value >> 6); writeConstantByte(128 | value & 63); }
            else { writeConstantByte(224 | value >> 12); writeConstantByte(128 | value >> 6 & 63); writeConstantByte(128 | value & 63); }
        }
        if (error) return 0;
        int lengthValue = constantSize - run - 3;
        constantValue[run + 1] = lengthValue >> 8; constantValue[run + 2] = lengthValue & 255;
        return registerConstant(run);
    }
    static int wordConstant(String wordText) { characterLength = 0; appendWord(wordText); return characterConstant(); }
    static int tokenConstant(int tokenValue) {
        characterLength = 0;
        for (int number = 0; number < tokenLength[tokenValue]; number++) appendText(source[tokenPosition[tokenValue] + number]);
        return characterConstant();
    }
    static int reference(int kindValue, int firstOperand, int secondOperand) {
        int run = constantSize; writeConstantByte(kindValue); writeConstantShort(firstOperand);
        if (kindValue == 9 || kindValue == 10 || kindValue == 12) writeConstantShort(secondOperand);
        return registerConstant(run);
    }
    static int externalReference(int kindValue, String ownerValue, String name, String descriptionValue) {
        int ownerIdentifier = reference(7, wordConstant(ownerValue), 0);
        int nameCount = wordConstant(name), formatCount = wordConstant(descriptionValue);
        return reference(kindValue, ownerIdentifier, reference(12, nameCount, formatCount));
    }
    static void emitValue(int value) {
        if (codeSize == codeValue.length) { failureValue("bytecode too large"); return; }
        codeValue[codeSize++] = value & 255;
    }
    static void command(int value, int arguments) { emitValue(value); emitValue(arguments >> 8); emitValue(arguments); }
    static void numericConstant(int value) {
        if (value >= -1 && value <= 5) { emitValue(value + 3); return; }
        int run = constantSize; writeConstantByte(3); writeConstantShort(value >>> 16); writeConstantShort(value);
        command(19, registerConstant(run));
    }
    static int branch(int command) { int result = codeSize; command(command, 0); return result; }
    static void linkValue(int branch, int targetObject) {
        if (error) return;
        int distanceValue = targetObject - branch;
        if (distanceValue < -32768 || distanceValue > 32767 || branch < 0 || branch + 2 >= codeSize) { failureValue("invalid branch"); return; }
        codeValue[branch + 1] = distanceValue >> 8 & 255; codeValue[branch + 2] = distanceValue & 255;
    }
    static void comparisonValue(int command) {
        int trueValue = branch(command); emitValue(3); int ending = branch(167);
        linkValue(trueValue, codeSize); emitValue(4); linkValue(ending, codeSize);
    }
    static int formatValue() {
        if (takeWord("void")) return 0;
        if (takeWord("int")) return 1;
        if (takeWord("boolean")) return 2;
        if (takeWord("char")) return 5;
        if (takeWord("FileInputStream")) return 6;
        if (takeWord("FileOutputStream")) return 7;
        if (takeWord("String")) { if (receive('[')) { requirementValue(']'); return 4; } return 3; }
        failureValue("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void addFormat(int typeValue) {
        if (typeValue == 0) appendText('V');
        if (typeValue == 1) appendText('I');
        if (typeValue == 2) appendText('Z');
        if (typeValue == 3) appendWord("Ljava/lang/String;");
        if (typeValue == 4) appendWord("[Ljava/lang/String;");
        if (typeValue == 5) appendText('C');
        if (typeValue == 6) appendWord("Ljava/io/FileInputStream;");
        if (typeValue == 7) appendWord("Ljava/io/FileOutputStream;");
    }
    // The restricted compiler supports throws declarations. Exception-handler bodies require host javac.
    static void readExceptionName() {
        boolean KoreanBundle = takeWord("English");
        if (KoreanBundle) { requirementValue('.'); requireWord("Native"); requirementValue('.'); }
        if (!KoreanBundle && (takeWord("Exception") || takeWord("IOException"))) return;
        if (takeWord("exception") || takeWord("ExecutionException") || takeWord("InputOutputException") || takeWord("WaitTimeoutException") || takeWord("AddressLookupException") || takeWord("MissingFileException") || takeWord("CommunicationException") || takeWord("InvalidArgumentException") || takeWord("NumberFormatFailure") || takeWord("BoundsException") || takeWord("ArrayBoundsException") || takeWord("StringBoundsException") || takeWord("NullReferenceException") || takeWord("ArithmeticFailure") || takeWord("StateException") || takeWord("TypeCastException") || takeWord("NegativeArraySizeFailure") || takeWord("ArrayStoreFailure") || takeWord("ThreadStateException") || takeWord("WaitInterruptedException")) return;
        failureValue("unsupported throws type");
    }
    static void readDeclaration() {
        while (takeWord("import")) {
            if (wordValue(position, "English")) readExceptionName();
            else {
                requireWord("java"); requirementValue('.'); requireWord("io"); requirementValue('.');
                if (!(takeWord("FileInputStream") || takeWord("FileOutputStream") || takeWord("IOException"))) failureValue("unsupported import");
            }
            requirementValue(';');
        }
        takeWord("public"); takeWord("final"); requireWord("class"); classToken = identifierValue();
        classConstant = reference(7, tokenConstant(classToken), 0);
        parentConstant = reference(7, wordConstant("java/lang/Object"), 0); codeConstant = wordConstant("Code"); requirementValue('{');
        while (!error && kindValue() != '}') {
            if (methodCount == 32) { failureValue("too many methods"); break; }
            int accessEntry = takeWord("public") ? 1 : takeWord("private") ? 2 : 0; requireWord("static");
            int functionValue = methodCount++;
            methodAccess[functionValue] = accessEntry | 8;
            methodReturn[functionValue] = formatValue(); methodEntryName[functionValue] = identifierValue(); requirementValue('(');
            for (int frontValue = 0; frontValue < functionValue; frontValue++) if (namesEqual(methodEntryName[frontValue], methodEntryName[functionValue])) failureValue("duplicate method (overloading unsupported)");
            while (!error && kindValue() != ')') {
                int number = methodArgumentCount[functionValue];
                if (number == 16) { failureValue("too many parameters"); break; }
                int typeValue = formatValue(); if (typeValue == 0) failureValue("void parameter");
                methodArgumentType[functionValue * 16 + number] = typeValue; methodArgumentName[functionValue * 16 + number] = identifierValue();
                methodArgumentCount[functionValue]++;
                if (!receive(',')) break;
            }
            requirementValue(')');
            if (takeWord("throws")) {
                do { readExceptionName(); } while (!error && receive(','));
            }
            methodBody[functionValue] = position; requirementValue('{');
            int nestingValue = 1;
            while (position < tokenCount && nestingValue > 0) {
                if (kindValue() == '{') nestingValue++;
                if (kindValue() == '}') nestingValue--;
                position++;
            }
            if (nestingValue != 0) failureValue("unclosed method body");
            methodEnd[functionValue] = position;
            methodNameConstant[functionValue] = tokenConstant(methodEntryName[functionValue]);
            characterLength = 0; appendText('(');
            for (int number = 0; number < methodArgumentCount[functionValue]; number++) addFormat(methodArgumentType[functionValue * 16 + number]);
            appendText(')'); addFormat(methodReturn[functionValue]); methodDescriptorConstant[functionValue] = characterConstant();
        }
        requirementValue('}'); if (position != tokenCount) failureValue("extra input after class");
    }
    static int findLocal(int name) {
        for (int number = localCount - 1; number >= 0; number--) if (localDepth[number] >= 0 && namesEqual(localName[number], name)) return number;
        failureValue("unknown variable"); return 0;
    }
    static int addLocal(int name, int typeValue) {
        for (int number = 0; number < localCount; number++) if (localDepth[number] >= 0 && namesEqual(localName[number], name)) failureValue("duplicate local variable");
        if (localCount == 128) { failureValue("too many locals"); return 0; }
        localName[localCount] = name; localType[localCount] = typeValue; localDepth[localCount] = depthValue;
        return localCount++;
    }
    static boolean integerType(int typeValue) { return typeValue == 1 || typeValue == 5; }
    static void readLocal(int number) { emitValue(localType[number] <= 2 || localType[number] == 5 ? 21 : 25); emitValue(number); }
    static void writeLocal(int number) { emitValue(localType[number] <= 2 || localType[number] == 5 ? 54 : 58); emitValue(number); }
    static void verifyType(int actualData, int expectation) { if (actualData != expectation && !(actualData == 5 && expectation == 1)) failureValue("type mismatch"); }
    static void readCharacterValue(int tokenValue) {
        characterLength = 0; int run = tokenPosition[tokenValue] + 1, ending = tokenPosition[tokenValue] + tokenLength[tokenValue] - 1;
        while (run < ending && !error) {
            int value = source[run++];
            if (value == '\\') {
                if (run == ending) { failureValue("invalid escape"); break; }
                value = source[run++];
                if (value == 'n') value = 10;
                else if (value == 'r') value = 13;
                else if (value == 't') value = 9;
                else if (value == 'b') value = 8;
                else if (value == 'f') value = 12;
                else if (value != '\\' && value != '"' && value != '\'') failureValue("unsupported escape");
            }
            appendText(value);
        }
    }
    static int parseInteger(int tokenValue, boolean negativeValue) {
        if (tokenLength[tokenValue] > 1 && source[tokenPosition[tokenValue]] == '0') failureValue("octal literals unsupported");
        int value = 0;
        for (int number = 0; number < tokenLength[tokenValue]; number++) {
            int digitItem = source[tokenPosition[tokenValue] + number] - '0';
            if (value < -214748364 || value == -214748364 && digitItem > (negativeValue ? 8 : 7)) failureValue("integer literal out of range");
            value = value * 10 - digitItem;
        }
        return negativeValue ? value : -value;
    }
    static int primaryExpression() {
        if (takeWord("new")) {
            int typeValue = formatValue();
            if (typeValue != 6 && typeValue != 7) { failureValue("only file streams supported by new in source"); return 0; }
            String ownerValue = typeValue == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            command(187, reference(7, wordConstant(ownerValue), 0)); emitValue(89);
            requirementValue('('); verifyType(expressionValue(), 3); boolean continuationValue = false;
            if (receive(',')) { if (typeValue != 7) failureValue("input stream constructor arguments"); verifyType(expressionValue(), 2); continuationValue = true; }
            requirementValue(')');
            command(183, externalReference(10, ownerValue, "<init>", continuationValue ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return typeValue;
        }
        if (receive('(')) { int typeValue = expressionValue(); requirementValue(')'); return typeValue; }
        if (kindValue() == 257) { numericConstant(parseInteger(position++, false)); return 1; }
        if (kindValue() == 258) { readCharacterValue(position++); command(19, reference(8, characterConstant(), 0)); return 3; }
        if (kindValue() == 259) { readCharacterValue(position++); if (characterLength != 1) failureValue("character literal length"); numericConstant(Characters[0]); return 5; }
        if (takeWord("true")) { emitValue(4); return 2; }
        if (takeWord("false")) { emitValue(3); return 2; }
        if (takeWord("English")) {
            requirementValue('.'); requireWord("Native"); requirementValue('.');
            String ownerValue = "", methodValue = "", descriptionValue = ""; int firstOperand = 0, secondOperand = 0, thirdOperand = 0, fourthOperand = 0, fifthOperand = 0, result = 0;
            if (takeWord("Output")) {
                ownerValue = "English/Native/Output"; requirementValue('.');
                if (takeWord("writeLine")) { methodValue = "writeLine"; descriptionValue = "(Ljava/lang/String;)V"; firstOperand = 3; }
                else if (takeWord("write")) { methodValue = "write"; descriptionValue = "(Ljava/lang/String;)V"; firstOperand = 3; }
                else if (takeWord("writeNumber")) { methodValue = "writeNumber"; descriptionValue = "(I)V"; firstOperand = 1; }
                else failureValue("unknown Korean output method");
            } else if (takeWord("Characters")) {
                ownerValue = "English/Native/Characters"; requirementValue('.'); firstOperand = 3;
                if (takeWord("lengthValue")) { methodValue = "lengthValue"; descriptionValue = "(Ljava/lang/String;)I"; result = 1; }
                else if (takeWord("codePointCount")) { methodValue = "codePointCount"; descriptionValue = "(Ljava/lang/String;)I"; result = 1; }
                else if (takeWord("parseInteger")) { methodValue = "parseInteger"; descriptionValue = "(Ljava/lang/String;)I"; result = 1; }
                else if (takeWord("writeIntegerValue")) { methodValue = "writeIntegerValue"; descriptionValue = "(I)Ljava/lang/String;"; firstOperand = 1; result = 3; }
                else if (takeWord("equalText")) { methodValue = "equalText"; descriptionValue = "(Ljava/lang/String;Ljava/lang/String;)Z"; secondOperand = 3; result = 2; }
                else if (takeWord("pasteText")) { methodValue = "pasteText"; descriptionValue = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; secondOperand = 3; result = 3; }
                else if (takeWord("cutValue")) { methodValue = "cutValue"; descriptionValue = "(Ljava/lang/String;II)Ljava/lang/String;"; secondOperand = 1; thirdOperand = 1; result = 3; }
                else failureValue("unknown Korean text method");
            } else if (takeWord("file")) {
                ownerValue = "English/Native/file"; requirementValue('.'); firstOperand = 3;
                if (takeWord("read")) { methodValue = "read"; descriptionValue = "(Ljava/lang/String;)Ljava/lang/String;"; result = 3; }
                else if (takeWord("write")) { methodValue = "write"; descriptionValue = "(Ljava/lang/String;Ljava/lang/String;)V"; secondOperand = 3; }
                else failureValue("unknown Korean file method");
            } else if (takeWord("Screen")) {
                ownerValue = "English/Native/Screen"; requirementValue('.');
                if (takeWord("widthValue")) { methodValue = "widthValue"; descriptionValue = "()I"; result = 1; }
                else if (takeWord("heightValue")) { methodValue = "heightValue"; descriptionValue = "()I"; result = 1; }
                else if (takeWord("rectangle")) { methodValue = "rectangle"; descriptionValue = "(IIIII)V"; firstOperand = 1; secondOperand = 1; thirdOperand = 1; fourthOperand = 1; fifthOperand = 1; }
                else if (takeWord("eraseEntry")) { methodValue = "eraseEntry"; descriptionValue = "(I)V"; firstOperand = 1; }
                else if (takeWord("await")) { methodValue = "await"; descriptionValue = "()V"; }
                else failureValue("unknown Korean framebuffer method");
            } else failureValue("unsupported Korean library class");
            requirementValue('('); if (firstOperand != 0) verifyType(expressionValue(), firstOperand);
            if (secondOperand != 0) { requirementValue(','); verifyType(expressionValue(), secondOperand); }
            if (thirdOperand != 0) { requirementValue(','); verifyType(expressionValue(), thirdOperand); }
            if (fourthOperand != 0) { requirementValue(','); verifyType(expressionValue(), fourthOperand); }
            if (fifthOperand != 0) { requirementValue(','); verifyType(expressionValue(), fifthOperand); }
            requirementValue(')'); command(184, externalReference(10, ownerValue, methodValue, descriptionValue)); return result;
        }
        if (takeWord("Integer")) {
            requirementValue('.'); requireWord("parseInt"); requirementValue('('); verifyType(expressionValue(), 3); requirementValue(')');
            command(184, externalReference(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int name = identifierValue();
        if (receive('(')) {
            int functionValue = -1;
            for (int number = 0; number < methodCount; number++) if (namesEqual(name, methodEntryName[number])) functionValue = number;
            if (functionValue < 0) { failureValue("unknown static method"); return 0; }
            int number = 0;
            while (!error && kindValue() != ')') {
                if (number >= methodArgumentCount[functionValue]) { failureValue("too many arguments"); break; }
                verifyType(expressionValue(), methodArgumentType[functionValue * 16 + number++]); if (!receive(',')) break;
            }
            requirementValue(')'); if (number != methodArgumentCount[functionValue]) failureValue("argument count mismatch");
            command(184, reference(10, classConstant, reference(12, methodNameConstant[functionValue], methodDescriptorConstant[functionValue])));
            return methodReturn[functionValue];
        }
        int localScope = findLocal(name), typeValue = localType[localScope]; readLocal(localScope);
        while (!error) {
            if (receive('[')) { verifyType(typeValue, 4); verifyType(expressionValue(), 1); requirementValue(']'); emitValue(50); typeValue = 3; }
            else if (receive('.')) {
                if (typeValue == 6 || typeValue == 7) {
                    String ownerValue = typeValue == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (takeWord("close")) { requirementValue('('); requirementValue(')'); command(182, externalReference(10, ownerValue, "close", "()V")); typeValue = 0; }
                    else if (typeValue == 6 && takeWord("read")) { requirementValue('('); requirementValue(')'); command(182, externalReference(10, ownerValue, "read", "()I")); typeValue = 1; }
                    else if (typeValue == 7 && takeWord("write")) { requirementValue('('); verifyType(expressionValue(), 1); requirementValue(')'); command(182, externalReference(10, ownerValue, "write", "(I)V")); typeValue = 0; }
                    else { failureValue("unsupported file stream method"); }
                    continue;
                }
                requireWord("length");
                if (typeValue == 4) { emitValue(190); typeValue = 1; }
                else { verifyType(typeValue, 3); requirementValue('('); requirementValue(')'); command(182, externalReference(10, "java/lang/String", "length", "()I")); typeValue = 1; }
            } else break;
        }
        return typeValue;
    }
    static int unaryValue() {
        if (++expressionDepth > 64) { failureValue("expression nesting too deep"); expressionDepth--; return 0; }
        int typeValue;
        if (receive('!')) { verifyType(unaryValue(), 2); comparisonValue(153); typeValue = 2; }
        else if (receive('-')) {
            if (kindValue() == 257) numericConstant(parseInteger(position++, true));
            else { verifyType(unaryValue(), 1); emitValue(116); }
            typeValue = 1;
        } else if (receive('+')) { verifyType(unaryValue(), 1); typeValue = 1; }
        else typeValue = primaryExpression();
        expressionDepth--; return typeValue;
    }
    static int multiplicationExpression() {
        int typeValue = unaryValue();
        while (!error && (kindValue() == '*' || kindValue() == '/' || kindValue() == '%')) {
            int encodingValue = kindValue(); position++; verifyType(typeValue, 1); verifyType(unaryValue(), 1);
            emitValue(encodingValue == '*' ? 104 : encodingValue == '/' ? 108 : 112); typeValue = 1;
        }
        return typeValue;
    }
    static int additionExpression() {
        int typeValue = multiplicationExpression();
        while (!error && (kindValue() == '+' || kindValue() == '-')) {
            int encodingValue = kindValue(); position++; int boundaryValue = codeSize, backValueType = multiplicationExpression();
            if (encodingValue == '+' && (typeValue == 3 || backValueType == 3)) { combineValues(boundaryValue, typeValue, backValueType); typeValue = 3; }
            else { verifyType(typeValue, 1); verifyType(backValueType, 1); emitValue(encodingValue == '+' ? 96 : 100); typeValue = 1; }
        }
        return typeValue;
    }
    static int attachedReference(int typeValue) {
        if (typeValue != 1 && typeValue != 2 && typeValue != 3 && typeValue != 5) failureValue("unsupported concatenation type");
        return externalReference(10, "java/lang/StringBuilder", "append", typeValue == 1 ? "(I)Ljava/lang/StringBuilder;"
            : typeValue == 2 ? "(Z)Ljava/lang/StringBuilder;" : typeValue == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void combineValues(int boundaryValue, int frontValueType, int backValueType) {
        // Insert generated code before the right operand's code, so the already computed left value is appended first.
        // Relative branches inside the right expression stay valid because the whole region moves together.
        int ending = codeSize;
        command(187, reference(7, wordConstant("java/lang/StringBuilder"), 0)); emitValue(89);
        command(183, externalReference(10, "java/lang/StringBuilder", "<init>", "()V")); emitValue(95); command(182, attachedReference(frontValueType));
        if (error) return;
        int lengthValue = codeSize - ending;
        for (int number = 0; number < lengthValue; number++) insertedCode[number] = codeValue[ending + number];
        for (int number = ending - 1; number >= boundaryValue; number--) codeValue[number + lengthValue] = codeValue[number];
        for (int number = 0; number < lengthValue; number++) codeValue[boundaryValue + number] = insertedCode[number];
        command(182, attachedReference(backValueType)); command(182, externalReference(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int comparisonExpression() {
        int typeValue = additionExpression();
        while (!error && (kindValue() == '<' || kindValue() == '>' || kindValue() == 302 || kindValue() == 303)) {
            int encodingValue = kindValue(); position++; verifyType(typeValue, 1); verifyType(additionExpression(), 1);
            comparisonValue(encodingValue == '<' ? 161 : encodingValue == '>' ? 163 : encodingValue == 302 ? 164 : 162); typeValue = 2;
        }
        return typeValue;
    }
    static int equalityExpression() {
        int typeValue = comparisonExpression();
        while (!error && (kindValue() == 300 || kindValue() == 301)) {
            int encodingValue = kindValue(); position++; int backValueType = comparisonExpression();
            if (typeValue == 0 || backValueType == 0) failureValue("void expression");
            if (!(integerType(typeValue) && integerType(backValueType))) verifyType(backValueType, typeValue);
            comparisonValue((typeValue <= 2 || typeValue == 5 ? 159 : 165) + (encodingValue == 301 ? 1 : 0)); typeValue = 2;
        }
        return typeValue;
    }
    static int logicalAnd() {
        int typeValue = equalityExpression();
        while (!error && receive(304)) {
            verifyType(typeValue, 2); int firstOperand = branch(153); verifyType(equalityExpression(), 2); int secondOperand = branch(153);
            emitValue(4); int ending = branch(167); linkValue(firstOperand, codeSize); linkValue(secondOperand, codeSize); emitValue(3); linkValue(ending, codeSize); typeValue = 2;
        }
        return typeValue;
    }
    static int expressionValue() {
        int typeValue = logicalAnd();
        while (!error && receive(305)) {
            verifyType(typeValue, 2); int firstOperand = branch(154); verifyType(logicalAnd(), 2); int secondOperand = branch(154);
            emitValue(3); int ending = branch(167); linkValue(firstOperand, codeSize); linkValue(secondOperand, codeSize); emitValue(4); linkValue(ending, codeSize); typeValue = 2;
        }
        return typeValue;
    }
    static void assignmentValue(boolean allowDeclaration) {
        if (wordValue(position, "int") || wordValue(position, "boolean") || wordValue(position, "String") || wordValue(position, "char")
            || wordValue(position, "FileInputStream") || wordValue(position, "FileOutputStream")) {
            if (!allowDeclaration) failureValue("declaration not allowed here");
            int typeValue = formatValue(), name = identifierValue(); requirementValue('='); verifyType(expressionValue(), typeValue);
            writeLocal(addLocal(name, typeValue)); return;
        }
        int name = identifierValue(), localScope = findLocal(name);
        if (receive('=')) { verifyType(expressionValue(), localType[localScope]); writeLocal(localScope); }
        else if (kindValue() >= 308 && kindValue() <= 312) {
            int encodingValue = kindValue(); position++; readLocal(localScope); int boundaryValue = codeSize, backValueType = expressionValue();
            if (encodingValue == 308 && localType[localScope] == 3) combineValues(boundaryValue, 3, backValueType);
            else {
                verifyType(localType[localScope], 1); verifyType(backValueType, 1);
                emitValue(encodingValue == 308 ? 96 : encodingValue == 309 ? 100 : encodingValue == 310 ? 104 : encodingValue == 311 ? 108 : 112);
                if (localType[localScope] == 5) emitValue(146);
            }
            writeLocal(localScope);
        }
        else if (kindValue() == 306 || kindValue() == 307) {
            verifyType(localType[localScope], 1); emitValue(132); emitValue(localScope); emitValue(kindValue() == 306 ? 1 : 255); position++;
            if (localType[localScope] == 5) { readLocal(localScope); emitValue(146); writeLocal(localScope); }
        } else failureValue("assignment or postfix increment required");
    }
    static void screenOutput() {
        requireWord("System"); requirementValue('.'); requireWord("out"); requirementValue('.');
        boolean newline = takeWord("println"); if (!newline) requireWord("print"); requirementValue('(');
        command(178, externalReference(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean emptyArgument = kindValue() == ')';
        int typeValue = emptyArgument ? 0 : expressionValue(); requirementValue(')'); requirementValue(';');
        String descriptionValue = typeValue == 0 ? "()V" : typeValue == 1 ? "(I)V" : typeValue == 2 ? "(Z)V" : typeValue == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (typeValue == 4 || typeValue >= 6 || typeValue == 0 && (!newline || !emptyArgument)) failureValue("unsupported print argument");
        command(182, externalReference(10, "java/io/PrintStream", newline ? "println" : "print", descriptionValue));
    }
    static boolean statementValue() {
        if (error) return false;
        if (depthValue > 32) { failureValue("statement nesting too deep"); return false; }
        if (receive('{')) {
            depthValue++; boolean returnResult = false;
            while (!error && kindValue() != '}') { if (returnResult) failureValue("unreachable statement"); returnResult = statementValue(); }
            requirementValue('}'); for (int number = 0; number < localCount; number++) if (localDepth[number] == depthValue) localDepth[number] = -1;
            depthValue--; return returnResult;
        }
        if (receive(';')) return false;
        if (takeWord("return")) {
            int typeValue = kindValue() == ';' ? 0 : expressionValue(); verifyType(typeValue, methodReturn[currentMethod]); requirementValue(';');
            emitValue(typeValue == 0 ? 177 : typeValue <= 2 || typeValue == 5 ? 172 : 176); return true;
        }
        if (takeWord("if")) {
            requirementValue('('); verifyType(expressionValue(), 2); requirementValue(')'); int falseValue = branch(153);
            depthValue++; boolean firstOperand = controlStatement(); depthValue--;
            if (takeWord("else")) { int ending = branch(167); linkValue(falseValue, codeSize); depthValue++; boolean secondOperand = controlStatement(); depthValue--; linkValue(ending, codeSize); return firstOperand && secondOperand; }
            linkValue(falseValue, codeSize); return false;
        }
        if (takeWord("while")) {
            int run = codeSize; requirementValue('('); verifyType(expressionValue(), 2); requirementValue(')'); int ending = branch(153);
            depthValue++; controlStatement(); depthValue--; linkValue(branch(167), run); linkValue(ending, codeSize); return false;
        }
        if (takeWord("for")) {
            depthValue++; requirementValue('('); if (kindValue() != ';') assignmentValue(true); requirementValue(';');
            int condition = codeSize; if (kindValue() == ';') emitValue(4); else verifyType(expressionValue(), 2); requirementValue(';');
            int ending = branch(153), bodyText = branch(167), refresh = codeSize;
            if (kindValue() != ')') assignmentValue(false); requirementValue(')'); linkValue(branch(167), condition); linkValue(bodyText, codeSize);
            controlStatement(); linkValue(branch(167), refresh); linkValue(ending, codeSize);
            for (int number = 0; number < localCount; number++) if (localDepth[number] == depthValue) localDepth[number] = -1;
            depthValue--; return false;
        }
        if (wordValue(position, "System")) { screenOutput(); return false; }
        if (kindValue() == 256 && position + 1 < tokenCount && (tokenKind[position + 1] == '(' || tokenKind[position + 1] == '.')) {
            int typeValue = expressionValue(); if (typeValue != 0) emitValue(87); requirementValue(';'); return false;
        }
        assignmentValue(true); requirementValue(';'); return false;
    }
    static boolean controlStatement() {
        if (wordValue(position, "int") || wordValue(position, "boolean") || wordValue(position, "char") || wordValue(position, "String")
            || wordValue(position, "FileInputStream") || wordValue(position, "FileOutputStream")) failureValue("local declaration requires braces");
        return statementValue();
    }
    static void emitClassByte(int value) { if (outputSize == Output.length) failureValue("class file too large"); else Output[outputSize++] = value & 255; }
    static void emitClassShort(int value) { emitClassByte(value >> 8); emitClassByte(value); }
    static void emitClassInteger(int value) { emitClassShort(value >>> 16); emitClassShort(value); }
    static void writeClass() {
        emitClassInteger(0xcafebabe); emitClassShort(0); emitClassShort(49); emitClassShort(constantCount);
        for (int number = 0; number < constantSize; number++) emitClassByte(constantValue[number]);
        emitClassShort(0x21); emitClassShort(classConstant); emitClassShort(parentConstant); emitClassShort(0); emitClassShort(0); emitClassShort(methodCount);
        for (int number = 0; number < methodCount; number++) {
            emitClassShort(methodAccess[number]); emitClassShort(methodNameConstant[number]); emitClassShort(methodDescriptorConstant[number]); emitClassShort(1); emitClassShort(codeConstant);
            emitClassInteger(12 + methodLength[number]); emitClassShort(128); emitClassShort(methodLocals[number]); emitClassInteger(methodLength[number]);
            for (int slotEntry = 0; slotEntry < methodLength[number]; slotEntry++) emitClassByte(codeValue[methodCode[number] + slotEntry]);
            emitClassShort(0); emitClassShort(0);
        }
        emitClassShort(0);
    }
    public static int run() {
        if (User.argumentsCount() == 1 && JavaTools.equalText(User.arguments(0), "-version")) {
            User.write("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (User.argumentsCount() != 1) { User.write("Usage: javac FILE.java\n"); return 2; }
        int nameSize = JavaTools.name(fileNameText, User.arguments(0));
        if (nameSize < 6 || nameSize > 62 || fileNameText[nameSize - 5] != '.' || fileNameText[nameSize - 4] != 'j'
            || fileNameText[nameSize - 3] != 'a' || fileNameText[nameSize - 2] != 'v' || fileNameText[nameSize - 1] != 'a') {
            User.write("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        sourceSize = User.readFile(fileNameText, source);
        if (sourceSize < 0) { User.write("javac: cannot read source: "); JavaTools.writeNumber(sourceSize); User.writeCharacterValue(10); return 1; }
        sourceSize = JavaTools.decodeSource(source, sourceSize);
        if (sourceSize < 0) { User.write("javac error: invalid UTF-8 source\n"); return 1; }
        cutValue(); if (!error) readDeclaration();
        if (!error) {
            if (tokenLength[classToken] != nameSize - 5) failureValue("class name must match file name");
            for (int number = 0; number < nameSize - 5; number++) if (source[tokenPosition[classToken] + number] != fileNameText[number]) failureValue("class name must match file name");
        }
        for (currentMethod = 0; currentMethod < methodCount && !error; currentMethod++) {
            position = methodBody[currentMethod]; methodCode[currentMethod] = codeSize; localCount = 0; depthValue = 0;
            for (int number = 0; number < methodArgumentCount[currentMethod]; number++) addLocal(methodArgumentName[currentMethod * 16 + number], methodArgumentType[currentMethod * 16 + number]);
            boolean returnResult = statementValue();
            if (!returnResult && methodReturn[currentMethod] != 0) failureValue("missing return");
            // The merge point after a branch must be an actual instruction (version 49 verifier).
            if (methodReturn[currentMethod] == 0) emitValue(177);
            else { boolean Integer = methodReturn[currentMethod] <= 2 || methodReturn[currentMethod] == 5; emitValue(Integer ? 3 : 1); emitValue(Integer ? 172 : 176); }
            if (position != methodEnd[currentMethod]) failureValue("invalid method body");
            methodLocals[currentMethod] = localCount; methodLength[currentMethod] = codeSize - methodCode[currentMethod];
        }
        if (error) return 1;
        writeClass(); if (error) return 1;
        fileNameText[nameSize - 4] = 'c'; fileNameText[nameSize - 3] = 'l'; fileNameText[nameSize - 2] = 'a';
        fileNameText[nameSize - 1] = 's'; fileNameText[nameSize] = 's'; fileNameText[nameSize + 1] = 0;
        int result = User.writeFile(fileNameText, Output, outputSize);
        if (result < 0) { User.write("javac: cannot save class: "); JavaTools.writeNumber(result); User.writeCharacterValue(10); return 1; }
        User.write("Compiled: "); for (int number = 0; fileNameText[number] != 0; number++) User.writeCharacterValue(fileNameText[number]);
        User.write(" (JVM class version 49)\n"); return 0;
    }
}
