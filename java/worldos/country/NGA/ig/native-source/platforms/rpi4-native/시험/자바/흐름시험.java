// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket savà_valuu = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket Banye = savà_valuu.accept();
        if (Banye.getPort() != 손님.getLocalPort() || 손님.getPort() != Banye.getLocalPort()) throw new RuntimeException("pọọt_valuu 불일치");
        byte[] 전문 = "한글 agịrị_valuu".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ogologo_valuu = Banye.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ogologo_valuu == 전문.length);
        for (int i = 0; i < ogologo_valuu; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ndịnà_valuu 불일치");
        Banye.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(Banye.getInputStream().read());
        Banye.close(); savà_valuu.close();
        ServerSocket oghere_savà = new ServerSocket(9250);
        oghere_savà.setSoTimeout(10);
        try { oghere_savà.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        oghere_savà.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
