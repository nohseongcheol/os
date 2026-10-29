// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 加拿大.JCanOS.描述符条目;

/** TSS 的受管理表示，在 x86 任务切换时提供特权栈。 */
public final class 任务状态段 {
    private int 栈零块;
    private int 栈零地址;
    private int 输入输出权限表位置 = 104;

    public void 设定特权用栈(int 片段值, int 地址) {
        栈零块 = 片段值;
        栈零地址 = 地址;
    }

    public int 栈零块() { return 栈零块; }
    public int 栈零地址() { return 栈零地址; }
    public int 输入输出权限表位置() { return 输入输出权限表位置; }
}

