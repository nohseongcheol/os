// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket مۇلازىمىتېر_قىممىتى = new ServerSocket(9250);
        Socket مېھمان_قىممىتى = new Socket("localhost", 9250);
        Socket ئۇلا = مۇلازىمىتېر_قىممىتى.accept();
        if (ئۇلا.getPort() != مېھمان_قىممىتى.getLocalPort() || مېھمان_قىممىتى.getPort() != ئۇلا.getLocalPort()) throw new RuntimeException("ئېغىز_قىممىتى 불일치");
        byte[] 전문 = "한글 ئېقىم_قىممىتى".getBytes("UTF-8");
        مېھمان_قىممىتى.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ئۇزۇنلۇق_قىممىتى = ئۇلا.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ئۇزۇنلۇق_قىممىتى == 전문.length);
        for (int i = 0; i < ئۇزۇنلۇق_قىممىتى; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("مەزمۇن_قىممىتى 불일치");
        ئۇلا.getOutputStream().write(42);
        System.out.println(مېھمان_قىممىتى.getInputStream().read());
        مېھمان_قىممىتى.close();
        System.out.println(ئۇلا.getInputStream().read());
        ئۇلا.close(); مۇلازىمىتېر_قىممىتى.close();
        ServerSocket بوش_مۇلازىمىتېر = new ServerSocket(9250);
        بوش_مۇلازىمىتېر.setSoTimeout(10);
        try { بوش_مۇلازىمىتېر.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        بوش_مۇلازىمىتېر.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
