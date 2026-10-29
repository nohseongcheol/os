// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket sefara_Boleng = new ServerSocket(9250);
        Socket moeng_Boleng = new Socket("localhost", 9250);
        Socket Golaganya = sefara_Boleng.accept();
        if (Golaganya.getPort() != moeng_Boleng.getLocalPort() || moeng_Boleng.getPort() != Golaganya.getLocalPort()) throw new RuntimeException("gorogisetsa_Boleng 불일치");
        byte[] 전문 = "한글 moela_Boleng".getBytes("UTF-8");
        moeng_Boleng.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int boleele_Boleng = Golaganya.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(boleele_Boleng == 전문.length);
        for (int i = 0; i < boleele_Boleng; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Diteng_Boleng 불일치");
        Golaganya.getOutputStream().write(42);
        System.out.println(moeng_Boleng.getInputStream().read());
        moeng_Boleng.close();
        System.out.println(Golaganya.getInputStream().read());
        Golaganya.close(); sefara_Boleng.close();
        ServerSocket lolea_sefara = new ServerSocket(9250);
        lolea_sefara.setSoTimeout(10);
        try { lolea_sefara.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        lolea_sefara.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
