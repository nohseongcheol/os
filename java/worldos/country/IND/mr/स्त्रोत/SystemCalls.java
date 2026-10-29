// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_mr;
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
    public static RandomAccessFile उघडा(String मार्ग, String पद्धती) throws IOException {
        return new RandomAccessFile(मार्ग, पद्धती);
    }
    public static int वाचन(RandomAccessFile फाइल, byte[] data) throws IOException {
        return फाइल.read(data);
    }
    public static void लेखन(RandomAccessFile फाइल, byte[] data) throws IOException {
        फाइल.write(data);
    }
    public static void seek(RandomAccessFile फाइल, long जागा) throws IOException {
        फाइल.seek(जागा);
    }
    public static void sync(RandomAccessFile फाइल) throws IOException {
        फाइल.getFD().sync();
    }
    public static void बंद_करा(RandomAccessFile फाइल) throws IOException {
        फाइल.close();
    }
    public static void काढून_टाका(String मार्ग) throws IOException {
        Files.delete(Paths.get(मार्ग));
    }
    public static long आकार(String मार्ग) throws IOException {
        return Files.size(Paths.get(मार्ग));
    }
    public static Socket जोडा(String address, int पोर्ट) throws IOException {
        return new Socket(address, पोर्ट);
    }
    public static DatagramSocket datagram(int पोर्ट) throws SocketException {
        return new DatagramSocket(पोर्ट);
    }
    public static Thread thread(Runnable कृती) {
        Thread thread = new Thread(कृती);
        thread.start();
        return thread;
    }
    public static Process कार्यान्वित_करा(List<String> आदेश) throws IOException {
        return new ProcessBuilder(आदेश).start();
    }
}
