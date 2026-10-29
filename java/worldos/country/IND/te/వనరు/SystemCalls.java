// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.IND.l_te;
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
    public static RandomAccessFile తెరువు(String పాత్, String రీతి) throws IOException {
        return new RandomAccessFile(పాత్, రీతి);
    }
    public static int చదువు(RandomAccessFile దస్త్రం, byte[] data) throws IOException {
        return దస్త్రం.read(data);
    }
    public static void వ్రాయుము(RandomAccessFile దస్త్రం, byte[] data) throws IOException {
        దస్త్రం.write(data);
    }
    public static void seek(RandomAccessFile దస్త్రం, long స్థానము) throws IOException {
        దస్త్రం.seek(స్థానము);
    }
    public static void sync(RandomAccessFile దస్త్రం) throws IOException {
        దస్త్రం.getFD().sync();
    }
    public static void మూసివేయి(RandomAccessFile దస్త్రం) throws IOException {
        దస్త్రం.close();
    }
    public static void తీసివేయు(String పాత్) throws IOException {
        Files.delete(Paths.get(పాత్));
    }
    public static long పరిమాణం(String పాత్) throws IOException {
        return Files.size(Paths.get(పాత్));
    }
    public static Socket కనెక్టుచేయి(String address, int పోర్టు) throws IOException {
        return new Socket(address, పోర్టు);
    }
    public static DatagramSocket datagram(int పోర్టు) throws SocketException {
        return new DatagramSocket(పోర్టు);
    }
    public static Thread thread(Runnable చర్య) {
        Thread thread = new Thread(చర్య);
        thread.start();
        return thread;
    }
    public static Process అమలుపరుచు(List<String> ఆదేశము) throws IOException {
        return new ProcessBuilder(ఆదేశము).start();
    }
}
