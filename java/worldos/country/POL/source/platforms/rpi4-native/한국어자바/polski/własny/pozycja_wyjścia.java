// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** własny 커널의 표준 pozycja_wyjścia. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class pozycja_wyjścia {
    private pozycja_wyjścia() {}
    public static void Zapis(String tekst) { System.out.print(tekst); }
    public static void zapis_linia(String tekst) { System.out.println(tekst); }
    public static void zapis_identyfikator(int identyfikator) { System.out.println(identyfikator); }
}
