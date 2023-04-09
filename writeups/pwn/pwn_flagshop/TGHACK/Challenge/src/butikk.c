#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#define LEN_PWD 32

int penger = 5;
char admin[] = "admin";
char pwd[LEN_PWD] = {0};

struct FLAG
{
    char navn[30];
    unsigned int pris;
    unsigned int antall;
};

struct FLAG vare_flag[3] = {{"CTF Flag", 100000, 1}, {"Norsk Flag", 5000, 10}, {"Svensk Flag", 5, 500}};

void banner(void)
{
    printf("Velkommen til flag butikken! Her kan du kjøpe litt forskjellige flag!\nVi har ikke så mange enda, men flere kommer så følg med!\n");
}

void meny(void)
{
    printf("Du har %d penger\n\n1. Kjøp flag\n2. Avslutt\n> ", penger);
}

void flag_meny(void)
{
    for(int i=0; i<sizeof(vare_flag)/sizeof(struct FLAG); i++)
    {
        printf("%d. %s - Antall: %d - Pris: %d\n", i+1, vare_flag[i].navn, vare_flag[i].antall, vare_flag[i].pris);
    }
    printf("> ");
}

void hemmelig_meny(void)
{
    char uname[LEN_PWD] = {0};
    char pass[LEN_PWD*2] = {0};
    getchar();
    printf("Brukernavn> ");
    fgets(uname, 10, stdin);
    printf("Passord> ");
    fgets(pass, LEN_PWD, stdin);
    if(strncmp(uname, admin, 5) == 0 && strncmp(pass, pwd, LEN_PWD) == 0)
    {
        system("/bin/sh");
    }
}

void kill_on_timeout(int sig) {
    if (sig == SIGALRM) {
        printf("[!] Anti DoS.");
        exit(0);
    }
}

void initialize(void)
{
    FILE * fp = fopen("/dev/urandom", "r");
    fread(&pwd, 1, LEN_PWD, fp);
    fclose(fp);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, kill_on_timeout);
    alarm(60);
}

void kjop_flag(int flag)
{
    flag--;
    unsigned int antall;
    printf("Hvor mange vil du ha?\n> ");
    if(scanf("%d", &antall) != 1)
    {
        printf("Ugyldig antall\n");
        return;
    }
    int total_pris = antall * vare_flag[flag].pris;
    printf("Total pris: %d\n", total_pris);
    if(total_pris <= penger)
    {
        printf("Du kjøpte %d for %d\n", antall, total_pris);
        penger = penger - total_pris;
        if(flag == 0)
        {
            FILE *fp = fopen("./flag.txt", "r");
            if(fp == NULL)
            {
                printf("Kunne ikke finne flag! Kontakt admin for å finne det.\n");
                exit(1);
            }
            char ch;
            while((ch = fgetc(fp)) != EOF)
            {
                putchar(ch);
            }
            fclose(fp);
        }
    }
    else
    {
        printf("Beklager, ikke nok penger :(\n");
    }
}

void main(void)
{
    unsigned int valg;
    int pris;
    initialize();
    banner();
    while(1)
    {
        meny();
        if(scanf("%d", &valg) == 1)
        {
            switch(valg)
            {
                case 1:
                {
                    flag_meny();
                    if(scanf("%d", &valg) != 1) continue;
                    if(valg > sizeof(vare_flag)/sizeof(struct FLAG) || valg < 1)
                    {
                        printf("Ugyldig valg!\n");
                        continue;
                    }
                    kjop_flag(valg);
                    break;
                }
                case 2:
                {
                    printf("Velkommen tilbake!\n");
                    exit(0);
                }
                case -1:
                {
                    hemmelig_meny();
                    break;
                }
                default:
                {
                    goto dno;
                    break;
                }
            }
        }
        else
        {
dno:
            printf("Skjønte ikke?!\n");
        }
    }

}