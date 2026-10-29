// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket sarworde_njaru = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket seŋaade = sarworde_njaru.accept();
        if (seŋaade.getPort() != 손님.getLocalPort() || 손님.getPort() != seŋaade.getLocalPort()) throw new RuntimeException("poor_njaru 불일치");
        byte[] 전문 = "한글 waraango_njaru".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int njuuteendi_njaru = seŋaade.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(njuuteendi_njaru == 전문.length);
        for (int i = 0; i < njuuteendi_njaru; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("loowdi_njaru 불일치");
        seŋaade.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(seŋaade.getInputStream().read());
        seŋaade.close(); sarworde_njaru.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
