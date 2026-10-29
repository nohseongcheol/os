// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** Irteera(出力)과 Stream_balio: 순서를 보존해 내보내는 바이트의 kanal_sarrera. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Idatzi(int balio) throws S_I_salbuespen {
        try { 표준흐름.write(balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void Idatzi(byte[] datuak) throws S_I_salbuespen {
        try { 표준흐름.write(datuak);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void Idatzi(byte[] datuak, int Exekutatu_2, int luzera_balio) throws S_I_salbuespen {
        try { 표준흐름.write(datuak, Exekutatu_2, luzera_balio);
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void 내보내기() throws S_I_salbuespen {
        try { 표준흐름.flush();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
    public void Itxi() throws S_I_salbuespen {
        try { 표준흐름.close();
        } catch (java.io.IOException errorea) { throw BIHURTU_salbuespen.S_I(errorea); }
        catch (RuntimeException errorea) { throw BIHURTU_salbuespen.exekutatu_komando(errorea); }
    }
}
