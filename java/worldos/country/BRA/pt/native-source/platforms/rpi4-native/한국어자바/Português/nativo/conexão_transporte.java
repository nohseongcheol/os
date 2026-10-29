// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
import java.net.*;
public final class conexão_transporte {
    private conexão_transporte() {}
    public static conexão Abrir(String Endereço, int número_da_porta) throws E_S_exceção {
        try { return conexão.Abrir(Endereço, número_da_porta);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static porta_de_recepção 수신열기(int número_da_porta) throws E_S_exceção {
        try { return porta_de_recepção.Abrir(número_da_porta);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static Socket Ligar(String Endereço, int porta_VALOR) throws E_S_exceção {
        try { return new Socket(Endereço, porta_VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static ServerSocket escutar_empresa(int porta_VALOR) throws E_S_exceção {
        try { return new ServerSocket(porta_VALOR);
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
    public static Socket receber(ServerSocket servidor_VALOR) throws E_S_exceção {
        try { return servidor_VALOR.accept();
        } catch (java.io.IOException erro) { throw CONVERTER_exceção.E_S(erro); }
        catch (RuntimeException erro) { throw CONVERTER_exceção.Executar_comando(erro); }
    }
}
