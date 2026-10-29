// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
/** 자체 커널의 표준 Aschur. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Aschur {
    private Aschur() {}
    public static void Scríobh(String Téacs) { System.out.print(Téacs); }
    public static void scríobh_líne(String Téacs) { System.out.println(Téacs); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
