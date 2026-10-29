// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 axın_VALUE: 순서대로 들어오는 바이트를 읽는 kanal_daxiletmə. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Oxuma() throws giriş_çıxış_istisna {
        try { return 표준흐름.read();
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public int Oxuma(byte[] verilənlər) throws giriş_çıxış_istisna {
        try { return 표준흐름.read(verilənlər);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public int Oxuma(byte[] verilənlər, int İcra_Et, int uzunluq_VALUE) throws giriş_çıxış_istisna {
        try { return 표준흐름.read(verilənlər, İcra_Et, uzunluq_VALUE);
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
    public void Bağla() throws giriş_çıxış_istisna {
        try { 표준흐름.close();
        } catch (java.io.IOException XƏTA) { throw CONVERT_istisna.giriş_çıxış(XƏTA); }
        catch (RuntimeException XƏTA) { throw CONVERT_istisna.icra_etmək_əmr(XƏTA); }
    }
}
