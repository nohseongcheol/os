// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** Izpis(出力)과 tok_VALUE: 순서를 보존해 내보내는 바이트의 Kanal_vnos. */
public final class izhodni_tok {
    private final java.io.OutputStream 표준흐름;
    izhodni_tok(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Pisanje(int VALUE) throws V_I_izjema {
        try { 표준흐름.write(VALUE);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void Pisanje(byte[] podatki) throws V_I_izjema {
        try { 표준흐름.write(podatki);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void Pisanje(byte[] podatki, int Zaženi, int 길이) throws V_I_izjema {
        try { 표준흐름.write(podatki, Zaženi, 길이);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void 내보내기() throws V_I_izjema {
        try { 표준흐름.flush();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void Zapri() throws V_I_izjema {
        try { 표준흐름.close();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
}
