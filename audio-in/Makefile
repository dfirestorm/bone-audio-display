#
# Programs
#
all:	analogInMatrix

analogInMatrix:	analogInMatrix.o
	$(CC) $(LDFLAGS) -o $@ $^


#
# Objects
#

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm analogInMatrix