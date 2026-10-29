// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** Sortida(出力)과 flux_VALOR: 순서를 보존해 내보내는 바이트의 Canal_introducció. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Escriptura(int VALOR) throws E_S_excepció {
        try { 표준흐름.write(VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void Escriptura(byte[] dades) throws E_S_excepció {
        try { 표준흐름.write(dades);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void Escriptura(byte[] dades, int Executa_2, int durada_VALOR) throws E_S_excepció {
        try { 표준흐름.write(dades, Executa_2, durada_VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void 내보내기() throws E_S_excepció {
        try { 표준흐름.flush();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void Tanca() throws E_S_excepció {
        try { 표준흐름.close();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
}
