// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MUS.l_ta;
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
    public static RandomAccessFile திற(String பாதை_2, String முறைமை) throws IOException {
        return new RandomAccessFile(பாதை_2, முறைமை);
    }
    public static int படி(RandomAccessFile கோப்பின்_பெயர், byte[] data) throws IOException {
        return கோப்பின்_பெயர்.read(data);
    }
    public static void எழுது(RandomAccessFile கோப்பின்_பெயர், byte[] data) throws IOException {
        கோப்பின்_பெயர்.write(data);
    }
    public static void seek(RandomAccessFile கோப்பின்_பெயர், long இடம்) throws IOException {
        கோப்பின்_பெயர்.seek(இடம்);
    }
    public static void sync(RandomAccessFile கோப்பின்_பெயர்) throws IOException {
        கோப்பின்_பெயர்.getFD().sync();
    }
    public static void மூடு(RandomAccessFile கோப்பின்_பெயர்) throws IOException {
        கோப்பின்_பெயர்.close();
    }
    public static void நீக்கு(String பாதை_2) throws IOException {
        Files.delete(Paths.get(பாதை_2));
    }
    public static long அளவு(String பாதை_2) throws IOException {
        return Files.size(Paths.get(பாதை_2));
    }
    public static Socket இணைக்க(String address, int துறை) throws IOException {
        return new Socket(address, துறை);
    }
    public static DatagramSocket datagram(int துறை) throws SocketException {
        return new DatagramSocket(துறை);
    }
    public static Thread thread(Runnable செயல்) {
        Thread thread = new Thread(செயல்);
        thread.start();
        return thread;
    }
    public static Process செயற்படுத்துக(List<String> கட்டளை) throws IOException {
        return new ProcessBuilder(கட்டளை).start();
    }
}
