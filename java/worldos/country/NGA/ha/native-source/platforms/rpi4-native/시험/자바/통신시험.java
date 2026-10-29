// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket kyamarar_gaba_Daraja = 통신.Buɗe(9431), Baya_Daraja = 통신.Buɗe(9432);
        try {
            통신.Aika(kyamarar_gaba_Daraja, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Baya_Daraja));
            byte[] tushe = 문자.부호화("회신"); kyamarar_gaba_Daraja.send(new DatagramPacket(tushe, tushe.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); Baya_Daraja.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Baya_Daraja.getLocalPort());
            Baya_Daraja.setSoTimeout(10);
            try { Baya_Daraja.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 lokaci_Daraja 초과"); }
            Baya_Daraja.close();
            try { Baya_Daraja.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { kyamarar_gaba_Daraja.close(); Baya_Daraja.close(); }
    }
}
