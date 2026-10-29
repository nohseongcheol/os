// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ਅੰਕ_ਕੀਮਤ 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ਖੋਲ੍ਹੋ(int ਪੋਰਟ_ਕੀਮਤ) throws 입출력예외 {
        try { return new DatagramSocket(ਪੋਰਟ_ਕੀਮਤ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static void ਈਮੇਲ(DatagramSocket 종단, int ਪੋਰਟ_ਕੀਮਤ, String ਤਤਕਰਾ_ਕੀਮਤ) throws 입출력예외 {
        try {
        ਈਮੇਲ(종단, "127.0.0.1", ਪੋਰਟ_ਕੀਮਤ, ਤਤਕਰਾ_ਕੀਮਤ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static void ਈਮੇਲ(DatagramSocket 종단, String ਪਤਾ, int ਪੋਰਟ_ਕੀਮਤ, String ਤਤਕਰਾ_ਕੀਮਤ) throws 입출력예외 {
        try {
        byte[] ਬਾਈਟ_ਕੀਮਤ = 문자.부호화(ਤਤਕਰਾ_ਕੀਮਤ);
        종단.send(new DatagramPacket(ਬਾਈਟ_ਕੀਮਤ, ਬਾਈਟ_ਕੀਮਤ.length, InetAddress.getByName(ਪਤਾ), ਪੋਰਟ_ਕੀਮਤ));
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] ਬਾਈਟ_ਕੀਮਤ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ਬਾਈਟ_ਕੀਮਤ, ਬਾਈਟ_ਕੀਮਤ.length); 종단.receive(전문);
        byte[] ਮਾਪ = new byte[전문.getLength()]; System.arraycopy(ਬਾਈਟ_ਕੀਮਤ, 0, ਮਾਪ, 0, ਮਾਪ.length); return 문자.ਬਦਲਾਵ_ਕਰੋ_ਸਮੱਗਰੀ(ਮਾਪ);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static void ਸਮਾਂ_ਸਮਾਪਤ(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ਗਲਤੀ) { throw 예외변환.ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ(ਗਲਤੀ); }
        catch (RuntimeException ਗਲਤੀ) { throw 예외변환.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਗਲਤੀ); }
    }
    public static void ਬੰਦ_ਕਰੋ(DatagramSocket 종단) { 종단.close(); }
}
