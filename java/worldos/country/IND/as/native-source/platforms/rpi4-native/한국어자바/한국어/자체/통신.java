// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 অংক_মান 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket খোলো(int পৰ্ট_মান) throws 입출력예외 {
        try { return new DatagramSocket(পৰ্ট_মান);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static void ই_মেইল_কৰক(DatagramSocket 종단, int পৰ্ট_মান, String সামগ্ৰী_মান) throws 입출력예외 {
        try {
        ই_মেইল_কৰক(종단, "127.0.0.1", পৰ্ট_মান, সামগ্ৰী_মান);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static void ই_মেইল_কৰক(DatagramSocket 종단, String ঠিকনা, int পৰ্ট_মান, String সামগ্ৰী_মান) throws 입출력예외 {
        try {
        byte[] বাইট_মান = 문자.부호화(সামগ্ৰী_মান);
        종단.send(new DatagramPacket(বাইট_মান, বাইট_মান.length, InetAddress.getByName(ঠিকনা), পৰ্ট_মান));
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static String 받기(DatagramSocket 종단) throws 입출력예외 {
        try {
        byte[] বাইট_মান = new byte[512]; DatagramPacket 전문 = new DatagramPacket(বাইট_মান, বাইট_মান.length); 종단.receive(전문);
        byte[] পৰিমাপ = new byte[전문.getLength()]; System.arraycopy(বাইট_মান, 0, পৰিমাপ, 0, পৰিমাপ.length); return 문자.ডিক্ৰিপ্ট_কৰক_ডাটা(পৰিমাপ);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws 입출력예외 {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static void বন্ধ_কৰক(DatagramSocket 종단) { 종단.close(); }
}
