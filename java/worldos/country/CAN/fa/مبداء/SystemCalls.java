// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_fa;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class SystemCalls {
    private SystemCalls() { }
    public static RandomAccessFile باز_کردن(String مسیر, String حالت) throws IOException {
        return new RandomAccessFile(مسیر, حالت);
    }
    public static int خواندن(RandomAccessFile پرونده, byte[] data) throws IOException {
        return پرونده.read(data);
    }
    public static void نوشتن(RandomAccessFile پرونده, byte[] data) throws IOException {
        پرونده.write(data);
    }
    public static void seek(RandomAccessFile پرونده, long position) throws IOException {
        پرونده.seek(position);
    }
    public static void sync(RandomAccessFile پرونده) throws IOException {
        پرونده.getFD().sync();
    }
    public static void بستن(RandomAccessFile پرونده) throws IOException {
        پرونده.close();
    }
    public static void حذف(String مسیر) throws IOException {
        Files.delete(Paths.get(مسیر));
    }
    public static long اندازه(String مسیر) throws IOException {
        return Files.size(Paths.get(مسیر));
    }
    public static Socket اتصال(String address, int درگاه) throws IOException {
        return new Socket(address, درگاه);
    }
    public static DatagramSocket datagram(int درگاه) throws SocketException {
        return new DatagramSocket(درگاه);
    }
    public static Thread thread(Runnable کنش) {
        Thread thread = new Thread(کنش);
        thread.start();
        return thread;
    }
    public static Process اجرا(List<String> فرمان) throws IOException {
        return new ProcessBuilder(فرمان).start();
    }
}
