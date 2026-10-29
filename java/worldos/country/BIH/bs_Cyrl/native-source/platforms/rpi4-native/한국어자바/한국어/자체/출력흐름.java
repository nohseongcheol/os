// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 ток_вриједност: 순서를 보존해 내보내는 바이트의 путања_унос. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void писати(int вриједност) throws 입출력예외 {
        try { 표준흐름.write(вриједност);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public void писати(byte[] подаци) throws 입출력예외 {
        try { 표준흐름.write(подаци);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public void писати(byte[] подаци, int 시작, int дужина_вриједност) throws 입출력예외 {
        try { 표준흐름.write(подаци, 시작, дужина_вриједност);
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
    public void затворити() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException грешка) { throw 예외변환.У_И(грешка); }
        catch (RuntimeException грешка) { throw 예외변환.실행(грешка); }
    }
}
