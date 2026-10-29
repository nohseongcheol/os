// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LKA.l_si;
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
    public static RandomAccessFile විවෘත_කරන්න(String මාර්_ගය, String mode) throws IOException {
        return new RandomAccessFile(මාර්_ගය, mode);
    }
    public static int කියවීම(RandomAccessFile ගොනු, byte[] data) throws IOException {
        return ගොනු.read(data);
    }
    public static void ලිවීම(RandomAccessFile ගොනු, byte[] data) throws IOException {
        ගොනු.write(data);
    }
    public static void seek(RandomAccessFile ගොනු, long පිහිටීම) throws IOException {
        ගොනු.seek(පිහිටීම);
    }
    public static void sync(RandomAccessFile ගොනු) throws IOException {
        ගොනු.getFD().sync();
    }
    public static void වසන්න(RandomAccessFile ගොනු) throws IOException {
        ගොනු.close();
    }
    public static void ඉවත්_කරන්න(String මාර්_ගය) throws IOException {
        Files.delete(Paths.get(මාර්_ගය));
    }
    public static long ප්_රමාණය(String මාර්_ගය) throws IOException {
        return Files.size(Paths.get(මාර්_ගය));
    }
    public static Socket සම්බන්ද_වන්න(String address, int කෙවනිය) throws IOException {
        return new Socket(address, කෙවනිය);
    }
    public static DatagramSocket datagram(int කෙවනිය) throws SocketException {
        return new DatagramSocket(කෙවනිය);
    }
    public static Thread thread(Runnable ක්_රීයාව) {
        Thread thread = new Thread(ක්_රීයාව);
        thread.start();
        return thread;
    }
    public static Process ක්_රියාත්මක_කරන්න(List<String> විධානය) throws IOException {
        return new ProcessBuilder(විධානය).start();
    }
}
