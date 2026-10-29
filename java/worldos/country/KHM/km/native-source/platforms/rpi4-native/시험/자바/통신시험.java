// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket ខាងមុខ_តំលៃ = 통신.បើក(9431), ការថយ_តំលៃ = 통신.បើក(9432);
        try {
            통신.ផ្ញើ(ខាងមុខ_តំលៃ, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ការថយ_តំលៃ));
            byte[] ប្រភព = 문자.부호화("회신"); ខាងមុខ_តំលៃ.send(new DatagramPacket(ប្រភព, ប្រភព.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); ការថយ_តំលៃ.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ការថយ_តំលៃ.getLocalPort());
            ការថយ_តំលៃ.setSoTimeout(10);
            try { ការថយ_តំលៃ.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 ពេល_វេលា_តំលៃ 초과"); }
            ការថយ_តំលៃ.close();
            try { ការថយ_តំលៃ.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { ខាងមុខ_តំលៃ.close(); ការថយ_តំលៃ.close(); }
    }
}
