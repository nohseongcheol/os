// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 숫자 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket 열기(int outtülee_ajutuu) throws 입출력예외 {
        try { return new DatagramSocket(outtülee_ajutuu);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static void ajütaa(DatagramSocket 종단, int outtülee_ajutuu, String alu_ujatüü_ajutuu) throws 입출력예외 {
        try {
        ajütaa(종단, "127.0.0.1", outtülee_ajutuu, alu_ujatüü_ajutuu);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static void ajütaa(DatagramSocket 종단, String ejepüsee, int outtülee_ajutuu, String alu_ujatüü_ajutuu) throws 입출력예외 {
        try {
        byte[] waai_ajutuu = 문자.부호화(alu_ujatüü_ajutuu);
        종단.send(new DatagramPacket(waai_ajutuu, waai_ajutuu.length, InetAddress.getByName(ejepüsee), outtülee_ajutuu));
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] waai_ajutuu = new byte[512]; DatagramPacket 전문 = new DatagramPacket(waai_ajutuu, waai_ajutuu.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(waai_ajutuu, 0, 결과, 0, 결과.length); return 문자.ale_ejiraa_amoutuushi_atijaaya(결과);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ajachitia) { throw 예외변환.E_A(ajachitia); }
        catch (RuntimeException ajachitia) { throw 예외변환.실행(ajachitia); }
    }
    public static void asürülaa(DatagramSocket 종단) { 종단.close(); }
}
