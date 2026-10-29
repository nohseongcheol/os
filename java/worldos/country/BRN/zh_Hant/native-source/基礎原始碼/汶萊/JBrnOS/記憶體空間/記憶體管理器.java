// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 汶萊.JBrnOS.記憶體空間;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 負責實體記憶體的對齊配置、釋放與合併。 */
public final class 記憶體管理器 {
    private final byte[] 記憶體空間;
    private final TreeMap<Integer, Integer> 空區域 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 已使用區域 = new TreeMap<Integer, Integer>();

    public 記憶體管理器(int 總計大小) {
        if (總計大小 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        記憶體空間 = new byte[總計大小];
        空區域.put(Integer.valueOf(4096), Integer.valueOf(總計大小 - 4096));
    }

    public synchronized int 分配存儲裝置(int 大小) {
        return 分配已對齊(大小, 1);
    }

    public synchronized int 分配已對齊(int 大小, int 對齊值) {
        if (大小 <= 0 || 對齊值 <= 0 || (對齊值 & (對齊值 - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> 條目值 : 空區域.entrySet()) {
            int 運行 = 條目值.getKey().intValue();
            int 區域大小 = 條目值.getValue().intValue();
            int 已對齊開始 = (運行 + 對齊值 - 1) & -對齊值;
            int 前端值大小 = 已對齊開始 - 運行;
            int 最終大小 = 區域大小 - 前端值大小 - 大小;
            if (最終大小 < 0) {
                continue;
            }
            空區域.remove(Integer.valueOf(運行));
            if (前端值大小 > 0) {
                空區域.put(Integer.valueOf(運行), Integer.valueOf(前端值大小));
            }
            if (最終大小 > 0) {
                空區域.put(Integer.valueOf(已對齊開始 + 大小), Integer.valueOf(最終大小));
            }
            已使用區域.put(Integer.valueOf(已對齊開始), Integer.valueOf(大小));
            Arrays.fill(記憶體空間, 已對齊開始, 已對齊開始 + 大小, (byte) 0);
            return 已對齊開始;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 釋放存儲裝置(int 地址) {
        Integer 大小物件 = 已使用區域.remove(Integer.valueOf(地址));
        if (大小物件 == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int 運行 = 地址;
        int 大小 = 大小物件.intValue();
        Map.Entry<Integer, Integer> 前端值 = 空區域.lowerEntry(Integer.valueOf(運行));
        if (前端值 != null && 前端值.getKey().intValue() + 前端值.getValue().intValue() == 運行) {
            運行 = 前端值.getKey().intValue();
            大小 += 前端值.getValue().intValue();
            空區域.remove(前端值.getKey());
        }
        Map.Entry<Integer, Integer> 後端值 = 空區域.ceilingEntry(Integer.valueOf(運行));
        if (後端值 != null && 運行 + 大小 == 後端值.getKey().intValue()) {
            大小 += 後端值.getValue().intValue();
            空區域.remove(後端值.getKey());
        }
        空區域.put(Integer.valueOf(運行), Integer.valueOf(大小));
    }

    public synchronized byte 讀取位元組值(int 地址) {
        檢查範圍(地址, 1);
        return 記憶體空間[地址];
    }

    public synchronized void 寫入位元組值(int 地址, byte 值) {
        檢查範圍(地址, 1);
        記憶體空間[地址] = 值;
    }

    public synchronized int 總計大小() {
        return 記憶體空間.length;
    }

    public synchronized int 已使用大小() {
        int 總計值 = 0;
        for (Integer 大小 : 已使用區域.values()) {
            總計值 += 大小.intValue();
        }
        return 總計值;
    }

    private void 檢查範圍(int 地址, int 大小) {
        if (地址 < 0 || 大小 < 0 || 地址 > 記憶體空間.length - 大小) {
            throw new IndexOutOfBoundsException("記憶體空間 범위를 벗어났습니다.");
        }
    }
}

