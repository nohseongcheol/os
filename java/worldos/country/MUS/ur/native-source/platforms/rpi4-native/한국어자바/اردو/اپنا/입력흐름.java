// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 입력(入力)과 بہاؤ_قدر: 순서대로 들어오는 바이트를 읽는 چینل_اندراج. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int پڑھیں() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return 표준흐름.read();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public int پڑھیں(byte[] کوائف) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return 표준흐름.read(کوائف);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public int پڑھیں(byte[] کوائف, int چلائیں, int لمبا_ئی_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return 표준흐름.read(کوائف, چلائیں, لمبا_ئی_قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void بند_کریں() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준흐름.close();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
}
