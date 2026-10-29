// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket ಸರ್ವರ್_ಮೌಲ್ಯ = new ServerSocket(9250);
        Socket ಅತಿಥಿ_ಮೌಲ್ಯ = new Socket("localhost", 9250);
        Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು = ಸರ್ವರ್_ಮೌಲ್ಯ.accept();
        if (ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getPort() != ಅತಿಥಿ_ಮೌಲ್ಯ.getLocalPort() || ಅತಿಥಿ_ಮೌಲ್ಯ.getPort() != ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getLocalPort()) throw new RuntimeException("ಪೋರ್ಟ್_ಮೌಲ್ಯ 불일치");
        byte[] 전문 = "한글 ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ".getBytes("UTF-8");
        ಅತಿಥಿ_ಮೌಲ್ಯ.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ಉದ್ದ_ಮೌಲ್ಯ = ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ಉದ್ದ_ಮೌಲ್ಯ == 전문.length);
        for (int i = 0; i < ಉದ್ದ_ಮೌಲ್ಯ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ವಿಷಯ_ಮೌಲ್ಯ 불일치");
        ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getOutputStream().write(42);
        System.out.println(ಅತಿಥಿ_ಮೌಲ್ಯ.getInputStream().read());
        ಅತಿಥಿ_ಮೌಲ್ಯ.close();
        System.out.println(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getInputStream().read());
        ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.close(); ಸರ್ವರ್_ಮೌಲ್ಯ.close();
        ServerSocket ಖಾಲಿ_ಸರ್ವರ್ = new ServerSocket(9250);
        ಖಾಲಿ_ಸರ್ವರ್.setSoTimeout(10);
        try { ಖಾಲಿ_ಸರ್ವರ್.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ಸಮಯ_ಮೌಲ್ಯ 제한"); }
        ಖಾಲಿ_ಸರ್ವರ್.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
