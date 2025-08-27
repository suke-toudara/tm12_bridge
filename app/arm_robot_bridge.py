#!/usr/bin/env python3

from pyModbusTCP.client import ModbusClient
import struct

class ArmRobot:
    def __init__(self):
        self.connect()

    def connect(self):
        self.client = ModbusClient(
            host='192.168.88.7',
            port=502,
            unit_id=1,
            timeout=30.0,
            auto_open=True,
            auto_close=False
        )
        # print("connect arm robot")

    def get_state(self):
        error = self.client.read_discrete_inputs(bit_addr=7201, bit_nb=1)
        print("error :" ,error)
        emergency_stop = self.client.read_input_registers(reg_addr=7218, reg_nb=1)
        print("emergency_stop : ",emergency_stop)

    """
    robot task
    """
    def task_start(self):
        q = self.client.write_single_coil(bit_addr=7103, bit_value=True)

    def task_pause(self):
        rq = self.client.write_single_coil(bit_addr=7108, bit_value=True)
    
    def task_stop(self):
        q = self.client.write_single_coil(bit_addr=7105, bit_value=True)

    def emergency_stop(self):
        rq = self.client.write_single_coil(bit_addr=7105, bit_value=True)

    def set_task_speed(self, speed: int):
        self.client.write_single_register(reg_addr=7101, reg_value=speed)

    def set_executing_task(self, task_id: int):
        self.client.write_single_register(reg_addr=7100, reg_value=task_id)

    """
    ロボット状態取得
    """
    @property # ライトカラー
    def set_light_color(self):     
        light_color = self.client.read_input_registers(reg_addr=7332, reg_nb=1)
        return light_color[0]        
    
    @property # 温度              
    def temp(self):
        temp = self.client.read_input_registers(reg_addr=7340, reg_nb=2)
        return self.byte2float(temp,len(temp)) 

    @property # 電圧
    def voltage(self):
        voltage = self.client.read_input_registers(reg_addr=7342, reg_nb=2)
        return self.byte2float(voltage,len(voltage)) 
    
    @property # 電力
    def power(self):
        power = self.client.read_input_registers(reg_addr=7344, reg_nb=2)
        return self.byte2float(power,len(power)) 
    
    @property # 電流
    def current(self):
        current = self.client.read_input_registers(reg_addr=7346, reg_nb=2)
        return self.byte2float(current,len(current)) 
    
    @property # エラーコード
    def get_error_code(self):
        pass

    @property # モード
    def M_A_mode(self):
        mode = self.client.read_input_registers(reg_addr=7102, reg_nb=1)
        return "Auto" if mode[0] == 1 else "Manual"

    @property #　エラー
    def error(self):
        error = self.client.read_discrete_inputs(bit_addr=7201, bit_nb=1)
        return error[0]
    
    @property # 緊急停止
    def emergency_stop(self):
        emergency_stop = self.client.read_input_registers(reg_addr=7218, reg_nb=1)
        return True if emergency_stop[0] == 1 else False

    @property 
    def status(self):
        status = self.client.read_input_registers(reg_addr=7215, reg_nb=1)
        if status == None:
            print(f"読み取りエラー: {status}")
            return None
        if status[0] == 0:
            return "通常"
        elif status[0] == 1:
            return "SOS"
        elif status[0] == 2:
            return "エラー"
        elif status[0] == 3:
            return "回復モード"
        elif status[0] == 4:
            return "STO"
    
    @property
    def project_run(self):
        project_run = self.client.read_discrete_inputs(bit_addr=7202, bit_nb=1)
        return project_run[0]
    @property
    def project_edit(self):
        project_edit = self.client.read_discrete_inputs(bit_addr=7203, bit_nb=1)
        return project_edit[0]
    
    @property
    def project_pause(self):
        project_pause = self.client.read_discrete_inputs(bit_addr=7204, bit_nb=1)
        return project_pause[0]
    
    @property
    def current_project(self):
        regs = self.client.read_input_registers(7701, 99)
        if regs:
            byte_array = bytearray()
            for r in regs:
                byte_array.extend(r.to_bytes(2, byteorder="big"))  
            # C文字列なので、\0 で終端
            project_name = byte_array.split(b"\x00", 1)[0].decode("ascii", errors="ignore")
        return project_name

    """
    検証中
    """    
    def set_project(self, project: str):
        # 文字列に終端\0を追加
        chars = list(project + "\0")
        # print("chars:", chars)
        # ASCIIコードに変換
        ascii_codes = [ord(c) for c in chars]
        # print("ascii:", ascii_codes)

        regs = []
        for i in range(0, len(ascii_codes), 2):
            hi = ascii_codes[i]                                     # 1文字目（上位バイト）
            lo = ascii_codes[i+1] if i+1 < len(ascii_codes) else 0  # 2文字目（下位バイト）
            val = (hi << 8) | lo
            regs.append(val)

        print("regs:", regs)


        # 複数レジスタに一括書き込み（7701番地から）
        result = self.client.write_multiple_registers(7701, regs)
        return result

    def disable_auto_mode(self):
        self.client.write_single_coil(7210,False)
    

    def enable_auto_mode(self):
        self.client.write_single_coil(7210,True)

    @property
    def auto_mode(self):
        auto_mode = self.client.read_discrete_inputs(bit_addr=7210, bit_nb=1)
        return auto_mode[0]
    """
    utils
    """
    def byte2float(self,regs,byte_len):
        if byte_len == 2 :
           # レジスタ配列 → バイト列（ビッグエンディアンと仮定）
            b = struct.pack('>HH', regs[0], regs[1])
            # 4バイト → float32 に変換
            val = struct.unpack('>f', b)[0]
            return val