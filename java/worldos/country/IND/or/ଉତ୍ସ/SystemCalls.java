// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_or;
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
    public static RandomAccessFile ଖୋଲନ୍ତୁ(String ପଥ, String ଧାରା) throws IOException {
        return new RandomAccessFile(ପଥ, ଧାରା);
    }
    public static int ପଢନ୍ତୁ(RandomAccessFile ଫାଇଲ, byte[] data) throws IOException {
        return ଫାଇଲ.read(data);
    }
    public static void ଲେଖନ୍ତୁ(RandomAccessFile ଫାଇଲ, byte[] data) throws IOException {
        ଫାଇଲ.write(data);
    }
    public static void seek(RandomAccessFile ଫାଇଲ, long ଅବସ୍ଥାନ) throws IOException {
        ଫାଇଲ.seek(ଅବସ୍ଥାନ);
    }
    public static void sync(RandomAccessFile ଫାଇଲ) throws IOException {
        ଫାଇଲ.getFD().sync();
    }
    public static void ବନ୍ଦ_କରନ୍ତୁ(RandomAccessFile ଫାଇଲ) throws IOException {
        ଫାଇଲ.close();
    }
    public static void ଅପସାରଣ_କରନ୍ତୁ(String ପଥ) throws IOException {
        Files.delete(Paths.get(ପଥ));
    }
    public static long ଆକାର(String ପଥ) throws IOException {
        return Files.size(Paths.get(ପଥ));
    }
    public static Socket ସଂଯୋଗ_କରନ୍ତୁ(String address, int ସଂଯୋଗିକୀ) throws IOException {
        return new Socket(address, ସଂଯୋଗିକୀ);
    }
    public static DatagramSocket datagram(int ସଂଯୋଗିକୀ) throws SocketException {
        return new DatagramSocket(ସଂଯୋଗିକୀ);
    }
    public static Thread thread(Runnable କାମ) {
        Thread thread = new Thread(କାମ);
        thread.start();
        return thread;
    }
    public static Process ନିଷ୍ପାଦନ_କରନ୍ତୁ(List<String> ନିର୍ଦ୍ଦେଶ) throws IOException {
        return new ProcessBuilder(ନିର୍ଦ୍ଦେଶ).start();
    }
}
