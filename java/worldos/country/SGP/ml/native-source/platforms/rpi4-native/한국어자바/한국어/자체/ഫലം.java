// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 커널의 표준 ഫലം. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class ഫലം {
    private ഫലം() {}
    public static void എഴുത്തു്(String പദാവലി) { System.out.print(പദാവലി); }
    public static void റൈറ്റ്_ചെയ്യുക_ലൈൻ(String പദാവലി) { System.out.println(പദാവലി); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
