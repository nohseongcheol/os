// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Standard output of the standalone kernel. UTF-16 surrogate pairs are sent as UTF-8 over UART. */
public final class Output {
    private Output() {}
    public static void write(String text) { System.out.print(text); }
    public static void writeLine(String text) { System.out.println(text); }
    public static void writeNumber(int number) { System.out.println(number); }
}
