// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import čeština.vlastní.문자;
import čeština.vlastní.komunikace;
public class test_Sítě {
    public static void main(String[] args) throws Exception {
        DatagramSocket přední_fotoaparát_HODNOTA = komunikace.Otevřít(9431), BACK_HODNOTA = komunikace.Otevřít(9432);
        try {
            komunikace.poslat(přední_fotoaparát_HODNOTA, 9432, "자바 UDP 한글😀"); System.out.println(komunikace.dostat(BACK_HODNOTA));
            byte[] zdrojový_soubor = 문자.kódovat("회신"); přední_fotoaparát_HODNOTA.send(new DatagramPacket(zdrojový_soubor, zdrojový_soubor.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_HODNOTA = new byte[32]; DatagramPacket datagram = new DatagramPacket(RECEIVED_HODNOTA, RECEIVED_HODNOTA.length); BACK_HODNOTA.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_HODNOTA.getLocalPort());
            BACK_HODNOTA.setSoTimeout(10);
            try { BACK_HODNOTA.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("dostat_HODNOTA časová_hodnota 초과"); }
            BACK_HODNOTA.close();
            try { BACK_HODNOTA.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 komunikace"); }
        } finally { přední_fotoaparát_HODNOTA.close(); BACK_HODNOTA.close(); }
    }
}
