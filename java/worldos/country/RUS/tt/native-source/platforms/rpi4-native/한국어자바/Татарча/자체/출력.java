// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
/** 자체 커널의 표준 출력. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class 출력 {
    private 출력() {}
    public static void язу(String Mäten) { System.out.print(Mäten); }
    public static void язу_юл(String Mäten) { System.out.println(Mäten); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
