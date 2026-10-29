// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 সংখ্যা_মান 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket খুলুন(int পোর্ট_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new DatagramSocket(পোর্ট_মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static void পাঠান(DatagramSocket 종단, int পোর্ট_মান, String সামগ্রি_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try {
        পাঠান(종단, "127.0.0.1", পোর্ট_মান, সামগ্রি_মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static void পাঠান(DatagramSocket 종단, String ইমেইল, int পোর্ট_মান, String সামগ্রি_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try {
        byte[] বাইট_মান = 문자.부호화(সামগ্রি_মান);
        종단.send(new DatagramPacket(বাইট_মান, বাইট_মান.length, InetAddress.getByName(ইমেইল), পোর্ট_মান));
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static String 받기(DatagramSocket 종단) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try {
        byte[] বাইট_মান = new byte[512]; DatagramPacket 전문 = new DatagramPacket(বাইট_মান, বাইট_মান.length); 종단.receive(전문);
        byte[] পরিমাপ = new byte[전문.getLength()]; System.arraycopy(বাইট_মান, 0, পরিমাপ, 0, পরিমাপ.length); return 문자.ডিক্রিপ্ট_ডাটা(পরিমাপ);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static void টাইমআউট(DatagramSocket 종단, int 밀리초) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static void বন্ধ_করুন(DatagramSocket 종단) { 종단.close(); }
}
