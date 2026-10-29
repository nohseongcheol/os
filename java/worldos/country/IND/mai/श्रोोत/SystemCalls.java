// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_mai;
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
    public static RandomAccessFile खोलू(String पथ, String मोड) throws IOException {
        return new RandomAccessFile(पथ, मोड);
    }
    public static int पढ़ू(RandomAccessFile फाइल, byte[] data) throws IOException {
        return फाइल.read(data);
    }
    public static void लिखू(RandomAccessFile फाइल, byte[] data) throws IOException {
        फाइल.write(data);
    }
    public static void seek(RandomAccessFile फाइल, long स्थिति) throws IOException {
        फाइल.seek(स्थिति);
    }
    public static void sync(RandomAccessFile फाइल) throws IOException {
        फाइल.getFD().sync();
    }
    public static void बन्न_करू(RandomAccessFile फाइल) throws IOException {
        फाइल.close();
    }
    public static void हटाबू(String पथ) throws IOException {
        Files.delete(Paths.get(पथ));
    }
    public static long आकार(String पथ) throws IOException {
        return Files.size(Paths.get(पथ));
    }
    public static Socket जुड़ू(String address, int पोर्ट) throws IOException {
        return new Socket(address, पोर्ट);
    }
    public static DatagramSocket datagram(int पोर्ट) throws SocketException {
        return new DatagramSocket(पोर्ट);
    }
    public static Thread thread(Runnable क्रिया) {
        Thread thread = new Thread(क्रिया);
        thread.start();
        return thread;
    }
    public static Process चलाउ(List<String> कमांड) throws IOException {
        return new ProcessBuilder(कमांड).start();
    }
}
