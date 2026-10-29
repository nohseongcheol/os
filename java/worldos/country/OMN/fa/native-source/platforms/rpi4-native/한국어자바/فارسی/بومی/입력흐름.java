// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** 입력(入力)과 جریان_مقدار: 순서대로 들어오는 바이트를 읽는 کانال_ورودی. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int خواندن() throws ورودی_خروجی_استثنا {
        try { return 표준흐름.read();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public int خواندن(byte[] داده_ها) throws ورودی_خروجی_استثنا {
        try { return 표준흐름.read(داده_ها);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public int خواندن(byte[] داده_ها, int اجرا_2, int طول_مقدار) throws ورودی_خروجی_استثنا {
        try { return 표준흐름.read(داده_ها, اجرا_2, طول_مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void بستن() throws ورودی_خروجی_استثنا {
        try { 표준흐름.close();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
}
