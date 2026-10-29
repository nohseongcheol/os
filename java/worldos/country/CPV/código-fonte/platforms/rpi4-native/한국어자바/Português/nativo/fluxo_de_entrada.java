// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** entrada_VALOR(入力)과 fluxo_VALOR: 순서대로 들어오는 바이트를 읽는 Canal_entrada. */
public final class fluxo_de_entrada {
    private final java.io.InputStream padrão_fluxo;
    fluxo_de_entrada(java.io.InputStream padrão_fluxo) { this.padrão_fluxo = padrão_fluxo; }
    public int Leitura() throws E_S_exceção {
        try { return padrão_fluxo.read();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public int Leitura(byte[] dados) throws E_S_exceção {
        try { return padrão_fluxo.read(dados);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public int Leitura(byte[] dados, int iniciar, int duração_VALOR) throws E_S_exceção {
        try { return padrão_fluxo.read(dados, iniciar, duração_VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void Fechar() throws E_S_exceção {
        try { padrão_fluxo.close();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
}
