// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket apèsè_iye = new ServerSocket(9250);
        Socket àlejò_iye = new Socket("localhost", 9250);
        Socket Darapọ̀ = apèsè_iye.accept();
        if (Darapọ̀.getPort() != àlejò_iye.getLocalPort() || àlejò_iye.getPort() != Darapọ̀.getLocalPort()) throw new RuntimeException("ojú_iye 불일치");
        byte[] 전문 = "한글 Stream_iye".getBytes("UTF-8");
        àlejò_iye.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int gígùn_iye = Darapọ̀.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(gígùn_iye == 전문.length);
        for (int i = 0; i < gígùn_iye; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Àkóónú_iye 불일치");
        Darapọ̀.getOutputStream().write(42);
        System.out.println(àlejò_iye.getInputStream().read());
        àlejò_iye.close();
        System.out.println(Darapọ̀.getInputStream().read());
        Darapọ̀.close(); apèsè_iye.close();
        ServerSocket òfìfo_apèsè = new ServerSocket(9250);
        òfìfo_apèsè.setSoTimeout(10);
        try { òfìfo_apèsè.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        òfìfo_apèsè.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
