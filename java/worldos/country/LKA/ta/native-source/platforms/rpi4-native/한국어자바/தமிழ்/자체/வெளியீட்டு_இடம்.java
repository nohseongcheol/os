// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
/** 자체 커널의 표준 வெளியீட்டு_இடம். UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class வெளியீட்டு_இடம் {
    private வெளியீட்டு_இடம்() {}
    public static void எழுது(String உரை) { System.out.print(உரை); }
    public static void எழுது_வரி(String உரை) { System.out.println(உரை); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
