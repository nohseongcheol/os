// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 法屬圭亞那.JGufOS.通信網絡;

import java.util.HashMap;
import java.util.Map;

/** 集中管理 Ethernet、ARP、IPv4、ICMP、UDP 與 TCP 接收分派。 */
public final class 網路層 {
    @FunctionalInterface
    public interface 資料處理程序 {
        void 程序值條目(byte[] 資料, int 運行, int 長度);
    }

    private final Map<Integer, 資料處理程序> 以太網處理程序 = new HashMap<Integer, 資料處理程序>();
    private final Map<Integer, 資料處理程序> 互聯網通訊協定處理程序 = new HashMap<Integer, 資料處理程序>();
    private final Map<Integer, 資料處理程序> 用戶資料單位處理程序 = new HashMap<Integer, 資料處理程序>();
    private final Map<Integer, 資料處理程序> 傳輸狀態控制處理程序 = new HashMap<Integer, 資料處理程序>();

    public void 寄存器以太網(int 種類值, 資料處理程序 處理程序) {
        以太網處理程序.put(Integer.valueOf(種類值 & 0xffff), 處理程序);
    }

    public void 寄存器互聯網通訊協定(int 契約值, 資料處理程序 處理程序) {
        互聯網通訊協定處理程序.put(Integer.valueOf(契約值 & 0xff), 處理程序);
    }

    public void 寄存器用戶資料單位(int 硬件埠, 資料處理程序 處理程序) {
        用戶資料單位處理程序.put(Integer.valueOf(硬件埠 & 0xffff), 處理程序);
    }

    public void 寄存器傳輸狀態控制(int 硬件埠, 資料處理程序 處理程序) {
        傳輸狀態控制處理程序.put(Integer.valueOf(硬件埠 & 0xffff), 處理程序);
    }

    public boolean 接收以太網(byte[] 幀索引) {
        if (!網路工具.是否以太網幀(幀索引)) {
            return false;
        }
        int 種類值 = 網路工具.以太網上位側通訊協定(幀索引);
        資料處理程序 直接處理程序 = 以太網處理程序.get(Integer.valueOf(種類值));
        if (直接處理程序 != null) {
            直接處理程序.程序值條目(幀索引, 14, 幀索引.length - 14);
            return true;
        }
        return 種類值 == 0x0800 && 接收互聯網數據包(幀索引, 14);
    }

    private boolean 接收互聯網數據包(byte[] 資料, int 運行) {
        if (!網路工具.是否IP版本4通訊協定(資料, 運行)) {
            return false;
        }
        int 標頭長度 = (資料[運行] & 0x0f) * 4;
        int 總計長度 = 網路工具.大字節序短整數(資料, 運行 + 2);
        if (總計長度 < 標頭長度 || 運行 + 總計長度 > 資料.length) {
            return false;
        }
        int 契約值 = 資料[運行 + 9] & 0xff;
        int 內容開始 = 運行 + 標頭長度;
        int 內容長度 = 總計長度 - 標頭長度;
        資料處理程序 直接處理程序 = 互聯網通訊協定處理程序.get(Integer.valueOf(契約值));
        if (直接處理程序 != null) {
            直接處理程序.程序值條目(資料, 內容開始, 內容長度);
            return true;
        }
        if (內容長度 < 4) {
            return false;
        }
        int 目的地址埠編號 = 網路工具.大字節序短整數(資料, 內容開始 + 2);
        Map<Integer, 資料處理程序> 埠表 = 契約值 == 17 ? 用戶資料單位處理程序 : 契約值 == 6 ? 傳輸狀態控制處理程序 : null;
        if (埠表 == null) {
            return false;
        }
        資料處理程序 埠處理程序 = 埠表.get(Integer.valueOf(目的地址埠編號));
        if (埠處理程序 == null) {
            return false;
        }
        埠處理程序.程序值條目(資料, 內容開始, 內容長度);
        return true;
    }
}

