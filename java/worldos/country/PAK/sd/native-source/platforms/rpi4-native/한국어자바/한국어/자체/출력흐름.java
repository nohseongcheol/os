// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 اسٽريم_قدر: 순서를 보존해 내보내는 바이트의 چينل_داخلا. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void لکو(int قدر) throws 입출력예외 {
        try { 표준흐름.write(قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public void لکو(byte[] ڪوائف) throws 입출력예외 {
        try { 표준흐름.write(ڪوائف);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public void لکو(byte[] ڪوائف, int هلائڻ, int لمبائي_قدر) throws 입출력예외 {
        try { 표준흐름.write(ڪوائف, هلائڻ, لمبائي_قدر);
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
    public void بند_ڪرڻ() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException نقص) { throw 예외변환.입출력(نقص); }
        catch (RuntimeException نقص) { throw 예외변환.تعميل_ڪرڻ_حڪم(نقص); }
    }
}
