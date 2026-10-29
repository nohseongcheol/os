// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 커널의 표준 Exito. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Exito {
    private Exito() {}
    public static void Scribe(String texto) { System.out.print(texto); }
    public static void 줄쓰기(String texto) { System.out.println(texto); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
