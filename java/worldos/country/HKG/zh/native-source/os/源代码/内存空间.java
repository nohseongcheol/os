// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 查询启动信息，分配和释放固定 4 KiB 任务区域；不是通用物理页管理器。 */
public final class 内存空间 {
    static int[] 区段值 = new int[8192];
    static int[] 使用值 = new int[8];

    static int 解析整数(int 地址) {
        return 设备.读取内存(地址) | (设备.读取内存(地址 + 1) << 8)
            | (设备.读取内存(地址 + 2) << 16) | (设备.读取内存(地址 + 3) << 24);
    }

    static int 上位侧内存大小() {
        int 系统信息 = 设备.启动信息();
        if (设备.启动标记() != 0x2badb002 || 系统信息 == 0 || (解析整数(系统信息) & 1) == 0) return -1;
        return 解析整数(系统信息 + 8);
    }

    static int 分配存储装置() {
        for (int 编号 = 0; 编号 < 使用值.length; 编号++) {
            if (使用值[编号] == 0) {
                使用值[编号] = 1;
                for (int 槽条目 = 0; 槽条目 < 1024; 槽条目++) 区段值[编号 * 1024 + 槽条目] = 0;
                return 编号;
            }
        }
        return -1;
    }

    static boolean 发回结果(int 编号) {
        if (编号 < 0 || 编号 >= 使用值.length || 使用值[编号] == 0) return false;
        使用值[编号] = 0;
        return true;
    }

    static int 已使用条目个数() {
        int 项目个数 = 0;
        for (int 编号 = 0; 编号 < 使用值.length; 编号++) 项目个数 += 使用值[编号];
        return 项目个数;
    }
}
