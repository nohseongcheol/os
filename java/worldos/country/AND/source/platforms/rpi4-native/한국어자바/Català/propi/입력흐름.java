// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 입력(入力)과 flux_VALOR: 순서대로 들어오는 바이트를 읽는 Canal_introducció. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Lectura() throws E_S_excepció {
        try { return 표준흐름.read();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public int Lectura(byte[] dades) throws E_S_excepció {
        try { return 표준흐름.read(dades);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public int Lectura(byte[] dades, int Executa_2, int durada_VALOR) throws E_S_excepció {
        try { return 표준흐름.read(dades, Executa_2, durada_VALOR);
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
    public void Tanca() throws E_S_excepció {
        try { 표준흐름.close();
        } catch (java.io.IOException s_ha_produït_un_error) { throw CONVERT_excepció.E_S(s_ha_produït_un_error); }
        catch (RuntimeException s_ha_produït_un_error) { throw CONVERT_excepció.Executa_ordre(s_ha_produït_un_error); }
    }
}
