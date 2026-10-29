// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 独立 Java 内核的 Pi4 初始移植版，不运行在 Linux 或宿主 JVM 之上。 */
public final class 内核 {
    static int[] 任务迭代次数 = new int[3];
    static int[] 任务总和 = new int[3];
    static int 任务排序;
    static int 任务错误;
    static int 随机种子 = 17;

    static void 验证(boolean 条件, int 编号) {
        if (!条件) { 终端输入输出.写入("FAIL "); 终端输入输出.数(编号); 板.停止(编号); }
    }
    static int 分支(int 值) {
        switch (值) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 稠密切换(int 值) {
        switch (值) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 发回数组(int[] 数组值) { return 数组值; }
    static void 测试算术() {
        int 值 = 随机种子;
        验证(值 * 7 - 值 == 102 && 值 / 3 == 5 && 值 % 3 == 2, 1);
        int 最小整数 = 0x80000000, 负数一 = -1;
        验证(最小整数 / 负数一 == 最小整数 && 最小整数 % 负数一 == 0, 2);
        验证(最小整数 + 最小整数 == 0 && -最小整数 == 最小整数, 3);
        验证((-值 >> 2) == -5 && (-值 >>> 2) == 1073741819 && (值 << 33) == 34, 4);
        验证((byte)(值 * 16) == 16 && (short)65535 == -1 && (char)负数一 == 65535, 5);
        int[] 数组值 = new int[5];
        for (int 循环索引 = 0; 循环索引 < 数组值.length; 循环索引++) 数组值[循环索引] = 循环索引 * 值;
        数组值[2]++;
        验证(发回数组(数组值) == 数组值 && 数组值[2] == 35 && 数组值[4] == 68, 6);
        验证(分支(值 - 117) == 7 && 分支(值 - 15) == 9 && 分支(值) == 3 && 稠密切换(值 - 15) == 17, 7);
        String 文本 = "한글 😀";
        验证(文本.length() == 5 && 文本.charAt(0) == '한' && 文本.charAt(3) == 0xd83d, 8);
        验证(板.CPU特权级别() == 1, 9);
        终端输入输出.写入("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 任务(int 编号) {
        // 检查让出执行权前后局部变量是否保持不变；每个任务使用独立的机器栈。
        int 局部值 = 编号 * 100;
        for (int 循环索引 = 0; 循环索引 < 10; 循环索引++) {
            if (任务排序 % 2 + 1 != 编号) 任务错误++;
            任务排序++;
            局部值 += 循环索引 + 编号;
            任务总和[编号] = 局部值;
            任务迭代次数[编号]++;
            板.挂起处理器();
            if (局部值 != 任务总和[编号]) 任务错误++;
        }
    }
    static void 测试任务列() {
        任务排序 = 0; 任务错误 = 0;
        任务迭代次数[1] = 0; 任务迭代次数[2] = 0;
        验证(板.创建任务(1) == 0 && 板.创建任务(2) == 0, 20);
        int 旋转个数 = 0;
        while (板.任务状态(1) != 0 || 板.任务状态(2) != 0) {
            板.挂起处理器();
            验证(++旋转个数 < 100, 21);
        }
        验证(任务迭代次数[1] == 10 && 任务迭代次数[2] == 10 && 任务排序 == 20 && 任务错误 == 0, 22);
        验证(任务总和[1] == 155 && 任务总和[2] == 265, 23);
        终端输入输出.写入("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 矩形(int 水平位置, int 垂直位置, int 宽度值, int 高度值, int 颜色值) {
        for (int Y_按钮坐标 = 垂直位置; Y_按钮坐标 < 垂直位置 + 高度值; Y_按钮坐标++)
            for (int 横坐标坐标 = 水平位置; 横坐标坐标 < 水平位置 + 宽度值; 横坐标坐标++) 板.放入屏幕像素(横坐标坐标, Y_按钮坐标, 颜色值);
    }
    static void 屏幕() {
        if (板.准备屏幕() == 0) { 终端输入输出.写入("FRAMEBUFFER unavailable\n"); return; }
        矩形(0, 0, 板.屏幕宽度(), 板.屏幕高度(), 0x302018);
        矩形(40, 40, 560, 400, 0xefe8e2);
        矩形(40, 40, 560, 40, 0x905020);
        矩形(60, 110, 240, 140, 0x90b050);
        矩形(320, 110, 260, 140, 0xd0a040);
        矩形(60, 290, 520, 120, 0xd8d0c8);
        终端输入输出.写入("FRAMEBUFFER PASS "); 终端输入输出.数(板.屏幕宽度()); 终端输入输出.字符('x');
        终端输入输出.数(板.屏幕高度()); 终端输入输出.写入(" RGB32 (drawing only)\n");
    }
    static void 测试C() {
        int 结果 = 板.测试Cpp();
        验证(结果 == 0, 100 + 结果);
        终端输入输出.写入("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 测试用户程序列() {
        验证(板.检查用户程序() == 0, 200);
        终端输入输出.写入("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 初始结果 = 板.运行用户程序(0);
        if (初始结果 != 0) { 终端输入输出.写入("USER DEMO RESULT "); 终端输入输出.数(初始结果); 终端输入输出.字符(10); }
        验证(初始结果 == 0, 201);
        终端输入输出.写入("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 预期值列 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int 编号 = 0; 编号 < 预期值列.length; 编号++) {
            终端输入输出.写入("USER CHECK "); 终端输入输出.数(编号); 终端输入输出.字符(10);
            int 结果 = 板.运行用户程序(编号 + 1);
            if (结果 != 预期值列[编号]) { 终端输入输出.写入("USER RESULT "); 终端输入输出.数(结果); 终端输入输出.字符(10); }
            验证(结果 == 预期值列[编号], 210 + 编号);
        }
        验证(板.运行用户程序(0) == 0, 220);
        终端输入输出.写入("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 测试联网() {
        int 结果 = 板.运行用户程序(9);
        if (结果 != 0) { 终端输入输出.写入("UDP RESULT "); 终端输入输出.数(结果); 终端输入输出.字符(10); }
        验证(结果 == 0, 230);
    }
    static void 系统信息() {
        终端输入输出.写入("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        终端输入输出.写入("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        终端输入输出.写入("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        终端输入输出.写入("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        终端输入输出.写入("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void 运行() {
        终端输入输出.写入("WorldOS zh · zh · 😀\n");
        测试算术();
        测试C();
        测试任务列();
        屏幕();
        测试用户程序列();
        测试联网();
        终端输入输出.写入("NATIVE READY\n");
        命令解释器.执行命令();
    }
}
