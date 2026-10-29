// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Generates C source for a standalone ARM64 kernel from Java class files. Runs on the host JDK. */
public final class AheadOfTimeCompiler {
    static final class TranslationError extends RuntimeException {
        TranslationError(String description) { super(description); }
    }
    static final class DataReader {
        final byte[] data;
        int position;
        DataReader(byte[] inputData) { data = inputData; }
        byte[] read(int lengthValue) {
            if (lengthValue < 0 || lengthValue > data.length - position) throw new TranslationError("clippedValue classValue 또는 command data");
            byte[] result = Arrays.copyOfRange(data, position, position + lengthValue); position += lengthValue; return result;
        }
        int readByte() { if (position >= data.length) throw new TranslationError("clippedValue command data"); return data[position++] & 255; }
        int readShort() { return (readByte() << 8) | readByte(); }
        int readInt() { return (readShort() << 16) | readShort(); }
        int readSignedByte() { return (byte) readByte(); }
        int readSignedShort() { return (short) readShort(); }
    }
    static final class MemberData {
        final int accessEntry;
        final String name, descriptionValue;
        final Map<String, byte[]> attributeValue;
        MemberData(int accessValue, String nameValue, String descriptorData, Map<String, byte[]> attributeData) {
            accessEntry = accessValue; name = nameValue; descriptionValue = descriptorData; attributeValue = attributeData;
        }
    }
    static final class MethodReference implements Comparable<MethodReference> {
        final String ownerValue, name, descriptionValue;
        MethodReference(String ownedValue, String nameValue, String descriptorData) { ownerValue = ownedValue; name = nameValue; descriptionValue = descriptorData; }
        String[] parts() { return new String[]{ownerValue, name, descriptionValue}; }
        public int compareTo(MethodReference peerValue) {
            int comparisonValue = ownerValue.compareTo(peerValue.ownerValue);
            if (comparisonValue == 0) comparisonValue = name.compareTo(peerValue.name);
            return comparisonValue == 0 ? descriptionValue.compareTo(peerValue.descriptionValue) : comparisonValue;
        }
        public boolean equals(Object peerValue) { return peerValue instanceof MethodReference && compareTo((MethodReference) peerValue) == 0; }
        public int hashCode() { return Objects.hash(ownerValue, name, descriptionValue); }
    }
    static final class ClassData {
        final int[] constantKind;
        final Object[] constantData;
        final String name;
        final List<MemberData> fieldValue, functionValue;
        ClassData(Path path) throws IOException {
            DataReader readerValue = new DataReader(Files.readAllBytes(path));
            if (readerValue.readInt() != 0xcafebabe) throw new TranslationError("Java classValue 표식이 아님");
            readerValue.read(4);
            int itemCount = readerValue.readShort(); constantKind = new int[itemCount]; constantData = new Object[itemCount];
            for (int ordinalIndex = 1; ordinalIndex < itemCount; ordinalIndex++) {
                int kindValue = readerValue.readByte(); constantKind[ordinalIndex] = kindValue;
                switch (kindValue) {
                    case 1:
                        int lengthValue = readerValue.readShort();
                        byte[] characterBuffer = readerValue.read(lengthValue), lengthPrefixedData = new byte[lengthValue + 2];
                        lengthPrefixedData[0] = (byte)(lengthValue >> 8); lengthPrefixedData[1] = (byte)lengthValue;
                        System.arraycopy(characterBuffer, 0, lengthPrefixedData, 2, lengthValue);
                        constantData[ordinalIndex] = new DataInputStream(new ByteArrayInputStream(lengthPrefixedData)).readUTF(); break;
                    case 3: constantData[ordinalIndex] = readerValue.readInt(); break;
                    case 4: readerValue.read(4); break;
                    case 5: case 6: readerValue.read(8); ordinalIndex++; break;
                    case 7: case 8: case 16: constantData[ordinalIndex] = readerValue.readShort(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        constantData[ordinalIndex] = new int[]{readerValue.readShort(), readerValue.readShort()}; break;
                    case 15: constantData[ordinalIndex] = new int[]{readerValue.readByte(), readerValue.readShort()}; break;
                    default: throw new TranslationError("지원하지 않는 constantValue kindValue: " + kindValue);
                }
            }
            readerValue.readShort(); name = className(readerValue.readShort());
            if (!className(readerValue.readShort()).equals("java/lang/Object") || readerValue.readShort() != 0)
                throw new TranslationError(name + ": 상속 및 인터페이스 isUnsupported");
            fieldValue = readMembers(readerValue); functionValue = readMembers(readerValue); readAttributes(readerValue);
            if (readerValue.position != readerValue.data.length) throw new TranslationError("classValue 뒤에 남은 data");
        }
        String Characters(int index) {
            if (index < 1 || index >= constantKind.length || constantKind[index] != 1) throw new TranslationError("Characters constantValue index error");
            return (String) constantData[index];
        }
        String className(int index) {
            if (index < 1 || index >= constantKind.length || constantKind[index] != 7) throw new TranslationError("classValue reference error");
            return Characters((Integer)constantData[index]);
        }
        MethodReference reference(int index) {
            if (index < 1 || index >= constantKind.length || constantKind[index] < 9 || constantKind[index] > 11) throw new TranslationError("멤버 reference error");
            int[] pairValue = (int[])constantData[index], namePair = (int[])constantData[pairValue[1]];
            return new MethodReference(className(pairValue[0]), Characters(namePair[0]), Characters(namePair[1]));
        }
        Map<String, byte[]> readAttributes(DataReader readerValue) {
            Map<String, byte[]> result = new LinkedHashMap<>();
            int itemCount = readerValue.readShort();
            for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) {
                String attributeName = Characters(readerValue.readShort()); byte[] value = readerValue.read(readerValue.readInt());
                if (result.put(attributeName, value) != null) throw new TranslationError("겹친 attributeValue: " + attributeName);
            }
            return result;
        }
        List<MemberData> readMembers(DataReader readerValue) {
            List<MemberData> result = new ArrayList<>(); int itemCount = readerValue.readShort();
            for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) {
                int accessEntry = readerValue.readShort(); String methodEntryName = Characters(readerValue.readShort()), descriptionValue = Characters(readerValue.readShort());
                result.add(new MemberData(accessEntry, methodEntryName, descriptionValue, readAttributes(readerValue)));
            }
            return result;
        }
    }
    static final class MethodDescriptor {
        final List<String> arguments = new ArrayList<>();
        final String returnResult;
        MethodDescriptor(String descriptionValue) {
            if (!descriptionValue.startsWith("(")) throw new TranslationError("functionValue descriptionValue error: " + descriptionValue);
            int ending = descriptionValue.indexOf(')'); if (ending < 0) throw new TranslationError("functionValue descriptionValue error: " + descriptionValue);
            arguments.addAll(parseTypes(descriptionValue.substring(1, ending)));
            List<String> returnedValues = parseTypes(descriptionValue.substring(ending + 1));
            if (arguments.contains("V") || returnedValues.size() != 1) throw new TranslationError("functionValue descriptionValue error: " + descriptionValue);
            returnResult = returnedValues.get(0);
        }
    }
    static List<String> parseTypes(String descriptionValue) {
        List<String> result = new ArrayList<>();
        String[] allowedFormat = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int position = 0; position < descriptionValue.length();) {
            String selectionValue = null;
            for (String formatValue : allowedFormat) if (descriptionValue.startsWith(formatValue, position)) { selectionValue = formatValue; break; }
            if (selectionValue == null) throw new TranslationError("지원하지 않는 dataType: " + descriptionValue);
            result.add(selectionValue); position += selectionValue.length();
        }
        return result;
    }
    static String symbol(String kindValue, String... parts) {
        try {
            byte[] hashFile = MessageDigest.getInstance("SHA-256").digest(String.join("\0", parts).getBytes(StandardCharsets.UTF_8));
            StringBuilder text = new StringBuilder("j_" + kindValue + "_");
            for (int ordinalIndex = 0; ordinalIndex < 12; ordinalIndex++) text.append(String.format(Locale.ROOT, "%02x", hashFile[ordinalIndex] & 255));
            return text.toString();
        } catch (Exception error) { throw new TranslationError(error.toString()); }
    }
    final Map<String, ClassData> classesList = new TreeMap<>();
    final Map<MethodReference, MemberData> methodsList = new TreeMap<>(), fieldsList = new TreeMap<>();
    final Map<String, String> stringValues = new LinkedHashMap<>(), machineFunctions = new LinkedHashMap<>();
    final String executionTarget, machineClass;
    final int heapWordCount;
    final Path resourcePath;
    AheadOfTimeCompiler(List<Path> pathList, String targetValue, int lexicalWordCount, Path resourceValue) throws IOException {
        if ((!targetValue.equals("kernel") && !targetValue.equals("user")) || lexicalWordCount < 1024 || lexicalWordCount > 1048576) throw new TranslationError("executeCommand targetValue 또는 memoryValue addressRegion size error");
        executionTarget = targetValue; heapWordCount = lexicalWordCount; resourcePath = resourceValue;
        // This name is also translated when generating each country's sources.
        machineClass = targetValue.equals("kernel") ? "Board" : "User";
        for (String line : Files.readAllLines(resourceValue.resolve("MachineFunctions.tsv"), StandardCharsets.UTF_8)) {
            String[] parts = line.split("\t", -1);
            if (parts.length != 4) throw new TranslationError("machine functionValue data error");
            if (parts[0].equals(targetValue)) machineFunctions.put(parts[1] + parts[2], parts[3]);
        }
        for (Path path : pathList) {
            ClassData data = new ClassData(path);
            if (classesList.put(data.name, data) != null) throw new TranslationError("중복 classValue: " + data.name);
            for (MemberData fieldValue : data.fieldValue) {
                if ((fieldValue.accessEntry & 8) == 0 || parseTypes(fieldValue.descriptionValue).equals(Collections.singletonList("V"))) throw new TranslationError("staticValue 필드만 supportValue");
                if (fieldsList.put(new MethodReference(data.name, fieldValue.name, fieldValue.descriptionValue), fieldValue) != null) throw new TranslationError("중복 fieldValue");
            }
            for (MemberData functionValue : data.functionValue) {
                if (functionValue.name.equals("<init>")) continue;
                if ((functionValue.accessEntry & 8) == 0 || (functionValue.accessEntry & (0x20 | 0x400)) != 0) throw new TranslationError("staticValue 비동기화 함수만 supportValue");
                new MethodDescriptor(functionValue.descriptionValue);
                if (methodsList.put(new MethodReference(data.name, functionValue.name, functionValue.descriptionValue), functionValue) != null) throw new TranslationError("중복 functionValue");
            }
        }
    }
    String stringSymbol(String text) { return stringValues.computeIfAbsent(text, value -> "j_text_" + stringValues.size()); }
    String constantExpression(ClassData data, int index) {
        if (index < 1 || index >= data.constantKind.length) throw new TranslationError("constantValue index clip error");
        if (data.constantKind[index] == 3) return "(word)(uint32_t)(" + data.constantData[index] + ")";
        if (data.constantKind[index] == 8) return "(word)" + stringSymbol(data.Characters((Integer)data.constantData[index]));
        throw new TranslationError("정수와 stringValue 상수만 supportValue");
    }
    String methodPrototype(MethodReference reference) {
        List<String> argumentsList = new ArrayList<>(); int itemCount = new MethodDescriptor(reference.descriptionValue).arguments.size();
        for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) argumentsList.add("word a" + ordinalIndex);
        return "static word " + symbol("method", reference.parts()) + "(" + (itemCount == 0 ? "void" : String.join(", ", argumentsList)) + ")";
    }
    void checkLocal(int index, int localVariableCount) { if (index < 0 || index >= localVariableCount) throw new TranslationError("localScope variableValue index clip error"); }
    void emitBranch(List<String> Output, Set<Integer> branchList, int position, int movementAmount, String condition) {
        int destinationValue = position + movementAmount; branchList.add(destinationValue);
        Output.add((condition == null ? "" : "if (" + condition + ") ") + "goto b" + destinationValue + ";");
    }
    String methodBody(MethodReference functionValue, MemberData data) {
        byte[] bodyData = data.attributeValue.get("Code"); if (bodyData == null) throw new TranslationError("functionValue 몸체가 missingMethod: " + functionValue.name);
        DataReader readerValue = new DataReader(bodyData); int stackDepth = readerValue.readShort(), localVariableCount = readerValue.readShort();
        DataReader commandData = new DataReader(readerValue.read(readerValue.readInt()));
        if (readerValue.readShort() != 0) throw new TranslationError("try/catch/finally isUnsupported");
        MethodDescriptor formatValue = new MethodDescriptor(functionValue.descriptionValue); if (localVariableCount < formatValue.arguments.size()) throw new TranslationError("매개변수보다 적은 localScope variableValue");
        ClassData classValue = classesList.get(functionValue.ownerValue);
        List<String> Output = new ArrayList<>(); Output.add(methodPrototype(functionValue) + " {");
        Output.add("word s[" + Math.max(stackDepth, 1) + "], l[" + Math.max(localVariableCount, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int ordinalIndex = 0; ordinalIndex < formatValue.arguments.size(); ordinalIndex++) Output.add("l[" + ordinalIndex + "] = a" + ordinalIndex + ";");
        Set<Integer> boundariesList = new HashSet<>(), branchList = new HashSet<>();
        String[] comparisonsList = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (commandData.position < commandData.data.length) {
            int position = commandData.position, command = commandData.readByte(); boundariesList.add(position); Output.add("b" + position + ":;");
            if (command == 0) continue;
            if (command == 1) Output.add("PUSH(0);");
            else if (command >= 2 && command <= 8) Output.add("PUSH((uint32_t)(" + (command - 3) + "));");
            else if (command == 16 || command == 17) Output.add("PUSH((uint32_t)(" + (command == 16 ? commandData.readSignedByte() : commandData.readSignedShort()) + "));");
            else if (command == 18 || command == 19) Output.add("PUSH(" + constantExpression(classValue, command == 18 ? commandData.readByte() : commandData.readShort()) + ");");
            else if (command == 21 || command == 25 || (command >= 26 && command <= 29) || (command >= 42 && command <= 45)) {
                int index = command == 21 || command == 25 ? commandData.readByte() : command - (command <= 29 ? 26 : 42);
                checkLocal(index, localVariableCount); Output.add("PUSH(l[" + index + "]);");
            } else if (command == 54 || command == 58 || (command >= 59 && command <= 62) || (command >= 75 && command <= 78)) {
                int index = command == 54 || command == 58 ? commandData.readByte() : command - (command <= 62 ? 59 : 75);
                checkLocal(index, localVariableCount); Output.add("l[" + index + "] = POP();");
            } else if (command == 46) Output.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (command == 79) Output.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (command == 87 || command == 88) Output.add(command == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (command >= 89 && command <= 95) {
                int[] itemCounts = {1,2,3,2,3,4,2}; String[] orderList = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int ordinalIndex = 0; ordinalIndex < itemCounts[command - 89]; ordinalIndex++) Output.add("abcd".charAt(ordinalIndex) + " = POP();");
                for (char value : orderList[command - 89].toCharArray()) Output.add("PUSH(" + value + ");");
            } else if (command == 96 || command == 100 || command == 104 || command == 126 || command == 128 || command == 130) {
                String operationValue = command == 96 ? "+" : command == 100 ? "-" : command == 104 ? "*" : command == 126 ? "&" : command == 128 ? "|" : "^";
                Output.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operationValue + " (uint32_t)b);");
            } else if (command == 108 || command == 112) Output.add("b = POP(); a = POP(); PUSH(divide(a,b," + (command == 112 ? 1 : 0) + "));");
            else if (command == 116) Output.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (command == 120 || command == 122 || command == 124) {
                Output.add("b = POP(); a = POP();"); Output.add("PUSH(" + (command == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (command == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (command == 132) {
                int index = commandData.readByte(), incrementAmount = commandData.readSignedByte(); checkLocal(index, localVariableCount);
                Output.add("l[" + index + "] = (uint32_t)l[" + index + "] + (uint32_t)(" + incrementAmount + ");");
            } else if (command >= 145 && command <= 147) Output.add("a = POP(); PUSH((uint32_t)(" + (command == 145 ? "int8_t" : command == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (command >= 153 && command <= 158) {
                Output.add("a = POP();"); emitBranch(Output, branchList, position, commandData.readSignedShort(), "(int32_t)a " + comparisonsList[command - 153] + " 0");
            } else if (command >= 159 && command <= 166) {
                Output.add("b = POP(); a = POP();"); emitBranch(Output, branchList, position, commandData.readSignedShort(), command >= 165 ? "a " + comparisonsList[command - 159] + " b" : "(int32_t)a " + comparisonsList[command - 159] + " (int32_t)b");
            } else if (command == 167 || command == 200) emitBranch(Output, branchList, position, command == 167 ? commandData.readSignedShort() : commandData.readInt(), null);
            else if (command == 170 || command == 171) {
                while (commandData.position % 4 != 0) commandData.readByte();
                int defaultValue = commandData.readInt(); Output.add("a = POP();");
                if (command == 170) {
                    int bottomValue = commandData.readInt(), topValue = commandData.readInt(); long itemCount = (long)topValue - bottomValue + 1;
                    if (itemCount < 1 || itemCount > (commandData.data.length - commandData.position) / 4) throw new TranslationError("switch clip error");
                    for (long value = bottomValue; value <= topValue; value++) emitBranch(Output, branchList, position, commandData.readInt(), "(int32_t)a == (" + value + ")");
                } else {
                    int itemCount = commandData.readInt(), frontData = 0;
                    if (itemCount < 0 || itemCount > (commandData.data.length - commandData.position) / 8) throw new TranslationError("switch size error");
                    for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) {
                        int value = commandData.readInt(); if (ordinalIndex > 0 && value <= frontData) throw new TranslationError("switch orderValue error"); frontData = value;
                        emitBranch(Output, branchList, position, commandData.readInt(), "(int32_t)a == (" + value + ")");
                    }
                }
                emitBranch(Output, branchList, position, defaultValue, null);
            } else if (command == 172 || command == 176 || command == 177) Output.add("return " + (command == 177 ? "0" : "POP()") + ";");
            else if (command == 178 || command == 179) {
                MethodReference reference = classValue.reference(commandData.readShort()); if (!fieldsList.containsKey(reference)) throw new TranslationError("알 number 없는 fieldValue");
                Output.add(symbol("init", reference.ownerValue) + "();"); String fieldValue = symbol("field", reference.parts());
                Output.add(command == 178 ? "PUSH(" + fieldValue + ");" : fieldValue + " = POP();");
            } else if (command == 184) {
                MethodReference reference = classValue.reference(commandData.readShort()); if (!methodsList.containsKey(reference)) throw new TranslationError("알 number 없는 functionValue");
                MethodDescriptor invocationType = new MethodDescriptor(reference.descriptionValue); int itemCount = invocationType.arguments.size();
                Output.add(symbol("init", reference.ownerValue) + "();"); Output.add("if(sp < " + itemCount + ") kernel_panic(\"call stack underflow\"); sp -= " + itemCount + ";");
                List<String> invocationArguments = new ArrayList<>(); for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) invocationArguments.add("s[sp + " + ordinalIndex + "]");
                Output.add("a = " + symbol("method", reference.parts()) + "(" + String.join(",", invocationArguments) + ");");
                if (!invocationType.returnResult.equals("V")) Output.add("PUSH(a);");
            } else if (command == 182) {
                MethodReference reference = classValue.reference(commandData.readShort());
                if (reference.equals(new MethodReference("java/lang/String", "length", "()I"))) Output.add("a = POP(); PUSH(length(a));");
                else if (reference.equals(new MethodReference("java/lang/String", "charAt", "(I)C"))) Output.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new TranslationError("가상 functionValue invoke isUnsupported");
            } else if (command == 188) {
                if (commandData.readByte() != 10) throw new TranslationError("new int[]만 supportValue"); Output.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (command == 190) Output.add("a = POP(); PUSH(length(a));");
            else if (command == 196) {
                int extensionValue = commandData.readByte(), index = commandData.readShort(); checkLocal(index, localVariableCount);
                if (extensionValue == 21 || extensionValue == 25) Output.add("PUSH(l[" + index + "]);");
                else if (extensionValue == 54 || extensionValue == 58) Output.add("l[" + index + "] = POP();");
                else if (extensionValue == 132) Output.add("l[" + index + "] = (uint32_t)l[" + index + "] + (uint32_t)(" + commandData.readSignedShort() + ");");
                else throw new TranslationError("isUnsupported wide command");
            } else if (command == 198 || command == 199) {
                Output.add("a = POP();"); emitBranch(Output, branchList, position, commandData.readSignedShort(), "a " + (command == 198 ? "==" : "!=") + " 0");
            } else throw new TranslationError(functionValue.ownerValue + "." + functionValue.name + ", byteValue " + position + ": isUnsupported command " + command);
        }
        if (!boundariesList.containsAll(branchList)) throw new TranslationError("command 경계가 아닌 곳으로 branch");
        Output.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Output);
    }
    String exportMethod(String linkSymbol, String targetValue, boolean hasEntryPoint) {
        int positionIndex = targetValue.lastIndexOf('.'); if (positionIndex < 0 || !linkSymbol.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new TranslationError("emitValue assignValue error");
        String ownerValue = targetValue.substring(0, positionIndex).replace('.', '/'), name = targetValue.substring(positionIndex + 1); MethodReference selectionValue = null;
        for (MethodReference reference : methodsList.keySet()) if (reference.ownerValue.equals(ownerValue) && reference.name.equals(name)) {
            if (selectionValue != null) throw new TranslationError("겹친 emitValue targetValue"); selectionValue = reference;
        }
        if (selectionValue == null || (methodsList.get(selectionValue).accessEntry & 0x100) != 0) throw new TranslationError("내보낼 함수가 missingMethod 또는 native functionValue");
        MethodDescriptor formatValue = new MethodDescriptor(selectionValue.descriptionValue);
        if ((hasEntryPoint && !formatValue.arguments.isEmpty()) || !Arrays.asList("V", "I").contains(formatValue.returnResult)) throw new TranslationError("entryPointValue 또는 C boundaryValue formatValue error");
        List<String> argumentsList = new ArrayList<>(), invocationArguments = new ArrayList<>();
        for (int ordinalIndex = 0; ordinalIndex < formatValue.arguments.size(); ordinalIndex++) {
            if (!formatValue.arguments.get(ordinalIndex).equals("I")) throw new TranslationError("C 경계는 int 인수만 supportValue");
            argumentsList.add("int32_t a" + ordinalIndex); invocationArguments.add("(uint32_t)a" + ordinalIndex);
        }
        return (formatValue.returnResult.equals("V") ? "void " : "int32_t ") + linkSymbol + "(" + (argumentsList.isEmpty() ? "void" : String.join(",", argumentsList)) + ") { " + symbol("init", selectionValue.ownerValue) + "(); " + (formatValue.returnResult.equals("V") ? "" : "return (int32_t)") + symbol("method", selectionValue.parts()) + "(" + String.join(",", invocationArguments) + "); }";
    }
    String generate(String entryPoint, List<String> exportEntries, boolean universalNotation) throws IOException {
        List<String> declarationsList = new ArrayList<>(), bodiesList = new ArrayList<>(), fieldDeclarations = new ArrayList<>();
        for (Map.Entry<MethodReference, MemberData> entryValue : methodsList.entrySet()) {
            MethodReference reference = entryValue.getKey(); MemberData data = entryValue.getValue(); declarationsList.add(methodPrototype(reference) + ";");
            if ((data.accessEntry & 0x100) != 0) {
                String connect = machineFunctions.get(reference.name + reference.descriptionValue);
                if (!reference.ownerValue.equals(machineClass) || connect == null) throw new TranslationError("허용되지 않은 native functionValue: " + reference.name);
                int itemCount = new MethodDescriptor(reference.descriptionValue).arguments.size(); List<String> argumentsList = new ArrayList<>();
                for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) argumentsList.add("a" + ordinalIndex);
                declarationsList.add("extern word " + connect + "(" + (itemCount == 0 ? "void" : String.join(",", Collections.nCopies(itemCount, "word"))) + ");");
                bodiesList.add(methodPrototype(reference) + " { return " + connect + "(" + String.join(",", argumentsList) + "); }");
            } else bodiesList.add(methodBody(reference, data));
        }
        for (Map.Entry<MethodReference, MemberData> entryValue : fieldsList.entrySet()) {
            MethodReference reference = entryValue.getKey(); byte[] constantValue = entryValue.getValue().attributeValue.get("ConstantValue");
            String value = constantValue == null ? "0" : constantExpression(classesList.get(reference.ownerValue), new DataReader(constantValue).readShort());
            fieldDeclarations.add("static word " + symbol("field", reference.parts()) + " = " + value + ";");
        }
        for (String name : classesList.keySet()) {
            String initialize = symbol("init", name), stateValue = symbol("state", name);
            declarationsList.add("static void " + initialize + "(void);"); fieldDeclarations.add("static unsigned " + stateValue + ";");
            MethodReference reference = new MethodReference(name, "<clinit>", "()V");
            bodiesList.add("static void " + initialize + "(void) { if(" + stateValue + ") return; " + stateValue + " = 1; " + (methodsList.containsKey(reference) ? symbol("method", reference.parts()) + "(); " : "") + stateValue + " = 2; }");
        }
        bodiesList.add(exportMethod("java_entry", entryPoint, true)); Set<String> exportedName = new HashSet<>();
        for (String assignValue : exportEntries) {
            int positionIndex = assignValue.indexOf('='); if (positionIndex < 1) throw new TranslationError("emitValue assignValue error");
            String name = assignValue.substring(0, positionIndex); exportedName.add(name); bodiesList.add(exportMethod(name, assignValue.substring(positionIndex + 1), false));
        }
        List<String> stringDeclarations = new ArrayList<>();
        for (Map.Entry<String, String> entryValue : stringValues.entrySet()) {
            String text = entryValue.getKey(); StringBuilder arrayValue = new StringBuilder("static const word " + entryValue.getValue() + "[] = {" + text.length());
            for (int ordinalIndex = 0; ordinalIndex < text.length(); ordinalIndex++) arrayValue.append(", ").append((int)text.charAt(ordinalIndex));
            stringDeclarations.add(arrayValue.append("};").toString());
        }
        String supportValue = Files.readString(resourcePath.resolve("RuntimeSupport.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heapWordCount));
        return localizeGeneratedSource(supportValue + String.join("\n", stringDeclarations) + "\n" + String.join("\n", declarationsList) + "\n" + String.join("\n", fieldDeclarations) + "\n" + String.join("\n", bodiesList) + "\n", exportedName, universalNotation);
    }
    String localizeGeneratedSource(String source, Set<String> exportedName, boolean universalNotation) throws IOException {
        Map<String, String> nameTable = new HashMap<>();
        for (String line : Files.readAllLines(resourcePath.resolve("GeneratedNames.tsv"), StandardCharsets.UTF_8)) {
            String[] pairValue = line.split("\t"); nameTable.put(pairValue[0], pairValue[1]);
        }
        Pattern chunkExpression = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher finderValue = chunkExpression.matcher(source); StringBuffer result = new StringBuffer();
        while (finderValue.find()) {
            String name = finderValue.group(), newName = name;
            if (!name.startsWith("//") && !name.startsWith("/*") && !name.startsWith("\"") && !name.startsWith("'") && !exportedName.contains(name)) {
                newName = nameTable.getOrDefault(name, name);
                if (name.matches("a[0-9]+")) newName = "arguments" + name.substring(1);
                if (name.matches("b[0-9]+")) newName = "branch" + name.substring(1);
                if (universalNotation) {
                    StringBuilder notationValue = new StringBuilder();
                    for (char characterValue : newName.toCharArray()) notationValue.append(characterValue < 128 ? Character.toString(characterValue) : String.format(Locale.ROOT, "\\u%04x", (int)characterValue));
                    newName = notationValue.toString();
                }
            }
            finderValue.appendReplacement(result, Matcher.quoteReplacement(newName));
        }
        finderValue.appendTail(result); return result.toString();
    }
    String x86MethodBody(MethodReference functionValue, MemberData data, Map<String,String> machineTable, String targetValue) {
        String markerValue = symbol("method", functionValue.parts());
        List<String> line = new ArrayList<>();
        if ((data.accessEntry & 0x100) != 0) {
            String connect = machineTable.get(functionValue.name + functionValue.descriptionValue);
            if (!functionValue.ownerValue.equals(targetValue.equals("kernel") ? "deviceValue" : "User") || connect == null) throw new TranslationError("허용되지 않은 native functionValue");
            return ".text\n" + markerValue + ":\njmp " + connect;
        }
        byte[] bodyText = data.attributeValue.get("Code"); if (bodyText == null) throw new TranslationError("functionValue 몸체가 missingMethod");
        DataReader readerValue = new DataReader(bodyText); readerValue.readShort(); int localCount = readerValue.readShort();
        DataReader commandData = new DataReader(readerValue.read(readerValue.readInt()));
        if (readerValue.readShort() != 0) throw new TranslationError("try/catch/finally isUnsupported");
        MethodDescriptor formatValue = new MethodDescriptor(functionValue.descriptionValue); if (localCount < formatValue.arguments.size()) throw new TranslationError("매개변수보다 적은 localScope variableValue");
        Collections.addAll(line,".text",".globl " + markerValue,".type " + markerValue + ", @function",markerValue + ":","pushl %ebp","movl %esp, %ebp","subl $" + localCount * 4 + ", %esp");
        for (int ordinalIndex = 0; ordinalIndex < formatValue.arguments.size(); ordinalIndex++) Collections.addAll(line,"movl " + (8 + 4 * (formatValue.arguments.size() - ordinalIndex - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (ordinalIndex + 1)) + "(%ebp)");
        ClassData classValue = classesList.get(functionValue.ownerValue); Set<Integer> boundariesList = new HashSet<>(), branchList = new HashSet<>();
        String[] comparisonsList = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (commandData.position < commandData.data.length) {
            int position = commandData.position, command = commandData.readByte(); String positionIndex = markerValue + "_b" + position;
            line.add(positionIndex + ":"); boundariesList.add(position);
            if (command == 0) line.add("nop");
            else if (command == 1) line.add("pushl $0");
            else if (command >= 2 && command <= 8) line.add("pushl $" + (command - 3));
            else if (command == 16 || command == 17) line.add("pushl $" + (command == 16 ? commandData.readSignedByte() : commandData.readSignedShort()));
            else if (command == 18 || command == 19) {
                int index = command == 18 ? commandData.readByte() : commandData.readShort();
                line.add("pushl $" + x86Constant(classValue,index));
            } else if (command == 21 || command == 25 || (command >= 26 && command <= 29) || (command >= 42 && command <= 45) || command == 54 || command == 58 || (command >= 59 && command <= 62) || (command >= 75 && command <= 78)) {
                boolean readResult = command < 54; int index = command == 21 || command == 25 || command == 54 || command == 58 ? commandData.readByte() : command - (command <= 29 ? 26 : command <= 45 ? 42 : command <= 62 ? 59 : 75);
                checkLocal(index,localCount); line.add((readResult ? "pushl " : "popl ") + "-" + (4 * (index + 1)) + "(%ebp)");
            } else if (command == 46) Collections.addAll(line,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (command == 79) Collections.addAll(line,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (command == 87 || command == 88) line.add("addl $" + (command == 87 ? 4 : 8) + ", %esp");
            else if (command >= 89 && command <= 95) {
                int[] itemCounts = {1,2,3,2,3,4,2}; int[][] orderList = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] registerValues = {"%eax","%ecx","%edx","%ebx"};
                for (int ordinalIndex = 0; ordinalIndex < itemCounts[command - 89]; ordinalIndex++) line.add("popl " + registerValues[ordinalIndex]);
                for (int ordinalIndex : orderList[command - 89]) line.add("pushl " + registerValues[ordinalIndex]);
            } else if (command == 96 || command == 100 || command == 104 || command == 126 || command == 128 || command == 130) {
                String operationValue = command == 96 ? "addl" : command == 100 ? "subl" : command == 104 ? "imull" : command == 126 ? "andl" : command == 128 ? "orl" : "xorl";
                Collections.addAll(line,"popl %ecx","popl %eax",operationValue + " %ecx, %eax","pushl %eax");
            } else if (command == 108 || command == 112) Collections.addAll(line,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + positionIndex + "_divide","cmpl $0x80000000, %eax","jne " + positionIndex + "_divide","xorl %edx, %edx","jmp " + positionIndex + "_done",positionIndex + "_divide:","cltd","idivl %ecx",positionIndex + "_done:","pushl " + (command == 108 ? "%eax" : "%edx"));
            else if (command == 116) line.add("negl (%esp)");
            else if (command == 120 || command == 122 || command == 124) Collections.addAll(line,"popl %ecx","popl %eax",(command == 120 ? "sall" : command == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (command == 132) {
                int index = commandData.readByte(), incrementValue = commandData.readSignedByte(); checkLocal(index,localCount); line.add("addl $" + incrementValue + ", -" + (4 * (index + 1)) + "(%ebp)");
            } else if (command >= 145 && command <= 147) Collections.addAll(line,"popl %eax",command == 145 ? "movsbl %al, %eax" : command == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (command >= 153 && command <= 166) {
                if (command <= 158) Collections.addAll(line,"popl %eax","testl %eax, %eax");
                else Collections.addAll(line,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int destinationValue = position + commandData.readSignedShort(); branchList.add(destinationValue); line.add(comparisonsList[command - (command <= 158 ? 153 : 159)] + " " + markerValue + "_b" + destinationValue);
            } else if (command == 167 || command == 200) {
                int destinationValue = position + (command == 167 ? commandData.readSignedShort() : commandData.readInt()); branchList.add(destinationValue); line.add("jmp " + markerValue + "_b" + destinationValue);
            } else if (command == 170 || command == 171) {
                while (commandData.position % 4 != 0) commandData.readByte();
                int defaultValue = position + commandData.readInt(); branchList.add(defaultValue); line.add("popl %eax");
                int itemCount, bottomValue = 0;
                if (command == 170) { bottomValue = commandData.readInt(); int topValue = commandData.readInt(); long lengthValue = (long)topValue - bottomValue + 1; if (lengthValue < 1 || lengthValue > (commandData.data.length - commandData.position) / 4) throw new TranslationError("switch clip error"); itemCount = (int)lengthValue; }
                else { itemCount = commandData.readInt(); if (itemCount < 0 || itemCount > (commandData.data.length - commandData.position) / 8) throw new TranslationError("switch size error"); }
                for (int ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) {
                    int value = command == 170 ? bottomValue + ordinalIndex : commandData.readInt(), destinationValue = position + commandData.readInt(); branchList.add(destinationValue);
                    Collections.addAll(line,"cmpl $" + value + ", %eax","je " + markerValue + "_b" + destinationValue);
                }
                line.add("jmp " + markerValue + "_b" + defaultValue);
            } else if (command == 172 || command == 176 || command == 177) {
                if (command != 177) line.add("popl %eax"); Collections.addAll(line,"leave","ret");
            } else if (command == 178 || command == 179) {
                MethodReference reference = classValue.reference(commandData.readShort()); if (!fieldsList.containsKey(reference)) throw new TranslationError("알 number 없는 fieldValue");
                Collections.addAll(line,"call " + symbol("init",reference.ownerValue),(command == 178 ? "pushl " : "popl ") + symbol("field",reference.parts()));
            } else if (command == 184) {
                MethodReference reference = classValue.reference(commandData.readShort()); if (!methodsList.containsKey(reference)) throw new TranslationError("알 number 없는 functionValue");
                MethodDescriptor invocationType = new MethodDescriptor(reference.descriptionValue); Collections.addAll(line,"call " + symbol("init",reference.ownerValue),"call " + symbol("method",reference.parts()));
                if (!invocationType.arguments.isEmpty()) line.add("addl $" + invocationType.arguments.size() * 4 + ", %esp");
                if (!invocationType.returnResult.equals("V")) line.add("pushl %eax");
            } else if (command == 182) {
                MethodReference reference = classValue.reference(commandData.readShort());
                if (reference.equals(new MethodReference("java/lang/String","length","()I"))) Collections.addAll(line,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (reference.equals(new MethodReference("java/lang/String","charAt","(I)C"))) Collections.addAll(line,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new TranslationError("가상 functionValue invoke isUnsupported");
            } else if (command == 188) {
                if (commandData.readByte() != 10) throw new TranslationError("new int[]만 supportValue"); Collections.addAll(line,"popl %eax","call rt_new_array","pushl %eax");
            } else if (command == 190) Collections.addAll(line,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (command == 196) {
                int extensionValue = commandData.readByte(), index = commandData.readShort(); checkLocal(index,localCount);
                if (extensionValue == 21 || extensionValue == 25 || extensionValue == 54 || extensionValue == 58) line.add((extensionValue <= 25 ? "pushl " : "popl ") + "-" + 4 * (index + 1) + "(%ebp)");
                else if (extensionValue == 132) line.add("addl $" + commandData.readSignedShort() + ", -" + 4 * (index + 1) + "(%ebp)");
                else throw new TranslationError("wide command isUnsupported");
            } else if (command == 198 || command == 199) {
                int destinationValue = position + commandData.readSignedShort(); branchList.add(destinationValue); Collections.addAll(line,"popl %eax","testl %eax, %eax",(command == 198 ? "je " : "jne ") + markerValue + "_b" + destinationValue);
            } else throw new TranslationError("isUnsupported command: " + command);
        }
        if (!boundariesList.containsAll(branchList)) throw new TranslationError("command 경계가 아닌 곳으로 branch");
        line.add(".size " + markerValue + ", .-" + markerValue); return String.join("\n",line);
    }
    String x86Constant(ClassData data, int index) {
        if (data.constantKind[index] == 3) return data.constantData[index].toString();
        if (data.constantKind[index] == 8) return stringSymbol(data.Characters((Integer)data.constantData[index]));
        throw new TranslationError("정수와 stringValue 상수만 supportValue");
    }
    String x86Assembly(String entryPoint, List<String> exportedValue, String targetValue) throws IOException {
        Map<String,String> machineTable = new HashMap<>();
        for (String line : Files.readAllLines(resourcePath.resolve("X86MachineFunctions.tsv"))) { String[] pairValue = line.split("\t"); if (pairValue[0].equals(targetValue)) machineTable.put(pairValue[1] + pairValue[2],pairValue[3]); }
        int positionIndex = entryPoint.lastIndexOf('.'); if (positionIndex < 0) throw new TranslationError("entryPoint assignValue error");
        String ownerValue = entryPoint.substring(0,positionIndex).replace('.','/'), methodEntryName = entryPoint.substring(positionIndex + 1); MethodReference entryPointValue = null;
        for (String descriptionValue : Arrays.asList("()I","()V")) { MethodReference reference = new MethodReference(ownerValue,methodEntryName,descriptionValue); if (methodsList.containsKey(reference)) { if (entryPointValue != null) throw new TranslationError("겹친 entryPoint"); entryPointValue = reference; } }
        if (entryPointValue == null || (methodsList.get(entryPointValue).accessEntry & 0x100) != 0) throw new TranslationError("entryPointValue functionValue formatValue error");
        List<String> line = new ArrayList<>(); line.add(".code32");
        for (ClassData data : classesList.values()) {
            String stateValue = symbol("state",data.name), initialize = symbol("init",data.name);
            Collections.addAll(line,".bss",".balign 4",stateValue + ": .long 0",".text",initialize + ":","cmpl $0, " + stateValue,"jne " + initialize + "_done","movl $1, " + stateValue);
            MethodReference initializerReference = new MethodReference(data.name,"<clinit>","()V"); if (methodsList.containsKey(initializerReference)) line.add("call " + symbol("method",initializerReference.parts()));
            Collections.addAll(line,"movl $2, " + stateValue,initialize + "_done:","ret");
            for (MemberData fieldValue : data.fieldValue) {
                byte[] constantValue = fieldValue.attributeValue.get("ConstantValue"); String value = constantValue == null ? "0" : x86Constant(data,new DataReader(constantValue).readShort());
                Collections.addAll(line,".data",".balign 4",symbol("field",data.name,fieldValue.name,fieldValue.descriptionValue) + ": .long " + value);
            }
            for (MemberData functionValue : data.functionValue) if (!functionValue.name.equals("<init>")) line.add(x86MethodBody(new MethodReference(data.name,functionValue.name,functionValue.descriptionValue),functionValue,machineTable,targetValue));
        }
        Collections.addAll(line,".text",".globl java_entry","java_entry:","call " + symbol("init",entryPointValue.ownerValue),"call " + symbol("method",entryPointValue.parts()));
        if (entryPointValue.descriptionValue.equals("()V")) line.add("xorl %eax, %eax"); line.add("ret");
        for (String assignValue : exportedValue) {
            int delimiterValue = assignValue.indexOf('='); if (delimiterValue < 1) throw new TranslationError("emitValue assignValue error");
            String externalValue = assignValue.substring(0,delimiterValue), functionValue = assignValue.substring(delimiterValue + 1); int divisionResult = functionValue.lastIndexOf('.');
            if (divisionResult < 0 || !externalValue.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new TranslationError("emitValue symbol error");
            String classValue = functionValue.substring(0,divisionResult).replace('.','/'), name = functionValue.substring(divisionResult + 1); MethodReference selectionValue = null;
            for (MethodReference reference : methodsList.keySet()) if (reference.ownerValue.equals(classValue) && reference.name.equals(name)) { if (selectionValue != null) throw new TranslationError("겹친 emitValue targetValue"); selectionValue = reference; }
            if (selectionValue == null) throw new TranslationError("내보낼 함수가 missingMethod");
            Collections.addAll(line,".text",".globl " + externalValue,externalValue + ":","call " + symbol("init",selectionValue.ownerValue),"jmp " + symbol("method",selectionValue.parts()));
        }
        line.add(".section .rodata");
        for (Map.Entry<String,String> entryValue : stringValues.entrySet()) {
            Collections.addAll(line,".balign 4",entryValue.getValue() + ":",".long " + entryValue.getKey().length());
            List<String> unitsList = new ArrayList<>(); for (char unitValue : entryValue.getKey().toCharArray()) unitsList.add(Integer.toString(unitValue)); if (!unitsList.isEmpty()) line.add(".long " + String.join(",",unitsList));
        }
        line.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",line) + "\n";
    }
    static void executeTool(List<String> command) throws Exception {
        if (new ProcessBuilder(command).inheritIO().start().waitFor() != 0) throw new TranslationError("compileSource error: " + command.get(0));
    }
    static String dataString(String text) { return "\"" + text.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void x86Translation(List<Path> inputList, String targetValue, String entryPoint, List<String> exportedValue, Path Output, Path resourceValue) throws Exception {
        Path temporaryValue = Files.createTempDirectory("jkoros-java-x86-"), classPath = temporaryValue.resolve("classes"); Files.createDirectory(classPath);
        try {
            List<String> javaCommand = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",classPath.toString(),"-sourcepath",classPath.toString(),"-d",classPath.toString()));
            List<Path> bytecode = new ArrayList<>(); int sourceCount = 0;
            for (Path inputValue : inputList) {
                if (Output.toAbsolutePath().normalize().equals(inputValue.toAbsolutePath().normalize())) throw new TranslationError("Output 파일과 입력이 equalText");
                if (inputValue.toString().endsWith(".java")) { javaCommand.add(inputValue.toString()); sourceCount++; }
                else if (inputValue.toString().endsWith(".class")) bytecode.add(inputValue);
                else throw new TranslationError(".java 또는 .class만 supportValue");
            }
            if (sourceCount > 0) executeTool(javaCommand);
            try (java.util.stream.Stream<Path> pathList = Files.walk(classPath)) { pathList.filter(path -> path.toString().endsWith(".class")).sorted().forEach(bytecode::add); }
            AheadOfTimeCompiler convertValue = new AheadOfTimeCompiler(bytecode,targetValue.equals("user") ? "user" : "kernel",262144,resourceValue);
            String assembleValue = convertValue.x86Assembly(entryPoint,exportedValue,targetValue); Files.writeString(temporaryValue.resolve("program.s"),assembleValue,StandardCharsets.UTF_8);
            Path toolPosition = resourceValue.getParent();
            executeTool(Arrays.asList("as","--32","-o",temporaryValue.resolve("program.o").toString(),temporaryValue.resolve("program.s").toString()));
            executeTool(Arrays.asList("as","--32","-o",temporaryValue.resolve("runtime.o").toString(),toolPosition.resolve("RuntimeSupport.s").toString()));
            List<String> connect = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (targetValue.equals("kernel")) connect.add("-r");
            else {
                executeTool(Arrays.asList("as","--32","-o",temporaryValue.resolve("start.o").toString(),toolPosition.resolve(targetValue.equals("user") ? "startUserProgram.s" : "linuxStartup.s").toString()));
                Collections.addAll(connect,"-e","_start",temporaryValue.resolve("start.o").toString());
                if (targetValue.equals("user")) Collections.addAll(connect,"-T",toolPosition.resolve("userLinkLayout.ld").toString());
            }
            Collections.addAll(connect,"-o",temporaryValue.resolve("result").toString(),temporaryValue.resolve("program.o").toString(),temporaryValue.resolve("runtime.o").toString()); executeTool(connect);
            Output = Output.toAbsolutePath(); Files.createDirectories(Output.getParent()); Path publishValue = Files.createTempFile(Output.getParent(),".elf-",".tmp");
            try { Files.copy(temporaryValue.resolve("result"),publishValue,StandardCopyOption.REPLACE_EXISTING); Files.move(publishValue,Output,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publishValue); }
            Files.setPosixFilePermissions(Output,java.nio.file.attribute.PosixFilePermissions.fromString(targetValue.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Output + ".s"),assembleValue,StandardCharsets.UTF_8);
            List<String> symbolData = new ArrayList<>(), sourceData = new ArrayList<>();
            for (MethodReference reference : convertValue.methodsList.keySet()) symbolData.add(dataString(symbol("method",reference.parts())) + ":" + dataString(reference.ownerValue + "." + reference.name + reference.descriptionValue));
            for (Path inputValue : inputList) {
                byte[] hashFile = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(inputValue)); StringBuilder text = new StringBuilder(); for (byte value : hashFile) text.append(String.format(Locale.ROOT,"%02x",value & 255));
                sourceData.add(dataString(inputValue.toAbsolutePath().toString()) + ":" + dataString(text.toString()));
            }
            Files.writeString(Paths.get(Output + ".json"),"{\"target\":" + dataString(targetValue) + ",\"entry\":" + dataString(entryPoint) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",symbolData) + "},\"sources\":{" + String.join(",",sourceData) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> pathList = Files.walk(temporaryValue)) { for (Path path : (Iterable<Path>)pathList.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(path); }
        }
    }
    public static void main(String[] arguments) {
        try {
            String entryPoint = null, targetValue = "kernel", x86Target = null; Path outputPath = null; int lexicalWordCount = 262144; boolean universalNotation = false;
            List<String> exportedValue = new ArrayList<>(); List<Path> pathList = new ArrayList<>();
            for (int ordinalIndex = 0; ordinalIndex < arguments.length; ordinalIndex++) {
                String value = arguments[ordinalIndex];
                switch (value) {
                    case "--target": x86Target = arguments[++ordinalIndex]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry classValue.functionValue -o Output [--target linux|kernel|user] [--profile kernel|user] [--export symbol=classValue.functionValue] 클래스파일 또는 Java원문"); return;
                    case "--entry": entryPoint = arguments[++ordinalIndex]; break;
                    case "--profile": targetValue = arguments[++ordinalIndex]; break;
                    case "--heap-words": lexicalWordCount = Integer.parseInt(arguments[++ordinalIndex]); break;
                    case "--export": exportedValue.add(arguments[++ordinalIndex]); break;
                    case "-o": outputPath = Paths.get(arguments[++ordinalIndex]); break;
                    case "--ucn": universalNotation = true; break;
                    default: if (value.startsWith("-")) throw new TranslationError("알 number 없는 옵션: " + value); pathList.add(Paths.get(value));
                }
            }
            if (entryPoint == null || outputPath == null || pathList.isEmpty()) throw new TranslationError("--entry, -o, classValue 파일이 필요합니다");
            Path resourceValue = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (x86Target != null) {
                if (!Arrays.asList("linux","kernel","user").contains(x86Target)) throw new TranslationError("알 number 없는 executeCommand targetValue");
                x86Translation(pathList,x86Target,entryPoint,exportedValue,outputPath,resourceValue); return;
            }
            String source = new AheadOfTimeCompiler(pathList, targetValue, lexicalWordCount, resourceValue).generate(entryPoint, exportedValue, universalNotation);
            outputPath = outputPath.toAbsolutePath(); Files.createDirectories(outputPath.getParent());
            Path temporaryValue = Files.createTempFile(outputPath.getParent(), ".aot-", ".tmp");
            try { Files.writeString(temporaryValue, source, StandardCharsets.UTF_8); Files.move(temporaryValue, outputPath, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(temporaryValue); }
        } catch (Exception error) { System.err.println("compileSource error: " + error.getMessage()); System.exit(1); }
    }
}
