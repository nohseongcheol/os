// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 tok_VALUE: 순서를 보존해 내보내는 바이트의 Kanal_stavka. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void 쓰기(int VALUE) throws U_I_izuzetak {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void 쓰기(byte[] podaci) throws U_I_izuzetak {
        try { 표준흐름.write(podaci);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void 쓰기(byte[] podaci, int koristiti, int 길이) throws U_I_izuzetak {
        try { 표준흐름.write(podaci, koristiti, 길이);
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void 내보내기() throws U_I_izuzetak {
        try { 표준흐름.flush();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
    public void Zatvori() throws U_I_izuzetak {
        try { 표준흐름.close();
        } catch (java.io.IOException greška) { throw CONVERT_izuzetak.U_I(greška); }
        catch (RuntimeException greška) { throw CONVERT_izuzetak.Izvrši_komanda(greška); }
    }
}
