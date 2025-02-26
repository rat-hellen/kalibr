import binascii
def lrc(buffer):
    cs = 0 
    i = 1
    while i < len(buffer):
        a = int(buffer[i:i+2],16)
        cs = (cs+a) & 0xFF
        i+=2

    #lrc = (((cs ^ 0xFF) + 1) & 0xFF)
    #lrc_1 = binascii.hexlify(lrc.to_bytes(1,'big')).upper()

    lrc_alt = ~cs + 1
    lrc_alt = binascii.hexlify(lrc_alt.to_bytes(2,'big', signed=True)).upper()
    #print(lrc_1, lrc_alt[-2:])
    return (lrc_alt[-2:])
    
    #lrc = (((cs ^ 0xFF) + 1) & 0xFF)
    #return binascii.hexlify(lrc.to_bytes(1,'big')).upper()
