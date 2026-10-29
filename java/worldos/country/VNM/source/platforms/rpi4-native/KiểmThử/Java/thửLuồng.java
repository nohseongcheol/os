// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class thửLuồng {
    public static void main(String[] args) throws Exception {
        ServerSocket giáTrịMáyChủ = new ServerSocket(9250);
        Socket giáTrịKhách = new Socket("localhost", 9250);
        Socket nốiKết = giáTrịMáyChủ.accept();
        if (nốiKết.getPort() != giáTrịKhách.getLocalPort() || giáTrịKhách.getPort() != nốiKết.getLocalPort()) throw new RuntimeException("giáTrịCổng 불일치");
        byte[] điệnDữLiệu = "한글 giáTrịLuồng".getBytes("UTF-8");
        giáTrịKhách.getOutputStream().write(điệnDữLiệu);
        byte[] phầnMụcĐãNhận = new byte[100];
        int độDài = nốiKết.getInputStream().read(phầnMụcĐãNhận, 0, phầnMụcĐãNhận.length);
        System.out.println(độDài == điệnDữLiệu.length);
        for (int i = 0; i < độDài; i++) if (phầnMụcĐãNhận[i] != điệnDữLiệu[i]) throw new RuntimeException("giáTrịNộiDung 불일치");
        nốiKết.getOutputStream().write(42);
        System.out.println(giáTrịKhách.getInputStream().read());
        giáTrịKhách.close();
        System.out.println(nốiKết.getInputStream().read());
        nốiKết.close(); giáTrịMáyChủ.close();
        ServerSocket máyChủRỗng = new ServerSocket(9250);
        máyChủRỗng.setSoTimeout(10);
        try { máyChủRỗng.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("giáTrịThờiGian giáTrịGiớiHạn"); }
        máyChủRỗng.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS làKhôngHỗTrợ"); }
        System.out.println("STREAM PASS");
    }
}
