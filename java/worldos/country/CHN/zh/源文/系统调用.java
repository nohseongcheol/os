// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CHN.l_zh;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class 系统调用 {
    private 系统调用() { }
    public static RandomAccessFile 打开(String 路径, String 方式) throws IOException {
        return new RandomAccessFile(路径, 方式);
    }
    public static int 读取(RandomAccessFile 文件, byte[] 数据) throws IOException {
        return 文件.read(数据);
    }
    public static void 写入(RandomAccessFile 文件, byte[] 数据) throws IOException {
        文件.write(数据);
    }
    public static void 定位(RandomAccessFile 文件, long 位置) throws IOException {
        文件.seek(位置);
    }
    public static void 同步(RandomAccessFile 文件) throws IOException {
        文件.getFD().sync();
    }
    public static void 关闭(RandomAccessFile 文件) throws IOException {
        文件.close();
    }
    public static void 删除(String 路径) throws IOException {
        Files.delete(Paths.get(路径));
    }
    public static long 大小(String 路径) throws IOException {
        return Files.size(Paths.get(路径));
    }
    public static Socket 连接(String 地址, int 端口号) throws IOException {
        return new Socket(地址, 端口号);
    }
    public static DatagramSocket 独立报文(int 端口号) throws SocketException {
        return new DatagramSocket(端口号);
    }
    public static Thread 线程(Runnable 动作) {
        Thread 线程 = new Thread(动作);
        线程.start();
        return 线程;
    }
    public static Process 执行(List<String> 命令) throws IOException {
        return new ProcessBuilder(命令).start();
    }
}
