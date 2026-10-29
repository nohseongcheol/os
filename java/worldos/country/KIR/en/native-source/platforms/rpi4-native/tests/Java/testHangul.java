// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Native.Characters;
import English.Native.file;
import English.Native.entryList;
import English.Native.Dictionary;
import English.Native.Output;
public class testHangul {
    public static void main(String[] a) throws Exception {
        String Greeting = "안녕하세요 · 日本語 · العربية · 😀";
        Output.writeLine(Characters.decryptData(Characters.encode(Greeting))); Output.writeNumber(Characters.codePointCount("한글😀"));
        file.write("한글자료.txt", Greeting); Output.writeLine(file.read("한글자료.txt"));
        entryList namesList = new entryList(); namesList.addValues("가람"); namesList.addValues("누리"); Output.writeLine(namesList.read(1));
        Dictionary meaningValue = new Dictionary(); meaningValue.putValue("가람", "강"); System.gc(); Output.writeLine(meaningValue.findEntry("가람"));
        try { Characters.decryptData(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Output.writeLine("UTF-8 error rejectValue"); }
        Output.writeLine("English library isComplete");
    }
}
