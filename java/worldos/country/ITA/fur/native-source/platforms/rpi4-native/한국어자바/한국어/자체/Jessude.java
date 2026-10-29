// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 커널의 표준 Jessude. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Jessude {
    private Jessude() {}
    public static void Scrivi(String Test) { System.out.print(Test); }
    public static void 줄쓰기(String Test) { System.out.println(Test); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
