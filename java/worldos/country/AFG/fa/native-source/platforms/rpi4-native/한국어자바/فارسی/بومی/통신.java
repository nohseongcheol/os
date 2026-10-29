// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 رقم_مقدار 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket باز_کردن(int تبدیل_مقدار) throws ورودی_خروجی_استثنا {
        try { return new DatagramSocket(تبدیل_مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static void ارسال(DatagramSocket 종단, int تبدیل_مقدار, String محتوا_مقدار) throws ورودی_خروجی_استثنا {
        try {
        ارسال(종단, "127.0.0.1", تبدیل_مقدار, محتوا_مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static void ارسال(DatagramSocket 종단, String آدرس, int تبدیل_مقدار, String محتوا_مقدار) throws ورودی_خروجی_استثنا {
        try {
        byte[] بایت_مقدار = 문자.부호화(محتوا_مقدار);
        종단.send(new DatagramPacket(بایت_مقدار, بایت_مقدار.length, InetAddress.getByName(آدرس), تبدیل_مقدار));
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static String 받기(DatagramSocket 종단) throws ورودی_خروجی_استثنا {
        try {
        byte[] بایت_مقدار = new byte[512]; DatagramPacket 전문 = new DatagramPacket(بایت_مقدار, بایت_مقدار.length); 종단.receive(전문);
        byte[] سنجش = new byte[전문.getLength()]; System.arraycopy(بایت_مقدار, 0, سنجش, 0, سنجش.length); return 문자.رمزگشایی_داده_ها(سنجش);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static void پایان_مهلت_زمانی(DatagramSocket 종단, int 밀리초) throws ورودی_خروجی_استثنا {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static void بستن(DatagramSocket 종단) { 종단.close(); }
}
