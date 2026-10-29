// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 泰國.JThaOS.記憶體空間;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 提供 4 KiB 頁對應與寫入時複製。 */
public final class 頁管理器 {
    public static final int 頁大小 = 4096;

    private static final class 頁值 {
        private byte[] 資料 = new byte[頁大小];
        private int 引用個數 = 1;
        private boolean 能夠寫入 = true;
        private boolean 複製啓用側寫入;
    }

    public static final class 地址空間 {
        private final Map<Integer, 頁值> 頁表 = new HashMap<Integer, 頁值>();
    }

    public 地址空間 新建地址空間() {
        return new 地址空間();
    }

    public void 映射表頁(地址空間 地址區域, int 虛擬地址, boolean 能夠寫入) {
        int 編號 = 頁編號(虛擬地址);
        頁值 新建頁 = new 頁值();
        新建頁.能夠寫入 = 能夠寫入;
        地址區域.頁表.put(Integer.valueOf(編號), 新建頁);
    }

    public 地址空間 克隆複製啓用側寫入(地址空間 原始) {
        地址空間 已克隆值 = new 地址空間();
        for (Map.Entry<Integer, 頁值> 條目值 : 原始.頁表.entrySet()) {
            頁值 共享頁 = 條目值.getValue();
            共享頁.引用個數++;
            if (共享頁.能夠寫入) {
                共享頁.能夠寫入 = false;
                共享頁.複製啓用側寫入 = true;
            }
            已克隆值.頁表.put(條目值.getKey(), 共享頁);
        }
        return 已克隆值;
    }

    public byte 讀取位元組值(地址空間 地址區域, int 虛擬地址) {
        頁值 目標值 = 查找頁(地址區域, 虛擬地址);
        return 目標值.資料[Math.floorMod(虛擬地址, 頁大小)];
    }

    public void 寫入位元組值(地址空間 地址區域, int 虛擬地址, byte 值) {
        int 編號 = 頁編號(虛擬地址);
        頁值 目標值 = 查找頁(地址區域, 虛擬地址);
        if (!目標值.能夠寫入) {
            if (!目標值.複製啓用側寫入) {
                throw new IllegalStateException("讀取 전용 쪽입니다.");
            }
            目標值 = 創建私有頁(地址區域, 編號, 目標值);
        }
        目標值.資料[Math.floorMod(虛擬地址, 頁大小)] = 值;
    }

    public void 私有範圍寫入(地址空間 地址區域, int 開始地址, int 大小) {
        if (大小 < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int 結束地址 = Math.addExact(開始地址, 大小);
        for (int 地址 = 開始地址; 地址 < 結束地址; 地址 = (頁編號(地址) + 1) * 頁大小) {
            int 編號 = 頁編號(地址);
            頁值 目標值 = 查找頁(地址區域, 地址);
            if (目標值.複製啓用側寫入) {
                創建私有頁(地址區域, 編號, 目標值);
            } else {
                目標值.能夠寫入 = true;
            }
        }
    }

    public void 範圍寫入(地址空間 地址區域, int 開始地址, byte[] 資料) {
        for (int 編號 = 0; 編號 < 資料.length; 編號++) {
            寫入位元組值(地址區域, 開始地址 + 編號, 資料[編號]);
        }
    }

    private 頁值 創建私有頁(地址空間 地址區域, int 編號, 頁值 共享頁) {
        頁值 私有頁 = new 頁值();
        私有頁.資料 = Arrays.copyOf(共享頁.資料, 共享頁.資料.length);
        私有頁.能夠寫入 = true;
        私有頁.複製啓用側寫入 = false;
        共享頁.引用個數--;
        地址區域.頁表.put(Integer.valueOf(編號), 私有頁);
        return 私有頁;
    }

    private 頁值 查找頁(地址空間 地址區域, int 地址) {
        頁值 目標值 = 地址區域.頁表.get(Integer.valueOf(頁編號(地址)));
        if (目標值 == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return 目標值;
    }

    private int 頁編號(int 地址) {
        if (地址 < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return 地址 / 頁大小;
    }
}

