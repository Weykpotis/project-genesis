#include <stdio.h>
#include <locale.h>
#include <stdlib.h>
#include <unistd.h>
#include "SDL2/SDL.h"
unsigned long long PC;
unsigned long long meml[97280];
unsigned long long reg[256];
unsigned long long ports[7];
unsigned long long instnum;
int i;
int j;
FILE* files;
SDL_Window* window;
SDL_Surface* surface;
SDL_Event* event;
unsigned char lb[8];
unsigned char tarr[8];
unsigned char tarra[9];
unsigned long long a;
unsigned long long b;
long long c;
long long d;
unsigned char cols[4] = {0, 85, 170, 255};
unsigned char scancodes[285];
void brncom(unsigned char reg1, unsigned char reg2, unsigned long long brn, unsigned char mode) {
	brn=brn-1;
	c=(long long int) reg[reg1];
	d=(long long int) reg[reg2];
	switch (mode) {
		case 0:
			if (c==d) {
	        		PC=brn;
			}
			break;
		case 1:
			if (c!=d) {
				PC=brn;
			}
			break;
	    	case 2:
		      	if (c<d) {
			        PC=brn;
			}
			break;
  	  	case 3:
 		     	if (c>d) {
  				PC=brn;
			}
			break;
   	 	case 4:
 		     	if (c<=d) {
 				PC=brn;
			}
			break;
    		case 5:
  			if (c>=d) {
 				PC=brn;
			}
			break;
	}
}
int main(int argc, char *argv[]) {
	for (i=0;i<285;i++) {
		scancodes[i]=0;
	}
	for (i=4;i<30;i++) {
		scancodes[i]=i+61;
	}
	for (i=30;i<39;i++) {
		scancodes[i]=i+19;
	}
	scancodes[39]=48;
	scancodes[40]=13;
	scancodes[41]=27;
	scancodes[42]=8;
	scancodes[43]=9;
	scancodes[44]=32;
	scancodes[45]=45;
	scancodes[46]=61;
	scancodes[47]=91;
	scancodes[48]=93;
	scancodes[49]=92;
	scancodes[51]=59;
	scancodes[52]=39;
	scancodes[53]=96;
	scancodes[54]=44;
	scancodes[55]=46;
	scancodes[56]=47;
	scancodes[57]=128;
	for (i=58;i<70;i++) {
		scancodes[i]=i+78;
	}
	scancodes[76]=127;
	scancodes[79]=161;
	scancodes[80]=163;
	scancodes[81]=162;
	scancodes[82]=160;
	scancodes[84]=178;
	scancodes[85]=42;
	scancodes[86]=174;
	scancodes[87]=43;
	scancodes[88]=13;
	for (i=89;i<98;i++) {
		scancodes[i]=i+76;
	}
	scancodes[98]=164;
	scancodes[99]=177;
	scancodes[100]=179;
	scancodes[103]=175;
	for (i=104;i<118;i++) {
		scancodes[i]=i+44;
	}
	scancodes[133]=176;
	scancodes[182]=40;
	scancodes[183]=41;
	scancodes[184]=123;
	scancodes[185]=125;
	scancodes[186]=9;
	scancodes[187]=8;
	scancodes[195]=94;
	scancodes[196]=37;
	scancodes[197]=60;
	scancodes[198]=62;
	scancodes[199]=38;
	scancodes[201]=95;
	scancodes[203]=58;
	scancodes[204]=35;
	scancodes[205]=32;
	scancodes[206]=64;
	scancodes[207]=33;
	scancodes[224]=132;
	scancodes[225]=129;
	scancodes[226]=130;
	scancodes[227]=134;
	scancodes[228]=133;
	scancodes[229]=129;
	scancodes[230]=131;
	scancodes[231]=135;
	setlocale(LC_ALL, "en_US.UTF-8");
	files=fopen("/Applications/AssemblyOS/dt.aod", "r+b");
	PC=0;
	instnum=0;
	for (i=0;i<7;i++) {
		ports[i]=0;
	}
	for (i=0;i<256;i++) {
		reg[i]=0;
	}
	for (i=0;i<97280;i++) {
		meml[i]=0;
	}
	SDL_SetMainReady();
	SDL_Init(SDL_INIT_TIMER|SDL_INIT_VIDEO|SDL_INIT_AUDIO);
	window=SDL_CreateWindow("AOS-CVM", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 320, 240, SDL_WINDOW_INPUT_GRABBED|SDL_WINDOW_FULLSCREEN);
	surface=SDL_GetWindowSurface(window);
	while (1) {
		printf("%llu %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu %llu \n", PC, reg[240], reg[241], reg[242], reg[243], reg[244], reg[245], reg[246], reg[247], reg[248], reg[249], reg[250], reg[251], reg[252], reg[253], reg[254]);
		fseek(files, 8*PC, SEEK_SET);
		fread(lb, 1, 8, files);
		for (i=0;i<8;i++) {
			tarra[i]=0;
		}
		switch (lb[0]) {
			case 0:
				reg[lb[1]]=meml[reg[lb[2]]];
				break;
			case 1:
				meml[reg[lb[2]]]=reg[lb[1]];
				break;
			case 2:
				reg[lb[1]]=meml[(lb[2]<<16)+(lb[3]<<8)+(lb[4])];
				break;
			case 3:
				meml[(lb[2]<<16)+(lb[3]<<8)+(lb[4])]=reg[lb[1]];
				break;
			case 4:
				fseek(files, 8*reg[lb[1]], SEEK_SET);
				fread(tarr, 1, 8, files);
				for (i=0;i<8;i++) {
					meml[reg[lb[2]]]+=tarr[i]<<(56-8*i);
				}
				break;
			case 5:
				fseek(files, 8*reg[lb[1]], SEEK_SET);
				for (i=0;i<8;i++) {
					tarr[i]=(meml[reg[lb[2]]]>>(8*i))%(1<<8);
				}
				fwrite(tarr, 1, 8, files);
				break;
			case 6:
				fseek(files, 8*(((lb[1]<<24)+(lb[2]<<16)+(lb[3]<<8)+(lb[4]))%4294967296), SEEK_SET);
				fread(tarr, 1, 8, files);
				for (i=0;i<8;i++) {
					meml[(lb[5]<<16)+(lb[6]<<8)+(lb[7])]+=tarr[i]<<(56-8*i);
				}
				break;
			case 7:
				fseek(files, 8*(((lb[1]<<24)+(lb[2]<<16)+(lb[3]<<8)+(lb[4]))%4294967296), SEEK_SET);
				for (i=0;i<8;i++) {
					tarr[i]=(meml[(lb[5]<<16)+(lb[6]<<8)+(lb[7])]>>(8*i))%256;
				}
				fwrite(tarr, 1, 8, files);
				break;
			case 8:
				meml[reg[lb[2]]]=ports[lb[1]];
				break;
			case 9:
				ports[lb[1]]=meml[reg[lb[2]]];
				break;
			case 10:
				meml[(lb[2]<<16)+(lb[3]<<8)+(lb[4])]=ports[lb[1]];
				break;
			case 11:
				ports[lb[1]]=meml[(lb[2]<<16)+(lb[3]<<8)+(lb[4])];
				break;
			case 12:
				reg[lb[1]]++;
				break;
			case 13:
				reg[lb[2]]=reg[lb[1]];
				break;
			case 14:
				brncom(lb[1], lb[2], ((lb[3]<<24)+(lb[4]<<16)+(lb[5]<<8)+(lb[6]))%4294967296, lb[7]);
				break;
			case 15:
				sleep(5);
				SDL_Quit();
				printf("%llu %s", instnum, " instructions executed.");
				fclose(files);
				exit(0);
				break;
			case 16:
				if (lb[3]==0) {
					reg[lb[1]]=reg[lb[1]]>>reg[lb[2]];
				}
				if (lb[3]==1) {
					reg[lb[1]]=reg[lb[1]]<<reg[lb[2]];
				}
				break;
			case 17:
				reg[lb[3]]=reg[lb[1]]^reg[lb[2]];
				break;
			case 18:
				reg[lb[3]]=reg[lb[1]]+reg[lb[2]];
				break;
			case 19:
				reg[lb[2]]=-reg[lb[1]];
				break;
			case 20:
				reg[lb[3]]=reg[lb[1]]*reg[lb[2]];
				break;
			case 21:
				if (lb[7]>15) {
					brncom(lb[1], lb[2], PC-((lb[3]<<24)+(lb[4]<<16)+(lb[5]<<8)+(lb[6]))%4294967296, lb[7]-16);
				}
				else {
					brncom(lb[1], lb[2], PC+((lb[3]<<24)+(lb[4]<<16)+(lb[5]<<8)+(lb[6]))%4294967296, lb[7]);
				}
				break;
			case 22:
				break;
			case 23:
				break;
			case 24:
				a=reg[lb[1]]%reg[lb[2]];
				b=reg[lb[1]]/reg[lb[2]];
				reg[lb[4]]=a;
				reg[lb[3]]=b;
				break;
			case 25:
				a=((lb[3]<<24)+(lb[4]<<16)+(lb[5]<<8)+(lb[6]));
				b=reg[lb[1]];
				if (lb[2]==0) {
					reg[lb[1]]=b-(b%4294967296)+(a%4294967296);
				}
				if (lb[2]==1) {
					reg[lb[1]]=(b%4294967296)+(4294967296*(a%4294967296));
				}
				break;
			case 26:
				brncom(lb[1], lb[2], reg[lb[3]], lb[4]);
				break;
			case 27:
				reg[lb[2]]=reg[lb[1]]+(((lb[3]<<24)+(lb[4]<<16)+(lb[5]<<8)+lb[6])%4294967296);
				break;
			case 28:
				reg[lb[2]]=reg[lb[1]]*(((lb[3]<<24)+(lb[4]<<16)+(lb[5]<<8)+lb[6])%4294967296);
				break;
			case 29:
				a=reg[lb[1]]%(((lb[2]<<24)+(lb[3]<<16)+(lb[4]<<8)+lb[5])%4294967296);
				b=reg[lb[1]]/(((lb[2]<<24)+(lb[3]<<16)+(lb[4]<<8)+lb[5])%4294967296);
				reg[lb[7]]=a;
				reg[lb[6]]=b;
				break;
			case 30:
				a=(((lb[2]<<24)+(lb[3]<<16)+(lb[4]<<8)+lb[5])%4294967296)%reg[lb[1]];
				b=(((lb[2]<<24)+(lb[3]<<16)+(lb[4]<<8)+lb[5])%4294967296)/reg[lb[1]];
				reg[lb[7]]=a;
				reg[lb[6]]=b;
				break;
			case 31:
				if (lb[4]>15) {
					brncom(lb[1], lb[2], PC-reg[lb[3]], lb[4]-16);
				}
				else {
					brncom(lb[1], lb[2], PC+reg[lb[3]], lb[4]);
				}
				break;
			case 32:
				if (lb[6]==0) {
					reg[lb[1]]=reg[lb[1]]>>(((lb[2]<<24)+(lb[3]<<16)+(lb[4]<<8)+lb[5])%4294967296);
				}
				if (lb[6]==1) {
					reg[lb[1]]=reg[lb[1]]<<(((lb[2]<<24)+(lb[3]<<16)+(lb[4]<<8)+lb[5])%4294967296);
				}
				break;
			case 33:
				a=(reg[lb[1]]%256)<<(lb[6]*8);
				b=(reg[lb[1]]%256)>>(72-(lb[6]*8));
				meml[(lb[2]<<16)+(lb[3]<<8)+lb[4]]=(a>>(lb[6]*8))+(b>>(72-(lb[6]*8)))+(lb[5]);
				break;
			case 34:
				b=(meml[(lb[2]<<16)+(lb[3]<<8)+lb[4]])>>(64-(lb[6]*8));
				reg[lb[1]]=b%256;
				break;
			case 35:
				a=(reg[lb[1]]%256)<<(lb[3]*8);
				b=(reg[lb[1]]%256)>>(72-(lb[3]*8));
				meml[reg[lb[2]]]=(a>>(lb[3]*8))+(b>>(72-(lb[3]*8)))+(lb[5]);
				break;
			case 36:
				b=(meml[reg[lb[2]]])>>(64-(reg[lb[3]]*8));
				reg[lb[1]]=b%256;
				break;
			default:
				printf("INVALID INSTRUCTION! CPU ERROR!");
				SDL_Quit();
				fclose(files);
				exit(1);
		}
		PC++;
		instnum++;
		reg[255]=PC;
		if (!((lb[0]-11)*(lb[0]-9))) {
			if (ports[0]!=0) {
				for (i=0;i<8;i++) {
					tarra[i]=((ports[0]-(1<<63))>>(8*i))%256;
				}
				printf("%s", tarra);
				ports[0]=0;
			}
			if (ports[1]==7090194570149783924) {
				ports[1]=0;
				scanf("%8s", tarra);
				ports[2]=0;
				for (i=0;i<8;i++) {
					ports[2]+=tarra[i]<<(56-8*i);
				}
			}
			if (ports[3]!=0) {
				SDL_memset(surface->pixels+4*(((ports[3]>>40)%65536)+(surface->w*((ports[3]>>24)%65536)))+2, cols[ports[3]>>62], 1);
				SDL_memset(surface->pixels+4*(((ports[3]>>40)%65536)+(surface->w*((ports[3]>>24)%65536)))+1, cols[(ports[3]>>60)%4], 1);
				SDL_memset(surface->pixels+4*(((ports[3]>>40)%65536)+(surface->w*((ports[3]>>24)%65536))), cols[(ports[3]>>58)%4], 1);
				SDL_memset(surface->pixels+4*(((ports[3]>>40)%65536)+(surface->w*((ports[3]>>24)%65536)))+3, cols[(ports[3]>>56)%4], 1);
				ports[3]=0;
			}
			if (ports[4]==7090194570149783924) {
				SDL_UpdateWindowSurface(window);
				ports[4]=0;
			}
			if (ports[6]==7311142570156320116) {
				i=0;
				while (SDL_PollEvent(event)) {
					i++;
					switch (event->type) {
						case SDL_KEYDOWN:
							ports[5]=(5<<60)+(scancodes[event->key.keysym.scancode]<<48);
							break;
						case SDL_KEYUP:
							ports[5]=(1<<62)+(scancodes[event->key.keysym.scancode]<<48);
							break;
						case SDL_MOUSEMOTION:
							ports[5]=5<<61;
							if (event->motion.xrel<0) {
								ports[5]+=(1<<58)+(event->motion.xrel<<40);
							}
							else {
								ports[5]+=(event->motion.xrel<<40);
							}
							if (event->motion.yrel<0) {
								ports[5]+=(1<<59)+(event->motion.yrel<<24);
							}
							else {
								ports[5]+=(event->motion.yrel<<24);
							}
							break;
						case SDL_MOUSEBUTTONUP:
							ports[5]=1<<63;
							switch (event->button.button) {
								case SDL_BUTTON_LEFT:
									break;
								case SDL_BUTTON_MIDDLE:
									ports[5]+=1<<58;
									break;
								case SDL_BUTTON_RIGHT:
									ports[5]+=1<<59;
									break;
							}
							break;
						case SDL_MOUSEBUTTONDOWN:
							ports[5]=9<<60;
							switch (event->button.button) {
								case SDL_BUTTON_LEFT:
									break;
								case SDL_BUTTON_MIDDLE:
									ports[5]+=1<<58;
									break;
								case SDL_BUTTON_RIGHT:
									ports[5]+=1<<59;
									break;
							}
							break;
						case SDL_MOUSEWHEEL:
							ports[5]=3<<62;
							if (event->wheel.x<0) {
								ports[5]+=(1<<58)+(event->wheel.x<<40);
							}
							else {
								ports[5]+=(event->wheel.x<<40);
							}
							if (event->wheel.y<0) {
								ports[5]+=(1<<59)+(event->wheel.y<<24);
							}
							else {
								ports[5]+=(event->wheel.y<<24);
							}
							break;
						default:
							i-=1;
					}
				}
				if (!i) {
					ports[5]=0;
				}
			}
		}
	}
}
