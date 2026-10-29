// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IRN.l_ps;
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
    public static RandomAccessFile پرانيستل(String يونلور, String اکر) throws IOException {
        return new RandomAccessFile(يونلور, اکر);
    }
    public static int لوستل(RandomAccessFile دوتنه, byte[] data) throws IOException {
        return دوتنه.read(data);
    }
    public static void لوستل_2(RandomAccessFile دوتنه, byte[] data) throws IOException {
        دوتنه.write(data);
    }
    public static void seek(RandomAccessFile دوتنه, long ځای) throws IOException {
        دوتنه.seek(ځای);
    }
    public static void sync(RandomAccessFile دوتنه) throws IOException {
        دوتنه.getFD().sync();
    }
    public static void بندول(RandomAccessFile دوتنه) throws IOException {
        دوتنه.close();
    }
    public static void ړنګول(String يونلور) throws IOException {
        Files.delete(Paths.get(يونلور));
    }
    public static long کچ(String يونلور) throws IOException {
        return Files.size(Paths.get(يونلور));
    }
    public static Socket نښلېدل(String address, int درشل) throws IOException {
        return new Socket(address, درشل);
    }
    public static DatagramSocket datagram(int درشل) throws SocketException {
        return new DatagramSocket(درشل);
    }
    public static Thread thread(Runnable چار) {
        Thread thread = new Thread(چار);
        thread.start();
        return thread;
    }
    public static Process چلول(List<String> بولۍ) throws IOException {
        return new ProcessBuilder(بولۍ).start();
    }
}
