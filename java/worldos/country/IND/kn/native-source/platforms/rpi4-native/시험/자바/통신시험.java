// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import ಕನ್ನಡ.자체.문자;
import ಕನ್ನಡ.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket ಮುಂದೆ_ಮೌಲ್ಯ = 통신.ತೆರೆ(9431), ಹಿಂದೆ_ಮೌಲ್ಯ = 통신.ತೆರೆ(9432);
        try {
            통신.ಕಳುಹಿಸಿ(ಮುಂದೆ_ಮೌಲ್ಯ, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ಹಿಂದೆ_ಮೌಲ್ಯ));
            byte[] ಮೂಲ = 문자.부호화("회신"); ಮುಂದೆ_ಮೌಲ್ಯ.send(new DatagramPacket(ಮೂಲ, ಮೂಲ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); ಹಿಂದೆ_ಮೌಲ್ಯ.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ಹಿಂದೆ_ಮೌಲ್ಯ.getLocalPort());
            ಹಿಂದೆ_ಮೌಲ್ಯ.setSoTimeout(10);
            try { ಹಿಂದೆ_ಮೌಲ್ಯ.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 ಸಮಯ_ಮೌಲ್ಯ 초과"); }
            ಹಿಂದೆ_ಮೌಲ್ಯ.close();
            try { ಹಿಂದೆ_ಮೌಲ್ಯ.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { ಮುಂದೆ_ಮೌಲ್ಯ.close(); ಹಿಂದೆ_ಮೌಲ್ಯ.close(); }
    }
}
