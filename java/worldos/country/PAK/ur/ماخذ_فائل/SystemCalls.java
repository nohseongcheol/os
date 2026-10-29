// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PAK.l_ur;
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
    public static RandomAccessFile کھولیں(String راستہ_2, String mode) throws IOException {
        return new RandomAccessFile(راستہ_2, mode);
    }
    public static int پڑھیں(RandomAccessFile فائل_کا_نام, byte[] data) throws IOException {
        return فائل_کا_نام.read(data);
    }
    public static void لکھیں(RandomAccessFile فائل_کا_نام, byte[] data) throws IOException {
        فائل_کا_نام.write(data);
    }
    public static void seek(RandomAccessFile فائل_کا_نام, long مقام) throws IOException {
        فائل_کا_نام.seek(مقام);
    }
    public static void sync(RandomAccessFile فائل_کا_نام) throws IOException {
        فائل_کا_نام.getFD().sync();
    }
    public static void بند_کریں(RandomAccessFile فائل_کا_نام) throws IOException {
        فائل_کا_نام.close();
    }
    public static void حذف_کریں(String راستہ_2) throws IOException {
        Files.delete(Paths.get(راستہ_2));
    }
    public static long حجم(String راستہ_2) throws IOException {
        return Files.size(Paths.get(راستہ_2));
    }
    public static Socket متصل_ہوں(String address, int پورٹ) throws IOException {
        return new Socket(address, پورٹ);
    }
    public static DatagramSocket datagram(int پورٹ) throws SocketException {
        return new DatagramSocket(پورٹ);
    }
    public static Thread thread(Runnable عمل) {
        Thread thread = new Thread(عمل);
        thread.start();
        return thread;
    }
    public static Process اطلاق(List<String> حکم) throws IOException {
        return new ProcessBuilder(حکم).start();
    }
}
