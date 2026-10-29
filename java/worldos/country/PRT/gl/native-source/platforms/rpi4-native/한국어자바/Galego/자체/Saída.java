// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** 자체 커널의 표준 Saída. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Saída {
    private Saída() {}
    public static void Escritura(String Texto) { System.out.print(Texto); }
    public static void escribir_liña(String Texto) { System.out.println(Texto); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
