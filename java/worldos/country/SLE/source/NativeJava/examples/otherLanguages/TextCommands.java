// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Java.Characters;

/** Small Java entry point whose results can be read by other languages from standard output. */
public final class TextCommands {
    public static void main(String[] arguments) {
        if (arguments.length != 1) {
            System.err.println("사용법: TextCommands stringValue");
            System.exit(2);
        }
        System.out.println(Characters.codePointCount(arguments[0]));
    }
}
