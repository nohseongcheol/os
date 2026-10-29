// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_ne;
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
    public static RandomAccessFile खोल्नुहोस्(String मार्ग, String मोड) throws IOException {
        return new RandomAccessFile(मार्ग, मोड);
    }
    public static int पढनुहोस्(RandomAccessFile फाइल, byte[] data) throws IOException {
        return फाइल.read(data);
    }
    public static void लेख्नुहोस्(RandomAccessFile फाइल, byte[] data) throws IOException {
        फाइल.write(data);
    }
    public static void seek(RandomAccessFile फाइल, long स्थिति) throws IOException {
        फाइल.seek(स्थिति);
    }
    public static void sync(RandomAccessFile फाइल) throws IOException {
        फाइल.getFD().sync();
    }
    public static void बन्दगर्नुहोस्(RandomAccessFile फाइल) throws IOException {
        फाइल.close();
    }
    public static void हटाउने(String मार्ग) throws IOException {
        Files.delete(Paths.get(मार्ग));
    }
    public static long आकार(String मार्ग) throws IOException {
        return Files.size(Paths.get(मार्ग));
    }
    public static Socket जडान(String address, int पोर्ट) throws IOException {
        return new Socket(address, पोर्ट);
    }
    public static DatagramSocket datagram(int पोर्ट) throws SocketException {
        return new DatagramSocket(पोर्ट);
    }
    public static Thread thread(Runnable कार्य) {
        Thread thread = new Thread(कार्य);
        thread.start();
        return thread;
    }
    public static Process कार्यान्वयन_गर्नुहोस्(List<String> आदेश) throws IOException {
        return new ProcessBuilder(आदेश).start();
    }
}
