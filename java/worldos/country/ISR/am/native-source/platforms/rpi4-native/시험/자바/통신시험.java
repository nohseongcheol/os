// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import አማርኛ.자체.문자;
import አማርኛ.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket ፊት_እሴት = 통신.መክፈቻ(9431), ተመለስ_እሴት = 통신.መክፈቻ(9432);
        try {
            통신.ላክ(ፊት_እሴት, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ተመለስ_እሴት));
            byte[] ምንጭ = 문자.부호화("회신"); ፊት_እሴት.send(new DatagramPacket(ምንጭ, ምንጭ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); ተመለስ_እሴት.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ተመለስ_እሴት.getLocalPort());
            ተመለስ_እሴት.setSoTimeout(10);
            try { ተመለስ_እሴት.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 ጊዜ_እሴት 초과"); }
            ተመለስ_እሴት.close();
            try { ተመለስ_እሴት.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { ፊት_እሴት.close(); ተመለስ_እሴት.close(); }
    }
}
