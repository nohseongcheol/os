// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 سٹریم_قدر: 순서를 보존해 내보내는 바이트의 چینل_داخلہ. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void لکھو(int قدر) throws 입출력예외 {
        try { 표준흐름.write(قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public void لکھو(byte[] کوائف) throws 입출력예외 {
        try { 표준흐름.write(کوائف);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public void لکھو(byte[] کوائف, int چلاؤ, int لمبائی_قدر) throws 입출력예외 {
        try { 표준흐름.write(کوائف, چلاؤ, لمبائی_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
    public void بند_کرو() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.نفاذ_کرو_حکم(نقص); }
    }
}
