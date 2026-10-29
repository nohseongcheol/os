// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class FileExample {
    public static void run() throws English.Native.InputOutputException {
        English.Native.file.write("java.txt", "JAVA file: en 😀\n");
        English.Native.Output.write(English.Native.file.read("java.txt"));
    }
}
