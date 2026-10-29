// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Do not select a private helper as the entry point of existing code that has a standard main method. */
public class EntryCompatibilityTest {
    private static void run() { System.out.println("auxiliaryValue functionValue invoke"); }
    public static void main(String[] arguments) {
        run();
        System.out.println("표준 entryPoint retainValue");
    }
}
