// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket ኣገልጋሊ_ዋጋ = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket ኣላግብ = ኣገልጋሊ_ዋጋ.accept();
        if (ኣላግብ.getPort() != 손님.getLocalPort() || 손님.getPort() != ኣላግብ.getLocalPort()) throw new RuntimeException("ወደብ_ዋጋ 불일치");
        byte[] 전문 = "한글 ወሓዚ_ዋጋ".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ንውሓት_ዋጋ = ኣላግብ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ንውሓት_ዋጋ == 전문.length);
        for (int i = 0; i < ንውሓት_ዋጋ; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ትሕዝቶ_ዋጋ 불일치");
        ኣላግብ.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(ኣላግብ.getInputStream().read());
        ኣላግብ.close(); ኣገልጋሊ_ዋጋ.close();
        ServerSocket ባዶ_ኣገልጋሊ = new ServerSocket(9250);
        ባዶ_ኣገልጋሊ.setSoTimeout(10);
        try { ባዶ_ኣገልጋሊ.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        ባዶ_ኣገልጋሊ.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
