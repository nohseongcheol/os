// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Colour {
    public static void main(String[] arguments) throws Exception {
        int sumValue = 0;
        int number = 1;
        while (number <= 10) {
            sumValue = sumValue + number;
            number = number + 1;
        }
        English.Native.Output.writeNumber(sumValue);
        English.Native.file.write("aot.txt", "한글 AOT file 😀");
        English.Native.Output.writeLine(English.Native.file.read("aot.txt"));
    }
}
