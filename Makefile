CC = gcc
INCPATHS = -I/usr/local/include
#macOS
#CFLAGS = -g -Wall -Xpreprocessor -fopenmp -lomp -std=c11 -O3 $(INCPATHS)
CFLAGS = -g -Wall -fopenmp -std=c11 -O3 $(INCPATHS)
LDLIBS = -lflint -lgmp -lmpfr -lm -lssl -lcrypto
LDPATH = -L/usr/local/lib

FHIPE = searchableencryption/fhipe
BUILD = $(FHIPE)/build
EXE = $(FHIPE)/gen_matrices

SRC = cryptorand.c gen_matrices.c

OBJPATHS = $(patsubst %.c,$(BUILD)/%.o, $(SRC))

all: $(OBJPATHS) $(EXE)

obj: $(OBJPATHS)


$(BUILD):
		mkdir -p $(BUILD)

$(BUILD)/%.o: $(FHIPE)/%.c | $(BUILD)
		$(CC) $(CFLAGS) -o $@ -c $<


$(EXE): $(OBJPATHS)
		$(CC) $(CFLAGS) -o $@ $(LDPATH) $(OBJPATHS) $(LDLIBS)

clean:
		rm -rf $(BUILD) $(EXE) *~

uninstall:
		make clean