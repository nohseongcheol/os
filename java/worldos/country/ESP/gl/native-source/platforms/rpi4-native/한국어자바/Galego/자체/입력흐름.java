// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 입력(入力)과 fluxo_VALOR: 순서대로 들어오는 바이트를 읽는 Canle_introdución. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Lectura() throws E_S_excepción {
        try { return 표준흐름.read();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public int Lectura(byte[] datos) throws E_S_excepción {
        try { return 표준흐름.read(datos);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public int Lectura(byte[] datos, int Executar_2, int duración_VALOR) throws E_S_excepción {
        try { return 표준흐름.read(datos, Executar_2, duración_VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void Pechar() throws E_S_excepción {
        try { 표준흐름.close();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
}
