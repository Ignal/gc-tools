BUILDDIRS = bstw qs bf ook
SUBDIRS = scripts bstw qs bf ook

.PHONY all depend clean:
	for i in $(BUILDDIRS); do make -C $$i $@; done

.PHONY install uninstall:
	for i in $(SUBDIRS); do make -C $$i $@; done
