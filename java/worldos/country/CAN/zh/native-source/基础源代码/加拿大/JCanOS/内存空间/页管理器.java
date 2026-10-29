// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 加拿大.JCanOS.内存空间;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 提供 4 KiB 页映射和写时复制。 */
public final class 页管理器 {
    public static final int 页大小 = 4096;

    private static final class 页值 {
        private byte[] 数据 = new byte[页大小];
        private int 引用个数 = 1;
        private boolean 能够写入 = true;
        private boolean 复制启用侧写入;
    }

    public static final class 地址空间 {
        private final Map<Integer, 页值> 页表 = new HashMap<Integer, 页值>();
    }

    public 地址空间 新建地址空间() {
        return new 地址空间();
    }

    public void 映射表页(地址空间 地址区域, int 虚拟地址, boolean 能够写入) {
        int 编号 = 页编号(虚拟地址);
        页值 新建页 = new 页值();
        新建页.能够写入 = 能够写入;
        地址区域.页表.put(Integer.valueOf(编号), 新建页);
    }

    public 地址空间 克隆复制启用侧写入(地址空间 原始) {
        地址空间 已克隆值 = new 地址空间();
        for (Map.Entry<Integer, 页值> 条目值 : 原始.页表.entrySet()) {
            页值 共享页 = 条目值.getValue();
            共享页.引用个数++;
            if (共享页.能够写入) {
                共享页.能够写入 = false;
                共享页.复制启用侧写入 = true;
            }
            已克隆值.页表.put(条目值.getKey(), 共享页);
        }
        return 已克隆值;
    }

    public byte 读取字节值(地址空间 地址区域, int 虚拟地址) {
        页值 目标值 = 查找页(地址区域, 虚拟地址);
        return 目标值.数据[Math.floorMod(虚拟地址, 页大小)];
    }

    public void 写入字节值(地址空间 地址区域, int 虚拟地址, byte 值) {
        int 编号 = 页编号(虚拟地址);
        页值 目标值 = 查找页(地址区域, 虚拟地址);
        if (!目标值.能够写入) {
            if (!目标值.复制启用侧写入) {
                throw new IllegalStateException("读取 전용 쪽입니다.");
            }
            目标值 = 创建私有页(地址区域, 编号, 目标值);
        }
        目标值.数据[Math.floorMod(虚拟地址, 页大小)] = 值;
    }

    public void 私有范围写入(地址空间 地址区域, int 开始地址, int 大小) {
        if (大小 < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int 结束地址 = Math.addExact(开始地址, 大小);
        for (int 地址 = 开始地址; 地址 < 结束地址; 地址 = (页编号(地址) + 1) * 页大小) {
            int 编号 = 页编号(地址);
            页值 目标值 = 查找页(地址区域, 地址);
            if (目标值.复制启用侧写入) {
                创建私有页(地址区域, 编号, 目标值);
            } else {
                目标值.能够写入 = true;
            }
        }
    }

    public void 范围写入(地址空间 地址区域, int 开始地址, byte[] 数据) {
        for (int 编号 = 0; 编号 < 数据.length; 编号++) {
            写入字节值(地址区域, 开始地址 + 编号, 数据[编号]);
        }
    }

    private 页值 创建私有页(地址空间 地址区域, int 编号, 页值 共享页) {
        页值 私有页 = new 页值();
        私有页.数据 = Arrays.copyOf(共享页.数据, 共享页.数据.length);
        私有页.能够写入 = true;
        私有页.复制启用侧写入 = false;
        共享页.引用个数--;
        地址区域.页表.put(Integer.valueOf(编号), 私有页);
        return 私有页;
    }

    private 页值 查找页(地址空间 地址区域, int 地址) {
        页值 目标值 = 地址区域.页表.get(Integer.valueOf(页编号(地址)));
        if (目标值 == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return 目标值;
    }

    private int 页编号(int 地址) {
        if (地址 < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return 地址 / 页大小;
    }
}

