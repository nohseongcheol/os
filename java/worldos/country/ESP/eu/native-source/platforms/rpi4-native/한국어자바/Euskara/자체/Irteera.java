// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 자체 커널의 표준 Irteera. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Irteera {
    private Irteera() {}
    public static void Idatzi(String Testua) { System.out.print(Testua); }
    public static void idatzi_lerro(String Testua) { System.out.println(Testua); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
