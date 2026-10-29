// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket Iseva_inani = new ServerSocket(9250);
        Socket isivakashi_inani = new Socket("localhost", 9250);
        Socket Xhumanisa = Iseva_inani.accept();
        if (Xhumanisa.getPort() != isivakashi_inani.getLocalPort() || isivakashi_inani.getPort() != Xhumanisa.getLocalPort()) throw new RuntimeException("intuba_inani 불일치");
        byte[] 전문 = "한글 Stream_inani".getBytes("UTF-8");
        isivakashi_inani.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ubude_inani = Xhumanisa.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ubude_inani == 전문.length);
        for (int i = 0; i < ubude_inani; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Okuqukethwe_inani 불일치");
        Xhumanisa.getOutputStream().write(42);
        System.out.println(isivakashi_inani.getInputStream().read());
        isivakashi_inani.close();
        System.out.println(Xhumanisa.getInputStream().read());
        Xhumanisa.close(); Iseva_inani.close();
        ServerSocket okungasho_lutho_Iseva = new ServerSocket(9250);
        okungasho_lutho_Iseva.setSoTimeout(10);
        try { okungasho_lutho_Iseva.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        okungasho_lutho_Iseva.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
