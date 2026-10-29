// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import ਪੰਜਾਬੀ.자체.문자;
import ਪੰਜਾਬੀ.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.ਖੋਲ੍ਹੋ(9431), ਪਿਛਲਾ_ਕੀਮਤ = 통신.ਖੋਲ੍ਹੋ(9432);
        try {
            통신.ਈਮੇਲ(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ਪਿਛਲਾ_ਕੀਮਤ));
            byte[] ਸਰੋਤ = 문자.부호화("회신"); 앞.send(new DatagramPacket(ਸਰੋਤ, ਸਰੋਤ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); ਪਿਛਲਾ_ਕੀਮਤ.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ਪਿਛਲਾ_ਕੀਮਤ.getLocalPort());
            ਪਿਛਲਾ_ਕੀਮਤ.setSoTimeout(10);
            try { ਪਿਛਲਾ_ਕੀਮਤ.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 시간 초과"); }
            ਪਿਛਲਾ_ਕੀਮਤ.close();
            try { ਪਿਛਲਾ_ਕੀਮਤ.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); ਪਿਛਲਾ_ਕੀਮਤ.close(); }
    }
}
