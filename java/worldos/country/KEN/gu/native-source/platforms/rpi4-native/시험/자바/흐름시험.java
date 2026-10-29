// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket સર્વર_મૂલ્ય = new ServerSocket(9250);
        Socket અતિથિ_મૂલ્ય = new Socket("localhost", 9250);
        Socket સંપર્ક_કરો = સર્વર_મૂલ્ય.accept();
        if (સંપર્ક_કરો.getPort() != અતિથિ_મૂલ્ય.getLocalPort() || અતિથિ_મૂલ્ય.getPort() != સંપર્ક_કરો.getLocalPort()) throw new RuntimeException("પૉર્ટ_મૂલ્ય 불일치");
        byte[] 전문 = "한글 સ્ટ્રીમ_મૂલ્ય".getBytes("UTF-8");
        અતિથિ_મૂલ્ય.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int લંબાઈ_મૂલ્ય = સંપર્ક_કરો.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(લંબાઈ_મૂલ્ય == 전문.length);
        for (int i = 0; i < લંબાઈ_મૂલ્ય; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("સામગ્રી_મૂલ્ય 불일치");
        સંપર્ક_કરો.getOutputStream().write(42);
        System.out.println(અતિથિ_મૂલ્ય.getInputStream().read());
        અતિથિ_મૂલ્ય.close();
        System.out.println(સંપર્ક_કરો.getInputStream().read());
        સંપર્ક_કરો.close(); સર્વર_મૂલ્ય.close();
        ServerSocket ખાલી_સર્વર = new ServerSocket(9250);
        ખાલી_સર્વર.setSoTimeout(10);
        try { ખાલી_સર્વર.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("સમય_મૂલ્ય 제한"); }
        ખાલી_સર્વર.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
