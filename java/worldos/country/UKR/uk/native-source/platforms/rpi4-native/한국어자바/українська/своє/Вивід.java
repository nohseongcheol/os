// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
/** своє 커널의 표준 Вивід. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Вивід {
    private Вивід() {}
    public static void Запис(String текст) { System.out.print(текст); }
    public static void записування_рядок(String текст) { System.out.println(текст); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
