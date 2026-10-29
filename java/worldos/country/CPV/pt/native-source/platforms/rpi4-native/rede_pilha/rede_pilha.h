#ifndef nativo_rede_Cabeçalho
#define nativo_rede_Cabeçalho
#include <stdint.h>
#include <stddef.h>
void Preparar_rede(void);
void 통신망살피기(void);
int Criar_soquete_empresa(int TIPO_área);
int NET_BIND(int identificador_de_arquivo, uint32_t Endereço, unsigned número_da_porta);
int NET_escutar(int identificador_de_arquivo);
void 통신주소재사용(int identificador_de_arquivo);
int NET_Conexão(int identificador_de_arquivo, uint32_t Endereço, unsigned número_da_porta);
int NET_aceitar(int identificador_de_arquivo);
int NET_leitura(int identificador_de_arquivo, void *dados, unsigned item_CONT_NÚM);
int NET_gravar(int identificador_de_arquivo, const void *dados, unsigned item_CONT_NÚM);
int enviar_datagrama(int identificador_de_arquivo, const void *dados, unsigned item_CONT_NÚM, uint32_t Endereço, unsigned número_da_porta);
int receber_datagrama(int identificador_de_arquivo, void *dados, unsigned item_CONT_NÚM);
unsigned rede_número_da_porta(int identificador_de_arquivo);
unsigned par_número_da_porta(int identificador_de_arquivo);
uint32_t NET_par_email(int identificador_de_arquivo);
void Close_rede(int identificador_de_arquivo);
int transferência_de_arquivo_visual(int Acção);
void 파일전송살피기(void);
uint32_t leitura_rede_Status(unsigned entrada_VALOR_962f286b, unsigned ÍNDICE);
int configurar_rede(unsigned Acção, uint32_t Endereço, uint32_t máscara_VALOR, uint32_t gateway_VALOR);
int START_réplica_teste(uint32_t Endereço, unsigned ordem_VALOR);
int leitura_réplica_teste(unsigned entrada_VALOR_962f286b);
#endif
