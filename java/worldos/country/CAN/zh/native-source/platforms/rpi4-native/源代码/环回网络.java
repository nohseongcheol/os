// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 初始网络层：单个内核中的 IPv4/UDP 回环传输。外部 IP 返回 ENETUNREACH，不代替 Ethernet/IP 数据包驱动。8 个端点，每个端点容纳 4 个报文，每个报文 512 字节。所有调用均为非阻塞调用。 */
public final class 环回网络 {
    static int[] 使用值 = new int[8];
    static int[] 端口值 = new int[8];
    static int[] 地址 = new int[8];
    static int[] 前端值 = new int[8];
    static int[] 项目个数 = new int[8];
    static int[] 已接收端口 = new int[8];
    static int[] 长度 = new int[32];
    static int[] 已发送端口 = new int[32];
    static int[] 数据 = new int[32 * 512];
    static int[] 前向值 = new int[512];
    static int 下一端点 = 49152;
    static int 验证(int 编号) { return 编号 >= 32 && 编号 < 40 && 使用值[编号 - 32] != 0 ? 编号 - 32 : -1; }
    static boolean 重叠区列(int 编号) {
        for (int 槽条目 = 0; 槽条目 < 8; 槽条目++) if (使用值[槽条目] != 0 && 端口值[槽条目] == 编号) return true;
        return false;
    }
    static int 临时端口() {
        for (int 尝试值 = 0; 尝试值 < 16; 尝试值++) {
            int 候选 = 下一端点++;
            if (下一端点 > 65535) 下一端点 = 49152;
            if (!重叠区列(候选)) return 候选;
        }
        return -98;
    }
    public static int 创建条目(int 区域值, int 种类值, int 契约值) {
        if (区域值 != 2) return -97;
        if (种类值 != 2 || (契约值 != 0 && 契约值 != 17)) return -93;
        for (int 槽条目 = 0; 槽条目 < 8; 槽条目++) if (使用值[槽条目] == 0) {
            使用值[槽条目] = 1; 端口值[槽条目] = 0; 地址[槽条目] = 0; 前端值[槽条目] = 0; 项目个数[槽条目] = 0; 已接收端口[槽条目] = 0;
            return 槽条目 + 32;
        }
        return -24;
    }
    public static int 可执行束打包(int 编号, int 网络地址, int 端点端口编号) {
        int 槽条目 = 验证(编号);
        if (槽条目 < 0) return -9;
        if (网络地址 != 0 && 网络地址 != 0x7f000001) return -99;
        if (端口值[槽条目] != 0 || 端点端口编号 < 0 || 端点端口编号 > 65535) return -22;
        if (端点端口编号 == 0) 端点端口编号 = 临时端口();
        if (端点端口编号 < 0) return 端点端口编号;
        if (重叠区列(端点端口编号)) return -98;
        端口值[槽条目] = 端点端口编号; 地址[槽条目] = 网络地址; return 0;
    }
    public static int 放入数据(int 编号, int 值) {
        if (编号 < 0 || 编号 >= 512) return -22;
        前向值[编号] = 值 & 255; return 0;
    }
    public static int 读取数据(int 编号) { return 编号 >= 0 && 编号 < 512 ? 前向值[编号] : -22; }
    public static int 发送(int 编号, int 网络地址, int 端点端口编号, int 大小) {
        int 槽条目 = 验证(编号);
        if (槽条目 < 0) return -9;
        if (网络地址 != 0x7f000001) return -101;
        if (端点端口编号 < 1 || 端点端口编号 > 65535) return -22;
        if (大小 < 0 || 大小 > 512) return -90;
        if (端口值[槽条目] == 0) {
            int 结果 = 可执行束打包(编号, 0x7f000001, 0);
            if (结果 < 0) return 结果;
        }
        int 目的地址值 = -1;
        for (int 候选 = 0; 候选 < 8; 候选++) if (使用值[候选] != 0 && 端口值[候选] == 端点端口编号) 目的地址值 = 候选;
        if (目的地址值 < 0) return -111;
        if (项目个数[目的地址值] == 4) return -11;
        int 位置索引 = 目的地址值 * 4 + (前端值[目的地址值] + 项目个数[目的地址值]) % 4;
        for (int 字节值 = 0; 字节值 < 大小; 字节值++) 数据[位置索引 * 512 + 字节值] = 前向值[字节值];
        长度[位置索引] = 大小; 已发送端口[位置索引] = 端口值[槽条目]; 项目个数[目的地址值]++;
        return 大小;
    }
    public static int 接收(int 编号, int 容量值) {
        int 槽条目 = 验证(编号);
        if (槽条目 < 0) return -9;
        if (容量值 < 0 || 容量值 > 512) return -22;
        if (项目个数[槽条目] == 0) return -11;
        int 位置索引 = 槽条目 * 4 + 前端值[槽条目];
        int 大小 = 长度[位置索引] < 容量值 ? 长度[位置索引] : 容量值;
        for (int 字节值 = 0; 字节值 < 大小; 字节值++) 前向值[字节值] = 数据[位置索引 * 512 + 字节值];
        已接收端口[槽条目] = 已发送端口[位置索引]; 前端值[槽条目] = (前端值[槽条目] + 1) % 4; 项目个数[槽条目]--;
        return 大小;
    }
    public static int 读取端点端口(int 编号) { int 槽条目 = 验证(编号); return 槽条目 < 0 ? -9 : 端口值[槽条目]; }
    public static int 读取地址(int 编号) { int 槽条目 = 验证(编号); return 槽条目 < 0 ? -9 : 地址[槽条目]; }
    public static int 发送方端点(int 编号) { int 槽条目 = 验证(编号); return 槽条目 < 0 ? -9 : 已接收端口[槽条目]; }
    public static int 关闭(int 编号) {
        int 槽条目 = 验证(编号); if (槽条目 < 0) return -9;
        使用值[槽条目] = 0; 项目个数[槽条目] = 0; 端口值[槽条目] = 0; return 0;
    }
}
