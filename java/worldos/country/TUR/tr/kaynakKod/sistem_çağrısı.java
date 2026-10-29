// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TUR.l_tr;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class sistem_çağrısı {
    private sistem_çağrısı() { }
    public static RandomAccessFile Aç(String yol, String Kip) throws IOException {
        return new RandomAccessFile(yol, Kip);
    }
    public static int Okuma(RandomAccessFile dosya, byte[] veri) throws IOException {
        return dosya.read(veri);
    }
    public static void Yazma(RandomAccessFile dosya, byte[] veri) throws IOException {
        dosya.write(veri);
    }
    public static void seek(RandomAccessFile dosya, long konum) throws IOException {
        dosya.seek(konum);
    }
    public static void sync(RandomAccessFile dosya) throws IOException {
        dosya.getFD().sync();
    }
    public static void Kapat(RandomAccessFile dosya) throws IOException {
        dosya.close();
    }
    public static void Kaldır(String yol) throws IOException {
        Files.delete(Paths.get(yol));
    }
    public static long Boyut(String yol) throws IOException {
        return Files.size(Paths.get(yol));
    }
    public static Socket Bağlan(String address, int bağlantıNoktasıNumarası) throws IOException {
        return new Socket(address, bağlantıNoktasıNumarası);
    }
    public static DatagramSocket datagram(int bağlantıNoktasıNumarası) throws SocketException {
        return new DatagramSocket(bağlantıNoktasıNumarası);
    }
    public static Thread yürütmeİşParçacığı(Runnable Eylem) {
        Thread yürütmeİşParçacığı = new Thread(Eylem);
        yürütmeİşParçacığı.start();
        return yürütmeİşParçacığı;
    }
    public static Process Çalıştır(List<String> komut) throws IOException {
        return new ProcessBuilder(komut).start();
    }
}
