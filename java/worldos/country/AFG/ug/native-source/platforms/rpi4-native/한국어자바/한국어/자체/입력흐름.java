// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ئېقىم_قىممىتى: 순서대로 들어오는 바이트를 읽는 قانال_كىرگۈزۈش. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int ئوقۇ() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public int ئوقۇ(byte[] مەلۇمات) throws 입출력예외 {
        try { return 표준흐름.read(مەلۇمات);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public int ئوقۇ(byte[] مەلۇمات, int ئىجرا_قىل_2, int ئۇزۇنلۇق_قىممىتى) throws 입출력예외 {
        try { return 표준흐름.read(مەلۇمات, ئىجرا_قىل_2, ئۇزۇنلۇق_قىممىتى);
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
    public void ياپ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException خاتالىق) { throw 예외변환.입출력(خاتالىق); }
        catch (RuntimeException خاتالىق) { throw 예외변환.ئىجرا_قىلىش_بۇيرۇق(خاتالىق); }
    }
}
