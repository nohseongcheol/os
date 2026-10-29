// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 实际启动后调用的 Java 入口，不依赖 JVM 或宿主操作系统。 */
public final class 内核 {
    static int 总计值(int 结尾) {
        int 总和值 = 0;
        for (int 编号 = 1; 编号 <= 结尾; 编号++) 总和值 += 编号;
        return 总和值;
    }

    static boolean 测试() {
        int[] 值列 = new int[4];
        值列[2] = 总计值(10);
        int 负数值 = -7;
        int 最小值 = 0x80000000;
        int 除法结果 = -1;
        int 编号 = 内存空间.分配存储装置();
        boolean 通过值 = 值列[0] == 0 && 值列[2] == 55 && 值列.length == 4
            && 负数值 / 3 == -2 && 负数值 % 3 == -1 && 最小值 / 除法结果 == 最小值
            && 最小值 % 除法结果 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && 编号 >= 0 && 内存空间.发回结果(编号) && !内存空间.发回结果(编号);
        字符终端.写入(通过值 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 通过值;
    }

    public static void 运行() {
        字符终端.准备();
        字符终端.写入("JKOROS NATIVE JAVA\n");
        字符终端.写入("Java 기계어 内核值 运行\n");
        if (设备.启动标记() != 0x2badb002) {
            字符终端.写入("BAD MULTIBOOT MAGIC\n");
            设备.停机执行状态();
        }
        if (!测试()) 设备.停机执行状态();
        if (内存空间.上位侧内存大小() < 15360) {
            字符终端.写入("At least 16 MiB RAM required\n");
            设备.停机执行状态();
        }
        设备.准备用户程序();
        字符终端.写入("USER ELF: ring 3 / paging / int 0x80\n");
        网络设备驱动.准备();
        通信网络.清洁进程();
        主存文件系统.准备();
        文件持久化.准备();
        命令解释器.运行();
    }
}
