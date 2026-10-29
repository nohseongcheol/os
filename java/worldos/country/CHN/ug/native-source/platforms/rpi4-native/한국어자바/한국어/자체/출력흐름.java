// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** چىقار(出力)과 ئېقىم_قىممىتى: 순서를 보존해 내보내는 바이트의 قانال_كىرگۈزۈش. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ياز(int قىممىتى) throws 입출력예외 {
        try { 표준흐름.write(قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void ياز(byte[] مەلۇمات) throws 입출력예외 {
        try { 표준흐름.write(مەلۇمات);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void ياز(byte[] مەلۇمات, int ئىجرا_قىل_2, int ئۇزۇنلۇق_قىممىتى) throws 입출력예외 {
        try { 표준흐름.write(مەلۇمات, ئىجرا_قىل_2, ئۇزۇنلۇق_قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void ياپ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
}
