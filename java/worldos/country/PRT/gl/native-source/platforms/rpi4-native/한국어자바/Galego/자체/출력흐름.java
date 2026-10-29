// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** Saída(出力)과 fluxo_VALOR: 순서를 보존해 내보내는 바이트의 Canle_introdución. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Escritura(int VALOR) throws E_S_excepción {
        try { 표준흐름.write(VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void Escritura(byte[] datos) throws E_S_excepción {
        try { 표준흐름.write(datos);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void Escritura(byte[] datos, int Executar_2, int duración_VALOR) throws E_S_excepción {
        try { 표준흐름.write(datos, Executar_2, duración_VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void 내보내기() throws E_S_excepción {
        try { 표준흐름.flush();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public void Pechar() throws E_S_excepción {
        try { 표준흐름.close();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
}
