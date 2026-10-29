// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket አገልጋይ_እሴት = new ServerSocket(9250);
        Socket እንግዳ_እሴት = new Socket("localhost", 9250);
        Socket መገናኛ = አገልጋይ_እሴት.accept();
        if (መገናኛ.getPort() != እንግዳ_እሴት.getLocalPort() || እንግዳ_እሴት.getPort() != መገናኛ.getLocalPort()) throw new RuntimeException("ወደብ_እሴት 불일치");
        byte[] 전문 = "한글 ልቀቅ_እሴት".getBytes("UTF-8");
        እንግዳ_እሴት.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ርዝመት_እሴት = መገናኛ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ርዝመት_እሴት == 전문.length);
        for (int i = 0; i < ርዝመት_እሴት; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ይዘት_እሴት 불일치");
        መገናኛ.getOutputStream().write(42);
        System.out.println(እንግዳ_እሴት.getInputStream().read());
        እንግዳ_እሴት.close();
        System.out.println(መገናኛ.getInputStream().read());
        መገናኛ.close(); አገልጋይ_እሴት.close();
        ServerSocket ባዶ_አገልጋይ = new ServerSocket(9250);
        ባዶ_አገልጋይ.setSoTimeout(10);
        try { ባዶ_አገልጋይ.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ጊዜ_እሴት 제한"); }
        ባዶ_አገልጋይ.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
