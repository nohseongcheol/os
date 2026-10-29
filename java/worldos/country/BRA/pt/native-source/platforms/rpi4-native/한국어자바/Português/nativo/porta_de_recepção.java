// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** receber_VALOR(受信)·porta_VALOR(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class porta_de_recepção {
    private final java.net.ServerSocket padrão_porta;
    private porta_de_recepção(int número_da_porta) throws E_S_exceção {
        try { padrão_porta = new java.net.ServerSocket(número_da_porta);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static porta_de_recepção Abrir(int número_da_porta) throws E_S_exceção {
        try { return new porta_de_recepção(número_da_porta);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public conexão receber() throws E_S_exceção {
        try { return new conexão(padrão_porta.accept());
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public int número_da_porta() { return padrão_porta.getLocalPort(); }
    public void TEMPOLIMITE(int 밀리초) throws E_S_exceção {
        try { padrão_porta.setSoTimeout(밀리초);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public boolean TI_fechado() { return padrão_porta.isClosed(); }
    public void Fechar() throws E_S_exceção {
        try { padrão_porta.close();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
}
