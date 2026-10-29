// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.USA.l_vi;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class lời_gọi_hệ_thống {
    private lời_gọi_hệ_thống() { }
    public static RandomAccessFile Mở(String đườngDẫn, String Chế_độ) throws IOException {
        return new RandomAccessFile(đườngDẫn, Chế_độ);
    }
    public static int Đọc(RandomAccessFile tậpTin, byte[] dữLiệu) throws IOException {
        return tậpTin.read(dữLiệu);
    }
    public static void Ghi(RandomAccessFile tậpTin, byte[] dữLiệu) throws IOException {
        tậpTin.write(dữLiệu);
    }
    public static void seek(RandomAccessFile tậpTin, long vị_trí) throws IOException {
        tậpTin.seek(vị_trí);
    }
    public static void sync(RandomAccessFile tậpTin) throws IOException {
        tậpTin.getFD().sync();
    }
    public static void Đóng_tập_tin(RandomAccessFile tậpTin) throws IOException {
        tậpTin.close();
    }
    public static void Gỡ_bỏ(String đườngDẫn) throws IOException {
        Files.delete(Paths.get(đườngDẫn));
    }
    public static long Kích_cỡ(String đườngDẫn) throws IOException {
        return Files.size(Paths.get(đườngDẫn));
    }
    public static Socket Kết_nối(String address, int sốCổng) throws IOException {
        return new Socket(address, sốCổng);
    }
    public static DatagramSocket datagram(int sốCổng) throws SocketException {
        return new DatagramSocket(sốCổng);
    }
    public static Thread luồngThựcThi(Runnable Hành_động) {
        Thread luồngThựcThi = new Thread(Hành_động);
        luồngThựcThi.start();
        return luồngThựcThi;
    }
    public static Process Chạy(List<String> lệnh) throws IOException {
        return new ProcessBuilder(lệnh).start();
    }
}
