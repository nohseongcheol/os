#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void సిద్ధం_చేయు_నెట్_వర్క్(void);
void 통신망살피기(void);
int 통신끝점만들기(int టైప్_చేయండి_వర్గం);
int 망주소묶기(int ఫైలు_నిర్వాహకం, uint32_t ఇమెయిల్, unsigned పోర్ట్_సంఖ్య);
int 연결기다리기(int ఫైలు_నిర్వాహకం);
void 통신주소재사용(int ఫైలు_నిర్వాహకం);
int 망연결하기(int ఫైలు_నిర్వాహకం, uint32_t ఇమెయిల్, unsigned పోర్ట్_సంఖ్య);
int 망연결받기(int ఫైలు_నిర్వాహకం);
int 통신읽기(int ఫైలు_నిర్వాహకం, void *డేటా, unsigned 개수);
int 통신쓰기(int ఫైలు_నిర్వాహకం, const void *డేటా, unsigned 개수);
int 전문보내기(int ఫైలు_నిర్వాహకం, const void *డేటా, unsigned 개수, uint32_t ఇమెయిల్, unsigned పోర్ట్_సంఖ్య);
int 전문받기(int ఫైలు_నిర్వాహకం, void *డేటా, unsigned 개수);
unsigned నెట్_వర్క్_పోర్ట్_సంఖ్య(int ఫైలు_నిర్వాహకం);
unsigned పియర్_పోర్ట్_సంఖ్య(int ఫైలు_నిర్వాహకం);
uint32_t 상대통신주소(int ఫైలు_నిర్వాహకం);
void మూసివేయి_నెట్_వర్క్(int ఫైలు_నిర్వాహకం);
int ఫైలు_బదిలీ_నియంత్రణ(int చర్య);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ప్రవేశం_మూల్యం, unsigned సూచీ);
int నిర్మితీకరించు_నెట్_వర్క్(unsigned చర్య, uint32_t ఇమెయిల్, uint32_t నిర్ధారకం_మూల్యం, uint32_t ప్రవేశద్వారం_మూల్యం);
int 응답시험시작(uint32_t ఇమెయిల్, unsigned క్రమం_మూల్యం);
int 응답시험읽기(unsigned ప్రవేశం_మూల్యం);
#endif
