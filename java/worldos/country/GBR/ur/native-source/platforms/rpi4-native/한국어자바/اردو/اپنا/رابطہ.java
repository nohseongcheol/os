// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** متصل_ہوں(連結)·چینل_اندراج(通路): 상대와 이어진 TCP بائٹ_قدر 흐름의 종단. */
public final class رابطہ {
    private final java.net.Socket 표준연결;
    رابطہ(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static رابطہ کھولیں(String پتہ, int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try {
            return new رابطہ(new java.net.Socket(پتہ, دہانہ_نمبر));
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public 입력흐름 입력() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public 출력흐름 اخراج_کا_مقام() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public void ٹائم_آؤٹ(int 밀리초) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public int دہانہ_نمبر() { return 표준연결.getPort(); }
    public int مقامی_دہانہ_نمبر() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void بند_کریں() throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { 표준연결.close();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
}
