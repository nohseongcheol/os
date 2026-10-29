// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static اتصال_d584d28a باز_کردن(String آدرس, int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try { return اتصال_d584d28a.باز_کردن(آدرس, شماره_درگاه);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static 수신창구 수신열기(int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try { return 수신창구.باز_کردن(شماره_درگاه);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static Socket اتصال(String آدرس, int تبدیل_مقدار) throws ورودی_خروجی_استثنا {
        try { return new Socket(آدرس, تبدیل_مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static ServerSocket 듣기(int تبدیل_مقدار) throws ورودی_خروجی_استثنا {
        try { return new ServerSocket(تبدیل_مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static Socket 받기(ServerSocket سرور_مقدار) throws ورودی_خروجی_استثنا {
        try { return سرور_مقدار.accept();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
}
