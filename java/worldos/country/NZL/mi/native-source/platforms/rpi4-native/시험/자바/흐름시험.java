// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket tūmau_uara = new ServerSocket(9250);
        Socket manuhiri_uara = new Socket("localhost", 9250);
        Socket TŪHONO = tūmau_uara.accept();
        if (TŪHONO.getPort() != manuhiri_uara.getLocalPort() || manuhiri_uara.getPort() != TŪHONO.getLocalPort()) throw new RuntimeException("kawe_uara 불일치");
        byte[] 전문 = "한글 roma_uara".getBytes("UTF-8");
        manuhiri_uara.getOutputStream().write(전문);
        byte[] RECEIVED_tuemi = new byte[100];
        int roa_uara = TŪHONO.getInputStream().read(RECEIVED_tuemi, 0, RECEIVED_tuemi.length);
        System.out.println(roa_uara == 전문.length);
        for (int i = 0; i < roa_uara; i++) if (RECEIVED_tuemi[i] != 전문[i]) throw new RuntimeException("Ihirangi_uara 불일치");
        TŪHONO.getOutputStream().write(42);
        System.out.println(manuhiri_uara.getInputStream().read());
        manuhiri_uara.close();
        System.out.println(TŪHONO.getInputStream().read());
        TŪHONO.close(); tūmau_uara.close();
        ServerSocket putua_tūmau = new ServerSocket(9250);
        putua_tūmau.setSoTimeout(10);
        try { putua_tūmau.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_uara 제한"); }
        putua_tūmau.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
