TARGET=qs
OBJ=$(TARGET:%=%.o)
SRC=$(OBJ:%.o=%.c)
DEPEND=.depend

all: $(TARGET)

$(TARGET): $(OBJ)
	gcc -o $@ $^

%.o: %.c
	gcc -c $<

clean:
	rm -fr rm-food $(TARGET) $(OBJ) $(DEPEND)

depend:
	gcc -E -MM $(SRC) > $(DEPEND)

install:
	cp -i $(TARGET) /usr/local/bin

uninstall:
	rm -f /usr/local/bin/$(TARGET)

-include $(DEPEND)
