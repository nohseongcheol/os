// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 بهنګ_ارزښت: 순서를 보존해 내보내는 바이트의 چینل_ننوت. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void لوستل_2(int ارزښت) throws 입출력예외 {
        try { 표준흐름.write(ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void لوستل_2(byte[] اومتوک) throws 입출력예외 {
        try { 표준흐름.write(اومتوک);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void لوستل_2(byte[] اومتوک, int ځغلول, int اوږدوالى_ارزښت) throws 입출력예외 {
        try { 표준흐름.write(اومتوک, ځغلول, اوږدوالى_ارزښت);
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
    public void بندول() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException تېروتنه) { throw 예외변환.ننوتنی_وتنی(تېروتنه); }
        catch (RuntimeException تېروتنه) { throw 예외변환.실행(تېروتنه); }
    }
}
