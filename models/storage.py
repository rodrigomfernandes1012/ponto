import os
import json
from datetime import datetime

class QRCodeStorage:
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.ensure_storage_exists()
    
    def ensure_storage_exists(self):
        """Garante que o arquivo de armazenamento existe"""
        if not os.path.exists(os.path.dirname(self.storage_file)):
            os.makedirs(os.path.dirname(self.storage_file))
        
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)
    
    def save_qrcode(self, qrcode):
        """Salva um QRCode no armazenamento"""
        qrcodes = self.get_all_qrcodes()
        
        # Verifica se já existe um QRCode com este ID
        for i, existing in enumerate(qrcodes):
            if existing.get('id') == qrcode.id:
                qrcodes[i] = qrcode.to_dict()
                break
        else:
            # Se não existir, adiciona um novo
            qrcodes.append(qrcode.to_dict())
        
        # Salva a lista atualizada
        with open(self.storage_file, 'w') as f:
            json.dump(qrcodes, f, indent=2)
        
        return qrcode
    
    def get_qrcode_by_id(self, qrcode_id):
        """Busca um QRCode pelo ID"""
        from src.models.qrcode import QRCode
        
        qrcodes = self.get_all_qrcodes()
        for qrcode_data in qrcodes:
            if qrcode_data.get('id') == qrcode_id:
                return QRCode.from_dict(qrcode_data)
        
        return None
    
    def get_all_qrcodes(self):
        """Retorna todos os QRCodes armazenados"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def get_qrcodes_by_central(self, taxi_central_code):
        """Busca QRCodes pela sigla da central de táxi"""
        from src.models.qrcode import QRCode
        
        qrcodes = self.get_all_qrcodes()
        result = []
        
        for qrcode_data in qrcodes:
            if qrcode_data.get('taxi_central_code') == taxi_central_code:
                result.append(QRCode.from_dict(qrcode_data))
        
        return result
    
    def get_qrcodes_by_central_and_contract(self, taxi_central_code, contract_number):
        """Busca QRCodes pela sigla da central e número do contrato"""
        from src.models.qrcode import QRCode
        
        qrcodes = self.get_all_qrcodes()
        result = []
        
        for qrcode_data in qrcodes:
            if (qrcode_data.get('taxi_central_code') == taxi_central_code and 
                str(qrcode_data.get('contract_number')) == str(contract_number)):
                result.append(QRCode.from_dict(qrcode_data))
        
        return result
    
    def delete_qrcode(self, qrcode_id):
        """Remove um QRCode do armazenamento"""
        qrcodes = self.get_all_qrcodes()
        qrcodes = [q for q in qrcodes if q.get('id') != qrcode_id]
        
        with open(self.storage_file, 'w') as f:
            json.dump(qrcodes, f, indent=2)
        
        return True
