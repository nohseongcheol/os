// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static رابطہ کھولیں(String پتہ, int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return رابطہ.کھولیں(پتہ, دہانہ_نمبر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static 수신창구 수신열기(int دہانہ_نمبر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return 수신창구.کھولیں(دہانہ_نمبر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static Socket متصل_ہوں(String پتہ, int پورٹ_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new Socket(پتہ, پورٹ_قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static ServerSocket 듣기(int پورٹ_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return new ServerSocket(پورٹ_قدر);
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
    public static Socket 받기(ServerSocket سرور_قدر) throws ان_پٹ_آؤٹ_پٹ_استثنا {
        try { return سرور_قدر.accept();
        } catch (java.io.IOException غلطی) { throw 예외변환.ان_پٹ_آؤٹ_پٹ(غلطی); }
        catch (RuntimeException غلطی) { throw 예외변환.نفاذ_کریں_حکم(غلطی); }
    }
}
