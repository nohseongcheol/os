// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 بهنګ_ارزښت: 순서대로 들어오는 바이트를 읽는 چینل_ننوت. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int لوستل() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public int لوستل(byte[] اومتوک) throws 입출력예외 {
        try { return 표준흐름.read(اومتوک);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public int لوستل(byte[] اومتوک, int ځغلول, int اوږدوالى_ارزښت) throws 입출력예외 {
        try { return 표준흐름.read(اومتوک, ځغلول, اوږدوالى_ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void بندول() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
}
