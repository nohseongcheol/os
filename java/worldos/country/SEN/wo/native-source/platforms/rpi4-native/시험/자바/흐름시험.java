// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket dëggu_xëyma = new ServerSocket(9250);
        Socket gan_xëyma = new Socket("localhost", 9250);
        Socket JOKKOO = dëggu_xëyma.accept();
        if (JOKKOO.getPort() != gan_xëyma.getLocalPort() || gan_xëyma.getPort() != JOKKOO.getLocalPort()) throw new RuntimeException("jël_xëyma 불일치");
        byte[] 전문 = "한글 dawal_xëyma".getBytes("UTF-8");
        gan_xëyma.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int diir_xëyma = JOKKOO.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(diir_xëyma == 전문.length);
        for (int i = 0; i < diir_xëyma; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Këmb_xëyma 불일치");
        JOKKOO.getOutputStream().write(42);
        System.out.println(gan_xëyma.getInputStream().read());
        gan_xëyma.close();
        System.out.println(JOKKOO.getInputStream().read());
        JOKKOO.close(); dëggu_xëyma.close();
        ServerSocket neen_dëggu = new ServerSocket(9250);
        neen_dëggu.setSoTimeout(10);
        try { neen_dëggu.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        neen_dëggu.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
