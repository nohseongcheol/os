// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import polski.własny.문자;
import polski.własny.komunikacja;
public class test_Sieć {
    public static void main(String[] args) throws Exception {
        DatagramSocket przód_WARTOŚĆ = komunikacja.Otwórz(9431), BACK_WARTOŚĆ = komunikacja.Otwórz(9432);
        try {
            komunikacja.wysłać(przód_WARTOŚĆ, 9432, "자바 UDP 한글😀"); System.out.println(komunikacja.odbierać(BACK_WARTOŚĆ));
            byte[] plik_źródłowy = 문자.kodować("회신"); przód_WARTOŚĆ.send(new DatagramPacket(plik_źródłowy, plik_źródłowy.length, InetAddress.getByName("localhost"), 9432));
            byte[] KWOTA_WYKUP_WARTOŚĆ = new byte[32]; DatagramPacket datagram = new DatagramPacket(KWOTA_WYKUP_WARTOŚĆ, KWOTA_WYKUP_WARTOŚĆ.length); BACK_WARTOŚĆ.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_WARTOŚĆ.getLocalPort());
            BACK_WARTOŚĆ.setSoTimeout(10);
            try { BACK_WARTOŚĆ.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("odbierać_WARTOŚĆ wartość_czasu 초과"); }
            BACK_WARTOŚĆ.close();
            try { BACK_WARTOŚĆ.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 komunikacja"); }
        } finally { przód_WARTOŚĆ.close(); BACK_WARTOŚĆ.close(); }
    }
}
