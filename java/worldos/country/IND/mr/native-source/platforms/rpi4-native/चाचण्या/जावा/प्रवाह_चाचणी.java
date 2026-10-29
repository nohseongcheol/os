// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class प्रवाह_चाचणी {
    public static void main(String[] args) throws Exception {
        ServerSocket सर्व्हर_मूल्य = new ServerSocket(9250);
        Socket अतिथी_मूल्य = new Socket("localhost", 9250);
        Socket जोडा = सर्व्हर_मूल्य.accept();
        if (जोडा.getPort() != अतिथी_मूल्य.getLocalPort() || अतिथी_मूल्य.getPort() != जोडा.getLocalPort()) throw new RuntimeException("पॉर्ट_मूल्य 불일치");
        byte[] स्वतंत्रसंदेश = "한글 प्रवाह_मूल्य".getBytes("UTF-8");
        अतिथी_मूल्य.getOutputStream().write(स्वतंत्रसंदेश);
        byte[] स्वीकारलेले_आयटम = new byte[100];
        int लांबी_मूल्य = जोडा.getInputStream().read(स्वीकारलेले_आयटम, 0, स्वीकारलेले_आयटम.length);
        System.out.println(लांबी_मूल्य == स्वतंत्रसंदेश.length);
        for (int i = 0; i < लांबी_मूल्य; i++) if (स्वीकारलेले_आयटम[i] != स्वतंत्रसंदेश[i]) throw new RuntimeException("सामुग्री_मूल्य 불일치");
        जोडा.getOutputStream().write(42);
        System.out.println(अतिथी_मूल्य.getInputStream().read());
        अतिथी_मूल्य.close();
        System.out.println(जोडा.getInputStream().read());
        जोडा.close(); सर्व्हर_मूल्य.close();
        ServerSocket रिक्त_सर्व्हर = new ServerSocket(9250);
        रिक्त_सर्व्हर.setSoTimeout(10);
        try { रिक्त_सर्व्हर.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("वेळ_मूल्य मर्यादा_मूल्य"); }
        रिक्त_सर्व्हर.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS आहे_असमर्थित"); }
        System.out.println("STREAM PASS");
    }
}
