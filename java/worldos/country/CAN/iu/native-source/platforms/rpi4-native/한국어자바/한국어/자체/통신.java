// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket matuirli(int kapputigaq_atuutilik) throws 입출력예외 {
        try { return new DatagramSocket(kapputigaq_atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static void nassiutili(DatagramSocket 종단, int kapputigaq_atuutilik, String Ilulingit_atuutilik) throws 입출력예외 {
        try {
        nassiutili(종단, "127.0.0.1", kapputigaq_atuutilik, Ilulingit_atuutilik);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static void nassiutili(DatagramSocket 종단, String turaarut, int kapputigaq_atuutilik, String Ilulingit_atuutilik) throws 입출력예외 {
        try {
        byte[] byte_atuutilik = 문자.부호화(Ilulingit_atuutilik);
        종단.send(new DatagramPacket(byte_atuutilik, byte_atuutilik.length, InetAddress.getByName(turaarut), kapputigaq_atuutilik));
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] byte_atuutilik = new byte[512]; DatagramPacket 전문 = new DatagramPacket(byte_atuutilik, byte_atuutilik.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(byte_atuutilik, 0, 결과, 0, 결과.length); return 문자.suqquinarunniirlit_titiqqat(결과);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException tammarniq) { throw 예외변환.I_O(tammarniq); }
        catch (RuntimeException tammarniq) { throw 예외변환.실행(tammarniq); }
    }
    public static void matuli(DatagramSocket 종단) { 종단.close(); }
}
