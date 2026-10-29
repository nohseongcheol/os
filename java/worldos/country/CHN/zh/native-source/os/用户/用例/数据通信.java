// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 数据通信 {
    static int 数字值(String 文本) {
        if (文本 == null || 文本.length() == 0) return -1;
        int 结果 = 0;
        for (int 编号 = 0; 编号 < 文本.length(); 编号++) {
            int 值 = 文本.charAt(编号) - '0';
            if (值 < 0 || 值 > 9 || 结果 > 6553) return -1;
            结果 = 结果 * 10 + 值;
            if (结果 > 65535) return -1;
        }
        return 结果;
    }
    static int 地址(String 文本) {
        if (文本 == null) return 0;
        int 值 = 0, 结果 = 0, 子部分值 = 0, 位数 = 0;
        for (int 编号 = 0; 编号 <= 文本.length(); 编号++) {
            int 字符 = 编号 == 文本.length() ? '.' : 文本.charAt(编号);
            if (字符 == '.') {
                if (位数 == 0 || 子部分值 == 4) return 0;
                结果 = (结果 << 8) | 值; 子部分值++; 值 = 0; 位数 = 0;
            } else {
                if (字符 < '0' || 字符 > '9') return 0;
                值 = 值 * 10 + 字符 - '0';
                if (++位数 > 3 || 值 > 255) return 0;
            }
        }
        return 子部分值 == 4 ? 结果 : 0;
    }
    public static int 运行() {
        if (用户.参数列个数() != 3) { 用户.写入("Usage: run udp IP PORT TEXT\n"); return 2; }
        int 地址 = 地址(用户.实参(0)), 端口值 = 数字值(用户.实参(1));
        String 内容值 = 用户.实参(2);
        if (地址 == 0 || 端口值 < 1 || 内容值.length() > 1024) { 用户.写入("Bad destination\n"); return 2; }
        int 句柄值 = 用户.打开网络(0);
        if (句柄值 < 0) { 用户.写入("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] 数据 = new int[1024];
        for (int 编号 = 0; 编号 < 内容值.length(); 编号++) 数据[编号] = 内容值.charAt(编号);
        if (用户.发送数据(句柄值, 地址, 端口值, 数据, 内容值.length()) < 0) {
            用户.写入("UDP SEND FAILED\n"); 用户.关闭网络(句柄值); return 4;
        }
        用户.写入("UDP SENT\n");
        int 已接收长度 = 用户.接收数据(句柄值, 数据, 1500);
        boolean 相等文本 = 已接收长度 == 内容值.length() && 用户.已发送地址(句柄值) == 地址 && 用户.已发送端口(句柄值) == 端口值;
        if (相等文本) for (int 编号 = 0; 编号 < 已接收长度; 编号++) if (数据[编号] != 内容值.charAt(编号)) 相等文本 = false;
        用户.关闭网络(句柄值);
        if (已接收长度 < 0) { 用户.写入("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        用户.写入(相等文本 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 相等文本 ? 0 : 6;
    }
}
