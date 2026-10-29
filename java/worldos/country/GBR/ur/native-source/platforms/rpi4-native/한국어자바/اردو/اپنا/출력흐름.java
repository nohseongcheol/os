// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** اخراج_کا_مقام(出力)과 بہاؤ_قدر: 순서를 보존해 내보내는 바이트의 چینل_اندراج. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void لکھیں(int قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준흐름.write(قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void لکھیں(byte[] کوائف) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준흐름.write(کوائف);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void لکھیں(byte[] کوائف, int چلائیں, int لمبا_ئی_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준흐름.write(کوائف, چلائیں, لمبا_ئی_قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void 내보내기() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준흐름.flush();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void بند_کریں() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준흐름.close();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
}
