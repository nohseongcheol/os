// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 印尼.JIdnOS.描述符條目;

/** TSS 的受管理表示，在 x86 工作切換時提供特權堆疊。 */
public final class 任務狀態段 {
    private int 棧零塊;
    private int 棧零地址;
    private int 輸入輸出權限表位置 = 104;

    public void 設定特權用棧(int 片段值, int 地址) {
        棧零塊 = 片段值;
        棧零地址 = 地址;
    }

    public int 棧零塊() { return 棧零塊; }
    public int 棧零地址() { return 棧零地址; }
    public int 輸入輸出權限表位置() { return 輸入輸出權限表位置; }
}

