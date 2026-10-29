// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** بومی 커널의 표준 خروجی. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class خروجی {
    private خروجی() {}
    public static void نوشتن(String متن) { System.out.print(متن); }
    public static void نوشتن_خط(String متن) { System.out.println(متن); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
