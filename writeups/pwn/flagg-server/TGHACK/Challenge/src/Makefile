LDFLAGS = -lssl -lcrypto

binexp: main.o crypto.o
	$(CC) $(LDFLAGS) -o $@ $?

.PHONY: clean
clean:
	rm -f binexp main.o crypto.o