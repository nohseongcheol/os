// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 Stream_نرخ: 순서를 보존해 내보내는 바이트의 کاناڵ_تێنووسین. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ڕایت_کردن(int نرخ) throws 입출력예외 {
        try { 표준흐름.write(نرخ);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public void ڕایت_کردن(byte[] دەیتا) throws 입출력예외 {
        try { 표준흐름.write(دەیتا);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public void ڕایت_کردن(byte[] دەیتا, int ڕادان, int درێژی_نرخ) throws 입출력예외 {
        try { 표준흐름.write(دەیتا, ڕادان, درێژی_نرخ);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public void داخستن() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
}
