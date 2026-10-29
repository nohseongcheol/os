// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** 자체 커널의 표준 Allbwn. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Allbwn {
    private Allbwn() {}
    public static void Ysgrifennu(String Testun) { System.out.print(Testun); }
    public static void ysgrifennu_llinell(String Testun) { System.out.println(Testun); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
