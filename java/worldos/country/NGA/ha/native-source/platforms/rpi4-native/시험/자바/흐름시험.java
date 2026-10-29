// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket Saba_Daraja = new ServerSocket(9250);
        Socket baƙo_Daraja = new Socket("localhost", 9250);
        Socket Haɗi = Saba_Daraja.accept();
        if (Haɗi.getPort() != baƙo_Daraja.getLocalPort() || baƙo_Daraja.getPort() != Haɗi.getLocalPort()) throw new RuntimeException("fot_Daraja 불일치");
        byte[] 전문 = "한글 watsuwa_Daraja".getBytes("UTF-8");
        baƙo_Daraja.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int Tsawo_Daraja = Haɗi.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(Tsawo_Daraja == 전문.length);
        for (int i = 0; i < Tsawo_Daraja; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("kunshiya_Daraja 불일치");
        Haɗi.getOutputStream().write(42);
        System.out.println(baƙo_Daraja.getInputStream().read());
        baƙo_Daraja.close();
        System.out.println(Haɗi.getInputStream().read());
        Haɗi.close(); Saba_Daraja.close();
        ServerSocket holoko_Saba = new ServerSocket(9250);
        holoko_Saba.setSoTimeout(10);
        try { holoko_Saba.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("lokaci_Daraja 제한"); }
        holoko_Saba.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
