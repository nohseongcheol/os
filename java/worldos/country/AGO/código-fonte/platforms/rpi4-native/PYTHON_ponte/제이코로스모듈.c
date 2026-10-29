// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "호출.h"
#include "rede_ABI.h"
static intptr_t 결과검사(intptr_t resultado) { if (resultado < 0) mp_raise_OSError(-resultado); return resultado; }
static const char *caminho_argumento(mp_obj_t VALOR) {
    size_t item_CONT_NÚM; const char *caminho = mp_obj_str_get_data(VALOR, &item_CONT_NÚM);
    if (!item_CONT_NÚM || item_CONT_NÚM > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t 순번 = 0; 순번 < item_CONT_NÚM; 순번++) if (!caminho[순번]) mp_raise_OSError(MP_EINVAL);
    return caminho;
}
static mp_obj_t leitura_Arquivo(mp_obj_t Nome) {
    intptr_t identificador_de_arquivo = 결과검사(사용자호출(3, (uintptr_t)caminho_argumento(Nome), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t 비지역복귀;
    if (nlr_push(&비지역복귀) == 0) {
        size_t Tamanho = 결과검사(사용자호출(9, identificador_de_arquivo, 0, 0, 0, 0, 0));
        vstr_t dados; vstr_init_len(&dados, Tamanho);
        intptr_t resultado = 사용자호출(2, identificador_de_arquivo, (uintptr_t)dados.buf, Tamanho, 0, 0, 0);
        결과검사(resultado); dados.len = resultado;
        mp_obj_t VALOR = mp_obj_new_bytes_from_vstr(&dados);
        nlr_pop(); 사용자호출(4, identificador_de_arquivo, 0, 0, 0, 0, 0); return VALOR;
    }
    사용자호출(4, identificador_de_arquivo, 0, 0, 0, 0, 0); nlr_jump(비지역복귀.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(Arquivo_Leitor_objeto, leitura_Arquivo);
static mp_obj_t leitura_STDIN(mp_obj_t 한도) {
    mp_int_t Tamanho=mp_obj_get_int(한도);
    if(Tamanho<0||Tamanho>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t dados; vstr_init_len(&dados,Tamanho);
    intptr_t item_CONT_NÚM=사용자호출(2,0,(uintptr_t)dados.buf,Tamanho,0,0,0);
    if(item_CONT_NÚM<0) { vstr_clear(&dados); 결과검사(item_CONT_NÚM); }
    dados.len=item_CONT_NÚM; return mp_obj_new_bytes_from_vstr(&dados);
}
static MP_DEFINE_CONST_FUN_OBJ_1(STDIN_Leitor_objeto, leitura_STDIN);
static mp_obj_t gravar_Arquivo(mp_obj_t Nome, mp_obj_t Conteúdo_VALOR) {
    const char *caminho = caminho_argumento(Nome);
    mp_buffer_info_t dados; mp_get_buffer_raise(Conteúdo_VALOR, &dados, MP_BUFFER_READ);
    if (dados.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t identificador_de_arquivo = 결과검사(사용자호출(3, (uintptr_t)caminho, 577, 0, 0, 0, 0));
    intptr_t entrada_CONT_NÚM_8f7753a1 = 사용자호출(1, identificador_de_arquivo, (uintptr_t)dados.buf, dados.len, 0, 0, 0);
    사용자호출(4, identificador_de_arquivo, 0, 0, 0, 0, 0); return mp_obj_new_int(결과검사(entrada_CONT_NÚM_8f7753a1));
}
static MP_DEFINE_CONST_FUN_OBJ_2(Arquivo_Writer_objeto, gravar_Arquivo);
static mp_obj_t remover_Arquivo(mp_obj_t Nome) { 결과검사(사용자호출(11, (uintptr_t)caminho_argumento(Nome), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(파일지우기객체, remover_Arquivo);
static mp_obj_t Paint_retângulo(size_t item_CONT_NÚM, const mp_obj_t *argumento_MATRIZ) {
    (void)item_CONT_NÚM; unsigned 첫째값[5]; for (unsigned 순번 = 0; 순번 < 5; 순번++) 첫째값[순번] = mp_obj_get_int(argumento_MATRIZ[순번]);
    결과검사(tela_retângulo(첫째값[0], 첫째값[1], 첫째값[2], 첫째값[3], 첫째값[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(retângulo_objeto, 5, 5, Paint_retângulo);
static mp_obj_t leitura_tela_dimensionar(void) {
    mp_obj_t Tamanho[2] = {mp_obj_new_int(결과검사(화면너비읽기())), mp_obj_new_int(결과검사(leitura_tela_altura()))};
    return mp_obj_new_tuple(2, Tamanho);
}
static MP_DEFINE_CONST_FUN_OBJ_0(tela_dimensionar_objeto, leitura_tela_dimensionar);
static mp_obj_t 화면입력기다리기(void) { return mp_obj_new_int(결과검사(화면키기다리기())); }
static MP_DEFINE_CONST_FUN_OBJ_0(tela_aguarde_objeto, 화면입력기다리기);
static mp_obj_t Relógio_VALOR(void) { return mp_obj_new_int_from_uint(사용자호출(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(Relógio_objeto, Relógio_VALOR);
static mp_obj_t UDP_abrir(mp_obj_t número_da_porta) {
    int dados_cargo = mp_obj_get_int(número_da_porta); if (dados_cargo < 0 || dados_cargo > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t identificador_de_arquivo = 결과검사(사용자호출(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dados_cargo); 첫째값.sin_addr.s_addr = 0;
    intptr_t resultado = 사용자호출(33, identificador_de_arquivo, (uintptr_t)&첫째값, sizeof(첫째값), 0, 0, 0);
    if (resultado < 0) { 사용자호출(4, identificador_de_arquivo, 0, 0, 0, 0, 0); 결과검사(resultado); }
    return mp_obj_new_int(identificador_de_arquivo);
}
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_abrir_OBJ, UDP_abrir);
static mp_obj_t UDP_enviar(mp_obj_t identificador_de_arquivo, mp_obj_t número_da_porta, mp_obj_t Conteúdo_VALOR) {
    int dados_cargo = mp_obj_get_int(número_da_porta); if (dados_cargo < 1 || dados_cargo > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dados; mp_get_buffer_raise(Conteúdo_VALOR, &dados, MP_BUFFER_READ);
    struct pk_sockaddr_in 첫째값 = {0}; 첫째값.sin_family = AF_INET; 첫째값.sin_port = pk_htons(dados_cargo); 첫째값.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(결과검사(사용자호출(34, mp_obj_get_int(identificador_de_arquivo), (uintptr_t)dados.buf, dados.len, 0, (uintptr_t)&첫째값, sizeof(첫째값))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(UDP_enviar_OBJ, UDP_enviar);
static uint32_t leitura_endereço_na_Internet(mp_obj_t VALOR) {
    size_t duração_VALOR; const char *texto=mp_obj_str_get_data(VALOR,&duração_VALOR);
    unsigned em_dia_cargo=0; uint32_t Endereço=0;
    for(unsigned 부분=0;부분<4;부분++) {
        unsigned VALOR=0,dígito_CONT_NÚM=0;
        while(em_dia_cargo<duração_VALOR&&texto[em_dia_cargo]>='0'&&texto[em_dia_cargo]<='9') {
            VALOR=VALOR*10+texto[em_dia_cargo++]-'0'; if(++dígito_CONT_NÚM>3||VALOR>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!dígito_CONT_NÚM)mp_raise_OSError(MP_EINVAL);
        Endereço=Endereço<<8|VALOR;
        if(부분<3&&(em_dia_cargo>=duração_VALOR||texto[em_dia_cargo++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(em_dia_cargo!=duração_VALOR)mp_raise_OSError(MP_EINVAL);
    return Endereço;
}
static mp_obj_t 전문주소전송(size_t entrada_CONT_NÚM_8f7753a1, const mp_obj_t *argumento_MATRIZ) {
    (void)entrada_CONT_NÚM_8f7753a1; uint32_t Endereço=leitura_endereço_na_Internet(argumento_MATRIZ[1]);
    int número_da_porta=mp_obj_get_int(argumento_MATRIZ[2]);if(número_da_porta<1||número_da_porta>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t dados;mp_get_buffer_raise(argumento_MATRIZ[3],&dados,MP_BUFFER_READ);
    struct pk_sockaddr_in meta={0};meta.sin_family=AF_INET;meta.sin_port=pk_htons(número_da_porta);meta.sin_addr.s_addr=pk_htonl(Endereço);
    return mp_obj_new_int(결과검사(사용자호출(34,mp_obj_get_int(argumento_MATRIZ[0]),(uintptr_t)dados.buf,dados.len,0,(uintptr_t)&meta,sizeof(meta))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(전문주소전송객체,4,4,전문주소전송);
static mp_obj_t 전문수신(mp_obj_t identificador_de_arquivo) {
    unsigned char dados[512]; struct pk_sockaddr_in par_VALOR; pk_socklen_t duração_dados = sizeof(par_VALOR);
    intptr_t Tamanho = 결과검사(사용자호출(35, mp_obj_get_int(identificador_de_arquivo), (uintptr_t)dados, 512, 0, (uintptr_t)&par_VALOR, (uintptr_t)&duração_dados));
    mp_obj_t 값들[2] = {mp_obj_new_bytes(dados, Tamanho), MP_OBJ_NEW_SMALL_INT(pk_htons(par_VALOR.sin_port))};
    return mp_obj_new_tuple(2, 값들);
}
static MP_DEFINE_CONST_FUN_OBJ_1(전문수신객체, 전문수신);
static mp_obj_t UDP_Close(mp_obj_t identificador_de_arquivo) { 결과검사(사용자호출(4, mp_obj_get_int(identificador_de_arquivo), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(UDP_Close_OBJ, UDP_Close);
static mp_obj_t abrir_fluxo(void) {
    return mp_obj_new_int(결과검사(사용자호출(32,malha_Família,fluxo_rede,fluxo_protocolo_de_transporte,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(흐름열기객체,abrir_fluxo);
static mp_obj_t Conexão_fluxo(mp_obj_t empresa,mp_obj_t email_SMS,mp_obj_t ÍNDICE) {
    int número_da_porta=mp_obj_get_int(ÍNDICE); if(número_da_porta<1||número_da_porta>65535)mp_raise_OSError(MP_EINVAL);
    struct malha_soquete_email Endereço={0}; Endereço.email_Família=malha_Família;
    Endereço.número_da_porta=망차례짧은수(número_da_porta); Endereço.endereço_na_Internet.email_VALOR=rede_inteiro(leitura_endereço_na_Internet(email_SMS));
    결과검사(사용자호출(37,mp_obj_get_int(empresa),(uintptr_t)&Endereço,sizeof(Endereço),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(fluxo_Conector_objeto,Conexão_fluxo);
static mp_obj_t leitura_fluxo(mp_obj_t empresa,mp_obj_t 한도) {
    int duração_VALOR=mp_obj_get_int(한도); if(duração_VALOR<1||duração_VALOR>512)mp_raise_OSError(MP_EINVAL);
    unsigned char dados[512];
    intptr_t item_CONT_NÚM=결과검사(사용자호출(2,mp_obj_get_int(empresa),(uintptr_t)dados,duração_VALOR,0,0,0));
    return mp_obj_new_bytes(dados,item_CONT_NÚM);
}
static MP_DEFINE_CONST_FUN_OBJ_2(fluxo_Leitor_objeto,leitura_fluxo);
static mp_obj_t gravar_fluxo(mp_obj_t empresa,mp_obj_t Conteúdo_VALOR) {
    mp_buffer_info_t dados; mp_get_buffer_raise(Conteúdo_VALOR,&dados,MP_BUFFER_READ);
    return mp_obj_new_int(결과검사(사용자호출(1,mp_obj_get_int(empresa),(uintptr_t)dados.buf,dados.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fluxo_Writer_objeto,gravar_fluxo);
static mp_obj_t 잠시기다리기(mp_obj_t valor_temporal) {
    결과검사(사용자호출(17,mp_obj_get_int(valor_temporal),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(aguarde_objeto,잠시기다리기);
static mp_obj_t entrada_Tipo(mp_obj_t Nome) {
    return mp_obj_new_int(결과검사(사용자호출(18,(uintptr_t)caminho_argumento(Nome),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(entrada_Tipo_objeto,entrada_Tipo);
static mp_obj_t Criar_Diretório(mp_obj_t Nome) {
    결과검사(사용자호출(18,(uintptr_t)caminho_argumento(Nome),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(Diretório_autor_objeto,Criar_Diretório);
static mp_obj_t remover_Diretório(mp_obj_t Nome) {
    결과검사(사용자호출(18,(uintptr_t)caminho_argumento(Nome),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(폴더지우기객체,remover_Diretório);
static const mp_rom_map_elem_t 모듈이름목록[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&흐름열기객체) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&fluxo_Conector_objeto) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&fluxo_Leitor_objeto) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&fluxo_Writer_objeto) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&aguarde_objeto) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&entrada_Tipo_objeto) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&Diretório_autor_objeto) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&폴더지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&STDIN_Leitor_objeto) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&Arquivo_Leitor_objeto) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&Arquivo_Writer_objeto) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&파일지우기객체) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&retângulo_objeto) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&tela_dimensionar_objeto) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&tela_aguarde_objeto) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&Relógio_objeto) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&UDP_abrir_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&UDP_enviar_OBJ) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&전문주소전송객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&전문수신객체) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&UDP_Close_OBJ) },
};
static MP_DEFINE_CONST_DICT(모듈전역목록, 모듈이름목록);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&모듈전역목록 };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
