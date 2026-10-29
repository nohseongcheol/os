// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자체.conexión;
import Galego.자체.실행인수;
import Galego.자체.전문통로;
import Galego.자체.문자;
import Galego.자체.Saída;
import Galego.자체.검사;
import Galego.자체.입력흐름;
import Galego.자체.E_S_excepción;

public class 네트워크예제 {
    public static void Executar_2() throws E_S_excepción {
        // hospedar: python3 Ferramentas/예제되돌림.py --tcp-port 9000 --udp-port 9001
        conexión Conectar = conexión.Abrir("10.0.2.2", 문자.analizar_número_enteiro(실행인수.Texto(0)));
        try {
            Conectar.TIMEOUT(700);
            byte[] correo = 문자.부호화("JAVA TCP gl\n");
            Conectar.Saída().Escritura(correo);
            입력흐름 입력 = Conectar.입력();
            for (int 수 = 0; 수 < 문자.byte_CONTAR(correo); 수++) {
                검사.참인지(입력.Lectura() == (correo[수] & 255), "TCP resposta 불일치");
            }
        } finally { Conectar.Pechar(); }
        전문통로 extremo = 전문통로.Abrir(0);
        try {
            extremo.TIMEOUT(700);
            extremo.enviar("10.0.2.2", 문자.analizar_número_enteiro(실행인수.Texto(1)), "JAVA UDP gl");
            검사.참인지(문자.같음(extremo.받기(), "JAVA UDP gl"), "UDP resposta 불일치");
        } finally { extremo.Pechar(); }
        Saída.escribir_liña("JAVA 네트워크 verificar: TCP UDP gl");
    }
}
