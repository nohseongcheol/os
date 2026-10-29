// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket seva_thamani = new ServerSocket(9250);
        Socket mgeni_thamani = new Socket("localhost", 9250);
        Socket UNGANISHA = seva_thamani.accept();
        if (UNGANISHA.getPort() != mgeni_thamani.getLocalPort() || mgeni_thamani.getPort() != UNGANISHA.getLocalPort()) throw new RuntimeException("kituo_thamani 불일치");
        byte[] 전문 = "한글 Stream_thamani".getBytes("UTF-8");
        mgeni_thamani.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int urefu_thamani = UNGANISHA.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(urefu_thamani == 전문.length);
        for (int i = 0; i < urefu_thamani; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("maudhui_thamani 불일치");
        UNGANISHA.getOutputStream().write(42);
        System.out.println(mgeni_thamani.getInputStream().read());
        mgeni_thamani.close();
        System.out.println(UNGANISHA.getInputStream().read());
        UNGANISHA.close(); seva_thamani.close();
        ServerSocket tupu_seva = new ServerSocket(9250);
        tupu_seva.setSoTimeout(10);
        try { tupu_seva.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("saa_thamani_4692cef5 제한"); }
        tupu_seva.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
