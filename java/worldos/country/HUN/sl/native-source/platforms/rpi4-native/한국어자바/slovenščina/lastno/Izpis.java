// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** lastno 커널의 표준 Izpis. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Izpis {
    private Izpis() {}
    public static void Pisanje(String Besedilo) { System.out.print(Besedilo); }
    public static void pisati_linija(String Besedilo) { System.out.println(Besedilo); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
