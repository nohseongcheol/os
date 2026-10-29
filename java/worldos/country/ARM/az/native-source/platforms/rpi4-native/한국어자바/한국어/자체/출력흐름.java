// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 axın_VALUE: 순서를 보존해 내보내는 바이트의 kanal_daxiletmə. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Yazma(int VALUE) throws giriş_çıxış_istisna {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void Yazma(byte[] verilənlər) throws giriş_çıxış_istisna {
        try { 표준흐름.write(verilənlər);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void Yazma(byte[] verilənlər, int İcra_Et, int uzunluq_VALUE) throws giriş_çıxış_istisna {
        try { 표준흐름.write(verilənlər, İcra_Et, uzunluq_VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void 내보내기() throws giriş_çıxış_istisna {
        try { 표준흐름.flush();
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void Bağla() throws giriş_çıxış_istisna {
        try { 표준흐름.close();
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
}
