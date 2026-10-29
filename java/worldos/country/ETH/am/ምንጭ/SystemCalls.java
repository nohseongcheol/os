// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ETH.l_am;
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
    public static RandomAccessFile መክፈቻ(String መተላለፊያ, String የአሠራሩ_ዘዴ) throws IOException {
        return new RandomAccessFile(መተላለፊያ, የአሠራሩ_ዘዴ);
    }
    public static int ማንበቢያ(RandomAccessFile ፋይል, byte[] data) throws IOException {
        return ፋይል.read(data);
    }
    public static void መጻፊያ(RandomAccessFile ፋይል, byte[] data) throws IOException {
        ፋይል.write(data);
    }
    public static void seek(RandomAccessFile ፋይል, long አካባቢ) throws IOException {
        ፋይል.seek(አካባቢ);
    }
    public static void sync(RandomAccessFile ፋይል) throws IOException {
        ፋይል.getFD().sync();
    }
    public static void መዝጊያ(RandomAccessFile ፋይል) throws IOException {
        ፋይል.close();
    }
    public static void ማስወገጃ(String መተላለፊያ) throws IOException {
        Files.delete(Paths.get(መተላለፊያ));
    }
    public static long መጠን(String መተላለፊያ) throws IOException {
        return Files.size(Paths.get(መተላለፊያ));
    }
    public static Socket መገናኛ(String address, int port) throws IOException {
        return new Socket(address, port);
    }
    public static DatagramSocket datagram(int port) throws SocketException {
        return new DatagramSocket(port);
    }
    public static Thread thread(Runnable ተግባር) {
        Thread thread = new Thread(ተግባር);
        thread.start();
        return thread;
    }
    public static Process መፈጸሚያ(List<String> ትእዛዝ) throws IOException {
        return new ProcessBuilder(ትእዛዝ).start();
    }
}
