// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** اتصال(連結)·کانال_ورودی(通路): 상대와 이어진 TCP بایت_مقدار 흐름의 종단. */
public final class اتصال_d584d28a {
    private final java.net.Socket 표준연결;
    اتصال_d584d28a(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static اتصال_d584d28a باز_کردن(String آدرس, int شماره_درگاه) throws ورودی_خروجی_استثنا {
        try {
            return new اتصال_d584d28a(new java.net.Socket(آدرس, شماره_درگاه));
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public 입력흐름 입력() throws ورودی_خروجی_استثنا {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public 출력흐름 خروجی() throws ورودی_خروجی_استثنا {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void پایان_مهلت_زمانی(int 밀리초) throws ورودی_خروجی_استثنا {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public int شماره_درگاه() { return 표준연결.getPort(); }
    public int محلی_شماره_درگاه() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void بستن() throws ورودی_خروجی_استثنا {
        try { 표준연결.close();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
}
