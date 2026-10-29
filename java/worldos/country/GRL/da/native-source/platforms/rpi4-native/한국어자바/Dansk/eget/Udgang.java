// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** eget 커널의 표준 Udgang. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Udgang {
    private Udgang() {}
    public static void Skrive(String Tekst) { System.out.print(Tekst); }
    public static void skrive_linje(String Tekst) { System.out.println(Tekst); }
    public static void skrive_tal(int tal) { System.out.println(tal); }
}
