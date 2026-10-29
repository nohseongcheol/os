// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 新加坡.JSgpOS.通信网络;

import java.util.HashMap;
import java.util.Map;

/** 集中管理 Ethernet、ARP、IPv4、ICMP、UDP 和 TCP 接收分派。 */
public final class 网络层 {
    @FunctionalInterface
    public interface 数据处理程序 {
        void 进程值条目(byte[] 数据, int 运行, int 长度);
    }

    private final Map<Integer, 数据处理程序> 以太网处理程序 = new HashMap<Integer, 数据处理程序>();
    private final Map<Integer, 数据处理程序> 互联网协议处理程序 = new HashMap<Integer, 数据处理程序>();
    private final Map<Integer, 数据处理程序> 用户数据单位处理程序 = new HashMap<Integer, 数据处理程序>();
    private final Map<Integer, 数据处理程序> 传输状态控制处理程序 = new HashMap<Integer, 数据处理程序>();

    public void 寄存器以太网(int 种类值, 数据处理程序 处理程序) {
        以太网处理程序.put(Integer.valueOf(种类值 & 0xffff), 处理程序);
    }

    public void 寄存器互联网协议(int 契约值, 数据处理程序 处理程序) {
        互联网协议处理程序.put(Integer.valueOf(契约值 & 0xff), 处理程序);
    }

    public void 寄存器用户数据单位(int 硬件端口, 数据处理程序 处理程序) {
        用户数据单位处理程序.put(Integer.valueOf(硬件端口 & 0xffff), 处理程序);
    }

    public void 寄存器传输状态控制(int 硬件端口, 数据处理程序 处理程序) {
        传输状态控制处理程序.put(Integer.valueOf(硬件端口 & 0xffff), 处理程序);
    }

    public boolean 接收以太网(byte[] 帧索引) {
        if (!网络工具.是否以太网帧(帧索引)) {
            return false;
        }
        int 种类值 = 网络工具.以太网上位侧协议(帧索引);
        数据处理程序 直接处理程序 = 以太网处理程序.get(Integer.valueOf(种类值));
        if (直接处理程序 != null) {
            直接处理程序.进程值条目(帧索引, 14, 帧索引.length - 14);
            return true;
        }
        return 种类值 == 0x0800 && 接收互联网数据包(帧索引, 14);
    }

    private boolean 接收互联网数据包(byte[] 数据, int 运行) {
        if (!网络工具.是否IP版本4协议(数据, 运行)) {
            return false;
        }
        int 头部长度 = (数据[运行] & 0x0f) * 4;
        int 总计长度 = 网络工具.大字节序短整数(数据, 运行 + 2);
        if (总计长度 < 头部长度 || 运行 + 总计长度 > 数据.length) {
            return false;
        }
        int 契约值 = 数据[运行 + 9] & 0xff;
        int 内容开始 = 运行 + 头部长度;
        int 内容长度 = 总计长度 - 头部长度;
        数据处理程序 直接处理程序 = 互联网协议处理程序.get(Integer.valueOf(契约值));
        if (直接处理程序 != null) {
            直接处理程序.进程值条目(数据, 内容开始, 内容长度);
            return true;
        }
        if (内容长度 < 4) {
            return false;
        }
        int 目的地址端口编号 = 网络工具.大字节序短整数(数据, 内容开始 + 2);
        Map<Integer, 数据处理程序> 端口表 = 契约值 == 17 ? 用户数据单位处理程序 : 契约值 == 6 ? 传输状态控制处理程序 : null;
        if (端口表 == null) {
            return false;
        }
        数据处理程序 端口处理程序 = 端口表.get(Integer.valueOf(目的地址端口编号));
        if (端口处理程序 == null) {
            return false;
        }
        端口处理程序.进程值条目(数据, 内容开始, 内容长度);
        return true;
    }
}

