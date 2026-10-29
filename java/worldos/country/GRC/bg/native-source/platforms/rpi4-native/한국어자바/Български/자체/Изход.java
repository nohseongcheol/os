// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
/** 자체 커널의 표준 Изход. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class Изход {
    private Изход() {}
    public static void Писане(String Текст) { System.out.print(Текст); }
    public static void записване_ред(String Текст) { System.out.println(Текст); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
