#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/wait.h>

#include "main.h"
#include "crypto.h"

#define MAX_BUFFER_SIZE 1024*16 // 16 kb


void write_to_user(userinfo_t *user, const char* buffer) {
    char* to_send = malloc(strlen(buffer) + 1);
    memcpy(to_send, buffer, strlen(buffer) + 1);
    // Should we attempt to encrypt?
    if(strlen(user->pubkey)) {
        // TODO if we make the task harder, we should probably just do the EVP conversion later
        EVP_PKEY* pub_key = load_public_key(user->pubkey);
        char* encrypted_data = encrypt_buffer(buffer, strlen(buffer), pub_key);
        if(!encrypted_data) {
            printf("Error encrypting data\n");
            goto cleanup;
        }

        free(to_send);
        int encrypted_output_size = strlen(encrypted_data) + 100 + sizeof("Encrypted: ");
        to_send = malloc(encrypted_output_size);
        sprintf(to_send, "Encrypted response: %s\n", encrypted_data);
        free(encrypted_data);
        EVP_PKEY_free(pub_key);
    }
    if (write(user->client_fd, to_send, strlen(to_send)) < 0) {
        perror("Write failed");
        close(user->client_fd);
        free(to_send);
        exit(EXIT_FAILURE);
    }
cleanup:
    free(to_send);
}

const char* ARNE_IP = "185.80.182.112"; // Gathering.org

void handle_client(int client_fd, struct sockaddr_in client_addr, char* flag) {
    char buffer[MAX_BUFFER_SIZE];

    // Set up user state
    userinfo_t* user_info = (userinfo_t*) malloc(sizeof(userinfo_t));
    user_info->is_authenticated = 0;
    user_info->client_fd = client_fd;
    memset(user_info->pubkey, 0, sizeof(user_info->pubkey));

    const char* ip = inet_ntoa(client_addr.sin_addr);
    if(!strcmp(ip, ARNE_IP)) {
        printf("Arne speaking!\n");
        user_info->is_authenticated = 1;
    }

    printf("Accepted new connection from %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

    while (1) {
        memset(buffer, 0, MAX_BUFFER_SIZE);
        if (write(user_info->client_fd, "> ", 2) < 0) {
            perror("Write failed");
            close(user_info->client_fd);
            exit(EXIT_FAILURE);
        }
        int num_bytes = read(client_fd, buffer, MAX_BUFFER_SIZE);

        if (num_bytes == 0) {
            // Connection closed by the client
            close(client_fd);
            break;
        } else if (num_bytes < 0) {
            perror("Read failed");
            close(client_fd);
            free(user_info);
            exit(EXIT_FAILURE);
        }

        printf("Received %d bytes from %s:%d\n", num_bytes, inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        if(!strncmp("PING", buffer, strlen("PING"))) {
            char* response = "PONG\n";
            write_to_user(user_info, response);
        } else if(!strncmp("HELP", buffer, strlen("HELP"))) {
            char* response = "B-gjengen safe flag fetcher 2000 help\n\tPING - Returns PONG\n\tHELP - Returns B-gjengen safe flag fetcher 2000 help\n\tFLAG - Safely returns a flag\n\tENCRYPT [pubkey] - Allows you to specify a public key.\n";
            write_to_user(user_info, response);
        } else if(!strncmp("EXIT", buffer, strlen("EXIT"))) {
            char* response = "Bye bye!";
            write_to_user(user_info, response);
        } else if(!strncmp("ENCRYPT ", buffer, strlen("ENCRYPT "))) {
            char* pubkey_location = &buffer[strlen("ENCRYPT ")];
            printf("Start: %p\n", pubkey_location);

            char* pubkey_end = strchr(pubkey_location, '\n');
            if(pubkey_end) {
                *pubkey_end = 0;
            }
            pubkey_end = strchr(pubkey_location, '\r');
            if(pubkey_end) {
                *pubkey_end = 0;
            }
            
            int pubkey_len = strlen(pubkey_location);

            printf("Got pubkey: \"%s\" (len %d)\n", pubkey_location, pubkey_len);
            // Ensure the pkey parses
            EVP_PKEY* pkey = load_public_key(pubkey_location);
            if(!pkey) {
                char* err = "Invalid key!\n";
                write_to_user(user_info, err);
                continue;
            }   
            EVP_PKEY_free(pkey);

            // Vulnerable
            memcpy(&user_info->pubkey, pubkey_location, pubkey_len);
            char* response = "Encryption set successfully\n";
            write_to_user(user_info, response);
        } else if(!strncmp("FLAG", buffer, strlen("FLAG"))) {
            if(user_info->is_authenticated) {
                char* response = calloc(128 + strlen(flag), 1);
                sprintf(response, "Congratulations. The flag: %s\n", flag);

                printf("User %s:%d successfully got the flag\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
                write_to_user(user_info, response);
                free(response);
            } else {
                char* response = "You are not allowed to get the flag\n";
                write_to_user(user_info, response);
            }
        } else {
            char* response = "?unknown command, type HELP for help\n";
            write_to_user(user_info, response);
        }

        memset(buffer, 0, MAX_BUFFER_SIZE);
    }

    free(user_info);
    printf("Connection closed by %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
}

int main(int argc, char *argv[]) {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    int opt = 1;
    int port;
    char* flag;

    if (argc != 3) {
        printf("Usage: %s [flag] [port]\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    port = atoi(argv[2]);
    flag = argv[1];

    // Create a socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Set socket options
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt failed");
        exit(EXIT_FAILURE);
    }

    // Bind socket to a specific address and port
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Listening on port %d...\n", port);

    // Accept incoming connections and handle them in separate processes
    while (1) {
        if ((client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_addr_len)) < 0) {
            perror("Accept failed");
            exit(EXIT_FAILURE);
        }

        // Fork a new process to handle the client
        pid_t pid = fork();

        if (pid == -1) {
            perror("Fork failed");
            close(client_fd);
            continue;
        } else if (pid == 0) {
            // Child process handles the client
            close(server_fd);
            handle_client(client_fd, client_addr, flag);
            exit(EXIT_SUCCESS);
        } else {
            // Parent process continues listening for incoming connections
            close(client_fd);
            signal(SIGCHLD, SIG_IGN); // Avoid zombies
        }
    }

    return 0;
}