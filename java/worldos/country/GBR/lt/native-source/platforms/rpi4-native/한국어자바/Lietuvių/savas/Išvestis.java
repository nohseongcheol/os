// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** savas 커널의 표준 Išvestis. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Išvestis {
    private Išvestis() {}
    public static void Rašymas(String Tekstas) { System.out.print(Tekstas); }
    public static void rašymas_eilutė(String Tekstas) { System.out.println(Tekstas); }
    public static void rašymas_numeris(int numeris) { System.out.println(numeris); }
}
