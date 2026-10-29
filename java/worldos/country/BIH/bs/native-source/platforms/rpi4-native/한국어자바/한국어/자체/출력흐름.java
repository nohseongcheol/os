// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Ispis(出力)과 tok_VALUE: 순서를 보존해 내보내는 바이트의 kanal_unos. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Piši(int VALUE) throws U_I_izuzetak {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public void Piši(byte[] podaci) throws U_I_izuzetak {
        try { 표준흐름.write(podaci);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public void Piši(byte[] podaci, int Pokreni, int dužina_VALUE) throws U_I_izuzetak {
        try { 표준흐름.write(podaci, Pokreni, dužina_VALUE);
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public void 내보내기() throws U_I_izuzetak {
        try { 표준흐름.flush();
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
    public void Zatvori() throws U_I_izuzetak {
        try { 표준흐름.close();
        } catch (java.io.IOException GRESKA) { throw CONVERT_izuzetak.U_I(GRESKA); }
        catch (RuntimeException GRESKA) { throw CONVERT_izuzetak.Izvrši_komanda(GRESKA); }
    }
}
