#ifndef yerel_ağ_Başlık
#define yerel_ağ_Başlık
#include <stdint.h>
#include <stddef.h>
void Hazırlan_ağ(void);
void 통신망살피기(void);
int açmak_yuva_uç_nokta(int TÜR_alan);
int NET_BIND(int dosya_tanıtıcısı, uint32_t ADRES, unsigned bağlantı_noktası_numarası);
int NET_dinlemek(int dosya_tanıtıcısı);
void 통신주소재사용(int dosya_tanıtıcısı);
int NET_bağla(int dosya_tanıtıcısı, uint32_t ADRES, unsigned bağlantı_noktası_numarası);
int NET_kabul_etmek(int dosya_tanıtıcısı);
int 통신읽기(int dosya_tanıtıcısı, void *veri, unsigned öğe_BAĞ_DEĞ_SAY);
int NET_yazma(int dosya_tanıtıcısı, const void *veri, unsigned öğe_BAĞ_DEĞ_SAY);
int göndermek_veri_birimi(int dosya_tanıtıcısı, const void *veri, unsigned öğe_BAĞ_DEĞ_SAY, uint32_t ADRES, unsigned bağlantı_noktası_numarası);
int almak_veri_birimi(int dosya_tanıtıcısı, void *veri, unsigned öğe_BAĞ_DEĞ_SAY);
unsigned ağ_bağlantı_noktası_numarası(int dosya_tanıtıcısı);
unsigned eş_bağlantı_noktası_numarası(int dosya_tanıtıcısı);
uint32_t NET_eş_ADRES(int dosya_tanıtıcısı);
void Kapat_ağ(int dosya_tanıtıcısı);
int dosya_aktarımı_denetim(int Eylem);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned girdi_değer, unsigned Dizin);
int yapılandırmak_ağ(unsigned Eylem, uint32_t ADRES, uint32_t maske_değer, uint32_t ağ_geçidi_değer);
int Start_cevap_test(uint32_t ADRES, unsigned düzen_değer);
int 응답시험읽기(unsigned girdi_değer);
#endif
