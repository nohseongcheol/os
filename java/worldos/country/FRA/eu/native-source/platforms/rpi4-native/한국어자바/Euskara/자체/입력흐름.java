// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 입력(入力)과 Stream_balio: 순서대로 들어오는 바이트를 읽는 kanal_sarrera. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Irakurri() throws S_I_salbuespen {
        try { return 표준흐름.read();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public int Irakurri(byte[] datuak) throws S_I_salbuespen {
        try { return 표준흐름.read(datuak);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public int Irakurri(byte[] datuak, int Exekutatu_2, int luzera_balio) throws S_I_salbuespen {
        try { return 표준흐름.read(datuak, Exekutatu_2, luzera_balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void Itxi() throws S_I_salbuespen {
        try { 표준흐름.close();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
}
