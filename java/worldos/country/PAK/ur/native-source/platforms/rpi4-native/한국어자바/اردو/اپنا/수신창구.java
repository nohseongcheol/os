// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 수신(受信)·پورٹ_قدر(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준창구 = new java.net.ServerSocket(دہانہ_نمبر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static 수신창구 کھولیں(int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new 수신창구(دہانہ_نمبر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public رابطہ 받기() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new رابطہ(표준창구.accept());
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public int دہانہ_نمبر() { return 표준창구.getLocalPort(); }
    public void ٹائم_آؤٹ(int 밀리초) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void بند_کریں() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준창구.close();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
}
