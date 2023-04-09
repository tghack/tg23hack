struct userinfo_t {
    char pubkey[512];
    char is_authenticated;
    int client_fd;
};

typedef struct userinfo_t userinfo_t;
