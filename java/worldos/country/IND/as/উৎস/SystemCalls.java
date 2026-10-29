// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_as;
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
    public static RandomAccessFile খোলো(String পথ, String মোড) throws IOException {
        return new RandomAccessFile(পথ, মোড);
    }
    public static int পড়া(RandomAccessFile নথিপত্ৰ, byte[] data) throws IOException {
        return নথিপত্ৰ.read(data);
    }
    public static void লিখা(RandomAccessFile নথিপত্ৰ, byte[] data) throws IOException {
        নথিপত্ৰ.write(data);
    }
    public static void seek(RandomAccessFile নথিপত্ৰ, long অৱস্থান) throws IOException {
        নথিপত্ৰ.seek(অৱস্থান);
    }
    public static void sync(RandomAccessFile নথিপত্ৰ) throws IOException {
        নথিপত্ৰ.getFD().sync();
    }
    public static void বন্ধ_কৰক(RandomAccessFile নথিপত্ৰ) throws IOException {
        নথিপত্ৰ.close();
    }
    public static void আঁতৰাওঁক(String পথ) throws IOException {
        Files.delete(Paths.get(পথ));
    }
    public static long মাপ(String পথ) throws IOException {
        return Files.size(Paths.get(পথ));
    }
    public static Socket সংযোগ_স্থাপনা(String address, int পোৰ্ট) throws IOException {
        return new Socket(address, পোৰ্ট);
    }
    public static DatagramSocket datagram(int পোৰ্ট) throws SocketException {
        return new DatagramSocket(পোৰ্ট);
    }
    public static Thread thread(Runnable কাৰ্য্য) {
        Thread thread = new Thread(কাৰ্য্য);
        thread.start();
        return thread;
    }
    public static Process চলাওক(List<String> কমান্ড) throws IOException {
        return new ProcessBuilder(কমান্ড).start();
    }
}
