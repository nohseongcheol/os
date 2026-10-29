// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket پرانيستل(int درشل_ارزښت) throws 입출력예외 {
        try { return new DatagramSocket(درشل_ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static void استول(DatagramSocket 종단, int درشل_ارزښت, String منځپانګه_ارزښت) throws 입출력예외 {
        try {
        استول(종단, "127.0.0.1", درشل_ارزښت, منځپانګه_ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static void استول(DatagramSocket 종단, String پته, int درشل_ارزښت, String منځپانګه_ارزښت) throws 입출력예외 {
        try {
        byte[] بايټ_ارزښت = 문자.부호화(منځپانګه_ارزښت);
        종단.send(new DatagramPacket(بايټ_ارزښت, بايټ_ارزښت.length, InetAddress.getByName(پته), درشل_ارزښت));
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] بايټ_ارزښت = new byte[512]; DatagramPacket 전문 = new DatagramPacket(بايټ_ارزښت, بايټ_ارزښت.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(بايټ_ارزښت, 0, 결과, 0, 결과.length); return 문자.کوډ_پرانېستل_اومتوک(결과);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public static void بندول(DatagramSocket 종단) { 종단.close(); }
}
