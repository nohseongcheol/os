// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 dijiti_thamani 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket unda(int kituo_thamani) throws I_T_vighairi {
        try { return new DatagramSocket(kituo_thamani);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static void tuma(DatagramSocket 종단, int kituo_thamani, String maudhui_thamani) throws I_T_vighairi {
        try {
        tuma(종단, "127.0.0.1", kituo_thamani, maudhui_thamani);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static void tuma(DatagramSocket 종단, String anwani, int kituo_thamani, String maudhui_thamani) throws I_T_vighairi {
        try {
        byte[] baiti_thamani = 문자.부호화(maudhui_thamani);
        종단.send(new DatagramPacket(baiti_thamani, baiti_thamani.length, InetAddress.getByName(anwani), kituo_thamani));
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static String 받기(DatagramSocket 종단) throws I_T_vighairi {
        try {
        byte[] baiti_thamani = new byte[512]; DatagramPacket 전문 = new DatagramPacket(baiti_thamani, baiti_thamani.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(baiti_thamani, 0, 결과, 0, 결과.length); return 문자.simbua_fiche_data(결과);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws I_T_vighairi {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException kosa) { throw 예외변환.I_T(kosa); }
        catch (RuntimeException kosa) { throw 예외변환.tekeleza_amri(kosa); }
    }
    public static void funga(DatagramSocket 종단) { 종단.close(); }
}
