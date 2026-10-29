// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** 수신(受信)·تبدیل_مقدار(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try { 표준창구 = new java.net.ServerSocket(شماره_درگاه);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static 수신창구 باز_کردن(int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try { return new 수신창구(شماره_درگاه);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public اتصال_d584d28a 받기() throws ورودی_خروجی_استثنا {
        try { return new اتصال_d584d28a(표준창구.accept());
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public int شماره_درگاه() { return 표준창구.getLocalPort(); }
    public void پایان_مهلت_زمانی(int 밀리초) throws ورودی_خروجی_استثنا {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void بستن() throws ورودی_خروجی_استثنا {
        try { 표준창구.close();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
}
