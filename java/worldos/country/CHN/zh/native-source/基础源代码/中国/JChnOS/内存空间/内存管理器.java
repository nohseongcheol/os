// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国.JChnOS.内存空间;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 负责物理内存的对齐分配、释放和合并。 */
public final class 内存管理器 {
    private final byte[] 内存空间;
    private final TreeMap<Integer, Integer> 空区域 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 已使用区域 = new TreeMap<Integer, Integer>();

    public 内存管理器(int 总计大小) {
        if (总计大小 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        内存空间 = new byte[总计大小];
        空区域.put(Integer.valueOf(4096), Integer.valueOf(总计大小 - 4096));
    }

    public synchronized int 分配存储装置(int 大小) {
        return 分配已对齐(大小, 1);
    }

    public synchronized int 分配已对齐(int 大小, int 对齐值) {
        if (大小 <= 0 || 对齐值 <= 0 || (对齐值 & (对齐值 - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> 条目值 : 空区域.entrySet()) {
            int 运行 = 条目值.getKey().intValue();
            int 区域大小 = 条目值.getValue().intValue();
            int 已对齐开始 = (运行 + 对齐值 - 1) & -对齐值;
            int 前端值大小 = 已对齐开始 - 运行;
            int 最终大小 = 区域大小 - 前端值大小 - 大小;
            if (最终大小 < 0) {
                continue;
            }
            空区域.remove(Integer.valueOf(运行));
            if (前端值大小 > 0) {
                空区域.put(Integer.valueOf(运行), Integer.valueOf(前端值大小));
            }
            if (最终大小 > 0) {
                空区域.put(Integer.valueOf(已对齐开始 + 大小), Integer.valueOf(最终大小));
            }
            已使用区域.put(Integer.valueOf(已对齐开始), Integer.valueOf(大小));
            Arrays.fill(内存空间, 已对齐开始, 已对齐开始 + 大小, (byte) 0);
            return 已对齐开始;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 释放存储装置(int 地址) {
        Integer 大小对象 = 已使用区域.remove(Integer.valueOf(地址));
        if (大小对象 == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int 运行 = 地址;
        int 大小 = 大小对象.intValue();
        Map.Entry<Integer, Integer> 前端值 = 空区域.lowerEntry(Integer.valueOf(运行));
        if (前端值 != null && 前端值.getKey().intValue() + 前端值.getValue().intValue() == 运行) {
            运行 = 前端值.getKey().intValue();
            大小 += 前端值.getValue().intValue();
            空区域.remove(前端值.getKey());
        }
        Map.Entry<Integer, Integer> 后端值 = 空区域.ceilingEntry(Integer.valueOf(运行));
        if (后端值 != null && 运行 + 大小 == 后端值.getKey().intValue()) {
            大小 += 后端值.getValue().intValue();
            空区域.remove(后端值.getKey());
        }
        空区域.put(Integer.valueOf(运行), Integer.valueOf(大小));
    }

    public synchronized byte 读取字节值(int 地址) {
        检查范围(地址, 1);
        return 内存空间[地址];
    }

    public synchronized void 写入字节值(int 地址, byte 值) {
        检查范围(地址, 1);
        内存空间[地址] = 值;
    }

    public synchronized int 总计大小() {
        return 内存空间.length;
    }

    public synchronized int 已使用大小() {
        int 总计值 = 0;
        for (Integer 大小 : 已使用区域.values()) {
            总计值 += 大小.intValue();
        }
        return 总计值;
    }

    private void 检查范围(int 地址, int 大小) {
        if (地址 < 0 || 大小 < 0 || 地址 > 内存空间.length - 大小) {
            throw new IndexOutOfBoundsException("内存空间 범위를 벗어났습니다.");
        }
    }
}

