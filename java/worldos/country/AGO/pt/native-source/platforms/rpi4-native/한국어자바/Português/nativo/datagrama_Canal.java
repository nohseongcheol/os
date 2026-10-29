// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** datagrama(電文)·Canal_entrada(通路): 경계를 가진 UDP 자료를 주고받는 empresa. */
public final class datagrama_Canal {
    private final java.net.DatagramSocket padrão_empresa;
    private datagrama_Canal(int número_da_porta) throws E_S_exceção {
        try { padrão_empresa = comunicação.Abrir(número_da_porta);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static datagrama_Canal Abrir(int número_da_porta) throws E_S_exceção {
        try { return new datagrama_Canal(número_da_porta);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void enviar(String Endereço, int número_da_porta, String dados) throws E_S_exceção {
        try { comunicação.enviar(padrão_empresa, Endereço, número_da_porta, dados);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public String receber() throws E_S_exceção {
        try { return comunicação.receber(padrão_empresa);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public void TEMPOLIMITE(int 밀리초) throws E_S_exceção {
        try { comunicação.TEMPOLIMITE(padrão_empresa, 밀리초);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public int número_da_porta() { return padrão_empresa.getLocalPort(); }
    public boolean TI_fechado() { return padrão_empresa.isClosed(); }
    public void Fechar() { comunicação.Fechar(padrão_empresa); }
}
