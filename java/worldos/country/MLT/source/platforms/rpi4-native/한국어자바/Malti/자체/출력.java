// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
/** 자체 커널의 표준 출력. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class 출력 {
    private 출력() {}
    public static void kiteb(String SMS) { System.out.print(SMS); }
    public static void kiteb_linja(String SMS) { System.out.println(SMS); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
