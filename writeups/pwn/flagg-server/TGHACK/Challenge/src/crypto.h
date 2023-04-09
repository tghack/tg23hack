#include <openssl/bio.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/rand.h>

EVP_PKEY* load_public_key(const char* key_str);
char* encrypt_buffer(const char* buffer, int buffer_len, EVP_PKEY* pub_key);