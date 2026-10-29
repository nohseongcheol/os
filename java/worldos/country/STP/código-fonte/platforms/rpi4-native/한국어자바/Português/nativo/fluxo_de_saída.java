// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** saídaTexto(出力)과 fluxo_VALOR: 순서를 보존해 내보내는 바이트의 Canal_entrada. */
public final class fluxo_de_saída {
    private final java.io.OutputStream padrão_fluxo;
    fluxo_de_saída(java.io.OutputStream padrão_fluxo) { this.padrão_fluxo = padrão_fluxo; }
    public void Escrita(int VALOR) throws E_S_exceção {
        try { padrão_fluxo.write(VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void Escrita(byte[] dados) throws E_S_exceção {
        try { padrão_fluxo.write(dados);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void Escrita(byte[] dados, int iniciar, int duração_VALOR) throws E_S_exceção {
        try { padrão_fluxo.write(dados, iniciar, duração_VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void 내보내기() throws E_S_exceção {
        try { padrão_fluxo.flush();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void Fechar() throws E_S_exceção {
        try { padrão_fluxo.close();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
}
