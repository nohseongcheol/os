// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עצמי 커널의 표준 פלטטקסט. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class פלטטקסט {
    private פלטטקסט() {}
    public static void כתוב(String טקסט) { System.out.print(טקסט); }
    public static void כתיבה_קו(String טקסט) { System.out.println(טקסט); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
