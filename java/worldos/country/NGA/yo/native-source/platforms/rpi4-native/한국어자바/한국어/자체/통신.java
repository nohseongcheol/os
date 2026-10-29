// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 díjììtì_iye 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Ṣi(int ojú_iye) throws 입출력예외 {
        try { return new DatagramSocket(ojú_iye);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static void í_meèlì(DatagramSocket 종단, int ojú_iye, String Àkóónú_iye) throws 입출력예외 {
        try {
        í_meèlì(종단, "127.0.0.1", ojú_iye, Àkóónú_iye);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static void í_meèlì(DatagramSocket 종단, String àdírẹ́ẹ̀sì, int ojú_iye, String Àkóónú_iye) throws 입출력예외 {
        try {
        byte[] báìtì_iye = 문자.부호화(Àkóónú_iye);
        종단.send(new DatagramPacket(báìtì_iye, báìtì_iye.length, InetAddress.getByName(àdírẹ́ẹ̀sì), ojú_iye));
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] báìtì_iye = new byte[512]; DatagramPacket 전문 = new DatagramPacket(báìtì_iye, báìtì_iye.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(báìtì_iye, 0, 결과, 0, 결과.length); return 문자.ṣàtúpalẹ̀_àrokò_détà(결과);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException àṣìṣe) { throw 예외변환.I_O(àṣìṣe); }
        catch (RuntimeException àṣìṣe) { throw 예외변환.ṣiṣẹ́_àṣẹ(àṣìṣe); }
    }
    public static void Ti(DatagramSocket 종단) { 종단.close(); }
}
