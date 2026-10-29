// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 不写磁盘的小型串口/PS2 命令解释器。 */
public final class 命令解释器 {
    static int[] 输入值 = new int[128];
    static int 长度 = 0;
    static boolean 发回目标侧上一个行 = false;
    static boolean 行溢出 = false;

    static boolean 命令(String 名称) {
        if (长度 < 名称.length()) return false;
        for (int 编号 = 0; 编号 < 名称.length(); 编号++)
            if (输入值[编号] != 名称.charAt(编号)) return false;
        return 长度 == 名称.length() || 输入值[名称.length()] == ' ';
    }

    static void 显示帮助() {
        字符终端.写入("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        字符终端.写入("apps | run NAME [ARGS] | net\n");
        字符终端.写入("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        字符终端.写入("sync (연결된 JKSTORE1 存储值 장치에 文件 보존)\n");
    }

    static void 进程值条目() {
        if (长度 == 0) return;
        if (命令("help")) 显示帮助();
        else if (命令("sync")) {
            int 结果 = 文件持久化.同步化();
            字符终端.写入("Sync: "); 字符终端.写入编号(结果); 字符终端.字符(10);
        }
        else if (命令("ls")) 主存文件系统.条目列表();
        else if (命令("edit")) 主存文件系统.命令(输入值, 4, 长度, 0);
        else if (命令("cat")) 主存文件系统.命令(输入值, 3, 长度, 1);
        else if (命令("rm")) 主存文件系统.命令(输入值, 2, 长度, 2);
        else if (命令("java") || 命令("javac")) {
            int 结果 = 执行管理.执行命令(输入值, 0, 长度);
            字符终端.写入("Exit: "); 字符终端.写入编号(结果); 字符终端.字符(10);
        }
        else if (命令("apps")) 执行管理.条目列表();
        else if (命令("net")) 通信网络.状态值();
        else if (命令("run")) {
            int 结果 = 执行管理.执行命令(输入值, 3, 长度);
            字符终端.写入("Exit: "); 字符终端.写入编号(结果); 字符终端.写入("\n");
        } else if (命令("info")) {
            字符终端.写入("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (命令("mem")) {
            字符终端.写入("上位侧侧 内存 地址区域(KiB): "); 字符终端.写入编号(内存空间.上位侧内存大小());
            字符终端.写入("\n배열 동적 内存 地址区域(字节值): "); 字符终端.写入编号(设备.数组用量());
            字符终端.写入(" / 262144\n작업 地址区域 区段值: "); 字符终端.写入编号(内存空间.已使用条目个数());
            字符终端.写入(" / 8 (각 4096바이트)\n");
        } else if (命令("alloc")) {
            int 编号 = 内存空间.分配存储装置();
            字符终端.写入("区段值 编号: "); 字符终端.写入编号(编号); 字符终端.写入("\n");
        } else if (命令("free")) {
            if (长度 == 6 && 输入值[4] == ' ' && 输入值[5] >= '0' && 输入值[5] <= '7') {
                字符终端.写入(内存空间.发回结果(输入值[5] - '0') ? "반환됨\n" : "할당되지 않은 区段值\n");
            } else 字符终端.写入("사용법: free 0..7\n");
        } else if (命令("echo")) {
            for (int 编号 = 5; 编号 < 长度; 编号++) 字符终端.字符(输入值[编号]);
            字符终端.字符(10);
        } else if (命令("clear")) 字符终端.擦除条目();
        else if (命令("test")) 内核.测试();
        else if (命令("halt")) {
            字符终端.写入("HALTED\n");
            设备.停机执行状态();
        } else 字符终端.写入("알 数 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 接受与写入(int 值) {
        if (值 == 10 && 发回目标侧上一个行) { 发回目标侧上一个行 = false; return; }
        发回目标侧上一个行 = 值 == 13;
        if (值 == 10 || 值 == 13) {
            字符终端.字符(10);
            if (主存文件系统.是否编辑中) 主存文件系统.已编辑行(输入值, 长度, 行溢出);
            else 进程值条目();
            长度 = 0;
            行溢出 = false;
            字符终端.写入(主存文件系统.是否编辑中 ? "...> " : "jkoros> ");
        } else if (值 == 8 || 值 == 127) {
            if (长度 > 0) {
                长度--;
                字符终端.串行字节(8); 字符终端.串行字节(32); 字符终端.串行字节(8);
                字符终端.屏幕字符(8);
            }
        } else if (值 >= 32 && 值 < 127 && 长度 < 输入值.length) {
            输入值[长度++] = 值;
            字符终端.字符(值);
        } else if (值 >= 32 && 值 < 127) 行溢出 = true;
    }

    static void 运行() {
        显示帮助();
        字符终端.写入("READY\njkoros> ");
        while (true) {
            int 值 = 字符终端.读取串行();
            if (值 < 0) 值 = 键盘.读取();
            if (值 >= 0) 接受与写入(值);
            else { 通信网络.验证(); 设备.挂起短暂地(); }
        }
    }
}
