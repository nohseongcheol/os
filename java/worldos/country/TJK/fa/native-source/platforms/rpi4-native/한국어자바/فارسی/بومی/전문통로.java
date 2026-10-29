// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** 전문(電文)·کانال_ورودی(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try { 표준종단 = 통신.باز_کردن(شماره_درگاه);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public static 전문통로 باز_کردن(int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try { return new 전문통로(شماره_درگاه);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void ارسال(String آدرس, int شماره_درگاه, String داده_ها) throws ورودی_خروجی_استثنا {
        try { 통신.ارسال(표준종단, آدرس, شماره_درگاه, داده_ها);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public String 받기() throws ورودی_خروجی_استثنا {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void پایان_مهلت_زمانی(int 밀리초) throws ورودی_خروجی_استثنا {
        try { 통신.پایان_مهلت_زمانی(표준종단, 밀리초);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public int شماره_درگاه() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void بستن() { 통신.بستن(표준종단); }
}
