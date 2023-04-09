#include "crypto.h"

#include <openssl/err.h>

EVP_PKEY* load_public_key(const char* key_str) {
    EVP_PKEY* pkey = NULL;
    BIO* bio = NULL;

    //Libcrypto wants these public key things
    int buffer_size = strlen(key_str) + 100;
    char* openssl_buffer = calloc(buffer_size, 1);
    sprintf(openssl_buffer, "-----BEGIN PUBLIC KEY-----\n%s\n-----END PUBLIC KEY-----\n", key_str);

    // Create a new memory BIO and write the key string to it
    bio = BIO_new_mem_buf(openssl_buffer, -1);
    if (!bio) {
        perror("Failed to create BIO");
        return NULL;
    }

    // Load the public key from the BIO
    pkey = PEM_read_bio_PUBKEY(bio, NULL, NULL, NULL);
    if (!pkey) {
        perror("Failed to load public key from BIO");
        BIO_free_all(bio);
        return NULL;
    }
    RSA *rsa_key = EVP_PKEY_get1_RSA(pkey);
    int key_length = RSA_size(rsa_key);
    RSA_free(rsa_key);
    if(key_length != 2048/8) {
        BIO_free_all(bio);
        free(openssl_buffer);
        printf("Invalid key size: %d...\n", key_length);
        return NULL;
    }

    // Free memory and clean up
    BIO_free_all(bio);
    free(openssl_buffer);

    return pkey;
}

char* encrypt_buffer(const char* buffer, int buffer_len, EVP_PKEY* pkey) {
    EVP_PKEY_CTX* ctx = EVP_PKEY_CTX_new(pkey, NULL);
    if (!ctx) {
        fprintf(stderr, "Error creating EVP_PKEY_CTX\n");
        exit(EXIT_FAILURE);
    }
    if (EVP_PKEY_encrypt_init(ctx) <= 0) {
        fprintf(stderr, "Error initializing EVP_PKEY_encrypt_init\n");
        exit(EXIT_FAILURE);
    }
    if (EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING) <= 0) {
        fprintf(stderr, "Error setting RSA padding\n");
        exit(EXIT_FAILURE);
    }

    size_t enc_len = 0;
    if (EVP_PKEY_encrypt(ctx, NULL, &enc_len, buffer, buffer_len) <= 0) {
        fprintf(stderr, "Error getting encrypted length\n");
        exit(EXIT_FAILURE);
    }
    char* encrypted = (char*) malloc(enc_len);

    if (EVP_PKEY_encrypt(ctx, (unsigned char*) encrypted, &enc_len, (unsigned char*) buffer, buffer_len) <= 0) {
        fprintf(stderr, "Error encrypting data\n");
        int error = ERR_get_error();
        char* error_str = ERR_error_string(error, NULL);
        if(error_str) {
            printf("%s\n", error_str);
        }
        exit(EXIT_FAILURE);
    }

    BIO* bio = BIO_new(BIO_s_mem());
    BIO* b64 = BIO_new(BIO_f_base64());
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
    bio = BIO_push(b64, bio);
    BIO_write(bio, encrypted, enc_len);
    BIO_flush(bio);
    BUF_MEM* bptr;
    BIO_get_mem_ptr(bio, &bptr);
    char* enc_buffer = (char*) malloc(bptr->length + 1);
    memcpy(enc_buffer, bptr->data, bptr->length);
    enc_buffer[bptr->length] = '\0';
    BIO_free_all(bio);
    free(encrypted);
    EVP_PKEY_CTX_free(ctx);
    return enc_buffer;
}