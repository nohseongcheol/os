// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Andorra.JAndOS.시험;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Andorra.JAndOS.기억공간.Memòria_administrador;
import Andorra.JAndOS.기억공간.pàgina_administrador;
import Andorra.JAndOS.입력.입력사건;
import Andorra.JAndOS.작업.Procés_VALOR;
import Andorra.JAndOS.체계호출.체계호출;
import Andorra.JAndOS.sistema_d_arxius.실행파일적재기;
import Andorra.JAndOS.nucli.nucli;
import Andorra.JAndOS.allotjar.호스트하드웨어;
import Andorra.JAndOS.interrupció.interrupció_administrador;
import Andorra.JAndOS.서술자.전역서술자표;
import Andorra.JAndOS.Emmagatzematge_dispositiu.고급기술결합장치;
import Andorra.JAndOS.dispositiu_VALOR.accessori_bus_administrador;
import Andorra.JAndOS.xarxa_Pila.xarxa_Eines;
import Andorra.JAndOS.xarxa_Pila.xarxa_capa;
import Andorra.JAndOS.dispositiu_VALOR.Rellotge;
import Andorra.JAndOS.서술자.tasca_Estat_segment;
import Andorra.JAndOS.화면.caràcter_mostrar;
import Andorra.JAndOS.sistema_d_arxius.기본분할영역표;

public final class 전체시험 {
    private static int transmetre_COMPT;

    private 전체시험() {
    }

    public static void main(String[] paràmetre_arg) {
        호스트하드웨어 dispositiu_VALOR = new 호스트하드웨어();
        nucli nucli_VALOR = new nucli(dispositiu_VALOR);
        nucli_VALOR.Executa_2();

        기억공간시험(nucli_VALOR);
        쪽관리시험(nucli_VALOR);
        파일과과정시험(nucli_VALOR);
        실행파일시험(nucli_VALOR);
        입력시험(nucli_VALOR);
        하드웨어시험(dispositiu_VALOR);
        개입중단과서술자시험();
        저장장치와통신망시험();
        화면과시계시험();

        System.out.println("JAndOS 시험 transmetre_VALOR: " + transmetre_COMPT);
    }

    private static void 기억공간시험(nucli nucli_VALOR) {
        Memòria_administrador administrador_VALOR = nucli_VALOR.기억공간();
        int 첫주소 = administrador_VALOR.정렬할당(100, 64);
        verificar((첫주소 & 63) == 0, "alinear_VALOR assignar_Emmagatzematge");
        administrador_VALOR.escriure_byte_VALOR(첫주소, (byte) 0x5a);
        verificar(administrador_VALOR.tancar_byte_VALOR(첫주소) == (byte) 0x5a, "물리 기억공간 읽고 Escriptura");
        int 사용전 = administrador_VALOR.사용크기();
        administrador_VALOR.versió_Emmagatzematge(첫주소);
        verificar(administrador_VALOR.사용크기() < 사용전, "기억공간 versió_Emmagatzematge");
    }

    private static void 쪽관리시험(nucli nucli_VALOR) {
        pàgina_administrador administrador_VALOR = nucli_VALOR.쪽관리();
        pàgina_administrador.ADREÇA_espai 부모공간 = administrador_VALOR.새주소공간();
        administrador_VALOR.MAP_pàgina(부모공간, 0x1000, true);
        administrador_VALOR.escriure_byte_VALOR(부모공간, 0x1010, (byte) 7);
        pàgina_administrador.ADREÇA_espai nen_espai = administrador_VALOR.쓰기시복사복제(부모공간);
        administrador_VALOR.escriure_byte_VALOR(nen_espai, 0x1010, (byte) 9);
        verificar(administrador_VALOR.tancar_byte_VALOR(부모공간, 0x1010) == 7, "Escriptura 시 copiar_VALOR 부모 격리");
        verificar(administrador_VALOR.tancar_byte_VALOR(nen_espai, 0x1010) == 9, "Escriptura 시 copiar_VALOR nen_VALOR Escriptura");
    }

    private static void 파일과과정시험(nucli nucli_VALOR) {
        byte[] contingut_VALOR = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        nucli_VALOR.sistema_d_arxius().Annexa_arxiu("시험", contingut_VALOR);
        Procés_VALOR 부모 = nucli_VALOR.첫과정();
        체계호출 호출 = nucli_VALOR.체계호출();
        int 서술자 = 호출.Obre(부모, "/시험", 체계호출.només_de_lectura_marcar);
        verificar(서술자 >= 3, "Fitxer Obre");

        byte[] rebre_destinació = new byte[contingut_VALOR.length];
        verificar(호출.Lectura(부모, 서술자, rebre_destinació, rebre_destinació.length) == contingut_VALOR.length, "Fitxer Lectura");
        verificar(Arrays.equals(contingut_VALOR, rebre_destinació), "Fitxer contingut_VALOR");
        verificar(호출.moure_càrrec(부모, 서술자, 0, 체계호출.Cerca_Inici) == 0, "Fitxer Posició moure_VALOR");

        int 복제서술자 = 호출.서술자복제(부모, 서술자);
        verificar(복제서술자 >= 0, "서술자 clon_VALOR");
        Procés_VALOR nen_VALOR = 호출.clon_Procés(부모);
        verificar(nen_VALOR.identificador_VALOR() != 부모.identificador_VALOR(), "Procés_VALOR identificador_VALOR 분리");
        verificar(nen_VALOR.부모식별자() == 부모.identificador_VALOR(), "부모 Procés_VALOR identificador_VALOR");
        verificar(호출.Tanca(nen_VALOR, 서술자) == 0 && 부모.파일서술자().tecnologies_de_la_informació_crear(서술자), "nen_VALOR Tanca 격리");

        int 이전끝 = 호출.프로그램끝늘리기(부모, 8192);
        verificar(이전끝 == 0x06000000, "programa_f5044b9b 끝 늘리기");
        verificar(부모.programa_pausa() == 0x06002000, "programa_f5044b9b 끝 반영");
        verificar(nen_VALOR.programa_pausa() == 0x06000000, "과정별 programa_f5044b9b 끝 격리");

        nen_VALOR.Surt_programa(7);
        verificar(호출.자식기다리기(부모, nen_VALOR.identificador_VALOR(), false) == (7 << 8), "nen_VALOR Surt_programa 기다리기");
        verificar(호출.접근가능("시험", 1) == -13, "Executa_ordre permís_VALOR rebutjar_VALOR");
        verificar(호출.ID_de_l_usuari() == 0 && 호출.Grup_identificador() == 0, "사용자와 무리 identificador_VALOR");
        verificar("/".equals(호출.현재작업목록(2)) && 호출.canvi_tasca_Llista("/") == 0, "현재 작업 introducció_Llista");
        verificar(호출.tecnologies_de_la_informació_Terminal(부모, 1), "표준 Sortida 단말");
        verificar("JAndOS".equals(호출.sistema_Detalls().sistema_nom()), "sistema_operatiu_VALOR msinfo32_exe");
    }

    private static void 실행파일시험(nucli nucli_VALOR) {
        byte[] dades = new byte[92];
        dades[0] = 0x7f;
        dades[1] = 'E';
        dades[2] = 'L';
        dades[3] = 'F';
        dades[4] = 1;
        dades[5] = 1;
        정수쓰기(dades, 24, 0x04001000);
        정수쓰기(dades, 32, 52);
        짧은정수쓰기(dades, 46, 40);
        짧은정수쓰기(dades, 48, 1);
        정수쓰기(dades, 56, 8);
        정수쓰기(dades, 60, 2);
        정수쓰기(dades, 64, 0x04002000);
        정수쓰기(dades, 72, 64);

        실행파일적재기.IMATGE IMATGE_VALOR = new 실행파일적재기().검사(dades);
        verificar(IMATGE_VALOR.Inici_ADREÇA() == 0x04001000, "ELF Executa_2 Adreça");
        verificar(IMATGE_VALOR.구역들().size() == 1 && IMATGE_VALOR.구역들().get(0).종류() == 8, "ELF 빈 dades secció_VALOR");
        int 서술자 = nucli_VALOR.체계호출().Obre(nucli_VALOR.첫과정(), "시험", 체계호출.només_de_lectura_marcar);
        verificar(nucli_VALOR.체계호출().arxiu_control(nucli_VALOR.첫과정(), 서술자, 2, 1) == 0, "Executa_ordre 시 Tanca Ajusts");
        verificar(nucli_VALOR.체계호출().Executa_ordre(nucli_VALOR.첫과정(), dades, new String[] {"시험", "값"}, new String[] {"Idioma=Català"}) == 0, "ELF Executa_ordre IMATGE_VALOR 적재");
        verificar(nucli_VALOR.첫과정().실행시작주소() == 0x04001000, "Executa_ordre Executa_2 Adreça 반영");
        verificar(nucli_VALOR.첫과정().실행인자().length == 2 && nucli_VALOR.첫과정().entorn_VALOR().length == 1, "Executa_ordre 인자와 entorn");
        verificar(!nucli_VALOR.첫과정().파일서술자().tecnologies_de_la_informació_crear(서술자), "Executa_ordre 시 서술자 Tanca");
        verificar(nucli_VALOR.쪽관리().tancar_byte_VALOR(nucli_VALOR.첫과정().ADREÇA_espai(), 0x04002000) == 0, "빈 dades secció_VALOR 영 inicialitzar");
    }

    private static void 입력시험(nucli nucli_VALOR) {
        nucli_VALOR.입력관리().키누름('가');
        nucli_VALOR.입력관리().쥐이동(3, -2);
        입력사건 첫사건 = nucli_VALOR.입력관리().Següent_incidència();
        입력사건 SEGON_incidència = nucli_VALOR.입력관리().Següent_incidència();
        verificar(첫사건.사건종류() == 입력사건.종류.키누름, "자판 Esdeveniment");
        verificar(SEGON_incidència.첫째값() == 3 && SEGON_incidència.SEGON_VALOR() == -2, "쥐 moure_VALOR Esdeveniment");
    }

    private static void 하드웨어시험(호스트하드웨어 dispositiu_VALOR) {
        dispositiu_VALOR.escriure_port_byte(0x3f8, 0xab);
        verificar(dispositiu_VALOR.tancar_port_byte(0x3f8) == 0xab, "포트 E_S 경계");
        verificar(dispositiu_VALOR.직렬기록().contains("JAndOS"), "직렬 LOG_fila");
    }

    private static void 개입중단과서술자시험() {
        interrupció_administrador administrador_VALOR = new interrupció_administrador();
        administrador_VALOR.registrar_se_introducció(0x21, Emmagatzematge_ADREÇA -> Emmagatzematge_ADREÇA + 4);
        administrador_VALOR.activar();
        verificar(administrador_VALOR.distribuir_VALOR(0x21, 100) == 104, "interrupció distribuir_VALOR");
        administrador_VALOR.desactivar();
        verificar(administrador_VALOR.distribuir_VALOR(0x21, 100) == 100, "interrupció desactivar");

        전역서술자표 서술자표 = new 전역서술자표();
        서술자표.conjunt_valor_per_defecte();
        verificar(서술자표.조각들().size() == 5, "전역 서술자표");
        tasca_Estat_segment tasca_Estat = new tasca_Estat_segment();
        tasca_Estat.특권쌓임공간설정(0x10, 0x800000);
        verificar(tasca_Estat.영번쌓임조각() == 0x10 && tasca_Estat.영번쌓임주소() == 0x800000, "작업 Estat_VALOR secció_VALOR");
    }

    private static void 저장장치와통신망시험() {
        고급기술결합장치 Emmagatzematge_dispositiu = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.secció_canviar_la_mida];
        byte[] tancar_dades_VALOR = new byte[고급기술결합장치.secció_canviar_la_mida];
        쓸자료[17] = 42;
        Emmagatzematge_dispositiu.Escriptura(2, 쓸자료);
        Emmagatzematge_dispositiu.Lectura(2, tancar_dades_VALOR);
        verificar(tancar_dades_VALOR[17] == 42, "ATA secció_VALOR 읽고 Escriptura");

        accessori_bus_administrador accessori = new accessori_bus_administrador();
        accessori.발견(new accessori_bus_administrador.dispositiu_VALOR(0x1022, 0x2000, 0xc000, 11));
        verificar(accessori.BUSCA_introducció(0x1022, 0x2000) != null, "주변 dispositiu_VALOR BUSCA_introducció");

        byte[] Ethernet_marc = new byte[34];
        Ethernet_marc[12] = 0x08;
        Ethernet_marc[13] = 0x00;
        Ethernet_marc[14] = 0x45;
        verificar(xarxa_Eines.Ethernet_MAJUSC_protocol(Ethernet_marc) == 0x0800, "이더넷 상위 cas_VALOR");
        verificar(xarxa_Eines.상호통신망규약사판인가(Ethernet_marc, 14), "상호통신망규약 4판");
        verificar(xarxa_Eines.núvol_suma_de_comprovació(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 suma_de_comprovació");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        정수쓰기(첫구역, 454, 63);
        정수쓰기(첫구역, 458, 1024);
        verificar(new 기본분할영역표().Lectura(첫구역).size() == 1, "valor_per_defecte 분할 영역표");

        xarxa_capa capa_VALOR = new xarxa_capa();
        int[] CANTIDAD_RECIBIDA_COMPT = new int[1];
        capa_VALOR.registrar_se_usuari_dades_lliçó(7, (dades, Executa_2, durada_VALOR) -> CANTIDAD_RECIBIDA_COMPT[0]++);
        byte[] marc_INDEX = new byte[14 + 20 + 8];
        marc_INDEX[12] = 0x08;
        marc_INDEX[13] = 0x00;
        marc_INDEX[14] = 0x45;
        marc_INDEX[16] = 0;
        marc_INDEX[17] = 28;
        marc_INDEX[23] = 17;
        marc_INDEX[36] = 0;
        marc_INDEX[37] = 7;
        verificar(capa_VALOR.rebre_Ethernet(marc_INDEX) && CANTIDAD_RECIBIDA_COMPT[0] == 1, "usuari dades lliçó_VALOR distribuir_VALOR");
    }

    private static void 화면과시계시험() {
        caràcter_mostrar 화면 = new caràcter_mostrar();
        화면.Sortida("가나\n다");
        verificar(화면.문자(0, 0) == '가' && 화면.문자(0, 1) == '다', "문자 화면 Sortida");
        Rellotge Rellotge = new Rellotge(100);
        for (int INDEX = 0; INDEX < 10; INDEX++) {
            Rellotge.틱();
        }
        verificar(Rellotge.지난밀리초() == 100, "Rellotge 틱 CONVERT_VALOR");
    }

    private static void 정수쓰기(byte[] dades, int Posició, int VALOR) {
        dades[Posició] = (byte) VALOR;
        dades[Posició + 1] = (byte) (VALOR >>> 8);
        dades[Posició + 2] = (byte) (VALOR >>> 16);
        dades[Posició + 3] = (byte) (VALOR >>> 24);
    }

    private static void 짧은정수쓰기(byte[] dades, int Posició, int VALOR) {
        dades[Posició] = (byte) VALOR;
        dades[Posició + 1] = (byte) (VALOR >>> 8);
    }

    private static void verificar(boolean condició, String Nom) {
        if (!condició) {
            throw new AssertionError("error_VALOR: " + Nom);
        }
        transmetre_COMPT++;
        System.out.println("transmetre_VALOR: " + Nom);
    }
}
