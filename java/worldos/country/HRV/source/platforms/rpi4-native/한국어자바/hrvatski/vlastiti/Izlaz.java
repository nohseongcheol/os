// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** vlastiti 커널의 표준 Izlaz. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Izlaz {
    private Izlaz() {}
    public static void Zapisuj(String Tekst) { System.out.print(Tekst); }
    public static void zapisivanje_red(String Tekst) { System.out.println(Tekst); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
