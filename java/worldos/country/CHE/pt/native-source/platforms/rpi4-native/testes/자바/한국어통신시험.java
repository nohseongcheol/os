// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.nativo.*;

/** 동일 바이트코드를 OpenJDK와 nativo JVM에서 실행하는 comunicação 계약 testes. */
public class 한국어통신시험 {
    public static void main(String[] argumentos) throws E_S_exceção {
        porta_de_recepção porta_VALOR = conexão_transporte.수신열기(0);
        conexão convidado_VALOR = conexão_transporte.Abrir("127.0.0.1", porta_VALOR.número_da_porta());
        conexão proprietário_identificador = porta_VALOR.receber();
        convidado_VALOR.TEMPOLIMITE(200); proprietário_identificador.TEMPOLIMITE(200);
        검사.참인지(convidado_VALOR.연결됨() && !convidado_VALOR.TI_fechado(), "Ligar Estado_VALOR");
        검사.참인지(proprietário_identificador.número_da_porta() == convidado_VALOR.local_número_da_porta(), "par_VALOR número_da_porta");
        검사.참인지(convidado_VALOR.número_da_porta() == proprietário_identificador.local_número_da_porta(), "local_Scope número_da_porta");
        fluxo_de_entrada entrada_VALOR = proprietário_identificador.entrada_VALOR(); fluxo_de_saída saída_página = convidado_VALOR.saídaTexto();
        byte[] email = 문자.codificar("한글 fluxo_VALOR");
        saída_página.Escrita(email, 0, email.length); saída_página.내보내기();
        byte[] RECEBER_SMS = new byte[email.length];
        int leitura_CONT_NÚM = 0;
        while (leitura_CONT_NÚM < RECEBER_SMS.length) {
            int 더읽음 = entrada_VALOR.Leitura(RECEBER_SMS, leitura_CONT_NÚM, RECEBER_SMS.length - leitura_CONT_NÚM);
            검사.참인지(더읽음 > 0, "예상하지 않은 ficheiro 끝"); leitura_CONT_NÚM += 더읽음;
        }
        검사.참인지(문자.같음(문자.descriptografar_dados(RECEBER_SMS), "한글 fluxo_VALOR"), "부분 읽기와 Escrita");
        saída_página.Escrita(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = entrada_VALOR.Leitura(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIZ_VALOR Leitura");
        if (첫읽기 == 1) 두바이트[1] = (byte)entrada_VALOR.Leitura();
        검사.참인지(두바이트[1] == 18, "나머지 Leitura");
        proprietário_identificador.saídaTexto().Escrita(255);
        검사.참인지(convidado_VALOR.entrada_VALOR().Leitura() == 255, "Codificação_VALOR 없는 한 byte_VALOR");
        saída_página.Fechar();
        검사.참인지(convidado_VALOR.TI_fechado() && entrada_VALOR.Leitura() == -1, "닫기와 ficheiro 끝");
        entrada_VALOR.Fechar(); 검사.참인지(proprietário_identificador.TI_fechado(), "entrada_VALOR fluxo_VALOR Fechar");
        convidado_VALOR.Fechar(); proprietário_identificador.Fechar();
        porta_VALOR.TEMPOLIMITE(15);
        boolean execução_TEMPOLIMITE = false;
        try { porta_VALOR.receber(); } catch (aguarde_TEMPOLIMITE_exceção 예상한오류) { execução_TEMPOLIMITE = true; }
        검사.참인지(execução_TEMPOLIMITE, "receber_VALOR TEMPOLIMITE");
        porta_VALOR.Fechar(); 검사.참인지(porta_VALOR.TI_fechado(), "porta_de_recepção Fechar");
        datagrama_Canal 받는곳 = datagrama_Canal.Abrir(0), 보내는곳 = datagrama_Canal.Abrir(0);
        받는곳.TEMPOLIMITE(200);
        보내는곳.enviar("127.0.0.1", 받는곳.número_da_porta(), "datagrama 한글");
        검사.참인지(문자.같음(받는곳.receber(), "datagrama 한글"), "datagrama 송수신");
        보내는곳.Fechar(); 받는곳.Fechar();
        검사.참인지(보내는곳.TI_fechado() && 받는곳.TI_fechado(), "datagrama Fechar");
        saídaTexto.gravar_linha("Português comunicação verificar: Ligar datagrama fluxo_VALOR execução_TEMPOLIMITE Fechar");
    }
}
