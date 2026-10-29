// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 සංඛ්_යාංකය_අගය 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket විවෘත_කරන්න(int තොට_අගය) throws 입출력예외 {
        try { return new DatagramSocket(තොට_අගය);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static void ඊමේල්(DatagramSocket 종단, int තොට_අගය, String අන්තර්ගතය_අගය) throws 입출력예외 {
        try {
        ඊමේල්(종단, "127.0.0.1", තොට_අගය, අන්තර්ගතය_අගය);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static void ඊමේල්(DatagramSocket 종단, String යොමුව, int තොට_අගය, String අන්තර්ගතය_අගය) throws 입출력예외 {
        try {
        byte[] බයිටය_අගය = 문자.부호화(අන්තර්ගතය_අගය);
        종단.send(new DatagramPacket(බයිටය_අගය, බයිටය_අගය.length, InetAddress.getByName(යොමුව), තොට_අගය));
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] බයිටය_අගය = new byte[512]; DatagramPacket 전문 = new DatagramPacket(බයිටය_අගය, බයිටය_අගය.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(බයිටය_අගය, 0, 결과, 0, 결과.length); return 문자.විගුප්ත_කේතනය_කරන්න_දත්ත(결과);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static void වසන්න(DatagramSocket 종단) { 종단.close(); }
}
