// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CAN.l_bn;
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
    public static RandomAccessFile খুলুন(String পথ_2, String মোড) throws IOException {
        return new RandomAccessFile(পথ_2, মোড);
    }
    public static int পড়া(RandomAccessFile নথির_নাম, byte[] data) throws IOException {
        return নথির_নাম.read(data);
    }
    public static void লেখা(RandomAccessFile নথির_নাম, byte[] data) throws IOException {
        নথির_নাম.write(data);
    }
    public static void seek(RandomAccessFile নথির_নাম, long অবস্থান) throws IOException {
        নথির_নাম.seek(অবস্থান);
    }
    public static void sync(RandomAccessFile নথির_নাম) throws IOException {
        নথির_নাম.getFD().sync();
    }
    public static void বন্ধ_করুন(RandomAccessFile নথির_নাম) throws IOException {
        নথির_নাম.close();
    }
    public static void মুছে_ফেলুন(String পথ_2) throws IOException {
        Files.delete(Paths.get(পথ_2));
    }
    public static long আকার(String পথ_2) throws IOException {
        return Files.size(Paths.get(পথ_2));
    }
    public static Socket সংযোগ_স্থাপনা(String address, int পোর্ট) throws IOException {
        return new Socket(address, পোর্ট);
    }
    public static DatagramSocket datagram(int পোর্ট) throws SocketException {
        return new DatagramSocket(পোর্ট);
    }
    public static Thread thread(Runnable কাজ) {
        Thread thread = new Thread(কাজ);
        thread.start();
        return thread;
    }
    public static Process চালানো(List<String> আদেশ) throws IOException {
        return new ProcessBuilder(আদেশ).start();
    }
}
