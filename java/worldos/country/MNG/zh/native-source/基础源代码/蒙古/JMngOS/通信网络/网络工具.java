// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蒙古.JMngOS.通信网络;

/** Ethernet/ARP/IPv4/ICMP/UDP 层共享的字节序和校验和工具。 */
public final class 网络工具 {
    private 网络工具() {
    }

    public static int 大字节序短整数(byte[] 数据, int 位置) {
        检查范围(数据, 位置, 2);
        return ((数据[位置] & 0xff) << 8) | (数据[位置 + 1] & 0xff);
    }

    public static long 大字节序整数(byte[] 数据, int 位置) {
        检查范围(数据, 位置, 4);
        return ((long) (数据[位置] & 0xff) << 24)
                | ((long) (数据[位置 + 1] & 0xff) << 16)
                | ((long) (数据[位置 + 2] & 0xff) << 8)
                | (数据[位置 + 3] & 0xffL);
    }

    public static int 互联网校验和(byte[] 数据, int 运行, int 长度) {
        检查范围(数据, 运行, 长度);
        long 总和值 = 0;
        int 结尾 = 运行 + 长度;
        int 位置 = 运行;
        while (位置 + 1 < 结尾) {
            总和值 += 大字节序短整数(数据, 位置);
            位置 += 2;
        }
        if (位置 < 结尾) {
            总和值 += (数据[位置] & 0xff) << 8;
        }
        while ((总和值 >>> 16) != 0) {
            总和值 = (总和值 & 0xffff) + (总和值 >>> 16);
        }
        return (int) (~总和值) & 0xffff;
    }

    public static boolean 是否以太网帧(byte[] 数据) {
        return 数据 != null && 数据.length >= 14;
    }

    public static int 以太网上位侧协议(byte[] 数据) {
        if (!是否以太网帧(数据)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 大字节序短整数(数据, 12);
    }

    public static boolean 是否IP版本4协议(byte[] 数据, int 位置) {
        if (数据 == null || 位置 < 0 || 数据.length - 位置 < 20) {
            return false;
        }
        int 版本值 = (数据[位置] >>> 4) & 0xf;
        int 头部长度 = (数据[位置] & 0xf) * 4;
        return 版本值 == 4 && 头部长度 >= 20 && 数据.length - 位置 >= 头部长度;
    }

    private static void 检查范围(byte[] 数据, int 运行, int 长度) {
        if (数据 == null || 运行 < 0 || 长度 < 0 || 运行 > 数据.length - 长度) {
            throw new IllegalArgumentException("通信网络 数据 범위를 벗어났습니다.");
        }
    }
}

