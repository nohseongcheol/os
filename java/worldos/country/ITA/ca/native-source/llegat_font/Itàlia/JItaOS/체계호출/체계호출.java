// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Itàlia.JItaOS.체계호출;

import Itàlia.JItaOS.기억공간.pàgina_administrador;
import Itàlia.JItaOS.작업.Procés_VALOR;
import Itàlia.JItaOS.작업.Planificador;
import Itàlia.JItaOS.sistema_d_arxius.실행파일적재기;
import Itàlia.JItaOS.sistema_d_arxius.sistema_d_arxius;
import Itàlia.JItaOS.sistema_d_arxius.arxiu_informació;
import Itàlia.JItaOS.nucli.하드웨어;
import Itàlia.JItaOS.입력.입력관리자;
import Itàlia.JItaOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int només_de_lectura_marcar = 0;
    public static final int Cerca_Inici = 0;
    public static final int 찾기현재 = 1;
    public static final int BUSCA_introducció_finalitzar = 2;

    private final sistema_d_arxius sistema_d_arxius;
    private final pàgina_administrador 쪽관리;
    private final Planificador Planificador;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 dispositiu_VALOR;
    private final 입력관리자 입력관리;

    public 체계호출(sistema_d_arxius sistema_d_arxius, pàgina_administrador 쪽관리, Planificador Planificador, 하드웨어 dispositiu_VALOR, 입력관리자 입력관리) {
        this.sistema_d_arxius = sistema_d_arxius;
        this.쪽관리 = 쪽관리;
        this.Planificador = Planificador;
        this.dispositiu_VALOR = dispositiu_VALOR;
        this.입력관리 = 입력관리;
    }

    public int Procés_identificador(Procés_VALOR 현재과정) {
        return 현재과정.identificador_VALOR();
    }

    public int 부모과정식별자(Procés_VALOR 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Obre(Procés_VALOR 현재과정, String Nom, int marcar_VALOR_58846146) {
        if (marcar_VALOR_58846146 != només_de_lectura_marcar) {
            return -30;
        }
        return 현재과정.파일서술자().Obre(Nom);
    }

    public int Lectura(Procés_VALOR 현재과정, int 서술자, byte[] rebre_destinació, int Mida) {
        if (서술자 == 0) {
            if (Mida <= 0 || rebre_destinació.length == 0) {
                return 0;
            }
            입력사건 Esdeveniment = 입력관리.Següent_incidència();
            if (Esdeveniment == null || Esdeveniment.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            rebre_destinació[0] = (byte) Esdeveniment.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Lectura(서술자, rebre_destinació, Mida);
    }

    public int Escriptura(Procés_VALOR 현재과정, int 서술자, byte[] dades, int Mida) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().tecnologies_de_la_informació_crear(서술자) ? -30 : -9;
        }
        if (Mida < 0 || Mida > dades.length) {
            return -22;
        }
        dispositiu_VALOR.직렬출력(new String(dades, 0, Mida, java.nio.charset.StandardCharsets.UTF_8));
        return Mida;
    }

    public int Tanca(Procés_VALOR 현재과정, int 서술자) {
        return 현재과정.파일서술자().Tanca(서술자);
    }

    public int moure_càrrec(Procés_VALOR 현재과정, int 서술자, int 거리, int Project_rel) {
        return 현재과정.파일서술자().moure_càrrec(서술자, 거리, Project_rel);
    }

    public int 서술자복제(Procés_VALOR 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Procés_VALOR 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nom, int 방식) {
        arxiu_informació msinfo32_exe = sistema_d_arxius.msinfo32_exe(Nom);
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

    public int canvi_tasca_Llista(String Nom) {
        return "/".equals(Nom) ? 0 : -20;
    }

    public String 현재작업목록(int rebre_canviar_la_mida) {
        return rebre_canviar_la_mida >= 2 ? "/" : null;
    }

    public int ID_de_l_usuari() { return 0; }
    public int efectiu_ID_de_l_usuari() { return 0; }
    public int Grup_identificador() { return 0; }
    public int efectiu_Grup_identificador() { return 0; }

    public int sincronitzar_arxiu(Procés_VALOR 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Lectura 전용이어서 밀어낼 자료가 없다.
    }

    public boolean tecnologies_de_la_informació_Terminal(Procés_VALOR 현재과정, int 서술자) {
        arxiu_informació msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int arxiu_control(Procés_VALOR 현재과정, int 서술자, int Ordre, int paràmetre_arg) {
        if (Ordre == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, paràmetre_arg);
        }
        if (Ordre == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Ordre == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (paràmetre_arg & 1) != 0);
        }
        if (Ordre == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : només_de_lectura_marcar;
        }
        if (Ordre == 4) {
            return paràmetre_arg == només_de_lectura_marcar ? 0 : -30;
        }
        return -22;
    }

    public int Crear_introducció(String Nom, int permís_VALOR) {
        return -30;
    }

    public arxiu_informació 서술자정보(Procés_VALOR 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public sistema_Detalls sistema_Detalls() {
        return new sistema_Detalls("JItaOS", "JItaOS", "0.1", "Java managed kernel", "i386");
    }

    public arxiu_informació arxiu_informació(String Nom) {
        return sistema_d_arxius.msinfo32_exe(Nom);
    }

    public Procés_VALOR clon_Procés(Procés_VALOR 부모) {
        return Planificador.clon_VALOR(부모);
    }

    public int 자식기다리기(Procés_VALOR 부모, int nen_identificador, boolean 기다리지않음) {
        return Planificador.자식기다리기(부모, nen_identificador, 기다리지않음);
    }

    public int programa_pausa(Procés_VALOR 현재과정, int 새끝) {
        int 이전끝 = 현재과정.programa_pausa();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / pàgina_administrador.mida_de_la_pàgina;
        int 끝쪽 = (새끝 + pàgina_administrador.mida_de_la_pàgina - 1) / pàgina_administrador.mida_de_la_pàgina;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adreça = INDEX * pàgina_administrador.mida_de_la_pàgina;
                try {
                    쪽관리.tancar_byte_VALOR(현재과정.ADREÇA_espai(), Adreça);
                } catch (IllegalStateException s_ha_produït_un_error) {
                    쪽관리.MAP_pàgina(현재과정.ADREÇA_espai(), Adreça, true);
                }
            }
        }
        현재과정.conjunt_programa_pausa(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Procés_VALOR 현재과정, int 증가량) {
        int 이전끝 = 현재과정.programa_pausa();
        int RESULTAT = programa_pausa(현재과정, 이전끝 + 증가량);
        return RESULTAT < 0 ? RESULTAT : 이전끝;
    }

    public int Executa_ordre(Procés_VALOR 현재과정, byte[] 실행파일) {
        return Executa_ordre(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int Executa_ordre(Procés_VALOR 현재과정, byte[] 실행파일, String[] paràmetre_arg, String[] entorn) {
        실행파일적재기.IMATGE IMATGE_VALOR;
        try {
            IMATGE_VALOR = 적재기.검사(실행파일);
        } catch (IllegalArgumentException s_ha_produït_un_error) {
            return -8;
        }
        if (paràmetre_arg == null || entorn == null || paràmetre_arg.length > 16 || entorn.length > 16) {
            return -7;
        }
        for (실행파일적재기.secció_VALOR secció_VALOR : IMATGE_VALOR.구역들()) {
            if ((secció_VALOR.marcar_VALOR_58846146() & 2) == 0 || secció_VALOR.Mida() == 0) {
                continue;
            }
            int 첫쪽 = secció_VALOR.Adreça() / pàgina_administrador.mida_de_la_pàgina;
            int 끝쪽 = (secció_VALOR.Adreça() + secció_VALOR.Mida() + pàgina_administrador.mida_de_la_pàgina - 1) / pàgina_administrador.mida_de_la_pàgina;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adreça = INDEX * pàgina_administrador.mida_de_la_pàgina;
                try {
                    쪽관리.tancar_byte_VALOR(현재과정.ADREÇA_espai(), Adreça);
                    쪽관리.Privat_interval_escriure(현재과정.ADREÇA_espai(), Adreça, pàgina_administrador.mida_de_la_pàgina);
                } catch (IllegalStateException s_ha_produït_un_error) {
                    쪽관리.MAP_pàgina(현재과정.ADREÇA_espai(), Adreça, true);
                }
            }
            for (int INDEX = 0; INDEX < secció_VALOR.Mida(); INDEX++) {
                byte VALOR = secció_VALOR.종류() == 8 ? 0 : 실행파일[secció_VALOR.arxiu_càrrec() + INDEX];
                쪽관리.escriure_byte_VALOR(현재과정.ADREÇA_espai(), secció_VALOR.Adreça() + INDEX, VALOR);
            }
        }
        현재과정.실행문맥설정(IMATGE_VALOR.Inici_ADREÇA(), paràmetre_arg, entorn);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void sortir_programa(Procés_VALOR 현재과정, int Estat_VALOR) {
        현재과정.Surt_programa(Estat_VALOR);
    }
}
