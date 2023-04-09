#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char pin[] = "6105";
char code[4] = {'0', '0', '0', '0'};

void open_door(void)
{
    pin[0] = pin[0]^0x1;
    pin[1] = pin[1]^0x2;
    pin[2] = pin[2]^0x3;
    pin[3] = pin[3]^0x4;
    if(strncmp(pin, code, 4) == 0)
    {
        FILE* fd = fopen("./flag.txt", "r");
        if(fd == NULL)
        {
            printf("Could not locate flag file! Contact admins to find it!\n");
            exit(1);
        }
        char ch;
        while((ch = fgetc(fd)) != EOF)
        {
            putchar(ch);
        }
        exit(0);
    }
    else
    {
        printf("Sorry incorrect PIN\n");
        exit(1);
    }
}
int direction = -1; 
char number = '0';
int idx = 0;
void rotate(void)
{
    number = number + direction;
    if(number > '9')
        number = '0';
    else if(number < '0')
        number = '9';
    code[idx] = number;
}
void rotate_left(void)
{
    if(direction != -1)
    {
        direction = -1;
        idx = (idx + 1) %4;
    }
    rotate();
}
void rotate_right(void)
{
    if(direction != 1)
    {
        direction = 1;
        idx = (idx + 1) % 4;
    }
    rotate();
}
void initialize(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void main(void)
{
    initialize();
    char passphrase[32] = {0};
    printf("Foran deg er en stor hvelv-dør, midt på er hjulet som sitter fast, men den står på tallet %c.\n", number);
    printf("Til høyre er et display med en touchpad som lyser opp\n");
    printf("Please supply passphrase: ");
    fgets(passphrase, 320, stdin);
}