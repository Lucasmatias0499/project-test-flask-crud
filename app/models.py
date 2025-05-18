import re


class User:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}
    
    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"    
    
    @staticmethod
    def validate_name(name):
        if not name:
            return "Nome é obrigatório."
        if not isinstance(name, str):
            return "Nome deve ser uma string."
        if len(name) < 2 or len(name) > 50:
            return "Nome deve ter entre 2 e 50 caracteres."
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', name):
            return "Nome deve conter apenas letras e espaços."
        return None