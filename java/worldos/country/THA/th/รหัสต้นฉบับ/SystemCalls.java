// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.THA.l_th;
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
    public static RandomAccessFile เปิด(String เส้นทาง, String โหมด) throws IOException {
        return new RandomAccessFile(เส้นทาง, โหมด);
    }
    public static int อ่าน(RandomAccessFile แฟ้ม, byte[] ข้อมูล) throws IOException {
        return แฟ้ม.read(ข้อมูล);
    }
    public static void เขียน(RandomAccessFile แฟ้ม, byte[] ข้อมูล) throws IOException {
        แฟ้ม.write(ข้อมูล);
    }
    public static void seek(RandomAccessFile แฟ้ม, long ตำแหน่ง) throws IOException {
        แฟ้ม.seek(ตำแหน่ง);
    }
    public static void sync(RandomAccessFile แฟ้ม) throws IOException {
        แฟ้ม.getFD().sync();
    }
    public static void ปิด(RandomAccessFile แฟ้ม) throws IOException {
        แฟ้ม.close();
    }
    public static void ลบ(String เส้นทาง) throws IOException {
        Files.delete(Paths.get(เส้นทาง));
    }
    public static long ขนาด(String เส้นทาง) throws IOException {
        return Files.size(Paths.get(เส้นทาง));
    }
    public static Socket เชื่อมต่อ(String address, int หมายเลขพอร์ต) throws IOException {
        return new Socket(address, หมายเลขพอร์ต);
    }
    public static DatagramSocket datagram(int หมายเลขพอร์ต) throws SocketException {
        return new DatagramSocket(หมายเลขพอร์ต);
    }
    public static Thread สายงาน(Runnable การกระทำ) {
        Thread สายงาน = new Thread(การกระทำ);
        สายงาน.start();
        return สายงาน;
    }
    public static Process เรียกทำงาน(List<String> คำสั่ง) throws IOException {
        return new ProcessBuilder(คำสั่ง).start();
    }
}
