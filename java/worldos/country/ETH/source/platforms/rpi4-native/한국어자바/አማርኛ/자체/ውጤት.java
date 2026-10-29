// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** 자체 커널의 표준 ውጤት. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class ውጤት {
    private ውጤት() {}
    public static void መጻፊያ(String ጽሁፍ) { System.out.print(ጽሁፍ); }
    public static void ጻፍ_መስመር(String ጽሁፍ) { System.out.println(ጽሁፍ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
