// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Antígua_e_Barbuda.JAtgOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Antígua_e_Barbuda.JAtgOS.Memória_região.Gerenciador_de_Páginas;
import Antígua_e_Barbuda.JAtgOS.sistema_de_arquivos.Arquivo_descritor_tabela;

/** Processo_VALOR 식별자와 라운드로빈 Preparar 대기열을 관리한다. */
public final class Agendador {
    private final Gerenciador_de_Páginas 쪽관리;
    private final Map<Integer, Processo_VALOR> Lista_de_Processos = new HashMap<Integer, Processo_VALOR>();
    private final Queue<Processo_VALOR> 준비대기열 = new ArrayDeque<Processo_VALOR>();
    private int Avançar_identificador = 1;

    public Agendador(Gerenciador_de_Páginas 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Processo_VALOR 첫과정(Arquivo_descritor_tabela Arquivo_descritor) {
        Processo_VALOR 새과정 = new Processo_VALOR(alocar_identificador(), 0, 쪽관리.새주소공간(), Arquivo_descritor);
        Lista_de_Processos.put(Integer.valueOf(새과정.identificador_VALOR()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Processo_VALOR clone_VALOR(Processo_VALOR pai_VALOR) {
        Processo_VALOR filho_VALOR = new Processo_VALOR(
                alocar_identificador(),
                pai_VALOR.identificador_VALOR(),
                쪽관리.clone_COW(pai_VALOR.espaço_de_endereço()),
                pai_VALOR.Arquivo_descritor().clone_VALOR());
        filho_VALOR.set_app_intervalo(pai_VALOR.app_intervalo());
        Lista_de_Processos.put(Integer.valueOf(filho_VALOR.identificador_VALOR()), filho_VALOR);
        준비대기열.offer(filho_VALOR);
        return filho_VALOR;
    }

    public Processo_VALOR Avançar_Processo() {
        int cheque_CONT_NÚM = 준비대기열.size();
        for (int ÍNDICE = 0; ÍNDICE < cheque_CONT_NÚM; ÍNDICE++) {
            Processo_VALOR Avançar_item = 준비대기열.poll();
            if (Avançar_item != null && (Avançar_item.Estado_VALOR() == Processo_Estado.Preparar || Avançar_item.Estado_VALOR() == Processo_Estado.Executar_comando)) {
                Avançar_item.set_Estado(Processo_Estado.Executar_comando);
                준비대기열.offer(Avançar_item);
                return Avançar_item;
            }
        }
        return null;
    }

    public int 자식기다리기(Processo_VALOR pai_VALOR, int filho_identificador, boolean 기다리지않음) {
        for (Processo_VALOR candidato : Lista_de_Processos.values()) {
            if (candidato.pai_identificador() != pai_VALOR.identificador_VALOR()) {
                continue;
            }
            if (filho_identificador > 0 && candidato.identificador_VALOR() != filho_identificador) {
                continue;
            }
            if (candidato.Estado_VALOR() == Processo_Estado.sair_app) {
                int resultado = (candidato.código_de_saída() & 0xff) << 8;
                Lista_de_Processos.remove(Integer.valueOf(candidato.identificador_VALOR()));
                return resultado;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Processo_VALOR PROCURAR_Processo(int identificador_VALOR) {
        return Lista_de_Processos.get(Integer.valueOf(identificador_VALOR));
    }

    private int alocar_identificador() {
        return Avançar_identificador++;
    }
}
