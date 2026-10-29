// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.AFG.l_ug;
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
    public static RandomAccessFile ئاچ(String يول, String ھالىتى) throws IOException {
        return new RandomAccessFile(يول, ھالىتى);
    }
    public static int ئوقۇ(RandomAccessFile ھۆججەت, byte[] data) throws IOException {
        return ھۆججەت.read(data);
    }
    public static void ياز(RandomAccessFile ھۆججەت, byte[] data) throws IOException {
        ھۆججەت.write(data);
    }
    public static void seek(RandomAccessFile ھۆججەت, long ئورۇن) throws IOException {
        ھۆججەت.seek(ئورۇن);
    }
    public static void sync(RandomAccessFile ھۆججەت) throws IOException {
        ھۆججەت.getFD().sync();
    }
    public static void ياپ(RandomAccessFile ھۆججەت) throws IOException {
        ھۆججەت.close();
    }
    public static void چىقىرىۋەت(String يول) throws IOException {
        Files.delete(Paths.get(يول));
    }
    public static long چوڭلۇقى(String يول) throws IOException {
        return Files.size(Paths.get(يول));
    }
    public static Socket ئۇلا(String address, int ئېغىز) throws IOException {
        return new Socket(address, ئېغىز);
    }
    public static DatagramSocket datagram(int ئېغىز) throws SocketException {
        return new DatagramSocket(ئېغىز);
    }
    public static Thread thread(Runnable مەشغۇلات) {
        Thread thread = new Thread(مەشغۇلات);
        thread.start();
        return thread;
    }
    public static Process ئىجرا_قىل(List<String> بۇيرۇق) throws IOException {
        return new ProcessBuilder(بۇيرۇق).start();
    }
}
