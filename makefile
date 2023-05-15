program: program.o
	ld -m elf_i386 -o program program.o

program.o: program.asm
	nasm -f elf32 -F dwarf -g program.asm
