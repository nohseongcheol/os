/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "remoto_VALOR.h"
#include "criptografia_Suporte.h"
#include "Perfil.h"
#include "../rede_pilha/rede_pilha.h"
/* The allocator/PRNG module descriptors are part of this pinned port's ABI. */
#define ASSH_PV
#include <assh/assh_session.h>
#include <assh/assh_context.h>
#include <assh/assh_service.h>
#include <assh/assh_transport.h>
#include <assh/assh_userauth_server.h>
#include <assh/assh_connection.h>
#include <assh/assh_kex.h>
#include <assh/assh_key.h>
#include <assh/assh_sign.h>
#include <assh/assh_cipher.h>
#include <assh/assh_mac.h>
#include <assh/assh_compress.h>
#include <assh/assh_alloc.h>
#include <assh/assh_prng.h>
#include <assh/mod_builtin.h>
#include <assh/assh_event.h>
#include <string.h>
extern uintptr_t 보드밀리초(void);
extern uintptr_t 보드글자쓰기(uintptr_t);
static struct assh_context_s *contexto_VALOR;
static struct assh_session_s *conexão_e05f319b;
static struct assh_channel_s *Canal_entrada;
static int Estou_ouvindo_empresa=-1,par_VALOR=-1,인증됨,셸시작됨,comando_TIPO,encerrar_Estado=-1,닫을예정,inicialização_erro,shell_Esperando;
static uintptr_t conexão_time,재접속시각,fechamento_time;
static unsigned char entrada_linha[8192],saída_linha[65536];
static unsigned entrada_HEAD,entrada_CONT_NÚM,saída_HEAD,saída_CONT_NÚM,Anterior_saída;
static void 진단(const char *Word_SMS,unsigned VALOR) {
    while(*Word_SMS)보드글자쓰기(*Word_SMS++);
    char dígito_VALOR[12];unsigned número=0;do{dígito_VALOR[número++]='0'+VALOR%10;VALOR/=10;}while(VALOR);
    while(número)보드글자쓰기(dígito_VALOR[--número]);보드글자쓰기(10);
}
static assh_status_t Preparar_Memória(void *dados,void **Endereço,size_t Tamanho,enum assh_alloc_type_e Tipo_VALOR) {
    (void)dados;(void)Tipo_VALOR;
    if(!Tamanho){lançar_remoto(*Endereço);*Endereço=0;return ASSH_OK;}
    void *새주소=원격재할당(*Endereço,Tamanho);
    if(!새주소)return ASSH_ERR_MEM;*Endereço=새주소;return ASSH_OK;
}
static assh_status_t Preparar_aleatório(struct assh_context_s *dados,const struct assh_buffer_s *valor_gerador) {
    (void)dados;(void)valor_gerador;unsigned char testes[32];int resultado=remoto_aleatório(testes,sizeof(testes));memset(testes,0,sizeof(testes));
    return resultado?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t leitura_aleatório(struct assh_context_s *dados,uint8_t *resultado,size_t duração_VALOR,uint_fast8_t Tipo_VALOR) {
    (void)dados;(void)Tipo_VALOR;if(duração_VALOR>65536)return ASSH_ERR_CRYPTO;
    return remoto_aleatório(resultado,duração_VALOR)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void aleatório_encerrar(struct assh_context_s *dados){(void)dados;}
static const struct assh_prng_s aleatório_gerador={Preparar_aleatório,leitura_aleatório,aleatório_encerrar};
static void Close_conexão(void) {
    인증됨=셸시작됨=0;Canal_entrada=0;
    if(conexão_e05f319b)assh_session_release(conexão_e05f319b);conexão_e05f319b=0;
    if(par_VALOR>=0)Close_rede(par_VALOR);par_VALOR=-1;comando_TIPO=0;encerrar_Estado=-1;닫을예정=0;
    entrada_HEAD=entrada_CONT_NÚM=saída_HEAD=saída_CONT_NÚM=Anterior_saída=0;재접속시각=보드밀리초()+250;
}
int feed_remoto_entrada(const unsigned char *dados,unsigned número) {
    if(número>sizeof(entrada_linha)-entrada_CONT_NÚM)return -11;
    for(unsigned 순번=0;순번<número;순번++)entrada_linha[(entrada_HEAD+entrada_CONT_NÚM++)%sizeof(entrada_linha)]=dados[순번];return número;
}
int remoto_entrada(void) {
    if(!entrada_CONT_NÚM)return -1;int caractere_VALOR=entrada_linha[entrada_HEAD];entrada_HEAD=(entrada_HEAD+1)%sizeof(entrada_linha);entrada_CONT_NÚM--;return caractere_VALOR;
}
void remoto_saída(unsigned char caractere_VALOR) {
    if(!셸시작됨||닫을예정)return;
    unsigned Acrescentar_MODO=caractere_VALOR==10&&Anterior_saída!=13;
    if(saída_CONT_NÚM+1+Acrescentar_MODO>sizeof(saída_linha)){닫을예정=2;return;}
    if(Acrescentar_MODO)saída_linha[(saída_HEAD+saída_CONT_NÚM++)%sizeof(saída_linha)]=13;
    saída_linha[(saída_HEAD+saída_CONT_NÚM++)%sizeof(saída_linha)]=caractere_VALOR;Anterior_saída=caractere_VALOR;
}
uintptr_t Quadro_encerrar_remoto_comando(uintptr_t Estado_VALOR){if(셸시작됨&&comando_TIPO)encerrar_Estado=(int)Estado_VALOR;return 0;}
uintptr_t Quadro_remoto_aguarde(uintptr_t Estado_VALOR){shell_Esperando=Estado_VALOR!=0;return 0;}
static int Preparar_shell(void) {
    if(Estou_ouvindo_empresa>=0)return 0;
    if(!contexto_VALOR){
        assh_status_t erro=assh_context_create(&contexto_VALOR,ASSH_SERVER,Preparar_Memória,0,&aleatório_gerador,0);
        if(erro)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *método_MODO[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        erro=assh_algo_register(contexto_VALOR,ASSH_SAFETY_WEAK,método_MODO);
        if(!erro)erro=assh_service_register_va(contexto_VALOR,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *Chave_material=celular_Chave;
        if(!erro)erro=assh_key_load(contexto_VALOR,assh_context_keys(contexto_VALOR),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&Chave_material,sizeof(celular_Chave));
        if(erro){진단("SSH init error ",erro);assh_context_release(contexto_VALOR);contexto_VALOR=0;return -5;}
    }
    int porta_VALOR=Criar_soquete_empresa(1);if(porta_VALOR<0)return porta_VALOR;통신주소재사용(porta_VALOR);
    int resultado=NET_BIND(porta_VALOR,0,22);if(!resultado)resultado=NET_escutar(porta_VALOR);
    if(resultado<0){Close_rede(porta_VALOR);return resultado;}Estou_ouvindo_empresa=porta_VALOR;return 0;
}
uintptr_t Quadro_sombreamento(uintptr_t Tipo_VALOR,uintptr_t Acção) {
    if(Tipo_VALOR==1)return(uint32_t)visual_remoto_visor(Acção);
    if(Acção==0){Close_conexão();if(Estou_ouvindo_empresa>=0)Close_rede(Estou_ouvindo_empresa);Estou_ouvindo_empresa=-1;return 0;}
    if(Acção==1){inicialização_erro=Preparar_shell();return(uint32_t)inicialização_erro;}
    return(uint32_t)(Estou_ouvindo_empresa>=0?1:inicialização_erro);
}
void Preparar_remoto(void){inicialização_erro=Preparar_shell();visual_remoto_visor(1);}
static int 같은말(const struct assh_cbuffer_s *dados,const char *Word_SMS) {
    size_t duração_VALOR=strlen(Word_SMS);return dados->size==duração_VALOR&&!memcmp(dados->data,Word_SMS,duração_VALOR);
}
static int Terminal_solicitação(const struct assh_cbuffer_s *dados) {
    if(dados->size<24)return 0;
    const unsigned char *dados_cargo=dados->data;unsigned duração_VALOR=assh_load_u32(dados_cargo);
    if(duração_VALOR>128||dados->size<duração_VALOR+24)return 0;
    unsigned MODO_VALOR=assh_load_u32(dados_cargo+4+duração_VALOR+16);
    return MODO_VALOR<=2048&&dados->size==duração_VALOR+24+MODO_VALOR;
}
static void alça_solicitação(struct assh_event_request_s *Evento) {
    if(!인증됨||Evento->ch!=Canal_entrada||!Canal_entrada)return;
    if(같은말(&Evento->type,"pty-req")) {
        if(!셸시작됨&&Terminal_solicitação(&Evento->rq_data))Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(같은말(&Evento->type,"window-change")) {
        if(셸시작됨&&Evento->rq_data.size==16)Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(셸시작됨||!shell_Esperando)return;
    const unsigned char *comando=0;unsigned duração_VALOR=0;
    if(같은말(&Evento->type,"exec")) {
        if(Evento->rq_data.size<4)return;
        duração_VALOR=assh_load_u32(Evento->rq_data.data);
        if(!duração_VALOR||duração_VALOR>2048||Evento->rq_data.size!=duração_VALOR+4)return;
        comando=Evento->rq_data.data+4;
        for(unsigned 순번=0;순번<duração_VALOR;순번++)if(!comando[순번])return;
        comando_TIPO=1;
    }else if(!같은말(&Evento->type,"shell")||Evento->rq_data.size)return;
    if(sizeof(entrada_linha)-entrada_CONT_NÚM<duração_VALOR+2)return;
    const unsigned char 지움=21,끝=13;
    feed_remoto_entrada(&지움,1);if(duração_VALOR)feed_remoto_entrada(comando,duração_VALOR);feed_remoto_entrada(&끝,1);
    셸시작됨=1;Evento->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!comando_TIPO){const char *LEIAME_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*LEIAME_eb81d7d9)remoto_saída(*LEIAME_eb81d7d9++);}
}
void 원격살피기(void) {
    원격화면살피기();
    if(Estou_ouvindo_empresa<0)return;
    uintptr_t AGORA_VALOR=보드밀리초();
    if(par_VALOR<0){if(AGORA_VALOR<재접속시각)return;par_VALOR=NET_aceitar(Estou_ouvindo_empresa);if(par_VALOR<0)return;
        conexão_time=AGORA_VALOR;assh_status_t erro=assh_session_create(contexto_VALOR,&conexão_e05f319b);
        if(erro){conexão_e05f319b=0;진단("SSH session error ",erro);Close_conexão();return;}}
    if((!인증됨&&AGORA_VALOR-conexão_time>30000)||닫을예정==2||(닫을예정&&AGORA_VALOR>=fechamento_time)){Close_conexão();return;}
    if(Canal_entrada&&셸시작됨&&!닫을예정) {
        if(saída_CONT_NÚM){size_t número=sizeof(saída_linha)-saída_HEAD;if(número>saída_CONT_NÚM)número=saída_CONT_NÚM;if(número>2048)número=2048;
            assh_status_t erro=assh_channel_data(Canal_entrada,saída_linha+saída_HEAD,&número);
            if(!erro){saída_HEAD=(saída_HEAD+número)%sizeof(saída_linha);saída_CONT_NÚM-=número;}
            else if(erro!=ASSH_NO_DATA){Close_conexão();return;}
        }
        if(encerrar_Estado>=0&&!saída_CONT_NÚM){unsigned char Estado_VALOR[4];assh_store_u32(Estado_VALOR,(uint32_t)encerrar_Estado);
            if(assh_request(conexão_e05f319b,Canal_entrada,"exit-status",11,Estado_VALOR,4,0)||assh_channel_eof(Canal_entrada)||assh_channel_close(Canal_entrada)) {Close_conexão();return;}
            닫을예정=1;fechamento_time=AGORA_VALOR+3000;
        }
    }
    for(unsigned SEQUÊNCIA_VALOR=0;SEQUÊNCIA_VALOR<16;SEQUÊNCIA_VALOR++) {
        struct assh_event_s Evento;
        if(!assh_event_get(conexão_e05f319b,&Evento,AGORA_VALOR/1000)){Close_conexão();return;}
        assh_status_t erro=ASSH_OK;int 쉬기=0,desconectar_empresa=0;
        switch(Evento.id) {
        case ASSH_EVENT_READ: {
            int número=NET_leitura(par_VALOR,Evento.transport.read.buf.data,Evento.transport.read.buf.size);
            if(número>0)Evento.transport.read.transferred=número;
            else if(número==-11)쉬기=1;else desconectar_empresa=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int número=NET_gravar(par_VALOR,Evento.transport.write.buf.data,Evento.transport.write.buf.size);
            if(número>0)Evento.transport.write.transferred=número;
            else if(número==-11)쉬기=1;else desconectar_empresa=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            Evento.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(Evento.userauth_server.methods.retries>3)Evento.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *dados=&Evento.userauth_server.password;
            if(같은말(&dados->username,"user")&&dados->password.size<=256&&!dados->new_password.size) {
                unsigned char resumo_VALOR[32];remoto_resumo(dados->password.data,dados->password.size,resumo_VALOR);
                unsigned 차이=0;for(unsigned 순번=0;순번<32;순번++)차이|=resumo_VALOR[순번]^shell_senha_resumo[순번];memset(resumo_VALOR,0,32);
                if(!차이)dados->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: 인증됨=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *dados=&Evento.connection.channel_open;
            if(인증됨&&!Canal_entrada&&shell_Esperando&&같은말(&dados->type,"session")&&!dados->rq_data.size) {
                dados->reply=ASSH_CONNECTION_REPLY_SUCCESS;dados->pkt_size=4096;
                dados->win_size=-1;Canal_entrada=dados->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: alça_solicitação(&Evento.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *dados=&Evento.connection.channel_data;
            if(!셸시작됨||dados->ch!=Canal_entrada||dados->ext){desconectar_empresa=1;break;}
            unsigned número=dados->data.size;if(número>sizeof(entrada_linha)-entrada_CONT_NÚM)número=sizeof(entrada_linha)-entrada_CONT_NÚM;
            for(unsigned 순번=0;순번<número;순번++)if(dados->data.data[순번]==4){encerrar_Estado=0;número=순번;dados->transferred=dados->data.size;break;}
            feed_remoto_entrada(dados->data.data,número);if(!dados->transferred)dados->transferred=número;
            if(!número&&encerrar_Estado<0)쉬기=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: Canal_entrada=0;셸시작됨=0;닫을예정=1;fechamento_time=AGORA_VALOR+1000;break;
        case ASSH_EVENT_SESSION_ERROR: 인증됨=셸시작됨=0;진단("SSH error ",Evento.session.error.code);desconectar_empresa=1;break;
        case ASSH_EVENT_DISCONNECT: desconectar_empresa=1;break;
        default: break;
        }
        assh_event_done(conexão_e05f319b,&Evento,erro);
        if(desconectar_empresa){Close_conexão();return;}if(쉬기)return;
    }
}
