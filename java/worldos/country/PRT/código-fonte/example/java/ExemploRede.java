// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.nativo.conexão;
import Português.nativo.실행인수;
import Português.nativo.datagrama_Canal;
import Português.nativo.문자;
import Português.nativo.saídaTexto;
import Português.nativo.검사;
import Português.nativo.fluxo_de_entrada;
import Português.nativo.E_S_exceção;

public class ExemploRede {
    public static void iniciar() throws E_S_exceção {
        // host: python3 ferramentas/예제되돌림.py --tcp-port 9000 --udp-port 9001
        conexão Ligar = conexão.Abrir("10.0.2.2", 문자.analisar_inteiro(실행인수.texto(0)));
        try {
            Ligar.TEMPOLIMITE(700);
            byte[] email = 문자.codificar("JAVA TCP Português\n");
            Ligar.saídaTexto().Escrita(email);
            fluxo_de_entrada entrada_VALOR = Ligar.entrada_VALOR();
            for (int número = 0; número < 문자.byte_CONT_NÚM(email); número++) {
                검사.참인지(entrada_VALOR.Leitura() == (email[número] & 255), "TCP resposta 불일치");
            }
        } finally { Ligar.Fechar(); }
        datagrama_Canal empresa = datagrama_Canal.Abrir(0);
        try {
            empresa.TEMPOLIMITE(700);
            empresa.enviar("10.0.2.2", 문자.analisar_inteiro(실행인수.texto(1)), "JAVA UDP Português");
            검사.참인지(문자.같음(empresa.receber(), "JAVA UDP Português"), "UDP resposta 불일치");
        } finally { empresa.Fechar(); }
        saídaTexto.gravar_linha("JAVA 네트워크 verificar: TCP UDP Português");
    }
}
