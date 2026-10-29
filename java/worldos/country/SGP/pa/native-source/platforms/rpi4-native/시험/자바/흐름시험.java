// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket ਸਰਵਰ_ਕੀਮਤ = new ServerSocket(9250);
        Socket ਗੈਸਟ_ਕੀਮਤ = new Socket("localhost", 9250);
        Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ = ਸਰਵਰ_ਕੀਮਤ.accept();
        if (ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getPort() != ਗੈਸਟ_ਕੀਮਤ.getLocalPort() || ਗੈਸਟ_ਕੀਮਤ.getPort() != ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getLocalPort()) throw new RuntimeException("ਪੋਰਟ_ਕੀਮਤ 불일치");
        byte[] 전문 = "한글 ਸਟ੍ਰੀਮ_ਕੀਮਤ".getBytes("UTF-8");
        ਗੈਸਟ_ਕੀਮਤ.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ਲੰਬਾਈ_ਕੀਮਤ = ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ਲੰਬਾਈ_ਕੀਮਤ == 전문.length);
        for (int i = 0; i < ਲੰਬਾਈ_ਕੀਮਤ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ਤਤਕਰਾ_ਕੀਮਤ 불일치");
        ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getOutputStream().write(42);
        System.out.println(ਗੈਸਟ_ਕੀਮਤ.getInputStream().read());
        ਗੈਸਟ_ਕੀਮਤ.close();
        System.out.println(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getInputStream().read());
        ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.close(); ਸਰਵਰ_ਕੀਮਤ.close();
        ServerSocket ਖਾਲੀ_ਸਰਵਰ = new ServerSocket(9250);
        ਖਾਲੀ_ਸਰਵਰ.setSoTimeout(10);
        try { ਖਾਲੀ_ਸਰਵਰ.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        ਖਾਲੀ_ਸਰਵਰ.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
