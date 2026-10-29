// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** eget 커널의 표준 Utgang. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Utgang {
    private Utgang() {}
    public static void Skriv(String Tekst) { System.out.print(Tekst); }
    public static void skrive_linje(String Tekst) { System.out.println(Tekst); }
    public static void skrive_nummer(int nummer) { System.out.println(nummer); }
}
