// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.체계호출;

import España.JEspOS.기억공간.páxina_xefe;
import España.JEspOS.작업.Proceso_VALOR;
import España.JEspOS.작업.Programador;
import España.JEspOS.sistema_de_ficheiros.실행파일적재기;
import España.JEspOS.sistema_de_ficheiros.sistema_de_ficheiros;
import España.JEspOS.sistema_de_ficheiros.Ficheiro_información;
import España.JEspOS.kernel.하드웨어;
import España.JEspOS.입력.입력관리자;
import España.JEspOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int só_de_lectura_marca = 0;
    public static final int ACHAR_START = 0;
    public static final int ACHAR_ao_corrente = 1;
    public static final int Busca_introdución_finalizar = 2;

    private final sistema_de_ficheiros sistema_de_ficheiros;
    private final páxina_xefe 쪽관리;
    private final Programador Programador;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 dispositivo_VALOR;
    private final 입력관리자 입력관리;

    public 체계호출(sistema_de_ficheiros sistema_de_ficheiros, páxina_xefe 쪽관리, Programador Programador, 하드웨어 dispositivo_VALOR, 입력관리자 입력관리) {
        this.sistema_de_ficheiros = sistema_de_ficheiros;
        this.쪽관리 = 쪽관리;
        this.Programador = Programador;
        this.dispositivo_VALOR = dispositivo_VALOR;
        this.입력관리 = 입력관리;
    }

    public int 과정식별자(Proceso_VALOR ao_corrente_Proceso) {
        return ao_corrente_Proceso.식별자();
    }

    public int 부모과정식별자(Proceso_VALOR ao_corrente_Proceso) {
        return ao_corrente_Proceso.부모식별자();
    }

    public int Abrir(Proceso_VALOR ao_corrente_Proceso, String Nome, int marca_VALOR) {
        if (marca_VALOR != só_de_lectura_marca) {
            return -30;
        }
        return ao_corrente_Proceso.파일서술자().Abrir(Nome);
    }

    public int Lectura(Proceso_VALOR ao_corrente_Proceso, int 서술자, byte[] 받을곳, int Tamaño) {
        if (서술자 == 0) {
            if (Tamaño <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Evento = 입력관리.Seguinte_evento();
            if (Evento == null || Evento.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) Evento.첫째값();
            return 1;
        }
        return ao_corrente_Proceso.파일서술자().Lectura(서술자, 받을곳, Tamaño);
    }

    public int Escritura(Proceso_VALOR ao_corrente_Proceso, int 서술자, byte[] datos, int Tamaño) {
        if (서술자 != 1 && 서술자 != 2) {
            return ao_corrente_Proceso.파일서술자().Tecnoloxía_da_información_TI_abrir(서술자) ? -30 : -9;
        }
        if (Tamaño < 0 || Tamaño > datos.length) {
            return -22;
        }
        dispositivo_VALOR.직렬출력(new String(datos, 0, Tamaño, java.nio.charset.StandardCharsets.UTF_8));
        return Tamaño;
    }

    public int Pechar(Proceso_VALOR ao_corrente_Proceso, int 서술자) {
        return ao_corrente_Proceso.파일서술자().Pechar(서술자);
    }

    public int mover_cargo(Proceso_VALOR ao_corrente_Proceso, int 서술자, int 거리, int Project_raíz) {
        return ao_corrente_Proceso.파일서술자().mover_cargo(서술자, 거리, Project_raíz);
    }

    public int 서술자복제(Proceso_VALOR ao_corrente_Proceso, int 서술자) {
        return ao_corrente_Proceso.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proceso_VALOR ao_corrente_Proceso, int 서술자, int 새서술자) {
        return ao_corrente_Proceso.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nome, int 방식) {
        Ficheiro_información msinfo32_exe = sistema_de_ficheiros.msinfo32_exe(Nome);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((방식 & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((방식 & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int mudar_lista_de_tarefas(String Nome) {
        return "/".equals(Nome) ? 0 : -20;
    }

    public String ao_corrente_lista_de_tarefas(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int 사용자식별자() { return 0; }
    public int 유효사용자식별자() { return 0; }
    public int 무리식별자() { return 0; }
    public int 유효무리식별자() { return 0; }

    public int sinc_Ficheiro(Proceso_VALOR ao_corrente_Proceso, int 서술자) {
        return ao_corrente_Proceso.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // ao_corrente_elemento 파일체계는 Lectura 전용이어서 밀어낼 자료가 없다.
    }

    public boolean Tecnoloxía_da_información_TI_Terminal(Proceso_VALOR ao_corrente_Proceso, int 서술자) {
        Ficheiro_información msinfo32_exe = ao_corrente_Proceso.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Ficheiro_control(Proceso_VALOR ao_corrente_Proceso, int 서술자, int Orde, int parámetro_argumento) {
        if (Orde == 0) {
            return ao_corrente_Proceso.파일서술자().복제서술자(서술자, parámetro_argumento);
        }
        if (Orde == 1) {
            return ao_corrente_Proceso.파일서술자().실행시닫기값(서술자);
        }
        if (Orde == 2) {
            return ao_corrente_Proceso.파일서술자().실행시닫기설정(서술자, (parámetro_argumento & 1) != 0);
        }
        if (Orde == 3) {
            return ao_corrente_Proceso.파일서술자().msinfo32_exe(서술자) == null ? -9 : só_de_lectura_marca;
        }
        if (Orde == 4) {
            return parámetro_argumento == só_de_lectura_marca ? 0 : -30;
        }
        return -22;
    }

    public int crear_introdución(String Nome, int permiso_VALOR) {
        return -30;
    }

    public Ficheiro_información 서술자정보(Proceso_VALOR ao_corrente_Proceso, int 서술자) {
        return ao_corrente_Proceso.파일서술자().msinfo32_exe(서술자);
    }

    public sistema_Detalles sistema_Detalles() {
        return new sistema_Detalles("JEspOS", "JEspOS", "0.1", "Java managed kernel", "i386");
    }

    public Ficheiro_información Ficheiro_información(String Nome) {
        return sistema_de_ficheiros.msinfo32_exe(Nome);
    }

    public Proceso_VALOR clon_Proceso(Proceso_VALOR 부모) {
        return Programador.clon_VALOR(부모);
    }

    public int 자식기다리기(Proceso_VALOR 부모, int 자식식별자, boolean 기다리지않음) {
        return Programador.자식기다리기(부모, 자식식별자, 기다리지않음);
    }

    public int apl_pausa(Proceso_VALOR ao_corrente_Proceso, int 새끝) {
        int 이전끝 = ao_corrente_Proceso.apl_pausa();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / páxina_xefe.tamaño_da_páxina;
        int 끝쪽 = (새끝 + páxina_xefe.tamaño_da_páxina - 1) / páxina_xefe.tamaño_da_páxina;
        if (새끝 > 이전끝) {
            for (int ÍNDICE = 첫쪽; ÍNDICE < 끝쪽; ÍNDICE++) {
                int ENDEREZO = ÍNDICE * páxina_xefe.tamaño_da_páxina;
                try {
                    쪽관리.바이트읽기(ao_corrente_Proceso.ENDEREZO_espazo(), ENDEREZO);
                } catch (IllegalStateException ERRO) {
                    쪽관리.MAP_páxina(ao_corrente_Proceso.ENDEREZO_espazo(), ENDEREZO, true);
                }
            }
        }
        ao_corrente_Proceso.conxunto_apl_pausa(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proceso_VALOR ao_corrente_Proceso, int 증가량) {
        int 이전끝 = ao_corrente_Proceso.apl_pausa();
        int RESULTANTE = apl_pausa(ao_corrente_Proceso, 이전끝 + 증가량);
        return RESULTANTE < 0 ? RESULTANTE : 이전끝;
    }

    public int executar_comando(Proceso_VALOR ao_corrente_Proceso, byte[] 실행파일) {
        return executar_comando(ao_corrente_Proceso, 실행파일, new String[0], new String[0]);
    }

    public int executar_comando(Proceso_VALOR ao_corrente_Proceso, byte[] 실행파일, String[] parámetro_argumento, String[] 환경) {
        실행파일적재기.IMAXE IMAXE_VALOR;
        try {
            IMAXE_VALOR = 적재기.검사(실행파일);
        } catch (IllegalArgumentException ERRO) {
            return -8;
        }
        if (parámetro_argumento == null || 환경 == null || parámetro_argumento.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.sección_VALOR sección_VALOR : IMAXE_VALOR.구역들()) {
            if ((sección_VALOR.marca_VALOR() & 2) == 0 || sección_VALOR.Tamaño() == 0) {
                continue;
            }
            int 첫쪽 = sección_VALOR.ENDEREZO() / páxina_xefe.tamaño_da_páxina;
            int 끝쪽 = (sección_VALOR.ENDEREZO() + sección_VALOR.Tamaño() + páxina_xefe.tamaño_da_páxina - 1) / páxina_xefe.tamaño_da_páxina;
            for (int ÍNDICE = 첫쪽; ÍNDICE < 끝쪽; ÍNDICE++) {
                int ENDEREZO = ÍNDICE * páxina_xefe.tamaño_da_páxina;
                try {
                    쪽관리.바이트읽기(ao_corrente_Proceso.ENDEREZO_espazo(), ENDEREZO);
                    쪽관리.Privado_intervalo_escribir(ao_corrente_Proceso.ENDEREZO_espazo(), ENDEREZO, páxina_xefe.tamaño_da_páxina);
                } catch (IllegalStateException ERRO) {
                    쪽관리.MAP_páxina(ao_corrente_Proceso.ENDEREZO_espazo(), ENDEREZO, true);
                }
            }
            for (int ÍNDICE = 0; ÍNDICE < sección_VALOR.Tamaño(); ÍNDICE++) {
                byte VALOR = sección_VALOR.종류() == 8 ? 0 : 실행파일[sección_VALOR.Ficheiro_cargo() + ÍNDICE];
                쪽관리.escribir_byte_VALOR(ao_corrente_Proceso.ENDEREZO_espazo(), sección_VALOR.ENDEREZO() + ÍNDICE, VALOR);
            }
        }
        ao_corrente_Proceso.실행문맥설정(IMAXE_VALOR.START_ENDEREZO(), parámetro_argumento, 환경);
        ao_corrente_Proceso.파일서술자().실행시닫기();
        return 0;
    }

    public void saír_apl_55b3a1cd(Proceso_VALOR ao_corrente_Proceso, int Estado_VALOR) {
        ao_corrente_Proceso.saír_apl(Estado_VALOR);
    }
}
