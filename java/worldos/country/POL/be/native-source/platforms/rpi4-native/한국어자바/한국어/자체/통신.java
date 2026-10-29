// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 лічба_значэнне 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket Адкрыць(int порт_значэнне) throws увод_вывад_выключэнне {
        try { return new DatagramSocket(порт_значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static void адправіць(DatagramSocket 종단, int порт_значэнне, String кантэнт_значэнне) throws увод_вывад_выключэнне {
        try {
        адправіць(종단, "127.0.0.1", порт_значэнне, кантэнт_значэнне);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static void адправіць(DatagramSocket 종단, String адрас, int порт_значэнне, String кантэнт_значэнне) throws увод_вывад_выключэнне {
        try {
        byte[] байт_значэнне = 문자.부호화(кантэнт_значэнне);
        종단.send(new DatagramPacket(байт_значэнне, байт_значэнне.length, InetAddress.getByName(адрас), порт_значэнне));
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static String 받기(DatagramSocket 종단) throws увод_вывад_выключэнне {
        try {
        byte[] байт_значэнне = new byte[512]; DatagramPacket 전문 = new DatagramPacket(байт_значэнне, байт_значэнне.length); 종단.receive(전문);
        byte[] 결과 = new byte[전문.getLength()]; System.arraycopy(байт_значэнне, 0, 결과, 0, 결과.length); return 문자.расшыфраваць_дадзеныя(결과);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws увод_вывад_выключэнне {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static void Закрыць(DatagramSocket 종단) { 종단.close(); }
}
