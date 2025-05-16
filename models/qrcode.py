from datetime import datetime
import uuid
import random
import string

class QRCode:
    def __init__(self, id=None, local_name=None, auth_user=None, auth_password=None, 
                 fixed_address=None, contract_number=None, taxi_central_code=None, 
                 background_image=None, created_at=None, address_lat=None, address_lng=None,
                 address_city=None, address_number=None, address_cep=None):
        self.id = id or str(uuid.uuid4())
        self.local_name = local_name
        self.auth_user = auth_user
        self.auth_password = auth_password
        self.fixed_address = fixed_address
        self.contract_number = contract_number
        self.taxi_central_code = taxi_central_code
        self.background_image = background_image
        self.created_at = created_at or datetime.now()
        self.booking_hash_prefix = self._generate_random_string(32)
        
        # Novos campos para geocodificação
        self.address_lat = address_lat
        self.address_lng = address_lng
        self.address_city = address_city
        self.address_number = address_number
        self.address_cep = address_cep
    
    def _generate_random_string(self, length):
        """Gera uma string aleatória de caracteres alfanuméricos"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def to_dict(self):
        """Converte o objeto para um dicionário"""
        return {
            'id': self.id,
            'local_name': self.local_name,
            'auth_user': self.auth_user,
            'auth_password': self.auth_password,
            'fixed_address': self.fixed_address,
            'contract_number': self.contract_number,
            'taxi_central_code': self.taxi_central_code,
            'background_image': self.background_image,
            'booking_hash_prefix': self.booking_hash_prefix,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'address_lat': self.address_lat,
            'address_lng': self.address_lng,
            'address_city': self.address_city,
            'address_number': self.address_number,
            'address_cep': self.address_cep
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto QRCode a partir de um dicionário"""
        if not data:
            return None
            
        qrcode = cls(
            id=data.get('id'),
            local_name=data.get('local_name'),
            auth_user=data.get('auth_user'),
            auth_password=data.get('auth_password'),
            fixed_address=data.get('fixed_address'),
            contract_number=data.get('contract_number'),
            taxi_central_code=data.get('taxi_central_code'),
            background_image=data.get('background_image'),
            created_at=data.get('created_at'),
            address_lat=data.get('address_lat'),
            address_lng=data.get('address_lng'),
            address_city=data.get('address_city'),
            address_number=data.get('address_number'),
            address_cep=data.get('address_cep')
        )
        
        # Restaurar o booking_hash_prefix se existir
        if 'booking_hash_prefix' in data:
            qrcode.booking_hash_prefix = data['booking_hash_prefix']
            
        return qrcode
