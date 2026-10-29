// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static conexión Abrir(String ENDEREZO, int número_do_porto) throws E_S_excepción {
        try { return conexión.Abrir(ENDEREZO, número_do_porto);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static 수신창구 수신열기(int número_do_porto) throws E_S_excepción {
        try { return 수신창구.Abrir(número_do_porto);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static Socket Conectar(String ENDEREZO, int porto_VALOR) throws E_S_excepción {
        try { return new Socket(ENDEREZO, porto_VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static ServerSocket agardar_extremo(int porto_VALOR) throws E_S_excepción {
        try { return new ServerSocket(porto_VALOR);
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
    public static Socket 받기(ServerSocket servidor_VALOR) throws E_S_excepción {
        try { return servidor_VALOR.accept();
        } catch (java.io.IOException ERRO) { throw CONVERTER_excepción.E_S(ERRO); }
        catch (RuntimeException ERRO) { throw CONVERTER_excepción.executar_comando(ERRO); }
    }
}
