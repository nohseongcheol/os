// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ციფრი_მნიშვნელობა 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket გახსნა(int პორტი_მნიშვნელობა) throws 입출력예외 {
        try { return new DatagramSocket(პორტი_მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static void გაგზავნა(DatagramSocket 종단, int პორტი_მნიშვნელობა, String შიგთავსი_მნიშვნელობა) throws 입출력예외 {
        try {
        გაგზავნა(종단, "127.0.0.1", პორტი_მნიშვნელობა, შიგთავსი_მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static void გაგზავნა(DatagramSocket 종단, String მისამართი, int პორტი_მნიშვნელობა, String შიგთავსი_მნიშვნელობა) throws 입출력예외 {
        try {
        byte[] ბაიტი_მნიშვნელობა = 문자.부호화(შიგთავსი_მნიშვნელობა);
        종단.send(new DatagramPacket(ბაიტი_მნიშვნელობა, ბაიტი_მნიშვნელობა.length, InetAddress.getByName(მისამართი), პორტი_მნიშვნელობა));
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] ბაიტი_მნიშვნელობა = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ბაიტი_მნიშვნელობა, ბაიტი_მნიშვნელობა.length); 종단.receive(전문);
        byte[] გაზომვა = new byte[전문.getLength()]; System.arraycopy(ბაიტი_მნიშვნელობა, 0, გაზომვა, 0, გაზომვა.length); return 문자.გაშიფვრა_მონაცემები(გაზომვა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static void დრო_ამოიწურა(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public static void დახურვა(DatagramSocket 종단) { 종단.close(); }
}
