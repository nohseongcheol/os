// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** eget 커널의 표준 utmatningsposition. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class utmatningsposition {
    private utmatningsposition() {}
    public static void Skriv(String text) { System.out.print(text); }
    public static void skriva_rad(String text) { System.out.println(text); }
    public static void skriva_nummer(int nummer) { System.out.println(nummer); }
}
