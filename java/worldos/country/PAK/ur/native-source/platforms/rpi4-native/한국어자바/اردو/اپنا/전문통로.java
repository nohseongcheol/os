// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 전문(電文)·چینل_اندراج(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준종단 = 통신.کھولیں(دہانہ_نمبر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static 전문통로 کھولیں(int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new 전문통로(دہانہ_نمبر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void بھیجیں(String پتہ, int دہانہ_نمبر, String کوائف) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 통신.بھیجیں(표준종단, پتہ, دہانہ_نمبر, کوائف);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public String 받기() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void ٹائم_آؤٹ(int 밀리초) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 통신.ٹائم_آؤٹ(표준종단, 밀리초);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public int دہانہ_نمبر() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void بند_کریں() { 통신.بند_کریں(표준종단); }
}
