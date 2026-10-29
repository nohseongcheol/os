// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** 자체 커널의 표준 આઉટપુટ. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class આઉટપુટ {
    private આઉટપુટ() {}
    public static void લખો(String લખાણ) { System.out.print(લખાણ); }
    public static void લખો_લાઇન(String લખાણ) { System.out.println(લખાણ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
