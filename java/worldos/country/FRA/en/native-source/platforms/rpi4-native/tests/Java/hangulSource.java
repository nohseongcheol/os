// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class hangulSource {
    public static void main(String[] arguments) throws English.Native.InputOutputException {
        English.Native.Output.writeLine("Native 컴파일러와 English library");
        int characterCount = English.Native.Characters.codePointCount("한글😀");
        English.Native.Output.writeNumber(characterCount);
        English.Native.file.write("한글자료.txt", "Native kernelValue 안에서 저장한 한글😀");
        English.Native.Output.writeLine(English.Native.file.read("한글자료.txt"));
    }
}
