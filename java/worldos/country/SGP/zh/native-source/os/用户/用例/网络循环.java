// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 使用最大长度和奇数长度的数据报测试真实 RTL8139 接收环的回绕。 */
public final class 网络循环 {
    public static int 运行() {
        if (用户.参数列个数() != 1) { 用户.写入("Usage: run stress PORT\n"); return 2; }
        String 文本 = 用户.实参(0);
        int 端口值 = 0;
        for (int 编号 = 0; 编号 < 文本.length(); 编号++) {
            if (文本.charAt(编号) < '0' || 文本.charAt(编号) > '9' || 端口值 > 6553) return 2;
            端口值 = 端口值 * 10 + 文本.charAt(编号) - '0';
        }
        if (端口值 < 1 || 端口值 > 65535) return 2;
        int 句柄值 = 用户.打开网络(0);
        if (句柄值 < 0) return 3;
        int[] 数据 = new int[1024];
        for (int 迭代序数 = 0; 迭代序数 < 24; 迭代序数++) {
            int 长度 = 1024 - (迭代序数 & 1);
            for (int 编号 = 0; 编号 < 长度; 编号++) 数据[编号] = (编号 + 迭代序数) & 255;
            if (用户.发送数据(句柄值, 0x0a000202, 端口值, 数据, 长度) != 长度) return 4;
            if (用户.接收数据(句柄值, 数据, 300) != 长度) return 5;
            for (int 编号 = 0; 编号 < 长度; 编号++) if (数据[编号] != ((编号 + 迭代序数) & 255)) return 6;
        }
        用户.关闭网络(句柄值);
        用户.写入("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
