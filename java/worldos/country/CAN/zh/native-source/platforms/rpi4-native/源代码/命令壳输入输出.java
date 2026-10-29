// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 管道按 16 KiB 分块顺序执行，不模拟进程或并发管道。 */
public final class 命令壳输入输出 {
    static int[] 输入数据 = new int[16384], 输出数据 = new int[16384];
    static int 输入长度, 输入位置, 输出长度, 输入文件 = -1, 输出文件 = -1;
    static boolean 管道输入, 管道输出;
    static int 失败值;
    static boolean 允许交互式 = true;
    public static int 是否交互式() { return 允许交互式 && 输入文件 < 3 && 输出文件 < 3 && !管道输入 && !管道输出 ? 1 : 0; }
    public static int 输出(int 信道值, int 值) {
        if (信道值 != 1) return 0;
        if (输出文件 >= 3) { int 已处理值 = 内存文件集.写入(输出文件, 值); if (已处理值 < 0) 失败值 = 已处理值; return 1; }
        if (!管道输出) return 0;
        if (输出长度 == 输出数据.length) 失败值 = -28;
        else 输出数据[输出长度++] = 值;
        return 1;
    }
    public static int 输入值() {
        if (输入文件 >= 3) { int 已处理值 = 内存文件集.读取(输入文件); return 已处理值 == 256 ? -2 : 已处理值; }
        if (管道输入) return 输入位置 < 输入长度 ? 输入数据[输入位置++] : -2;
        return -3; // 转发至 UART。
    }
    static void 运行(boolean 前导管道, boolean 尾随管道) {
        管道输入 = 前导管道; 管道输出 = 尾随管道;
        输入位置 = 0; 输出长度 = 0; 输入文件 = -1; 输出文件 = -1; 失败值 = 0;
    }
    static void 结尾() {
        板.切换输入输出(0);
        if (输入文件 >= 3) 内存文件集.关闭(输入文件);
        if (输出文件 >= 3) 内存文件集.关闭(输出文件);
        if (管道输出) { 输入长度 = 输出长度; for (int 循环索引 = 0; 循环索引 < 输出长度; 循环索引++) 输入数据[循环索引] = 输出数据[循环索引]; }
        输入文件 = -1; 输出文件 = -1; 管道输入 = false; 管道输出 = false;
    }
}
