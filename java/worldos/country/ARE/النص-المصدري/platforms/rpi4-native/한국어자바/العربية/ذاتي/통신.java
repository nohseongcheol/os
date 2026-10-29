// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP رزمةمستقلة. خارجي_قيمة 주소는 رقم_قيمة 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket فتح(int منفذ_قيمة) throws إدخال_إخراج_استثناء {
        try { return new DatagramSocket(منفذ_قيمة);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static void يرسل(DatagramSocket المشارك, int منفذ_قيمة, String محتوى_قيمة) throws إدخال_إخراج_استثناء {
        try {
        يرسل(المشارك, "127.0.0.1", منفذ_قيمة, محتوى_قيمة);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static void يرسل(DatagramSocket المشارك, String عنوان, int منفذ_قيمة, String محتوى_قيمة) throws إدخال_إخراج_استثناء {
        try {
        byte[] بايت_قيمة = 문자.يرمّز(محتوى_قيمة);
        المشارك.send(new DatagramPacket(بايت_قيمة, بايت_قيمة.length, InetAddress.getByName(عنوان), منفذ_قيمة));
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static String يستلم(DatagramSocket المشارك) throws إدخال_إخراج_استثناء {
        try {
        byte[] بايت_قيمة = new byte[512]; DatagramPacket رزمةمستقلة = new DatagramPacket(بايت_قيمة, بايت_قيمة.length); المشارك.receive(رزمةمستقلة);
        byte[] نتيجة = new byte[رزمةمستقلة.getLength()]; System.arraycopy(بايت_قيمة, 0, نتيجة, 0, نتيجة.length); return 문자.يفك_التشفير_بيانات(نتيجة);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static void 대기시간(DatagramSocket المشارك, int 밀리초) throws إدخال_إخراج_استثناء {
        try { المشارك.setSoTimeout(밀리초);
        } catch (java.io.IOException خطأ) { throw تحويل_استثناء.إدخال_إخراج(خطأ); }
        catch (RuntimeException خطأ) { throw تحويل_استثناء.ينفذ_أمر(خطأ); }
    }
    public static void إغلاق(DatagramSocket المشارك) { المشارك.close(); }
}
