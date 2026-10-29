// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** خروجی(出力)과 جریان_مقدار: 순서를 보존해 내보내는 바이트의 کانال_ورودی. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void نوشتن(int مقدار) throws ورودی_خروجی_استثنا {
        try { 표준흐름.write(مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void نوشتن(byte[] داده_ها) throws ورودی_خروجی_استثنا {
        try { 표준흐름.write(داده_ها);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void نوشتن(byte[] داده_ها, int اجرا_2, int طول_مقدار) throws ورودی_خروجی_استثنا {
        try { 표준흐름.write(داده_ها, اجرا_2, طول_مقدار);
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void 내보내기() throws ورودی_خروجی_استثنا {
        try { 표준흐름.flush();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
    public void بستن() throws ورودی_خروجی_استثنا {
        try { 표준흐름.close();
        } catch (java.io.IOException خطا) { throw 예외변환.ورودی_خروجی(خطا); }
        catch (RuntimeException خطا) { throw 예외변환.اجرا_فرمان(خطا); }
    }
}
