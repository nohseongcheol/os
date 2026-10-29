// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket tenar_VALUE = new ServerSocket(9250);
        Socket gjest_VALUE = new Socket("localhost", 9250);
        Socket Kopla_til = tenar_VALUE.accept();
        if (Kopla_til.getPort() != gjest_VALUE.getLocalPort() || gjest_VALUE.getPort() != Kopla_til.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        gjest_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_vare = new byte[100];
        int lengd_VALUE = Kopla_til.getInputStream().read(RECEIVED_vare, 0, RECEIVED_vare.length);
        System.out.println(lengd_VALUE == 전문.length);
        for (int i = 0; i < lengd_VALUE; i++) if (RECEIVED_vare[i] != 전문[i]) throw new RuntimeException("Innhald_VALUE 불일치");
        Kopla_til.getOutputStream().write(42);
        System.out.println(gjest_VALUE.getInputStream().read());
        gjest_VALUE.close();
        System.out.println(Kopla_til.getInputStream().read());
        Kopla_til.close(); tenar_VALUE.close();
        ServerSocket tom_tenar = new ServerSocket(9250);
        tom_tenar.setSoTimeout(10);
        try { tom_tenar.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        tom_tenar.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
