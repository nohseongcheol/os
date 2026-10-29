// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 இலக்கம்_மதிப்பு 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket திற(int முணையம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { return new DatagramSocket(முணையம்_மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static void அனுப்பு(DatagramSocket முடிவுப்_புள்ளி, int முணையம்_மதிப்பு, String உள்ளடக்கம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try {
        அனுப்பு(முடிவுப்_புள்ளி, "127.0.0.1", முணையம்_மதிப்பு, உள்ளடக்கம்_மதிப்பு);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static void அனுப்பு(DatagramSocket முடிவுப்_புள்ளி, String முகவரி, int முணையம்_மதிப்பு, String உள்ளடக்கம்_மதிப்பு) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try {
        byte[] பைட்_மதிப்பு = 문자.부호화(உள்ளடக்கம்_மதிப்பு);
        முடிவுப்_புள்ளி.send(new DatagramPacket(பைட்_மதிப்பு, பைட்_மதிப்பு.length, InetAddress.getByName(முகவரி), முணையம்_மதிப்பு));
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static String 받기(DatagramSocket முடிவுப்_புள்ளி) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try {
        byte[] பைட்_மதிப்பு = new byte[512]; DatagramPacket 전문 = new DatagramPacket(பைட்_மதிப்பு, பைட்_மதிப்பு.length); முடிவுப்_புள்ளி.receive(전문);
        byte[] அளவிடக்கூடியது = new byte[전문.getLength()]; System.arraycopy(பைட்_மதிப்பு, 0, அளவிடக்கூடியது, 0, அளவிடக்கூடியது.length); return 문자.குறிநீக்கு_தரவு(அளவிடக்கூடியது);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static void 대기시간(DatagramSocket முடிவுப்_புள்ளி, int 밀리초) throws உள்ளீடு_வெளியீடு_விதிவிலக்கு {
        try { முடிவுப்_புள்ளி.setSoTimeout(밀리초);
        } catch (java.io.IOException பிழை) { throw 예외변환.உள்ளீடு_வெளியீடு(பிழை); }
        catch (RuntimeException பிழை) { throw 예외변환.இயக்கு_கட்டளை(பிழை); }
    }
    public static void மூடு(DatagramSocket முடிவுப்_புள்ளி) { முடிவுப்_புள்ளி.close(); }
}
