// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** 입력(入力)과 tok_VALUE: 순서대로 들어오는 바이트를 읽는 Kanal_vnos. */
public final class vhodni_tok {
    private final java.io.InputStream 표준흐름;
    vhodni_tok(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Branje() throws V_I_izjema {
        try { return 표준흐름.read();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public int Branje(byte[] podatki) throws V_I_izjema {
        try { return 표준흐름.read(podatki);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public int Branje(byte[] podatki, int Zaženi, int 길이) throws V_I_izjema {
        try { return 표준흐름.read(podatki, Zaženi, 길이);
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
    public void Zapri() throws V_I_izjema {
        try { 표준흐름.close();
        } catch (java.io.IOException NAPAKA) { throw CONVERT_izjema.V_I(NAPAKA); }
        catch (RuntimeException NAPAKA) { throw CONVERT_izjema.Izvedi_ukaz(NAPAKA); }
    }
}
