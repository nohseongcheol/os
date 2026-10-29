// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.記憶領域;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 物理記憶域の整列確保、解放、空き領域の併合を担う。 */
public final class 記憶管理器 {
    private final byte[] 記憶領域;
    private final TreeMap<Integer, Integer> 空領域 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 使用済み領域 = new TreeMap<Integer, Integer>();

    public 記憶管理器(int 合計容量) {
        if (合計容量 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        記憶領域 = new byte[合計容量];
        空領域.put(Integer.valueOf(4096), Integer.valueOf(合計容量 - 4096));
    }

    public synchronized int 記憶装置確保(int 容量) {
        return 整列済み確保(容量, 1);
    }

    public synchronized int 整列済み確保(int 容量, int 整列値) {
        if (容量 <= 0 || 整列値 <= 0 || (整列値 & (整列値 - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> 入口値 : 空領域.entrySet()) {
            int 起動処理 = 入口値.getKey().intValue();
            int 領域容量 = 入口値.getValue().intValue();
            int 整列済み開始処理 = (起動処理 + 整列値 - 1) & -整列値;
            int 前面値容量 = 整列済み開始処理 - 起動処理;
            int 最終容量 = 領域容量 - 前面値容量 - 容量;
            if (最終容量 < 0) {
                continue;
            }
            空領域.remove(Integer.valueOf(起動処理));
            if (前面値容量 > 0) {
                空領域.put(Integer.valueOf(起動処理), Integer.valueOf(前面値容量));
            }
            if (最終容量 > 0) {
                空領域.put(Integer.valueOf(整列済み開始処理 + 容量), Integer.valueOf(最終容量));
            }
            使用済み領域.put(Integer.valueOf(整列済み開始処理), Integer.valueOf(容量));
            Arrays.fill(記憶領域, 整列済み開始処理, 整列済み開始処理 + 容量, (byte) 0);
            return 整列済み開始処理;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 記憶装置解放(int 番地) {
        Integer 容量オブジェクト = 使用済み領域.remove(Integer.valueOf(番地));
        if (容量オブジェクト == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int 起動処理 = 番地;
        int 容量 = 容量オブジェクト.intValue();
        Map.Entry<Integer, Integer> 前面値 = 空領域.lowerEntry(Integer.valueOf(起動処理));
        if (前面値 != null && 前面値.getKey().intValue() + 前面値.getValue().intValue() == 起動処理) {
            起動処理 = 前面値.getKey().intValue();
            容量 += 前面値.getValue().intValue();
            空領域.remove(前面値.getKey());
        }
        Map.Entry<Integer, Integer> 後端値 = 空領域.ceilingEntry(Integer.valueOf(起動処理));
        if (後端値 != null && 起動処理 + 容量 == 後端値.getKey().intValue()) {
            容量 += 後端値.getValue().intValue();
            空領域.remove(後端値.getKey());
        }
        空領域.put(Integer.valueOf(起動処理), Integer.valueOf(容量));
    }

    public synchronized byte バイト値読取(int 番地) {
        範囲検査(番地, 1);
        return 記憶領域[番地];
    }

    public synchronized void バイト値書込(int 番地, byte 値) {
        範囲検査(番地, 1);
        記憶領域[番地] = 値;
    }

    public synchronized int 合計容量() {
        return 記憶領域.length;
    }

    public synchronized int 使用済み容量() {
        int 合計値 = 0;
        for (Integer 容量 : 使用済み領域.values()) {
            合計値 += 容量.intValue();
        }
        return 合計値;
    }

    private void 範囲検査(int 番地, int 容量) {
        if (番地 < 0 || 容量 < 0 || 番地 > 記憶領域.length - 容量) {
            throw new IndexOutOfBoundsException("記憶領域 범위를 벗어났습니다.");
        }
    }
}

