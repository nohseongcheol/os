// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** Ligar(連結)·Canal_entrada(通路): 상대와 이어진 TCP byte_VALOR 흐름의 empresa. */
public final class conexão {
    private final java.net.Socket padrão_biblioteca_ponte;
    conexão(java.net.Socket padrão_biblioteca_ponte) { this.padrão_biblioteca_ponte = padrão_biblioteca_ponte; }
    public static conexão Abrir(String Endereço, int número_da_porta) throws E_S_exceção {
        try {
            return new conexão(new java.net.Socket(Endereço, número_da_porta));
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public fluxo_de_entrada entrada_VALOR() throws E_S_exceção {
        try { return new fluxo_de_entrada(padrão_biblioteca_ponte.getInputStream());
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public fluxo_de_saída saídaTexto() throws E_S_exceção {
        try { return new fluxo_de_saída(padrão_biblioteca_ponte.getOutputStream());
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void TEMPOLIMITE(int 밀리초) throws E_S_exceção {
        try { padrão_biblioteca_ponte.setSoTimeout(밀리초);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public int número_da_porta() { return padrão_biblioteca_ponte.getPort(); }
    public int local_número_da_porta() { return padrão_biblioteca_ponte.getLocalPort(); }
    public boolean TI_fechado() { return padrão_biblioteca_ponte.isClosed(); }
    public boolean 연결됨() { return padrão_biblioteca_ponte.isConnected(); }
    public void Fechar() throws E_S_exceção {
        try { padrão_biblioteca_ponte.close();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
}
