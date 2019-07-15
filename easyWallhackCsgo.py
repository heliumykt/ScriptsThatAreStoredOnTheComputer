from pymem import process, Pymem, exception

dwEntityList = (0x4D04B04)
dwGlowObject = (0x5245018)
m_iGlowIndex = (0xA40C)

pm = Pymem("csgo.exe")
client = process.module_from_name(pm.process_handle, "client_panorama.dll").lpBaseOfDll

while True:
    try:
        for i in range(0, 11):
            glow_player_glow_index = pm.read_int(pm.read_int(client + dwEntityList + i * 0x10) + m_iGlowIndex)
            pm.write_float((pm.read_int(client + dwGlowObject) + ((glow_player_glow_index * 0x38) + 0x8)), float(1))
            pm.write_float((pm.read_int(client + dwGlowObject) + ((glow_player_glow_index * 0x38) + 0x10)), float(1))
            pm.write_int((pm.read_int(client + dwGlowObject) + ((glow_player_glow_index * 0x38) + 0x24)), 1)
        
    except exception.MemoryReadError: 
        pass
        