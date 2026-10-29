// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** oma 커널의 표준 Väljund. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Väljund {
    private Väljund() {}
    public static void Kirjutamine(String Tekst) { System.out.print(Tekst); }
    public static void kirjutamine_liin(String Tekst) { System.out.println(Tekst); }
    public static void kirjutamine_number(int number) { System.out.println(number); }
}
